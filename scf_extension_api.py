import json
import os
import sys # Import sys for stderr
import re # Import re for regular expressions
from pathlib import Path
from typing import List, Dict, Any, Optional

# Assuming buildstate_hunter_learner.py exists and has a discover_projects function
# For now, we'll mock this or create a simplified version.

def _find_scf_projects(root_dir: Path) -> List[str]:
    """
    Recursively finds directories containing a '.scf/BUILDSTATE.json' file.
    """
    scf_projects = []
    for item in root_dir.rglob('.scf/BUILDSTATE.json'):
        scf_projects.append(str(item.parent.parent)) # Get the project root
    return scf_projects

def get_all_scf_projects() -> str:
    """
    Discovers all SCF projects in the workspace and returns their paths as a JSON string.
    """
    # In a real scenario, this would use buildstate_hunter_learner.py
    # For now, we'll simulate discovery within the current workspace.
    workspace_root = Path(os.getcwd()) # This will be the session-continuity-framework root
    projects = _find_scf_projects(workspace_root)
    
    # Add the main SCF project itself if it has a buildstate (which it should)
    if (workspace_root / '.scf' / 'BUILDSTATE.json').exists():
        if str(workspace_root) not in projects:
            projects.insert(0, str(workspace_root)) # Add main project at the beginning

    return json.dumps({"projects": projects})

def get_project_summary(project_path: str) -> str:
    """
    Retrieves a detailed summary of a specific project's buildstate,
    including key sections from both JSON and Markdown.
    """
    project_root = Path(project_path)
    buildstate_json_path = project_root / '.scf' / 'BUILDSTATE.json'
    buildstate_md_path = project_root / '.scf' / 'BUILDSTATE.md'

    summary: Dict[str, Any] = {
        "name": project_root.name,
        "path": project_path,
        "status": "N/A",
        "last_modified_by": "N/A",
        "last_modified_at": "N/A",
        "requires_review": False,
        "review_reason": None,
        "description": "No buildstate found.",
        "full_description": "No detailed description available.",
        "objectives": [],
        "next_steps": [],
        "features": [],
        "tech_stack": [],
        "coding_standards": {},
        "recent_decisions": []
    }

    buildstate_data: Dict[str, Any] = {}
    if buildstate_json_path.exists():
        try:
            with open(buildstate_json_path, 'r', encoding='utf-8') as f:
                buildstate_data = json.load(f)
            
            session_state = buildstate_data.get('_session_state', {})
            project_metadata = buildstate_data.get('project_metadata', {})
            idea = buildstate_data.get('idea', {})

            summary["status"] = buildstate_data.get('stage', 'unknown')
            summary["last_modified_by"] = session_state.get('last_modified_by', 'Unknown')
            summary["last_modified_at"] = session_state.get('last_modified_at', 'N/A')
            summary["requires_review"] = session_state.get('requires_review', False)
            summary["review_reason"] = session_state.get('review_reason')
            summary["name"] = project_metadata.get('name', project_root.name)
            summary["description"] = idea.get('problem', 'No problem statement defined.')
            summary["full_description"] = idea.get('vision', summary["description"])
            summary["objectives"] = buildstate_data.get('objectives', [])
            summary["next_steps"] = buildstate_data.get('next_steps', [])
            summary["features"] = [f.get('name', '') for f in buildstate_data.get('features', []) if f.get('name')]
            summary["tech_stack"] = buildstate_data.get('stack', [])
            summary["coding_standards"] = buildstate_data.get('coding_standards', {})
            summary["recent_decisions"] = [
                {"decision": d.get('decision', ''), "impact": d.get('impact', 0)}
                for d in buildstate_data.get('decisions', [])[-3:] # Last 3 decisions
            ]
            
        except json.JSONDecodeError:
            summary["description"] = "Invalid BUILDSTATE.json"
            summary["full_description"] = "Could not parse BUILDSTATE.json."
        except Exception as e:
            summary["description"] = f"Error reading BUILDSTATE.json: {e}"
            summary["full_description"] = f"Error reading BUILDSTATE.json: {e}"
    
    if buildstate_md_path.exists():
        try:
            with open(buildstate_md_path, 'r', encoding='utf-8') as f:
                md_content = f.read()
            
            # Enhance summary with Markdown content if not already rich from JSON
            if summary["description"] == "No buildstate found." or summary["description"] == "No problem statement defined.":
                name_match = next(re.finditer(r'#\s*(.+)', md_content), None)
                problem_match = next(re.finditer(r'##\s*The Problem\s*\n\n(.+?)(?=##|\Z)', md_content, re.DOTALL), None)
                vision_match = next(re.finditer(r'##\s*The Vision\s*\n\n(.+?)(?=##|\Z)', md_content, re.DOTALL), None)
                
                if name_match:
                    summary["name"] = name_match.group(1).strip()
                if problem_match:
                    summary["description"] = problem_match.group(1).strip().split('\n')[0] + "..."
                if vision_match:
                    summary["full_description"] = vision_match.group(1).strip()
            
            # Extract other sections from Markdown if not present in JSON or to enrich
            if not summary["objectives"]:
                objectives_match = next(re.finditer(r'##\s*(?:Current\s+)?(?:Objectives?|Goals?)\s*\n(.*?)(?=##|\Z)', md_content, re.DOTALL | re.IGNORECASE), None)
                if objectives_match:
                    summary["objectives"] = [line.strip('- *0123456789.').strip() for line in objectives_match.group(1).split('\n') if line.strip()]
            
            if not summary["next_steps"]:
                next_steps_match = next(re.finditer(r'##\s*(?:Next Steps?|Action Items?)\s*\n(.*?)(?=##|\Z)', md_content, re.DOTALL | re.IGNORECASE), None)
                if next_steps_match:
                    summary["next_steps"] = [line.strip('- *0123456789.').strip() for line in next_steps_match.group(1).split('\n') if line.strip()]

        except Exception as e:
            # If MD parsing fails, keep JSON data or initial defaults
            print(f"Error reading BUILDSTATE.md: {e}", file=sys.stderr)

    return json.dumps(summary)

def chat_with_scf_buddy(project_path: str, message: str) -> str:
    """
    Provides an intelligent chat interface with the SCF AI buddy.
    Context-aware responses that understand the HUB-Spoke relationship.
    """
    project_name = Path(project_path).name
    message_lower = message.lower()
    
    # Build context-aware response based on message content
    response = ""
    
    # Detect intent and provide intelligent responses
    if any(word in message_lower for word in ['help', 'what can you do', 'commands', 'capabilities']):
        response = f"I'm your SCF AI Buddy for **{project_name}** (Spoke Project). I'm connected to the SCF HUB which maintains cross-project knowledge.\n\n" \
                  f"I can help you:\n" \
                  f"• **Learn**: Record insights from this session to the HUB\n" \
                  f"• **Teach**: Apply HUB knowledge and patterns to this project\n" \
                  f"• **Rebalance**: Optimize buildstate weights based on HUB patterns\n" \
                  f"• **Sync**: Update this project with latest HUB templates\n\n" \
                  f"Just click the action buttons above or ask me about your project!"
                  
    elif any(word in message_lower for word in ['learn', 'record', 'capture', 'insight']):
        response = f"I can help record learning moments from your current session with **{project_name}**. " \
                  f"These insights will be stored in the HUB and become available to all your SCF projects. " \
                  f"Click the 📚 Learn button to capture current session insights, or ask me specific questions about what you've learned."
                  
    elif any(word in message_lower for word in ['teach', 'apply', 'knowledge', 'patterns']):
        response = f"The HUB contains accumulated knowledge from all your SCF projects. I can apply relevant patterns, " \
                  f"coding standards, and architectural decisions to **{project_name}**. " \
                  f"Click the 🎓 Teach button to apply HUB knowledge, or tell me what specific area you'd like guidance on."
                  
    elif any(word in message_lower for word in ['rebalance', 'optimize', 'weights']):
        response = f"I can rebalance the buildstate for **{project_name}** using patterns learned from the HUB. " \
                  f"This optimizes section weights and priorities based on successful patterns across your projects. " \
                  f"Click the ⚖️ Rebalance button to optimize now."
                  
    elif any(word in message_lower for word in ['sync', 'update', 'hub', 'latest']):
        response = f"I can sync **{project_name}** with the latest templates and structures from the HUB. " \
                  f"This ensures your spoke project stays aligned with your evolving SCF standards. " \
                  f"Click the 🔄 Sync button to update now."
                  
    elif any(word in message_lower for word in ['status', 'state', 'how is', "what's"]):
        # Get project summary
        try:
            summary_json = get_project_summary(project_path)
            summary = json.loads(summary_json)
            response = f"**{project_name}** Status:\n" \
                      f"• Stage: {summary.get('status', 'N/A')}\n" \
                      f"• Last modified by: {summary.get('last_modified_by', 'N/A')}\n" \
                      f"• Requires review: {'Yes - ' + summary.get('review_reason', '') if summary.get('requires_review') else 'No'}\n\n" \
                      f"This spoke project is connected to the SCF HUB. Use the action buttons above to leverage HUB capabilities."
        except:
            response = f"I'm monitoring **{project_name}** as a spoke project connected to the SCF HUB. " \
                      f"I can help you learn from this session, apply HUB knowledge, or sync with latest patterns."
    else:
        # Generic response with context
        response = f"I'm your SCF AI Buddy for **{project_name}**. This spoke project is connected to the central SCF HUB, " \
                  f"which provides cross-project learning and pattern recognition.\n\n" \
                  f"You said: '{message}'\n\n" \
                  f"I can help with learning from this session, applying HUB knowledge, rebalancing buildstate, or syncing templates. " \
                  f"What would you like to do?"
    
    return json.dumps({"response": response})

def get_learning_moments() -> str:
    """
    Retrieves aggregated learning moments from the SCF hub.
    """
    # Placeholder for actual implementation using buildstate_hunter_learner.py
    moments = [
        {"id": "m1", "title": "Event Sourcing Pattern", "impact": 9, "source_project": "napkin-hero"},
        {"id": "m2", "title": "Consistent Error Handling", "impact": 8, "source_project": "scf-web-app"}
    ]
    return json.dumps({"moments": moments})

def get_voice_profiles() -> str:
    """
    Retrieves aggregated AI voice profiles from the SCF hub.
    """
    # Placeholder for actual implementation
    profiles = [
        {"ai_name": "Claude-Sonnet", "strength": "Architectural Analysis", "sessions": 22},
        {"ai_name": "GitHub Copilot", "strength": "Idiomatic Code", "sessions": 15}
    ]
    return json.dumps({"profiles": profiles})

def check_proactive_alerts() -> str:
    """
    Checks for proactive alerts across all discovered SCF projects.
    This is a placeholder for more sophisticated logic.
    """
    alerts = []
    # Simulate checking for alerts
    # In a real scenario, this would involve:
    # 1. Running buildstate_hunter_learner.py to get all projects
    # 2. Iterating through each project's buildstate
    # 3. Applying logic to detect "proactive" events (e.g., new high-impact decisions, low balance scores, inactivity)

    # Example: If a dummy project 'test-scf-app' exists and needs review
    workspace_root = Path(os.getcwd())
    test_project_path = workspace_root / 'test-scf-app'
    test_buildstate_path = test_project_path / 'buildstate.json'

    if test_buildstate_path.exists():
        try:
            with open(test_buildstate_path, 'r', encoding='utf-8') as f:
                buildstate_data = json.load(f)
            session_state = buildstate_data.get('_session_state', {})
            if session_state.get('requires_review', False):
                alerts.append({
                    "type": "review_required",
                    "project_name": "test-scf-app",
                    "message": f"Review required for 'test-scf-app': {session_state.get('review_reason', 'No reason provided')}",
                    "severity": "high"
                })
            # Simulate a "new learning moment" alert
            if buildstate_data.get('learning_moments_count', 0) > 0 and buildstate_data['learning_moments_count'] % 2 == 0:
                 alerts.append({
                    "type": "new_learning_moment",
                    "project_name": "test-scf-app",
                    "message": "A new learning moment was detected in 'test-scf-app'. Check the SCF Hub for details.",
                    "severity": "medium"
                })
        except Exception as e:
            print(f"Error checking alerts for test-scf-app: {e}", file=sys.stderr)

    return json.dumps({"alerts": alerts})

def trigger_scf_action(project_path: str, action_type: str) -> str:
    """
    Triggers a specific SCF action for a given project.
    Integrates with actual SCF scripts for learn, teach, rebalance, and sync actions.
    """
    import subprocess
    
    project_name = Path(project_path).name
    hub_path = Path(__file__).parent  # Assumes this script is in the HUB directory
    
    try:
        if action_type == "learn":
            # Call scf_meta_learner.py to record learning moments
            script_path = hub_path / "scf_meta_learner.py"
            if script_path.exists():
                result = subprocess.run(
                    [sys.executable, str(script_path), "learn", "--project-path", project_path],
                    capture_output=True,
                    text=True,
                    cwd=str(hub_path)
                )
                if result.returncode == 0:
                    response = {"status": "success", "actionType": action_type, 
                               "message": f"Learning recorded for '{project_name}'. HUB now has insights from this session."}
                else:
                    response = {"status": "error", "actionType": action_type,
                               "message": f"Learn action failed: {result.stderr}"}
            else:
                response = {"status": "error", "actionType": action_type,
                           "message": "scf_meta_learner.py not found in HUB."}
                           
        elif action_type == "teach":
            # Call teach.py to apply HUB knowledge to project
            script_path = hub_path / "teach.py"
            if script_path.exists():
                result = subprocess.run(
                    [sys.executable, str(script_path), "--project-path", project_path],
                    capture_output=True,
                    text=True,
                    cwd=str(hub_path)
                )
                if result.returncode == 0:
                    response = {"status": "success", "actionType": action_type,
                               "message": f"HUB knowledge applied to '{project_name}'. Check buildstate for insights."}
                else:
                    response = {"status": "error", "actionType": action_type,
                               "message": f"Teach action failed: {result.stderr}"}
            else:
                response = {"status": "error", "actionType": action_type,
                           "message": "teach.py not found in HUB."}
                           
        elif action_type == "rebalance":
            # Call scf_rebalancer.py to rebalance buildstate
            script_path = hub_path / "scf_rebalancer.py"
            if script_path.exists():
                result = subprocess.run(
                    [sys.executable, str(script_path), project_path],
                    capture_output=True,
                    text=True,
                    cwd=str(hub_path)
                )
                if result.returncode == 0:
                    response = {"status": "success", "actionType": action_type,
                               "message": f"Buildstate rebalanced for '{project_name}'. Weights optimized based on HUB patterns."}
                else:
                    response = {"status": "error", "actionType": action_type,
                               "message": f"Rebalance action failed: {result.stderr}"}
            else:
                response = {"status": "error", "actionType": action_type,
                           "message": "scf_rebalancer.py not found in HUB."}
                           
        elif action_type == "sync":
            # Call update_scf.py to sync with HUB
            script_path = hub_path / "update_scf.py"
            if script_path.exists():
                result = subprocess.run(
                    [sys.executable, str(script_path), "--target", project_path],
                    capture_output=True,
                    text=True,
                    cwd=str(hub_path)
                )
                if result.returncode == 0:
                    response = {"status": "success", "actionType": action_type,
                               "message": f"'{project_name}' synced with HUB. Templates and structures updated."}
                else:
                    response = {"status": "error", "actionType": action_type,
                               "message": f"Sync action failed: {result.stderr}"}
            else:
                response = {"status": "error", "actionType": action_type,
                           "message": "update_scf.py not found in HUB."}
        else:
            response = {"status": "error", "actionType": action_type,
                       "message": f"Unknown action type: {action_type}. Available: learn, teach, rebalance, sync"}
    except Exception as e:
        response = {"status": "error", "actionType": action_type,
                   "message": f"Error executing {action_type}: {str(e)}"}

    return json.dumps(response)

def main():
    import argparse
    import sys
    import re

    parser = argparse.ArgumentParser(description="SCF Extension API")
    parser.add_argument("command", choices=["get_all_scf_projects", "get_project_summary", "chat_with_scf_buddy", "get_learning_moments", "get_voice_profiles", "check_proactive_alerts", "trigger_scf_action"])
    parser.add_argument("--project-path", help="Path to the SCF project")
    parser.add_argument("--message", help="Message for the SCF AI buddy")
    parser.add_argument("--action-type", help="Type of SCF action to trigger (e.g., 'rebalance', 'update')")

    args = parser.parse_args()

    if args.command == "get_all_scf_projects":
        print(get_all_scf_projects())
    elif args.command == "get_project_summary":
        if not args.project_path:
            print(json.dumps({"error": "project-path is required for get_project_summary"}), file=sys.stderr)
            sys.exit(1)
        print(get_project_summary(args.project_path))
    elif args.command == "chat_with_scf_buddy":
        if not args.project_path or not args.message:
            print(json.dumps({"error": "project-path and message are required for chat_with_scf_buddy"}), file=sys.stderr)
            sys.exit(1)
        print(chat_with_scf_buddy(args.project_path, args.message))
    elif args.command == "get_learning_moments":
        print(get_learning_moments())
    elif args.command == "get_voice_profiles":
        print(get_voice_profiles())
    elif args.command == "check_proactive_alerts":
        print(check_proactive_alerts())
    elif args.command == "trigger_scf_action":
        if not args.project_path or not args.action_type:
            print(json.dumps({"error": "project-path and action-type are required for trigger_scf_action"}), file=sys.stderr)
            sys.exit(1)
        print(trigger_scf_action(args.project_path, args.action_type))

if __name__ == "__main__":
    main()