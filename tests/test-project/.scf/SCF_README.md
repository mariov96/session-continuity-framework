# Session Continuity Framework (SCF)

**For Humans:** This project uses SCF for AI-assisted development with continuous context across sessions.

**For AI Assistants:** Read the sections below BEFORE making any changes to this project.

---

## 🤖 AI INSTRUCTIONS - READ FIRST

### What is SCF?

You're working on a project using the **Session Continuity Framework**. This means:

1. **Context persists** - You're not starting from scratch. Project history is available.
2. **Multiple AIs collaborate** - Claude, GitHub Copilot, and others may work here. Coordinate!
3. **Your learnings matter** - High-impact insights benefit the entire project ecosystem.
4. **You receive learnings** - This project gets best practices from other successful projects.

### Your Core Files

📄 **BUILDSTATE.json** - Technical specification (YOU UPDATE)
- Features, stack, decisions, bugs, next steps
- Session state tracking (who, when, what changed)
- Deterministic data for AI consumption

📝 **BUILDSTATE.md** - Strategic context (YOU UPDATE)
- Vision, ideation, human-readable rationale
- Why decisions were made
- User stories and success metrics

📡 **spoke-signals.jsonl** - Communication log (YOU APPEND)
- Signal high-impact learnings to hub
- Request hub actions (rebalance, updates)
- Append-only log (don't overwrite!)

📊 **kb-sync.json** - Knowledge tracking (READ ONLY)
- What you've learned from the hub
- Current sync status
- Updated by hub via teach.py

📖 **This file (SCF_README.md)** - Your instructions (HUB UPDATES)
- Current SCF policies
- Learnings from other projects
- Project-specific recommendations
- Updated when user runs teach.py

---

## 📋 Current SCF Policies

### Policy: Session State Updates (v2025-11-25)

**ALWAYS update `_session_state` in BUILDSTATE.json when you make changes:**

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

1. Add decision to `decisions` array in BUILDSTATE.json
2. Append offer to spoke-signals.jsonl

**Example code:**
```python
import json
from datetime import datetime, timezone

# 1. Add to decisions in BUILDSTATE.json (do this first)
decision = {
    "date": datetime.now().date().isoformat(),
    "impact": 9,
    "decision": "Centralized error handling with request tracking",
    "rationale": "Consistent error format improves debugging and client integration",
    "context": "Multiple endpoints had different error formats causing client confusion"
}

# 2. Append signal to spoke-signals.jsonl
signal = {
    "timestamp": datetime.now(timezone.utc).isoformat(),
    "by": "Claude",  # Your AI name
    "hub_kb_version": "2025-11-30T00:00:00Z",  # From kb-sync.json
    "spoke_kb_version": "2025-11-30T00:00:00Z",  # From kb-sync.json
    "offers": [{
        "type": "architectural_breakthrough",
        "topic": "Centralized API error handling",
        "impact": 9,
        "location": "BUILDSTATE.json:decisions[12]",
        "context": "Pattern applicable to any REST API project. Improves debugging with request IDs and consistent format."
    }],
    "requests": [],
    "flags": {
        "needs_rebalance": False,
        "has_high_impact_learnings": True
    }
}

# Append to file (don't overwrite!)
with open(".scf/spoke-signals.jsonl", "a") as f:
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

**Why:** Your breakthrough might save another project days of work. Quality over quantity!

---

### Policy: Hub Check-In (v2025-11-30)

**Periodically check if hub has new learnings for you:**

```python
import json
from datetime import datetime
from pathlib import Path

# Read sync status
kb_sync = json.loads(Path(".scf/kb-sync.json").read_text())

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
1. This file (SCF_README.md) - Instructions and learnings
2. BUILDSTATE.md - Project vision and strategic context
3. BUILDSTATE.json - Current technical state
4. spoke-signals.jsonl (last few lines) - Recent activity

**Quick context check:**
```python
import json
from pathlib import Path

# Read session state
buildstate = json.loads(Path("BUILDSTATE.json").read_text())
session = buildstate.get("_session_state", {})

print(f"Last modified by: {session.get('last_modified_by')}")
print(f"At: {session.get('last_modified_at')}")
print(f"Requires review: {session.get('requires_review')}")
if session.get('review_reason'):
    print(f"Reason: {session.get('review_reason')}")
```

### Updating Context

**After making changes:**
1. Update BUILDSTATE.json with your changes
2. Update _session_state (who, when, review status)
3. Add to decisions if impact ≥ 5
4. Append to spoke-signals.jsonl if impact ≥ 8

---

## 🔗 Integration Points

### AGENTS.md Symlink

This project has: `AGENTS.md -> .scf/SCF_README.md`

Tools like Zed, Cursor, and Aider will read this file for agent instructions.

### Git Hooks (Optional)

Consider adding a post-commit hook to update signals:
```bash
# .git/hooks/post-commit
#!/bin/bash
# Remind to update signal after commits
echo "Reminder: Update .scf/spoke-signals.jsonl if you made high-impact changes"
```

---

## ❓ Need Help?

**For project context:**
- Read BUILDSTATE.md for vision
- Check decisions array for past reasoning
- Review spoke-signals.jsonl for recent activity

**For SCF help:**
- Hub location: {{HUB_PATH}}
- Documentation: {{HUB_PATH}}/docs/
- Issues: https://github.com/mariov96/session-continuity-framework/issues

---

**Last updated by hub:** {{LAST_UPDATED}}
**Via:** teach.py

---

*This file is maintained by the SCF Hub. Local edits may be overwritten when teach.py runs.*
