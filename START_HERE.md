# 🚀 SCF Quick Bootstrap

**AI Assistant: Read ONLY this file to initialize a project from conversation.**

## Your Task

Extract conversation context and generate buildstate files in proper `.scf/` folder structure.

---

## Step 1: Extract These 5 Things

From the conversation, identify:

1. **Project name/concept** - What's being built?
2. **Problem statement** - What pain does this solve?
3. **Features discussed** - What capabilities mentioned? (minimum 2-3)
4. **Technical decisions** - Any tech choices or approaches?
5. **Vision/goal** - Where is this headed?

---

## Step 2: Generate BUILDSTATE.json

```json
{
  "project_metadata": {
    "name": "[project-name]",
    "inception_date": "[YYYY-MM-DD]",
    "initialized_from": "conversation_eject",
    "ejected_at": "[ISO-timestamp]"
  },
  
  "idea": {
    "problem": "[one sentence problem statement]",
    "vision": "[one sentence goal]",
    "for_who": "[target users]"
  },
  
  "features": {
    "discussed": [
      {
        "name": "[feature-name]",
        "description": "[brief description]",
        "source": "conversation"
      }
    ]
  },
  
  "decisions": [
    {
      "decision": "[what was decided]",
      "rationale": "[why]",
      "date": "[YYYY-MM-DD]",
      "alternatives": ["[other options discussed]"]
    }
  ],
  
  "conversation_summary": "[2-3 sentences capturing essence of discussion]",
  
  "next_steps": [
    "[action item 1]",
    "[action item 2]"
  ],
  
  "stage": "ideation",
  
  "_session_state": {
    "session_count": 1,
    "last_updated": "[ISO-timestamp]",
    "initialized_by": "conversation_bootstrap",
    "scf_hub": "/home/mario/projects/session-continuity-framework"
  }
}
```

---

## Step 3: Generate BUILDSTATE.md

```markdown
# [Project Name]

**Started:** [Date]  
**Stage:** Ideation  
**Status:** Active

---

## The Problem

[2-3 sentences describing the pain point or opportunity]

## The Vision  

[What we're building and why it matters]

## For Who

[Target users/audience]

---

## What We've Discussed

### Features & Capabilities
- **[Feature 1]**: [Description]
- **[Feature 2]**: [Description]
- **[Feature 3]**: [Description]

### Key Decisions
- **[Decision 1]**: [Rationale] *(date)*
- **[Decision 2]**: [Rationale] *(date)*

---

## Next Steps

1. [Action item from conversation]
2. [Action item from conversation]

---

## Conversation Summary

[3-4 sentences capturing the key insights and direction from discussion]

---

*Context ejected on [date] at [time]*  
*Hub: /home/mario/projects/session-continuity-framework*  
*Continue by loading these files into any SCF-aware AI tool*
```

---

## Step 4: Ask User

**"Where should I save these files?"**

Suggest:
- `~/.scf/ideas/[project-name]/` (if exploring ideas)
- `~/projects/[project-name]/.scf/` (if ready to build)
- Current directory `.scf/` (if already in project)
- Custom path (user's choice)

---

## Step 5: Create Folder Structure

Create the `.scf/` directory structure in target location:

```bash
mkdir -p .scf/archives
```

**Structure**:
```
.scf/
├── BUILDSTATE.json          # Technical specs
├── BUILDSTATE.md            # Strategic narrative  
└── archives/                # Auto-generated backups (timestamped)
```

**Hub vs Spoke Architecture**:
- **Hub** = `/home/mario/projects/session-continuity-framework` (meta-learnings, templates)
- **Spoke** = Each project's `.scf/` directory (project-specific context)
- Hub tracks spokes via discovery (buildstate_hunter_learner.py)
- Spokes reference hub in `_session_state.scf_hub`
- No duplication - hub learns from spokes, doesn't store their files

**Optional**: Create ecosystem-compatible symlink in project root:
```bash
ln -s .scf/BUILDSTATE.md AGENTS.md
```

---

## Step 6: Create Files

Create both files in `.scf/` directory:
- `.scf/BUILDSTATE.json`
- `.scf/BUILDSTATE.md`

---

## Done!

Tell user:
```
✅ Context ejected successfully!

Created:
  .scf/BUILDSTATE.json (structured data)
  .scf/BUILDSTATE.md (human-readable)
  [AGENTS.md symlink - if created]

Location: [path]

You can now:
  • Continue in any AI tool by loading these files
  • Version control your thinking (add .scf/ to git or .gitignore)
  • Never lose this context
  • Connect to SCF hub for ecosystem learning
```

---

## If Missing Info

If conversation didn't cover something, use:
- `"[to-be-determined]"` for unclear items
- Empty arrays `[]` if no decisions yet
- `"stage": "ideation"` if just talking
- `"stage": "development"` if coding started

---

## Token Budget

This file: ~850 tokens

Works even in 95% full conversations.

---

## User Command

Tell your AI assistant:

```
Read /home/mario/projects/session-continuity-framework/START_HERE.md 
and initialize this project
```

The AI will extract our conversation and create buildstate files in proper `.scf/` structure.
