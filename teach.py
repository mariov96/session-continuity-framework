#!/usr/bin/env python3
"""
teach.py - SCF Knowledge Distribution

Push SCF templates, learnings, and updates to spoke projects.

Usage:
    python teach.py --init <project-path>      # Initialize new project with SCF
    python teach.py --update <project-path>    # Push latest learnings to existing project
    python teach.py --upgrade <project-path>   # Upgrade old SCF version to v2.1

Context-Aware Behavior:
    From Hub: Teach spokes (push templates and learnings)
    From Spoke: Request teachings from hub (pull mode)

Examples:
    # Initialize new project
    python teach.py --init ~/projects/my-new-app

    # Update existing project with latest learnings
    python teach.py --update ~/projects/my-app

    # Upgrade old SCF v1.0 project to v2.1
    python teach.py --upgrade ~/projects/old-app

    # Update all spokes
    python teach.py --update-all
"""

import sys
import json
import shutil
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime, timezone
import subprocess

# ANSI color codes
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def detect_context() -> str:
    """Determine if we're running from Hub or Spoke."""
    cwd = Path.cwd()
    if (cwd / '.scf-registry').exists() and (cwd / '.scf-registry' / 'spokes').exists():
        return 'hub'
    if (cwd / '.scf' / 'BUILDSTATE.json').exists() or (cwd / 'buildstate.json').exists():
        return 'spoke'
    return 'unknown'

def find_hub() -> Optional[Path]:
    """Find SCF hub directory."""
    # Check if we're in the hub
    if (Path.cwd() / '.scf-registry').exists():
        return Path.cwd()

    # Check buildstate for hub_path
    buildstate_path = Path.cwd() / '.scf' / 'BUILDSTATE.json'
    if not buildstate_path.exists():
        buildstate_path = Path.cwd() / 'buildstate.json'

    if buildstate_path.exists():
        try:
            with open(buildstate_path) as f:
                buildstate = json.load(f)
            hub_path = buildstate.get('_scf_metadata', {}).get('scf_home')
            if hub_path:
                return Path(hub_path).expanduser()
        except (json.JSONDecodeError, KeyError):
            pass

    # Search parent directories
    current = Path.cwd().parent
    for _ in range(5):
        if (current / '.scf-registry' / 'spokes').exists():
            return current
        current = current.parent

    return None

def get_hub_git_metadata(hub_path: Path) -> Dict[str, Any]:
    """
    Get comprehensive git metadata for the hub repository
    """
    try:
        # Get current commit hash
        result = subprocess.run(['git', 'rev-parse', 'HEAD'], 
                              cwd=hub_path, capture_output=True, text=True, check=True)
        current_hash = result.stdout.strip()
        
        # Get short hash
        result = subprocess.run(['git', 'rev-parse', '--short=7', 'HEAD'], 
                              cwd=hub_path, capture_output=True, text=True, check=True)
        current_hash_short = result.stdout.strip()
        
        # Get current branch
        result = subprocess.run(['git', 'branch', '--show-current'], 
                              cwd=hub_path, capture_output=True, text=True, check=True)
        current_branch = result.stdout.strip()
        
        # Get remote origin URL
        result = subprocess.run(['git', 'config', '--get', 'remote.origin.url'], 
                              cwd=hub_path, capture_output=True, text=True, check=True)
        origin_url = result.stdout.strip()
        
        # Parse GitHub repo from URL
        github_repo = None
        if 'github.com' in origin_url:
            if origin_url.startswith('git@'):
                github_repo = origin_url.split(':')[1].replace('.git', '')
            else:
                github_repo = '/'.join(origin_url.split('/')[-2:]).replace('.git', '')
        
        # Get last commit info
        result = subprocess.run([
            'git', 'log', '-1', '--format=%ad|%s|%an', '--date=iso'
        ], cwd=hub_path, capture_output=True, text=True, check=True)
        
        last_commit_info = result.stdout.strip().split('|', 2)
        last_commit_date = last_commit_info[0] if len(last_commit_info) > 0 else ''
        last_commit_message = last_commit_info[1] if len(last_commit_info) > 1 else ''
        last_commit_author = last_commit_info[2] if len(last_commit_info) > 2 else ''
        
        return {
            'current_hash': current_hash,
            'current_hash_short': current_hash_short,
            'current_branch': current_branch,
            'github_repo': github_repo,
            'github_links': {
                'commit_link': f"https://github.com/{github_repo}/commit/{current_hash}" if github_repo else None,
                'repo_link': f"https://github.com/{github_repo}" if github_repo else None
            },
            'last_commit': {
                'date': last_commit_date,
                'message': last_commit_message,
                'author': last_commit_author
            },
            'captured_at': datetime.now(timezone.utc).isoformat()
        }
        
    except subprocess.CalledProcessError as e:
        return {'error': f'Git command failed: {e}'}

def get_file_git_metadata(file_path: Path, repo_path: Path) -> Dict[str, Any]:
    """
    Get git metadata for a specific file
    """
    try:
        relative_path = file_path.relative_to(repo_path)
        
        # Get last commit info for this file
        result = subprocess.run([
            'git', 'log', '-1', '--format=%H|%ad|%s|%an', 
            '--date=iso', '--', str(relative_path)
        ], cwd=repo_path, capture_output=True, text=True, check=True)
        
        if result.stdout.strip():
            parts = result.stdout.strip().split('|', 3)
            last_hash = parts[0]
            last_date = parts[1]
            last_message = parts[2] if len(parts) > 2 else ''
            last_author = parts[3] if len(parts) > 3 else ''
            
            # Calculate days since last commit
            commit_date = datetime.fromisoformat(last_date.replace(' ', 'T'))
            days_since = (datetime.now() - commit_date.replace(tzinfo=None)).days
            
            return {
                'file_path': str(relative_path),
                'last_commit': {
                    'hash': last_hash,
                    'hash_short': last_hash[:7],
                    'date': last_date,
                    'message': last_message,
                    'author': last_author,
                    'days_ago': days_since
                },
                'staleness_score': min(days_since / 30.0, 1.0)  # 0-1 scale
            }
        else:
            return {'error': 'No git history found'}
            
    except subprocess.CalledProcessError as e:
        return {'error': f'Git command failed: {e}'}
    except Exception as e:
        return {'error': f'Metadata extraction failed: {e}'}

def get_hub_kb_version(hub_path: Path) -> str:
    """Get current hub knowledge base version."""
    # Read from hub's kb-sync.json
    kb_sync_file = hub_path / '.scf' / 'kb-sync.json'
    if kb_sync_file.exists():
        try:
            with open(kb_sync_file) as f:
                kb_sync = json.load(f)
            return kb_sync.get('hub_kb_version', datetime.now().isoformat())
        except:
            pass
    return datetime.now().isoformat()

def init_project(project_path: Path, hub_path: Path, verbose: bool = False):
    """
    Initialize a new project with SCF templates.

    Phase 1 - Ideation (Markdown-first):
        .scf/BUILDSTATE.md        # Strategic planning, easily shareable
        .scf/SCF_README.md         # AI instructions

    Phase 2 - Optional (when development starts):
        .scf/BUILDSTATE.json       # Technical tracking
        .scf/kb-sync.json          # Knowledge sync
        .scf/spoke-signals.jsonl   # Hub communication

    Philosophy: Start with markdown for ideation. Users can take BUILDSTATE.md
    to any LLM (ChatGPT, Claude, etc.) for productive conversations without
    needing structured JSON until actual development begins.
    """
    project_path = project_path.expanduser().resolve()

    print(f"\n{Colors.HEADER}Initializing SCF in:{Colors.ENDC} {project_path.name}")
    print(f"Hub: {hub_path}\n")
    print(f"{Colors.OKCYAN}Philosophy:{Colors.ENDC} Starting with markdown for ideation")
    print(f"  BUILDSTATE.md + SCF_README.md = easily shareable with any LLM")
    print(f"  BUILDSTATE.json created later when development starts\n")

    # Create .scf directory
    scf_dir = project_path / '.scf'
    scf_dir.mkdir(exist_ok=True)

    if verbose:
        print(f"  Created .scf/ directory")

    # Copy templates
    templates_dir = hub_path / 'templates'

    # PRIORITY ORDER: Markdown first, JSON optional
    files_to_copy = [
        ('BUILDSTATE.md', '.scf/BUILDSTATE.md'),        # FIRST: Strategic planning
        ('SCF_README.md', '.scf/SCF_README.md'),        # SECOND: AI instructions
        ('kb-sync.json', '.scf/kb-sync.json'),          # Optional: KB tracking
        ('spoke-signals.jsonl', '.scf/spoke-signals.jsonl')  # Optional: Hub comms
        # Note: BUILDSTATE.json NOT created by default - add when dev starts
    ]

    hub_kb_version = get_hub_kb_version(hub_path)

    for template_name, dest_path in files_to_copy:
        template_file = templates_dir / template_name
        dest_file = project_path / dest_path

        if not template_file.exists():
            print(f"  {Colors.WARNING}! Template not found:{Colors.ENDC} {template_name}")
            continue

        if dest_file.exists():
            print(f"  {Colors.WARNING}SKIP{Colors.ENDC} {dest_path} (already exists)")
            continue

        # Copy and customize
        shutil.copy2(template_file, dest_file)

        # Update kb-sync.json with current hub version
        if template_name == 'kb-sync.json':
            with open(dest_file, 'r') as f:
                kb_sync = json.load(f)

            kb_sync['hub_kb_version'] = hub_kb_version
            kb_sync['spoke_kb_version'] = hub_kb_version
            kb_sync['last_sync_date'] = datetime.now().isoformat()

            with open(dest_file, 'w') as f:
                json.dump(kb_sync, f, indent=2)

        print(f"  {Colors.OKGREEN}OK{Colors.ENDC} Created {dest_path}")

    # Create AGENTS.md symlink
    agents_md = project_path / 'AGENTS.md'
    if not agents_md.exists():
        try:
            # Create relative symlink
            agents_md.symlink_to('.scf/SCF_README.md')
            print(f"  {Colors.OKGREEN}OK{Colors.ENDC} Created AGENTS.md symlink")
        except:
            print(f"  {Colors.WARNING}!{Colors.ENDC} Could not create AGENTS.md symlink (may require admin on Windows)")

    print(f"\n{Colors.OKGREEN}{Colors.BOLD}Success!{Colors.ENDC} SCF initialized in {project_path.name}")
    print(f"\n{Colors.BOLD}Markdown-First Approach:{Colors.ENDC}")
    print(f"  Your project now has BUILDSTATE.md + SCF_README.md")
    print(f"  These are easily shareable with any LLM for ideation\n")
    print(f"{Colors.BOLD}Next steps:{Colors.ENDC}")
    print(f"  1. Open .scf/BUILDSTATE.md and fill in project vision")
    print(f"  2. Share with ChatGPT/Claude/etc for productive ideation")
    print(f"  3. When development starts, add BUILDSTATE.json for tracking")
    print(f"  4. AI assistants will auto-read SCF_README.md for context\n")

def check_foundation_status(project_path: Path) -> dict:
    """
    Check if project foundation is complete and detect potential drift.

    Returns dict with:
        - complete: bool
        - issues: list of issues found
        - recommendations: list of recommended actions
    """
    result = {
        'complete': False,
        'issues': [],
        'recommendations': []
    }

    # Find buildstate file
    scf_dir = project_path / '.scf'
    buildstate_path = scf_dir / 'BUILDSTATE.json'
    if not buildstate_path.exists():
        buildstate_path = scf_dir / 'buildstate.json'
    if not buildstate_path.exists():
        buildstate_path = project_path / 'buildstate.json'

    if not buildstate_path.exists():
        result['issues'].append("No buildstate.json found")
        result['recommendations'].append("Run 'scf init --guided' to establish project foundation")
        return result

    try:
        with open(buildstate_path) as f:
            buildstate = json.load(f)
    except json.JSONDecodeError:
        result['issues'].append("buildstate.json is not valid JSON")
        return result

    # Check foundation
    foundation = buildstate.get('_project_foundation', {})

    if not foundation:
        result['issues'].append("No _project_foundation section found")
        result['recommendations'].append("AI should guide user through foundation setup before work")
        return result

    if not foundation.get('completed'):
        result['issues'].append("Project foundation not completed")
        result['recommendations'].append("Complete foundation with 'scf init --guided' or have AI guide setup")
        return result

    # Foundation exists and is complete
    result['complete'] = True

    # Check for required fields
    identity = foundation.get('identity', {})
    if not identity.get('one_liner'):
        result['issues'].append("Missing project one-liner description")
        result['recommendations'].append("Add identity.one_liner to foundation")

    if not identity.get('success_looks_like'):
        result['issues'].append("Missing success definition")
        result['recommendations'].append("Define what success looks like")

    boundaries = foundation.get('boundaries', {})
    if not boundaries.get('in_scope'):
        result['issues'].append("No scope boundaries defined")
        result['recommendations'].append("Define in_scope and out_of_scope boundaries")

    # Check session state
    session = buildstate.get('_session_state', {})
    if session.get('requires_review'):
        result['issues'].append(f"Review required: {session.get('review_reason', 'Unknown reason')}")
        result['recommendations'].append("Review recent changes before proceeding")

    return result


def update_project(project_path: Path, hub_path: Path, verbose: bool = False):
    """
    Update existing project with latest learnings from hub.

    Updates:
        .scf/SCF_README.md (with latest learnings)
        .scf/kb-sync.json (hub_kb_version)

    Also checks foundation status and reports issues.
    """
    project_path = project_path.expanduser().resolve()

    print(f"\n{Colors.HEADER}Updating SCF in:{Colors.ENDC} {project_path.name}")
    print(f"Hub: {hub_path}\n")

    # Check foundation status first
    foundation_status = check_foundation_status(project_path)

    if not foundation_status['complete']:
        print(f"{Colors.WARNING}⚠️  Foundation Status: INCOMPLETE{Colors.ENDC}")
        for issue in foundation_status['issues']:
            print(f"   • {issue}")
        print()
        for rec in foundation_status['recommendations']:
            print(f"   → {rec}")
        print()
        print(f"{Colors.OKCYAN}Tip:{Colors.ENDC} AI assistants should complete foundation before starting work.\n")
    elif foundation_status['issues']:
        print(f"{Colors.OKCYAN}📋 Foundation Status: Complete (with notes){Colors.ENDC}")
        for issue in foundation_status['issues']:
            print(f"   • {issue}")
        print()

    # Check if project has SCF
    scf_dir = project_path / '.scf'
    if not scf_dir.exists():
        print(f"{Colors.FAIL}Error:{Colors.ENDC} Project not initialized with SCF")
        print(f"Run: python teach.py --init {project_path}")
        return 1

    # Get current versions
    kb_sync_file = scf_dir / 'kb-sync.json'
    if kb_sync_file.exists():
        with open(kb_sync_file) as f:
            kb_sync = json.load(f)
        current_spoke_version = kb_sync.get('spoke_kb_version', 'unknown')
    else:
        current_spoke_version = 'unknown'
        # Initialize kb_sync if file doesn't exist
        kb_sync = {
            'hub_kb_version': 'unknown',
            'spoke_kb_version': 'unknown',
            'last_sync_date': 'never',
            'sync_method': 'teach.py --init'
        }

    hub_kb_version = get_hub_kb_version(hub_path)

    print(f"Current spoke KB version: {current_spoke_version}")
    print(f"Hub KB version: {hub_kb_version}\n")

    # Update SCF_README.md with template replacement
    readme_template = hub_path / 'templates' / 'SCF_README.md'
    readme_dest = scf_dir / 'SCF_README.md'

    if readme_template.exists():
        # Read template and replace placeholders
        template_content = readme_template.read_text()
        
        # Get current date for last updated
        current_date = datetime.now(timezone.utc).strftime("%B %d, %Y")
        
        # Replace template placeholders with actual values
        updated_content = template_content.replace(
            '{{LAST_UPDATED}}', current_date
        ).replace(
            '{{HUB_KB_VERSION}}', hub_kb_version
        ).replace(
            '{{SPOKE_KB_VERSION}}', kb_sync.get('spoke_kb_version', 'unknown')
        ).replace(
            '{{HUB_PATH}}', str(hub_path)
        ).replace(
            '{{SCF_VERSION}}', 'v2.1'
        ).replace(
            '{{USER_NAME}}', 'Developer'
        ).replace(
            '{{WORK_STYLE}}', 'Collaborative'
        ).replace(
            '{{LANGUAGES}}', 'JavaScript, Python, TypeScript'
        ).replace(
            '{{PATTERNS}}', 'Clean code, Test-driven development'
        ).replace(
            '{{HEALTH_CHECKS}}', 'SCF active, Hub connected'
        ).replace(
            '{{RECOMMENDATIONS}}', 'Continue with current development approach'
        )
        
        # Write the updated content
        readme_dest.write_text(updated_content)
        print(f"  {Colors.OKGREEN}OK{Colors.ENDC} Updated SCF_README.md with latest learnings")

    # Update buildstate.json with comprehensive tracking (consolidating kb-sync data)
    buildstate_file = scf_dir / 'buildstate.json'
    if not buildstate_file.exists():
        buildstate_file = scf_dir / 'BUILDSTATE.json'
    
    if buildstate_file.exists():
        with open(buildstate_file, 'r') as f:
            buildstate_data = json.load(f)
    else:
        buildstate_data = {}
    
    # Ensure _scf_metadata section exists
    if '_scf_metadata' not in buildstate_data:
        buildstate_data['_scf_metadata'] = {}
    
    scf_meta = buildstate_data['_scf_metadata']
    
    # Add comprehensive git metadata tracking to buildstate
    hub_git_info = get_hub_git_metadata(hub_path)
    
    # Update core sync information
    scf_meta['hub_kb_version'] = hub_kb_version
    scf_meta['spoke_kb_version'] = hub_kb_version
    scf_meta['last_sync_date'] = datetime.now(timezone.utc).isoformat()
    scf_meta['sync_method'] = 'teach.py --update'
    
    # Add hub reference with git metadata
    scf_meta['hub_reference'] = hub_git_info
    
    # Track file-specific metadata
    if 'file_metadata' not in scf_meta:
        scf_meta['file_metadata'] = {}
    scf_meta['file_metadata']['SCF_README.md'] = get_file_git_metadata(readme_dest, hub_path)
    
    # Add development health metrics
    scf_meta['development_health'] = {
        'days_since_sync': 0,
        'sync_frequency': 'regular',  # Will be calculated from history
        'drift_score': 0.0,
        'last_teach_run': datetime.now(timezone.utc).isoformat()
    }
    
    # Add sync history tracking (keep last 10 syncs)
    if 'sync_history' not in scf_meta:
        scf_meta['sync_history'] = []
    
    current_sync = {
        'date': datetime.now(timezone.utc).isoformat(),
        'method': 'teach.py --update',
        'hub_hash': hub_git_info.get('current_hash', 'unknown'),
        'changes_applied': 1,  # SCF_README.md update
        'files_touched': ['SCF_README.md', 'buildstate.json']
    }
    scf_meta['sync_history'].append(current_sync)
    if len(scf_meta['sync_history']) > 10:
        scf_meta['sync_history'] = scf_meta['sync_history'][-10:]

    # Write updated buildstate with enhanced tracking
    with open(buildstate_file, 'w') as f:
        json.dump(buildstate_data, f, indent=2)

    print(f"  {Colors.OKGREEN}OK{Colors.ENDC} Updated buildstate with enhanced tracking")

    print(f"\n{Colors.OKGREEN}{Colors.BOLD}Success!{Colors.ENDC} {project_path.name} updated with latest learnings\n")

def upgrade_project(project_path: Path, hub_path: Path, verbose: bool = False):
    """
    Upgrade old SCF version to v2.1.

    Upgrades:
        - Moves buildstate.json to .scf/BUILDSTATE.json
        - Creates .scf/ directory structure
        - Adds missing v2.1 features (_scf_metadata, _session_state)
        - Copies missing templates
    """
    project_path = project_path.expanduser().resolve()

    print(f"\n{Colors.HEADER}Upgrading SCF in:{Colors.ENDC} {project_path.name}")
    print(f"Hub: {hub_path}\n")

    # Check for old buildstate.json
    old_buildstate = project_path / 'buildstate.json'
    new_buildstate = project_path / '.scf' / 'BUILDSTATE.json'

    if not old_buildstate.exists() and not new_buildstate.exists():
        print(f"{Colors.FAIL}Error:{Colors.ENDC} No buildstate.json found")
        print(f"Run: python teach.py --init {project_path}")
        return 1

    # Create .scf directory
    scf_dir = project_path / '.scf'
    scf_dir.mkdir(exist_ok=True)
    print(f"  {Colors.OKGREEN}OK{Colors.ENDC} Created .scf/ directory")

    # Move buildstate.json if needed
    if old_buildstate.exists() and not new_buildstate.exists():
        shutil.move(old_buildstate, new_buildstate)
        print(f"  {Colors.OKGREEN}OK{Colors.ENDC} Moved buildstate.json to .scf/BUILDSTATE.json")

    # Read buildstate and add v2.1 features
    with open(new_buildstate, 'r') as f:
        buildstate = json.load(f)

    # Add _scf_metadata if missing
    if '_scf_metadata' not in buildstate:
        buildstate['_scf_metadata'] = {
            'version': '2.1.0',
            'scf_home': str(hub_path),
            'structure_version': 'v2',
            'upgraded_from': buildstate.get('meta', {}).get('spec', 'v1.0'),
            'upgraded_at': datetime.now().isoformat()
        }
        print(f"  {Colors.OKGREEN}OK{Colors.ENDC} Added _scf_metadata")

    # Add _session_state if missing
    if '_session_state' not in buildstate:
        buildstate['_session_state'] = {
            'last_session_id': 'teach-upgrade',
            'last_modified_by': 'teach.py --upgrade',
            'last_modified_at': datetime.now().isoformat(),
            'requires_review': False,
            'review_reason': None,
            'session_count': 1
        }
        print(f"  {Colors.OKGREEN}OK{Colors.ENDC} Added _session_state")

    # Write updated buildstate
    with open(new_buildstate, 'w') as f:
        json.dump(buildstate, f, indent=4)

    # Copy missing templates
    templates_to_add = [
        'SCF_README.md',
        'kb-sync.json',
        'spoke-signals.jsonl',
        'BUILDSTATE.md'
    ]

    hub_kb_version = get_hub_kb_version(hub_path)
    templates_dir = hub_path / 'templates'

    for template_name in templates_to_add:
        dest_file = scf_dir / template_name
        if not dest_file.exists():
            template_file = templates_dir / template_name
            if template_file.exists():
                shutil.copy2(template_file, dest_file)

                # Customize kb-sync.json
                if template_name == 'kb-sync.json':
                    with open(dest_file, 'r') as f:
                        kb_sync = json.load(f)
                    kb_sync['hub_kb_version'] = hub_kb_version
                    kb_sync['spoke_kb_version'] = hub_kb_version
                    kb_sync['last_sync_date'] = datetime.now().isoformat()
                    with open(dest_file, 'w') as f:
                        json.dump(kb_sync, f, indent=2)

                print(f"  {Colors.OKGREEN}OK{Colors.ENDC} Added {template_name}")

    # Create AGENTS.md symlink
    agents_md = project_path / 'AGENTS.md'
    if not agents_md.exists():
        try:
            agents_md.symlink_to('.scf/SCF_README.md')
            print(f"  {Colors.OKGREEN}OK{Colors.ENDC} Created AGENTS.md symlink")
        except:
            print(f"  {Colors.WARNING}!{Colors.ENDC} Could not create AGENTS.md symlink")

    print(f"\n{Colors.OKGREEN}{Colors.BOLD}Success!{Colors.ENDC} {project_path.name} upgraded to SCF v2.1\n")

def main():
    parser = argparse.ArgumentParser(
        description='SCF Knowledge Distribution - Push templates and learnings to spokes',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    parser.add_argument('--init', metavar='PATH', help='Initialize new project with SCF')
    parser.add_argument('--update', metavar='PATH', help='Update project with latest learnings')
    parser.add_argument('--upgrade', metavar='PATH', help='Upgrade old SCF version to v2.1')
    parser.add_argument('--update-all', action='store_true', help='Update all spokes in registry')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')

    args = parser.parse_args()

    # Find hub
    hub_path = find_hub()
    if not hub_path:
        print(f"{Colors.FAIL}Error:{Colors.ENDC} Could not locate SCF hub")
        print(f"\nOptions:")
        print(f"  1. Run from hub directory")
        print(f"  2. Add 'scf_home' to _scf_metadata in buildstate.json")
        return 1

    # Execute command
    if args.init:
        project_path = Path(args.init)
        init_project(project_path, hub_path, args.verbose)

    elif args.update:
        project_path = Path(args.update)
        update_project(project_path, hub_path, args.verbose)

    elif args.upgrade:
        project_path = Path(args.upgrade)
        upgrade_project(project_path, hub_path, args.verbose)

    elif args.update_all:
        # TODO: Implement update-all
        print(f"{Colors.WARNING}update-all not yet implemented{Colors.ENDC}")
        print(f"Coming soon: Update all spokes in .scf-registry/spokes/")

    else:
        parser.print_help()
        return 1

    return 0

if __name__ == '__main__':
    sys.exit(main())
