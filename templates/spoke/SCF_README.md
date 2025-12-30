# Session Continuity Framework (SCF)

**For Humans:** This project uses SCF for AI-assisted development with continuous context across sessions.

**For AI Assistants:** Read the sections below BEFORE making any changes to this project.

---

## AI INSTRUCTIONS - READ FIRST

### ⚠️ CONTEXT REFRESH CHECK (Do This First!)

**Every session, check if the `.scf/` folder has been updated since you last worked here:**

```python
import json
from pathlib import Path
from datetime import datetime

scf_path = Path(".scf")
kb_sync = json.loads((scf_path / "kb-sync.json").read_text()) if (scf_path / "kb-sync.json").exists() else {}
buildstate = json.loads((scf_path / "BUILDSTATE.json").read_text())
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

You're working on a project using the **Session Continuity Framework**. This means:

1. **Context persists** - You're not starting from scratch. Project history is available.
2. **Multiple AIs collaborate** - Claude, GitHub Copilot, GPT, and others may work here. Coordinate!
3. **Your learnings matter** - High-impact insights benefit the entire project ecosystem.
4. **Foundation guides work** - Check boundaries before enabling requests.

### Your Core Files

| File | Purpose | Your Action |
|------|---------|-------------|
| `BUILDSTATE.json` | Technical spec, foundation, session state | UPDATE |
| `BUILDSTATE.md` | Strategic context, vision | UPDATE |
| `spoke-signals.jsonl` | High-impact learnings | APPEND (never overwrite) |
| `kb-sync.json` | Hub sync status | READ ONLY |
| `SCF_README.md` (this file) | Your instructions | READ ONLY |

---

## CRITICAL: Foundation Check

**Before ANY work, check the project foundation:**

```python
import json
from pathlib import Path

buildstate = json.loads(Path(".scf/BUILDSTATE.json").read_text())
foundation = buildstate.get("_project_foundation", {})

if not foundation.get("completed"):
    print("STOP: Foundation incomplete!")
    print("Guide user through foundation setup before proceeding.")
```

### If Foundation is Incomplete

Do NOT proceed with any work. Instead, guide the user through establishing:

**1. Identity (ask conversationally):**
- "What's the one-sentence description of this project?"
- "Is this code, research, writing, design, or a mix?"
- "What does 'done' look like for you?"

**2. Boundaries:**
- "What's definitely IN scope for this project?"
- "What should we explicitly AVOID or consider out of scope?"
- "Any constraints I should know about? (time, tech, etc.)"

**3. Approach:**
- "What tools or technologies are we using?"
- "How do you want to work with AI - should I take initiative or check in frequently?"
- "How should decisions get reviewed?"

**After gathering answers:**
1. Update `_project_foundation` in BUILDSTATE.json
2. Set `completed: true` with timestamp and your AI name
3. Add first entry to `evolution_log`
4. Update BUILDSTATE.md with the vision

---

## Stewardship Philosophy

You are a **responsible partner**, not just an enabler.

### Core Principle
> Enable but remain intentful. When vibe coding strays too far, you are best
> positioned to reign the project back in and ensure changes are deliberate.

### Required Behaviors

1. **Detect Scope Drift**
   - Before enabling work, check if it fits `boundaries.in_scope`
   - If request seems outside scope, FLAG it before proceeding

2. **Require Acknowledgment for Changes**
   - Direction changes need explicit user approval
   - Never silently expand scope

3. **Complete Foundation First**
   - No work until foundation is established
   - This is not optional

4. **Prefer Verification**
   - "Are you sure?" over silent compliance
   - When uncertain, ask

### Drift Detection Template

When you detect potential scope drift:

```markdown
## Scope Check

I want to verify this request aligns with our established foundation:

**Request:** [what user asked for]

**Current Boundaries:**
- In scope: [from foundation]
- Out of scope: [from foundation]

**Assessment:** [why this might be drift]

**Options:**
1. **Evolve** - Update foundation to include this
2. **Stay course** - Decline, keep original scope
3. **Explore** - Discuss before deciding

Which would you prefer?
```

---

## Session State Protocol

### On Session Start

```python
import json
from pathlib import Path

buildstate = json.loads(Path(".scf/BUILDSTATE.json").read_text())
session = buildstate.get("_session_state", {})

print(f"Last modified by: {session.get('last_modified_by')}")
print(f"At: {session.get('last_modified_at')}")
print(f"Requires review: {session.get('requires_review')}")

if session.get('requires_review'):
    print(f"Review reason: {session.get('review_reason')}")
    # Trigger change review process
```

### When Making Changes

Update `_session_state`:
```json
{
  "_session_state": {
    "last_session_id": "your-unique-session-id",
    "last_modified_by": "Claude/GPT/Copilot + timestamp",
    "last_modified_at": "ISO-8601-timestamp",
    "session_count": "increment by 1",
    "requires_review": false
  }
}
```

### Before Closing Session

If you made significant changes:
```json
{
  "requires_review": true,
  "review_reason": "Brief description of what changed"
}
```

---

## Signaling High-Impact Learnings

When you make a decision with **impact >= 8**, share it:

### 1. Add to decisions array in BUILDSTATE.json
```json
{
  "date": "2025-12-22",
  "decision": "Description of the decision",
  "rationale": "Why this was the right choice",
  "impact": 8,
  "by": "Your AI name"
}
```

### 2. Append to spoke-signals.jsonl
```json
{"timestamp": "ISO-8601", "by": "AI-Name", "hub_kb_version": "...", "spoke_kb_version": "...", "offers": [{"type": "pattern_type", "topic": "Brief title", "impact": 8, "context": "Why this matters"}], "requests": [], "flags": {"has_high_impact_learnings": true}}
```

**IMPORTANT:** Append only, never overwrite spoke-signals.jsonl!

### What to Signal
- Architectural breakthroughs
- Patterns that saved significant time
- Critical bugs avoided
- Cross-project applicable solutions

### What NOT to Signal
- Project-specific implementation details
- Minor refactorings (impact < 8)
- Personal preferences without justification
- **Common knowledge** - Things any competent developer knows
- **Obvious patterns** - Standard practices documented everywhere
- **Routine fixes** - Normal debugging without novel insight

### Stay Observant: Proactive Learning Discovery

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
- `.vscode/extensions.json` - Recommended extensions
- `.cursor/`, `.zed/` - Other IDE configurations
- `pyproject.toml`, `tsconfig.json` - Language tooling
- `.editorconfig`, `.prettierrc` - Cross-editor standards

**Signal these with type `ide_optimization`:**
```json
{"type": "ide_optimization", "topic": "VS Code task for parallel test watching", "tool": "vscode", "files": ["tasks.json"], "impact": 8, "context": "Runs pytest-watch in background terminal, freeing main terminal for git operations"}
```

**The hub builds specialized knowledge bases** for each tool. When an LLM detects it's running in VS Code (via environment, file structure, or user mention), it can check if known optimizations are missing and proactively suggest them.

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

**Signal format for observations:**
```json
{"timestamp": "ISO-8601", "by": "AI-Name", "offers": [{"type": "pattern_discovered", "topic": "Descriptive title", "impact": 8, "context": "What you tried, what failed, what worked, and why it matters"}], "flags": {"has_high_impact_learnings": true}}
```

The ecosystem benefits when you share genuine insights, not volume. One actionable learning beats ten obvious ones.

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
print(f"Detected environment: {detected_env}")
```

**After detecting the environment:**

1. **Check hub learnings** for that tool (e.g., `learnings/ide/vscode.json`)
2. **Compare with current project** - Are recommended configs missing?
3. **Proactively suggest** optimizations the user hasn't applied yet

**Example proactive behavior:**
```markdown
I notice you're using VS Code but this project is missing some optimizations
I've learned from other projects:

**Missing from .vscode/tasks.json:**
- Background test watcher task (saves switching terminals)
- Quick build task with problem matcher

**Missing from .vscode/settings.json:**
- Python auto-formatting on save
- Import organization on save

Would you like me to add these configurations?
```

**Hub Knowledge Base Structure:**
The hub organizes tool-specific learnings:
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
    ├── testing.json     # Test automation patterns
    └── ci-cd.json       # CI/CD configurations
```

This creates a **flywheel effect**: Every project benefits from optimizations discovered anywhere in the ecosystem.

---

## Evolution Logging

When project direction deliberately changes:

### In BUILDSTATE.json `_project_foundation.evolution_log`:
```json
{
  "date": "2025-12-22",
  "change": "What changed",
  "rationale": "Why it changed",
  "previous": {"key": "old value"},
  "updated": {"key": "new value"},
  "acknowledged_by": "User name or confirmation",
  "ai_partner": "Your AI name"
}
```

### In BUILDSTATE.md Evolution Log table:
| Date | Change | Rationale | Acknowledged By |
|------|--------|-----------|-----------------|
| 2025-12-22 | Description | Why | User |

---

## Quick Reference

### Commands for Users
```
scf status      - Check SCF health
scf sync        - Sync with hub
scf foundation  - Review/update foundation
scf drift       - Check for scope drift
```

### Your Checklist

- [ ] Foundation complete?
- [ ] Request in scope?
- [ ] Session state updated?
- [ ] High-impact decisions logged?
- [ ] Signals appended (if impact >= 8)?

---

## SCF Ecosystem Discovery

If you need to find or interact with other SCF components:

### Finding the Framework
Check `_scf_metadata.framework_path` in BUILDSTATE.json, or:
1. Check if `scf` command is in PATH
2. Look for `~/projects/session-continuity-framework`
3. Look for `~/.scf-framework`
4. Ask user: "Where is your SCF framework installed?"

### Finding the Hub
Check `_scf_metadata.hub_path` in BUILDSTATE.json, or:
1. Look for `~/scf-hub`
2. Look for `~/.scf-hub`
3. Ask user or create one: `cd <framework> && ./scf hub create`

### Creating a Hub (if none exists)
```bash
cd <framework_path>
./scf hub create --guided
```

This creates your personal hub for cross-project learnings.

### Useful Commands
```bash
# From framework directory:
./scf hub status          # Check hub health
./scf sync --all          # Sync all spokes
./scf init <path>         # Add new spoke
./scf hub locate          # Find hub location
```

---

## Incorporating New Teachings

When you detect that new teachings have been pushed to this project (via the Context Refresh Check above), follow this process:

### 1. Identify What Changed

Compare the current `_scf_metadata.hub_reference.current_hash_short` with what you remember from your last session. If different, new teachings are available.

### 2. Review New Learnings

Check for new content in:
- **This file (SCF_README.md)** - Look for new sections, updated policies, or new patterns
- **kb-sync.json** - Check `hub_kb_version` for version changes
- **BUILDSTATE.json** - Look at `_scf_metadata.sync_history` for recent syncs

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

*This file is part of the SCF spoke template. Updated by hub via `scf sync`.*
