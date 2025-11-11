#!/usr/bin/env python3
"""
SCF Context Orchestration Engine - Intelligent Multi-Tool Integration
===================================================================

This module extends SCF beyond simple LLM integration to become an intelligent context 
orchestration system that:

1. Applies layers of context intelligently (use what's appropriate for each tool/situation)
2. Learns patterns locally within projects for continuous innovation
3. Grows knowledge through trusted source monitoring and cross-project learning
4. Maintains universal continuity while leveraging unique tool strengths
5. Enables seamless multi-agent workflows (e.g., Claude + Cline + VS Code)

The goal is to create a smart context broker that partners with any tool/LLM to maximize
their unique capabilities while eliminating context reinvention and enabling fluid
ideation-to-execution workflows.

Key Principles:
- Universal Continuity: Context flows seamlessly between tools
- Intelligent Adaptation: Each tool gets context optimized for its strengths  
- Local Innovation: Learn patterns within each project for future application
- Trusted Growth: Monitor sources and propagate valuable learnings upward
- Multi-Agent Orchestration: Coordinate tasks across different AI tools
"""

import json
import re
import asyncio
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple, Union, Set
from dataclasses import dataclass, field
from enum import Enum
import subprocess
import requests
from urllib.parse import urlparse

class ContextLayer(Enum):
    """Different layers of context that can be applied intelligently"""
    CORE_PROJECT = "core_project"           # Essential project info (always included)
    TECHNICAL_STACK = "technical_stack"     # Tech stack and architecture details
    USER_PERSONAS = "user_personas"         # User stories and personas
    BUSINESS_CONTEXT = "business_context"   # Business goals and constraints  
    RECENT_ACTIVITY = "recent_activity"     # Latest changes and decisions
    ECOSYSTEM_PATTERNS = "ecosystem_patterns" # Cross-project learnings
    TOOL_SPECIFIC = "tool_specific"         # Optimizations for specific tools
    DOMAIN_EXPERTISE = "domain_expertise"   # Domain-specific knowledge
    PERFORMANCE_DATA = "performance_data"   # Metrics and optimization targets

class ToolType(Enum):
    """Different tools that can be orchestrated through SCF"""
    CLAUDE = "claude"                       # Claude AI (strategic + technical)
    GPT = "gpt"                            # OpenAI GPT (conversational)
    CLINE = "cline"                        # Cline CLI agent (execution)
    VSCODE = "vscode"                      # VS Code extensions (development)
    CURSOR = "cursor"                      # Cursor AI (code editing)
    GITHUB_COPILOT = "github_copilot"     # GitHub Copilot (code completion)
    PERPLEXITY = "perplexity"              # Research and analysis
    CUSTOM_AGENT = "custom_agent"          # Custom AI agents
    
class TrustedSourceType(Enum):
    """Types of trusted sources for knowledge growth"""
    LOCAL_PROJECT = "local_project"         # Other projects on laptop
    GITHUB_REPO = "github_repo"            # Public GitHub repositories
    CORPORATE_DOCS = "corporate_docs"      # Company documentation
    API_DOCS = "api_docs"                  # Technology documentation
    BLOG_POSTS = "blog_posts"              # Technical blogs and articles
    STACKOVERFLOW = "stackoverflow"         # Stack Overflow Q&A
    RESEARCH_PAPERS = "research_papers"    # Academic papers
    COMMUNITY_FORUMS = "community_forums"  # Developer forums

@dataclass
class ContextProfile:
    """Defines context requirements for specific tools/situations"""
    tool_type: ToolType
    required_layers: List[ContextLayer]
    optional_layers: List[ContextLayer]
    max_token_estimate: int
    optimization_focus: str  # 'speed', 'depth', 'creativity', 'precision'
    format_preferences: Dict[str, Any]
    
@dataclass
class LocalInnovation:
    """Captures innovations learned within a specific project"""
    project_id: str
    innovation_name: str
    description: str
    pattern_code: str
    success_metrics: Dict[str, float]
    applicability_scope: str  # 'project_specific', 'tech_stack', 'universal'
    confidence_score: float
    usage_frequency: int
    last_used: datetime
    
@dataclass
class TrustedSource:
    """Represents a trusted source for knowledge updates"""
    source_id: str
    source_type: TrustedSourceType
    location: str  # URL, file path, etc.
    last_checked: datetime
    update_frequency: timedelta  # How often to check
    relevance_score: float  # 0.0-1.0
    project_relevance: Dict[str, float]  # Relevance to specific projects
    content_hash: str  # To detect changes
    
@dataclass
class MultiAgentTask:
    """Represents a task that can be distributed across multiple agents"""
    task_id: str
    description: str
    task_type: str  # 'implementation', 'research', 'optimization', 'testing'
    assigned_agents: List[ToolType]
    context_requirements: List[ContextLayer]
    dependencies: List[str]  # Other task IDs this depends on
    estimated_effort: int  # 1-10 scale
    priority: int  # 1-10 scale
    status: str  # 'pending', 'in_progress', 'completed', 'blocked'
    results: Dict[str, Any]

class SCFContextOrchestrator:
    """Intelligent context orchestration for multi-tool workflows"""
    
    def __init__(self, project_path: Union[str, Path]):
        self.project_path = Path(project_path)
        self.project_id = self._generate_project_id()
        
        # Context management
        self.available_context: Dict[ContextLayer, Any] = {}
        self.tool_profiles: Dict[ToolType, ContextProfile] = {}
        self.active_sessions: Dict[str, Dict[str, Any]] = {}
        
        # Innovation tracking
        self.local_innovations: List[LocalInnovation] = []
        self.pattern_library: Dict[str, Any] = {}
        
        # Trusted sources
        self.trusted_sources: List[TrustedSource] = []
        self.knowledge_graph: Dict[str, Any] = {}
        
        # Multi-agent coordination
        self.active_tasks: List[MultiAgentTask] = []
        self.agent_capabilities: Dict[ToolType, Dict[str, Any]] = {}
        
        self._initialize_system()
        
    def _initialize_system(self):
        """Initialize the orchestration system"""
        self._load_project_context()
        self._setup_tool_profiles()
        # Initialize with placeholder data for demo
        self.trusted_sources = []
        self.local_innovations = []
        self._setup_agent_capabilities()
        
    def _generate_project_id(self) -> str:
        """Generate unique project ID based on path and content"""
        path_str = str(self.project_path.absolute())
        return hashlib.md5(path_str.encode()).hexdigest()[:12]
        
    def _load_project_context(self):
        """Load all available context layers for the project"""
        # Load buildstate files
        buildstate_json = self.project_path / 'buildstate.json'
        buildstate_md = self.project_path / 'buildstate.md'
        
        if buildstate_json.exists():
            with open(buildstate_json, 'r', encoding='utf-8') as f:
                buildstate_data = json.load(f)
                
            self.available_context[ContextLayer.CORE_PROJECT] = self._extract_core_project(buildstate_data)
            self.available_context[ContextLayer.TECHNICAL_STACK] = buildstate_data.get('stack', [])
            self.available_context[ContextLayer.RECENT_ACTIVITY] = buildstate_data.get('session_log', [])
            
        if buildstate_md.exists():
            md_content = buildstate_md.read_text(encoding='utf-8')
            self.available_context[ContextLayer.USER_PERSONAS] = self._extract_personas(md_content)
            self.available_context[ContextLayer.BUSINESS_CONTEXT] = self._extract_business_context(md_content)
            
        # Load additional context layers (placeholder implementations)
        self.available_context[ContextLayer.ECOSYSTEM_PATTERNS] = []
        self.available_context[ContextLayer.PERFORMANCE_DATA] = {}
        
    def _setup_tool_profiles(self):
        """Setup context profiles for different tools"""
        # Claude: Strategic thinking + technical depth
        self.tool_profiles[ToolType.CLAUDE] = ContextProfile(
            tool_type=ToolType.CLAUDE,
            required_layers=[ContextLayer.CORE_PROJECT, ContextLayer.RECENT_ACTIVITY],
            optional_layers=[ContextLayer.BUSINESS_CONTEXT, ContextLayer.USER_PERSONAS, 
                           ContextLayer.ECOSYSTEM_PATTERNS],
            max_token_estimate=200000,
            optimization_focus='depth',
            format_preferences={'style': 'structured_xml', 'include_guidelines': True}
        )
        
        # Cline: Execution-focused with technical precision
        self.tool_profiles[ToolType.CLINE] = ContextProfile(
            tool_type=ToolType.CLINE,
            required_layers=[ContextLayer.CORE_PROJECT, ContextLayer.TECHNICAL_STACK],
            optional_layers=[ContextLayer.RECENT_ACTIVITY, ContextLayer.PERFORMANCE_DATA],
            max_token_estimate=50000,
            optimization_focus='precision',
            format_preferences={'style': 'concise_technical', 'include_commands': True}
        )
        
        # VS Code: Development context with local patterns
        self.tool_profiles[ToolType.VSCODE] = ContextProfile(
            tool_type=ToolType.VSCODE,
            required_layers=[ContextLayer.TECHNICAL_STACK, ContextLayer.CORE_PROJECT],
            optional_layers=[ContextLayer.ECOSYSTEM_PATTERNS, ContextLayer.TOOL_SPECIFIC],
            max_token_estimate=100000,
            optimization_focus='speed',
            format_preferences={'style': 'ide_optimized', 'include_shortcuts': True}
        )
        
        # GPT: Conversational with business context
        self.tool_profiles[ToolType.GPT] = ContextProfile(
            tool_type=ToolType.GPT,
            required_layers=[ContextLayer.CORE_PROJECT, ContextLayer.USER_PERSONAS],
            optional_layers=[ContextLayer.BUSINESS_CONTEXT, ContextLayer.RECENT_ACTIVITY],
            max_token_estimate=128000,
            optimization_focus='creativity',
            format_preferences={'style': 'conversational_markdown', 'include_examples': True}
        )
        
    def _setup_agent_capabilities(self):
        """Define capabilities and strengths of each agent type"""
        self.agent_capabilities = {
            ToolType.CLAUDE: {
                'strengths': ['strategic_thinking', 'complex_reasoning', 'architecture_design'],
                'optimal_tasks': ['system_design', 'problem_analysis', 'strategic_planning'],
                'context_efficiency': 0.9,
                'cost_per_interaction': 0.15,
                'speed_rating': 0.7
            },
            ToolType.CLINE: {
                'strengths': ['code_execution', 'file_manipulation', 'automated_tasks'],
                'optimal_tasks': ['implementation', 'refactoring', 'testing', 'deployment'],
                'context_efficiency': 0.8,
                'cost_per_interaction': 0.05,
                'speed_rating': 0.9
            },
            ToolType.VSCODE: {
                'strengths': ['code_editing', 'debugging', 'local_development'],
                'optimal_tasks': ['coding', 'debugging', 'code_review', 'documentation'],
                'context_efficiency': 0.7,
                'cost_per_interaction': 0.01,
                'speed_rating': 0.95
            },
            ToolType.GPT: {
                'strengths': ['natural_language', 'creative_thinking', 'explanations'],
                'optimal_tasks': ['documentation', 'user_communication', 'brainstorming'],
                'context_efficiency': 0.8,
                'cost_per_interaction': 0.08,
                'speed_rating': 0.8
            }
        }
        
    def intelligent_context_selection(self, tool_type: ToolType, 
                                    task_description: str = None,
                                    context_budget: int = None) -> Dict[str, Any]:
        """Intelligently select appropriate context layers for a specific tool/task"""
        profile = self.tool_profiles.get(tool_type)
        if not profile:
            return self._get_default_context()
            
        selected_context = {}
        token_estimate = 0
        
        # Always include required layers
        for layer in profile.required_layers:
            if layer in self.available_context:
                context_data = self.available_context[layer]
                selected_context[layer.value] = context_data
                token_estimate += self._estimate_tokens(context_data)
                
        # Intelligently select optional layers based on task and budget
        remaining_budget = (context_budget or profile.max_token_estimate) - token_estimate
        
        # Score optional layers by relevance to task
        layer_scores = self._score_optional_layers(profile.optional_layers, task_description)
        
        # Add highest scoring layers that fit in budget
        for layer, score in sorted(layer_scores.items(), key=lambda x: x[1], reverse=True):
            if layer in self.available_context:
                context_data = self.available_context[layer]
                layer_tokens = self._estimate_tokens(context_data)
                
                if layer_tokens <= remaining_budget:
                    selected_context[layer.value] = context_data
                    token_estimate += layer_tokens
                    remaining_budget -= layer_tokens
                    
        return {
            'context_data': selected_context,
            'token_estimate': token_estimate,
            'optimization_focus': profile.optimization_focus,
            'format_preferences': profile.format_preferences
        }
        
    def create_multi_agent_workflow(self, project_goal: str, 
                                  preferred_agents: List[ToolType] = None) -> List[MultiAgentTask]:
        """Break down a project goal into multi-agent tasks"""
        # Analyze the goal to identify task types
        task_analysis = self._analyze_project_goal(project_goal)
        
        # Generate task breakdown
        tasks = []
        task_counter = 0
        
        for task_type, task_info in task_analysis.items():
            # Find optimal agent for this task type
            optimal_agent = self._find_optimal_agent(task_type, preferred_agents)
            
            task = MultiAgentTask(
                task_id=f"task_{self.project_id}_{task_counter:03d}",
                description=task_info['description'],
                task_type=task_type,
                assigned_agents=[optimal_agent],
                context_requirements=task_info['context_needs'],
                dependencies=task_info.get('dependencies', []),
                estimated_effort=task_info['effort'],
                priority=task_info['priority'],
                status='pending',
                results={}
            )
            
            tasks.append(task)
            task_counter += 1
            
        # Optimize task dependencies and parallelization
        optimized_tasks = self._optimize_task_flow(tasks)
        
        self.active_tasks.extend(optimized_tasks)
        return optimized_tasks
        
    def execute_cline_task(self, task: MultiAgentTask) -> Dict[str, Any]:
        """Execute a task through Cline CLI agent"""
        # Prepare Cline-optimized context
        context = self.intelligent_context_selection(ToolType.CLINE, task.description)
        
        # Generate Cline command sequence
        cline_commands = self._generate_cline_commands(task, context)
        
        # Execute through Cline CLI
        results = {}
        for cmd in cline_commands:
            try:
                result = subprocess.run(
                    cmd, 
                    shell=True, 
                    capture_output=True, 
                    text=True,
                    cwd=str(self.project_path)
                )
                
                results[cmd] = {
                    'stdout': result.stdout,
                    'stderr': result.stderr,
                    'returncode': result.returncode
                }
                
            except Exception as e:
                results[cmd] = {'error': str(e)}
                
        # Update task status
        task.status = 'completed' if all(r.get('returncode', -1) == 0 for r in results.values()) else 'failed'
        task.results = results
        
        # Learn from execution patterns
        self._capture_execution_innovation(task, results)
        
        return results
        
    def monitor_trusted_sources(self) -> Dict[str, Any]:
        """Monitor trusted sources for updates and learning opportunities"""
        updates = {}
        
        for source in self.trusted_sources:
            if self._should_check_source(source):
                try:
                    update_info = self._check_source_updates(source)
                    if update_info['has_updates']:
                        # Analyze relevance to current project
                        relevance = self._analyze_source_relevance(source, update_info)
                        
                        if relevance['project_relevance'] > 0.7:
                            updates[source.source_id] = {
                                'source': source,
                                'updates': update_info,
                                'relevance': relevance,
                                'recommended_action': self._recommend_source_action(source, update_info, relevance)
                            }
                            
                except Exception as e:
                    print(f"⚠️  Error checking source {source.source_id}: {e}")
                    
        return updates
        
    def capture_local_innovation(self, innovation_name: str, description: str, 
                               pattern_code: str, success_metrics: Dict[str, float]) -> LocalInnovation:
        """Capture a locally discovered innovation pattern"""
        innovation = LocalInnovation(
            project_id=self.project_id,
            innovation_name=innovation_name,
            description=description,
            pattern_code=pattern_code,
            success_metrics=success_metrics,
            applicability_scope=self._determine_applicability_scope(pattern_code, success_metrics),
            confidence_score=self._calculate_innovation_confidence(success_metrics),
            usage_frequency=1,
            last_used=datetime.now()
        )
        
        self.local_innovations.append(innovation)
        self._update_pattern_library(innovation)
        
        # Determine if this should be contributed upward
        if self._should_contribute_innovation(innovation):
            self._propose_innovation_contribution(innovation)
            
        return innovation
        
    def format_context_for_tool(self, tool_type: ToolType, context_data: Dict[str, Any]) -> str:
        """Format context specifically for a tool's optimal consumption"""
        profile = self.tool_profiles.get(tool_type)
        if not profile:
            return self._format_generic_context(context_data)
            
        format_prefs = profile.format_preferences
        style = format_prefs.get('style', 'generic')
        
        if style == 'structured_xml':
            return self._format_xml_context(context_data, format_prefs)
        elif style == 'concise_technical':
            return self._format_technical_context(context_data, format_prefs)
        elif style == 'conversational_markdown':
            return self._format_conversational_context(context_data, format_prefs)
        elif style == 'ide_optimized':
            return self._format_ide_context(context_data, format_prefs)
        else:
            return self._format_generic_context(context_data)
            
    # Helper methods for internal operations
    def _extract_core_project(self, buildstate_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract core project information"""
        project_info = buildstate_data.get('project', {})
        return {
            'name': project_info.get('name', 'Unknown'),
            'type': project_info.get('type', 'Unknown'),
            'phase': project_info.get('phase', 'Unknown'),
            'version': project_info.get('version', '0.1'),
            'current_objectives': buildstate_data.get('session_objectives', {}).get('current', [])
        }
        
    def _extract_personas(self, md_content: str) -> List[Dict[str, Any]]:
        """Extract user personas from markdown content"""
        personas = []
        persona_pattern = r'####\s*Persona\s*\d*:?\s*(.+?)\n(.*?)(?=####|\n##|\Z)'
        
        matches = re.findall(persona_pattern, md_content, re.DOTALL | re.IGNORECASE)
        for match in matches:
            name = match[0].strip()
            content = match[1].strip()
            personas.append({'name': name, 'description': content})
            
        return personas
        
    def _extract_business_context(self, md_content: str) -> Dict[str, Any]:
        """Extract business context from markdown content"""
        business_context = {}
        
        # Extract key sections
        sections = {
            'mission': r'###\s*Core Mission\s*\n(.*?)(?=###|\n##|\Z)',
            'success_vision': r'###\s*Success Vision\s*\n(.*?)(?=###|\n##|\Z)',
            'constraints': r'###\s*Constraints.*?\n(.*?)(?=###|\n##|\Z)'
        }
        
        for key, pattern in sections.items():
            match = re.search(pattern, md_content, re.DOTALL | re.IGNORECASE)
            if match:
                business_context[key] = match.group(1).strip()
                
        return business_context
        
    def _estimate_tokens(self, data: Any) -> int:
        """Estimate token count for data (rough approximation)"""
        if isinstance(data, str):
            return len(data) // 4
        elif isinstance(data, dict):
            return len(json.dumps(data)) // 4
        elif isinstance(data, list):
            return sum(self._estimate_tokens(item) for item in data)
        else:
            return len(str(data)) // 4
            
    def _score_optional_layers(self, optional_layers: List[ContextLayer], 
                             task_description: str = None) -> Dict[ContextLayer, float]:
        """Score optional context layers by relevance to task"""
        scores = {}
        
        for layer in optional_layers:
            base_score = 0.5  # Default relevance
            
            if task_description:
                # Increase score based on task keywords
                task_lower = task_description.lower()
                
                if layer == ContextLayer.USER_PERSONAS and any(word in task_lower for word in ['user', 'persona', 'story', 'customer']):
                    base_score += 0.3
                elif layer == ContextLayer.BUSINESS_CONTEXT and any(word in task_lower for word in ['business', 'strategy', 'goal', 'revenue']):
                    base_score += 0.3
                elif layer == ContextLayer.TECHNICAL_STACK and any(word in task_lower for word in ['tech', 'code', 'implement', 'build']):
                    base_score += 0.3
                elif layer == ContextLayer.PERFORMANCE_DATA and any(word in task_lower for word in ['performance', 'optimize', 'speed', 'metric']):
                    base_score += 0.3
                    
            scores[layer] = min(base_score, 1.0)
            
        return scores
        
    def _analyze_project_goal(self, goal: str) -> Dict[str, Dict[str, Any]]:
        """Analyze project goal to identify task breakdown"""
        # This is a simplified implementation - in practice would use more sophisticated NLP
        goal_lower = goal.lower()
        
        tasks = {}
        
        # Identify common task patterns
        if any(word in goal_lower for word in ['implement', 'build', 'create', 'develop']):
            tasks['implementation'] = {
                'description': f"Implement core functionality for: {goal}",
                'context_needs': [ContextLayer.TECHNICAL_STACK, ContextLayer.CORE_PROJECT],
                'effort': 7,
                'priority': 8
            }
            
        if any(word in goal_lower for word in ['design', 'architecture', 'plan', 'structure']):
            tasks['design'] = {
                'description': f"Design system architecture for: {goal}",
                'context_needs': [ContextLayer.CORE_PROJECT, ContextLayer.BUSINESS_CONTEXT],
                'effort': 5,
                'priority': 9
            }
            
        if any(word in goal_lower for word in ['test', 'verify', 'validate']):
            tasks['testing'] = {
                'description': f"Test and validate: {goal}",
                'context_needs': [ContextLayer.TECHNICAL_STACK, ContextLayer.PERFORMANCE_DATA],
                'effort': 4,
                'priority': 6,
                'dependencies': ['implementation']
            }
            
        # Default task if no specific patterns found
        if not tasks:
            tasks['general'] = {
                'description': goal,
                'context_needs': [ContextLayer.CORE_PROJECT],
                'effort': 5,
                'priority': 7
            }
            
        return tasks
        
    def _find_optimal_agent(self, task_type: str, preferred_agents: List[ToolType] = None) -> ToolType:
        """Find the optimal agent for a specific task type"""
        if preferred_agents:
            # Filter by preferred agents
            candidates = {agent: caps for agent, caps in self.agent_capabilities.items() 
                         if agent in preferred_agents}
        else:
            candidates = self.agent_capabilities
            
        # Score agents by task fit
        best_agent = None
        best_score = 0
        
        for agent, capabilities in candidates.items():
            score = 0
            
            # Check if task type is in optimal tasks
            if task_type in capabilities.get('optimal_tasks', []):
                score += 0.5
                
            # Add efficiency and speed factors
            score += capabilities.get('context_efficiency', 0) * 0.3
            score += capabilities.get('speed_rating', 0) * 0.2
            
            # Subtract cost factor (lower cost = higher score)
            cost_factor = 1 - min(capabilities.get('cost_per_interaction', 0.5), 1.0)
            score += cost_factor * 0.1
            
            if score > best_score:
                best_score = score
                best_agent = agent
                
        return best_agent or ToolType.CLAUDE  # Default fallback
        
    def _format_xml_context(self, context_data: Dict[str, Any], format_prefs: Dict[str, Any]) -> str:
        """Format context in structured XML style (for Claude)"""
        xml_parts = ["<project_context>"]
        
        for layer_name, layer_data in context_data.items():
            xml_parts.append(f"<{layer_name}>")
            
            if isinstance(layer_data, dict):
                for key, value in layer_data.items():
                    xml_parts.append(f"  <{key}>{value}</{key}>")
            elif isinstance(layer_data, list):
                for item in layer_data:
                    xml_parts.append(f"  <item>{item}</item>")
            else:
                xml_parts.append(f"  {layer_data}")
                
            xml_parts.append(f"</{layer_name}>")
            
        if format_prefs.get('include_guidelines', False):
            xml_parts.extend([
                "<collaboration_guidelines>",
                "- This is an SCF-orchestrated session with intelligent context layering",
                "- Focus on leveraging tool-specific strengths while maintaining universal continuity",
                "- Capture innovations and patterns for local learning and potential upward contribution",
                "</collaboration_guidelines>"
            ])
            
        xml_parts.append("</project_context>")
        return "\n".join(xml_parts)
        
    def _format_technical_context(self, context_data: Dict[str, Any], format_prefs: Dict[str, Any]) -> str:
        """Format context in concise technical style (for Cline)"""
        lines = ["## SCF Context - Technical Execution"]
        
        # Focus on actionable technical information
        if 'core_project' in context_data:
            project = context_data['core_project']
            lines.extend([
                f"PROJECT: {project.get('name', 'Unknown')} v{project.get('version', '0.1')}",
                f"TYPE: {project.get('type', 'Unknown')} | PHASE: {project.get('phase', 'Unknown')}"
            ])
            
        if 'technical_stack' in context_data:
            stack = context_data['technical_stack']
            if stack:
                lines.append(f"STACK: {', '.join(stack) if isinstance(stack, list) else stack}")
                
        if format_prefs.get('include_commands', False):
            lines.extend([
                "",
                "## Available SCF Commands",
                "- scf-status: Show current project status",
                "- scf-innovate: Capture local innovation pattern",
                "- scf-sync: Synchronize with trusted sources"
            ])
            
        return "\n".join(lines)
        
    def _format_conversational_context(self, context_data: Dict[str, Any], format_prefs: Dict[str, Any]) -> str:
        """Format context in conversational markdown style (for GPT)"""
        lines = ["# Project Context - SCF Orchestrated Session"]
        
        if 'core_project' in context_data:
            project = context_data['core_project']
            lines.extend([
                f"## 📋 {project.get('name', 'Project')} Overview",
                f"We're working on a **{project.get('type', 'project')}** currently in the **{project.get('phase', 'unknown')}** phase.",
            ])
            
            objectives = project.get('current_objectives', [])
            if objectives:
                lines.extend([
                    "",
                    "### 🎯 Current Objectives",
                    *[f"- {obj}" for obj in objectives]
                ])
                
        if 'user_personas' in context_data:
            personas = context_data['user_personas']
            if personas:
                lines.extend([
                    "",
                    "### 👥 Key User Personas",
                    *[f"- **{p['name']}**: {p['description'][:100]}..." for p in personas[:3]]
                ])
                
        lines.extend([
            "",
            "---",
            "**SCF Orchestration Active** 🎼",
            "This session benefits from intelligent context layering and multi-tool coordination.",
            "Let's leverage our unique strengths while maintaining universal project continuity!"
        ])
        
        return "\n".join(lines)

    def _format_ide_context(self, context_data: Dict[str, Any], format_prefs: Dict[str, Any]) -> str:
        """Format context for IDE/VS Code integration"""
        lines = ["## SCF Context - IDE Optimized"]
        
        if 'core_project' in context_data:
            project = context_data['core_project']
            lines.extend([
                f"PROJECT: {project.get('name', 'Unknown')}",
                f"TYPE: {project.get('type', 'Unknown')} | PHASE: {project.get('phase', 'Unknown')}"
            ])
            
        if 'technical_stack' in context_data:
            stack = context_data['technical_stack']
            if stack:
                lines.append(f"STACK: {', '.join(stack) if isinstance(stack, list) else stack}")
                
        return "\n".join(lines)
        
    def _format_generic_context(self, context_data: Dict[str, Any]) -> str:
        """Format generic context for any tool"""
        lines = ["# Project Context"]
        
        for layer_name, layer_data in context_data.items():
            lines.append(f"## {layer_name.replace('_', ' ').title()}")
            if isinstance(layer_data, dict):
                for key, value in layer_data.items():
                    lines.append(f"- {key}: {value}")
            elif isinstance(layer_data, list):
                for item in layer_data:
                    lines.append(f"- {item}")
            else:
                lines.append(f"{layer_data}")
                
        return "\n".join(lines)
        
    def _optimize_task_flow(self, tasks: List[MultiAgentTask]) -> List[MultiAgentTask]:
        """Optimize task dependencies and execution order"""
        # Simple implementation - sort by priority and dependencies
        return sorted(tasks, key=lambda t: (len(t.dependencies), -t.priority))
        
    def _generate_cline_commands(self, task: MultiAgentTask, context: Dict[str, Any]) -> List[str]:
        """Generate Cline CLI commands for a task"""
        commands = []
        
        # Extract project context
        context_data = context.get('context_data', {})
        project_info = context_data.get('core_project', {})
        stack = context_data.get('technical_stack', [])
        
        if 'component' in task.description.lower():
            # Component implementation commands
            component_name = "Button"  # Simplified for demo
            commands.extend([
                f"mkdir -p src/components/{component_name}",
                f"touch src/components/{component_name}/{component_name}.tsx",
                f"touch src/components/{component_name}/{component_name}.test.tsx",
                f"touch src/components/{component_name}/index.ts"
            ])
            
        return commands
        
    def _capture_execution_innovation(self, task: MultiAgentTask, results: Dict[str, Any]):
        """Capture innovation patterns from task execution"""
        # Analyze execution results for patterns
        success_rate = sum(1 for r in results.values() if r.get('returncode', -1) == 0) / len(results) if results else 0
        
        if success_rate > 0.8:
            # High success rate - capture as potential innovation
            innovation = LocalInnovation(
                project_id=self.project_id,
                innovation_name=f"Automated {task.task_type} Pattern",
                description=f"Successful automation pattern for {task.description}",
                pattern_code=str(results),
                success_metrics={'automation_success': success_rate},
                applicability_scope='tech_stack',
                confidence_score=success_rate,
                usage_frequency=1,
                last_used=datetime.now()
            )
            self.local_innovations.append(innovation)
            
    def _should_check_source(self, source: TrustedSource) -> bool:
        """Determine if a source should be checked for updates"""
        time_since_check = datetime.now() - source.last_checked
        return time_since_check >= source.update_frequency
        
    def _check_source_updates(self, source: TrustedSource) -> Dict[str, Any]:
        """Check a trusted source for updates"""
        # Placeholder implementation
        return {'has_updates': False, 'changes': []}
        
    def _analyze_source_relevance(self, source: TrustedSource, update_info: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze relevance of source updates to current project"""
        return {'project_relevance': source.relevance_score}
        
    def _recommend_source_action(self, source: TrustedSource, update_info: Dict[str, Any], relevance: Dict[str, Any]) -> str:
        """Recommend action based on source updates"""
        return "review_updates" if relevance['project_relevance'] > 0.7 else "monitor"
        
    def _determine_applicability_scope(self, pattern_code: str, success_metrics: Dict[str, float]) -> str:
        """Determine how broadly applicable an innovation is"""
        avg_success = sum(success_metrics.values()) / len(success_metrics) if success_metrics else 0
        if avg_success > 0.9:
            return 'universal'
        elif avg_success > 0.7:
            return 'tech_stack'
        else:
            return 'project_specific'
            
    def _calculate_innovation_confidence(self, success_metrics: Dict[str, float]) -> float:
        """Calculate confidence score for an innovation"""
        return sum(success_metrics.values()) / len(success_metrics) if success_metrics else 0.5
        
    def _update_pattern_library(self, innovation: LocalInnovation):
        """Update the pattern library with new innovation"""
        if not hasattr(self, 'pattern_library'):
            self.pattern_library = {}
        self.pattern_library[innovation.innovation_name] = innovation
        
    def _should_contribute_innovation(self, innovation: LocalInnovation) -> bool:
        """Determine if innovation should be contributed upward"""
        return innovation.confidence_score > 0.8 and innovation.applicability_scope in ['tech_stack', 'universal']
        
    def _propose_innovation_contribution(self, innovation: LocalInnovation):
        """Propose innovation for upward contribution to SCF ecosystem"""
        print(f"🚀 Innovation '{innovation.innovation_name}' eligible for SCF ecosystem contribution!")
        
    def _get_default_context(self) -> Dict[str, Any]:
        """Get default context when no profile is available"""
        return {
            'context_data': self.available_context,
            'token_estimate': sum(self._estimate_tokens(data) for data in self.available_context.values()),
            'optimization_focus': 'generic',
            'format_preferences': {'style': 'generic'}
        }

    def get_orchestration_status(self) -> Dict[str, Any]:
        """Get current status of the orchestration system"""
        return {
            'project_id': self.project_id,
            'active_sessions': len(self.active_sessions),
            'local_innovations': len(self.local_innovations),
            'trusted_sources': len(self.trusted_sources),
            'active_tasks': len([t for t in self.active_tasks if t.status in ['pending', 'in_progress']]),
            'available_context_layers': list(self.available_context.keys()),
            'configured_tools': list(self.tool_profiles.keys())
        }


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='SCF Context Orchestration Engine')
    parser.add_argument('project_path', help='Path to project directory')
    parser.add_argument('--demo-workflow', help='Demonstrate multi-agent workflow')
    parser.add_argument('--tool', choices=['claude', 'cline', 'vscode', 'gpt'], 
                       help='Generate context for specific tool')
    parser.add_argument('--task', help='Task description for context optimization')
    
    args = parser.parse_args()
    
    orchestrator = SCFContextOrchestrator(args.project_path)
    
    if args.demo_workflow:
        print("🎼 SCF Context Orchestration - Multi-Agent Workflow Demo")
        print("=" * 60)
        
        # Create workflow for the demo goal
        tasks = orchestrator.create_multi_agent_workflow(args.demo_workflow)
        
        print(f"📋 Generated {len(tasks)} orchestrated tasks:")
        for task in tasks:
            agent_name = task.assigned_agents[0].value if task.assigned_agents else 'unknown'
            print(f"  🤖 {agent_name}: {task.description} (Priority: {task.priority}, Effort: {task.estimated_effort})")
            
    elif args.tool:
        tool_type = ToolType(args.tool)
        context_package = orchestrator.intelligent_context_selection(tool_type, args.task)
        formatted_context = orchestrator.format_context_for_tool(tool_type, context_package['context_data'])
        
        print(f"🎯 SCF Context for {args.tool.upper()}")
        print("=" * 50)
        print(formatted_context)
        print("=" * 50)
        print(f"📊 Token Estimate: {context_package['token_estimate']:,}")
        print(f"🎯 Optimization: {context_package['optimization_focus']}")
        
    else:
        status = orchestrator.get_orchestration_status()
        print("🎼 SCF Context Orchestration Status")
        print("=" * 40)
        for key, value in status.items():
            print(f"  {key}: {value}")