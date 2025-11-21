# SCF Migration Guide: V1 → V2

**Version:** 2.0  
**Created:** November 20, 2025  
**Status:** Production Ready

---

## Overview

This guide helps you migrate Session Continuity Framework projects from V1 (root-based files) to V2 (.scf/ directory structure).

**Migration Time:** 2-5 minutes per project  
**Risk Level:** Low (backup created automatically)  
**Reversible:** Yes (keep v1 backup)

---

## What Changes in V2?

### File Locations
| V1 | V2 |
|----|-----|
| `buildstate.json` | `.scf/BUILDSTATE.json` |
| `buildstate.md` | `.scf/BUILDSTATE.md` |
| `buildstate.json.backup` | `.scf/archives/BUILDSTATE_*.json` |
| `AGENTS.md` (file) | `AGENTS.md` (symlink to `.scf/BUILDSTATE.md`) |

### File Names
- **V1:** lowercase (`buildstate.json`)
- **V2:** UPPERCASE (`BUILDSTATE.json`)

### New Structure
```
.scf/
├── BUILDSTATE.json
├── BUILDSTATE.md
├── archives/
├── sessions/
└── voices/
```

### New Fields
- `_session_state.scf_hub` - Hub location reference
- `_session_state.active_voice` - Current AI tracker
- `voice_context` - AI handoff information
- `moments[]` - Breakthrough insights array

---

## Pre-Migration Checklist

- [ ] Backup project (entire directory recommended)
- [ ] Commit current work to git
- [ ] Note current SCF version (`grep scf_version buildstate.json`)
- [ ] Verify buildstate files exist and are valid JSON
- [ ] Close any open AI sessions

---

## Migration Methods

### Method 1: Automated (Recommended)

```bash
# Single project
python3 /path/to/session-continuity-framework/scf_migrate_v2.py /path/to/project

# Dry run (preview changes)
python3 scf_migrate_v2.py /path/to/project --dry-run

# Multiple projects
python3 scf_migrate_v2.py --all --backup
```

**What it does:**
1. Creates timestamped backup
2. Creates `.scf/` directory structure
3. Moves and renames files
4. Updates `_session_state` with hub reference
5. Creates `AGENTS.md` symlink
6. Updates `.gitignore` if needed

---

### Method 2: Manual Migration

**Step 1: Create Directory Structure**
```bash
cd /path/to/project
mkdir -p .scf/archives .scf/sessions .scf/voices
```

**Step 2: Move and Rename Files**
```bash
# Move main files (rename to uppercase)
mv buildstate.json .scf/BUILDSTATE.json
mv buildstate.md .scf/BUILDSTATE.md

# Move backups to archives
for f in buildstate.json.backup*; do
  timestamp=$(date -r "$f" +%Y%m%d_%H%M%S)
  mv "$f" ".scf/archives/BUILDSTATE_${timestamp}.json"
done
```

**Step 3: Update BUILDSTATE.json**
```bash
# Add scf_hub reference
python3 << 'PYEOF'
import json
with open('.scf/BUILDSTATE.json', 'r') as f:
    data = json.load(f)
data['_session_state']['scf_hub'] = '/home/mario/projects/session-continuity-framework'
data['_session_state']['active_voice'] = None
if 'voice_context' not in data:
    data['voice_context'] = {"last_ai": None, "ai_handoff_notes": []}
with open('.scf/BUILDSTATE.json', 'w') as f:
    json.dump(data, f, indent=2)
print("✅ Updated BUILDSTATE.json")
PYEOF
```

**Step 4: Create AGENTS.md Symlink**
```bash
# Linux/Mac
ln -s .scf/BUILDSTATE.md AGENTS.md

# Windows (PowerShell as Admin)
New-Item -ItemType SymbolicLink -Path "AGENTS.md" -Target ".scf\BUILDSTATE.md"
```

**Step 5: Update .gitignore (Optional)**
```bash
# If you want to ignore session/voice data
echo ".scf/sessions/" >> .gitignore
echo ".scf/voices/" >> .gitignore
```

---

## Verification

### Check Migration Success
```bash
# Verify structure
ls -la .scf/

# Expected output:
# .scf/
# ├── BUILDSTATE.json
# ├── BUILDSTATE.md
# ├── archives/
# ├── sessions/
# └── voices/

# Verify symlink
ls -l AGENTS.md
# Expected: AGENTS.md -> .scf/BUILDSTATE.md

# Verify hub reference
grep scf_hub .scf/BUILDSTATE.json
# Expected: "scf_hub": "/home/mario/projects/session-continuity-framework"
```

### Test with SCF Tools
```bash
# Load project (should detect v2)
python3 /path/to/scf/scf_load_project.py .

# Check status
python3 -c "import json; print('V2 ✅' if '.scf/BUILDSTATE.json' in str(json.loads(open('.scf/BUILDSTATE.json').read())) else 'V1')"
```

---

## Common Issues & Solutions

### Issue: Symlink not working on Windows
**Solution:**
```powershell
# Run PowerShell as Administrator
New-Item -ItemType SymbolicLink -Path "AGENTS.md" -Target ".scf\BUILDSTATE.md"

# Alternative: Hard link
New-Item -ItemType HardLink -Path "AGENTS.md" -Target ".scf\BUILDSTATE.md"

# Last resort: Copy file (not recommended - creates duplication)
Copy-Item .scf\BUILDSTATE.md AGENTS.md
```

### Issue: JSON syntax error after migration
**Solution:**
```bash
# Validate JSON
python3 -m json.tool .scf/BUILDSTATE.json > /dev/null
# If error, restore from backup and retry
```

### Issue: Old files still in root
**Solution:**
```bash
# Verify migration completed
ls buildstate.json 2>/dev/null && echo "❌ Old files still present" || echo "✅ Clean"

# If old files exist, remove after verifying .scf/ has them
rm buildstate.json buildstate.md buildstate.json.backup*
```

### Issue: Git tracking issues
**Solution:**
```bash
# Stage new structure
git add .scf/
git add AGENTS.md

# Remove old tracking
git rm --cached buildstate.json buildstate.md

# Commit migration
git commit -m "Migrate to SCF v2.0 (.scf/ structure)"
```

---

## Rollback Procedure

If migration fails or you want to revert:

### Automated Rollback
```bash
python3 scf_migrate_v2.py /path/to/project --rollback
```

### Manual Rollback
```bash
# Restore from backup
cp .scf/archives/BUILDSTATE_*.json buildstate.json
cp .scf/archives/BUILDSTATE_*.md buildstate.md

# Remove .scf/ directory
rm -rf .scf/

# Remove symlink
rm AGENTS.md

# Create standalone AGENTS.md if needed
cp buildstate.md AGENTS.md
```

---

## .gitignore Strategies

### Strategy 1: Commit Everything (Recommended)
```gitignore
# No .scf/ ignore - full context in version control
```

**Pros:** Full team collaboration, complete context  
**Cons:** Slightly larger repo

### Strategy 2: Ignore Ephemeral Data
```gitignore
# Commit buildstate, ignore sessions/voices
.scf/sessions/
.scf/voices/
```

**Pros:** Core context shared, personal data private  
**Cons:** Voice profiles not shared across team

### Strategy 3: Ignore Everything (Not Recommended)
```gitignore
# Ignore all SCF files
.scf/
AGENTS.md
```

**Pros:** Clean repo  
**Cons:** ❌ Defeats SCF purpose

---

## Project Type-Specific Guidance

### Node.js Projects
```bash
# Update package.json scripts if needed
# No changes typically required
```

### Python Projects
```bash
# Add to .gitignore if not tracking
echo ".scf/sessions/" >> .gitignore
echo ".scf/voices/" >> .gitignore
```

### Monorepos
```bash
# Each package gets own .scf/
project/
├── packages/
│   ├── app1/
│   │   └── .scf/
│   └── app2/
│       └── .scf/
```

### Docker Projects
```Dockerfile
# Add to .dockerignore
.scf/sessions/
.scf/voices/
.scf/archives/
```

---

## Batch Migration

### Migrate All Discovered Projects
```bash
# Find all SCF projects
python3 buildstate_hunter_learner.py --ecosystem-wide --list-only > projects.txt

# Migrate each
while read project; do
  echo "Migrating: $project"
  python3 scf_migrate_v2.py "$project"
done < projects.txt
```

### Migrate by Directory
```bash
# Migrate all in ~/projects
find ~/projects -name "buildstate.json" -exec dirname {} \; | while read dir; do
  python3 scf_migrate_v2.py "$dir"
done
```

---

## Post-Migration Tasks

- [ ] Test project loads in AI tools
- [ ] Verify symlink works
- [ ] Update team documentation
- [ ] Notify team of migration
- [ ] Update CI/CD if referencing old paths
- [ ] Run `scf_status` to verify health

---

## Backward Compatibility

### V1 Tools Still Work
SCF v2 tools detect v1 projects automatically:
```python
# Auto-detection in all tools
def load_buildstate(project_path):
    if os.path.exists(f"{project_path}/.scf/BUILDSTATE.json"):
        return load_v2(project_path)
    elif os.path.exists(f"{project_path}/buildstate.json"):
        print("⚠️  V1 detected. Migrate: python3 scf_migrate_v2.py .")
        return load_v1(project_path)
```

### Support Timeline
- **Now - May 2026:** Full v1 + v2 support
- **May 2026:** V1 deprecated (still works, warnings)
- **Nov 2026:** V1 support removed

---

## FAQ

**Q: Will this break my project?**  
A: No. Migration is safe, reversible, and creates backups.

**Q: Do I need to migrate immediately?**  
A: No. V1 supported until May 2026. Migrate at your convenience.

**Q: Can I migrate one project at a time?**  
A: Yes. V1 and V2 projects coexist peacefully.

**Q: What if migration fails?**  
A: Automatic backup created. Rollback with `--rollback` flag.

**Q: Will my team see changes?**  
A: Yes, if `.scf/` committed to git. Coordinate with team.

**Q: What about GitHub Copilot integration?**  
A: Works automatically. Copilot reads symlinked AGENTS.md.

**Q: Can I keep old files?**  
A: Not recommended. Clean up after verifying migration.

---

## Migration Script Source

**Location:** `/path/to/session-continuity-framework/scf_migrate_v2.py`

**Usage:**
```bash
python3 scf_migrate_v2.py [project-path] [options]

Options:
  --dry-run          Preview changes without applying
  --backup           Create timestamped backup
  --rollback         Revert to v1 structure
  --force            Skip confirmation prompts
  --all              Migrate all discovered projects
```

---

## Support

**Issues?** Report at: https://github.com/mariov96/session-continuity-framework/issues

**Questions?** See:
- docs/SCF_V2_VISION.md
- docs/SCF_FOLDER_STRUCTURE.md
- docs/SCF_V2_OVERNIGHT_PLAN.md

---

*Document Status: Production Ready*  
*Last Updated: 2025-11-20*  
*Migration tested: ✅ Safe for production use*
