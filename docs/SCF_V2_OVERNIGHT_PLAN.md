# SCF v2.0 Overnight Planning Session
**Created:** November 19, 2025  
**Status:** Awaiting Approval  
**Target:** Complete planning, ready for implementation approval

---

## 🎯 Vision: SCF as Universal Context Orchestrator

**"The MCP of Your Mind"** - Hub-and-spoke architecture enabling:
- Multi-project learning ("rising tide lifts all boats")
- Conversation bootstrapping ("eject button")
- Voice profile tracking (Claude vs Copilot vs GPT behaviors)
- Moment detection (capture breakthrough decisions)
- Lightweight entry (minimal token consumption)

---

## 📁 Core Change: .scf/ Directory Standard

### V1 (Current - Root-based)
```
project/
├── buildstate.json
├── buildstate.md
├── AGENTS.md
└── .github/
    └── copilot-instructions.md
```

### V2 (New - .scf/-based)
```
project/
├── .scf/
│   ├── BUILDSTATE.json          # Technical specs
│   ├── BUILDSTATE.md            # Strategic narrative
│   ├── archives/                # Timestamped backups
│   │   └── BUILDSTATE_20251119_230422.json
│   ├── sessions/                # Session state tracking
│   │   └── current.json
│   └── voices/                  # AI personality profiles
│       ├── claude.json
│       └── copilot.json
├── AGENTS.md -> .scf/BUILDSTATE.md  # Symlink for ecosystem
└── .github/
    └── copilot-instructions.md
```

**Rationale:**
- ✅ Clean project root (one .scf/ folder vs scattered files)
- ✅ Clear ownership (SCF lives in .scf/)
- ✅ Easy .gitignore management
- ✅ Scales to new features (voices, sessions, moments)
- ✅ Backward compatible (symlinks for AGENTS.md)

---

## 🏗️ Architecture: Hub & Spoke

### Hub (This Repo)
**Location:** `/home/mario/projects/session-continuity-framework`

**Responsibilities:**
- Store templates (BUILDSTATE.json, BUILDSTATE.md)
- Provide bootstrap entry points (START_HERE.md)
- Track spoke registry (discovered projects)
- Aggregate learnings (moments, patterns, voice profiles)
- **Never duplicate spoke files** (discovery only)

**New Structure:**
```
session-continuity-framework/
├── templates/
│   ├── BUILDSTATE.json
│   └── BUILDSTATE.md
├── START_HERE.md               # Primary bootstrap (~850 tokens)
├── START_HERE_TINY.md          # Emergency bootstrap (~170 tokens)
├── .scf-registry/              # Hub-specific tracking
│   ├── spoke-projects.json     # Discovered project paths
│   ├── learning-moments.json   # Significant insights
│   └── voice-profiles.json     # Aggregated AI behaviors
├── scf_moment_detector.py      # NEW: Identify breakthroughs
├── scf_enforcer.py             # NEW: Validate compliance
└── docs/
    ├── SCF_V2_VISION.md
    ├── SCF_FOLDER_STRUCTURE.md
    ├── SCF_VOICE_PROFILES.md
    ├── MIGRATION_V1_TO_V2.md
    └── V2_RELEASE_CHECKLIST.md
```

### Spoke (Individual Projects)
**Location:** Any project directory (e.g., `/mnt/c/code/napkin-hero/`)

**Responsibilities:**
- Store project-specific context in `.scf/`
- Reference hub in `_session_state.scf_hub`
- Track own sessions, voices, moments
- Inherit patterns from hub via inheritance chain

**Files:**
```
project/.scf/
├── BUILDSTATE.json             # Project specs
├── BUILDSTATE.md               # Project narrative
├── archives/                   # Backups
├── sessions/                   # Session tracking
└── voices/                     # AI profiles for this project
```

---

## 🎭 New Feature: Voice Profiles

**Purpose:** Capture how different AIs approach the same project

### Structure: `.scf/voices/[ai-name].json`
```json
{
  "ai_name": "claude-sonnet-4.5",
  "sessions": 12,
  "first_session": "2025-11-10",
  "last_session": "2025-11-19",
  "communication_style": {
    "verbosity": "concise",
    "explanation_depth": "detailed-when-asked",
    "emoji_usage": "rare",
    "code_comments": "extensive"
  },
  "decision_patterns": {
    "architecture_preference": "modular-functional",
    "error_handling": "explicit-verbose",
    "testing_approach": "test-first",
    "refactoring_tendency": "high"
  },
  "strengths": [
    "Deep architectural analysis",
    "Comprehensive error handling",
    "Clear documentation"
  ],
  "moments_created": 5,
  "impact_score_avg": 7.8
}
```

**Use Cases:**
- Understand which AI is best for which task
- Handoff context: "Claude prefers functional patterns, Copilot is pragmatic"
- Learn from AI diversity (aggregate hub wisdom)
- Detect AI drift (has Claude's approach changed?)

---

## ⚡ New Feature: Moment Detection

**Purpose:** Identify and propagate breakthrough insights across ecosystem

### What is a Moment?
- **Breakthrough Decision:** Impact score 8+ (architectural pivot, major insight)
- **Pattern Discovery:** Reusable solution identified
- **Bug Insight:** Root cause revelation that changes approach
- **Learning Catalyst:** Something worth sharing across projects

### Structure: Tagged in Decisions
```json
{
  "decisions": [
    {
      "decision": "Use event sourcing for state management",
      "rationale": "Enables time-travel debugging and audit trail",
      "impact": 9,
      "date": "2025-11-19",
      "is_moment": true,
      "moment_type": "architectural_breakthrough",
      "propagate_to_org": true
    }
  ]
}
```

### Hub Aggregation: `.scf-registry/learning-moments.json`
```json
{
  "moments": [
    {
      "id": "moment-001",
      "source_project": "/mnt/c/code/napkin-hero",
      "decision": "Use event sourcing for state management",
      "impact": 9,
      "date": "2025-11-19",
      "ai_author": "claude-sonnet-4.5",
      "applicable_to": ["state-heavy apps", "audit-required systems"],
      "adopted_by": ["/home/mario/projects/finance-tracker"]
    }
  ]
}
```

**Workflow:**
1. Spoke: High-impact decision made → tagged as moment
2. Hub: `buildstate_hunter_learner.py --discover-moments`
3. Hub: Aggregate to learning-moments.json
4. Other spokes: Inherit via org-standards.json
5. Ecosystem benefits: "Rising tide lifts all boats"

---

## 📋 Implementation Phases

### Phase 0: Bootstrap System ✅ (COMPLETE)
- [x] START_HERE.md created (~850 tokens)
- [x] START_HERE_TINY.md created (~170 tokens)
- [x] Templates renamed to BUILDSTATE.json/md
- [x] README.md updated with bootstrap section

**Status:** Ready to test with real project

---

### Phase 1: Core Structure (Week 1)
**Goal:** Establish .scf/ standard and migration path

#### Tasks:
1. **Document .scf/ Standard**
   - File: `docs/SCF_FOLDER_STRUCTURE.md`
   - Content: Directory layout, file purposes, rationale
   - Deliverable: Clear spec for all future implementations

2. **Update init_scf.py**
   - Create `.scf/` directory structure
   - Generate files in `.scf/` location
   - Add `scf_hub` reference to `_session_state`
   - Create `AGENTS.md` symlink in root
   - Support both v1 (root) and v2 (.scf/) detection

3. **Update update_scf.py**
   - Detect v1 vs v2 format
   - Migrate v1 → v2 (move files, preserve archives)
   - Update references and paths

4. **Create Migration Guide**
   - File: `docs/MIGRATION_V1_TO_V2.md`
   - Manual steps for existing projects
   - Automated migration script: `scf_migrate_v2.py`
   - Backward compatibility strategy

5. **Update Templates**
   - Add `scf_hub` to `_session_state`
   - Add voice profile tracking fields
   - Add moment tagging structure
   - Update documentation strings

**Deliverables:**
- ✅ .scf/ standard documented
- ✅ init_scf.py v2-ready
- ✅ Migration path clear
- ✅ Templates updated
- ✅ Test project migrated (test-scf-app)

---

### Phase 2: Voice Profiles (Week 2)
**Goal:** Capture AI personality and decision patterns

#### Tasks:
1. Design voice profile schema
2. Create scf_voice_tracker.py
3. Update scf_load_project.py for AI detection
4. Hub aggregation to .scf-registry/voice-profiles.json

---

### Phase 3: Moment Detection (Week 3)
**Goal:** Identify and propagate breakthroughs

#### Tasks:
1. Create scf_moment_detector.py
2. Update decision tracking with moment fields
3. Hub moment aggregation
4. Inheritance integration

---

### Phase 4: Enforcement & Quality (Week 4)
**Goal:** Ensure buildstate compliance

#### Tasks:
1. Create scf_enforcer.py
2. Pre-commit hook template
3. CI/CD integration guide
4. Enhanced status dashboard

---

### Phase 5: Documentation & Release (Week 5)
**Goal:** Complete docs and release v2.0

#### Tasks:
1. Update all documentation
2. Create SCF_V2_VISION.md
3. Create V2_RELEASE_CHECKLIST.md
4. Write release notes
5. Update examples

---

## 🚧 Breaking Changes

### File Locations
**V1:** `project/buildstate.json`  
**V2:** `project/.scf/BUILDSTATE.json`

### File Names
**V1:** `buildstate.json` (lowercase)  
**V2:** `BUILDSTATE.json` (uppercase)

### Session State
**V1:** No hub reference  
**V2:** `_session_state.scf_hub` required

---

## 🎬 Next Steps (When You Wake Up)

### Review This Plan
1. Read through vision and architecture
2. Approve/modify .scf/ folder structure
3. Confirm voice profile schema makes sense
4. Validate moment detection criteria
5. Approve phase priorities

### First Approvals Needed
- [ ] Approve .scf/ directory standard
- [ ] Approve voice profile JSON structure
- [ ] Approve moment detection criteria (impact 8+)
- [ ] Approve 5-week timeline
- [ ] Approve breaking changes (file locations, names)

### Then I'll Start
1. Create docs/SCF_V2_VISION.md
2. Create docs/SCF_FOLDER_STRUCTURE.md
3. Update init_scf.py for v2.0
4. Test with fresh project initialization

---

## 💭 Open Questions for Tomorrow

1. **Voice Profile Fields:** Too many? Too few? What else should we track?
2. **Moment Threshold:** Impact 8+ seems right, or should it be 9+?
3. **Hub Privacy:** What spoke data is OK to aggregate vs should stay private?
4. **File Names:** BUILDSTATE.json (caps) or buildstate.json (lowercase)?
5. **Symlinks:** AGENTS.md symlink or separate file?
6. **Migration:** Force v2 or allow v1 indefinitely?

---

*Sleep well! This will be here when you wake up, ready for your review and approval.* 🌙
