# SCF v2.0 Vision: The MCP of Your Mind

**Status:** Design Document  
**Created:** November 19, 2025  
**Target Release:** Q1 2026

---

## Executive Summary

Session Continuity Framework v2.0 transforms from a single-project context manager into a **universal orchestrator for AI-assisted development**. The hub-and-spoke architecture enables multi-project learning, voice profile tracking, and moment detection—creating an ecosystem where insights from one project automatically benefit all others.

**Core Innovation:** SCF becomes the persistent memory layer that AI assistants access to understand not just *what* you're building, but *how* different AIs approach problems and *which insights* are worth propagating across your entire development ecosystem.

---

## The Problem with AI Context Today

### Current State (Painful)
- **Context Loss:** Network drops, token limits, platform switches = start over
- **Isolated Learning:** Each project reinvents patterns, no cross-pollination
- **AI Amnesia:** Every new session begins from scratch
- **Tool Fragmentation:** Claude, Copilot, GPT, Cursor—each needs re-explanation
- **Pattern Blindness:** Breakthroughs in Project A never reach Project B

### SCF v1 Solution (Good)
- Single-project context persistence
- Dual-file system (JSON + Markdown)
- Change notifications
- GitHub Copilot integration
- Self-aware buildstate

### SCF v2 Solution (Transformational)
- **Multi-project orchestration** - Hub learns from all spokes
- **Voice profiles** - Track how different AIs work
- **Moment detection** - Capture and propagate breakthroughs
- **Conversation bootstrap** - "Eject button" from any chat
- **Ecosystem learning** - Rising tide lifts all boats

---

## Architecture: Hub & Spoke

```
┌─────────────────────────────────────────────────────────────┐
│                    SCF Hub (Central Brain)                   │
│         /home/mario/projects/session-continuity-framework    │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  Templates   │  │  Bootstrap   │  │   Registry   │     │
│  │ BUILDSTATE.* │  │ START_HERE.md│  │ .scf-registry│     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│                                                              │
│  Aggregates: Moments, Voice Profiles, Patterns              │
│  Never Stores: Spoke files, secrets, project code           │
└─────────────────────────────────────────────────────────────┘
                           │
            ┌──────────────┼──────────────┐
            │              │              │
            ▼              ▼              ▼
    ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
    │   Spoke 1    │ │   Spoke 2    │ │   Spoke 3    │
    │ napkin-hero  │ │ scf-web-app  │ │ test-project │
    │              │ │              │ │              │
    │ .scf/        │ │ .scf/        │ │ .scf/        │
    │  BUILDSTATE.*│ │  BUILDSTATE.*│ │  BUILDSTATE.*│
    │  voices/     │ │  voices/     │ │  voices/     │
    │  sessions/   │ │  sessions/   │ │  sessions/   │
    └──────────────┘ └──────────────┘ └──────────────┘
```

### Hub Responsibilities
1. **Template Source** - Canonical BUILDSTATE structures
2. **Bootstrap Provider** - START_HERE.md for conversation ejection
3. **Discovery Engine** - Find spokes via buildstate_hunter_learner.py
4. **Learning Aggregator** - Collect moments, voice profiles, patterns
5. **Inheritance Root** - Provide org-standards.json for propagation

### Spoke Responsibilities
1. **Project Context** - Store own BUILDSTATE files in .scf/
2. **Hub Reference** - Point to hub via `_session_state.scf_hub`
3. **Session Tracking** - Log AI sessions and decisions
4. **Voice Profiles** - Track which AIs work on this project
5. **Moment Tagging** - Identify high-impact decisions

---

## Key Innovation: .scf/ Directory Standard

### The Problem with Root-based Files
**V1 Approach:**
```
project/
├── buildstate.json          ← Clutters root
├── buildstate.md            ← Clutters root
├── AGENTS.md                ← Clutters root
├── buildstate.json.backup   ← Even more clutter
└── .github/
```

**Issues:**
- 3+ files in root just for SCF
- Hard to .gitignore selectively
- No clear ownership
- Doesn't scale to new features (voices, sessions, moments)

### The V2 Solution: .scf/ Directory
```
project/
├── .scf/                           ← Single SCF folder
│   ├── BUILDSTATE.json             ← Technical specs
│   ├── BUILDSTATE.md               ← Strategic narrative
│   ├── archives/                   ← Auto-generated backups
│   │   ├── BUILDSTATE_20251119_230422.json
│   │   └── BUILDSTATE_20251119_230422.md
│   ├── sessions/                   ← Session state tracking
│   │   └── current.json
│   └── voices/                     ← AI personality profiles
│       ├── claude-sonnet-4.5.json
│       └── github-copilot.json
├── AGENTS.md -> .scf/BUILDSTATE.md ← Symlink for ecosystem
└── .github/
```

**Benefits:**
- ✅ Clean root (one .scf/ folder)
- ✅ Clear ownership (everything SCF in one place)
- ✅ Easy .gitignore: add `.scf/` and done
- ✅ Scales infinitely (add voices/, sessions/, moments/)
- ✅ Professional appearance (matches .git/, .github/, .vscode/)

---

## Feature: Voice Profiles

### The Insight
**Different AIs have different personalities and strengths.**

- Claude: Deep architectural analysis, comprehensive docs, functional patterns
- Copilot: Pragmatic solutions, quick fixes, idiomatic code
- GPT-4: Creative problem-solving, broad knowledge, conversational
- Cursor: Context-aware suggestions, file-level intelligence

### The Problem
When switching AIs mid-project, you lose this context:
- "Claude already refactored this to use immutable patterns"
- "Copilot prefers explicit error handling here"
- "GPT suggested this creative approach that worked well"

### The Solution: Track Voice Profiles

**Structure:** `.scf/voices/[ai-name].json`

```json
{
  "ai_name": "claude-sonnet-4.5",
  "version": "2025-11-19",
  "sessions": 12,
  "first_session": "2025-11-10T09:00:00Z",
  "last_session": "2025-11-19T23:00:00Z",
  
  "communication_style": {
    "verbosity": "concise",
    "explanation_depth": "detailed-when-asked",
    "emoji_usage": "minimal",
    "code_comments": "extensive",
    "documentation_style": "comprehensive"
  },
  
  "decision_patterns": {
    "architecture_preference": "modular-functional",
    "error_handling": "explicit-verbose",
    "testing_approach": "test-first",
    "refactoring_tendency": "high",
    "dependency_philosophy": "minimal-curated"
  },
  
  "technical_strengths": [
    "Deep architectural analysis",
    "Comprehensive error handling",
    "Clear documentation",
    "Security-conscious design",
    "Performance optimization"
  ],
  
  "typical_workflow": [
    "Analyze requirements thoroughly",
    "Propose multiple approaches",
    "Implement with extensive comments",
    "Write comprehensive tests",
    "Document architectural decisions"
  ],
  
  "moments_created": 5,
  "impact_score_avg": 7.8,
  
  "notable_contributions": [
    {
      "date": "2025-11-15",
      "type": "architectural_decision",
      "description": "Introduced event sourcing pattern",
      "impact": 9
    }
  ]
}
```

### Use Cases

**1. AI Handoff Context**
```
User: "Load napkin-hero project"
Copilot: "I see Claude worked on this last. They implemented 
          event sourcing with immutable state patterns. I'll 
          continue that architectural approach."
```

**2. AI Selection Guidance**
```
User: "Which AI should I use for database optimization?"
Hub: "Based on past projects, Claude excels at database design 
      (avg impact 8.2), while Copilot is better for quick 
      query fixes (faster turnaround)."
```

**3. Learning Across Projects**
```
Hub aggregates: "Claude consistently prefers functional patterns 
                 across all projects. This approach has 8.5/10 
                 success rate. Consider adopting org-wide."
```

**4. Drift Detection**
```
System: "Warning: Claude's recent sessions show increased 
         refactoring tendency (was 'medium', now 'very-high'). 
         This may indicate code quality concerns."
```

---

## Feature: Moment Detection

### The Insight
**Not all decisions are created equal. Some are breakthroughs worth sharing.**

- Architectural pivot that solves a class of problems
- Bug insight that reveals a deeper pattern
- Creative solution that works across domains
- Pattern discovery that deserves propagation

### The Problem
Currently, breakthroughs are lost:
- Project A discovers event sourcing solves state complexity
- Project B reinvents the same solution 2 months later
- No mechanism to propagate learning across ecosystem
- Valuable insights buried in decision logs

### The Solution: Moment Detection

**What Qualifies as a Moment?**

1. **Impact Score 8+** - High-impact architectural decision
2. **Pattern Discovery** - Reusable solution identified
3. **Bug Insight** - Root cause that changes understanding
4. **Innovation** - Novel approach that works
5. **Learning Catalyst** - Something worth teaching others

**Structure:** Tagged in decisions array

```json
{
  "decisions": [
    {
      "decision": "Use event sourcing for state management",
      "rationale": "Enables time-travel debugging, audit trail, and simplified state reasoning",
      "impact": 9,
      "date": "2025-11-19",
      "alternatives": ["Redux", "MobX", "Direct state mutation"],
      
      "is_moment": true,
      "moment_type": "architectural_breakthrough",
      "moment_tags": ["state-management", "event-driven", "audit"],
      "propagate_to_org": true,
      "applicable_to": ["state-heavy applications", "audit-required systems"],
      
      "ai_author": "claude-sonnet-4.5",
      "moment_context": "After struggling with complex state updates and debugging, event sourcing eliminated entire class of bugs"
    }
  ]
}
```

### Hub Aggregation

**Structure:** `.scf-registry/learning-moments.json`

```json
{
  "schema_version": "2.0",
  "last_updated": "2025-11-19T23:00:00Z",
  "total_moments": 42,
  
  "moments": [
    {
      "id": "moment-001",
      "source_project": "/mnt/c/code/napkin-hero",
      "project_name": "Napkin Hero",
      "decision": "Use event sourcing for state management",
      "impact": 9,
      "date": "2025-11-19",
      "ai_author": "claude-sonnet-4.5",
      
      "moment_type": "architectural_breakthrough",
      "tags": ["state-management", "event-driven", "audit"],
      "applicable_to": ["state-heavy apps", "audit-required systems"],
      
      "adopted_by": [
        {
          "project": "/home/mario/projects/finance-tracker",
          "date": "2025-11-20",
          "result": "Reduced state bugs by 80%"
        }
      ],
      
      "propagation_score": 8.5,
      "ecosystem_impact": "high"
    }
  ],
  
  "moment_stats": {
    "by_type": {
      "architectural_breakthrough": 12,
      "pattern_discovery": 15,
      "bug_insight": 8,
      "innovation": 7
    },
    "by_ai": {
      "claude-sonnet-4.5": 22,
      "github-copilot": 15,
      "gpt-4": 5
    },
    "avg_impact": 8.2,
    "adoption_rate": 0.65
  }
}
```

### Workflow

**1. Spoke: Moment Creation**
```bash
# AI makes high-impact decision
Decision: Use event sourcing
Impact: 9
→ Auto-tagged as moment (impact 8+)
→ Saved to .scf/BUILDSTATE.json
```

**2. Hub: Discovery**
```bash
python3 buildstate_hunter_learner.py --discover-moments
→ Scans all spokes
→ Finds decisions with is_moment=true
→ Aggregates to .scf-registry/learning-moments.json
```

**3. Hub: Propagation**
```bash
python3 buildstate_hunter_learner.py --update-libraries --propagate-moments
→ Adds moment to ~/scf-library/org-standards.json
→ Makes available to all spokes via inheritance
```

**4. Other Spokes: Adoption**
```bash
# New project initializes
python3 init_scf.py /new-project
→ Inherits org-standards.json
→ Sees: "Consider event sourcing for state-heavy apps (9/10 impact)"
→ AI suggests pattern automatically
```

**5. Hub: Track Impact**
```bash
# Spoke adopts moment
Project: finance-tracker adopts moment-001
Result: "Reduced state bugs by 80%"
→ Hub updates adopted_by[] array
→ Increases propagation_score
→ Validates moment effectiveness
```

---

## Feature: Conversation Bootstrap ("Eject Button")

### The Insight
**The best time to capture context is during the conversation itself.**

### The Problem
- Token limits hit mid-conversation
- Network drops kill session
- Want to switch AI platforms
- Need to capture state before closing

### The Solution: START_HERE.md

**Minimal Command:**
```
Read /home/mario/projects/session-continuity-framework/START_HERE.md 
and initialize this project
```

**What Happens:**
1. AI reads 800-token bootstrap instructions
2. Extracts 5 key things from conversation:
   - Project name/concept
   - Problem statement
   - Features discussed
   - Technical decisions
   - Vision/goal
3. Generates BUILDSTATE.json (structured)
4. Generates BUILDSTATE.md (narrative)
5. Creates .scf/ folder structure
6. Saves files to project root
7. Returns portable context

**Token Budget:**
- START_HERE.md: ~850 tokens
- START_HERE_TINY.md: ~170 tokens (emergency)
- Works even at 95% context capacity

**Use Cases:**

**1. Token Exhaustion**
```
User at 98% context: "Read START_HERE.md and initialize this project"
AI: [Extracts conversation, generates files]
→ Context saved, can continue in new session
```

**2. Platform Switch**
```
Claude conversation hitting limits
→ Eject context to BUILDSTATE files
→ Load files in Copilot
→ Continue seamlessly
```

**3. Idea Capture**
```
Brainstorming session with AI
→ Don't want to lose ideas
→ Eject to .scf/ files
→ Version control your thinking
```

**4. Session Handoff**
```
Claude: "I've implemented the auth system"
→ User ejects context
→ Tomorrow: Copilot reads files
→ Copilot: "I see Claude implemented auth. I'll continue with the dashboard."
```

---

## Migration Strategy: V1 → V2

### Backward Compatibility Approach

**Goal:** Zero Breaking Changes for V1 Users

**Strategy:**
1. **Dual Support Period** - 6 months (Nov 2025 - May 2026)
2. **V1 Detection** - Auto-detect root-based files
3. **V2 Default** - New projects use .scf/ by default
4. **Migration Tool** - Automated v1→v2 migration
5. **Deprecation Warnings** - Gentle nudges to upgrade

### Detection Logic

```python
def detect_scf_version(project_path):
    """Detect which SCF version project uses"""
    
    # Check for v2 structure
    if os.path.exists(f"{project_path}/.scf/BUILDSTATE.json"):
        return "v2"
    
    # Check for v1 structure
    if os.path.exists(f"{project_path}/buildstate.json"):
        return "v1"
    
    # No SCF detected
    return None

def load_buildstate(project_path):
    """Load buildstate regardless of version"""
    version = detect_scf_version(project_path)
    
    if version == "v2":
        return load_v2_buildstate(f"{project_path}/.scf/BUILDSTATE.json")
    elif version == "v1":
        print("⚠️  V1 detected. Consider migrating: python3 scf_migrate_v2.py")
        return load_v1_buildstate(f"{project_path}/buildstate.json")
    else:
        raise FileNotFoundError("No SCF buildstate found")
```

### Migration Tool: scf_migrate_v2.py

```bash
# Migrate single project
python3 scf_migrate_v2.py /path/to/project

# Preview changes (dry run)
python3 scf_migrate_v2.py /path/to/project --dry-run

# Migrate all discovered projects
python3 scf_migrate_v2.py --all --backup
```

**What It Does:**
1. Create `.scf/` directory structure
2. Move `buildstate.json` → `.scf/BUILDSTATE.json`
3. Move `buildstate.md` → `.scf/BUILDSTATE.md`
4. Move backups → `.scf/archives/`
5. Add `scf_hub` reference to `_session_state`
6. Create `AGENTS.md` symlink
7. Update `.gitignore` if needed
8. Create timestamped backup of v1 structure

---

## Technical Specifications

### File Naming Convention
**Decision:** UPPERCASE (BUILDSTATE.json, BUILDSTATE.md)

**Rationale:**
- Matches markdown convention (README.md, LICENSE, CONTRIBUTING.md)
- High visibility in file lists
- Distinguishes from regular code files
- Signals "framework file" status

**Exceptions:**
- Hub registry: lowercase (.scf-registry/ for hidden directory)
- Spoke subdirectories: lowercase (.scf/voices/, .scf/sessions/)

### Hub Registry Structure

```
.scf-registry/
├── schema.json                  # Registry schema definition
├── spoke-projects.json          # Discovered project paths
├── learning-moments.json        # Aggregated breakthrough insights
├── voice-profiles.json          # Aggregated AI behavior patterns
└── stats.json                   # Ecosystem health metrics
```

### Spoke Structure

```
.scf/
├── BUILDSTATE.json              # Technical specifications
├── BUILDSTATE.md                # Strategic narrative
├── archives/                    # Timestamped backups
│   ├── BUILDSTATE_20251119_230422.json
│   └── BUILDSTATE_20251119_230422.md
├── sessions/                    # Session tracking
│   ├── current.json             # Current session state
│   └── history.json             # Session log
└── voices/                      # AI personality profiles
    ├── claude-sonnet-4.5.json
    ├── github-copilot.json
    └── gpt-4.json
```

---

## Success Metrics

### Hub Metrics
- **Spoke Count:** # of discovered projects
- **Moment Count:** # of breakthrough insights captured
- **Voice Diversity:** # of different AIs tracked
- **Adoption Rate:** % of moments adopted across projects
- **Ecosystem Health:** Average balance score, moment density

### Spoke Metrics
- **Balance Score:** 0.0-1.0 (content optimization)
- **Session Count:** # of AI sessions
- **Moment Density:** Moments per 100 decisions
- **Voice Diversity:** # of AIs used on project
- **Hub Connectivity:** Last sync with hub

### User Metrics
- **Context Survival:** % of sessions resumed successfully
- **Platform Switches:** # of seamless AI transitions
- **Bootstrap Usage:** # of conversation ejections
- **Cross-Project Learning:** # of moments adopted

---

## Future Vision (v2.x and Beyond)

### V2.1: Enhanced Enforcement
- Pre-commit hooks for buildstate validation
- CI/CD integration
- Automated balance monitoring
- Real-time compliance dashboard

### V2.2: AI Recommendations
- "Which AI should I use for this task?"
- Voice profile analysis
- Strength-based routing
- Collaboration suggestions

### V2.3: Visual Dashboard
- Web UI for hub registry
- Project relationship graphs
- Moment propagation visualization
- Voice profile comparisons

### V2.4: Real-time Sync
- Live moment notifications
- Cross-project alerts
- Ecosystem-wide broadcasts
- Collaborative learning loops

### V3.0: The Network Effect
- Public hub for community learning
- Privacy-preserving aggregation
- Anonymous moment sharing
- Global pattern library

---

## Conclusion

SCF v2.0 transforms from a project-level tool into an **ecosystem orchestrator**. The hub-and-spoke architecture, combined with voice profiles and moment detection, creates a persistent memory layer that makes AI assistants truly intelligent collaborators.

**The Vision:**
- Your projects learn from each other
- Your AIs understand context and history
- Your breakthroughs propagate automatically
- Your development ecosystem gets smarter over time

**The Result:**
- Never lose context again
- Switch AI tools seamlessly
- Benefit from your own past insights
- Build a rising tide that lifts all boats

This is SCF v2.0: **The MCP of Your Mind** 🧠

---

*Document Status: Complete*  
*Next Steps: Review, approve, implement*  
*Questions? See SCF_V2_OVERNIGHT_PLAN.md for detailed roadmap*
