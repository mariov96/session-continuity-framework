#!/usr/bin/env python3
"""
SCF LLM Integration Engine - Universal AI Context Driver
=====================================================

This module provides tight integration between Session Continuity Framework (SCF) and ANY LLM
by making buildstate the central driver of every AI interaction. It automatically:

1. Injects buildstate context at conversation start
2. Tracks learning and decisions during sessions
3. Updates buildstate continuously until rebalancing triggers
4. Provides universal LLM compatibility through adaptive formatting
5. Captures session insights for ecosystem learning

The goal is to make buildstate the "first thought" of every LLM interaction, ensuring
perfect context continuity and intelligent decision capture across all AI sessions.

Usage:
    # Initialize LLM session with buildstate context
    integrator = SCFLLMIntegrator(project_path="/path/to/project")
    
    # Auto-inject buildstate context for any LLM
    context = integrator.prepare_session_context(llm_type="claude|gpt|grok|gemini")
    
    # Track session insights and decisions
    integrator.capture_insight("User decided to use React over Vue for better team familiarity")
    integrator.capture_decision("Architecture: Microservices with API Gateway", impact=8)
    
    # Auto-update buildstate during session
    integrator.track_feature_progress("user-authentication", status="in_progress", completion=0.7)
    
    # Session completion with rebalancing check
    integrator.complete_session(trigger_rebalancing=True)
"""

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple, Union
from dataclasses import dataclass, field
from enum import Enum
from scf_analytics import SCFAnalytics

try:
    from scf_enhanced_overview import generate_enhanced_overview
except ImportError:
    # Fallback if enhanced overview is not available
    def generate_enhanced_overview(project_path):
        return "## SCF Overview\n\nEnhanced tracking not available."

class LLMType(Enum):
    """Supported LLM types with specific formatting needs"""
    CLAUDE = "claude"
    GPT = "gpt"
    GROK = "grok"
    GEMINI = "gemini"
    GENERIC = "generic"

class SessionType(Enum):
    """Types of AI sessions with different context needs"""
    IDEATION = "ideation"           # Strategic planning, brainstorming
    IMPLEMENTATION = "implementation"  # Coding, debugging, building
    ANALYSIS = "analysis"           # Research, investigation, learning
    OPTIMIZATION = "optimization"   # Performance, refactoring, improvement
    PLANNING = "planning"           # Architecture, design, roadmapping

@dataclass
class SessionInsight:
    """Captures insights and learnings during AI sessions"""
    timestamp: datetime
    content: str
    insight_type: str  # 'decision', 'learning', 'pattern', 'issue', 'solution'
    confidence: float  # 0.0-1.0
    impact_level: int  # 1-10
    tags: List[str] = field(default_factory=list)
    source_context: str = ""
    
@dataclass
class SessionContext:
    """Complete context package for LLM sessions"""
    buildstate_summary: str
    current_objectives: List[str]
    recent_changes: List[Dict[str, Any]]
    key_constraints: List[str]
    ai_rules: Dict[str, Any]
    session_type: SessionType
    priority_focus: str
    formatted_context: str  # LLM-specific formatted context

class SCFLLMIntegrator:
    """Universal LLM integration engine for Session Continuity Framework"""
    
    def __init__(self, project_path: Union[str, Path], auto_detect: bool = True):
        """Initialize SCF LLM Integrator
        
        Args:
            project_path: Path to project containing buildstate files
            auto_detect: Automatically detect buildstate files and project structure
        """
        self.project_path = Path(project_path)
        self.buildstate_json_path = None
        self.buildstate_md_path = None
        self.session_insights: List[SessionInsight] = []
        self.current_session_id = None
        self.session_start_time = None
        self.analytics = None
        
        if auto_detect:
            self._detect_buildstate_files()
            if self.buildstate_json_path:
                self.analytics = SCFAnalytics(self.buildstate_json_path)
            
    def _detect_buildstate_files(self):
        """Automatically detect buildstate files in project"""
        # Look for buildstate files in common patterns
        patterns = [
            "**/buildstate.json",
            "**/buildstate.md", 
            "**/_SC-buildstate.json",
            "**/_SC-buildstate.md",
            "**/buildstate.*.json",
            "**/buildstate.*.md"
        ]
        
        for pattern in patterns:
            files = list(self.project_path.glob(pattern))
            for file_path in files:
                if file_path.suffix == '.json':
                    self.buildstate_json_path = file_path
                elif file_path.suffix == '.md':
                    self.buildstate_md_path = file_path
                    
        if not (self.buildstate_json_path or self.buildstate_md_path):
            print(f"⚠️  No buildstate files found in {self.project_path}")
            print("   Consider initializing SCF with: scf_project_starter.py")
            
    def prepare_session_context(self, 
                              session_type: SessionType = SessionType.IMPLEMENTATION,
                              llm_type: LLMType = LLMType.GENERIC,
                              focus_areas: List[str] = None) -> SessionContext:
        """Prepare complete context package for LLM session
        
        Args:
            session_type: Type of session (ideation, implementation, etc.)
            llm_type: Target LLM for context formatting
            focus_areas: Specific areas to emphasize in context
            
        Returns:
            SessionContext: Complete formatted context for LLM
        """
        self.current_session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.session_start_time = datetime.now()
        
        # Start analytics tracking
        if self.analytics:
            self.analytics.start_session()
        
        # Load current buildstate data
        buildstate_data = self._load_buildstate_data()
        
        # Generate session context
        context = SessionContext(
            buildstate_summary=self._generate_buildstate_summary(buildstate_data, session_type),
            current_objectives=self._extract_current_objectives(buildstate_data, session_type),
            recent_changes=self._extract_recent_changes(buildstate_data),
            key_constraints=self._extract_constraints(buildstate_data),
            ai_rules=self._extract_ai_rules(buildstate_data),
            session_type=session_type,
            priority_focus=self._determine_priority_focus(buildstate_data, focus_areas),
            formatted_context=""  # Will be set below
        )
        
        # Format context for specific LLM
        context.formatted_context = self._format_for_llm(context, llm_type)
        
        return context
        
    def _load_buildstate_data(self) -> Dict[str, Any]:
        """Load and merge buildstate data from both JSON and MD files"""
        data = {'json_data': {}, 'md_content': '', 'combined': {}}
        
        # Load JSON buildstate
        if self.buildstate_json_path and self.buildstate_json_path.exists():
            try:
                with open(self.buildstate_json_path, 'r', encoding='utf-8') as f:
                    data['json_data'] = json.load(f)
                    data['combined'].update(data['json_data'])
            except Exception as e:
                print(f"⚠️  Error loading {self.buildstate_json_path}: {e}")
                
        # Load Markdown buildstate 
        if self.buildstate_md_path and self.buildstate_md_path.exists():
            try:
                data['md_content'] = self.buildstate_md_path.read_text(encoding='utf-8')
                # Extract structured data from markdown if possible
                md_data = self._extract_data_from_markdown(data['md_content'])
                data['combined'].update(md_data)
            except Exception as e:
                print(f"⚠️  Error loading {self.buildstate_md_path}: {e}")
                
        return data
        
    def _extract_data_from_markdown(self, md_content: str) -> Dict[str, Any]:
        """Extract structured data from markdown buildstate"""
        data = {}
        
        # Extract key sections using regex patterns
        sections = {
            'objectives': r'##\s*(?:Current\s+)?(?:Objectives?|Goals?)\s*\n(.*?)(?=##|\Z)',
            'features': r'###?\s*(?:Features?|User Stories)\s*\n(.*?)(?=##|\Z)', 
            'constraints': r'##\s*(?:Constraints?|Limitations?)\s*\n(.*?)(?=##|\Z)',
            'decisions': r'##\s*(?:Decisions?|Decision Log)\s*\n(.*?)(?=##|\Z)',
            'next_steps': r'##\s*(?:Next Steps?|Action Items?)\s*\n(.*?)(?=##|\Z)'
        }
        
        for key, pattern in sections.items():
            match = re.search(pattern, md_content, re.DOTALL | re.IGNORECASE)
            if match:
                content = match.group(1).strip()
                # Convert to list if it looks like a list
                if content.startswith('-') or content.startswith('*') or content.startswith('1.'):
                    items = [line.strip('- *0123456789.').strip() 
                           for line in content.split('\n') 
                           if line.strip() and (line.strip().startswith('-') or 
                                               line.strip().startswith('*') or
                                               any(line.strip().startswith(f'{i}.') for i in range(1, 10)))]
                    data[key] = items
                else:
                    data[key] = content
                    
        return data
        
    def _generate_buildstate_summary(self, buildstate_data: Dict[str, Any], 
                                   session_type: SessionType) -> str:
        """Generate concise buildstate summary optimized for session type"""
        combined = buildstate_data['combined']
        
        # Start with enhanced SCF overview if available (uses buildstate._scf_metadata)
        try:
            enhanced_overview = generate_enhanced_overview(self.project_path)
            # If we got a valid enhanced overview, use it as the header
            if enhanced_overview and "Enhanced tracking not available" not in enhanced_overview:
                summary_parts = [enhanced_overview]
                summary_parts.append("\n---\n")  # Separator
            else:
                raise ImportError("Enhanced overview not available")
        except (ImportError, Exception):
            # Fallback to basic project info if enhanced overview fails
            project_info = combined.get('project', {})
            project_name = project_info.get('name', 'Unknown Project')
            project_phase = project_info.get('phase', 'unknown')
            project_type = project_info.get('type', 'unknown')
            
            summary_parts = [f"📋 **{project_name}** ({project_type}, {project_phase} phase)"]
        
        # Session-type specific summaries
        if session_type == SessionType.IMPLEMENTATION:
            # Focus on technical details
            current_state = combined.get('current_state', {})
            implemented = current_state.get('implemented', [])
            in_progress = current_state.get('in_progress', [])
            
            if implemented:
                summary_parts.append(f"✅ **Completed:** {len(implemented)} features implemented")
            if in_progress:
                summary_parts.append(f"🚧 **Active:** {len(in_progress)} features in progress")
                summary_parts.append(f"   - {', '.join(in_progress[:3])}")
                
            # Tech stack
            stack = combined.get('stack', [])
            if stack:
                stack_str = ', '.join(stack[:4]) if isinstance(stack, list) else str(stack)
                summary_parts.append(f"🛠️  **Stack:** {stack_str}")
                
        elif session_type == SessionType.IDEATION:
            # Focus on strategic elements
            objectives = combined.get('objectives', [])
            if objectives:
                summary_parts.append(f"🎯 **Key Objectives:** {len(objectives)} defined")
                summary_parts.append(f"   - {', '.join(objectives[:2])}")
                
            # User stories/features
            features = combined.get('features', [])
            if features:
                summary_parts.append(f"📝 **Features Planned:** {len(features)} user stories")
                
        # Always include recent activity
        session_log = combined.get('session_log', [])
        if session_log:
            latest = session_log[-1]
            summary_parts.append(f"🕒 **Last Activity:** {latest.get('date', 'unknown')} - {latest.get('type', 'update')}")
            
        return '\n'.join(summary_parts)
        
    def _extract_current_objectives(self, buildstate_data: Dict[str, Any], 
                                  session_type: SessionType) -> List[str]:
        """Extract current objectives based on session type"""
        combined = buildstate_data['combined']
        objectives = []
        
        # Direct objectives
        if 'objectives' in combined:
            obj_data = combined['objectives']
            if isinstance(obj_data, list):
                objectives.extend(obj_data)
            elif isinstance(obj_data, str):
                objectives.append(obj_data)
                
        # Session-type specific objective extraction
        if session_type == SessionType.IMPLEMENTATION:
            # Extract from next_steps, in_progress items
            next_steps = combined.get('next_steps', [])
            in_progress = combined.get('current_state', {}).get('in_progress', [])
            objectives.extend(next_steps[:3])
            objectives.extend([f"Complete: {item}" for item in in_progress[:2]])
            
        elif session_type == SessionType.IDEATION:
            # Extract from features, user stories
            features = combined.get('features', [])
            objectives.extend([f"Define: {feature}" for feature in features[:3]])
            
        # Remove duplicates and limit
        unique_objectives = []
        seen = set()
        for obj in objectives:
            if obj and obj not in seen:
                unique_objectives.append(obj)
                seen.add(obj)
                if len(unique_objectives) >= 5:
                    break
                    
        return unique_objectives
        
    def _extract_recent_changes(self, buildstate_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract recent changes and updates"""
        combined = buildstate_data['combined']
        changes = []
        
        # From session_log
        session_log = combined.get('session_log', [])
        for entry in session_log[-3:]:  # Last 3 sessions
            if isinstance(entry, dict):
                changes.append({
                    'date': entry.get('date', 'unknown'),
                    'type': 'session',
                    'description': entry.get('type', 'update'),
                    'details': entry.get('changes', [])
                })
                
        # From change_log
        change_log = combined.get('change_log', [])
        for entry in change_log[-2:]:  # Last 2 changes
            if isinstance(entry, dict):
                changes.append({
                    'date': entry.get('date', 'unknown'),
                    'type': 'change',
                    'description': entry.get('desc', entry.get('description', 'update')),
                    'version': entry.get('version', '')
                })
                
        # Sort by date (most recent first)
        try:
            changes.sort(key=lambda x: x.get('date', ''), reverse=True)
        except:
            pass  # If dates aren't sortable, keep original order
            
        return changes[:5]  # Return max 5 recent changes
        
    def _extract_constraints(self, buildstate_data: Dict[str, Any]) -> List[str]:
        """Extract key constraints and limitations"""
        combined = buildstate_data['combined']
        constraints = []
        
        # Direct constraints
        if 'constraints' in combined:
            const_data = combined['constraints']
            if isinstance(const_data, list):
                constraints.extend(const_data)
            elif isinstance(const_data, str):
                constraints.append(const_data)
                
        # Technical constraints from environment
        env = combined.get('environment', {})
        if env:
            phase = env.get('phase')
            if phase:
                constraints.append(f"Current phase: {phase}")
                
        # Budget/resource constraints
        budget = combined.get('budget', {})
        if budget:
            constraints.append(f"Budget considerations: {budget}")
            
        # Timeline constraints
        timeline = combined.get('timeline', {})
        if timeline:
            constraints.append(f"Timeline: {timeline}")
            
        return constraints[:4]  # Limit to most important
        
    def _extract_ai_rules(self, buildstate_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract AI collaboration rules and preferences"""
        combined = buildstate_data['combined']
        
        # Default AI rules
        ai_rules = {
            'session_tracking': True,
            'capacity_monitoring': True,
            'alert_threshold': '80%',
            'context_preservation': True,
            'learning_capture': True
        }
        
        # Load from buildstate
        if 'ai_rules' in combined:
            ai_rules.update(combined['ai_rules'])
        elif 'ai_context' in combined:
            ai_rules.update(combined['ai_context'])
            
        return ai_rules
        
    def _determine_priority_focus(self, buildstate_data: Dict[str, Any], 
                                focus_areas: List[str] = None) -> str:
        """Determine the priority focus for this session"""
        if focus_areas:
            return f"Focus areas: {', '.join(focus_areas)}"
            
        combined = buildstate_data['combined']
        
        # Check for urgent items
        bugs = combined.get('bugs', [])
        if bugs:
            return f"🚨 Priority: Resolve {len(bugs)} active bugs"
            
        # Check current phase
        project = combined.get('project', {})
        phase = project.get('phase', '').lower()
        
        phase_focuses = {
            'ideation': 'Strategic planning and feature definition',
            'development': 'Implementation and feature building', 
            'testing': 'Quality assurance and bug fixes',
            'deployment': 'Production readiness and optimization',
            'maintenance': 'Performance optimization and improvements'
        }
        
        return phase_focuses.get(phase, 'General development and problem solving')
        
    def _format_for_llm(self, context: SessionContext, llm_type: LLMType) -> str:
        """Format context specifically for target LLM type"""
        
        if llm_type == LLMType.CLAUDE:
            return self._format_for_claude(context)
        elif llm_type == LLMType.GPT:
            return self._format_for_gpt(context)
        elif llm_type == LLMType.GROK:
            return self._format_for_grok(context)
        elif llm_type == LLMType.GEMINI:
            return self._format_for_gemini(context)
        else:
            return self._format_generic(context)
            
    def _format_for_claude(self, context: SessionContext) -> str:
        """Format context optimized for Claude's structured approach"""
        return f"""<project_context>
<buildstate_summary>
{context.buildstate_summary}
</buildstate_summary>

<current_objectives>
{chr(10).join(f"- {obj}" for obj in context.current_objectives)}
</current_objectives>

<recent_activity>
{chr(10).join(f"• {change['date']}: {change['description']}" for change in context.recent_changes[:3])}
</recent_activity>

<session_parameters>
- Session Type: {context.session_type.value}
- Priority Focus: {context.priority_focus}
- AI Rules: {context.ai_rules.get('session_tracking', 'enabled')}
</session_parameters>

<collaboration_guidelines>
- This is a Session Continuity Framework (SCF) project
- Automatically capture decisions and insights during our conversation
- Alert when approaching context limits (80% threshold)
- Maintain focus on current objectives while considering constraints
- Update buildstate continuously until rebalancing triggers
</collaboration_guidelines>
</project_context>

I'm ready to assist with this {context.session_type.value} session. The buildstate context has been loaded and I'll automatically track our progress and decisions. What would you like to work on first?"""

    def _format_for_gpt(self, context: SessionContext) -> str:
        """Format context optimized for GPT's conversational style"""
        return f"""# Project Context - {context.session_type.value.title()} Session

## 📋 Current Project State
{context.buildstate_summary}

## 🎯 Session Objectives
{chr(10).join(f"• {obj}" for obj in context.current_objectives)}

## 🕒 Recent Activity
{chr(10).join(f"- **{change['date']}**: {change['description']}" for change in context.recent_changes[:3])}

## ⚙️ Session Configuration  
- **Focus**: {context.priority_focus}
- **SCF Mode**: Active (automatic progress tracking)
- **Context Monitoring**: {context.ai_rules.get('alert_threshold', '80%')} threshold

---

**Session Continuity Framework Active** 🔄
I'll automatically track our decisions, insights, and progress throughout this session. The buildstate will be updated continuously until rebalancing triggers activate.

Ready to begin! What's our first priority?"""

    def _format_for_grok(self, context: SessionContext) -> str:
        """Format context optimized for Grok's direct approach"""
        return f"""⚡ SCF SESSION ACTIVE ⚡

PROJECT: {context.buildstate_summary.split('**')[1].split('**')[0] if '**' in context.buildstate_summary else 'Current Project'}
MODE: {context.session_type.value.upper()}

🎯 OBJECTIVES:
{chr(10).join(f"→ {obj}" for obj in context.current_objectives[:3])}

📊 RECENT MOVES:
{chr(10).join(f"• {change['description']}" for change in context.recent_changes[:2])}

🔧 FOCUS: {context.priority_focus}

SCF RULES: Auto-tracking ON, Context alerts at {context.ai_rules.get('alert_threshold', '80%')}

Let's build something awesome. What's the mission?"""

    def _format_for_gemini(self, context: SessionContext) -> str:
        """Format context optimized for Gemini's analytical approach"""
        return f"""## Project Analysis Context

### Project Overview
{context.buildstate_summary}

### Current Objectives Analysis
{chr(10).join(f"{i+1}. {obj}" for i, obj in enumerate(context.current_objectives))}

### Recent Development Trajectory  
{chr(10).join(f"- {change['date']}: {change['description']}" for change in context.recent_changes)}

### Session Parameters
- **Session Type**: {context.session_type.value}
- **Priority Focus**: {context.priority_focus}
- **Context Management**: SCF automated tracking enabled

### Collaboration Framework
The Session Continuity Framework (SCF) is active for this project, which means:
- Automatic capture of decisions and technical insights
- Continuous buildstate updates throughout our session
- Context monitoring with alerts at {context.ai_rules.get('alert_threshold', '80%')} capacity
- Intelligent rebalancing triggered by major milestones

I'm prepared to assist with analysis, implementation, and strategic guidance. What aspect would you like to explore first?"""

    def _format_generic(self, context: SessionContext) -> str:
        """Generic format compatible with any LLM"""
        return f"""PROJECT CONTEXT - {context.session_type.value.upper()} SESSION

{context.buildstate_summary}

CURRENT OBJECTIVES:
{chr(10).join(f"• {obj}" for obj in context.current_objectives)}

RECENT CHANGES:
{chr(10).join(f"• {change['description']}" for change in context.recent_changes[:3])}

SESSION FOCUS: {context.priority_focus}

SESSION CONTINUITY FRAMEWORK (SCF) ACTIVE
- Automatic decision tracking
- Progress monitoring 
- Context limit alerts at {context.ai_rules.get('alert_threshold', '80%')}

Ready to proceed. What would you like to work on?"""

    def capture_insight(self, content: str, insight_type: str = 'learning', 
                       confidence: float = 0.8, impact_level: int = 5,
                       tags: List[str] = None, source_context: str = ""):
        """Capture insight or learning during session
        
        Args:
            content: The insight content
            insight_type: Type of insight (decision, learning, pattern, issue, solution)
            confidence: Confidence level 0.0-1.0
            impact_level: Impact level 1-10
            tags: Optional tags for categorization
            source_context: Context where insight was discovered
        """
        insight = SessionInsight(
            timestamp=datetime.now(),
            content=content,
            insight_type=insight_type,
            confidence=confidence,
            impact_level=impact_level,
            tags=tags or [],
            source_context=source_context
        )
        
        self.session_insights.append(insight)
        
        # Auto-update buildstate for high-impact insights
        if impact_level >= 7:
            self._auto_update_buildstate(insight)
            
    def capture_decision(self, decision: str, impact: int = 5, 
                        rationale: str = "", alternatives: List[str] = None):
        """Capture a decision made during the session"""
        decision_content = f"DECISION: {decision}"
        if rationale:
            decision_content += f"\nRationale: {rationale}"
        if alternatives:
            decision_content += f"\nAlternatives considered: {', '.join(alternatives)}"
            
        self.capture_insight(
            content=decision_content,
            insight_type='decision',
            confidence=0.9,
            impact_level=impact,
            tags=['decision', 'architecture'] if 'architecture' in decision.lower() else ['decision']
        )
        
    def track_feature_progress(self, feature_name: str, status: str, 
                             completion: float = 0.0, notes: str = ""):
        """Track progress on specific features"""
        progress_content = f"PROGRESS: {feature_name} -> {status}"
        if completion > 0:
            progress_content += f" ({completion:.0%} complete)"
        if notes:
            progress_content += f"\nNotes: {notes}"
            
        self.capture_insight(
            content=progress_content,
            insight_type='progress',
            confidence=0.9,
            impact_level=6,
            tags=['progress', feature_name.replace('-', '_')]
        )
        
    def _auto_update_buildstate(self, insight: SessionInsight):
        """Automatically update buildstate with high-impact insights"""
        if not self.buildstate_json_path or not self.buildstate_json_path.exists():
            return
            
        try:
            # Load current buildstate
            with open(self.buildstate_json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # Add insight to session log
            if 'session_log' not in data:
                data['session_log'] = []
                
            # Create session log entry
            log_entry = {
                'date': insight.timestamp.strftime('%Y-%m-%d'),
                'time': insight.timestamp.strftime('%H:%M:%S'),
                'type': f'ai_session_{insight.insight_type}',
                'content': insight.content[:200] + ('...' if len(insight.content) > 200 else ''),
                'impact': insight.impact_level,
                'confidence': insight.confidence,
                'session_id': self.current_session_id
            }
            
            data['session_log'].append(log_entry)
            
            # Update decisions section for decision insights
            if insight.insight_type == 'decision':
                if 'decisions' not in data:
                    data['decisions'] = []
                    
                decision_entry = {
                    'date': insight.timestamp.isoformat(),
                    'decision': insight.content,
                    'impact': insight.impact_level,
                    'session_id': self.current_session_id
                }
                data['decisions'].append(decision_entry)
                
            # Save updated buildstate
            with open(self.buildstate_json_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            print(f"⚠️  Error auto-updating buildstate: {e}")
            
    def get_session_summary(self) -> Dict[str, Any]:
        """Get summary of current session insights"""
        if not self.session_insights:
            return {'message': 'No insights captured yet'}
            
        # Group insights by type
        by_type = {}
        for insight in self.session_insights:
            if insight.insight_type not in by_type:
                by_type[insight.insight_type] = []
            by_type[insight.insight_type].append(insight)
            
        # Calculate metrics
        high_impact = [i for i in self.session_insights if i.impact_level >= 7]
        avg_confidence = sum(i.confidence for i in self.session_insights) / len(self.session_insights)
        
        return {
            'session_duration': str(datetime.now() - self.session_start_time) if self.session_start_time else 'unknown',
            'total_insights': len(self.session_insights),
            'high_impact_insights': len(high_impact),
            'average_confidence': avg_confidence,
            'insights_by_type': {k: len(v) for k, v in by_type.items()},
            'recent_insights': [
                {
                    'content': i.content[:100] + ('...' if len(i.content) > 100 else ''),
                    'type': i.insight_type,
                    'impact': i.impact_level
                }
                for i in self.session_insights[-3:]
            ]
        }
        
    def complete_session(self, trigger_rebalancing: bool = True, 
                        session_summary: str = "") -> Dict[str, Any]:
        """Complete session and optionally trigger rebalancing"""
        completion_time = datetime.now()
        
        # Generate session completion summary
        summary = self.get_session_summary()
        
        # End analytics session
        if self.analytics:
            # Estimate time saved for now, can be refined later
            time_saved_estimate = summary.get('high_impact_insights', 0) * 5
            self.analytics.end_session(
                time_saved_minutes=time_saved_estimate,
                context_reused=True # Assume context was reused
            )

        # Update buildstate with session completion
        if self.buildstate_json_path and self.buildstate_json_path.exists():
            try:
                with open(self.buildstate_json_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                # Add session completion log
                if 'session_log' not in data:
                    data['session_log'] = []
                    
                completion_entry = {
                    'date': completion_time.strftime('%Y-%m-%d'),
                    'time': completion_time.strftime('%H:%M:%S'),
                    'type': 'ai_session_complete',
                    'session_id': self.current_session_id,
                    'duration': str(completion_time - self.session_start_time) if self.session_start_time else 'unknown',
                    'insights_captured': summary['total_insights'],
                    'high_impact_insights': summary['high_impact_insights'],
                    'summary': session_summary
                }
                
                data['session_log'].append(completion_entry)
                
                # Save updated buildstate
                with open(self.buildstate_json_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                    
            except Exception as e:
                print(f"⚠️  Error updating buildstate on session completion: {e}")
                
        # Trigger rebalancing if requested
        rebalance_result = None
        if trigger_rebalancing:
            rebalance_result = self._trigger_rebalancing()
            
        # Log the conversation
        log_summary = f"Session completed with {summary.get('total_insights', 0)} insights captured."
        if session_summary:
            log_summary += f" User summary: {session_summary}"
        self.log_conversation(self.current_session_id, log_summary)

        # Reset session state
        completion_summary = {
            'session_id': self.current_session_id,
            'completion_time': completion_time.isoformat(),
            'session_summary': summary,
            'rebalancing_triggered': trigger_rebalancing,
            'rebalance_result': rebalance_result
        }
        
        self.current_session_id = None
        self.session_start_time = None
        self.session_insights = []
        
        return completion_summary

    def log_conversation(self, session_id: str, summary: str, commit_hash: Optional[str] = None):
        """Logs a conversation summary to the buildstate."""
        if not self.buildstate_json_path or not self.buildstate_json_path.exists():
            print("⚠️  Cannot log conversation, buildstate.json not found.")
            return

        try:
            with open(self.buildstate_json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            if '_conversation_log' not in data:
                data['_conversation_log'] = []

            log_entry = {
                "session_id": session_id,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "summary": summary,
                "commit_hash": commit_hash
            }
            data['_conversation_log'].append(log_entry)

            with open(self.buildstate_json_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print("✅ Conversation logged successfully.")

        except Exception as e:
            print(f"⚠️  Error logging conversation: {e}")
        
    def _trigger_rebalancing(self) -> Dict[str, Any]:
        """Trigger SCF rebalancing process"""
        try:
            from scf_rebalancer import SCFBuildstateRebalancer
            
            rebalancer = SCFBuildstateRebalancer()
            
            # Analyze current balance
            if self.buildstate_json_path:
                analysis = rebalancer.analyze_buildstate_balance(str(self.buildstate_json_path))
                
                # Trigger rebalancing if needed
                if analysis.needs_rebalancing:
                    result = rebalancer.rebalance_buildstate(str(self.buildstate_json_path))
                    return {
                        'triggered': True,
                        'balance_score_before': analysis.balance_score,
                        'balance_score_after': result.get('new_balance_score'),
                        'changes_made': result.get('changes_applied', [])
                    }
                else:
                    return {
                        'triggered': False,
                        'reason': 'Balance score acceptable',
                        'current_balance': analysis.balance_score
                    }
                    
        except ImportError:
            return {
                'triggered': False,
                'error': 'SCF rebalancer not available'
            }
        except Exception as e:
            return {
                'triggered': False,
                'error': f'Rebalancing error: {e}'
            }
            
    def generate_agents_md(self, output_path: Optional[Path] = None) -> str:
        """Generate AGENTS.md from SCF buildstate for ecosystem compatibility"""
        if output_path is None:
            output_path = self.project_path / "AGENTS.md"
            
        # Load buildstate data
        buildstate_data = self._load_buildstate_data()
        if not buildstate_data:
            return ""
            
        combined = buildstate_data.get('combined', {})
        
        # Generate AGENTS.md content
        content = f"""# AGENTS.md

## Project Overview
{combined.get('project', {}).get('name', 'SCF Project')} - {combined.get('meta', {}).get('purpose', 'Session Continuity Framework project')}

**Phase**: {combined.get('environment', {}).get('phase', 'Development')}  
**Stack**: {', '.join(combined.get('stack', []))}

## Setup Commands
- Install deps: `{combined.get('tasks', {}).get('start', 'npm install')}`
- Start dev: `{combined.get('tasks', {}).get('test', 'npm start')}`
- Run tests: `{combined.get('tasks', {}).get('test', 'npm test')}`

## Code Style & Standards
"""
        
        # Add coding standards
        standards = combined.get('coding_standards', {})
        if standards:
            if 'organization' in standards:
                content += f"- Organization: {standards['organization']}\n"
            if 'naming' in standards:
                naming = standards['naming']
                content += "- Naming conventions:\n"
                for key, value in naming.items():
                    content += f"  - {key}: {value}\n"
            if 'errors' in standards:
                content += f"- Error handling: {', '.join(standards['errors'])}\n"
            if 'performance' in standards:
                content += f"- Performance: {', '.join(standards['performance'])}\n"

        # Add AI rules
        ai_rules = combined.get('ai_rules', {})
        if ai_rules:
            content += "\n## AI Session Guidelines\n"
            content += f"- Purpose: {ai_rules.get('purpose', 'Technical development sessions')}\n"
            content += f"- Context: {ai_rules.get('session', 'Load buildstate.json for technical work')}\n"
            content += f"- Tracking: {ai_rules.get('track', 'Monitor context usage')}\n"
            content += f"- Updates: {ai_rules.get('update', 'Update buildstate with changes')}\n"

        # Add current objectives
        current_objectives = combined.get('session_objectives', {}).get('current', [])
        if current_objectives:
            content += "\n## Current Focus Areas\n"
            for obj in current_objectives[:5]:  # Top 5 objectives
                content += f"- {obj}\n"

        # Add next steps
        next_steps = combined.get('next_steps', [])
        if next_steps:
            content += "\n## Immediate Next Steps\n"
            for step in next_steps[:5]:  # Top 5 steps
                content += f"- {step}\n"

        # Add SCF integration note
        content += """
## SCF Integration Active
This project uses Session Continuity Framework (SCF):
- Buildstate files provide complete project context
- Session insights automatically captured
- Cross-project pattern learning enabled
- Use `buildstate.json` for technical sessions, `buildstate.md` for ideation

Generated from SCF buildstate for agents.md ecosystem compatibility.
"""

        # Write to file if output path provided
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
                
        return content

    def generate_copilot_instructions(self, output_path: Optional[Path] = None, 
                                       max_length: int = 4000) -> str:
        """Generate .github/copilot-instructions.md from SCF buildstate
        
        GitHub Copilot uses this file for repository-wide context in all features:
        - Copilot Chat, inline completions, code review, coding agent
        - Combined with AGENTS.md (lower precedence) for full context
        - 4000 char limit for code review, unlimited for Chat
        
        Args:
            output_path: Where to write copilot-instructions.md (default: .github/)
            max_length: Max chars (4000 for code review compatibility)
        """
        if output_path is None:
            output_path = self.project_path / ".github" / "copilot-instructions.md"
            
        # Ensure .github directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
            
        # Load buildstate data
        buildstate_data = self._load_buildstate_data()
        if not buildstate_data:
            return ""
            
        combined = buildstate_data.get('combined', {})
        
        # Build concise instructions (optimized for Copilot's guidelines)
        sections = []
        
        # 1. Project Overview (required per Copilot docs)
        project_name = combined.get('project', {}).get('name', 'SCF Project')
        purpose = combined.get('meta', {}).get('purpose', 'Session Continuity Framework project')
        sections.append(f"# Project Overview\n\n{project_name} - {purpose}")
        
        # 2. Folder Structure (required per Copilot docs)
        structure = combined.get('file_structure', {})
        if structure:
            sections.append("\n## Folder Structure\n")
            for key, desc in list(structure.items())[:8]:  # Top 8 folders
                sections.append(f"- `{key}`: {desc}")
        
        # 3. Libraries and Frameworks (required per Copilot docs)
        stack = combined.get('stack', [])
        if stack:
            sections.append(f"\n## Libraries and Frameworks\n\n{', '.join(stack[:10])}")
        
        # 4. Coding Standards (required per Copilot docs)
        standards = combined.get('coding_standards', {})
        if standards:
            sections.append("\n## Coding Standards\n")
            if 'naming' in standards:
                naming = standards['naming']
                for key, value in list(naming.items())[:5]:  # Top 5 conventions
                    sections.append(f"- {key}: {value}")
            if 'organization' in standards:
                sections.append(f"- Code organization: {standards['organization']}")
            if 'errors' in standards and standards['errors']:
                sections.append(f"- Error handling: {standards['errors'][0]}")
        
        # 5. Build/Run Commands
        tasks = combined.get('tasks', {})
        if tasks:
            sections.append("\n## Common Commands\n")
            if 'start' in tasks:
                sections.append(f"- Start dev: `{tasks['start']}`")
            if 'test' in tasks:
                sections.append(f"- Run tests: `{tasks['test']}`")
            if 'build' in tasks:
                sections.append(f"- Build: `{tasks['build']}`")
        
        # 6. Current Phase & Context
        phase = combined.get('environment', {}).get('phase', 'development')
        sections.append(f"\n## Development Phase\n\nCurrently in **{phase}** phase.")
        
        # 7. Key Constraints
        constraints = combined.get('constraints', [])
        if constraints:
            sections.append("\n## Project Constraints\n")
            for constraint in constraints[:5]:  # Top 5
                sections.append(f"- {constraint}")
        
        # Combine all sections
        content = "\n".join(sections)
        
        # Add SCF note (minimal)
        content += "\n\n<!-- SCF: Session Continuity Framework active. See buildstate.json/md for full context. -->"
        
        # Trim to max_length if needed (preserve complete sentences)
        if len(content) > max_length:
            content = content[:max_length].rsplit('\n', 1)[0]
            content += "\n\n<!-- Content truncated to 4000 chars for code review compatibility -->"
        
        # Write to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
                
        return content

    def generate_path_instructions(self, path: str, output_dir: Optional[Path] = None) -> str:
        """Generate path-specific instructions for a directory
        
        GitHub Copilot uses .github/instructions/**/NAME.instructions.md for
        path-specific context (e.g., different rules for /src vs /tests).
        
        Args:
            path: Directory path (e.g., 'src', 'tests', 'docs')
            output_dir: Where to write (default: .github/instructions/)
        """
        if output_dir is None:
            output_dir = self.project_path / ".github" / "instructions"
            
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / f"{path.replace('/', '-')}.instructions.md"
        
        # Load buildstate data
        buildstate_data = self._load_buildstate_data()
        if not buildstate_data:
            return ""
            
        combined = buildstate_data.get('combined', {})
        
        # Generate path-specific content
        content = f"# Instructions for `{path}/`\n\n"
        
        # Customize based on common directory patterns
        if 'src' in path or 'lib' in path:
            content += "## Source Code Guidelines\n"
            standards = combined.get('coding_standards', {})
            if standards.get('naming'):
                content += "- Follow project naming conventions\n"
            if standards.get('errors'):
                content += f"- Error handling: {standards['errors'][0]}\n"
            content += "- Prioritize readability and maintainability\n"
            
        elif 'test' in path:
            content += "## Testing Guidelines\n"
            content += "- Write clear, descriptive test names\n"
            content += "- Follow AAA pattern (Arrange, Act, Assert)\n"
            content += "- Test edge cases and error conditions\n"
            
        elif 'doc' in path:
            content += "## Documentation Guidelines\n"
            content += "- Use clear, concise language\n"
            content += "- Include code examples where helpful\n"
            content += "- Keep docs in sync with code changes\n"
            
        else:
            # Generic instructions
            standards = combined.get('coding_standards', {})
            if standards:
                content += "Follow project coding standards:\n"
                for key, value in list(standards.get('naming', {}).items())[:3]:
                    content += f"- {key}: {value}\n"
        
        # Add SCF note
        content += "\n<!-- Generated by SCF for path-specific Copilot context -->"
        
        # Write to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
                
        return content

    def generate_prompt_files(self, output_dir: Optional[Path] = None) -> Dict[str, str]:
        """Generate reusable prompt files for SCF workflows
        
        Prompt files (*.prompt.md) are reusable templates for common tasks.
        Available in VS Code and JetBrains IDEs (public preview).
        
        Returns: Dict mapping prompt file names to their content
        """
        if output_dir is None:
            output_dir = self.project_path / ".github" / "prompts"
            
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Load buildstate for context
        buildstate_data = self._load_buildstate_data()
        combined = buildstate_data.get('combined', {}) if buildstate_data else {}
        
        prompts = {}
        
        # 1. SCF Initialize Prompt
        prompts['scf-init.prompt.md'] = """# Initialize SCF for New Project

Your goal is to set up Session Continuity Framework for a new project.

Ask for the project details if not provided:
- Project name and purpose
- Tech stack
- Development phase

Then execute:
```bash
python init_scf.py --path <project-path> --interactive
```

Follow the initialization wizard and confirm all settings.
"""

        # 2. SCF Update Prompt
        prompts['scf-update.prompt.md'] = """# Update SCF Buildstate

Your goal is to update and rebalance the buildstate for this project.

Check current balance:
```bash
python update_scf.py --path . --dry-run
```

If rebalancing needed:
```bash
python update_scf.py --path . --rebalance
```

Review changes and confirm updates to AGENTS.md and LLM context.
"""

        # 3. SCF Feature Workflow
        prompts['scf-feature.prompt.md'] = f"""# Add Feature with SCF Context

Your goal is to implement a new feature with full SCF tracking.

Requirements:
- Follow coding standards: [buildstate.json](../buildstate.json)
- Update feature status in buildstate
- Track decisions and learnings
- Write tests per project standards

Steps:
1. Review current objectives in buildstate
2. Implement feature following standards
3. Update buildstate with progress
4. Add entry to session_log

Current stack: {', '.join(combined.get('stack', ['See buildstate']))}
"""

        # 4. SCF Debug Workflow
        prompts['scf-debug.prompt.md'] = """# Debug with SCF History

Your goal is to debug an issue using buildstate context.

Context available:
- Recent changes: [buildstate.json](../buildstate.json) → decisions[]
- Session log: buildstate.json → session_log[]
- Known issues: buildstate.md → Known Issues section

Steps:
1. Check session_log for recent changes
2. Review decisions[] for architectural context
3. Use buildstate.md for known issues
4. Document solution in buildstate
"""

        # Write all prompt files
        for filename, content in prompts.items():
            output_path = output_dir / filename
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
        
        return prompts

    def check_session_state(self) -> Dict[str, Any]:
        """Check if another AI session modified the project (self-aware buildstate)
        
        Returns:
            Dict with session state and whether review is required
        """
        main_buildstate = self.project_path / "buildstate.json"
        
        if not main_buildstate.exists():
            return {
                'error': 'No buildstate.json found',
                'requires_review': False
            }
        
        try:
            with open(main_buildstate, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            session_state = data.get('_session_state', {})
            
            result = {
                'last_session_id': session_state.get('last_session_id'),
                'last_modified_by': session_state.get('last_modified_by'),
                'last_modified_at': session_state.get('last_modified_at'),
                'session_count': session_state.get('session_count', 0),
                'requires_review': session_state.get('requires_review', False),
                'review_reason': session_state.get('review_reason'),
                'is_first_session': session_state.get('last_modified_by') is None,
                'message': None
            }
            
            # Determine if review is needed
            if result['requires_review']:
                result['message'] = f"⚠️ Review required: {result['review_reason']}"
            elif result['is_first_session']:
                result['message'] = "✅ First session - no prior changes to review"
            else:
                result['message'] = f"📋 Last modified by: {result['last_modified_by']} at {result['last_modified_at']}"
            
            return result
            
        except Exception as e:
            return {
                'error': f'Error reading session state: {e}',
                'requires_review': False
            }

    def update_session_state(self, session_id: str, modified_by: str, 
                            requires_review: bool = False, 
                            review_reason: Optional[str] = None) -> bool:
        """Update session state after AI session (marks who modified buildstate)
        
        Args:
            session_id: Unique session identifier
            modified_by: AI name and timestamp (e.g., "Claude-2025-11-10T14:30")
            requires_review: Set true if significant changes made
            review_reason: Brief description of changes for next session
        
        Returns:
            True if successful, False otherwise
        """
        main_buildstate = self.project_path / "buildstate.json"
        
        if not main_buildstate.exists():
            return False
        
        try:
            with open(main_buildstate, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Update or create _session_state
            if '_session_state' not in data:
                data['_session_state'] = {}
            
            data['_session_state']['last_session_id'] = session_id
            data['_session_state']['last_modified_by'] = modified_by
            data['_session_state']['last_modified_at'] = datetime.now().isoformat()
            data['_session_state']['session_count'] = data['_session_state'].get('session_count', 0) + 1
            data['_session_state']['requires_review'] = requires_review
            data['_session_state']['review_reason'] = review_reason
            
            # Write back
            with open(main_buildstate, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            return True
            
        except Exception as e:
            print(f"Error updating session state: {e}")
            return False

    def generate_self_aware_context(self, session_id: str, ai_name: str = "AI") -> str:
        """Generate context with self-awareness check (for AI to read first thing)
        
        This is the main entry point for self-aware buildstate.
        AI reads this first, checks if another AI made changes, and decides whether to review.
        
        Args:
            session_id: Current AI session ID
            ai_name: Name of current AI (e.g., "Claude", "GPT-4", "Copilot")
        
        Returns:
            Formatted context with self-awareness protocol
        """
        # Check session state
        state = self.check_session_state()
        
        context = f"""# 🤖 SCF Self-Aware Buildstate - Session Start

**Session ID**: {session_id}
**AI**: {ai_name}
**Project**: {self.project_path.name}

---

## Session State Check

{state.get('message', 'No session state')}

"""
        
        # If review is required or another AI modified
        if state.get('requires_review') or (not state.get('is_first_session') and state.get('last_modified_by')):
            # Detect changes
            changes = self.detect_recent_changes(since_hours=168)  # Last week
            
            if changes.get('requires_review'):
                context += """
⚠️ **ATTENTION: Changes detected from another AI session!**

Another AI has modified this project. You MUST review changes before proceeding.

"""
                # Add change review prompt
                review = self.generate_change_review_prompt(changes)
                context += review
            else:
                context += """
✅ **No significant changes detected.**

Previous AI session(s) accessed the project but made no high-impact changes.
You may proceed with normal workflow.

"""
        else:
            context += """
✅ **First session or no prior changes.**

This is either the first AI session for this project, or previous sessions made no changes.
You may proceed with normal workflow.

"""
        
        # Add instruction to update session state at end
        context += f"""

---

## 📝 Your Responsibility

**Before closing this session**, update session state:

```python
# Example (adapt to your environment):
integrator.update_session_state(
    session_id="{session_id}",
    modified_by="{ai_name}-{datetime.now().strftime('%Y-%m-%dT%H:%M')}",
    requires_review=True,  # Set True if you made significant changes
    review_reason="Brief description of what changed"
)
```

Or manually update `buildstate.json` → `_session_state`:
- `last_session_id`: "{session_id}"
- `last_modified_by`: "{ai_name}-{datetime.now().strftime('%Y-%m-%dT%H:%M')}"
- `last_modified_at`: "{datetime.now().isoformat()}"
- `session_count`: {state.get('session_count', 0) + 1}
- `requires_review`: true/false
- `review_reason`: "what you changed"

---

## 📚 Full Project Context

"""
        
        # Add full buildstate context
        full_context = self.prepare_session_context(SessionType.IMPLEMENTATION, LLMType.GENERIC)
        context += full_context.formatted_context
        
        return context

    def detect_recent_changes(self, since_hours: int = 24) -> Dict[str, Any]:
        """Detect changes in buildstate since last session or specified time
        
        Returns:
            Dict with new decisions, next_steps, features, bugs, and metadata
        """
        # Always use main buildstate.json for change detection (not library)
        main_buildstate = self.project_path / "buildstate.json"
        
        if not main_buildstate.exists():
            return {'error': 'No buildstate.json found - use main project file for tracking changes'}
        
        try:
            with open(main_buildstate, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            cutoff_time = datetime.now().timestamp() - (since_hours * 3600)
            
            changes = {
                'new_decisions': [],
                'new_next_steps': [],
                'modified_features': [],
                'new_bugs': [],
                'updated_stack': [],
                'change_summary': {},
                'requires_review': False
            }
            
            # Check decisions for recent entries
            for decision in data.get('decisions', []):
                decision_date = decision.get('date', '')
                try:
                    # Parse date and check if recent
                    dt = datetime.strptime(decision_date, '%Y-%m-%d')
                    # Compare dates directly (ignore time portion)
                    cutoff_date = datetime.fromtimestamp(cutoff_time)
                    if dt >= cutoff_date:
                        changes['new_decisions'].append({
                            'date': decision_date,
                            'decision': decision.get('decision', ''),
                            'impact': decision.get('impact', 0),
                            'rationale': decision.get('rationale', ''),
                            'context': decision.get('context', '')
                        })
                except (ValueError, AttributeError):
                    pass
            
            # Check next_steps for new items (simple check - no timestamps)
            next_steps = data.get('next_steps', [])
            if next_steps:
                # Flag any that aren't marked as complete
                for step in next_steps:
                    if not step.startswith('✅'):
                        changes['new_next_steps'].append(step)
            
            # Check features for status changes
            for feature in data.get('features', []):
                if feature.get('status') in ['🔄', '🚧', '⚠️']:  # In progress, blocked, warning
                    changes['modified_features'].append({
                        'id': feature.get('id'),
                        'name': feature.get('name'),
                        'status': feature.get('status'),
                        'priority': feature.get('priority')
                    })
            
            # Check for new bugs
            bugs = data.get('bugs', [])
            if bugs:
                changes['new_bugs'] = bugs
            
            # Determine if review is required
            changes['requires_review'] = (
                len(changes['new_decisions']) > 0 or
                len(changes['new_next_steps']) > 0 or
                len(changes['modified_features']) > 0 or
                len(changes['new_bugs']) > 0
            )
            
            # Summary
            changes['change_summary'] = {
                'total_new_decisions': len(changes['new_decisions']),
                'high_impact_decisions': len([d for d in changes['new_decisions'] if d['impact'] >= 7]),
                'pending_next_steps': len(changes['new_next_steps']),
                'features_in_progress': len(changes['modified_features']),
                'open_bugs': len(changes['new_bugs'])
            }
            
            return changes
            
        except Exception as e:
            return {'error': f'Error detecting changes: {e}'}

    def generate_change_review_prompt(self, changes: Optional[Dict[str, Any]] = None) -> str:
        """Generate a prompt for LLM to review recent changes and assess impact
        
        This creates a structured prompt that:
        1. Presents recent changes
        2. Asks LLM to assess impact and risks
        3. Requests recommendations
        4. Requires explicit approval before implementation
        """
        if changes is None:
            changes = self.detect_recent_changes()
        
        if not changes.get('requires_review'):
            return "✅ No recent changes detected. Project is up to date."
        
        prompt = f"""# 🔔 SCF Change Notification - Review Required

## Project Update Detected
Recent changes have been made to this project's buildstate. Please review and assess before proceeding.

---

## 📊 Change Summary
"""
        
        summary = changes.get('change_summary', {})
        if summary:
            prompt += f"""
- **New Decisions**: {summary.get('total_new_decisions', 0)} (High Impact: {summary.get('high_impact_decisions', 0)})
- **Pending Next Steps**: {summary.get('pending_next_steps', 0)}
- **Features In Progress**: {summary.get('features_in_progress', 0)}
- **Open Bugs**: {summary.get('open_bugs', 0)}
"""
        
        # New Decisions Section
        new_decisions = changes.get('new_decisions', [])
        if new_decisions:
            prompt += "\n---\n\n## 🎯 New Decisions (Require Impact Assessment)\n\n"
            for i, decision in enumerate(new_decisions, 1):
                impact_emoji = "🔴" if decision['impact'] >= 8 else "🟡" if decision['impact'] >= 5 else "🟢"
                prompt += f"""
### {i}. {decision['decision']}
- **Date**: {decision['date']}
- **Impact**: {impact_emoji} {decision['impact']}/10
- **Rationale**: {decision['rationale']}
- **Context**: {decision['context']}
"""
        
        # Next Steps Section
        next_steps = changes.get('new_next_steps', [])
        if next_steps:
            prompt += "\n---\n\n## 📋 Pending Next Steps\n\n"
            for i, step in enumerate(next_steps[:10], 1):  # Limit to top 10
                prompt += f"{i}. {step}\n"
        
        # Features Section
        features = changes.get('modified_features', [])
        if features:
            prompt += "\n---\n\n## 🚧 Features In Progress\n\n"
            for feature in features:
                prompt += f"- **{feature['name']}** ({feature['status']}) - Priority: {feature['priority']}\n"
        
        # Bugs Section
        bugs = changes.get('new_bugs', [])
        if bugs:
            prompt += "\n---\n\n## 🐛 Open Bugs\n\n"
            for bug in bugs[:5]:  # Limit to top 5
                prompt += f"- {bug}\n"
        
        # Assessment Instructions
        prompt += """

---

## ⚠️ REQUIRED: Impact & Risk Assessment

Before taking any action, please:

### 1. Review Each Change
Carefully read all new decisions, next steps, and feature updates above.

### 2. Assess Impact & Risks
For each HIGH IMPACT decision (🔴 7+/10), identify:
- **Potential Risks**: What could go wrong?
- **Dependencies**: What else might be affected?
- **Implementation Complexity**: Easy, Medium, or Complex?
- **Resource Requirements**: Time, tools, expertise needed
- **Reversibility**: Can this be easily undone if needed?

### 3. Provide Recommendations
- **Priority Order**: Which items should be addressed first?
- **Cautions**: Any warnings or concerns to raise?
- **Prerequisites**: What needs to be done before implementation?
- **Alternative Approaches**: Are there better ways to achieve the goals?

### 4. Request Approval
**DO NOT implement anything yet.** After your assessment:
- Present your findings and recommendations
- Ask: "May I proceed with implementing [specific changes]?"
- Wait for explicit user approval before taking action

---

## 📝 Your Assessment Format

Please structure your response as:

```
## Impact & Risk Assessment

### High Priority Items
[List items that need immediate attention with risk levels]

### Risk Analysis
[For each high-impact decision, detail risks and concerns]

### Recommendations
[Specific recommendations with reasoning]

### Implementation Order
[Suggested sequence if proceeding]

### Questions & Concerns
[Any clarifications needed before proceeding]

---

**Ready to implement?** Please confirm which changes you approve for implementation.
```

---

**Note**: This review ensures we catch potential issues early and maintain project quality. Thank you for the careful assessment! 🙏
"""
        
        return prompt

    def load_project_context_with_notifications(self, session_type: SessionType = SessionType.IMPLEMENTATION) -> str:
        """Load project and generate context with change notifications if needed
        
        This is the main entry point for LLM sessions. It:
        1. Loads full buildstate context
        2. Detects recent changes
        3. Generates review prompt if changes found
        4. Returns formatted context ready for LLM
        """
        # Detect changes
        changes = self.detect_recent_changes(since_hours=168)  # Last 7 days
        
        # Prepare base context
        context = self.prepare_session_context(session_type, LLMType.GENERIC)
        
        # Add change notification if needed
        if changes.get('requires_review'):
            review_prompt = self.generate_change_review_prompt(changes)
            
            notification = f"""
{review_prompt}

---

## 📚 Full Project Context
{context.formatted_context}
"""
            return notification
        else:
            return context.formatted_context

    def get_context_usage_estimate(self) -> Dict[str, Any]:
        """Estimate current context usage for capacity monitoring"""
        # Calculate estimated token usage
        total_content = ""
        
        # Add buildstate content
        if self.buildstate_json_path and self.buildstate_json_path.exists():
            total_content += self.buildstate_json_path.read_text(encoding='utf-8')
        if self.buildstate_md_path and self.buildstate_md_path.exists():
            total_content += self.buildstate_md_path.read_text(encoding='utf-8')
            
        # Add session insights
        for insight in self.session_insights:
            total_content += insight.content
            
        # Rough token estimation (1 token ≈ 4 characters)
        estimated_tokens = len(total_content) // 4
        
        # Different LLMs have different context limits
        context_limits = {
            LLMType.CLAUDE: 200000,  # Claude 3.5 Sonnet
            LLMType.GPT: 128000,     # GPT-4 Turbo
            LLMType.GROK: 128000,    # Grok estimated
            LLMType.GEMINI: 128000,  # Gemini Pro
            LLMType.GENERIC: 100000  # Conservative estimate
        }
        
        usage_percentages = {}
        for llm_type, limit in context_limits.items():
            percentage = (estimated_tokens / limit) * 100
            usage_percentages[llm_type.value] = {
                'percentage': percentage,
                'estimated_tokens': estimated_tokens,
                'context_limit': limit,
                'alert_needed': percentage >= 80
            }
            
        return {
            'estimated_tokens': estimated_tokens,
            'usage_by_llm': usage_percentages,
            'content_breakdown': {
                'buildstate_files': len(total_content) - sum(len(i.content) for i in self.session_insights),
                'session_insights': sum(len(i.content) for i in self.session_insights)
            }
        }


def create_llm_startup_script(project_path: str, session_type: str = "implementation", 
                            llm_type: str = "claude") -> str:
    """Generate a startup script for LLM sessions
    
    This creates a ready-to-paste context block for starting AI sessions
    with full SCF integration.
    """
    integrator = SCFLLMIntegrator(project_path)
    
    # Convert string parameters to enums
    session_enum = SessionType(session_type.lower())
    llm_enum = LLMType(llm_type.lower())
    
    # Prepare context
    context = integrator.prepare_session_context(session_enum, llm_enum)
    
    return context.formatted_context


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='SCF LLM Integration Engine')
    parser.add_argument('project_path', help='Path to project with buildstate files')
    parser.add_argument('--session-type', choices=['ideation', 'implementation', 'analysis', 'optimization', 'planning'],
                      default='implementation', help='Type of AI session')
    parser.add_argument('--llm-type', choices=['claude', 'gpt', 'grok', 'gemini', 'generic'],
                      default='claude', help='Target LLM type')
    parser.add_argument('--output', help='Save formatted context to file')
    
    args = parser.parse_args()
    
    # Generate startup context
    startup_context = create_llm_startup_script(args.project_path, args.session_type, args.llm_type)
    
    if args.output:
        Path(args.output).write_text(startup_context, encoding='utf-8')
        print(f"💾 LLM startup context saved to: {args.output}")
    else:
        print("🚀 SCF LLM STARTUP CONTEXT")
        print("=" * 50)
        print(startup_context)
        print("=" * 50)
        print("\n📋 Copy the above context to start your AI session with full SCF integration!")