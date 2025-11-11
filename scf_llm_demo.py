#!/usr/bin/env python3
"""
SCF LLM Integration Demo - Quick Start Tool
==========================================

This demonstration script shows how the enhanced Session Continuity Framework (SCF)
makes buildstate the central driver of every LLM interaction. It showcases:

1. Automatic context injection for any LLM
2. Real-time session tracking and learning capture
3. Intelligent rebalancing integration
4. Universal LLM compatibility

Run this to see how SCF transforms AI from order-taker to informed project partner.

Usage:
    python3 scf_llm_demo.py [project_path] [--llm claude|gpt|grok|gemini] [--session ideation|implementation]
    
Example:
    python3 scf_llm_demo.py /path/to/project --llm claude --session implementation
"""

import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List

# Add current directory to path for imports
sys.path.append(str(Path(__file__).parent))

try:
    from scf_llm_integration import SCFLLMIntegrator, SessionType, LLMType
    from buildstate_hunter_learner import BuildstateHunter, InnovationLearner, RecommendationEngine
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("Ensure scf_llm_integration.py and buildstate_hunter_learner.py are in the current directory")
    sys.exit(1)

class SCFLLMDemo:
    """Demonstrates SCF LLM integration capabilities"""
    
    def __init__(self, project_path: str = None):
        self.project_path = Path(project_path) if project_path else Path.cwd()
        self.demo_project_path = self.project_path / 'scf-llm-demo'
        
    def run_demo(self, llm_type: str = 'claude', session_type: str = 'implementation'):
        """Run complete SCF LLM integration demonstration"""
        print("🚀 SCF LLM Integration Demonstration")
        print("=" * 60)
        print(f"Target LLM: {llm_type.upper()}")
        print(f"Session Type: {session_type.upper()}")
        print(f"Demo Project: {self.demo_project_path}")
        print()
        
        # Phase 1: Setup demo project
        print("📋 Phase 1: Setting up demo project with enhanced buildstate...")
        self._setup_demo_project()
        
        # Phase 2: Initialize LLM integration
        print("\n🧠 Phase 2: Initializing LLM integration engine...")
        integrator = SCFLLMIntegrator(self.demo_project_path)
        
        # Phase 3: Demonstrate context preparation
        print(f"\n⚙️  Phase 3: Preparing {session_type} session context for {llm_type}...")
        session_enum = SessionType(session_type.lower())
        llm_enum = LLMType(llm_type.lower())
        
        context = integrator.prepare_session_context(session_enum, llm_enum)
        
        # Phase 4: Show formatted context
        print("\n📤 Phase 4: Generated LLM context (ready to paste into any AI chat):")
        print("-" * 60)
        print(context.formatted_context)
        print("-" * 60)
        
        # Phase 5: Simulate session interactions
        print("\n🎯 Phase 5: Simulating AI session with learning capture...")
        self._simulate_session_interactions(integrator)
        
        # Phase 6: Show session insights
        print("\n📊 Phase 6: Session insights and learning capture:")
        summary = integrator.get_session_summary()
        self._display_session_summary(summary)
        
        # Phase 7: Context usage monitoring
        print("\n📈 Phase 7: Context usage monitoring:")
        usage = integrator.get_context_usage_estimate()
        self._display_context_usage(usage, llm_type)
        
        # Phase 8: Session completion with rebalancing
        print("\n🏁 Phase 8: Session completion with rebalancing...")
        completion = integrator.complete_session(
            trigger_rebalancing=True,
            session_summary="Demo session showcasing SCF LLM integration capabilities"
        )
        self._display_completion_summary(completion)
        
        # Phase 9: Ecosystem intelligence
        print("\n🌐 Phase 9: Ecosystem intelligence and cross-project learning...")
        self._demonstrate_ecosystem_intelligence()
        
        print("\n✅ SCF LLM Integration Demo Complete!")
        print(f"\n💡 Your enhanced buildstate files are ready at: {self.demo_project_path}")
        print("   • Use scf_llm_integration.py to integrate with any LLM")
        print("   • Buildstate automatically becomes the central driver of AI interactions")
        print("   • Perfect context continuity and intelligent learning capture included")
        
    def _setup_demo_project(self):
        """Setup demo project with enhanced buildstate files"""
        # Create demo project directory
        self.demo_project_path.mkdir(exist_ok=True)
        
        # Copy enhanced templates
        templates_path = Path(__file__).parent / 'templates'
        
        # Enhanced JSON buildstate
        enhanced_json_path = templates_path / 'buildstate-llm-enhanced.json'
        if enhanced_json_path.exists():
            target_json = self.demo_project_path / 'buildstate.json'
            
            # Customize for demo
            with open(enhanced_json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # Add demo-specific content
            data['project'] = {
                "name": "SCF LLM Integration Demo",
                "version": "1.0.0",
                "type": "demonstration_project",
                "stakeholder": "SCF Framework Users",
                "phase": "demonstration"
            }
            
            data['current_state'] = {
                "implemented": ["llm_context_injection", "session_tracking", "learning_capture"],
                "in_progress": ["rebalancing_integration", "ecosystem_intelligence"],
                "testing": ["universal_llm_compatibility"],
                "blocked": [],
                "ready_for_review": ["context_optimization"]
            }
            
            data['session_objectives'] = {
                "current": [
                    "Demonstrate automatic context injection",
                    "Show intelligent learning capture",
                    "Prove universal LLM compatibility",
                    "Showcase session continuity features"
                ],
                "completed_this_session": [],
                "deferred": [],
                "next_session": ["Advanced ecosystem intelligence", "Cross-project pattern propagation"]
            }
            
            data['stack'] = ["Python", "JSON", "Markdown", "SCF Framework", "Universal LLM APIs"]
            
            data['features'] = [
                "Automatic buildstate context injection for any LLM",
                "Real-time session tracking and insight capture",
                "Universal compatibility (Claude, GPT, Grok, Gemini)",
                "Intelligent content rebalancing integration",
                "Context usage monitoring with 80% alerts",
                "Session continuity across conversation boundaries"
            ]
            
            with open(target_json, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
            print(f"   ✅ Enhanced buildstate.json created")
        
        # Enhanced Markdown buildstate
        enhanced_md_path = templates_path / 'buildstate-llm-enhanced.md'
        if enhanced_md_path.exists():
            target_md = self.demo_project_path / 'buildstate.md'
            
            md_content = enhanced_md_path.read_text(encoding='utf-8')
            
            # Customize for demo
            demo_customizations = """

## Demo Project Overview

This is a demonstration of the SCF LLM Integration Engine showcasing:

### 🎯 Demo Objectives
- **Universal LLM Compatibility:** Works seamlessly with Claude, GPT, Grok, Gemini
- **Automatic Context Injection:** Buildstate becomes the first thought of every AI interaction
- **Intelligent Learning Capture:** Decisions and insights automatically preserved
- **Session Continuity:** Perfect context preservation across conversation boundaries
- **Ecosystem Intelligence:** Cross-project learning and pattern propagation

### 🚀 Key Features Demonstrated
1. **Context Preparation:** Automatic formatting for specific LLM types
2. **Session Management:** Real-time tracking and insight capture
3. **Rebalancing Integration:** Content optimization between .md and .json files
4. **Context Monitoring:** Token usage tracking with intelligent overflow handling
5. **Universal Compatibility:** Same buildstate works across all major LLMs

### 💡 Real-World Applications
- **Development Projects:** Technical sessions with perfect context continuity
- **Strategic Planning:** Ideation sessions with automatic decision capture
- **Research Projects:** Analysis sessions with intelligent insight aggregation
- **Optimization Work:** Performance sessions with pattern learning
- **Architecture Planning:** Design sessions with cross-project intelligence

"""
            
            # Insert demo content before the final section
            md_content = md_content.replace(
                "\n---\n\n*This LLM-enhanced strategic buildstate",
                demo_customizations + "\n---\n\n*This LLM-enhanced strategic buildstate"
            )
            
            target_md.write_text(md_content, encoding='utf-8')
            print(f"   ✅ Enhanced buildstate.md created")
            
    def _simulate_session_interactions(self, integrator: SCFLLMIntegrator):
        """Simulate realistic AI session interactions"""
        interactions = [
            {
                'type': 'decision',
                'content': 'Use FastAPI for API framework due to automatic OpenAPI documentation and high performance',
                'impact': 8,
                'rationale': 'Team familiar with Python, need rapid prototyping capabilities'
            },
            {
                'type': 'insight',
                'content': 'Pattern identified: Projects with early API documentation have 40% fewer integration issues',
                'impact': 7,
                'tags': ['pattern', 'documentation', 'api']
            },
            {
                'type': 'progress',
                'content': 'Authentication system implementation',
                'status': 'in_progress',
                'completion': 0.65,
                'notes': 'OAuth2 integration complete, testing JWT tokens'
            },
            {
                'type': 'learning',
                'content': 'SCF buildstate integration reduces context setup time by 80% compared to manual briefing',
                'impact': 9,
                'confidence': 0.95
            }
        ]
        
        for i, interaction in enumerate(interactions, 1):
            print(f"   {i}. Capturing {interaction['type']}: {interaction['content'][:60]}...")
            
            if interaction['type'] == 'decision':
                integrator.capture_decision(
                    interaction['content'],
                    impact=interaction['impact'],
                    rationale=interaction.get('rationale', '')
                )
            elif interaction['type'] == 'progress':
                integrator.track_feature_progress(
                    interaction['content'].lower().replace(' ', '-'),
                    interaction['status'],
                    interaction['completion'],
                    interaction['notes']
                )
            else:
                integrator.capture_insight(
                    interaction['content'],
                    insight_type=interaction['type'],
                    impact_level=interaction['impact'],
                    confidence=interaction.get('confidence', 0.8),
                    tags=interaction.get('tags', [])
                )
                
    def _display_session_summary(self, summary: Dict[str, Any]):
        """Display session summary in readable format"""
        print(f"   📊 Session Duration: {summary.get('session_duration', 'unknown')}")
        print(f"   💡 Total Insights: {summary.get('total_insights', 0)}")
        print(f"   🎯 High Impact: {summary.get('high_impact_insights', 0)}")
        print(f"   📈 Avg Confidence: {summary.get('average_confidence', 0):.2f}")
        
        insights_by_type = summary.get('insights_by_type', {})
        if insights_by_type:
            print("   📋 Insights by Type:")
            for insight_type, count in insights_by_type.items():
                print(f"      • {insight_type.title()}: {count}")
                
        recent_insights = summary.get('recent_insights', [])
        if recent_insights:
            print("   🔥 Recent Insights:")
            for insight in recent_insights:
                print(f"      • [{insight['type']}] {insight['content']} (Impact: {insight['impact']})")
                
    def _display_context_usage(self, usage: Dict[str, Any], target_llm: str):
        """Display context usage monitoring"""
        estimated_tokens = usage.get('estimated_tokens', 0)
        print(f"   🔢 Estimated Tokens: {estimated_tokens:,}")
        
        usage_by_llm = usage.get('usage_by_llm', {})
        target_usage = usage_by_llm.get(target_llm, {})
        
        if target_usage:
            percentage = target_usage.get('percentage', 0)
            limit = target_usage.get('context_limit', 0)
            alert_needed = target_usage.get('alert_needed', False)
            
            print(f"   📊 {target_llm.upper()} Usage: {percentage:.1f}% of {limit:,} token limit")
            if alert_needed:
                print("   ⚠️  Alert: Approaching 80% context limit - rebalancing recommended")
            else:
                print("   ✅ Context usage healthy")
                
        breakdown = usage.get('content_breakdown', {})
        if breakdown:
            print("   📦 Content Breakdown:")
            for source, size in breakdown.items():
                print(f"      • {source.replace('_', ' ').title()}: {size:,} characters")
                
    def _display_completion_summary(self, completion: Dict[str, Any]):
        """Display session completion summary"""
        session_id = completion.get('session_id', 'unknown')
        completion_time = completion.get('completion_time', 'unknown')
        
        print(f"   🆔 Session ID: {session_id}")
        print(f"   ⏰ Completed: {completion_time}")
        
        rebalancing_triggered = completion.get('rebalancing_triggered', False)
        if rebalancing_triggered:
            rebalance_result = completion.get('rebalance_result', {})
            if rebalance_result.get('triggered', False):
                print("   ⚖️  Rebalancing: Executed successfully")
                changes = rebalance_result.get('changes_made', [])
                if changes:
                    print(f"      • Applied {len(changes)} content optimizations")
            else:
                reason = rebalance_result.get('reason', 'unknown')
                print(f"   ⚖️  Rebalancing: Skipped ({reason})")
        else:
            print("   ⚖️  Rebalancing: Not requested")
            
    def _demonstrate_ecosystem_intelligence(self):
        """Demonstrate ecosystem intelligence capabilities"""
        hunter = BuildstateHunter([self.demo_project_path])
        learner = InnovationLearner()
        recommender = RecommendationEngine()
        
        # Hunt for buildstate files
        buildstate_files = hunter.hunt_buildstate_files()
        print(f"   🔍 Discovered: {len(buildstate_files)} buildstate files")
        
        # Learn innovations
        innovations = learner.learn_from_files(buildstate_files)
        print(f"   💡 Identified: {len(innovations)} innovation patterns")
        
        # Generate recommendations
        recommendations = recommender.generate_recommendations(innovations, buildstate_files)
        high_priority = recommendations.get('high_priority', [])
        print(f"   🎯 Generated: {len(high_priority)} high-priority recommendations")
        
        if innovations:
            print("   🚀 Top Innovation:")
            top_innovation = innovations[0]
            print(f"      • {top_innovation.name}: {top_innovation.description}")
            print(f"      • Value Score: {top_innovation.value_score}/10")
            print(f"      • Category: {top_innovation.category}")


def main():
    """Main entry point for SCF LLM demo"""
    import argparse
    
    parser = argparse.ArgumentParser(description='SCF LLM Integration Demonstration')
    parser.add_argument('project_path', nargs='?', default=None,
                      help='Path to project directory (default: current directory)')
    parser.add_argument('--llm', choices=['claude', 'gpt', 'grok', 'gemini', 'generic'],
                      default='claude', help='Target LLM type for demonstration')
    parser.add_argument('--session', choices=['ideation', 'implementation', 'analysis', 'optimization', 'planning'],
                      default='implementation', help='Session type to demonstrate')
    parser.add_argument('--quick', action='store_true', help='Run quick demo without detailed output')
    
    args = parser.parse_args()
    
    # Run demonstration
    demo = SCFLLMDemo(args.project_path)
    
    if args.quick:
        print("🚀 Quick SCF LLM Integration Demo")
        print("=" * 40)
        # Just show the context generation
        demo._setup_demo_project()
        from scf_llm_integration import create_llm_startup_script
        context = create_llm_startup_script(str(demo.demo_project_path), args.session, args.llm)
        print(f"Generated {args.llm.upper()} context for {args.session} session:")
        print("-" * 40)
        print(context)
        print("-" * 40)
    else:
        demo.run_demo(args.llm, args.session)


if __name__ == '__main__':
    main()