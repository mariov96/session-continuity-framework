#!/usr/bin/env python3
"""
SCF Project Initializer
======================

Initialize a specific project with Session Continuity Framework (SCF).
This script sets up a single project with the latest SCF templates,
inheritance chain, and ecosystem compatibility features.

Usage:
    python3 init_scf.py /path/to/project
    python3 init_scf.py /path/to/project --template-type web-app
    python3 init_scf.py /path/to/project --dry-run

Features:
- Copies latest buildstate templates
- Sets up 4-level inheritance chain
- Creates AGENTS.md ecosystem compatibility
- Initializes project-specific SCF configuration
- Creates .scf directory with project library
- Does NOT scan other projects (use buildstate_hunter_learner.py for that)
"""

import json
import shutil
import argparse
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any

# Import SCF components
try:
    from scf_inheritance import SCFProjectSetup, SCFInheritanceResolver
    from scf_llm_integration import SCFLLMIntegrator
    INHERITANCE_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  SCF inheritance system not available: {e}")
    INHERITANCE_AVAILABLE = False

class SCFProjectInitializer:
    """Initialize individual projects with SCF"""
    
    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        self.framework_root = Path(__file__).parent
        self.templates_dir = self.framework_root / "templates"
        
    def init_project(self, project_path: Path, template_type: str = "default", 
                    force: bool = False,
                    auto_commit: bool = False) -> bool:
        """Initialize SCF for a specific project"""
        
        print(f"🚀 Initializing SCF for project: {project_path}")
        print(f"📁 Project path: {project_path.absolute()}")
        print(f"📋 Template type: {template_type}")
        if self.dry_run:
            print("🔍 DRY RUN - No files will be modified")
        print("=" * 60)
        
        # Validate project path
        if not project_path.exists():
            print(f"❌ Error: Project path does not exist: {project_path}")
            return False
            
        if not project_path.is_dir():
            print(f"❌ Error: Path is not a directory: {project_path}")
            return False
        
        # Check if already SCF-enabled
        buildstate_json = project_path / "buildstate.json"
        buildstate_md = project_path / "buildstate.md"
        
        if (buildstate_json.exists() or buildstate_md.exists()) and not force:
            print(f"⚠️  Project already has SCF files:")
            if buildstate_json.exists():
                print(f"   📄 {buildstate_json}")
            if buildstate_md.exists():
                print(f"   📄 {buildstate_md}")
            print("   Use --force to reinitialize or use update_scf.py to update")
            return False
            
        # Step 1: Copy buildstate templates
        success = self._copy_templates(project_path, template_type)
        if not success:
            return False
            
        # Step 2: Customize templates for project
        success = self._customize_templates(project_path)
        if not success:
            return False
            
        # Step 3: Set up inheritance chain
        if INHERITANCE_AVAILABLE:
            success = self._setup_inheritance(project_path)
            if not success:
                return False
        else:
            print("⚠️  Inheritance system not available - skipping")
            
        # Step 4: Create AGENTS.md ecosystem compatibility
        success = self._setup_agents_compatibility(project_path)
        if not success:
            return False
            
        # Step 5: Initialize LLM integration
        success = self._setup_llm_integration(project_path)
        if not success:
            return False

        # Step 6: Auto-commit changes if requested
        if auto_commit:
            self._auto_commit_changes(project_path)
            
        print("\n🎉 SCF initialization complete!")
        print(f"✅ Project {project_path.name} is now SCF-enabled")
        print("\n📋 Next steps:")
        print("   1. Edit buildstate.md for project ideation and strategy")
        print("   2. Edit buildstate.json for technical specifications")
        print("   3. Use update_scf.py for future maintenance")
        print("   4. Use buildstate_hunter_learner.py for ecosystem learning")
        
        return True
    
    def _copy_templates(self, project_path: Path, template_type: str) -> bool:
        """Copy appropriate buildstate templates to project"""
        
        print(f"📋 Step 1: Copying SCF templates")
        
        # Determine template files
        if template_type == "llm-enhanced":
            json_template = self.templates_dir / "buildstate-llm-enhanced.json"
            md_template = self.templates_dir / "buildstate-llm-enhanced.md"
        else:
            json_template = self.templates_dir / "buildstate.json"
            md_template = self.templates_dir / "buildstate.md"
            
        if not json_template.exists():
            print(f"   ❌ JSON template not found: {json_template}")
            return False
            
        if not md_template.exists():
            print(f"   ❌ Markdown template not found: {md_template}")
            return False
            
        # Copy templates
        target_json = project_path / "buildstate.json"
        target_md = project_path / "buildstate.md"
        
        if not self.dry_run:
            shutil.copy2(json_template, target_json)
            shutil.copy2(md_template, target_md)
            
        print(f"   ✅ Copied: {json_template.name} → {target_json.name}")
        print(f"   ✅ Copied: {md_template.name} → {target_md.name}")
        
        return True
    
    def _customize_templates(self, project_path: Path) -> bool:
        """Customize templates with project-specific information"""
        
        print(f"🔧 Step 2: Customizing templates for {project_path.name}")
        
        buildstate_json_path = project_path / "buildstate.json"
        
        if self.dry_run:
            print(f"   🔍 Would customize {buildstate_json_path}")
            return True
            
        try:
            # Load and customize JSON template
            with open(buildstate_json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # Update project-specific fields
            data['project']['name'] = project_path.name
            data['meta']['repo'] = project_path.name

            # Update SCF metadata
            if '_scf_metadata' in data:
                data['_scf_metadata']['last_sync_date'] = datetime.utcnow().isoformat()
            
            # Add initialization log entry
            if 'change_log' not in data:
                data['change_log'] = []
                
            data['change_log'].append({
                "date": datetime.now().strftime('%Y-%m-%d'),
                "version": "v1.0",
                "desc": f"SCF initialization for {project_path.name}",
                "synced_with": "buildstate.md",
                "scf_version": "enhanced"
            })
            
            # Update next steps for new project
            data['next_steps'] = [
                "Define project scope and objectives in buildstate.md",
                "Set up development environment",
                "Establish technical stack and architecture",
                "Create initial project structure"
            ]
            
            # Save customized template
            with open(buildstate_json_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
                
            print(f"   ✅ Customized buildstate.json for {project_path.name}")
            
        except Exception as e:
            print(f"   ❌ Error customizing templates: {e}")
            return False
            
        return True
    
    def _setup_inheritance(self, project_path: Path) -> bool:
        """Set up SCF inheritance chain"""
        
        print(f"🔗 Step 3: Setting up inheritance chain")
        
        if self.dry_run:
            print(f"   🔍 Would set up inheritance for {project_path}")
            return True
            
        try:
            # Create private directory and .gitignore
            scf_dir = project_path / ".scf"
            private_dir = scf_dir / "private"
            private_dir.mkdir(parents=True, exist_ok=True)
            
            gitignore_path = scf_dir / ".gitignore"
            gitignore_content = "private/"
            if not gitignore_path.exists() or gitignore_content not in gitignore_path.read_text():
                with open(gitignore_path, "a") as f:
                    f.write(f"\n{gitignore_content}\n")
                print(f"   ✅ Created .gitignore to protect private overrides")

            project_setup = SCFProjectSetup()
            success = project_setup.setup_project_inheritance(
                project_path,
                create_missing=True
            )
            
            if success:
                print(f"   ✅ Inheritance chain established")
            else:
                print(f"   ⚠️  Inheritance setup completed with warnings")
                
        except Exception as e:
            print(f"   ❌ Error setting up inheritance: {e}")
            return False
            
        return True
    
    def _setup_agents_compatibility(self, project_path: Path) -> bool:
        """Set up AGENTS.md ecosystem compatibility"""
        
        print(f"🔗 Step 4: Setting up AGENTS.md ecosystem compatibility")
        
        agents_md_path = project_path / "AGENTS.md"
        buildstate_md_path = project_path / "buildstate.md"
        
        if self.dry_run:
            print(f"   🔍 Would create AGENTS.md symlink: {agents_md_path}")
            return True
            
        try:
            # Create symlink to buildstate.md
            if buildstate_md_path.exists():
                # Remove existing symlink if present
                if agents_md_path.is_symlink():
                    agents_md_path.unlink()
                    
                # Create relative symlink
                agents_md_path.symlink_to("buildstate.md")
                print(f"   ✅ Created AGENTS.md → buildstate.md symlink")
                
            else:
                print(f"   ⚠️  buildstate.md not found - skipping AGENTS.md setup")
                
        except (OSError, FileExistsError) as e:
            print(f"   ⚠️  Could not create symlink: {e}")
            # Fallback: Generate static AGENTS.md
            try:
                integrator = SCFLLMIntegrator(project_path)
                content = integrator.generate_agents_md()
                with open(agents_md_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"   ✅ Generated static AGENTS.md from templates")
            except Exception as fallback_error:
                print(f"   ⚠️  Fallback AGENTS.md generation failed: {fallback_error}")
                
        return True
    
    def _setup_llm_integration(self, project_path: Path) -> bool:
        """Initialize LLM integration capabilities"""
        
        print(f"🤖 Step 5: Setting up LLM integration")
        
        if self.dry_run:
            print(f"   🔍 Would initialize LLM integration for {project_path}")
            print(f"   🔍 Would generate .github/copilot-instructions.md")
            print(f"   🔍 Would generate .github/instructions/*.instructions.md")
            print(f"   🔍 Would generate .github/prompts/*.prompt.md")
            return True
            
        try:
            # Test LLM integration initialization
            integrator = SCFLLMIntegrator(project_path)
            
            # Verify buildstate loading works
            context = integrator.prepare_session_context(
                session_type=integrator.SessionType.INITIALIZATION,
                llm_type=integrator.LLMType.GENERIC
            )
            
            if context:
                print(f"   ✅ LLM integration ready")
                print(f"   📊 Context prepared: {len(context.formatted_context)} chars")
            else:
                print(f"   ⚠️  LLM integration initialized but context generation needs buildstate content")
            
            # Generate GitHub Copilot instructions
            print(f"\n   📝 Generating GitHub Copilot instructions...")
            try:
                # Repository-wide instructions
                copilot_content = integrator.generate_copilot_instructions()
                print(f"   ✅ Generated .github/copilot-instructions.md ({len(copilot_content)} chars)")
                
                # Path-specific instructions for common directories
                common_paths = ['src', 'tests', 'docs']
                for path in common_paths:
                    if (project_path / path).exists():
                        integrator.generate_path_instructions(path)
                        print(f"   ✅ Generated .github/instructions/{path.replace('/', '-')}.instructions.md")
                
                # Prompt file templates
                prompts = integrator.generate_prompt_files()
                print(f"   ✅ Generated {len(prompts)} prompt files in .github/prompts/")
                
                print(f"   🎯 GitHub Copilot now has full project context!")
                
            except Exception as copilot_error:
                print(f"   ⚠️  GitHub Copilot instructions generation warning: {copilot_error}")
                # Not critical, continue
                
        except Exception as e:
            print(f"   ⚠️  LLM integration setup warning: {e}")
            # Not critical for initialization
            
        return True

    def _auto_commit_changes(self, project_path: Path):
        """Automatically commit initial SCF files to git."""
        if self.dry_run:
            print("   🔍 Would auto-commit initial SCF files")
            return

        print(f"🤖 Step 6: Auto-committing initial files")
        try:
            # Check if it's a git repository
            subprocess.run(["git", "rev-parse"], cwd=project_path, check=True, capture_output=True)

            commit_message = f"feat(scf): Initialize Session Continuity Framework\n\n"
            commit_message += "This commit adds the initial SCF files to the project, including:\n"
            commit_message += "- buildstate.json: For technical specifications and AI rules.\n"
            commit_message += "- buildstate.md: For strategic vision and documentation.\n"
            commit_message += "- .scf/: For inheritance and private configurations.\n"
            commit_message += "- AGENTS.md: For ecosystem compatibility."

            # Stage the new files
            files_to_add = [
                "buildstate.json",
                "buildstate.md",
                ".scf/",
                "AGENTS.md",
                ".github/" # Also add copilot files
            ]
            for file_path in files_to_add:
                if (project_path / file_path).exists():
                    subprocess.run(["git", "add", str(file_path)], cwd=project_path, check=True)
            
            # Commit the changes
            subprocess.run(["git", "commit", "-m", commit_message], cwd=project_path, check=True)
            
            print("   ✅ Initial SCF files committed successfully.")

        except (subprocess.CalledProcessError, FileNotFoundError):
            print("   ⚠️  Could not auto-commit. Is this a git repository?")

def main():
    parser = argparse.ArgumentParser(
        description="Initialize SCF for a specific project",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 init_scf.py /path/to/my-project
  python3 init_scf.py /path/to/my-project --template-type llm-enhanced
  python3 init_scf.py /path/to/my-project --dry-run
  python3 init_scf.py /path/to/my-project --force
        """
    )
    
    parser.add_argument('project_path', type=Path, 
                       help='Path to project directory to initialize with SCF')
    parser.add_argument('--template-type', choices=['default', 'llm-enhanced'],
               default='llm-enhanced',
               help='Type of SCF templates to use (default: llm-enhanced)')
    parser.add_argument('--force', action='store_true',
                       help='Force initialization even if SCF files exist')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be done without making changes')
    parser.add_argument('--auto-commit', action='store_true',
                       help='Automatically commit the initial SCF files')
    
    args = parser.parse_args()
    
    # Initialize the project
    initializer = SCFProjectInitializer(dry_run=args.dry_run)
    success = initializer.init_project(
        args.project_path, 
        template_type=args.template_type,
        force=args.force,
        auto_commit=args.auto_commit
    )
    
    if success:
        print(f"\n🎯 SCF initialization successful for {args.project_path.name}")
        exit(0)
    else:
        print(f"\n❌ SCF initialization failed for {args.project_path}")
        exit(1)

if __name__ == "__main__":
    main()