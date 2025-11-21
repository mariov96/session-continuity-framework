#!/usr/bin/env python3
"""
SCF Project Updater
==================

Update an existing SCF-enabled project with latest improvements.
This script performs targeted maintenance on a single project including
rebalancing, template updates, symlink management, and inheritance sync.

Usage:
    python3 update_scf.py /path/to/project
    python3 update_scf.py /path/to/project --force-rebalance
    python3 update_scf.py /path/to/project --dry-run

Features:
- Rebalances buildstate.json/md content
- Updates AGENTS.md symlink
- Syncs inheritance chain
- Merges template improvements
- Preserves project customizations
- Reports all changes made
- Does NOT scan other projects (use buildstate_hunter_learner.py for that)
"""

import json
import shutil
import argparse
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any, List, Tuple

# Import SCF components
try:
    from scf_rebalancer import SCFRebalancer
    REBALANCER_AVAILABLE = True
except ImportError:
    print("⚠️  SCF rebalancer not available")
    REBALANCER_AVAILABLE = False

try:
    from scf_inheritance import SCFProjectSetup, SCFInheritanceResolver
    INHERITANCE_AVAILABLE = True
except ImportError:
    print("⚠️  SCF inheritance system not available")
    INHERITANCE_AVAILABLE = False

try:
    from scf_llm_integration import SCFLLMIntegrator
    LLM_INTEGRATION_AVAILABLE = True
except ImportError:
    print("⚠️  SCF LLM integration not available")
    LLM_INTEGRATION_AVAILABLE = False

class SCFProjectUpdater:
    """Update and maintain individual SCF projects"""
    
    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        self.framework_root = Path(__file__).parent
        self.templates_dir = self.framework_root / "templates"
        self.changes_made = []
        
    def update_project(self, project_path: Path, 
                      force_rebalance: bool = False,
                      skip_inheritance: bool = False,
                      skip_rebalance: bool = False,
                      auto_commit: bool = False) -> bool:
       """Update SCF for a specific project"""
        
        print(f"🔄 Updating SCF for project: {project_path.name}")
        print(f"📁 Project path: {project_path.absolute()}")
        if self.dry_run:
            print("🔍 DRY RUN - No files will be modified")
        print("=" * 60)
        
        # Validate project
        if not self._validate_project(project_path):
            return False
            
        # Step 1: Rebalance content
        if not skip_rebalance:
            success = self._rebalance_content(project_path, force_rebalance)
            if not success:
                print("   ⚠️  Rebalancing skipped or failed")
        else:
            print("⏭️  Step 1: Rebalancing skipped (--skip-rebalance)")
            
        # Step 2: Update AGENTS.md compatibility
        success = self._update_agents_compatibility(project_path)
        if not success:
            print("   ⚠️  AGENTS.md update had issues")
            
        # Step 3: Sync inheritance chain
        if not skip_inheritance and INHERITANCE_AVAILABLE:
            success = self._sync_inheritance(project_path)
            if not success:
                print("   ⚠️  Inheritance sync had issues")
        else:
            if skip_inheritance:
                print("⏭️  Step 3: Inheritance sync skipped (--skip-inheritance)")
            else:
                print("⏭️  Step 3: Inheritance system not available")
                
        # Step 4: Merge template improvements (carefully)
        success = self._merge_template_updates(project_path)
        if not success:
            print("   ⚠️  Template merge had issues")
            
        # Step 5: Update LLM integration
        success = self._update_llm_integration(project_path)
        if not success:
            print("   ⚠️  LLM integration update had issues")
            
        # Report changes
        self._report_changes(project_path)

        # Step 6: Auto-commit changes if requested
        if auto_commit:
            self._auto_commit_changes(project_path)
        
        print("\n🎉 SCF update complete!")
        print(f"✅ Project {project_path.name} is up to date")
        
        return True
    
    def _validate_project(self, project_path: Path) -> bool:
        """Validate project is SCF-enabled"""
        
        if not project_path.exists():
            print(f"❌ Error: Project path does not exist: {project_path}")
            return False
            
        if not project_path.is_dir():
            print(f"❌ Error: Path is not a directory: {project_path}")
            return False
            
        buildstate_json = project_path / "buildstate.json"
        buildstate_md = project_path / "buildstate.md"
        
        if not buildstate_json.exists() and not buildstate_md.exists():
            print(f"❌ Error: Project is not SCF-enabled")
            print(f"   No buildstate files found in {project_path}")
            print(f"   Use init_scf.py to initialize SCF first")
            return False
            
        print("✅ Project validation passed")
        return True
    
    def _rebalance_content(self, project_path: Path, force: bool = False) -> bool:
        """Rebalance buildstate.json and buildstate.md content"""
        
        print(f"⚖️  Step 1: Rebalancing content")
        
        if not REBALANCER_AVAILABLE:
            print("   ⏭️  Rebalancer not available - skipping")
            return True
            
        try:
            rebalancer = SCFRebalancer()
            
            # Check current balance
            score = rebalancer.analyze_balance(project_path)
            print(f"   📊 Current balance score: {score:.2f}")
            
            # Only rebalance if needed or forced
            threshold = 0.7
            needs_rebalance = score < threshold or force
            
            if needs_rebalance:
                if self.dry_run:
                    print(f"   🔍 Would rebalance (score: {score:.2f} < {threshold})")
                    suggestions = rebalancer.suggest_moves(project_path)
                    print(f"   📋 Suggested moves: {len(suggestions)}")
                else:
                    print(f"   🔄 Rebalancing project...")
                    result = rebalancer.rebalance_project(project_path)
                    if result['success']:
                        self.changes_made.append(f"Rebalanced content (score: {score:.2f} → {result['new_score']:.2f})")
                        print(f"   ✅ Rebalancing complete: {score:.2f} → {result['new_score']:.2f}")
                    else:
                        print(f"   ⚠️  Rebalancing failed: {result.get('error', 'Unknown error')}")
                        return False
            else:
                print(f"   ✅ Balance is good (score: {score:.2f} >= {threshold})")
                
        except Exception as e:
            print(f"   ❌ Error during rebalancing: {e}")
            return False
            
        return True
    
    def _update_agents_compatibility(self, project_path: Path) -> bool:
        """Update or create AGENTS.md symlink"""
        
        print(f"🔗 Step 2: Updating AGENTS.md compatibility")
        
        agents_md_path = project_path / "AGENTS.md"
        buildstate_md_path = project_path / "buildstate.md"
        
        if not buildstate_md_path.exists():
            print("   ⚠️  buildstate.md not found - cannot create AGENTS.md")
            return False
            
        try:
            # Check current state
            if agents_md_path.is_symlink():
                target = agents_md_path.resolve()
                if target == buildstate_md_path:
                    print("   ✅ AGENTS.md symlink already correct")
                    return True
                else:
                    print(f"   🔄 AGENTS.md points to wrong target: {target}")
                    if not self.dry_run:
                        agents_md_path.unlink()
                        
            elif agents_md_path.exists():
                print("   ⚠️  AGENTS.md exists as regular file (not symlink)")
                print("   💡 Tip: Remove it manually to create symlink, or keep custom version")
                return True
                
            # Create symlink
            if self.dry_run:
                print(f"   🔍 Would create AGENTS.md → buildstate.md symlink")
            else:
                agents_md_path.symlink_to("buildstate.md")
                self.changes_made.append("Created AGENTS.md → buildstate.md symlink")
                print(f"   ✅ Created AGENTS.md → buildstate.md symlink")
                
        except (OSError, FileExistsError) as e:
            print(f"   ⚠️  Could not create symlink: {e}")
            # Try generating static AGENTS.md as fallback
            if LLM_INTEGRATION_AVAILABLE and not self.dry_run:
                try:
                    integrator = SCFLLMIntegrator(project_path)
                    content = integrator.generate_agents_md()
                    with open(agents_md_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    self.changes_made.append("Generated static AGENTS.md")
                    print(f"   ✅ Generated static AGENTS.md as fallback")
                except Exception as fallback_error:
                    print(f"   ❌ Fallback generation failed: {fallback_error}")
                    return False
                    
        return True
    
    def _sync_inheritance(self, project_path: Path) -> bool:
        """Sync inheritance chain and pull updates"""
        
        print(f"🔗 Step 3: Syncing inheritance chain")
        
        if self.dry_run:
            print(f"   🔍 Would sync inheritance for {project_path.name}")
            return True
            
        try:
            # Check if .scf directory exists
            scf_dir = project_path / ".scf"
            if not scf_dir.exists():
                print("   ⚠️  No .scf directory - setting up inheritance")
                project_setup = SCFProjectSetup()
                project_setup.setup_project_inheritance(project_path, create_missing=True)
                self.changes_made.append("Set up inheritance chain")
                return True
                
            # Resolve current configuration
            resolver = SCFInheritanceResolver()
            chain = resolver.setup_inheritance_chain(project_path)
            
            print(f"   📋 Inheritance chain:")
            for rule in chain:
                status = "✅" if rule.exists else "❌"
                print(f"      {status} {rule.level.value}: {rule.path}")
                
            # Check for library updates
            resolved = resolver.resolve_configuration()
            self.changes_made.append("Synced inheritance chain")
            print(f"   ✅ Inheritance chain synced")
            
        except Exception as e:
            print(f"   ❌ Error syncing inheritance: {e}")
            return False
            
        return True
    
    def _merge_template_updates(self, project_path: Path) -> bool:
        """Carefully merge template improvements without overwriting customizations"""
        
        print(f"🔄 Step 4: Merging template improvements")
        
        buildstate_json_path = project_path / "buildstate.json"
        
        if not buildstate_json_path.exists():
            print("   ⚠️  No buildstate.json to update")
            return False
            
        try:
            # Load current project buildstate
            with open(buildstate_json_path, 'r', encoding='utf-8') as f:
                project_data = json.load(f)
                
            # Load latest template (favoring llm-enhanced)
            template_path = self.templates_dir / "buildstate-llm-enhanced.json"
            if not template_path.exists():
                template_path = self.templates_dir / "buildstate.json"

            if not template_path.exists():
                print("   ⚠️  No suitable template found - skipping merge")
                return True
                
            with open(template_path, 'r', encoding='utf-8') as f:
                template_data = json.load(f)
                
            # Merge improvements (preserve customizations)
            updates_made = self._recursive_merge(template_data, project_data)

            # Also update the sync date and version
            if '_scf_metadata' in project_data and '_scf_metadata' in template_data:
                project_data['_scf_metadata']['last_sync_date'] = datetime.utcnow().isoformat()
                new_version = template_data['_scf_metadata'].get('template_version')
                if new_version:
                    project_data['_scf_metadata']['template_version'] = new_version
                updates_made.append("Updated _scf_metadata sync date and version")
            
            # Save if updates were made
            if updates_made:
                if self.dry_run:
                    print(f"   🔍 Would merge {len(updates_made)} improvements:")
                    for update in updates_made:
                        print(f"     - {update}")
                else:
                    # Create backup first
                    backup_path = buildstate_json_path.with_suffix(f'.json.backup.{datetime.now().strftime("%Y%m%d_%H%M%S")}')
                    shutil.copy2(buildstate_json_path, backup_path)
                    
                    # Save updated file
                    with open(buildstate_json_path, 'w', encoding='utf-8') as f:
                        json.dump(project_data, f, indent=2, ensure_ascii=False)
                        
                    self.changes_made.extend(updates_made)
                    print(f"   ✅ Merged {len(updates_made)} template improvements")
                    print(f"   💾 Backup saved: {backup_path.name}")
            else:
                print(f"   ✅ Project already has latest template features")
                
        except Exception as e:
            print(f"   ❌ Error merging templates: {e}")
            return False
            
        return True

    def _recursive_merge(self, template: Dict[str, Any], project: Dict[str, Any], path: str = "") -> List[str]:
        """
        Recursively merge new keys from template into project data.
        Returns a list of changes made.
        """
        changes = []
        for key, value in template.items():
            current_path = f"{path}.{key}" if path else key
            if key not in project:
                project[key] = value
                changes.append(f"Added new key: {current_path}")
            elif isinstance(value, dict) and isinstance(project.get(key), dict):
                # Recurse into nested dictionaries
                nested_changes = self._recursive_merge(value, project[key], path=current_path)
                changes.extend(nested_changes)
        return changes
    
    def _update_llm_integration(self, project_path: Path) -> bool:
        """Update LLM integration capabilities"""
        
        print(f"🤖 Step 5: Updating LLM integration")
        
        if not LLM_INTEGRATION_AVAILABLE:
            print("   ⏭️  LLM integration not available - skipping")
            return True
            
        if self.dry_run:
            print(f"   🔍 Would update LLM integration for {project_path.name}")
            print(f"   🔍 Would regenerate .github/copilot-instructions.md")
            print(f"   🔍 Would update .github/instructions/*.instructions.md")
            print(f"   🔍 Would update .github/prompts/*.prompt.md")
            return True
            
        try:
            # Test integration
            integrator = SCFLLMIntegrator(project_path)
            
            # Generate fresh AGENTS.md if needed
            agents_md = project_path / "AGENTS.md"
            if not agents_md.exists() or not agents_md.is_symlink():
                content = integrator.generate_agents_md()
                if content:
                    self.changes_made.append("Refreshed AGENTS.md content")
                    print(f"   ✅ AGENTS.md updated")
            else:
                print(f"   ✅ AGENTS.md symlink functional")
            
            # Regenerate GitHub Copilot instructions
            print(f"\n   📝 Updating GitHub Copilot instructions...")
            try:
                # Repository-wide instructions
                copilot_content = integrator.generate_copilot_instructions()
                self.changes_made.append("Updated .github/copilot-instructions.md")
                print(f"   ✅ Updated .github/copilot-instructions.md ({len(copilot_content)} chars)")
                
                # Path-specific instructions for existing directories
                common_paths = ['src', 'tests', 'docs', 'lib', 'components']
                updated_paths = []
                for path in common_paths:
                    if (project_path / path).exists():
                        integrator.generate_path_instructions(path)
                        updated_paths.append(path)
                
                if updated_paths:
                    self.changes_made.append(f"Updated path instructions for: {', '.join(updated_paths)}")
                    print(f"   ✅ Updated {len(updated_paths)} path-specific instruction files")
                
                # Prompt file templates
                prompts = integrator.generate_prompt_files()
                self.changes_made.append(f"Updated {len(prompts)} prompt files")
                print(f"   ✅ Updated {len(prompts)} prompt files")
                
                print(f"   🎯 GitHub Copilot context refreshed!")
                
            except Exception as copilot_error:
                print(f"   ⚠️  GitHub Copilot instructions update warning: {copilot_error}")
                # Not critical, continue
                
        except Exception as e:
            print(f"   ⚠️  LLM integration check warning: {e}")
            # Not critical
            
        return True

    def _auto_commit_changes(self, project_path: Path):
        """Automatically commit changes to git if requested."""
        if not self.changes_made or self.dry_run:
            return

        print(f"🤖 Step 6: Auto-committing changes")
        try:
            # Check if it's a git repository
            subprocess.run(["git", "rev-parse"], cwd=project_path, check=True, capture_output=True)

            commit_message = f"chore(scf): Auto-update SCF for {project_path.name}\n\n"
            commit_message += "Changes made:\n"
            for change in self.changes_made:
                commit_message += f"- {change}\n"

            # Stage the buildstate files
            subprocess.run(["git", "add", "buildstate.json", "buildstate.md"], cwd=project_path, check=True)
            
            # Commit the changes
            subprocess.run(["git", "commit", "-m", commit_message], cwd=project_path, check=True)
            
            print("   ✅ Changes committed successfully.")

        except (subprocess.CalledProcessError, FileNotFoundError):
            print("   ⚠️  Could not auto-commit. Is this a git repository?")
    
    def _report_changes(self, project_path: Path):
        """Report all changes made during update"""
        
        print(f"\n📊 Update Summary for {project_path.name}")
        print("=" * 60)
        
        if not self.changes_made:
            print("✅ No changes needed - project is up to date")
        else:
            print(f"✅ Made {len(self.changes_made)} changes:")
            for i, change in enumerate(self.changes_made, 1):
                print(f"   {i}. {change}")
                
        if self.dry_run:
            print("\n🔍 DRY RUN - No actual changes were made")
            print("   Run without --dry-run to apply changes")

def main():
    parser = argparse.ArgumentParser(
        description="Update SCF for a specific project",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 update_scf.py /path/to/my-project
  python3 update_scf.py /path/to/my-project --force-rebalance
  python3 update_scf.py /path/to/my-project --dry-run
  python3 update_scf.py /path/to/my-project --skip-rebalance
        """
    )
    
    parser.add_argument('project_path', type=Path,
                       help='Path to SCF-enabled project to update')
    parser.add_argument('--force-rebalance', action='store_true',
                       help='Force rebalancing even if score is good')
    parser.add_argument('--skip-rebalance', action='store_true',
                       help='Skip content rebalancing step')
    parser.add_argument('--skip-inheritance', action='store_true',
                       help='Skip inheritance chain sync')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be done without making changes')
    parser.add_argument('--auto-commit', action='store_true',
                       help='Automatically commit changes with a standardized message')
    
    args = parser.parse_args()
    
    # Update the project
    updater = SCFProjectUpdater(dry_run=args.dry_run)
    success = updater.update_project(
        args.project_path,
        force_rebalance=args.force_rebalance,
        skip_inheritance=args.skip_inheritance,
        skip_rebalance=args.skip_rebalance,
        auto_commit=args.auto_commit
    )
    
    if success:
        print(f"\n🎯 SCF update successful for {args.project_path.name}")
        exit(0)
    else:
        print(f"\n❌ SCF update had issues for {args.project_path}")
        exit(1)

if __name__ == "__main__":
    main()
