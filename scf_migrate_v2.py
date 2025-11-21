#!/usr/bin/env python3
"""
SCF v1 to v2 Migration Script - Automated migration from root-level buildstate to .scf/ structure
"""
import json, shutil, sys
from pathlib import Path
from datetime import datetime

class SCFMigrationV2:
    def __init__(self, project_path, dry_run=False):
        self.project_path = Path(project_path).resolve()
        self.dry_run = dry_run
        self.backup_dir = self.project_path / ".scf_v1_backup"
        self.scf_dir = self.project_path / ".scf"
        self.hub_path = Path.home() / "projects" / "session-continuity-framework"
    
    def detect_v1_files(self):
        return {
            "buildstate.json": (self.project_path / "buildstate.json").exists(),
            "buildstate.md": (self.project_path / "buildstate.md").exists()
        }
    
    def run_migration(self):
        print(f"\n{'='*60}\nSCF v1 → v2 Migration\nProject: {self.project_path}")
        if self.dry_run: print("Mode: DRY RUN")
        print(f"{'='*60}\n")
        
        v1_files = self.detect_v1_files()
        if not any(v1_files.values()):
            print("❌ No SCF v1 files found. Use init_scf.py for new projects.")
            return False
        
        # Step 1: Backup
        print("📦 Creating backup...")
        if not self.dry_run:
            self.backup_dir.mkdir(exist_ok=True)
            for name, exists in v1_files.items():
                if exists:
                    shutil.copy2(self.project_path / name, self.backup_dir / name)
            print("   ✅ Backup created")
        else:
            print("   [DRY RUN] Would create backup")
        
        # Step 2: Create .scf structure
        print("\n📁 Creating .scf/ structure...")
        dirs = [self.scf_dir, self.scf_dir / "archives", self.scf_dir / "sessions", self.scf_dir / "voices"]
        if not self.dry_run:
            for d in dirs: d.mkdir(parents=True, exist_ok=True)
            print("   ✅ Structure created")
        else:
            print("   [DRY RUN] Would create .scf/ directories")
        
        # Step 3: Migrate buildstate.json
        print("\n📝 Migrating buildstate.json...")
        if v1_files["buildstate.json"]:
            if not self.dry_run:
                with open(self.project_path / "buildstate.json", 'r') as f:
                    data = json.load(f)
                data["meta"]["scf_version"] = "v2.0.0"
                data["project"]["structure_version"] = "v2-dotscf"
                data["project"]["expected_location"] = ".scf/"
                if "scf_metadata" not in data:
                    data["scf_metadata"] = {}
                data["scf_metadata"]["scf_hub"] = str(self.hub_path)
                data["scf_metadata"]["migrated_from_v1"] = datetime.now().isoformat()
                with open(self.scf_dir / "BUILDSTATE.json", 'w') as f:
                    json.dump(data, f, indent=2)
                (self.project_path / "buildstate.json").unlink()
                print("   ✅ Migrated buildstate.json → .scf/BUILDSTATE.json")
            else:
                print("   [DRY RUN] Would migrate buildstate.json")
        
        # Step 4: Migrate buildstate.md
        print("\n📝 Migrating buildstate.md...")
        if v1_files["buildstate.md"]:
            if not self.dry_run:
                content = (self.project_path / "buildstate.md").read_text()
                if "SCF v2.0" not in content:
                    header = f"**SCF v2.0** | **Structure: v2 (.scf/)** | **Hub: {self.hub_path}**\n\n---\n\n"
                    lines = content.split('\n')
                    if lines and lines[0].startswith('#'):
                        lines.insert(1, '\n' + header)
                        content = '\n'.join(lines)
                (self.scf_dir / "BUILDSTATE.md").write_text(content)
                (self.project_path / "buildstate.md").unlink()
                print("   ✅ Migrated buildstate.md → .scf/BUILDSTATE.md")
            else:
                print("   [DRY RUN] Would migrate buildstate.md")
        
        # Step 5: Create AGENTS.md
        print("\n🔗 Creating AGENTS.md...")
        if not self.dry_run:
            try:
                (self.project_path / "AGENTS.md").symlink_to(".scf/BUILDSTATE.md")
                print("   ✅ Created AGENTS.md symlink")
            except:
                shutil.copy2(self.scf_dir / "BUILDSTATE.md", self.project_path / "AGENTS.md")
                print("   ✅ Created AGENTS.md (copy)")
        else:
            print("   [DRY RUN] Would create AGENTS.md")
        
        print(f"\n{'='*60}")
        if self.dry_run:
            print("✅ Dry run complete. Run without --dry-run to migrate.")
        else:
            print("🎉 Migration complete!\n")
            print("📋 Next steps:")
            print("   1. Review .scf/BUILDSTATE.json and .scf/BUILDSTATE.md")
            print("   2. Test your project")
            print("   3. Delete .scf_v1_backup/ once verified")
        print(f"{'='*60}\n")
        return True

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Migrate SCF v1 to v2")
    parser.add_argument("project_path", type=Path)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    
    migrator = SCFMigrationV2(args.project_path, dry_run=args.dry_run)
    sys.exit(0 if migrator.run_migration() else 1)
