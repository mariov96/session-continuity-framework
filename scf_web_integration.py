#!/usr/bin/env python3
"""
SCF Web Integration & Universal Context Sync
==========================================

This module extends SCF beyond local projects to web interactions, browser tab management,
team collaboration, and universal context synchronization. It enables:

1. Web LLM Context Sync - Keep web-based AI conversations in sync with project buildstate
2. Browser Tab Management - Convert open tabs into organized task lists and context
3. Team Collaboration - Share buildstate insights across team members automatically
4. Tool Coexistence - Work alongside claude.md, llm.md, and other tool-specific files
5. Interactive Education - Personalized LLM-guided setup and optimization

The goal is to create a universal context awareness system that captures insights from
everywhere (web, local, team) and feeds them back into the buildstate ecosystem for
maximum benefit retention and cross-pollination.

Features:
- Browser extension integration for web LLM sync
- Tab-to-task conversion with context preservation  
- Team buildstate synchronization and contribution
- Coexistence with existing tool-specific workflows
- Interactive LLM-powered setup and education system
"""

import json
import sqlite3
import hashlib
import asyncio
import websockets
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, field
from enum import Enum
import subprocess
import requests
import webbrowser
from urllib.parse import urlparse, parse_qs

class WebLLMProvider(Enum):
    """Web-based LLM providers that can sync with SCF"""
    CLAUDE_WEB = "claude.ai"
    CHATGPT_WEB = "chat.openai.com"  
    PERPLEXITY_WEB = "perplexity.ai"
    GEMINI_WEB = "gemini.google.com"
    CUSTOM_WEB = "custom"

class TabContextType(Enum):
    """Types of browser tab content for context analysis"""
    LLM_CONVERSATION = "llm_conversation"
    DOCUMENTATION = "documentation" 
    GITHUB_REPO = "github_repo"
    STACK_OVERFLOW = "stackoverflow"
    TUTORIAL = "tutorial"
    REFERENCE = "reference"
    RESEARCH = "research"
    UNKNOWN = "unknown"

class TeamContributionType(Enum):
    """Types of team contributions to buildstate ecosystem"""
    PATTERN_SHARE = "pattern_share"
    SOLUTION_TEMPLATE = "solution_template"
    BEST_PRACTICE = "best_practice"
    TOOL_INTEGRATION = "tool_integration"
    LESSON_LEARNED = "lesson_learned"

@dataclass
class WebLLMSession:
    """Represents a web-based LLM conversation session"""
    session_id: str
    provider: WebLLMProvider
    url: str
    title: str
    start_time: datetime
    last_activity: datetime
    message_count: int
    key_insights: List[str]
    decisions_made: List[str]
    project_relevance: float  # 0.0-1.0
    sync_status: str  # 'synced', 'pending', 'failed'
    local_buildstate_path: Optional[str]

@dataclass
class BrowserTab:
    """Represents a browser tab with context analysis"""
    tab_id: str
    url: str
    title: str
    content_type: TabContextType
    relevance_score: float
    key_concepts: List[str]
    potential_tasks: List[str]
    last_accessed: datetime
    session_duration: timedelta
    project_connections: List[str]

@dataclass
class TeamContribution:
    """Represents a contribution from team member to SCF ecosystem"""
    contribution_id: str
    contributor: str
    contribution_type: TeamContributionType
    title: str
    description: str
    content: Dict[str, Any]
    applicable_projects: List[str]
    validation_score: float
    usage_count: int
    created_at: datetime
    
@dataclass
class InteractiveLearningSession:
    """Represents an interactive SCF learning session with LLM"""
    session_id: str
    user_profile: Dict[str, Any]
    learning_objectives: List[str]
    current_step: int
    completed_steps: List[str]
    personalized_recommendations: List[str]
    project_analysis: Dict[str, Any]
    setup_progress: float  # 0.0-1.0

class SCFWebIntegration:
    """Universal SCF integration for web, team, and interactive learning"""
    
    def __init__(self, base_project_path: str = None):
        self.base_path = Path(base_project_path) if base_project_path else Path.cwd()
        self.scf_web_db = self.base_path / '.scf' / 'web_integration.db'
        self.browser_extension_port = 8765
        self.team_sync_enabled = False
        
        # Web session tracking
        self.active_web_sessions: Dict[str, WebLLMSession] = {}
        self.browser_tabs: Dict[str, BrowserTab] = {}
        
        # Team collaboration
        self.team_contributions: List[TeamContribution] = []
        self.team_sync_url: Optional[str] = None
        
        # Interactive learning
        self.learning_sessions: Dict[str, InteractiveLearningSession] = {}
        
        self._initialize_web_integration()
        
    def _initialize_web_integration(self):
        """Initialize web integration components"""
        # Create SCF web directory
        (self.base_path / '.scf').mkdir(exist_ok=True)
        
        # Initialize database
        self._setup_web_database()
        
        # Load existing sessions
        self._load_web_sessions()
        
        # Check for browser extension
        self._check_browser_extension()
        
    def _setup_web_database(self):
        """Setup SQLite database for web integration data"""
        conn = sqlite3.connect(self.scf_web_db)
        
        # Web LLM sessions table
        conn.execute('''
            CREATE TABLE IF NOT EXISTS web_llm_sessions (
                session_id TEXT PRIMARY KEY,
                provider TEXT,
                url TEXT,
                title TEXT,
                start_time TEXT,
                last_activity TEXT,
                message_count INTEGER,
                key_insights TEXT,
                decisions_made TEXT,
                project_relevance REAL,
                sync_status TEXT,
                local_buildstate_path TEXT
            )
        ''')
        
        # Browser tabs table
        conn.execute('''
            CREATE TABLE IF NOT EXISTS browser_tabs (
                tab_id TEXT PRIMARY KEY,
                url TEXT,
                title TEXT,
                content_type TEXT,
                relevance_score REAL,
                key_concepts TEXT,
                potential_tasks TEXT,
                last_accessed TEXT,
                session_duration TEXT,
                project_connections TEXT
            )
        ''')
        
        # Team contributions table
        conn.execute('''
            CREATE TABLE IF NOT EXISTS team_contributions (
                contribution_id TEXT PRIMARY KEY,
                contributor TEXT,
                contribution_type TEXT,
                title TEXT,
                description TEXT,
                content TEXT,
                applicable_projects TEXT,
                validation_score REAL,
                usage_count INTEGER,
                created_at TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
        
    def sync_web_llm_session(self, provider: WebLLMProvider, url: str, 
                           conversation_data: Dict[str, Any]) -> WebLLMSession:
        """Sync a web-based LLM conversation with local buildstate"""
        session_id = hashlib.md5(f"{provider.value}_{url}".encode()).hexdigest()[:12]
        
        # Analyze conversation for insights and decisions
        insights = self._extract_conversation_insights(conversation_data)
        decisions = self._extract_conversation_decisions(conversation_data)
        
        # Determine project relevance
        relevance = self._calculate_project_relevance(conversation_data)
        
        # Find best matching local buildstate
        buildstate_path = self._find_matching_buildstate(conversation_data, relevance)
        
        session = WebLLMSession(
            session_id=session_id,
            provider=provider,
            url=url,
            title=conversation_data.get('title', 'Untitled Conversation'),
            start_time=datetime.now(),
            last_activity=datetime.now(),
            message_count=len(conversation_data.get('messages', [])),
            key_insights=insights,
            decisions_made=decisions,
            project_relevance=relevance,
            sync_status='pending',
            local_buildstate_path=buildstate_path
        )
        
        # Sync with local buildstate if relevance is high
        if relevance > 0.7 and buildstate_path:
            self._sync_to_local_buildstate(session, conversation_data)
            session.sync_status = 'synced'
        
        self.active_web_sessions[session_id] = session
        self._save_web_session(session)
        
        return session
        
    def convert_tabs_to_tasks(self, browser_tabs_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Convert open browser tabs into organized tasks and context"""
        task_groups = {
            'immediate_tasks': [],
            'research_topics': [],
            'reference_materials': [],
            'learning_resources': []
        }
        
        for tab_data in browser_tabs_data:
            tab = self._analyze_browser_tab(tab_data)
            self.browser_tabs[tab.tab_id] = tab
            
            # Convert to tasks based on content type and relevance
            if tab.relevance_score > 0.8:
                # High relevance - immediate tasks
                for task in tab.potential_tasks:
                    task_groups['immediate_tasks'].append({
                        'task': task,
                        'source_url': tab.url,
                        'source_title': tab.title,
                        'priority': min(int(tab.relevance_score * 10), 10),
                        'context': tab.key_concepts
                    })
            elif tab.content_type in [TabContextType.DOCUMENTATION, TabContextType.TUTORIAL]:
                # Learning resources
                task_groups['learning_resources'].append({
                    'resource': tab.title,
                    'url': tab.url,
                    'concepts': tab.key_concepts,
                    'estimated_time': self._estimate_learning_time(tab)
                })
            elif tab.content_type == TabContextType.RESEARCH:
                # Research topics
                task_groups['research_topics'].extend([{
                    'topic': concept,
                    'source': tab.url,
                    'relevance': tab.relevance_score
                } for concept in tab.key_concepts])
            else:
                # Reference materials
                task_groups['reference_materials'].append({
                    'title': tab.title,
                    'url': tab.url,
                    'concepts': tab.key_concepts
                })
                
        # Update local buildstate with organized tasks
        self._update_buildstate_with_tasks(task_groups)
        
        return task_groups
        
    def setup_team_collaboration(self, team_sync_url: str, team_members: List[str]):
        """Setup team collaboration for buildstate sharing"""
        self.team_sync_url = team_sync_url
        self.team_sync_enabled = True
        
        # Initialize team collaboration
        team_config = {
            'sync_url': team_sync_url,
            'members': team_members,
            'auto_sync': True,
            'contribution_validation': True,
            'pattern_sharing': True
        }
        
        # Save team configuration
        team_config_path = self.base_path / '.scf' / 'team_config.json'
        with open(team_config_path, 'w') as f:
            json.dump(team_config, f, indent=2)
            
        print(f"✅ Team collaboration enabled with {len(team_members)} members")
        
    def contribute_to_team(self, contribution_type: TeamContributionType, 
                          title: str, description: str, content: Dict[str, Any],
                          applicable_projects: List[str] = None) -> TeamContribution:
        """Contribute insights/patterns to team buildstate ecosystem"""
        contribution = TeamContribution(
            contribution_id=hashlib.md5(f"{title}_{datetime.now().isoformat()}".encode()).hexdigest()[:12],
            contributor=self._get_current_user(),
            contribution_type=contribution_type,
            title=title,
            description=description,
            content=content,
            applicable_projects=applicable_projects or [],
            validation_score=0.0,
            usage_count=0,
            created_at=datetime.now()
        )
        
        self.team_contributions.append(contribution)
        self._save_team_contribution(contribution)
        
        # Sync with team if enabled
        if self.team_sync_enabled:
            self._sync_team_contribution(contribution)
            
        return contribution
        
    def create_interactive_learning_session(self, user_profile: Dict[str, Any] = None) -> str:
        """Create personalized SCF learning session with LLM guidance"""
        session_id = f"learn_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Analyze user's current setup and projects
        project_analysis = self._analyze_user_projects()
        
        # Generate personalized learning objectives
        learning_objectives = self._generate_learning_objectives(user_profile, project_analysis)
        
        session = InteractiveLearningSession(
            session_id=session_id,
            user_profile=user_profile or {},
            learning_objectives=learning_objectives,
            current_step=0,
            completed_steps=[],
            personalized_recommendations=[],
            project_analysis=project_analysis,
            setup_progress=0.0
        )
        
        self.learning_sessions[session_id] = session
        
        # Launch interactive learning chat
        self._launch_interactive_learning_chat(session)
        
        return session_id
        
    def coexist_with_tool_files(self, project_path: str) -> Dict[str, Any]:
        """Ensure SCF coexists with claude.md, llm.md, and other tool-specific files"""
        project_path = Path(project_path)
        
        # Scan for existing tool-specific files
        tool_files = {
            'claude.md': project_path / 'claude.md',
            'llm.md': project_path / 'llm.md', 
            'gpt.md': project_path / 'gpt.md',
            'cursor.md': project_path / 'cursor.md',
            'copilot.md': project_path / 'copilot.md'
        }
        
        existing_files = {name: path for name, path in tool_files.items() if path.exists()}
        
        if existing_files:
            print(f"🔍 Found {len(existing_files)} existing tool-specific files:")
            for name, path in existing_files.items():
                print(f"  📄 {name} - {path}")
                
        # Create SCF awareness integration
        integration_plan = {
            'existing_tools': list(existing_files.keys()),
            'scf_role': 'orchestration_and_context',
            'tool_roles': {},
            'integration_strategy': 'coexistence_with_awareness'
        }
        
        # Define roles for each tool file
        for tool_name in existing_files.keys():
            if 'claude' in tool_name:
                integration_plan['tool_roles'][tool_name] = {
                    'purpose': 'Claude-specific prompts and conversation patterns',
                    'scf_awareness': 'References buildstate for project context',
                    'major_actions': 'Reports architectural decisions to buildstate'
                }
            elif 'gpt' in tool_name or 'llm' in tool_name:
                integration_plan['tool_roles'][tool_name] = {
                    'purpose': 'GPT/LLM-specific templates and workflows',
                    'scf_awareness': 'Loads buildstate context automatically', 
                    'major_actions': 'Syncs insights back to buildstate'
                }
            elif 'cursor' in tool_name:
                integration_plan['tool_roles'][tool_name] = {
                    'purpose': 'Cursor AI-specific coding patterns',
                    'scf_awareness': 'Uses buildstate technical context',
                    'major_actions': 'Reports code changes and patterns'
                }
                
        # Create SCF integration snippets for existing files
        self._create_scf_integration_snippets(existing_files, integration_plan)
        
        return integration_plan
        
    def _extract_conversation_insights(self, conversation_data: Dict[str, Any]) -> List[str]:
        """Extract key insights from web LLM conversation"""
        insights = []
        messages = conversation_data.get('messages', [])
        
        for message in messages:
            content = message.get('content', '')
            
            # Look for insight patterns
            insight_patterns = [
                r'I learned that (.+?)(?:\.|$)',
                r'Key insight: (.+?)(?:\.|$)',
                r'This means (.+?)(?:\.|$)',
                r'The important point is (.+?)(?:\.|$)'
            ]
            
            for pattern in insight_patterns:
                import re
                matches = re.findall(pattern, content, re.IGNORECASE)
                insights.extend(matches)
                
        return insights[:10]  # Limit to top 10 insights
        
    def _extract_conversation_decisions(self, conversation_data: Dict[str, Any]) -> List[str]:
        """Extract decisions made during web LLM conversation"""
        decisions = []
        messages = conversation_data.get('messages', [])
        
        for message in messages:
            content = message.get('content', '')
            
            # Look for decision patterns
            decision_patterns = [
                r'I(?:\'ll| will) (.+?)(?:\.|$)',
                r'Let\'s (.+?)(?:\.|$)',
                r'We should (.+?)(?:\.|$)',
                r'Decision: (.+?)(?:\.|$)'
            ]
            
            for pattern in decision_patterns:
                import re
                matches = re.findall(pattern, content, re.IGNORECASE)
                decisions.extend(matches)
                
        return decisions[:10]  # Limit to top 10 decisions
        
    def _calculate_project_relevance(self, conversation_data: Dict[str, Any]) -> float:
        """Calculate how relevant a conversation is to local projects"""
        # Analyze conversation content for project-related terms
        content = ' '.join([msg.get('content', '') for msg in conversation_data.get('messages', [])])
        
        # Load local buildstate files to compare
        buildstate_files = list(self.base_path.rglob('buildstate.json'))
        
        if not buildstate_files:
            return 0.3  # Default relevance if no buildstate files
            
        # Simple keyword matching (in practice, would use more sophisticated NLP)
        project_keywords = set()
        for buildstate_file in buildstate_files:
            try:
                with open(buildstate_file, 'r') as f:
                    data = json.load(f)
                    
                # Extract keywords from project data
                project_info = data.get('project', {})
                stack = data.get('stack', [])
                features = data.get('features', [])
                
                project_keywords.update([
                    project_info.get('name', '').lower(),
                    project_info.get('type', '').lower()
                ])
                project_keywords.update([s.lower() for s in stack if isinstance(s, str)])
                project_keywords.update([f.lower() for f in features if isinstance(f, str)])
                
            except:
                continue
                
        # Calculate relevance based on keyword matches
        content_lower = content.lower()
        matches = sum(1 for keyword in project_keywords if keyword and keyword in content_lower)
        total_keywords = len(project_keywords)
        
        relevance = matches / max(total_keywords, 1) if total_keywords > 0 else 0.0
        return min(relevance * 2, 1.0)  # Scale up but cap at 1.0
        
    def _find_matching_buildstate(self, conversation_data: Dict[str, Any], relevance: float) -> Optional[str]:
        """Find the best matching buildstate file for a conversation"""
        if relevance < 0.5:
            return None
            
        buildstate_files = list(self.base_path.rglob('buildstate.json'))
        
        if not buildstate_files:
            return None
            
        # For simplicity, return the first buildstate file
        # In practice, would do more sophisticated matching
        return str(buildstate_files[0])
        
    def _sync_to_local_buildstate(self, session: WebLLMSession, conversation_data: Dict[str, Any]):
        """Sync web conversation insights to local buildstate"""
        if not session.local_buildstate_path:
            return
            
        try:
            buildstate_path = Path(session.local_buildstate_path)
            
            with open(buildstate_path, 'r') as f:
                buildstate_data = json.load(f)
                
            # Add web session insights to session log
            if 'web_sessions' not in buildstate_data:
                buildstate_data['web_sessions'] = []
                
            web_session_entry = {
                'session_id': session.session_id,
                'provider': session.provider.value,
                'url': session.url,
                'sync_date': datetime.now().isoformat(),
                'insights_count': len(session.key_insights),
                'decisions_count': len(session.decisions_made),
                'relevance_score': session.project_relevance
            }
            
            buildstate_data['web_sessions'].append(web_session_entry)
            
            # Add insights to general insights section
            if 'insights' not in buildstate_data:
                buildstate_data['insights'] = []
                
            for insight in session.key_insights:
                buildstate_data['insights'].append({
                    'content': insight,
                    'source': f'web_llm_{session.provider.value}',
                    'date': datetime.now().isoformat(),
                    'type': 'web_conversation'
                })
                
            # Save updated buildstate
            with open(buildstate_path, 'w') as f:
                json.dump(buildstate_data, f, indent=2)
                
            print(f"✅ Synced web session {session.session_id} to {buildstate_path.name}")
            
        except Exception as e:
            print(f"⚠️  Error syncing to buildstate: {e}")
            session.sync_status = 'failed'
            
    def _analyze_browser_tab(self, tab_data: Dict[str, Any]) -> BrowserTab:
        """Analyze a browser tab for context and potential tasks"""
        url = tab_data.get('url', '')
        title = tab_data.get('title', '')
        
        # Determine content type based on URL and title
        content_type = self._classify_tab_content(url, title)
        
        # Extract key concepts
        key_concepts = self._extract_tab_concepts(title, url)
        
        # Generate potential tasks
        potential_tasks = self._generate_tab_tasks(content_type, title, key_concepts)
        
        # Calculate relevance score
        relevance_score = self._calculate_tab_relevance(url, title, key_concepts)
        
        return BrowserTab(
            tab_id=hashlib.md5(url.encode()).hexdigest()[:12],
            url=url,
            title=title,
            content_type=content_type,
            relevance_score=relevance_score,
            key_concepts=key_concepts,
            potential_tasks=potential_tasks,
            last_accessed=datetime.now(),
            session_duration=timedelta(minutes=5),  # Default estimate
            project_connections=[]
        )
        
    def _classify_tab_content(self, url: str, title: str) -> TabContextType:
        """Classify browser tab content type"""
        url_lower = url.lower()
        title_lower = title.lower()
        
        # LLM conversation detection
        llm_domains = ['claude.ai', 'chat.openai.com', 'perplexity.ai', 'gemini.google.com']
        if any(domain in url_lower for domain in llm_domains):
            return TabContextType.LLM_CONVERSATION
            
        # GitHub repository
        if 'github.com' in url_lower and any(word in url_lower for word in ['/blob/', '/tree/', '/commit/']):
            return TabContextType.GITHUB_REPO
            
        # Stack Overflow
        if 'stackoverflow.com' in url_lower:
            return TabContextType.STACK_OVERFLOW
            
        # Documentation
        if any(word in url_lower for word in ['docs.', 'documentation', 'api.', 'developer.']):
            return TabContextType.DOCUMENTATION
            
        # Tutorial/Learning
        if any(word in title_lower for word in ['tutorial', 'guide', 'how to', 'learn']):
            return TabContextType.TUTORIAL
            
        return TabContextType.UNKNOWN
        
    def _extract_tab_concepts(self, title: str, url: str) -> List[str]:
        """Extract key concepts from tab title and URL"""
        concepts = []
        
        # Extract from title
        title_words = title.lower().split()
        tech_keywords = ['react', 'python', 'javascript', 'typescript', 'node', 'api', 'database', 'aws', 'docker']
        concepts.extend([word for word in title_words if word in tech_keywords])
        
        # Extract from URL path
        path_parts = url.split('/')
        concepts.extend([part for part in path_parts if len(part) > 3 and part.isalpha()])
        
        return list(set(concepts))[:5]  # Limit to 5 unique concepts
        
    def _generate_tab_tasks(self, content_type: TabContextType, title: str, concepts: List[str]) -> List[str]:
        """Generate potential tasks based on tab content"""
        tasks = []
        
        if content_type == TabContextType.LLM_CONVERSATION:
            tasks.append("Review conversation insights and sync to buildstate")
            tasks.append("Extract decisions made and update project context")
            
        elif content_type == TabContextType.DOCUMENTATION:
            tasks.append(f"Study {title} documentation")
            tasks.append("Update technical requirements based on API capabilities")
            
        elif content_type == TabContextType.GITHUB_REPO:
            tasks.append("Analyze repository structure and patterns")
            tasks.append("Consider implementation approaches for current project")
            
        elif content_type == TabContextType.TUTORIAL:
            tasks.append(f"Complete tutorial: {title}")
            tasks.append("Apply learned concepts to current project")
            
        return tasks
        
    def _calculate_tab_relevance(self, url: str, title: str, concepts: List[str]) -> float:
        """Calculate tab relevance to current projects"""
        # Load project context for comparison
        relevance = 0.0
        
        buildstate_files = list(self.base_path.rglob('buildstate.json'))
        
        for buildstate_file in buildstate_files:
            try:
                with open(buildstate_file, 'r') as f:
                    data = json.load(f)
                    
                project_stack = data.get('stack', [])
                project_features = data.get('features', [])
                
                # Check concept overlap
                project_concepts = [s.lower() for s in project_stack if isinstance(s, str)]
                project_concepts.extend([f.lower() for f in project_features if isinstance(f, str)])
                
                overlap = len(set(concepts) & set(project_concepts))
                total_concepts = len(set(concepts) | set(project_concepts))
                
                if total_concepts > 0:
                    relevance = max(relevance, overlap / total_concepts)
                    
            except:
                continue
                
        return min(relevance * 1.5, 1.0)  # Scale up but cap at 1.0
        
    def _launch_interactive_learning_chat(self, session: InteractiveLearningSession):
        """Launch interactive SCF learning chat with LLM"""
        chat_content = self._generate_learning_chat_content(session)
        
        # Create temporary HTML file for interactive chat
        chat_file = self.base_path / '.scf' / f'interactive_learning_{session.session_id}.html'
        
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>SCF Interactive Learning - Personalized Setup</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui; margin: 0; padding: 20px; background: #f5f5f5; }}
        .container {{ max-width: 800px; margin: 0 auto; background: white; border-radius: 12px; padding: 30px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
        .header {{ text-align: center; margin-bottom: 30px; }}
        .chat-area {{ border: 1px solid #ddd; border-radius: 8px; padding: 20px; min-height: 400px; background: #fafafa; }}
        .progress {{ width: 100%; height: 8px; background: #eee; border-radius: 4px; margin: 20px 0; }}
        .progress-bar {{ height: 100%; background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); border-radius: 4px; width: {session.setup_progress * 100}%; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎯 SCF Interactive Learning</h1>
            <p>Personalized Session Continuity Framework setup tailored for you</p>
            <div class="progress"><div class="progress-bar"></div></div>
            <p>Progress: {session.setup_progress * 100:.0f}% complete</p>
        </div>
        
        <div class="chat-area">
            {chat_content}
        </div>
        
        <div style="margin-top: 20px; padding: 20px; background: #f0f7ff; border-radius: 8px;">
            <h3>🚀 Your Personalized Learning Plan</h3>
            <ul>
                {chr(10).join(f'<li>{obj}</li>' for obj in session.learning_objectives)}
            </ul>
        </div>
    </div>
</body>
</html>
        """
        
        with open(chat_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
            
        # Open in browser
        webbrowser.open(f'file://{chat_file.absolute()}')
        
        print(f"🎯 Interactive SCF learning session launched!")
        print(f"📖 Session ID: {session.session_id}")
        print(f"🎨 Learning objectives: {len(session.learning_objectives)}")
        
    def _generate_learning_chat_content(self, session: InteractiveLearningSession) -> str:
        """Generate personalized learning chat content"""
        analysis = session.project_analysis
        
        chat_content = f"""
        <div style="margin-bottom: 20px; padding: 15px; background: white; border-radius: 8px; border-left: 4px solid #667eea;">
            <h4>👋 Welcome to SCF Interactive Learning!</h4>
            <p>I've analyzed your development environment and created a personalized learning plan just for you.</p>
        </div>
        
        <div style="margin-bottom: 20px; padding: 15px; background: white; border-radius: 8px;">
            <h4>📊 Your Development Profile Analysis</h4>
            <ul>
                <li><strong>Projects Found:</strong> {analysis.get('project_count', 0)}</li>
                <li><strong>Primary Technologies:</strong> {', '.join(analysis.get('tech_stack', ['Not detected']))}</li>
                <li><strong>Current SCF Usage:</strong> {analysis.get('scf_usage_level', 'Beginner')}</li>
                <li><strong>Optimization Potential:</strong> {analysis.get('optimization_score', 0):.0%}</li>
            </ul>
        </div>
        
        <div style="margin-bottom: 20px; padding: 15px; background: #f8fff4; border-radius: 8px; border-left: 4px solid #22c55e;">
            <h4>💡 Personalized Recommendations</h4>
            <p>Based on your profile, here's what will give you the biggest impact:</p>
            <ol>
                <li><strong>Quick Win:</strong> Set up buildstate files in your top 3 active projects</li>
                <li><strong>Workflow Enhancement:</strong> Configure your most-used AI tools for automatic context loading</li>
                <li><strong>Team Collaboration:</strong> Enable buildstate sharing for maximum team benefit</li>
            </ol>
        </div>
        
        <div style="padding: 15px; background: #fef3c7; border-radius: 8px; border-left: 4px solid #f59e0b;">
            <h4>🎯 Next Steps</h4>
            <p>Copy and paste this context into your preferred AI tool to continue the interactive setup:</p>
            <pre style="background: white; padding: 10px; border-radius: 4px; font-size: 12px; overflow-x: auto;">
**SCF Interactive Learning Session**
User Profile: {json.dumps(session.user_profile, indent=2)}
Learning Objectives: {', '.join(session.learning_objectives)}
Project Analysis: {json.dumps(analysis, indent=2)}

Please guide me through SCF setup with personalized recommendations based on my profile.
Start with the highest-impact improvements for my specific situation.
            </pre>
        </div>
        """
        
        return chat_content
        
    # Helper methods and utilities
    def _load_web_sessions(self):
        """Load existing web sessions from database"""
        if not self.scf_web_db.exists():
            return
            
        conn = sqlite3.connect(self.scf_web_db)
        cursor = conn.execute('SELECT * FROM web_llm_sessions')
        
        for row in cursor.fetchall():
            session = WebLLMSession(
                session_id=row[0],
                provider=WebLLMProvider(row[1]),
                url=row[2],
                title=row[3],
                start_time=datetime.fromisoformat(row[4]),
                last_activity=datetime.fromisoformat(row[5]),
                message_count=row[6],
                key_insights=json.loads(row[7]) if row[7] else [],
                decisions_made=json.loads(row[8]) if row[8] else [],
                project_relevance=row[9],
                sync_status=row[10],
                local_buildstate_path=row[11]
            )
            self.active_web_sessions[session.session_id] = session
            
        conn.close()
        
    def _save_web_session(self, session: WebLLMSession):
        """Save web session to database"""
        conn = sqlite3.connect(self.scf_web_db)
        conn.execute('''
            INSERT OR REPLACE INTO web_llm_sessions 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            session.session_id,
            session.provider.value,
            session.url,
            session.title,
            session.start_time.isoformat(),
            session.last_activity.isoformat(),
            session.message_count,
            json.dumps(session.key_insights),
            json.dumps(session.decisions_made),
            session.project_relevance,
            session.sync_status,
            session.local_buildstate_path
        ))
        conn.commit()
        conn.close()
        
    def get_web_integration_status(self) -> Dict[str, Any]:
        """Get status of web integration features"""
        return {
            'active_web_sessions': len(self.active_web_sessions),
            'synced_sessions': len([s for s in self.active_web_sessions.values() if s.sync_status == 'synced']),
            'browser_tabs_tracked': len(self.browser_tabs),
            'team_contributions': len(self.team_contributions),
            'team_sync_enabled': self.team_sync_enabled,
            'learning_sessions_active': len(self.learning_sessions)
        }


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='SCF Web Integration & Universal Context Sync')
    parser.add_argument('project_path', nargs='?', default='.',
                      help='Base project path for SCF integration')
    parser.add_argument('--interactive-learning', action='store_true',
                      help='Launch interactive SCF learning session')
    parser.add_argument('--coexist-check', action='store_true',
                      help='Check coexistence with existing tool files')
    parser.add_argument('--status', action='store_true',
                      help='Show web integration status')
    
    args = parser.parse_args()
    
    web_integration = SCFWebIntegration(args.project_path)
    
    if args.interactive_learning:
        print("🎯 Launching SCF Interactive Learning Session...")
        user_profile = {
            'experience_level': 'intermediate',
            'primary_languages': ['Python', 'JavaScript'],
            'preferred_tools': ['Claude', 'VS Code', 'Git'],
            'team_size': 'individual',
            'project_types': ['web_applications', 'automation_scripts']
        }
        session_id = web_integration.create_interactive_learning_session(user_profile)
        print(f"✅ Learning session created: {session_id}")
        
    elif args.coexist_check:
        print("🔍 Checking coexistence with existing tool files...")
        integration_plan = web_integration.coexist_with_tool_files(args.project_path)
        print(f"📊 Integration Plan:")
        print(f"   Existing tools: {integration_plan['existing_tools']}")
        print(f"   Strategy: {integration_plan['integration_strategy']}")
        
    elif args.status:
        status = web_integration.get_web_integration_status()
        print("🌐 SCF Web Integration Status:")
        for key, value in status.items():
            print(f"   {key}: {value}")
            
    else:
        print("🌐 SCF Web Integration & Universal Context Sync")
        print("=" * 50)
        print("Features available:")
        print("  --interactive-learning: Personalized SCF setup with LLM guidance")
        print("  --coexist-check: Verify coexistence with existing tool files")  
        print("  --status: Show current web integration status")
        print()
        print("💡 Use --help for detailed options")