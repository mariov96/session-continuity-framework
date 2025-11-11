#!/usr/bin/env python3
"""
SCF Multi-Tool Orchestration Demo - Cline + Claude + VS Code Integration
======================================================================

This demo showcases how SCF orchestrates multiple AI tools to maximize their unique 
strengths while maintaining universal continuity. It demonstrates:

1. Claude for strategic thinking and architecture design
2. Cline for automated execution and file manipulation  
3. VS Code for development environment optimization
4. Context flow between tools without reinvention

The demo shows a realistic workflow where:
- Claude designs the system architecture
- Cline executes the implementation tasks
- VS Code provides development environment insights
- All tools share intelligent context layers appropriate to their strengths
"""

import json
import sys
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

# Add current directory to path for imports
sys.path.append(str(Path(__file__).parent))

try:
    from scf_context_orchestrator import (
        SCFContextOrchestrator, ToolType, ContextLayer, MultiAgentTask
    )
    from scf_llm_integration import SCFLLMIntegrator, SessionType, LLMType
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("Ensure scf_context_orchestrator.py and scf_llm_integration.py are available")
    sys.exit(1)

class SCFMultiToolDemo:
    """Demonstrates intelligent multi-tool orchestration with SCF"""
    
    def __init__(self, project_path: str = None):
        self.project_path = Path(project_path) if project_path else Path.cwd()
        self.demo_project_path = self.project_path / 'scf-multi-tool-demo'
        self.orchestrator = None
        
    def run_complete_demo(self):
        """Run complete multi-tool orchestration demonstration"""
        print("🎼 SCF Multi-Tool Orchestration Demonstration")
        print("=" * 70)
        print("Showcasing: Claude (Strategy) + Cline (Execution) + VS Code (Development)")
        print()
        
        # Phase 1: Setup demo project with different tool contexts
        print("📋 Phase 1: Setting up multi-tool demo environment...")
        self._setup_demo_project()
        
        # Phase 2: Initialize orchestrator
        print("\n🎼 Phase 2: Initializing SCF Context Orchestrator...")
        self.orchestrator = SCFContextOrchestrator(self.demo_project_path)
        status = self.orchestrator.get_orchestration_status()
        self._display_orchestration_status(status)
        
        # Phase 3: Demonstrate intelligent context selection
        print("\n🧠 Phase 3: Demonstrating intelligent context layering...")
        self._demonstrate_context_intelligence()
        
        # Phase 4: Create multi-agent workflow
        print("\n🤖 Phase 4: Creating multi-agent workflow...")
        project_goal = "Build a React component library with automated testing and documentation"
        tasks = self.orchestrator.create_multi_agent_workflow(project_goal)
        self._display_workflow_plan(tasks)
        
        # Phase 5: Execute tasks across different tools
        print("\n⚡ Phase 5: Executing tasks across orchestrated tools...")
        self._demonstrate_tool_execution(tasks)
        
        # Phase 6: Show context continuity
        print("\n🔄 Phase 6: Demonstrating universal continuity across tools...")
        self._demonstrate_context_continuity()
        
        # Phase 7: Capture and propagate innovations
        print("\n💡 Phase 7: Capturing local innovations for ecosystem growth...")
        self._demonstrate_innovation_capture()
        
        print("\n✅ Multi-Tool Orchestration Demo Complete!")
        print(f"\n💡 Key Benefits Demonstrated:")
        print("   • Each tool gets context optimized for its strengths")
        print("   • No context reinvention - universal continuity maintained")
        print("   • Local patterns captured and available for propagation")
        print("   • Cost-effective task distribution based on tool capabilities")
        print("   • Seamless workflow from ideation (Claude) → execution (Cline) → development (VS Code)")
        
    def _setup_demo_project(self):
        """Setup demo project with SCF-enhanced structure"""
        self.demo_project_path.mkdir(exist_ok=True)
        
        # Create buildstate with multi-tool context
        buildstate_data = {
            "_scf_header": {
                "framework": "Session Continuity Framework - Multi-Tool Orchestration",
                "description": "Demonstrates intelligent context orchestration across Claude, Cline, and VS Code",
                "version": "v2.1-multi-tool"
            },
            "project": {
                "name": "React Component Library",
                "type": "component_library",
                "phase": "design_and_implementation",
                "version": "0.1.0"
            },
            "orchestration_config": {
                "preferred_agents": ["claude", "cline", "vscode"],
                "context_optimization": True,
                "cost_awareness": True,
                "parallel_execution": True
            },
            "stack": ["React", "TypeScript", "Storybook", "Jest", "Rollup"],
            "features": [
                "Button component with variants",
                "Input component with validation", 
                "Card component with layouts",
                "Automated testing suite",
                "Storybook documentation",
                "NPM package build"
            ],
            "tool_preferences": {
                "architecture_design": "claude",
                "code_implementation": "cline",
                "development_environment": "vscode",
                "documentation": "claude",
                "testing": "cline",
                "optimization": "vscode"
            },
            "session_objectives": {
                "current": [
                    "Design component architecture with Claude's strategic thinking",
                    "Implement components with Cline's automated execution",
                    "Optimize development environment with VS Code integration",
                    "Maintain context continuity across all tools"
                ]
            },
            "multi_agent_capabilities": {
                "claude": {
                    "optimal_for": ["system_design", "architecture_decisions", "strategic_planning"],
                    "context_needs": ["business_context", "user_personas", "technical_requirements"]
                },
                "cline": {
                    "optimal_for": ["file_creation", "code_generation", "automated_tasks", "testing"],
                    "context_needs": ["technical_stack", "implementation_details", "file_structure"]
                },
                "vscode": {
                    "optimal_for": ["code_editing", "debugging", "environment_setup", "extensions"],
                    "context_needs": ["development_workflow", "tool_configuration", "productivity_patterns"]
                }
            }
        }
        
        # Save buildstate.json
        buildstate_path = self.demo_project_path / 'buildstate.json'
        with open(buildstate_path, 'w', encoding='utf-8') as f:
            json.dump(buildstate_data, f, indent=2)
            
        print(f"   ✅ Enhanced multi-tool buildstate created")
        
        # Create sample project structure
        (self.demo_project_path / 'src' / 'components').mkdir(parents=True, exist_ok=True)
        (self.demo_project_path / 'tests').mkdir(exist_ok=True)
        (self.demo_project_path / 'stories').mkdir(exist_ok=True)
        
        # Sample package.json for realistic context
        package_json = {
            "name": "scf-component-library",
            "version": "0.1.0",
            "description": "React component library built with SCF multi-tool orchestration",
            "main": "dist/index.js",
            "scripts": {
                "build": "rollup -c",
                "test": "jest",
                "storybook": "start-storybook -p 6006",
                "dev": "rollup -c -w"
            },
            "devDependencies": {
                "react": "^18.0.0",
                "typescript": "^4.9.0",
                "rollup": "^3.0.0",
                "@storybook/react": "^6.5.0",
                "jest": "^29.0.0"
            }
        }
        
        with open(self.demo_project_path / 'package.json', 'w') as f:
            json.dump(package_json, f, indent=2)
            
        print(f"   ✅ Project structure and configuration created")
        
    def _display_orchestration_status(self, status: Dict[str, Any]):
        """Display orchestration system status"""
        print(f"   📊 Project ID: {status['project_id']}")
        print(f"   🎯 Available Context Layers: {len(status['available_context_layers'])}")
        print(f"   🛠️  Configured Tools: {len(status['configured_tools'])}")
        print(f"   💡 Local Innovations: {status['local_innovations']}")
        print(f"   📡 Trusted Sources: {status['trusted_sources']}")
        
    def _demonstrate_context_intelligence(self):
        """Show how context is intelligently selected for different tools"""
        task_descriptions = [
            ("claude", "Design the overall component architecture and API design patterns"),
            ("cline", "Implement Button component with TypeScript and automated tests"),
            ("vscode", "Setup development environment with optimal extensions and debugging")
        ]
        
        for tool_name, task_desc in task_descriptions:
            tool_type = ToolType(tool_name)
            context_package = self.orchestrator.intelligent_context_selection(tool_type, task_desc)
            
            print(f"\n   🎯 Context for {tool_name.upper()} ({task_desc[:40]}...):")
            print(f"      📊 Token Estimate: {context_package['token_estimate']:,}")
            print(f"      🎛️  Optimization: {context_package['optimization_focus']}")
            print(f"      📋 Context Layers: {list(context_package['context_data'].keys())}")
            
            # Show formatted context sample
            formatted = self.orchestrator.format_context_for_tool(tool_type, context_package['context_data'])
            sample = formatted[:200] + "..." if len(formatted) > 200 else formatted
            print(f"      📝 Format Sample: {sample}")
            
    def _display_workflow_plan(self, tasks: List[MultiAgentTask]):
        """Display the generated multi-agent workflow plan"""
        print(f"   📋 Generated {len(tasks)} orchestrated tasks:")
        
        # Group tasks by assigned agent
        tasks_by_agent = {}
        for task in tasks:
            agent = task.assigned_agents[0] if task.assigned_agents else 'unknown'
            if agent not in tasks_by_agent:
                tasks_by_agent[agent] = []
            tasks_by_agent[agent].append(task)
            
        for agent, agent_tasks in tasks_by_agent.items():
            agent_name = agent.value if hasattr(agent, 'value') else str(agent)
            print(f"\n   🤖 {agent_name.upper()} ({len(agent_tasks)} tasks):")
            for task in agent_tasks:
                deps = f" (depends: {', '.join(task.dependencies)})" if task.dependencies else ""
                print(f"      • {task.description} [P{task.priority}, E{task.estimated_effort}]{deps}")
                
    def _demonstrate_tool_execution(self, tasks: List[MultiAgentTask]):
        """Demonstrate execution across different tools"""
        print("   🚀 Simulating task execution across tools...")
        
        # Find a Cline task to demonstrate
        cline_tasks = [t for t in tasks if t.assigned_agents and t.assigned_agents[0] == ToolType.CLINE]
        
        if cline_tasks:
            cline_task = cline_tasks[0]
            print(f"\n   ⚡ Executing Cline Task: {cline_task.description}")
            
            # Generate Cline-optimized context
            context_package = self.orchestrator.intelligent_context_selection(ToolType.CLINE, cline_task.description)
            formatted_context = self.orchestrator.format_context_for_tool(ToolType.CLINE, context_package['context_data'])
            
            print(f"      📝 Cline Context Generated ({context_package['token_estimate']:,} tokens):")
            print("      " + "\n      ".join(formatted_context.split('\n')[:8]))
            
            # Simulate Cline commands (in practice, these would execute through Cline CLI)
            simulated_commands = [
                f"mkdir -p {self.demo_project_path}/src/components/Button",
                f"touch {self.demo_project_path}/src/components/Button/Button.tsx",
                f"touch {self.demo_project_path}/src/components/Button/Button.test.tsx",
                f"touch {self.demo_project_path}/src/components/Button/index.ts"
            ]
            
            print(f"\n      🔧 Simulated Cline Commands:")
            for cmd in simulated_commands:
                print(f"         $ {cmd}")
                # Actually create the directories/files for demo
                try:
                    if cmd.startswith('mkdir'):
                        Path(cmd.split()[-1]).mkdir(parents=True, exist_ok=True)
                    elif cmd.startswith('touch'):
                        Path(cmd.split()[-1]).touch()
                    print(f"         ✅ Executed successfully")
                except Exception as e:
                    print(f"         ⚠️  Simulated: {e}")
                    
        # Demonstrate Claude strategic thinking
        claude_tasks = [t for t in tasks if t.assigned_agents and t.assigned_agents[0] == ToolType.CLAUDE]
        if claude_tasks:
            claude_task = claude_tasks[0]
            print(f"\n   🧠 Claude Strategic Analysis: {claude_task.description}")
            
            context_package = self.orchestrator.intelligent_context_selection(ToolType.CLAUDE, claude_task.description)
            print(f"      📊 Context: {context_package['token_estimate']:,} tokens, {context_package['optimization_focus']} focus")
            print(f"      🎯 Strategic Output: Component architecture with modular design principles,")
            print(f"         TypeScript interfaces for props, and accessibility considerations")
            
        # Demonstrate VS Code integration
        vscode_tasks = [t for t in tasks if t.assigned_agents and t.assigned_agents[0] == ToolType.VSCODE]
        if vscode_tasks:
            vscode_task = vscode_tasks[0]
            print(f"\n   💻 VS Code Optimization: {vscode_task.description}")
            print(f"      🔧 Environment Setup: ESLint, Prettier, TypeScript configs")
            print(f"      🎨 Recommended Extensions: React snippets, Auto imports, GitLens")
            print(f"      ⚡ Productivity Boost: Intelligent autocomplete with project context")
            
    def _demonstrate_context_continuity(self):
        """Show how context flows seamlessly between tools"""
        print("   🔄 Universal Continuity Demonstration:")
        
        # Show how the same core information is presented differently for each tool
        core_project_info = {
            'name': 'React Component Library',
            'current_objectives': ['Build reusable Button component', 'Implement automated testing']
        }
        
        tools_demo = [
            (ToolType.CLAUDE, "Strategic architectural decisions"),
            (ToolType.CLINE, "Automated implementation tasks"),
            (ToolType.VSCODE, "Development environment optimization")
        ]
        
        for tool_type, purpose in tools_demo:
            context_package = self.orchestrator.intelligent_context_selection(tool_type, purpose)
            formatted = self.orchestrator.format_context_for_tool(tool_type, context_package['context_data'])
            
            print(f"\n      📤 {tool_type.value.upper()} receives context optimized for {purpose}:")
            
            # Show key differences in formatting
            if tool_type == ToolType.CLAUDE:
                print("         • Structured XML with collaboration guidelines")
                print("         • Business context and strategic objectives emphasized")
            elif tool_type == ToolType.CLINE:
                print("         • Concise technical format with actionable commands")
                print("         • Implementation details and file structures prioritized")
            elif tool_type == ToolType.VSCODE:
                print("         • IDE-optimized with development workflow focus")
                print("         • Tool configuration and productivity patterns highlighted")
                
            print(f"         • Same core information, {tool_type.value}-optimized presentation")
            print(f"         • Zero context loss, maximum tool leverage")
            
    def _demonstrate_innovation_capture(self):
        """Show how local innovations are captured and can be propagated"""
        print("   💡 Local Innovation Capture Demonstration:")
        
        # Simulate discovering a useful pattern during the workflow
        innovation_example = {
            'name': 'Component-Story-Test Trinity Pattern',
            'description': 'Co-located component, Storybook story, and test file with shared TypeScript interfaces',
            'pattern_code': '''
// Pattern: Always create three files together
Button/
  ├── Button.tsx        // Component implementation
  ├── Button.stories.tsx // Storybook documentation
  ├── Button.test.tsx   // Jest tests
  └── types.ts          // Shared TypeScript interfaces
            ''',
            'success_metrics': {
                'development_speed': 0.85,
                'test_coverage': 0.95,
                'documentation_completeness': 0.90,
                'team_adoption': 0.80
            }
        }
        
        # Capture the innovation
        innovation = self.orchestrator.capture_local_innovation(
            innovation_example['name'],
            innovation_example['description'],
            innovation_example['pattern_code'],
            innovation_example['success_metrics']
        )
        
        print(f"      ✨ Captured Innovation: {innovation.innovation_name}")
        print(f"         📊 Confidence Score: {innovation.confidence_score:.2f}")
        print(f"         🎯 Applicability: {innovation.applicability_scope}")
        print(f"         📈 Success Metrics: Avg {sum(innovation.success_metrics.values()) / len(innovation.success_metrics):.2f}")
        
        # Show how it would be considered for upward contribution
        if innovation.confidence_score > 0.8:
            print(f"         🚀 Eligible for SCF ecosystem contribution!")
            print(f"         📡 Would be propagated to organization and global libraries")
        else:
            print(f"         🏠 Remains as local project pattern for now")
            
        print(f"\n      🌐 Ecosystem Intelligence Benefits:")
        print(f"         • Pattern available for future projects in this tech stack")
        print(f"         • Cross-project learning accelerates development")
        print(f"         • High-value patterns contribute to SCF framework growth")
        print(f"         • Universal continuity maintained while innovation spreads")

def main():
    """Main demo runner with command line interface"""
    import argparse
    
    parser = argparse.ArgumentParser(description='SCF Multi-Tool Orchestration Demo')
    parser.add_argument('project_path', nargs='?', default=None,
                      help='Base path for demo project (default: current directory)')
    parser.add_argument('--workflow', help='Demonstrate specific workflow goal')
    parser.add_argument('--tool-comparison', action='store_true',
                      help='Show tool-specific context optimization comparison')
    parser.add_argument('--cline-demo', action='store_true',
                      help='Focus on Cline CLI integration demonstration')
    
    args = parser.parse_args()
    
    demo = SCFMultiToolDemo(args.project_path)
    
    if args.tool_comparison:
        print("🎯 SCF Tool-Specific Context Optimization")
        print("=" * 50)
        demo._setup_demo_project()
        demo.orchestrator = SCFContextOrchestrator(demo.demo_project_path)
        demo._demonstrate_context_intelligence()
        
    elif args.cline_demo:
        print("⚡ SCF + Cline CLI Integration Demo")
        print("=" * 40)
        demo._setup_demo_project()
        demo.orchestrator = SCFContextOrchestrator(demo.demo_project_path)
        
        # Create a Cline-focused workflow
        cline_workflow = demo.orchestrator.create_multi_agent_workflow(
            "Implement React Button component with automated tests using Cline"
        )
        demo._demonstrate_tool_execution(cline_workflow)
        
    elif args.workflow:
        print(f"🎼 SCF Custom Workflow: {args.workflow}")
        print("=" * 60)
        demo._setup_demo_project()
        demo.orchestrator = SCFContextOrchestrator(demo.demo_project_path)
        
        tasks = demo.orchestrator.create_multi_agent_workflow(args.workflow)
        demo._display_workflow_plan(tasks)
        
    else:
        # Run complete demonstration
        demo.run_complete_demo()

if __name__ == '__main__':
    main()