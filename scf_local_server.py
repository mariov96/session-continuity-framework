#!/usr/bin/env python3
"""
SCF Local Server
Handles communication between browser extension and local buildstate files
Provides web endpoint for universal context sync
"""

import asyncio
import json
import os
import sqlite3
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

import aiofiles
import aiohttp
from aiohttp import web, web_request
from aiohttp.web_response import Response
from aiohttp_cors import CorsConfig, setup as cors_setup

class SCFLocalServer:
    def __init__(self, port: int = 8765, workspace_root: Optional[str] = None):
        self.port = port
        self.workspace_root = Path(workspace_root or os.getcwd())
        self.buildstate_dir = self.workspace_root / "buildstate"
        self.db_path = self.workspace_root / "scf_web_sessions.db"
        
        # Ensure directories exist
        self.buildstate_dir.mkdir(exist_ok=True)
        
        # Initialize database
        self.init_database()
        
        print(f"🎼 SCF Local Server initializing...")
        print(f"   Workspace: {self.workspace_root}")
        print(f"   Buildstate: {self.buildstate_dir}")
        print(f"   Port: {self.port}")
    
    def init_database(self):
        """Initialize SQLite database for web sessions"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS web_sessions (
                id TEXT PRIMARY KEY,
                provider TEXT NOT NULL,
                title TEXT,
                url TEXT,
                start_time TEXT,
                last_activity TEXT,
                message_count INTEGER DEFAULT 0,
                insights_count INTEGER DEFAULT 0,
                decisions_count INTEGER DEFAULT 0,
                conversation_data TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS web_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                author TEXT,
                content TEXT,
                message_type TEXT,
                timestamp TEXT,
                element_id TEXT,
                FOREIGN KEY (session_id) REFERENCES web_sessions (id)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS buildstate_updates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                file_path TEXT,
                update_type TEXT,
                content TEXT,
                timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (session_id) REFERENCES web_sessions (id)
            )
        """)
        
        conn.commit()
        conn.close()
    
    async def health_check(self, request: web_request.Request) -> Response:
        """Health check endpoint"""
        return web.json_response({
            "status": "healthy",
            "version": "2.0",
            "workspace": str(self.workspace_root),
            "buildstate_files": len(list(self.buildstate_dir.glob("*.md"))),
            "timestamp": datetime.now().isoformat()
        })
    
    async def sync_conversation(self, request: web_request.Request) -> Response:
        """Main endpoint for syncing web LLM conversations"""
        try:
            data = await request.json()
            
            if data.get("action") != "sync_conversation":
                return web.json_response(
                    {"error": "Invalid action"}, 
                    status=400
                )
            
            conversation_data = data.get("data", {})
            
            # Process the conversation
            result = await self.process_conversation(conversation_data)
            
            return web.json_response({
                "success": True,
                "session_id": result["session_id"],
                "buildstate_updated": result["buildstate_updated"],
                "insights_extracted": result["insights_extracted"],
                "timestamp": datetime.now().isoformat()
            })
            
        except Exception as e:
            print(f"❌ Error syncing conversation: {e}")
            return web.json_response(
                {"error": str(e)}, 
                status=500
            )
    
    async def process_conversation(self, conversation_data: Dict) -> Dict:
        """Process incoming conversation data and update buildstate"""
        
        # Generate session ID
        session_id = f"{conversation_data.get('provider', 'unknown')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Store session in database
        await self.store_web_session(session_id, conversation_data)
        
        # Extract insights and decisions
        insights = self.extract_insights(conversation_data.get('messages', []))
        decisions = self.extract_decisions(conversation_data.get('messages', []))
        
        # Update buildstate files
        buildstate_updated = await self.update_buildstate_from_web(
            session_id, 
            conversation_data, 
            insights, 
            decisions
        )
        
        return {
            "session_id": session_id,
            "buildstate_updated": buildstate_updated,
            "insights_extracted": len(insights) + len(decisions)
        }
    
    async def store_web_session(self, session_id: str, conversation_data: Dict):
        """Store web session data in database"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        messages = conversation_data.get('messages', [])
        insights_count = len([m for m in messages if m.get('type') == 'insight'])
        decisions_count = len([m for m in messages if m.get('type') == 'decision'])
        
        # Insert session
        cursor.execute("""
            INSERT OR REPLACE INTO web_sessions 
            (id, provider, title, url, start_time, last_activity, message_count, 
             insights_count, decisions_count, conversation_data)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            session_id,
            conversation_data.get('provider', 'unknown'),
            conversation_data.get('title', 'Untitled'),
            conversation_data.get('url', ''),
            conversation_data.get('startTime', datetime.now().isoformat()),
            datetime.now().isoformat(),
            len(messages),
            insights_count,
            decisions_count,
            json.dumps(conversation_data)
        ))
        
        # Insert messages
        for message in messages:
            cursor.execute("""
                INSERT INTO web_messages 
                (session_id, author, content, message_type, timestamp, element_id)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                session_id,
                message.get('author', 'unknown'),
                message.get('content', ''),
                message.get('type', 'message'),
                message.get('timestamp', datetime.now().isoformat()),
                message.get('element_id', '')
            ))
        
        conn.commit()
        conn.close()
    
    def extract_insights(self, messages: List[Dict]) -> List[Dict]:
        """Extract insights from conversation messages"""
        insights = []
        
        for message in messages:
            content = message.get('content', '').lower()
            
            # Look for insight patterns
            insight_patterns = [
                "i learned that",
                "key insight",
                "this means",
                "important point",
                "conclusion:",
                "takeaway:",
                "discovered that"
            ]
            
            if any(pattern in content for pattern in insight_patterns):
                insights.append({
                    "content": message.get('content', ''),
                    "author": message.get('author', 'unknown'),
                    "timestamp": message.get('timestamp', ''),
                    "type": "insight"
                })
        
        return insights
    
    def extract_decisions(self, messages: List[Dict]) -> List[Dict]:
        """Extract decisions from conversation messages"""
        decisions = []
        
        for message in messages:
            content = message.get('content', '').lower()
            
            # Look for decision patterns
            decision_patterns = [
                "i'll",
                "i will",
                "let's",
                "we should",
                "decision:",
                "going with",
                "plan to",
                "next step"
            ]
            
            if any(pattern in content for pattern in decision_patterns):
                decisions.append({
                    "content": message.get('content', ''),
                    "author": message.get('author', 'unknown'),
                    "timestamp": message.get('timestamp', ''),
                    "type": "decision"
                })
        
        return decisions
    
    async def update_buildstate_from_web(self, session_id: str, conversation_data: Dict, insights: List[Dict], decisions: List[Dict]) -> bool:
        """Update buildstate files with web conversation data"""
        
        try:
            # Determine buildstate file name
            provider = conversation_data.get('provider', 'web')
            title = conversation_data.get('title', 'conversation')
            
            # Clean title for filename
            clean_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
            clean_title = clean_title.replace(' ', '_').lower()
            
            filename = f"web_{provider}_{clean_title}_{datetime.now().strftime('%Y%m%d')}.md"
            filepath = self.buildstate_dir / filename
            
            # Generate buildstate content
            content = self.generate_buildstate_content(
                session_id, 
                conversation_data, 
                insights, 
                decisions
            )
            
            # Write buildstate file
            async with aiofiles.open(filepath, 'w', encoding='utf-8') as f:
                await f.write(content)
            
            # Log update in database
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO buildstate_updates 
                (session_id, file_path, update_type, content)
                VALUES (?, ?, ?, ?)
            """, (
                session_id,
                str(filepath),
                "web_conversation_sync",
                content[:1000] + "..." if len(content) > 1000 else content
            ))
            conn.commit()
            conn.close()
            
            print(f"✅ Buildstate updated: {filepath}")
            return True
            
        except Exception as e:
            print(f"❌ Error updating buildstate: {e}")
            return False
    
    def generate_buildstate_content(self, session_id: str, conversation_data: Dict, insights: List[Dict], decisions: List[Dict]) -> str:
        """Generate buildstate content from web conversation"""
        
        provider = conversation_data.get('provider', 'web')
        title = conversation_data.get('title', 'Web Conversation')
        url = conversation_data.get('url', '')
        messages = conversation_data.get('messages', [])
        
        content = f"""# Web LLM Session: {title}

## Session Metadata
- **Provider**: {provider}
- **URL**: {url}
- **Session ID**: {session_id}
- **Start Time**: {conversation_data.get('startTime', 'Unknown')}
- **Messages**: {len(messages)}
- **Insights**: {len(insights)}
- **Decisions**: {len(decisions)}
- **Synced**: {datetime.now().isoformat()}

## Context Summary
This buildstate was automatically generated from a web LLM conversation. It captures key insights, decisions, and context that can be applied to local development work.

"""

        # Add insights section
        if insights:
            content += "## 🔍 Key Insights\n\n"
            for i, insight in enumerate(insights, 1):
                content += f"### Insight {i}\n"
                content += f"**Author**: {insight['author']}\n\n"
                content += f"{insight['content']}\n\n"
                content += f"*Timestamp: {insight['timestamp']}*\n\n"
        
        # Add decisions section
        if decisions:
            content += "## ✅ Decisions Made\n\n"
            for i, decision in enumerate(decisions, 1):
                content += f"### Decision {i}\n"
                content += f"**Author**: {decision['author']}\n\n"
                content += f"{decision['content']}\n\n"
                content += f"*Timestamp: {decision['timestamp']}*\n\n"
        
        # Add conversation context
        content += "## 💬 Conversation Context\n\n"
        
        # Include last few meaningful messages
        meaningful_messages = [
            msg for msg in messages[-10:] 
            if len(msg.get('content', '')) > 50
        ]
        
        for msg in meaningful_messages:
            author_emoji = "🤖" if msg.get('author') == 'assistant' else "👤"
            content += f"**{author_emoji} {msg.get('author', 'Unknown')}**:\n\n"
            content += f"{msg.get('content', '')}\n\n"
            content += "---\n\n"
        
        # Add integration notes
        content += """## 🔄 Integration Notes

This web conversation has been automatically synced with your local SCF buildstate. Consider:

1. **Apply insights to current project**: Review the insights above and see how they apply to your local work
2. **Implement decisions**: Use the decisions captured here to guide your next development steps
3. **Update project context**: Merge relevant context into your main project buildstate files
4. **Share with team**: If working in a team, consider sharing relevant insights through your team's buildstate sharing system

## 🎼 SCF Integration Status

- ✅ Web conversation captured
- ✅ Insights extracted
- ✅ Decisions identified
- ✅ Buildstate generated
- 🔄 Ready for local integration

*This file was auto-generated by SCF Universal Context Sync*
"""
        
        return content
    
    async def list_sessions(self, request: web_request.Request) -> Response:
        """List all web sessions"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id, provider, title, url, start_time, last_activity, 
                       message_count, insights_count, decisions_count
                FROM web_sessions 
                ORDER BY last_activity DESC
                LIMIT 50
            """)
            
            sessions = []
            for row in cursor.fetchall():
                sessions.append({
                    "id": row[0],
                    "provider": row[1],
                    "title": row[2],
                    "url": row[3],
                    "start_time": row[4],
                    "last_activity": row[5],
                    "message_count": row[6],
                    "insights_count": row[7],
                    "decisions_count": row[8]
                })
            
            conn.close()
            
            return web.json_response({
                "sessions": sessions,
                "total": len(sessions)
            })
            
        except Exception as e:
            return web.json_response(
                {"error": str(e)}, 
                status=500
            )
    
    async def get_session_details(self, request: web_request.Request) -> Response:
        """Get detailed information about a specific session"""
        try:
            session_id = request.match_info['session_id']
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get session data
            cursor.execute("""
                SELECT * FROM web_sessions WHERE id = ?
            """, (session_id,))
            
            session_row = cursor.fetchone()
            if not session_row:
                return web.json_response(
                    {"error": "Session not found"}, 
                    status=404
                )
            
            # Get messages
            cursor.execute("""
                SELECT author, content, message_type, timestamp 
                FROM web_messages 
                WHERE session_id = ? 
                ORDER BY timestamp
            """, (session_id,))
            
            messages = []
            for row in cursor.fetchall():
                messages.append({
                    "author": row[0],
                    "content": row[1],
                    "type": row[2],
                    "timestamp": row[3]
                })
            
            conn.close()
            
            # Parse conversation data
            conversation_data = json.loads(session_row[9]) if session_row[9] else {}
            
            return web.json_response({
                "session": {
                    "id": session_row[0],
                    "provider": session_row[1],
                    "title": session_row[2],
                    "url": session_row[3],
                    "start_time": session_row[4],
                    "last_activity": session_row[5],
                    "message_count": session_row[6],
                    "insights_count": session_row[7],
                    "decisions_count": session_row[8]
                },
                "messages": messages,
                "conversation_data": conversation_data
            })
            
        except Exception as e:
            return web.json_response(
                {"error": str(e)}, 
                status=500
            )
    
    def setup_routes(self, app: web.Application):
        """Setup web routes"""
        app.router.add_get('/health', self.health_check)
        app.router.add_post('/sync', self.sync_conversation)
        app.router.add_get('/sessions', self.list_sessions)
        app.router.add_get('/sessions/{session_id}', self.get_session_details)
        
        # Add CORS support
        cors = cors_setup(app, defaults={
            "*": aiohttp_cors.ResourceOptions(
                allow_credentials=True,
                expose_headers="*",
                allow_headers="*",
                allow_methods="*"
            )
        })
        
        # Apply CORS to all routes
        for route in list(app.router.routes()):
            cors.add(route)
    
    async def start_server(self):
        """Start the local server"""
        app = web.Application()
        self.setup_routes(app)
        
        print(f"🚀 SCF Local Server starting on port {self.port}")
        print(f"   Health check: http://localhost:{self.port}/health")
        print(f"   Sync endpoint: http://localhost:{self.port}/sync")
        print("   Ready for browser extension connections...")
        
        runner = web.AppRunner(app)
        await runner.setup()
        
        site = web.TCPSite(runner, 'localhost', self.port)
        await site.start()
        
        # Keep server running
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 SCF Local Server stopping...")
            await runner.cleanup()

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="SCF Local Server for Web Integration")
    parser.add_argument('--port', type=int, default=8765, help='Server port (default: 8765)')
    parser.add_argument('--workspace', type=str, help='Workspace root directory')
    
    args = parser.parse_args()
    
    server = SCFLocalServer(port=args.port, workspace_root=args.workspace)
    
    try:
        asyncio.run(server.start_server())
    except KeyboardInterrupt:
        print("\n👋 SCF Local Server stopped")

if __name__ == "__main__":
    main()