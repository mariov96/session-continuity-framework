# Session Continuity Framework - Strategic Buildstate

---

> **For SCF Users (Fork/Clone Notice):**
>
> These are the spoke files for SCF's own development - we eat our own dog food.
> When you fork or clone this repo, you have options:
> - **Keep as reference**: See how SCF tracks itself as a living example
> - **Reset for your fork**: Run `scf init --fresh` to start with your own context
> - **Build on it**: Your changes to `.scf/` won't conflict with framework updates
>
> This is intentional - the framework's own development serves as documentation.

---

**Session Continuity Framework v2.2.0**
**Structure:** v2 (.scf/ directory)
**Type:** Framework (Spoke project tracking its own development)
**Repository:** https://github.com/mariov96/session-continuity-framework
**Created by:** Mario Vaccari

*This project uses SCF to maintain perfect context across AI sessions. SCF transforms AI from order-taker to informed, responsible project partner.*

---

## Project Foundation

### Identity
- **Type:** Framework
- **One-liner:** AI-agnostic context persistence for any knowledge work
- **Success looks like:** Any AI assistant can pick up any project with full context, and learnings flow across projects automatically

### Boundaries

**In Scope:**
- Core framework code (CLI, Python modules)
- Spoke templates and schemas
- Hub creation tooling
- Documentation for SCF usage
- AI instruction generation (SCF_README.md)
- Cross-project learning protocols

**Out of Scope:**
- Hub storage (user creates separately)
- User's personal data/preferences
- IDE extensions (separate repos)
- Browser extensions (separate repos)
- Project-specific implementations

**Constraints:**
- AI-agnostic: Must work with Claude, GPT, Copilot, Gemini, etc.
- Environment-agnostic: No lock-in to specific tools
- Lightweight: Minimal dependencies, easy adoption
- Non-coding support: Works for research, writing, design - not just code

### Approach
- **Stack:** Python 3.7+, JSON/JSONL, Markdown
- **Workflow:** Dogfooding - SCF tracks its own development
- **AI Collaboration:** Collaborative - AI proposes, human approves direction changes

---

## Core Philosophy: AI as Responsible Partner

SCF's differentiating philosophy:

> **AI should enable but remain intentful.** When vibe coding strays too far,
> the LLM is best positioned to reign us back in and make intentional changes.

### Stewardship Behaviors
1. **Detect scope drift** - Flag before enabling work outside boundaries
2. **Require acknowledgment** - Direction changes need explicit approval
3. **Complete foundation first** - Guide setup before diving into work
4. **Prefer verification** - "Are you sure?" over silent compliance

### Evolution, Not Drift
When project direction changes, it should be **deliberate**:
- AI detects the drift
- Presents options to user
- User explicitly acknowledges the change
- Change is logged in `evolution_log` with rationale

---

## Architecture: Framework + Hub + Spokes

```
┌─────────────────────────────────────────────────────────────┐
│  SCF Framework (this repo)                                  │
│  - Core code (CLI, Python modules)                          │
│  - Spoke templates                                          │
│  - Hub creation tooling                                     │
│  - Documentation                                            │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ User runs: scf hub create
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  User's Hub (~/scf-hub/ or custom location)                 │
│  - hub-profile.json (personal preferences)                  │
│  - .scf-registry/ (discovered projects)                     │
│  - learnings/ (cross-project patterns)                      │
└─────────────────────────────────────────────────────────────┘
                              │
            ┌─────────────────┼─────────────────┐
            ▼                 ▼                 ▼
      ┌──────────┐      ┌──────────┐      ┌──────────┐
      │ Project A│      │ Project B│      │ Project C│
      │  (spoke) │      │  (spoke) │      │  (spoke) │
      │  .scf/   │      │  .scf/   │      │  .scf/   │
      └──────────┘      └──────────┘      └──────────┘
```

**Key insight:** The framework provides the intelligence. The hub stores YOUR learnings. Spokes are your projects.

---

## Inspiration: Learning from Conductor

Google's Conductor for Gemini CLI validates our approach:
- Both: Persistent files over ephemeral chat
- Both: Planning before implementation
- Both: Structured specs and context

**SCF goes further:**
- AI-agnostic (not locked to one AI)
- Non-coding support (research, writing, design)
- Cross-project learning (hub propagates insights)
- Responsible partner philosophy (drift detection)

---

## Current Focus

### Active Work
- Project Foundation system with drift detection
- Framework-Hub separation (clean architecture)
- Spoke templates with foundation schema

### Next Up
- `scf hub create` command for guided hub setup
- Extension separation (VS Code, Browser to own repos)
- Non-coding project templates

### Future Vision
- Multi-AI handoff protocols
- Team hub sharing
- Learning marketplace

---

## Session Continuity Commands

```
/scf_status        Check SCF compliance
/scf_sync          Sync with hub
/scf_session       Check who last modified
/scf_foundation    Review/update project foundation
/scf_drift         Check for scope drift
/scf_evolve        Deliberately change project direction
```

---

## Evolution Log

| Date | Change | Rationale | Acknowledged By |
|------|--------|-----------|-----------------|
| 2025-12-22 | Framework-Hub separation | Clean architecture - framework is code, hub is user's data | Mario Vaccari |
| 2025-12-22 | Project Foundation system | Learned from Conductor - guided setup with drift detection | Mario Vaccari |
| 2025-12-22 | AI stewardship philosophy | Enable but remain intentful - AI as responsible partner | Mario Vaccari |

---

## AI Session Instructions

### Before Starting Work
1. Read `SCF_README.md` for current policies
2. Check `_session_state` in BUILDSTATE.json
3. Check `_project_foundation.boundaries` - is this request in scope?
4. If drift detected, flag before proceeding

### During Work
- Update `_session_state.last_modified_by` and `last_modified_at`
- Add decisions with impact >= 5 to decisions array
- Signal learnings with impact >= 8 to spoke-signals.jsonl

### On Direction Change
- Present drift detection alert
- Require explicit user choice (evolve/stay course/explore)
- Log to `evolution_log` if user approves change

---

*This strategic buildstate tracks SCF's own development - a living example of the framework in action.*
