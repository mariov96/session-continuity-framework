# Wheelwright Framework (SCF)

**For Humans:** This project uses SCF for AI-assisted development with continuous context across sessions.

**For AI Assistants:** Read the sections below BEFORE making any changes to this project.

---

## 🤖 AI INSTRUCTIONS - READ FIRST

### ⚠️ CONTEXT REFRESH CHECK (Do This First!)

**Every session, check if the `.WAI/` folder has been updated since you last worked here:**

```python
import json
from pathlib import Path

scf_path = Path(".scf")
buildstate = json.loads((scf_path / "WAI-State.json").read_text())
scf_meta = buildstate.get("_scf_metadata", {})

# Check for new hub teachings
hub_version = scf_meta.get("hub_reference", {}).get("current_hash_short", "unknown")
last_teach = scf_meta.get("sync_history", [{}])[-1].get("date", "never") if scf_meta.get("sync_history") else "never"

print(f"Hub version: {hub_version}")
print(f"Last teach sync: {last_teach}")
print(f"Days since sync: {scf_meta.get('development_health', {}).get('days_since_sync', 'unknown')}")
```

**If you see new learnings or policies were added:**
1. Read this entire file again for updated instructions
2. Check `kb-sync.json` for new hub knowledge version
3. Review any new sections in this README (especially "Learnings from Hub")
4. Apply new patterns to your current work

**Why this matters:** The hub may have pushed new best practices, patterns, or policies since your last session. Incorporating these keeps your work aligned with the broader ecosystem.

---

### What is SCF?

You're working on a project using the **Wheelwright Framework**. This means:

1. **Context persists** - You're not starting from scratch. Project history is available.
2. **Multiple AIs collaborate** - Claude, GitHub Copilot, and others may work here. Coordinate!
3. **Your learnings matter** - High-impact insights benefit the entire project ecosystem.
4. **You receive learnings** - This project gets best practices from other successful projects.

### Your Core Files

📄 **WAI-State.json** - Technical specification (YOU UPDATE)
- Features, stack, decisions, bugs, next steps
- Session state tracking (who, when, what changed)
- Deterministic data for AI consumption

📝 **WAI-State.md** - Strategic context (YOU UPDATE)
- Vision, ideation, human-readable rationale
- Why decisions were made
- User stories and success metrics

📡 **wheel-signals.jsonl** - Communication log (YOU APPEND)
- Signal high-impact learnings to hub
- Request hub actions (rebalance, updates)
- Append-only log (don't overwrite!)

📊 **kb-sync.json** - Knowledge tracking (READ ONLY)
- What you've learned from the hub
- Current sync status
- Updated by unified CLI via `WAI sync`

📖 **This file (WAI-Guide.md)** - Your instructions (HUB UPDATES)
- Current SCF policies
- Learnings from other projects
- Project-specific recommendations
- Updated when user runs teach.py

---

## 📋 Current SCF Policies

### Policy: Session State Updates (v2025-11-25)

**ALWAYS update `_session_state` in WAI-State.json when you make changes:**

```json
{
  "_session_state": {
    "last_modified_by": "Claude",
    "last_modified_at": "2025-11-30T18:30:00Z",
    "session_count": 15,
    "requires_review": false,
    "review_reason": null
  }
}
```

**Set `requires_review: true` AND provide `review_reason` if:**
- You're a different AI than `last_modified_by`
- You made architectural changes
- You're unsure about previous context
- You modified core functionality

**Example:**
```json
{
  "requires_review": true,
  "review_reason": "Refactored authentication system - please review security implications"
}
```

**Why this matters:** Helps the next AI (or human) understand what changed and why review is needed.

---

### Policy: High-Impact Learning Sharing (v2025-11-30)

**When you make a decision with impact score ≥ 8, share it with the hub:**

1. Add decision to `decisions` array in WAI-State.json
2. Append offer to wheel-signals.jsonl

**Example code:**
```python
import json
from datetime import datetime, timezone

# 1. Add to decisions in WAI-State.json (do this first)
decision = {
    "date": datetime.now().date().isoformat(),
    "impact": 9,
    "decision": "Centralized error handling with request tracking",
    "rationale": "Consistent error format improves debugging and client integration",
    "context": "Multiple endpoints had different error formats causing client confusion"
}

# 2. Append signal to wheel-signals.jsonl
signal = {
    "timestamp": datetime.now(timezone.utc).isoformat(),
    "by": "Claude",  # Your AI name
    "hub_kb_version": "2025-11-30T00:00:00Z",  # From kb-sync.json
    "spoke_kb_version": "2025-11-30T00:00:00Z",  # From kb-sync.json
    "offers": [{
        "type": "architectural_breakthrough",
        "topic": "Centralized API error handling",
        "impact": 9,
        "location": "WAI-State.json:decisions[12]",
        "context": "Pattern applicable to any REST API project. Improves debugging with request IDs and consistent format."
    }],
    "requests": [],
    "flags": {
        "needs_rebalance": False,
        "has_high_impact_learnings": True
    }
}

# Append to file (don't overwrite!)
with open(".WAI/wheel-signals.jsonl", "a") as f:
    f.write(json.dumps(signal) + "\n")
```

**What to share:**
- ✅ Architectural breakthroughs
- ✅ Patterns that saved significant time
- ✅ Critical bugs avoided
- ✅ Performance optimizations with measurable results
- ✅ Cross-project applicable solutions

**What NOT to share:**
- ❌ Project-specific implementation details
- ❌ Minor refactorings
- ❌ Routine bug fixes
- ❌ Personal preferences without impact justification
- ❌ **Common knowledge** - Things any competent developer knows
- ❌ **Obvious patterns** - Standard practices documented everywhere

**Why:** Your breakthrough might save another project days of work. Quality over quantity!

### 🔍 Stay Observant: Proactive Learning Discovery

**As you work, actively notice insights worth sharing.** Don't wait for explicit "high-impact" moments—valuable learnings often emerge from:

**Patterns Worth Signaling:**
- A non-obvious solution that took multiple attempts to discover
- A debugging approach that revealed a hidden root cause
- An architectural decision that prevented future problems
- A workflow optimization that significantly improved efficiency
- A gotcha or pitfall that others would likely hit

**🔧 IDE & Tooling Configurations (High Value!):**

Configuration files that improve developer experience are **excellent candidates** for spoke-signals because they:
- Transfer to ALL projects using that tool
- Are often discovered through trial and error
- Compound in value across the ecosystem

**Watch for optimizations in:**
- `.vscode/settings.json` - Editor preferences, formatters, linting
- `.vscode/tasks.json` - Build tasks, test runners, automation
- `.vscode/launch.json` - Debug configurations
- `.cursor/`, `.zed/` - Other IDE configurations
- `pyproject.toml`, `tsconfig.json` - Language tooling

**Signal these with type `ide_optimization`:**
```json
{"type": "ide_optimization", "topic": "VS Code task for parallel test watching", "tool": "vscode", "files": ["tasks.json"], "impact": 8, "context": "Runs pytest-watch in background terminal, freeing main terminal for git operations"}
```

**Struggles Worth Signaling:**
- Recurring friction points in a technology or library
- Documentation gaps that caused confusion
- Edge cases that standard approaches miss
- Integration challenges between tools/services

**Use Your Judgment - The Quality Filter:**

Before signaling, ask yourself:
1. **Would this save someone else real time?** (Not just minutes, but hours or days)
2. **Is this transferable?** (Applies beyond this specific project)
3. **Is this non-obvious?** (Not the first thing someone would try)
4. **Did I learn something I didn't expect?** (Genuine insight, not confirmation)

**Example of good judgment:**
- ❌ "Use async/await for API calls" → Too common
- ✅ "Batch API calls with 50ms debounce to avoid rate limits while maintaining UX responsiveness" → Specific, actionable, non-obvious

The ecosystem benefits when you share genuine insights, not volume. **One actionable learning beats ten obvious ones.**

### 🎯 Environment-Aware Optimization (Proactive Application)

**Detect your environment and apply relevant learnings automatically.**

When starting a session, identify the context:
```python
import os
from pathlib import Path

# Detect IDE environment
env_hints = {
    'vscode': Path('.vscode').exists() or os.environ.get('TERM_PROGRAM') == 'vscode',
    'cursor': Path('.cursor').exists() or 'cursor' in os.environ.get('TERM_PROGRAM', '').lower(),
    'zed': Path('.zed').exists(),
    'claude_code': os.environ.get('CLAUDE_CODE') == '1',
}

detected_env = [k for k, v in env_hints.items() if v]
```

**After detecting the environment:**
1. **Check hub learnings** for that tool (e.g., `learnings/ide/vscode.json`)
2. **Compare with current project** - Are recommended configs missing?
3. **Proactively suggest** optimizations the user hasn't applied yet

**Hub Knowledge Base Structure:**
```
learnings/
├── ide/
│   ├── vscode.json      # VS Code optimizations
│   ├── cursor.json      # Cursor-specific configs
│   └── zed.json         # Zed configurations
├── languages/
│   ├── python.json      # Python tooling
│   └── typescript.json  # TS/JS tooling
└── workflows/
    └── testing.json     # Test automation patterns
```

This creates a **flywheel effect**: Every project benefits from optimizations discovered anywhere in the ecosystem.

---

### Policy: Hub Check-In (v2025-11-30)

**Periodically check if hub has new learnings for you:**

```python
import json
from datetime import datetime
from pathlib import Path

# Read sync status
kb_sync = json.loads(Path(".WAI/kb-sync.json").read_text())

# Check if hub has updates
hub_version = datetime.fromisoformat(kb_sync["hub_kb_version"])
spoke_version = datetime.fromisoformat(kb_sync["spoke_kb_version"])
last_sync = datetime.fromisoformat(kb_sync["last_sync_date"])
days_since_sync = (datetime.now() - last_sync).days

if hub_version > spoke_version or days_since_sync > 30:
    print(f"🔄 Hub has new learnings available!")
    print(f"Last sync: {days_since_sync} days ago")
    print(f"Recommendation: Ask user to run:")
    print(f"  python <hub-path>/teach.py --update {Path.cwd()}")
```

**When to check:**
- Starting a major new feature
- Last sync was >30 days ago
- You notice kb-sync shows versions out of sync

**Why:** Stay current with ecosystem learnings and best practices.

---

## 🎯 Hub Developer Profile

The hub knows about the developer you're working with:

**Name:** {{USER_NAME}}
**Work Style:** {{WORK_STYLE}}
**Preferred Languages:** {{LANGUAGES}}
**Coding Patterns:** {{PATTERNS}}

**Use these preferences** when making suggestions, but don't override explicit project requirements.

---

## 💡 Learnings from Hub

### Pattern: [Pattern Name] (impact: X)
**From project:** [source-project]
**Date pushed:** [date]

**Description:**
[What the pattern does]

**Implementation:**
```code
[Example code]
```

**Why this matters:**
[Benefits and use cases]

**Your action:** Review your current approach. If you've solved this differently with good results, add to your decisions and signal back!

---

## 🔧 Project-Specific Status

**SCF Template Version:** {{SCF_VERSION}}
**Hub KB Version:** {{HUB_KB_VERSION}}
**Spoke KB Version:** {{SPOKE_KB_VERSION}}

**Health Status:**
- {{HEALTH_CHECKS}}

**Recommendations:**
- {{RECOMMENDATIONS}}

---

## 📚 Working with Buildstate

### Reading Context

**Start every session by reading:**
1. This file (WAI-Guide.md) - Instructions and learnings
2. WAI-State.md - Project vision and strategic context
3. WAI-State.json - Current technical state
4. wheel-signals.jsonl (last few lines) - Recent activity

**Quick context check:**
```python
import json
from pathlib import Path

# Read session state
buildstate = json.loads(Path("WAI-State.json").read_text())
session = buildstate.get("_session_state", {})

print(f"Last modified by: {session.get('last_modified_by')}")
print(f"At: {session.get('last_modified_at')}")
print(f"Requires review: {session.get('requires_review')}")
if session.get('review_reason'):
    print(f"Reason: {session.get('review_reason')}")
```

### Updating Context

**After making changes:**
1. Update WAI-State.json with your changes
2. Update _session_state (who, when, review status)
3. Add to decisions if impact ≥ 5
4. Append to wheel-signals.jsonl if impact ≥ 8

---

## 🔗 Integration Points

### AGENTS.md Symlink

This project has: `AGENTS.md -> .WAI/WAI-Guide.md`

Tools like Zed, Cursor, and Aider will read this file for agent instructions.

### Git Hooks (Optional)

Consider adding a post-commit hook to update signals:
```bash
# .git/hooks/post-commit
#!/bin/bash
# Remind to update signal after commits
echo "Reminder: Update .WAI/wheel-signals.jsonl if you made high-impact changes"
```

---

## ❓ Need Help?

**For project context:**
- Read WAI-State.md for vision
- Check decisions array for past reasoning
- Review wheel-signals.jsonl for recent activity

**For SCF help:**
- Hub location: {{HUB_PATH}}
- Documentation: {{HUB_PATH}}/docs/
- Issues: https://github.com/wheelwright-ai/framework/issues

---

## 🔧 THIS IS THE FRAMEWORK

**Important:** This project IS the SCF framework itself - the source of all templates and tools.

### What This Repo Provides
- `./scf` - Unified CLI for all SCF operations
- `teach.py` - Initialize and update spoke projects
- `recon.py` - Discover and scan projects
- `templates/spoke/` - Templates for new projects
- `templates/hub/` - Templates for hub creation

### Key Commands (run from this directory)
```bash
./WAI hub create          # Create a personal hub
./WAI hub status          # Check hub health
./WAI hub locate          # Find where hub is

./WAI init <path>         # Add SCF to a project
./WAI init <path> --guided # Guided foundation setup
./WAI sync                # Sync spoke with hub
./WAI sync --all          # Sync all spokes
```

### Connected Components
- **Hub:** ~/wheelwright-hub (user's personal learnings)
- **Spokes:** Individual projects using SCF

### For Contributors
This repo uses SCF to track its own development (dogfooding).
Check `.WAI/WAI-State.json` for current project state.

---

**Last updated by hub:** {{LAST_UPDATED}}
**Via:** teach.py

---

*This file is maintained by the Wheelwright Hub. Local edits may be overwritten when teach.py runs.*

---

## 🔄 Incorporating New Teachings

When you detect that new teachings have been pushed to this project (via the Context Refresh Check above), follow this process:

### 1. Identify What Changed

Compare the current `_scf_metadata.hub_reference.current_hash_short` with what you remember from your last session. If different, new teachings are available.

### 2. Review New Learnings

Check for new content in:
- **This file (WAI-Guide.md)** - Look for new sections, updated policies, or new patterns
- **kb-sync.json** - Check `hub_kb_version` for version changes
- **WAI-State.json** - Look at `_scf_metadata.sync_history` for recent syncs

### 3. Apply to Current Work

For each new learning or policy:
- **Consider relevance** - Does this apply to your current task?
- **Check conflicts** - Does it conflict with existing project decisions?
- **Adopt or adapt** - Either apply directly or note why it doesn't fit this project

### 4. Acknowledge Receipt

Update `_session_state` to indicate you've reviewed new teachings:
```json
{
  "_session_state": {
    "last_modified_by": "Claude",
    "last_modified_at": "ISO-8601-timestamp",
    "context_refreshed": true,
    "hub_version_reviewed": "hash-from-hub-reference"
  }
}
```

### Why This Matters

The SCF ecosystem continuously improves based on learnings from all projects. By incorporating new teachings:
- You benefit from patterns discovered in other projects
- You avoid repeating mistakes already solved elsewhere
- Your work stays aligned with ecosystem best practices
- The user gets consistent quality across all their projects

---

## 🆕 Recent SCF Enhancements (v2025-12-15)

### Unified CLI Interface
- **New command:** `./scf` replaces 25+ separate Python scripts
- **Role-based onboarding:** Clear Hub vs Spoke distinction  
- **Progressive complexity:** UI adapts to user expertise level

### Security Hardening
- **XSS Prevention:** Content Security Policy in webviews
- **Input Validation:** API endpoints protected against injection
- **Path Security:** Directory traversal prevention
- **File Consolidation:** Single source of truth architecture

### Performance Optimizations  
- **Database Indices:** Optimized query performance
- **Memory Management:** Proper cleanup in extensions
- **Caching Strategy:** Reduced file I/O operations

### Enhanced Tracking Consolidation
- **Single Source:** All tracking in WAI-State.json._scf_metadata
- **Comprehensive Data:** Git metadata, sync history, development health
- **Eliminated Sprawl:** No more separate kb-sync.json dependency

---

**Updated:** 2025-12-15T21:52:44.645496+00:00 via `WAI sync` (unified CLI)

