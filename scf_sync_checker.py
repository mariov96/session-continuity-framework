#!/usr/bin/env python3
"""
SCF Sync Status Checker

Quick utility to check if a spoke project has accurate sync information
and is using the enhanced tracking system.
"""

import json
from datetime import datetime, timezone
from pathlib import Path
import sys


def check_sync_status(project_path):
    """Check if project has enhanced tracking and accurate sync data"""
    project_path = Path(project_path)
    
    # Check for enhanced tracking in buildstate._scf_metadata
    buildstate_path = project_path / '.scf' / 'buildstate.json'
    
    print(f"🔍 Checking SCF sync status for: {project_path.name}")
    print("=" * 50)
    
    # Enhanced tracking check
    if buildstate_path.exists():
        try:
            with open(buildstate_path, 'r') as f:
                buildstate = json.load(f)
            
            scf_metadata = buildstate.get('_scf_metadata', {})
            if scf_metadata and 'last_sync_date' in scf_metadata:
                print("✅ Enhanced tracking available (buildstate._scf_metadata)")
            
                # Check last sync
                last_sync = scf_metadata.get('last_sync_date')
                if last_sync:
                    sync_dt = datetime.fromisoformat(last_sync.replace('Z', '+00:00'))
                    now = datetime.now(timezone.utc)
                    hours_ago = (now - sync_dt).total_seconds() / 3600
                
                if hours_ago < 1:
                    print(f"🟢 Recently synced: {int((now - sync_dt).total_seconds() / 60)} minutes ago")
                elif hours_ago < 24:
                    print(f"🟡 Synced: {int(hours_ago)} hours ago")
                else:
                    days_ago = int(hours_ago / 24)
                    print(f"🔴 Last sync: {days_ago} days ago")
            
                # Check hub reference
                hub_ref = scf_metadata.get('hub_reference', {})
                if hub_ref:
                    print(f"🔗 Hub: {hub_ref.get('github_repo', 'Unknown')}")
                    print(f"📍 Location: {hub_ref.get('local_path', 'Unknown')}")
                
                # Check sync history
                sync_history = scf_metadata.get('sync_history', [])
                if sync_history:
                    latest = sync_history[-1]
                    method = latest.get('method', 'unknown')
                    files = latest.get('files_touched', [])
                    print(f"🔄 Last sync method: {method}")
                    if files:
                        print(f"📂 Files updated: {len(files)} files")
            else:
                print("⚠️ Enhanced tracking section found but missing sync data")
            
        except Exception as e:
            print(f"❌ Error reading buildstate: {e}")
    else:
        print("⚠️ No enhanced tracking (missing buildstate.json)")
    
    # Legacy tracking check
    if buildstate_path.exists():
        try:
            with open(buildstate_path, 'r') as f:
                buildstate = json.load(f)
            
            session_state = buildstate.get('_session_state', {})
            scf_metadata = buildstate.get('_scf_metadata', {})
            
            print("\n📋 Legacy tracking (buildstate.json):")
            
            # Session info
            last_modified = session_state.get('last_modified_at')
            if last_modified:
                print(f"   Last modified: {last_modified}")
            
            session_count = session_state.get('session_count', 0)
            print(f"   Session count: {session_count}")
            
            # SCF metadata
            last_sync_legacy = scf_metadata.get('last_sync_date')
            if last_sync_legacy:
                print(f"   Legacy sync date: {last_sync_legacy}")
            
        except Exception as e:
            print(f"❌ Error reading buildstate: {e}")
    
    print("\n💡 Recommendations:")
    if buildstate_path.exists():
        with open(buildstate_path, 'r') as f:
            buildstate = json.load(f)
        
        if not buildstate.get('_scf_metadata', {}).get('last_sync_date'):
            print("   • Run 'teach.py --update' from hub to enable enhanced tracking")
        else:
            print("   • Enhanced tracking is active and up-to-date")
    else:
        print("   • Project not initialized with SCF - run 'teach.py --init'")


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python3 scf_sync_checker.py <project_path>")
        sys.exit(1)
    
    check_sync_status(sys.argv[1])