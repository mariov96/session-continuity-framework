#!/usr/bin/env python3
"""
SCF Project Context Loader
===========================

Quick tool to load project context with automatic change detection and review prompts.

Usage:
    # Load project with change notifications
    python3 scf_load_project.py /path/to/project
    
    # Check changes from last 48 hours
    python3 scf_load_project.py /path/to/project --since-hours 48
    
    # Just show changes without full context
    python3 scf_load_project.py /path/to/project --changes-only
    
    # Save output to file
    python3 scf_load_project.py /path/to/project --output context.md
"""

import argparse
import sys
from pathlib import Path
from scf_llm_integration import SCFLLMIntegrator, SessionType


def main():
    parser = argparse.ArgumentParser(
        description="Load SCF project context with change notifications",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Load project with notifications
  python3 scf_load_project.py /path/to/my-project
  
  # Check last 48 hours
  python3 scf_load_project.py /path/to/my-project --since-hours 48
  
  # Just show changes
  python3 scf_load_project.py /path/to/my-project --changes-only
  
  # Save to file
  python3 scf_load_project.py /path/to/my-project --output context.md
        """
    )
    
    parser.add_argument('project_path', type=Path,
                       help='Path to SCF-enabled project')
    parser.add_argument('--since-hours', type=int, default=168,
                       help='Check for changes in last N hours (default: 168 = 7 days)')
    parser.add_argument('--changes-only', action='store_true',
                       help='Only show changes, not full context')
    parser.add_argument('--session-type', 
                       choices=['ideation', 'implementation', 'analysis', 'optimization', 'planning'],
                       default='implementation',
                       help='Type of session (default: implementation)')
    parser.add_argument('--session-id', type=str,
                       help='Unique session identifier (auto-generated if not provided)')
    parser.add_argument('--ai-name', type=str, default='AI',
                       help='Name of AI (e.g., Claude, GPT-4, Copilot)')
    parser.add_argument('--self-aware', action='store_true',
                       help='Use self-aware protocol (checks if another AI modified project)')
    parser.add_argument('--update-state', action='store_true',
                       help='Update session state after loading (marks you as last modifier)')
    parser.add_argument('--output', type=Path,
                       help='Save output to file instead of printing')
    parser.add_argument('--quiet', action='store_true',
                       help='Suppress status messages')
    
    args = parser.parse_args()
    
    # Generate session ID if not provided
    if not args.session_id:
        import uuid
        args.session_id = str(uuid.uuid4())[:8]
    
    # Validate project
    if not args.project_path.exists():
        print(f"❌ Error: Project path does not exist: {args.project_path}", file=sys.stderr)
        sys.exit(1)
    
    # Check for buildstate
    buildstate_json = args.project_path / "buildstate.json"
    buildstate_md = args.project_path / "buildstate.md"
    
    if not buildstate_json.exists() and not buildstate_md.exists():
        print(f"❌ Error: No buildstate files found in {args.project_path}", file=sys.stderr)
        print("   Use init_scf.py to initialize SCF first", file=sys.stderr)
        sys.exit(1)
    
    if not args.quiet:
        print(f"🔍 Loading project: {args.project_path.name}")
        print(f"📁 Path: {args.project_path}")
        if args.self_aware:
            print(f"🤖 AI: {args.ai_name}")
            print(f"🆔 Session: {args.session_id}")
            print(f"🧠 Mode: Self-Aware (checks for other AI modifications)")
        else:
            print(f"⏰ Checking changes from last {args.since_hours} hours")
        print()
    
    # Initialize integrator
    try:
        integrator = SCFLLMIntegrator(args.project_path)
    except Exception as e:
        print(f"❌ Error initializing project: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Generate output based on mode
    if args.self_aware:
        # Self-aware mode: checks session state automatically
        if not args.quiet:
            print("🧠 Checking session state...")
        
        output = integrator.generate_self_aware_context(
            session_id=args.session_id,
            ai_name=args.ai_name
        )
        
        # Update session state if requested
        if args.update_state:
            success = integrator.update_session_state(
                session_id=args.session_id,
                modified_by=f"{args.ai_name}-{args.session_id}",
                requires_review=False,  # Will be updated at session end if needed
                review_reason=None
            )
            if not args.quiet:
                if success:
                    print("✅ Session state updated")
                else:
                    print("⚠️  Could not update session state")
        
    elif args.changes_only:
        # Just show change review prompt
        if not args.quiet:
            print("🔎 Detecting recent changes...")
        
        changes = integrator.detect_recent_changes(since_hours=args.since_hours)
        
        if 'error' in changes:
            print(f"❌ Error detecting changes: {changes['error']}", file=sys.stderr)
            sys.exit(1)
        
        output = integrator.generate_change_review_prompt(changes)
    else:
        # Legacy mode: time-based change detection
        if not args.quiet:
            print("🔎 Detecting recent changes...")
        
        session_enum = SessionType(args.session_type.upper())
        output = integrator.load_project_context_with_notifications(session_enum)
    
    # Print summary (if not self-aware mode, which has its own)
    if not args.self_aware and not args.quiet:
        changes = integrator.detect_recent_changes(since_hours=args.since_hours)
        if changes.get('requires_review'):
            summary = changes.get('change_summary', {})
            print(f"📊 Changes detected:")
            print(f"   - New decisions: {summary.get('total_new_decisions', 0)}")
            print(f"   - Pending next steps: {summary.get('pending_next_steps', 0)}")
            print(f"   - Features in progress: {summary.get('features_in_progress', 0)}")
            print(f"   - Open bugs: {summary.get('open_bugs', 0)}")
            print()
            print("⚠️  Review required before proceeding!")
            print()
        elif not args.quiet:
            print("✅ No recent changes detected - project is up to date")
            print()
    
    # Output
    if args.output:
        # Save to file
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output)
        if not args.quiet:
            print(f"💾 Context saved to: {args.output}")
    else:
        # Print to stdout
        print("="*80)
        print(output)
        print("="*80)
    
    if not args.quiet:
        print()
        print("✅ Project context loaded successfully!")
        print()
        print("📝 Usage Tips:")
        print("   - Copy the output above and paste into your LLM session")
        print("   - Review any change notifications before implementing")
        print("   - Use --output to save context for later reference")


if __name__ == '__main__':
    main()
