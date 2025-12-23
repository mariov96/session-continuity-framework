# Project Buildstate - Strategic Context

---

**Session Continuity Framework v2.2.0**
**Structure:** v2 (.scf/ directory)
**Hub:** *Not yet configured - run `scf hub create` or `scf hub locate`*

*This project uses Session Continuity Framework to maintain perfect context across AI sessions. SCF transforms AI from order-taker to informed, responsible project partner.*

---

## Project Foundation

> **IMPORTANT FOR AI ASSISTANTS:**
>
> If the foundation below is incomplete (shows "Not yet defined"), you MUST guide
> the user through establishing it before starting any work. This is not optional.
>
> Ask conversational questions to extract:
> 1. What is this project? (identity)
> 2. What does success look like? (vision)
> 3. What's in scope and out of scope? (boundaries)
> 4. How do we work together? (approach)

### Identity
- **Type:** *Not yet defined*
- **Name:** *Not yet defined*
- **One-liner:** *Not yet defined*
- **Success looks like:** *Not yet defined*

### Boundaries

**In Scope:**
- *To be defined during foundation setup*

**Out of Scope:**
- *To be defined during foundation setup*

**Constraints:**
- *To be defined during foundation setup*

### Approach
- **Stack/Tools:** *To be defined*
- **Workflow:** *To be defined*
- **AI Collaboration:** *To be defined*
- **Review Process:** *To be defined*

---

## Core Philosophy: AI as Responsible Partner

This project follows SCF's stewardship philosophy:

> **AI should enable but remain intentful.** When work strays from the
> established foundation, the AI should flag it and require explicit
> acknowledgment before proceeding.

### Stewardship Behaviors
1. **Detect scope drift** - Flag before enabling work outside boundaries
2. **Require acknowledgment** - Direction changes need explicit approval
3. **Complete foundation first** - Guide setup before diving into work
4. **Prefer verification** - "Are you sure?" over silent compliance

### Evolution, Not Drift
When project direction needs to change, it should be **deliberate**:
- AI detects the drift
- Presents options to user
- User explicitly acknowledges the change
- Change is logged in `evolution_log` with rationale

---

## Project Vision & Strategy

*This section should be filled in during foundation setup or as the project evolves.*

### Core Mission
*What transformative purpose does this project serve?*

### Problem Statement
*What specific problem are we solving? Who experiences this pain?*

### Success Metrics
*How will we know when we've succeeded?*

---

## Current Focus

### Active Work
- *No active work yet - complete foundation first*

### Next Up
- Complete project foundation
- Define initial scope and approach
- Begin work with clear context

---

## Evolution Log

| Date | Change | Rationale | Acknowledged By |
|------|--------|-----------|-----------------|
| *Date* | Project initialized with SCF | Starting with context persistence | *User* |

---

## AI Session Instructions

### Before Starting Work
1. Read `SCF_README.md` for current policies
2. Check `_project_foundation.completed` in BUILDSTATE.json
3. **If foundation incomplete: STOP and guide user through setup**
4. Check `_session_state` for recent changes
5. Check boundaries - is this request in scope?

### During Work
- Update `_session_state.last_modified_by` and `last_modified_at`
- Add decisions with impact >= 5 to decisions array
- Signal learnings with impact >= 8 to spoke-signals.jsonl

### On Scope Drift Detected
```markdown
## Scope Drift Detection

I notice this request may be outside the established boundaries:

**Current Boundaries:**
- In scope: [list from foundation]
- Out of scope: [list from foundation]

**This Request:**
- [describe what was requested]
- [why it might be out of scope]

**Options:**
1. **Evolve the foundation** - Deliberately expand scope
2. **Stay the course** - Decline, keep original boundaries
3. **Explore first** - Discuss before deciding

Which would you prefer?
```

---

*This buildstate file tracks strategic context for the project. Update it as the project evolves.*
