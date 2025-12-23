#!/usr/bin/env python3
"""
SCF Enhanced Overview Generator

This module generates accurate SCF overview information using the enhanced 
tracking data from buildstate._scf_metadata (consolidated from legacy kb-sync.json).
It provides the corrected dates and comprehensive tracking information.
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, Optional


def load_enhanced_tracking_data(project_path: Path) -> Optional[Dict[str, Any]]:
    """Load enhanced tracking data from buildstate._scf_metadata"""
    buildstate_paths = [
        project_path / '.scf' / 'BUILDSTATE.json',
        project_path / '.scf' / 'buildstate.json',
        project_path / 'buildstate.json'
    ]
    
    for buildstate_path in buildstate_paths:
        if buildstate_path.exists():
            try:
                with open(buildstate_path, 'r') as f:
                    buildstate_data = json.load(f)
                
                # Return the enhanced tracking data from _scf_metadata
                return buildstate_data.get('_scf_metadata', {})
            except Exception as e:
                print(f"Error reading {buildstate_path}: {e}")
                continue
    
    return None


def load_buildstate_data(project_path: Path) -> Optional[Dict[str, Any]]:
    """Load basic project data from buildstate.json for fallback info"""
    buildstate_paths = [
        project_path / '.scf' / 'BUILDSTATE.json',
        project_path / '.scf' / 'buildstate.json',
        project_path / 'buildstate.json'
    ]
    
    for buildstate_path in buildstate_paths:
        if buildstate_path.exists():
            try:
                with open(buildstate_path, 'r') as f:
                    return json.load(f)
            except Exception:
                continue
    
    return None


def format_datetime_human(iso_string: str) -> str:
    """Format ISO datetime string for human readability"""
    try:
        dt = datetime.fromisoformat(iso_string.replace('Z', '+00:00'))
        # Convert to local timezone for display
        local_dt = dt.astimezone()
        return local_dt.strftime('%B %d, %Y at %H:%M %Z')
    except Exception:
        return iso_string


def calculate_time_ago(iso_string: str) -> str:
    """Calculate how long ago something happened"""
    try:
        dt = datetime.fromisoformat(iso_string.replace('Z', '+00:00'))
        now = datetime.now(timezone.utc)
        diff = now - dt
        
        if diff.days > 0:
            return f"about {diff.days} {'day' if diff.days == 1 else 'days'} ago"
        elif diff.seconds > 3600:
            hours = diff.seconds // 3600
            return f"about {hours} {'hour' if hours == 1 else 'hours'} ago"
        else:
            minutes = diff.seconds // 60
            return f"about {minutes} {'minute' if minutes == 1 else 'minutes'} ago"
    except Exception:
        return "unknown"


def generate_enhanced_overview(project_path: Path) -> str:
    """Generate comprehensive SCF overview using enhanced tracking data"""
    
    # Load enhanced tracking data from buildstate._scf_metadata
    scf_metadata = load_enhanced_tracking_data(project_path)
    buildstate = load_buildstate_data(project_path)
    
    if not scf_metadata and not buildstate:
        return "## ❌ SCF Overview Not Available\n\nNo SCF tracking data found in this project."
    
    project_name = project_path.name
    if buildstate and buildstate.get('project', {}).get('name'):
        project_name = buildstate['project']['name']
    
    overview = f"""## 🤖 SCF (Session Continuity Framework) Overview

This project uses **Session Continuity Framework (SCF)** - a system that maintains perfect context across AI development sessions. The SCF was created by Mario Vaccari to transform AI from "order-taker to informed project partner."

## 📅 Last Update Timeline

**Spoke Project Updates:**

"""
    
    # Get session information - use enhanced tracking from buildstate._scf_metadata
    if buildstate and buildstate.get('_session_state'):
        session_state = buildstate['_session_state']
        last_modified_by = session_state.get('last_modified_by', 'Unknown')
        last_modified_at = session_state.get('last_modified_at')
        session_count = session_state.get('session_count', 0)
        
        if last_modified_at:
            formatted_time = format_datetime_human(last_modified_at)
            overview += f"- **Last modified by:** {last_modified_by} ({formatted_time})\n"
        else:
            overview += f"- **Last modified by:** {last_modified_by}\n"
            
        overview += f"- **Session count:** {session_count} sessions so far\n"
    
    # Enhanced tracking from buildstate._scf_metadata
    if scf_metadata:
        # Last sync information with enhanced accuracy
        last_sync_date = scf_metadata.get('last_sync_date')
        if last_sync_date:
            formatted_sync = format_datetime_human(last_sync_date)
            time_ago = calculate_time_ago(last_sync_date)
            overview += f"- **Last sync with hub:** {formatted_sync} ({time_ago})\n"
        
        # Hub reference information
        hub_ref = scf_metadata.get('hub_reference', {})
        if hub_ref:
            hub_last_commit = hub_ref.get('last_commit_date')
            if hub_last_commit:
                formatted_hub = format_datetime_human(hub_last_commit)
                overview += f"- **Hub last updated:** {formatted_hub} (via teach.py)\n"
        
        # Recent sync details from sync_history
        sync_history = scf_metadata.get('sync_history', [])
        if sync_history:
            latest_sync = sync_history[-1]
            sync_method = latest_sync.get('method', 'unknown')
            files_updated = latest_sync.get('files_touched', [])
            if files_updated:
                overview += f"\n**Key updates in recent session:**\n\n"
                for file_update in files_updated[:5]:  # Show first 5 files
                    overview += f"- {file_update}\n"
    else:
        # No enhanced tracking data available
        pass
    
    overview += "\n## 🏗️ Hub Architecture & Communication\n\n**Hub Details:**\n\n"
    
    # Hub information - enhanced from buildstate._scf_metadata
    if scf_metadata and scf_metadata.get('hub_reference'):
        hub_ref = scf_metadata['hub_reference']
        hub_location = hub_ref.get('local_path', '/home/mario/projects/session-continuity-framework')
        hub_repo = hub_ref.get('github_repo')
        hub_commit = hub_ref.get('current_commit_hash', 'unknown')
        
        overview += f"- **Location:** `{hub_location}`\n"
        if hub_repo:
            overview += f"- **Repository:** `{hub_repo}`\n"
        overview += f"- **Current commit:** `{hub_commit}`\n"
    else:
        # Fallback to buildstate
        if buildstate and buildstate.get('_session_state', {}).get('scf_hub'):
            hub_path = buildstate['_session_state']['scf_hub']
            overview += f"- **Location:** `{hub_path}`\n"
        else:
            overview += f"- **Location:** `/home/mario/projects/session-continuity-framework`\n"
        
        overview += f"- **Repository:** `https://github.com/mariov96/session-continuity-framework`\n"
    
    # Version information
    if buildstate and buildstate.get('_scf_metadata'):
        scf_version = buildstate['_scf_metadata'].get('scf_version', 'v2.1.0')
        overview += f"- **Framework version:** {scf_version}\n"
    else:
        overview += f"- **Framework version:** v2.1.0\n"
    
    # KB version alignment
    if scf_metadata:
        hub_kb_version = scf_metadata.get('hub_kb_version')
        spoke_kb_version = scf_metadata.get('spoke_kb_version')
        if hub_kb_version and spoke_kb_version:
            if hub_kb_version == spoke_kb_version:
                formatted_version = format_datetime_human(hub_kb_version)
                overview += f"- **KB Version:** {formatted_version} (hub and spoke aligned)\n"
            else:
                overview += f"- **KB Version:** Hub: {format_datetime_human(hub_kb_version)}, Spoke: {format_datetime_human(spoke_kb_version)} ⚠️ **Out of sync**\n"
    
    # Health metrics if available
    if scf_metadata and scf_metadata.get('health_metrics'):
        health = scf_metadata['health_metrics']
        days_since_sync = health.get('days_since_sync', 0)
        sync_frequency = health.get('sync_frequency', 'unknown')
        drift_score = health.get('drift_score', 0.0)
        
        overview += f"\n**Sync Health:**\n"
        overview += f"- **Days since sync:** {days_since_sync}\n"
        overview += f"- **Sync frequency:** {sync_frequency}\n"
        overview += f"- **Drift score:** {drift_score:.1f}\n"
    
    return overview


def main():
    """CLI entry point"""
    if len(sys.argv) != 2:
        print("Usage: python3 scf_enhanced_overview.py <project_path>")
        sys.exit(1)
    
    project_path = Path(sys.argv[1]).resolve()
    if not project_path.exists():
        print(f"Error: Project path '{project_path}' does not exist")
        sys.exit(1)
    
    overview = generate_enhanced_overview(project_path)
    print(overview)


if __name__ == '__main__':
    main()