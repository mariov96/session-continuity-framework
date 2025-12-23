#!/usr/bin/env python3
"""
recon.py - SCF Project Reconnaissance
=====================================

Context-aware script that adapts behavior based on execution location (Hub vs Spoke).

FROM HUB:
  Discover projects, update spoke registry, read spoke-signals, generate recommendations
  Ingest pending signals, deploy policies to spokes

FROM SPOKE:
  Self-assess health, verify hub connection, update spoke-signal, notify hub

Usage:
  python recon.py --help              Show this help
  python recon.py                     Auto-detect context and run
  python recon.py --scan-path PATH    [Hub] Scan specific path for projects
  python recon.py --ingest            [Hub] Ingest pending signals from all spokes
  python recon.py --deploy            [Hub] Deploy hub policies to all spokes
  python recon.py --update-hub        [Spoke] Send signal to hub
  python recon.py --verbose           Detailed output

Examples:
  # From Hub - discover all projects
  cd ~/projects/session-continuity-framework
  python recon.py --scan-path ~/projects

  # From Hub - ingest all pending spoke signals
  python recon.py --ingest

  # From Hub - deploy policies to all spokes
  python recon.py --deploy

  # From Spoke - phone home
  cd ~/projects/my-web-app
  python ~/projects/session-continuity-framework/recon.py --update-hub
"""

import json
import os
import sys
import hashlib
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional, Tuple
import argparse
import shutil

# ANSI color codes for output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def detect_context() -> str:
    """
    Determine if we're running from Hub or Spoke.

    Returns:
        'hub' if running from hub directory
        'spoke' if running from spoke directory
        'unknown' otherwise
    """
    cwd = Path.cwd()

    # Check for hub indicators
    if (cwd / '.scf-registry').exists() and (cwd / '.scf-registry' / 'spokes').exists():
        return 'hub'

    # Check for spoke indicators
    if (cwd / '.scf' / 'BUILDSTATE.json').exists() or (cwd / 'buildstate.json').exists():
        return 'spoke'

    return 'unknown'

def find_hub_from_spoke() -> Optional[Path]:
    """
    Find hub path from spoke's buildstate.

    Returns:
        Path to hub directory, or None if not found
    """
    # Try .scf/BUILDSTATE.json first
    buildstate_path = Path.cwd() / '.scf' / 'BUILDSTATE.json'
    if not buildstate_path.exists():
        buildstate_path = Path.cwd() / 'buildstate.json'

    if not buildstate_path.exists():
        return None

    try:
        with open(buildstate_path) as f:
            buildstate = json.load(f)

        hub_path = buildstate.get('_scf_metadata', {}).get('hub_path')
        if hub_path:
            return Path(hub_path).expanduser()
    except (json.JSONDecodeError, KeyError):
        pass

    # Search parent directories for hub
    current = Path.cwd().parent
    for _ in range(5):  # Search up to 5 levels
        if (current / '.scf-registry' / 'spokes').exists():
            return current
        current = current.parent

    return None

def is_scf_enabled(project_path: Path) -> Tuple[bool, Optional[str]]:
    """
    Check if project has SCF enabled and determine version.

    Returns:
        (is_enabled, version)
    """
    buildstate_json = project_path / '.scf' / 'BUILDSTATE.json'
    if not buildstate_json.exists():
        buildstate_json = project_path / 'buildstate.json'

    if not buildstate_json.exists():
        return (False, None)

    try:
        with open(buildstate_json) as f:
            data = json.load(f)

        version = data.get('_scf_metadata', {}).get('template_version') or \
                  data.get('_scf_header', {}).get('version') or \
                  data.get('meta', {}).get('spec', 'unknown')

        return (True, version)
    except (json.JSONDecodeError, KeyError):
        return (True, 'unknown')

def should_skip_project(project_path: Path, hub_path: Path) -> bool:
    """
    Determine if project should be skipped during discovery.

    Skip if:
    - It's the hub itself
    - It's in tests/ directory
    - It's excluded by .scfignore
    """
    # Skip hub itself
    if project_path.resolve() == hub_path.resolve():
        return False  # Hub scans itself but marks as hub

    # Skip tests directory
    if 'tests' in project_path.parts:
        return True

    # Check for .scfignore in hub
    scfignore = hub_path / 'tests' / '.scfignore'
    if scfignore.exists():
        # Simple check - if project path contains 'test-project', skip it
        if 'test-project' in str(project_path):
            return True

    return False

def run_from_hub(args):
    """
    Hub mode: Discover projects, read spoke-signals, generate recommendations.
    Optionally ingest signals or deploy policies.
    """
    hub_path = Path.cwd()
    scan_path = Path(args.scan_path).expanduser() if args.scan_path else hub_path.parent

    print(f"{Colors.HEADER}======================================={Colors.ENDC}")
    print(f"{Colors.HEADER}  SCF Hub Reconnaissance{Colors.ENDC}")
    print(f"{Colors.HEADER}======================================={Colors.ENDC}\n")
    print(f"Hub: {hub_path}")
    print(f"Scanning: {scan_path}\n")

    # Discover projects
    discovered = discover_projects(scan_path, hub_path, args.verbose)

    print(f"\n{Colors.OKGREEN}Found {len(discovered)} projects in scan{Colors.ENDC}\n")

    # Handle --ingest flag
    if args.ingest:
        print(f"{Colors.OKCYAN}{Colors.BOLD}** Ingesting Pending Signals...{Colors.ENDC}\n")
        ingested = ingest_signals(hub_path, discovered, args.verbose)
        print(f"\n{Colors.OKGREEN}✓ Ingested {ingested} signals into hub knowledge base{Colors.ENDC}\n")
        return 0

    # Handle --deploy flag
    if args.deploy:
        print(f"{Colors.OKCYAN}{Colors.BOLD}** Deploying Hub Policies to Spokes...{Colors.ENDC}\n")
        deployed = deploy_policies(hub_path, discovered, args.verbose)
        print(f"\n{Colors.OKGREEN}✓ Made {deployed} policy deployments{Colors.ENDC}\n")
        return 0

    # Generate recommendations by reading spoke-signals.jsonl from each project
    recommendations = generate_recommendations(discovered, args.verbose)

    if recommendations:
        print(f"\n{Colors.OKCYAN}{Colors.BOLD}** Recommendations:{Colors.ENDC}\n")
        for i, rec in enumerate(recommendations, 1):
            priority_color = Colors.FAIL if rec['priority'] == 'high' else Colors.WARNING
            print(f"{priority_color}[{rec['priority'].upper()}]{Colors.ENDC} {rec['action']}")
            print(f"  Command: {Colors.OKBLUE}{rec['command']}{Colors.ENDC}")
            print(f"  Reason: {rec['reason']}\n")
        
        # Offer quick actions
        pending_signals = [r for r in recommendations if 'signal_id' in r]
        if pending_signals:
            print(f"{Colors.OKCYAN}TIP: Run 'python recon.py --ingest' to ingest {len(pending_signals)} pending signals{Colors.ENDC}\n")
    else:
        print(f"\n{Colors.OKGREEN}OK All projects healthy - no actions needed{Colors.ENDC}\n")

def discover_projects(scan_path: Path, hub_path: Path, verbose: bool = False) -> List[Dict]:
    """
    Discover SCF projects in scan path.
    """
    discovered = []
    seen_projects = set()

    # Find all buildstate.json files (both root and .scf/)
    for pattern in ['buildstate.json', '.scf/BUILDSTATE.json', '.scf/buildstate.json']:
        for buildstate in scan_path.rglob(pattern):
            # For .scf/BUILDSTATE.json, project is the parent of .scf
            if '.scf' in buildstate.parts:
                project_path = buildstate.parent.parent
            else:
                project_path = buildstate.parent

            # Skip if already discovered
            project_key = str(project_path.resolve())
            if project_key in seen_projects:
                continue
            seen_projects.add(project_key)

            if should_skip_project(project_path, hub_path):
                if verbose:
                    print(f"SKIP Skipping: {project_path.name} (internal/test project)")
                continue

            is_enabled, version = is_scf_enabled(project_path)

            project_info = {
                'path': str(project_path),
                'name': project_path.name,
                'scf_enabled': is_enabled,
                'version': version
            }

            discovered.append(project_info)

            if verbose:
                status = f"SCF {version}" if is_enabled else "No SCF"
                print(f"  Found: {project_path.name} ({status})")

    return discovered

def generate_recommendations(projects: List[Dict], verbose: bool = False) -> List[Dict]:
    """
    Read spoke-signals.jsonl from each project and generate action recommendations.

    Args:
        projects: List of discovered project info dicts
        verbose: Print debug information

    Returns:
        List of recommendation dicts with action, priority, command, reason
    """
    recommendations = []

    for project in projects:
        project_path = Path(project['path'])
        project_name = project['name']

        # Check for spoke-signals.jsonl
        signal_file = project_path / '.scf' / 'spoke-signals.jsonl'
        if not signal_file.exists():
            if verbose:
                print(f"  No signals from {project_name}")
            continue

        try:
            # Read JSONL file (each line is a complete JSON object)
            with open(signal_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    # Skip comments and empty lines
                    if not line or line.startswith('#'):
                        continue

                    try:
                        signal = json.loads(line)

                        flags = signal.get('flags', {})
                        requests = signal.get('requests', [])
                        offers = signal.get('offers', [])

                        # Check flags for recommended actions
                        if flags.get('needs_rebalance'):
                            recommendations.append({
                                'action': f'rebalance {project_name}',
                                'priority': 'high',
                                'command': f'python rebalance.py --project {project_path}',
                                'reason': 'Rebalance requested by spoke'
                            })

                        if flags.get('has_high_impact_learnings') or len(offers) > 0:
                            recommendations.append({
                                'action': f'learn from {project_name}',
                                'priority': 'high',
                                'command': f'python learn.py --project {project_path}',
                                'reason': f'{len(offers)} high-impact learnings available'
                            })

                        if flags.get('needs_template_update'):
                            recommendations.append({
                                'action': f'teach {project_name}',
                                'priority': 'medium',
                                'command': f'python teach.py --update {project_path}',
                                'reason': 'Template update requested'
                            })

                        # Check requests
                        for request in requests:
                            request_type = request.get('type', 'unknown')
                            if request_type == 'template_upgrade':
                                recommendations.append({
                                    'action': f'teach {project_name}',
                                    'priority': 'medium',
                                    'command': f'python teach.py --upgrade {project_path}',
                                    'reason': 'Upgrade to latest SCF version'
                                })
                            elif request_type == 'hub_guidance':
                                recommendations.append({
                                    'action': f'review {project_name}',
                                    'priority': 'low',
                                    'command': f'# Review project: {project_path}',
                                    'reason': request.get('description', 'Guidance requested')
                                })

                        # NEW FORMAT: Handle extension-generated signals
                        if signal.get('signal_id') and signal.get('status') == 'pending':
                            scope = signal.get('scope', 'this_spoke')
                            labels = signal.get('labels', [])
                            content = signal.get('content', '')[:100]
                            
                            priority = 'high' if scope == 'all_projects' else 'medium'
                            recommendations.append({
                                'action': f'ingest signal from {project_name}',
                                'priority': priority,
                                'command': f'python recon.py --ingest',
                                'reason': f'Pending signal ({scope}): {content}...',
                                'signal_id': signal.get('signal_id'),
                                'signal_data': signal
                            })

                    except json.JSONDecodeError as e:
                        if verbose:
                            print(f"  Warning: Invalid JSON in {signal_file.name}: {e}")
                        continue

        except Exception as e:
            if verbose:
                print(f"  Warning: Could not read signals from {project_name}: {e}")

    return recommendations


def get_hub_version(hub_path: Path) -> str:
    """Get the current hub SCF version."""
    hub_profile = hub_path / '.scf-registry' / 'hub-profile.json'
    if hub_profile.exists():
        try:
            with open(hub_profile) as f:
                data = json.load(f)
            return data.get('hub_config', {}).get('version', 'unknown')
        except:
            pass
    return 'unknown'


def check_spoke_version_compatibility(spoke_path: Path, hub_path: Path, verbose: bool = False) -> Tuple[bool, str]:
    """
    Check if spoke SCF version is compatible with hub.
    
    Returns:
        (is_compatible, message)
    """
    hub_version = get_hub_version(hub_path)
    _, spoke_version = is_scf_enabled(spoke_path)
    
    if not spoke_version or spoke_version == 'unknown':
        return (False, "Spoke has unknown/missing SCF version")
    
    # Parse versions (format: v2.1, v1.0, etc.)
    try:
        hub_major = int(hub_version.replace('v', '').split('.')[0]) if hub_version != 'unknown' else 0
        spoke_major = int(spoke_version.replace('v', '').split('.')[0]) if spoke_version not in ['unknown', None] else 0
        
        if hub_major > 0 and spoke_major > 0:
            if hub_major - spoke_major >= 2:
                return (False, f"Spoke is dramatically out of date (v{spoke_major}.x vs Hub v{hub_major}.x). Run: python teach.py {spoke_path}")
            elif hub_major > spoke_major:
                return (True, f"Spoke is slightly behind (v{spoke_major}.x vs Hub v{hub_major}.x)")
    except:
        pass
    
    return (True, "Version compatible")


def ingest_signals(hub_path: Path, projects: List[Dict], verbose: bool = False) -> int:
    """
    Ingest pending signals from all spokes into hub knowledge base.
    
    Returns:
        Number of signals ingested
    """
    ingested_count = 0
    hub_ideas_file = hub_path / '.scf-registry' / 'hub-ideas.json'
    
    # Load existing hub ideas
    hub_ideas = []
    if hub_ideas_file.exists():
        try:
            with open(hub_ideas_file) as f:
                hub_ideas = json.load(f)
        except:
            hub_ideas = []
    
    for project in projects:
        project_path = Path(project['path'])
        project_name = project['name']
        signal_file = project_path / '.scf' / 'spoke-signals.jsonl'
        
        if not signal_file.exists():
            continue
        
        # Check version compatibility first
        is_compatible, compat_msg = check_spoke_version_compatibility(project_path, hub_path, verbose)
        if not is_compatible:
            print(f"{Colors.WARNING}! {project_name}: {compat_msg}{Colors.ENDC}")
            continue
        
        # Read and process signals
        updated_lines = []
        signals_to_archive = []
        
        try:
            with open(signal_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            for line in lines:
                line = line.strip()
                if not line or line.startswith('#'):
                    updated_lines.append(line + '\n' if line else '')
                    continue
                
                try:
                    signal = json.loads(line)
                    
                    # Only process new-format pending signals
                    if signal.get('signal_id') and signal.get('status') == 'pending':
                        # Generate hub idea ID
                        hub_idea_id = 'hub-' + hashlib.sha256(
                            (signal['signal_id'] + signal.get('content', '')).encode()
                        ).hexdigest()[:8]
                        
                        # Create hub idea from signal
                        hub_idea = {
                            'idea_id': hub_idea_id,
                            'source_signal': signal['signal_id'],
                            'source_project': project_name,
                            'source_path': str(project_path),
                            'ingested_at': datetime.now(timezone.utc).isoformat(),
                            'type': signal.get('type', 'learning'),
                            'content': signal.get('content', ''),
                            'scope': signal.get('scope', 'this_spoke'),
                            'labels': signal.get('labels', []),
                            'impact': signal.get('impact', 5),
                            'status': 'active',
                            'deployed_to': []
                        }
                        hub_ideas.append(hub_idea)
                        
                        # Mark signal as archived
                        signal['status'] = 'archived'
                        signal['hub_idea_id'] = hub_idea_id
                        signal['archived_at'] = datetime.now(timezone.utc).isoformat()
                        
                        ingested_count += 1
                        if verbose:
                            print(f"  {Colors.OKGREEN}✓{Colors.ENDC} Ingested: {signal['signal_id']} → {hub_idea_id}")
                    
                    updated_lines.append(json.dumps(signal) + '\n')
                    
                except json.JSONDecodeError:
                    updated_lines.append(line + '\n')
                    continue
            
            # Write updated signals back (with archived status)
            with open(signal_file, 'w', encoding='utf-8') as f:
                f.writelines(updated_lines)
                
        except Exception as e:
            if verbose:
                print(f"  {Colors.FAIL}Error processing {project_name}: {e}{Colors.ENDC}")
    
    # Save hub ideas
    if ingested_count > 0:
        with open(hub_ideas_file, 'w', encoding='utf-8') as f:
            json.dump(hub_ideas, f, indent=2)
    
    return ingested_count


def deploy_policies(hub_path: Path, projects: List[Dict], verbose: bool = False) -> int:
    """
    Deploy hub policies/ideas to all registered spokes based on scope.
    
    Returns:
        Number of deployments made
    """
    hub_ideas_file = hub_path / '.scf-registry' / 'hub-ideas.json'
    hub_profile_file = hub_path / '.scf-registry' / 'hub-profile.json'
    
    if not hub_ideas_file.exists():
        if verbose:
            print("  No hub ideas to deploy")
        return 0
    
    try:
        with open(hub_ideas_file) as f:
            hub_ideas = json.load(f)
    except:
        return 0
    
    # Load hub profile for policies
    hub_policies = []
    if hub_profile_file.exists():
        try:
            with open(hub_profile_file) as f:
                profile = json.load(f)
            hub_policies = profile.get('spoke_contributions', {}).get('suggested_patterns', [])
        except:
            pass
    
    deployment_count = 0
    
    for project in projects:
        project_path = Path(project['path'])
        project_name = project['name']
        
        # Skip hub itself
        if project_path.resolve() == hub_path.resolve():
            continue
        
        # Check version compatibility
        is_compatible, compat_msg = check_spoke_version_compatibility(project_path, hub_path, verbose)
        if not is_compatible:
            print(f"{Colors.WARNING}! Skipping {project_name}: {compat_msg}{Colors.ENDC}")
            continue
        
        # Find buildstate
        buildstate_path = project_path / '.scf' / 'BUILDSTATE.json'
        if not buildstate_path.exists():
            buildstate_path = project_path / 'buildstate.json'
        if not buildstate_path.exists():
            continue
        
        try:
            with open(buildstate_path) as f:
                buildstate = json.load(f)
        except:
            continue
        
        # Ensure hub_policies section exists
        if 'hub_policies' not in buildstate:
            buildstate['hub_policies'] = []
        
        existing_ids = {p.get('idea_id') for p in buildstate['hub_policies'] if isinstance(p, dict)}
        
        # Deploy applicable ideas
        deployed_any = False
        for idea in hub_ideas:
            if idea['idea_id'] in existing_ids:
                continue  # Already deployed
            
            if idea['status'] != 'active':
                continue
            
            scope = idea.get('scope', 'this_spoke')
            
            # Check if this idea applies to this spoke
            should_deploy = False
            if scope == 'all_projects':
                should_deploy = True
            elif scope == 'similar_projects':
                # TODO: Check match_criteria against project stack
                should_deploy = True  # For now, deploy to all
            elif scope == 'this_spoke' and idea.get('source_path') == str(project_path):
                should_deploy = True
            
            if should_deploy:
                # Add to spoke's hub_policies
                policy_entry = {
                    'idea_id': idea['idea_id'],
                    'type': idea['type'],
                    'content': idea['content'],
                    'labels': idea['labels'],
                    'deployed_at': datetime.now(timezone.utc).isoformat(),
                    'from_hub': str(hub_path)
                }
                buildstate['hub_policies'].append(policy_entry)
                
                # Track deployment in hub
                if project_name not in idea.get('deployed_to', []):
                    idea.setdefault('deployed_to', []).append(project_name)
                
                deployed_any = True
                deployment_count += 1
                if verbose:
                    print(f"  {Colors.OKGREEN}✓{Colors.ENDC} Deployed {idea['idea_id']} to {project_name}")
        
        if deployed_any:
            # Save updated buildstate
            with open(buildstate_path, 'w', encoding='utf-8') as f:
                json.dump(buildstate, f, indent=2)
    
    # Save updated hub ideas with deployment tracking
    with open(hub_ideas_file, 'w', encoding='utf-8') as f:
        json.dump(hub_ideas, f, indent=2)
    
    return deployment_count


def run_from_spoke(args):
    """
    Spoke mode: Self-assess, verify hub connection, send signal.
    """
    spoke_path = Path.cwd()

    print(f"{Colors.HEADER}======================================={Colors.ENDC}")
    print(f"{Colors.HEADER}  SCF Spoke Self-Assessment{Colors.ENDC}")
    print(f"{Colors.HEADER}======================================={Colors.ENDC}\n")
    print(f"Spoke: {spoke_path.name}")
    print(f"Path: {spoke_path}\n")

    # Find hub
    hub_path = find_hub_from_spoke()
    if not hub_path:
        print(f"{Colors.FAIL}X Hub not found{Colors.ENDC}")
        print(f"\nCannot locate SCF hub. Options:")
        print(f"  1. Add 'hub_path' to _scf_metadata in buildstate.json")
        print(f"  2. Run from a project within hub's directory tree")
        return 1

    print(f"{Colors.OKGREEN}OK Hub connected:{Colors.ENDC} {hub_path}")

    # Self-assess
    is_enabled, version = is_scf_enabled(spoke_path)
    if not is_enabled:
        print(f"{Colors.WARNING}! SCF not initialized{Colors.ENDC}")
        print(f"\nRun: python {hub_path}/teach.py --init {spoke_path}")
        return 1

    print(f"{Colors.OKGREEN}OK SCF version:{Colors.ENDC} {version}")

    # TODO: Calculate health metrics, update spoke signal
    print(f"\n{Colors.OKCYAN}TIP: Spoke signal functionality coming soon{Colors.ENDC}")
    print(f"   Will automatically update hub registry on buildstate changes")

    return 0

def main():
    parser = argparse.ArgumentParser(
        description='SCF Project Reconnaissance - Context-aware discovery and signaling',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    parser.add_argument('--scan-path', help='[Hub] Path to scan for projects')
    parser.add_argument('--ingest', action='store_true', help='[Hub] Ingest pending signals from all spokes')
    parser.add_argument('--deploy', action='store_true', help='[Hub] Deploy hub policies to all spokes')
    parser.add_argument('--update-hub', action='store_true', help='[Spoke] Send signal to hub')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')

    args = parser.parse_args()

    context = detect_context()

    if context == 'hub':
        return run_from_hub(args)
    elif context == 'spoke':
        return run_from_spoke(args)
    else:
        print(f"{Colors.FAIL}Error: Cannot determine context{Colors.ENDC}")
        print(f"\nNot running from Hub (no .scf-registry/) or Spoke (no buildstate.json)")
        print(f"Current directory: {Path.cwd()}")
        return 1

if __name__ == '__main__':
    sys.exit(main() or 0)
