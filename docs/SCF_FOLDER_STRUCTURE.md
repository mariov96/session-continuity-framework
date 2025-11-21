# SCF .scf/ Folder Structure Specification

**Version:** 2.0  
**Status:** Canonical Standard  
**Created:** November 19, 2025

---

## Overview

The `.scf/` directory is the standardized location for all Session Continuity Framework files within a project. This specification defines the canonical structure, file purposes, and migration path from v1.

**Design Goals:**
- Clean project root (single `.scf/` folder)
- Clear ownership (SCF owns `.scf/`)
- Infinite scalability (add features without cluttering root)
- Professional appearance (matches `.git/`, `.github/`, `.vscode/`)
- Easy .gitignore management

---

## Complete Directory Structure

```
project-root/
├── .scf/                           # SCF directory (v2.0 standard)
│   │
│   ├── BUILDSTATE.json             # Technical specifications
│   ├── BUILDSTATE.md               # Strategic narrative
│   │
│   ├── archives/                   # Timestamped backups
│   │   ├── BUILDSTATE_20251119_230422.json
│   │   ├── BUILDSTATE_20251119_230422.md
│   │   ├── BUILDSTATE_20251118_153012.json
│   │   └── BUILDSTATE_20251118_153012.md
│   │
│   ├── sessions/                   # Session state tracking
│   │   ├── current.json            # Current session state
│   │   └── history.json            # Session history log
│   │
│   ├── voices/                     # AI personality profiles
│   │   ├── claude-sonnet-4.5.json
│   │   ├── github-copilot.json
│   │   ├── gpt-4.json
│   │   └── cursor-ai.json
│   │
│   └── .gitkeep                    # Ensures directory tracked in git
│
├── AGENTS.md -> .scf/BUILDSTATE.md # Symlink for ecosystem compatibility
│
└── .gitignore                      # Optional: ignore .scf/ or commit it
```

---

## File Specifications

### BUILDSTATE.json

**Purpose:** Technical specifications, structured data, AI rules

**Location:** `.scf/BUILDSTATE.json`

**Required Fields:**
```json
{
  "project_metadata": {
    "name": "project-name",
    "version": "0.1.0",
    "inception_date": "YYYY-MM-DD",
    "scf_version": "2.0"
  },
  
  "idea": {
    "problem": "What pain point does this solve?",
    "vision": "What are we building?",
    "for_who": "Target users"
  },
  
  "tech_stack": {
    "language": "primary language",
    "framework": "main framework",
    "dependencies": []
  },
  
  "features": {
    "implemented": [],
    "in_progress": [],
    "planned": []
  },
  
  "decisions": [],
  
  "next_steps": [],
  
  "stage": "ideation|development|production",
  
  "_session_state": {
    "session_count": 0,
    "last_updated": "ISO-timestamp",
    "last_modified_by": "ai-name",
    "scf_hub": "/path/to/session-continuity-framework"
  }
}
```

**V2.0 Additions:**
- `_session_state.scf_hub` - Reference to hub location
- `_session_state.last_modified_by` - Track which AI modified
- Voice profile references in decisions
- Moment tagging fields

---

### BUILDSTATE.md

**Purpose:** Strategic narrative, user stories, contextual explanations

**Location:** `.scf/BUILDSTATE.md`

**Required Sections:**
```markdown
# Project Name

**Stage:** [ideation|development|production]
**Last Updated:** [date]
**SCF Version:** 2.0

---

## The Problem

[User pain point or opportunity]

## The Vision

[What we're building and why it matters]

## For Who

[Target users/audience]

---

## Features

### Implemented
- Feature 1: Description

### In Progress
- Feature 2: Description

### Planned
- Feature 3: Description

---

## Key Decisions

- **[Decision]**: Rationale (date)

---

## Next Steps

1. Action item 1
2. Action item 2

---

## Project Context

[Strategic thinking, architectural philosophy, team conventions]

---

*Hub: /path/to/session-continuity-framework*
*Continue by loading these files in any SCF-aware AI tool*
```

---

### archives/

**Purpose:** Timestamped backups of BUILDSTATE files

**Location:** `.scf/archives/`

**Naming Convention:**
```
BUILDSTATE_YYYYMMDD_HHMMSS.json
BUILDSTATE_YYYYMMDD_HHMMSS.md
```

**Automatic Creation:**
- Before any modification to BUILDSTATE files
- Timestamp format: `20251119_230422` (UTC)
- Both JSON and MD backed up together

**Retention Policy:**
- Keep all archives (disk is cheap, context is precious)
- Optional: compress archives older than 30 days
- Never auto-delete (user decision only)

**Example:**
```
archives/
├── BUILDSTATE_20251119_230422.json
├── BUILDSTATE_20251119_230422.md
├── BUILDSTATE_20251118_153012.json
├── BUILDSTATE_20251118_153012.md
├── BUILDSTATE_20251117_094533.json
└── BUILDSTATE_20251117_094533.md
```

---

### sessions/

**Purpose:** Track AI session state and history

**Location:** `.scf/sessions/`

#### current.json

**Purpose:** Current session state

**Structure:**
```json
{
  "session_id": "uuid-v4",
  "ai_name": "claude-sonnet-4.5",
  "ai_version": "2025-11-19",
  "started_at": "2025-11-19T23:00:00Z",
  "last_activity": "2025-11-19T23:45:00Z",
  "status": "active|paused|completed",
  
  "context": {
    "last_task": "Implementing user authentication",
    "current_focus": "Password hashing and session management",
    "files_modified": ["src/auth.ts", "src/session.ts"],
    "decisions_made": 3,
    "moments_created": 1
  },
  
  "conversation_summary": "Working on secure authentication with bcrypt and JWT tokens",
  
  "pending_actions": [
    "Write tests for auth endpoints",
    "Update documentation"
  ]
}
```

#### history.json

**Purpose:** Log of all past sessions

**Structure:**
```json
{
  "sessions": [
    {
      "session_id": "uuid-v4",
      "ai_name": "claude-sonnet-4.5",
      "started_at": "2025-11-19T23:00:00Z",
      "ended_at": "2025-11-19T23:45:00Z",
      "duration_minutes": 45,
      "decisions_made": 3,
      "moments_created": 1,
      "files_modified": 5,
      "summary": "Implemented authentication system with JWT"
    }
  ],
  
  "stats": {
    "total_sessions": 12,
    "total_duration_hours": 18.5,
    "ai_usage": {
      "claude-sonnet-4.5": 8,
      "github-copilot": 4
    },
    "most_productive_ai": "claude-sonnet-4.5",
    "avg_session_minutes": 92
  }
}
```

---

### voices/

**Purpose:** AI personality profiles and behavioral patterns

**Location:** `.scf/voices/`

**File Naming:** `[ai-name].json`

**Structure:** See SCF_VOICE_PROFILES.md for complete schema

**Example Files:**
```
voices/
├── claude-sonnet-4.5.json
├── github-copilot.json
├── gpt-4.json
└── cursor-ai.json
```

**Each File Contains:**
- Communication style (verbosity, explanation depth)
- Decision patterns (architecture preferences, testing approach)
- Technical strengths
- Typical workflow
- Moments created
- Notable contributions

---

## AGENTS.md Symlink

**Purpose:** Ecosystem compatibility (Aider, Cursor, Zed, etc.)

**Location:** `project-root/AGENTS.md` (symlink to `.scf/BUILDSTATE.md`)

**Creation:**
```bash
ln -s .scf/BUILDSTATE.md AGENTS.md
```

**Rationale:**
- Many AI tools expect `AGENTS.md` in project root
- Symlink avoids duplication
- Single source of truth (`.scf/BUILDSTATE.md`)
- Updates to either file reflect immediately

**Windows Support:**
```powershell
# PowerShell
New-Item -ItemType SymbolicLink -Path "AGENTS.md" -Target ".scf\BUILDSTATE.md"

# CMD
mklink AGENTS.md .scf\BUILDSTATE.md
```

---

## .gitignore Strategies

### Strategy 1: Commit Everything (Recommended)
```gitignore
# No .scf/ ignore - commit all context
```

**Pros:**
- Full context in version control
- Team shares knowledge
- Audit trail preserved
- No context loss

**Cons:**
- Repo slightly larger
- May expose internal thinking

---

### Strategy 2: Ignore Sessions & Voices
```gitignore
# Commit buildstate, ignore ephemeral data
.scf/sessions/
.scf/voices/
```

**Pros:**
- Core context committed
- Personal AI preferences private
- Smaller repo

**Cons:**
- Voice profiles not shared
- Session history lost

---

### Strategy 3: Ignore Everything
```gitignore
# Ignore all SCF files (not recommended)
.scf/
AGENTS.md
```

**Pros:**
- Clean repo (no SCF files)

**Cons:**
- ❌ Defeats purpose of SCF
- ❌ No context sharing
- ❌ Not recommended

---

## Migration from V1

### V1 Structure (Root-based)
```
project-root/
├── buildstate.json
├── buildstate.md
├── AGENTS.md
└── buildstate.json.backup
```

### Migration Process

**Automated Migration:**
```bash
python3 scf_migrate_v2.py /path/to/project
```

**Manual Migration:**
```bash
# 1. Create .scf/ directory
mkdir -p .scf/archives .scf/sessions .scf/voices

# 2. Move buildstate files (rename to uppercase)
mv buildstate.json .scf/BUILDSTATE.json
mv buildstate.md .scf/BUILDSTATE.md

# 3. Move backups to archives (rename to new format)
mv buildstate.json.backup .scf/archives/BUILDSTATE_20251119_000000.json
mv buildstate.md.backup .scf/archives/BUILDSTATE_20251119_000000.md

# 4. Create AGENTS.md symlink
ln -s .scf/BUILDSTATE.md AGENTS.md

# 5. Update _session_state in BUILDSTATE.json
# Add: "scf_hub": "/home/mario/projects/session-continuity-framework"

# 6. Update .gitignore if needed
echo "# .scf/sessions/" >> .gitignore
```

---

## File Size Guidelines

### BUILDSTATE.json
- **Target:** 5-20 KB
- **Max:** 50 KB
- **If larger:** Move verbose content to BUILDSTATE.md

### BUILDSTATE.md
- **Target:** 5-15 KB
- **Max:** 50 KB
- **If larger:** Consider breaking into separate docs/

### archives/
- **Growth Rate:** ~10-20 KB per backup
- **Typical Size:** 500 KB - 5 MB over project lifetime
- **Cleanup:** Only if exceeds 100 MB

### voices/
- **Per File:** 2-5 KB
- **Total:** 10-20 KB (typically 3-5 AI profiles)

---

## Best Practices

### 1. Keep BUILDSTATE Files Lean
- JSON: Technical specs only
- MD: Strategic context only
- Don't duplicate information
- Use references, not repetition

### 2. Archive Regularly
- Backup before major changes
- Use meaningful timestamps
- Don't delete archives manually

### 3. Update Session State
- Mark session_count on each session
- Update last_modified_by
- Keep conversation_summary current

### 4. Track Voice Profiles
- Update after each significant session
- Note decision patterns
- Document AI strengths/weaknesses

### 5. Maintain Symlink
- Always create AGENTS.md symlink
- Test symlink after git operations
- Re-create if broken

---

## Tools Support

### init_scf.py
Creates complete `.scf/` structure automatically

### update_scf.py
Updates existing projects (v1 or v2) to latest standards

### scf_migrate_v2.py
Migrates v1 (root-based) to v2 (.scf/-based)

### buildstate_hunter_learner.py
Discovers .scf/ directories across ecosystem

### scf_load_project.py
Loads buildstate from `.scf/` location

---

## FAQ

**Q: Why .scf/ instead of scf/?**  
A: Matches convention (.git/, .github/, .vscode/). Hidden directory signals "framework/tool", not project code.

**Q: Should I commit .scf/ to git?**  
A: Yes, recommended. Commit BUILDSTATE files and archives. Optionally ignore sessions/ and voices/ if too personal.

**Q: Why BUILDSTATE.json not buildstate.json?**  
A: Uppercase matches markdown convention (README.md, LICENSE). High visibility in file lists.

**Q: Can I use v1 and v2 simultaneously?**  
A: No. Choose one. Use scf_migrate_v2.py to migrate v1→v2.

**Q: What if AGENTS.md symlink breaks?**  
A: Re-create: `ln -s .scf/BUILDSTATE.md AGENTS.md`

**Q: How do I backup .scf/ separately?**  
A: `tar -czf scf-backup-$(date +%Y%m%d).tar.gz .scf/`

**Q: Can I nest .scf/ in subdirectories?**  
A: No. Always at project root. One .scf/ per project.

---

## Version History

- **2.0** (Nov 2025): Initial .scf/ standard
  - Introduced .scf/ directory structure
  - Added sessions/ and voices/ subdirectories
  - Defined BUILDSTATE.json v2 schema
  - Created migration path from v1

---

*Specification Status: Finalized*  
*Implementation: See init_scf.py and scf_migrate_v2.py*  
*Questions? Consult SCF_V2_VISION.md or SCF_V2_OVERNIGHT_PLAN.md*
