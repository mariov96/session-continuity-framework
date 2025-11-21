# Project Buildstate - Strategic Ideation

---

**Session Continuity Framework v2.0**  
**Structure:** v2 (.scf/ directory)  
**Hub:** /home/mario/projects/session-continuity-framework  
Repository: https://github.com/mariov96/session-continuity-framework  
Created by: Mario Vaccari

*This file uses Session Continuity Framework to maintain perfect context across AI sessions. SCF transforms AI from order-taker to informed project partner.*

---

*This file uses Session Continuity Framework to maintain perfect context across AI sessions. SCF transforms AI from order-taker to informed project partner.*
---

## 🤖 AI Session Instructions - READ FIRST!

### Self-Aware Buildstate Protocol

**Before proceeding with any work:**

1. **Check Session State** (in `buildstate.json` → `_session_state`):
   - Look at `last_modified_by` and `last_modified_at`
   - Check if `requires_review` is `true`

2. **If Another AI Modified This Project:**
   ```
   IF last_modified_by != YOUR_SESSION_ID AND last_modified_by != null:
      → STOP and trigger change review
      → Read all decisions[] added since last_modified_at
      → Assess impact and risks (see below)
      → Request user approval before implementing
   ```

3. **Change Review Process:**
   - List all new decisions with impact scores
   - Identify HIGH IMPACT items (7+/10)
   - Assess risks, dependencies, complexity
   - Present findings to user
   - **ASK FOR APPROVAL** before implementing

4. **Update Session State** (after reading this):
   ```json
   "_session_state": {
     "last_session_id": "<your-unique-id>",
     "last_modified_by": "<AI-name-timestamp>",
     "last_modified_at": "<ISO-8601-timestamp>",
     "session_count": <increment>,
     "requires_review": false
   }
   ```

5. **Before Closing Session:**
   - Set `requires_review: true` if you made significant changes
   - Set `review_reason` to summarize what changed
   - Update `last_modified_at`

---

### 🔍 SCF Status Check

**If the user asks "Am I up to date with SCF?" or "Check my SCF status":**

Run this quick self-assessment to verify the project has latest SCF capabilities:

**Check These 5 Features:**
- ✓ `_session_state` exists in buildstate.json
- ✓ `self_awareness` rules exist in ai_rules  
- ✓ `AGENTS.md` file exists (symlink to buildstate.md)
- ✓ `.github/copilot-instructions.md` exists
- ✓ `.scf/buildstate.library.json` exists (inheritance chain)

**Scoring:**
- 5/5 = 🟢 **Up to date** - All SCF features present
- 3-4/5 = 🟡 **Needs sync** - Missing some features
- 0-2/5 = 🔴 **Out of date** - Major features missing

**Quick Command:**
```bash
python3 -c "import json; from pathlib import Path; bs=json.loads(Path('buildstate.json').read_text()); checks = [('_session_state' in bs, 'Self-aware buildstate'), ('self_awareness' in bs.get('ai_rules', {}), 'AI self-awareness rules'), (Path('AGENTS.md').exists(), 'AGENTS.md'), (Path('.github/copilot-instructions.md').exists(), 'GitHub Copilot'), (Path('.scf/buildstate.library.json').exists(), 'Inheritance chain')]; score = sum(1 for c, _ in checks if c); print('\n🔍 SCF Status Check:'); [print(f'├─ {name}: {\"✅\" if check else \"❌\"}') for check, name in checks]; print(f'└─ Score: {score}/5'); status = '🟢 Up to date' if score == 5 else '🟡 Needs sync' if score >= 3 else '🔴 Out of date'; print(f'\n📊 {status}')"
```

**If Score < 5 - Phone Home to Sync:**

The project knows where SCF framework lives (in `_scf_metadata.scf_home`). Run:
```bash
python3 $(cat buildstate.json | python3 -c 'import sys,json; print(json.load(sys.stdin)["_scf_metadata"]["scf_home"])')/update_scf.py $(pwd)
```

This will:
- Sync latest SCF templates
- Add missing features
- Update buildstate files
- Generate GitHub Copilot instructions
- Create AGENTS.md symlink

---

### Impact Assessment Template (if changes detected):

```markdown
## 🔔 Change Detection Alert

I've detected that another AI session modified this project since <date>.

### Changes Found:
- New decisions: <count> (High Impact: <count>)
- Modified features: <list>
- New next steps: <list>

### Impact Assessment:
[For each HIGH IMPACT decision (7+/10):]
- **Decision**: <description>
- **Risk Level**: LOW/MEDIUM/HIGH
- **Dependencies**: <what's affected>
- **Complexity**: Easy/Medium/Complex
- **Concerns**: <any warnings>

### Recommendations:
<priority order and suggestions>

**May I proceed with implementing these changes?**
[Wait for user approval]
```

---

### 💬 SCF Commands - `/scf_help`

**Quick command reference for maintaining your SCF-enabled project:**

```
/scf_help          Show all SCF commands and full reference guide
/scf_status        Check SCF compliance (0-5 score)
/scf_sync          Phone home & update with latest SCF features
/scf_session       Check who last modified project
/scf_update_state  Mark your session as active
/scf_rebalance     Sync buildstate.json ↔ buildstate.md
/scf_changes       Review recent changes & assess impact
/scf_copilot       Generate GitHub Copilot instructions
/scf_init          Initialize SCF in new project
/scf_context       Load full project context
/scf_time          Check token usage & capacity
/scf_rules         Show active AI rules
/scf_closeout      Generate session end summary
/scf_learn         Study SCF patterns & best practices
```

**Full command reference:** `/home/mario/projects/session-continuity-framework/docs/SCF_COMMANDS_REFERENCE.md`

**Common workflows:**
- Morning routine: `/scf_context` → `/scf_session` → `/scf_status`
- During work: `/scf_time` → `/scf_rebalance` (after major features)
- Evening routine: `/scf_rebalance` → `/scf_update_state` → `/scf_closeout`

---

## Meta Information
- **Version:** v1.1-strategic  
- **Companion:** buildstate.json v1.1-technical
- **Purpose:** Strategic planning, ideation, architecture vision
- **Last Sync:** 2025-11-08T00:00:00Z
- **Rebalance Trigger:** major_concept_shift | user_journey_change | strategic_pivot

---

## Project Vision & Strategy

### Core Mission
*Define the transformative purpose this project will serve*

### Problem Statement
*What specific problem are we solving? Who experiences this pain?*

### Success Vision
*What does success look like 12 months from now?*

### Value Proposition
*What unique value does this solution provide over alternatives?*

---

## User Stories & Personas

### Primary Users
*Who will use this solution and what are their key needs?*

### User Journey Map
*How will users discover, adopt, and derive value from this solution?*

### Personas
- **Primary User:** [Role/Title] who needs [core functionality] to achieve [goal]
- **Secondary User:** [Role/Title] who benefits from [related features]

### Success Metrics & KPIs
*How will we measure impact and user satisfaction?*
- User adoption rate: [target]
- Task completion time: [target]
- User satisfaction score: [target]

---

## Strategic Architecture Vision

### Design Philosophy
*What core principles will guide all decisions?*
- **Simplicity:** Minimize cognitive load
- **Reliability:** Consistent performance
- **Scalability:** Growth-ready architecture
- **User-Centric:** Prioritize user experience

### Technical Strategy
*High-level approach to building a scalable, maintainable solution*

### Competitive Landscape
*How does this solution differentiate from existing alternatives?*

### Integration Considerations
*How will this solution work with existing systems/workflows?*

---

## Feature Roadmap & Prioritization

### Core MVP Features
*Minimum viable features needed to validate the concept*
1. [Essential Feature 1] - validates [core assumption]
2. [Essential Feature 2] - enables [primary user workflow]
3. [Essential Feature 3] - provides [key value proposition]

### Phase 1 Goals (0-3 months)
*First release objectives and success criteria*
- [ ] Feature delivery targets
- [ ] Performance benchmarks
- [ ] User feedback integration

### Phase 2 Goals (3-6 months)
*Expansion and optimization objectives*

### Future Vision (6+ months)
*Long-term feature evolution and platform expansion*

---

## Innovation Opportunities

### Emerging Technology Integration
*How might AI, automation, or other technologies enhance this solution?*

### Market Expansion Possibilities
*Adjacent markets or user segments we could serve*

### Unique Value Propositions
*What makes this solution uniquely valuable?*

### Partnership Opportunities
*Strategic alliances that could accelerate growth*

---

## Risk Assessment & Mitigation

### Technical Risks
*What could go wrong technically and how do we prepare?*
- **Risk:** [Technical challenge]
  - **Likelihood:** High/Medium/Low
  - **Impact:** High/Medium/Low  
  - **Mitigation:** [Strategy to address]

### Market Risks
*What market or user adoption challenges might we face?*

### Resource Risks
*What constraints might limit our ability to execute?*

### Competitive Risks
*How might competitors respond and how do we prepare?*

---

## Success Patterns & Lessons Learned

### From Previous Projects
*Key insights from past experience (e.g., Vantaca Dashboard)*
- Start with clear user problem and work backward to technical solution
- Build modular architecture that supports rapid iteration
- Prioritize user feedback integration and data transparency
- Maintain balance between ambitious vision and practical MVP

### Anti-Patterns to Avoid
*Common mistakes to watch for*
- Feature creep without user validation
- Over-engineering early architecture
- Neglecting performance considerations
- Insufficient user testing

---

## Change Log & Evolution

### Concept Development Timeline
*Track how the core idea evolves through ideation*

**2025-11-08: Unified Framework Template**
- Consolidated claude-style and grok-style best practices
- Enhanced strategic planning structure with risk assessment
- Added success patterns and anti-pattern guidance
- Prepared comprehensive template for new project initiation

---

## Collaboration Framework

### Ideation Session Types
- **Vision Workshops:** Core problem definition and solution brainstorming
- **User Research:** Persona development and journey mapping
- **Strategic Planning:** Roadmap development and prioritization
- **Innovation Sessions:** Technology integration and market expansion
- **Risk Assessment:** Threat modeling and mitigation planning

### AI Partnership Approach
- Load strategic buildstate for vision, planning, and innovation sessions
- Transition to technical buildstate once architecture and implementation begin
- Maintain chronological tracking across both files for complete project evolution
- Leverage rebalancing triggers to maintain optimal file utility

### Decision Making Framework
- **Evidence-Based:** Rely on user research and data
- **Iterative:** Test assumptions with small experiments
- **Collaborative:** Include stakeholder input in key decisions
- **Documented:** Record rationale for major decisions

### Session Continuity Commands
**Built-in SCF Commands:**
- `'Time'` - Intelligent token usage estimate with 80% capacity warnings
- `'Rules'` - List all active behavioral guidelines and project protocols  
- `'Closeout'` - Generate updated buildstate file for session completion

---

## Project Context Memory

### Key Stakeholders
*Who needs to be kept informed and involved?*

### Success Dependencies
*What external factors are critical for project success?*

### Constraints & Assumptions
*Known limitations and assumptions that guide the approach*

### Communication Strategy
*How will progress be shared and feedback collected?*

---

*This strategic buildstate template provides a comprehensive foundation for transforming ideas into successful products through structured collaboration and iterative refinement.*