#!/usr/bin/env python3
"""
SCF Inheritance System
=====================

Implements a rule-based inheritance hierarchy for buildstate files:
1. Local file (project-specific overrides)
2. External file in project (project-level configuration) 
3. Referenced file in another location (shared library/organization patterns)

This allows updating library files without touching actual project files.

Inheritance Chain:
  Local buildstate.json
    ↓ inherits from
  Project .scf/buildstate.library.json  
    ↓ inherits from
  Organization ~/scf-library/org-standards.json
    ↓ inherits from
  Global ~/.scf/global-defaults.json

Usage:
    # Set up inheritance for a project
    python scf_inheritance.py setup-project /path/to/project
    
    # Update library patterns (affects all inheriting projects)  
    python scf_inheritance.py update-library org-standards
    
    # Resolve final configuration for a project
    python scf_inheritance.py resolve /path/to/project/buildstate.json
"""

import json
import os
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, field
import argparse
from collections import ChainMap

@dataclass
class InheritanceRule:
    """Defines an inheritance rule in the chain"""
    level: int  # 0=local, 1=project, 2=org, 3=global
    name: str
    path: Path
    exists: bool = False
    content: Dict[str, Any] = field(default_factory=dict)
    last_modified: Optional[datetime] = None

class SCFInheritanceResolver:
    """Resolves buildstate inheritance chain"""
    
    def __init__(self):
        self.inheritance_chain = []
        self.resolved_config = {}
        
    def setup_inheritance_chain(self, project_path: Path) -> List[InheritanceRule]:
        """Establish the complete inheritance chain for a project"""
        
        chain = []
        
        # Level 0: Local project buildstate.json
        local_file = project_path / "buildstate.json"
        chain.append(InheritanceRule(
            level=0,
            name="local",
            path=local_file,
            exists=local_file.exists()
        ))
        
        # Level 1: Project library file (.scf/buildstate.library.json)
        project_lib = project_path / ".scf" / "buildstate.library.json"
        chain.append(InheritanceRule(
            level=1, 
            name="project_library",
            path=project_lib,
            exists=project_lib.exists()
        ))
        
        # Level 2: Organization standards (look for reference or default location)
        org_standards = self._find_org_standards(project_path)
        chain.append(InheritanceRule(
            level=2,
            name="org_standards", 
            path=org_standards,
            exists=org_standards.exists() if org_standards else False
        ))
        
        # Level 3: Global defaults (~/.scf/global-defaults.json)
        global_defaults = Path.home() / ".scf" / "global-defaults.json"
        chain.append(InheritanceRule(
            level=3,
            name="global_defaults",
            path=global_defaults,
            exists=global_defaults.exists()
        ))
        
        # Load content for existing files
        for rule in chain:
            if rule.exists:
                try:
                    rule.content = json.loads(rule.path.read_text(encoding='utf-8'))
                    rule.last_modified = datetime.fromtimestamp(rule.path.stat().st_mtime)
                except Exception as e:
                    print(f"⚠️  Warning: Could not load {rule.path}: {e}")
                    rule.exists = False
        
        self.inheritance_chain = chain
        return chain
        
    def _find_org_standards(self, project_path: Path) -> Optional[Path]:
        """Find organization standards file through various methods"""
        
        # Method 1: Check for .scf-org-ref file in project
        org_ref_file = project_path / ".scf" / ".scf-org-ref"
        if org_ref_file.exists():
            try:
                ref_path = Path(org_ref_file.read_text().strip())
                if ref_path.exists():
                    return ref_path
            except:
                pass
        
        # Method 2: Look for scf-library in parent directories
        current = project_path
        for _ in range(5):  # Search up 5 levels
            scf_lib = current / "scf-library" / "org-standards.json"
            if scf_lib.exists():
                return scf_lib
            current = current.parent
            if current == current.parent:  # Reached root
                break
                
        # Method 3: Check common organization locations
        common_locations = [
            Path.home() / "scf-library" / "org-standards.json",
            Path("/opt/scf-library/org-standards.json"),
            Path("C:/scf-library/org-standards.json"),
        ]
        
        for location in common_locations:
            if location.exists():
                return location
                
        return None
        
    def resolve_configuration(self, override_local: Dict = None) -> Dict[str, Any]:
        """Resolve the final configuration by merging inheritance chain"""
        
        if not self.inheritance_chain:
            raise ValueError("Inheritance chain not established. Call setup_inheritance_chain() first.")
        
        # Start with deepest inheritance (global) and work up
        configs = []
        
        for rule in reversed(self.inheritance_chain):
            if rule.exists and rule.content:
                configs.append(rule.content)
                
        # Add local override if provided
        if override_local:
            configs.append(override_local)
            
        # Use ChainMap for intelligent merging
        merged = {}
        for config in configs:
            merged = self._deep_merge(merged, config)
            
        # Add inheritance metadata
        merged['_inheritance'] = {
            'resolved_at': datetime.now().isoformat(),
            'chain': [
                {
                    'level': rule.level,
                    'name': rule.name,
                    'path': str(rule.path),
                    'exists': rule.exists,
                    'last_modified': rule.last_modified.isoformat() if rule.last_modified else None
                }
                for rule in self.inheritance_chain
            ]
        }
        
        self.resolved_config = merged
        return merged
        
    def _deep_merge(self, base: Dict, override: Dict) -> Dict:
        """Deep merge two dictionaries, with override taking precedence"""
        result = base.copy()
        
        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = value
                
        return result
        
    def show_inheritance_chain(self):
        """Display the current inheritance chain"""
        print("🔗 SCF Inheritance Chain")
        print("=" * 30)
        
        for rule in self.inheritance_chain:
            status = "✅" if rule.exists else "❌"
            modified = rule.last_modified.strftime("%Y-%m-%d %H:%M") if rule.last_modified else "N/A"
            
            print(f"{status} Level {rule.level}: {rule.name}")
            print(f"    📄 {rule.path}")
            if rule.exists:
                print(f"    🕒 Modified: {modified}")
                print(f"    📊 Keys: {len(rule.content)} configuration items")
            print()

class SCFLibraryManager:
    """Manages SCF library files and updates"""
    
    def __init__(self):
        self.library_locations = {}
        self._discover_libraries()
        
    def _discover_libraries(self):
        """Discover all SCF library locations"""
        
        # Common library locations
        locations = [
            Path.home() / "scf-library",
            Path("/opt/scf-library"), 
            Path("C:/scf-library"),
            # Look in current project ecosystem
            Path.cwd().parent / "scf-library"
        ]
        
        for location in locations:
            if location.exists():
                self.library_locations[location.name] = location
                
    def create_org_standards_template(self, output_path: Path):
        """Create a comprehensive organization standards template"""
        
        org_standards = {
            "_meta": {
                "type": "scf_org_standards",
                "version": "1.0",
                "description": "Organization-wide SCF standards and patterns",
                "created": datetime.now().isoformat(),
                "inheritance_level": 2
            },
            
            # Standard project structure
            "project_structure": {
                "required_files": ["README.md", "buildstate.json"],
                "recommended_dirs": ["src", "docs", "tests"],
                "forbidden_patterns": ["temp*", "*.tmp", "backup*"]
            },
            
            # Organization-wide coding standards  
            "coding_standards": {
                "organization": "Modular components, separate logic/services, grouped folders",
                "naming": {
                    "components": "PascalCase",
                    "functions": "camelCase", 
                    "constants": "UPPER_SNAKE_CASE",
                    "files": "kebab-case"
                },
                "documentation": {
                    "required": ["File headers", "Function comments", "API documentation"],
                    "style": "JSDoc for JavaScript, docstrings for Python"
                },
                "quality_gates": {
                    "linting": "required",
                    "testing": "min_coverage_80%",
                    "code_review": "required"
                }
            },
            
            # Standard AI collaboration rules
            "ai_rules": {
                "purpose": "Guide technical sessions using SCF buildstate files",
                "session": "Load buildstate.json for coding; use buildstate.md for ideation",
                "context_management": "Track exchanges, alert at 80% context limit", 
                "update_protocol": "Update features, bugs, next_steps, change_log after sessions",
                "rebalance_trigger": "After major feature implementation or bug resolution"
            },
            
            # Standard feature categories
            "feature_templates": {
                "authentication": {
                    "priority": "high",
                    "security_requirements": ["input_validation", "secure_storage", "session_management"]
                },
                "api_integration": {
                    "patterns": ["error_handling", "rate_limiting", "caching"]
                },
                "user_interface": {
                    "standards": ["accessibility", "responsive_design", "performance"]
                }
            },
            
            # Development environment standards
            "dev_environment": {
                "required_tools": ["git", "code_formatter", "linter"],
                "ide_configuration": {
                    "extensions": ["language_server", "formatter", "debugger"],
                    "settings": "standardized_across_team"
                },
                "containerization": {
                    "docker_required": False,
                    "dev_container_recommended": True
                }
            },
            
            # Quality metrics and tracking
            "quality_metrics": {
                "code_quality": ["complexity_score", "test_coverage", "documentation_ratio"],
                "project_health": ["active_development", "dependency_freshness", "security_status"],
                "team_velocity": ["feature_delivery_rate", "bug_resolution_time"]
            }
        }
        
        # Ensure directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write template
        with open(output_path, 'w') as f:
            json.dump(org_standards, f, indent=2)
            
        print(f"✅ Created organization standards template: {output_path}")
        
    def create_global_defaults(self, output_path: Path):
        """Create global SCF defaults"""
        
        global_defaults = {
            "_meta": {
                "type": "scf_global_defaults",
                "version": "1.0", 
                "description": "Global SCF framework defaults",
                "created": datetime.now().isoformat(),
                "inheritance_level": 3
            },
            
            # Basic project metadata template
            "meta": {
                "spec": "v1.0",
                "purpose": "Technical specification. See buildstate.md for ideation.",
                "framework": "SCF"
            },
            
            # Default project structure
            "project": {
                "version": "1.0",
                "stakeholder": "TBD"
            },
            
            # Basic lifecycle tracking
            "environment": {
                "phase": "Ideation",
                "focus": "Define scope, stack, and architecture"
            },
            
            # Standard tracking sections
            "user_stories": [],
            "success_metrics": [],
            "features": [],
            "bugs": [],
            "decisions": [],
            "issues": [],
            "next_steps": [],
            
            # Change tracking
            "change_log": [
                {
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "version": "v1.0",
                    "desc": "Initial SCF project setup",
                    "source": "scf_inheritance_system"
                }
            ],
            
            # Basic AI collaboration
            "ai_rules": {
                "purpose": "Guide technical sessions",
                "session": "Load for coding/debugging context",
                "update": "Maintain current state in buildstate files"
            }
        }
        
        # Ensure directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w') as f:
            json.dump(global_defaults, f, indent=2)
            
        print(f"✅ Created global defaults: {output_path}")
        
    def update_library_file(self, library_name: str, updates: Dict[str, Any], 
                           affected_projects: List[Path] = None):
        """Update a library file and optionally propagate to projects"""
        
        if library_name not in self.library_locations:
            print(f"❌ Library '{library_name}' not found")
            return
            
        library_path = self.library_locations[library_name]
        
        # Update the library file
        if (library_path / "org-standards.json").exists():
            standards_file = library_path / "org-standards.json"
            
            # Load current content
            current = json.loads(standards_file.read_text())
            
            # Create backup
            backup_path = standards_file.with_suffix(f".json.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}")
            shutil.copy2(standards_file, backup_path)
            print(f"📦 Backup created: {backup_path}")
            
            # Apply updates
            merged = self._deep_merge(current, updates)
            
            # Update modification metadata
            if '_meta' not in merged:
                merged['_meta'] = {}
            merged['_meta']['last_updated'] = datetime.now().isoformat()
            merged['_meta']['update_source'] = 'scf_library_manager'
            
            # Write updated file
            with open(standards_file, 'w') as f:
                json.dump(merged, f, indent=2)
                
            print(f"✅ Updated library file: {standards_file}")
            
            # Show what was updated
            print("📝 Updates applied:")
            for key, value in updates.items():
                print(f"   • {key}: {str(value)[:100]}...")
                
        else:
            print(f"❌ Standards file not found in {library_path}")
            
    def _deep_merge(self, base: Dict, override: Dict) -> Dict:
        """Deep merge utility"""
        result = base.copy()
        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = value
        return result

class SCFProjectSetup:
    """Sets up SCF inheritance for projects"""
    
    def __init__(self):
        self.resolver = SCFInheritanceResolver()
        self.library_manager = SCFLibraryManager()
        
    def setup_project_inheritance(self, project_path: Path, 
                                 create_missing: bool = True) -> bool:
        """Set up complete inheritance chain for a project"""
        
        print(f"🔧 Setting up SCF inheritance for: {project_path.name}")
        print("=" * 50)
        
        # Create .scf directory if needed
        scf_dir = project_path / ".scf"
        if not scf_dir.exists():
            scf_dir.mkdir(parents=True)
            print(f"📁 Created .scf directory")
            
        # Create project library file
        project_lib = scf_dir / "buildstate.library.json"
        if not project_lib.exists() and create_missing:
            self._create_project_library_template(project_lib, project_path)
            
        # Set up org standards reference
        self._setup_org_reference(scf_dir, create_missing)
        
        # Set up global defaults
        self._setup_global_defaults(create_missing)
        
        # Test the inheritance chain
        chain = self.resolver.setup_inheritance_chain(project_path)
        self.resolver.show_inheritance_chain()
        
        # Create AGENTS.md symlink for ecosystem compatibility
        self._setup_agents_md_compatibility(project_path)
        
        # Show resolved configuration sample
        if any(rule.exists for rule in chain):
            print("🎯 Sample Resolved Configuration:")
            resolved = self.resolver.resolve_configuration()
            
            # Show key inherited sections
            sample_keys = ['coding_standards', 'ai_rules', 'project_structure']
            for key in sample_keys:
                if key in resolved:
                    print(f"   📋 {key}: {len(resolved[key])} inherited items")
                    
        return True
        
    def _create_project_library_template(self, output_path: Path, project_path: Path):
        """Create project-specific library template"""
        
        project_lib = {
            "_meta": {
                "type": "scf_project_library",
                "version": "1.0",
                "description": f"Project-specific SCF configuration for {project_path.name}",
                "created": datetime.now().isoformat(),
                "inheritance_level": 1
            },
            
            # Project-specific overrides
            "project": {
                "name": project_path.name,
                "type": "TBD",  # Will be detected/specified
                "domain": "TBD"
            },
            
            # Project-specific coding standards (if different from org)
            "coding_standards": {
                "project_specific": {
                    "file_naming": f"{project_path.name.lower().replace('-', '_')}_*",
                    "module_prefix": project_path.name.lower().replace('-', '_')
                }
            },
            
            # Project-specific development environment
            "dev_environment": {
                "project_tools": [],
                "local_dependencies": [],
                "build_configuration": {}
            },
            
            # Project-specific AI context
            "ai_context": {
                "project_focus": "TBD - Define project's primary purpose",
                "technical_stack": "TBD - Define technologies used",
                "complexity_level": "medium"
            }
        }
        
        with open(output_path, 'w') as f:
            json.dump(project_lib, f, indent=2)
            
        print(f"📝 Created project library: {output_path}")
        
    def _setup_org_reference(self, scf_dir: Path, create_missing: bool):
        """Set up organization standards reference"""
        
        org_ref_file = scf_dir / ".scf-org-ref"
        
        # Look for existing org standards
        org_standards_path = self.resolver._find_org_standards(scf_dir.parent)
        
        if not org_standards_path and create_missing:
            # Create in a reasonable location
            org_lib_dir = Path.home() / "scf-library"
            org_lib_dir.mkdir(parents=True, exist_ok=True)
            org_standards_path = org_lib_dir / "org-standards.json"
            
            self.library_manager.create_org_standards_template(org_standards_path)
            
        if org_standards_path:
            # Create reference file
            org_ref_file.write_text(str(org_standards_path))
            print(f"🔗 Organization reference: {org_standards_path}")
        else:
            print("⚠️  No organization standards found or created")
            
    def _setup_global_defaults(self, create_missing: bool):
        """Set up global SCF defaults"""
        
        global_defaults_path = Path.home() / ".scf" / "global-defaults.json"
        
        if not global_defaults_path.exists() and create_missing:
            self.library_manager.create_global_defaults(global_defaults_path)
    
    def _setup_agents_md_compatibility(self, project_path: Path):
        """Set up AGENTS.md compatibility for ecosystem integration"""
        agents_md_path = project_path / "AGENTS.md"
        buildstate_md_path = project_path / "buildstate.md"
        
        # Skip if AGENTS.md already exists and is not a symlink
        if agents_md_path.exists() and not agents_md_path.is_symlink():
            print(f"   📄 AGENTS.md already exists (not overriding)")
            return
            
        # Create symlink to buildstate.md if it exists
        if buildstate_md_path.exists():
            try:
                # Remove existing symlink if present
                if agents_md_path.is_symlink():
                    agents_md_path.unlink()
                    
                # Create relative symlink
                agents_md_path.symlink_to("buildstate.md")
                print(f"   🔗 Created AGENTS.md → buildstate.md symlink")
                
            except (OSError, FileExistsError) as e:
                print(f"   ⚠️  Could not create AGENTS.md symlink: {e}")
                # Fallback: Generate static AGENTS.md from SCF
                try:
                    from scf_llm_integration import SCFLLMIntegrator
                    integrator = SCFLLMIntegrator(project_path)
                    content = integrator.generate_agents_md()
                    with open(agents_md_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"   📄 Generated static AGENTS.md from SCF buildstate")
                except ImportError:
                    print(f"   ⚠️  SCF LLM integration not available for AGENTS.md generation")
        else:
            print(f"   📄 buildstate.md not found - skipping AGENTS.md setup")

def main():
    parser = argparse.ArgumentParser(description="SCF Inheritance System")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Setup project command
    setup_parser = subparsers.add_parser('setup-project', help='Set up inheritance for a project')
    setup_parser.add_argument('project_path', type=Path, help='Path to project directory')
    setup_parser.add_argument('--no-create', action='store_true', help="Don't create missing files")
    
    # Resolve command
    resolve_parser = subparsers.add_parser('resolve', help='Resolve final configuration')
    resolve_parser.add_argument('buildstate_path', type=Path, help='Path to buildstate.json')
    resolve_parser.add_argument('--output', type=Path, help='Output resolved config to file')
    resolve_parser.add_argument('--show-chain', action='store_true', help='Show inheritance chain')
    
    # Update library command
    update_parser = subparsers.add_parser('update-library', help='Update organization library')
    update_parser.add_argument('library_name', help='Library name (e.g., org-standards)')
    update_parser.add_argument('--set', action='append', nargs=2, metavar=('KEY', 'VALUE'),
                              help='Set configuration values (can use multiple times)')
    
    # Show chain command
    chain_parser = subparsers.add_parser('show-chain', help='Show inheritance chain for project')
    chain_parser.add_argument('project_path', type=Path, help='Path to project directory')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
        
    if args.command == 'setup-project':
        setup = SCFProjectSetup()
        success = setup.setup_project_inheritance(
            args.project_path,
            create_missing=not args.no_create
        )
        if success:
            print("\n🎉 Project inheritance setup complete!")
        
    elif args.command == 'resolve':
        resolver = SCFInheritanceResolver()
        project_path = args.buildstate_path.parent
        
        chain = resolver.setup_inheritance_chain(project_path)
        
        if args.show_chain:
            resolver.show_inheritance_chain()
            
        resolved = resolver.resolve_configuration()
        
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(resolved, f, indent=2)
            print(f"✅ Resolved configuration saved to: {args.output}")
        else:
            print("\n🎯 Resolved Configuration Sample:")
            sample_keys = ['project', 'coding_standards', 'ai_rules']
            for key in sample_keys:
                if key in resolved:
                    print(f"   {key}: {json.dumps(resolved[key], indent=2)[:200]}...")
                    
    elif args.command == 'update-library':
        library_manager = SCFLibraryManager()
        
        if args.set:
            updates = {}
            for key, value in args.set:
                # Try to parse as JSON, fall back to string
                try:
                    updates[key] = json.loads(value)
                except:
                    updates[key] = value
                    
            library_manager.update_library_file(args.library_name, updates)
        else:
            print("No updates specified. Use --set KEY VALUE to update configurations.")
            
    elif args.command == 'show-chain':
        resolver = SCFInheritanceResolver()
        chain = resolver.setup_inheritance_chain(args.project_path)
        resolver.show_inheritance_chain()

if __name__ == "__main__":
    main()