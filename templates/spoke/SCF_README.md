# Session Continuity Framework (SCF)

**For Humans:** This project uses SCF for AI-assisted development with continuous context across sessions.

**For AI Assistants:** Read the sections below BEFORE making any changes to this project.

---

## AI INSTRUCTIONS - READ FIRST

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

*This file is part of the SCF spoke template. Updated by hub via `scf sync`.*
