# SCF Change Notification System

**Status**: ✅ COMPLETE  
**Date**: 2025-11-10  
**Purpose**: Alert LLMs to review project changes and assess risks before implementation

---

## Overview

The SCF Change Notification System solves a critical problem: **How do you tell an LLM there are new decisions/instructions it should review before taking action?**

When you run `update_scf.py` or make changes to your buildstate, the LLM needs to:
1. **Detect** what changed
2. **Assess** impact and risks
3. **Request approval** before implementing

This system automates that entire workflow.

---

## How It Works

### 1. Automatic Change Detection
The system scans `buildstate.json` for recent changes:
- **New decisions** (with dates and impact scores)
- **Pending next_steps** (not marked complete)
- **Modified features** (in progress, blocked, or warning status)
- **New bugs** (open issues)

### 2. Impact Assessment Prompt
Generates a structured review prompt that asks the LLM to:
- Review each HIGH IMPACT decision (7+/10)
- Identify potential risks and dependencies
- Assess implementation complexity
- Evaluate resource requirements
- Check reversibility

### 3. Approval Gate
**Critical**: The LLM is explicitly instructed:
- ❌ **DO NOT implement anything yet**
- ✅ Present findings and recommendations first
- ✅ Ask "May I proceed with implementing [specific changes]?"
- ✅ Wait for explicit user approval

---

## Usage

### Quick Start
```bash
# Load project with automatic change detection
python3 scf_load_project.py /path/to/project

# Check changes from last 48 hours
python3 scf_load_project.py /path/to/project --since-hours 48

# Just show changes (no full context)
python3 scf_load_project.py /path/to/project --changes-only

# Save to file for sharing with LLM
python3 scf_load_project.py /path/to/project --output context.md
```

### Programmatic Usage
```python
from scf_llm_integration import SCFLLMIntegrator
from pathlib import Path

# Initialize integrator
integrator = SCFLLMIntegrator(Path('/path/to/project'))

# Detect changes from last 7 days
changes = integrator.detect_recent_changes(since_hours=168)

# Generate review prompt
if changes['requires_review']:
    review_prompt = integrator.generate_change_review_prompt(changes)
    print(review_prompt)

# Load full context with notifications
context = integrator.load_project_context_with_notifications()
print(context)
```

---

## Example Workflow

### Scenario: After Running `update_scf.py`

1. **User updates project**:
   ```bash
   python3 update_scf.py my-project
   ```

2. **LLM starts new session**:
   ```bash
   python3 scf_load_project.py my-project
   ```

3. **System detects changes**:
   ```
   📊 Changes detected:
      - New decisions: 3
      - Pending next steps: 5
      - Features in progress: 2
   
   ⚠️ Review required before proceeding!
   ```

4. **LLM receives structured prompt**:
   ```markdown
   # 🔔 SCF Change Notification - Review Required
   
   ## New Decisions (Require Impact Assessment)
   
   ### 1. Implement GitHub Copilot integration
   - Date: 2025-11-10
   - Impact: 🔴 10/10
   - Rationale: Auto-generate custom instructions...
   
   ## ⚠️ REQUIRED: Impact & Risk Assessment
   [Detailed assessment instructions]
   ```

5. **LLM assesses and responds**:
   ```markdown
   ## Impact & Risk Assessment
   
   ### High Priority Items
   1. GitHub Copilot integration (Impact 10/10)
      - Risk: MEDIUM - Well-documented API
      - Complexity: LOW - Clear implementation path
      - Time: 2-3 hours
   
   ### Recommendations
   - Proceed with Copilot integration first (high value, low risk)
   - Test on single project before rolling out
   
   **Ready to implement?** May I proceed with the GitHub Copilot 
   integration following the plan above?
   ```

6. **User approves**:
   ```
   Yes, proceed with the Copilot integration.
   ```

7. **LLM implements** with confidence.

---

## Change Detection Logic

### Time-Based Filtering
Changes are detected using date comparison:
- Decisions with `date` field in `YYYY-MM-DD` format
- Compared against `since_hours` parameter (default: 24 hours)
- Recent changes flagged for review

### Status-Based Detection
- **Next Steps**: Any not starting with ✅ (incomplete)
- **Features**: Status is 🔄 (in progress), 🚧 (blocked), or ⚠️ (warning)
- **Bugs**: Any entries in `bugs` array

### Impact Scoring
Decisions are categorized by impact:
- 🔴 **HIGH** (7-10): Requires detailed risk assessment
- 🟡 **MEDIUM** (4-6): Moderate consideration needed
- 🟢 **LOW** (1-3): Minor changes

---

## Generated Prompt Structure

The system generates a comprehensive review prompt:

```markdown
# 🔔 SCF Change Notification - Review Required

## 📊 Change Summary
- New Decisions: 7 (High Impact: 5)
- Pending Next Steps: 10
- Features In Progress: 3
- Open Bugs: 2

## 🎯 New Decisions (Require Impact Assessment)
[Each decision with date, impact, rationale, context]

## 📋 Pending Next Steps
[List of incomplete action items]

## 🚧 Features In Progress
[Active features with status]

## 🐛 Open Bugs
[Known issues]

## ⚠️ REQUIRED: Impact & Risk Assessment
[Detailed assessment instructions]

## 📝 Your Assessment Format
[Template for LLM response]
```

---

## Integration with SCF Workflow

### init_scf.py
When initializing a new project:
- No changes detected (new project)
- Full context loaded without notifications

### update_scf.py
After updating a project:
- Changes logged to buildstate
- Next LLM session gets notification automatically

### Continuous Development
During active development:
- Changes accumulate in buildstate
- Periodic reviews catch new decisions
- Impact assessment prevents oversight

---

## Benefits

### 🛡️ Risk Mitigation
- Catches high-impact changes before implementation
- Forces explicit risk assessment
- Prevents "surprise" breaking changes

### 🎯 Focus & Clarity
- LLM knows exactly what's new
- Clear priorities for implementation
- Structured decision-making process

### ✅ Approval Control
- User maintains control over implementation
- No unauthorized changes
- Explicit consent required

### 📊 Audit Trail
- All decisions logged with dates and impact
- Review history preserved in buildstate
- Clear rationale for every change

---

## CLI Reference

### scf_load_project.py

**Synopsis**:
```bash
python3 scf_load_project.py PROJECT_PATH [OPTIONS]
```

**Arguments**:
- `PROJECT_PATH` - Path to SCF-enabled project

**Options**:
- `--since-hours N` - Check changes from last N hours (default: 168 = 7 days)
- `--changes-only` - Only show changes, not full context
- `--session-type TYPE` - Session type: ideation, implementation, analysis, optimization, planning
- `--output FILE` - Save output to file
- `--quiet` - Suppress status messages

**Examples**:
```bash
# Load with 24-hour change detection
python3 scf_load_project.py my-project --since-hours 24

# Just show changes
python3 scf_load_project.py my-project --changes-only

# Save for later use
python3 scf_load_project.py my-project --output context.md

# Quiet mode (pipe to LLM)
python3 scf_load_project.py my-project --quiet | pbcopy
```

---

## API Reference

### SCFLLMIntegrator Methods

#### `detect_recent_changes(since_hours=24)`
Detect changes in buildstate since specified time.

**Parameters**:
- `since_hours` (int): Hours to look back (default: 24)

**Returns**:
```python
{
    'new_decisions': [
        {'date': '2025-11-10', 'decision': '...', 'impact': 10, ...}
    ],
    'new_next_steps': ['Step 1', 'Step 2'],
    'modified_features': [
        {'id': 'feat-1', 'status': '🔄', 'priority': 'high'}
    ],
    'new_bugs': ['Bug description'],
    'change_summary': {
        'total_new_decisions': 3,
        'high_impact_decisions': 2,
        'pending_next_steps': 5,
        'features_in_progress': 2,
        'open_bugs': 1
    },
    'requires_review': True
}
```

#### `generate_change_review_prompt(changes=None)`
Generate structured review prompt for LLM.

**Parameters**:
- `changes` (Dict, optional): Changes dict from `detect_recent_changes()`. If None, detects automatically.

**Returns**: Formatted markdown prompt string

#### `load_project_context_with_notifications(session_type=SessionType.IMPLEMENTATION)`
Main entry point - loads context with change notifications.

**Parameters**:
- `session_type` (SessionType): Type of session

**Returns**: Complete context string ready for LLM

---

## Configuration

### Default Time Windows
```python
# Default: 7 days (168 hours)
changes = integrator.detect_recent_changes(since_hours=168)

# Last 24 hours (daily review)
changes = integrator.detect_recent_changes(since_hours=24)

# Last 48 hours (after weekend)
changes = integrator.detect_recent_changes(since_hours=48)

# Last 30 days (monthly review)
changes = integrator.detect_recent_changes(since_hours=720)
```

### Impact Thresholds
Defined in prompt generation:
- **HIGH** (🔴): `impact >= 7` - Detailed risk assessment required
- **MEDIUM** (🟡): `impact >= 5` - Moderate review needed
- **LOW** (🟢): `impact < 5` - Informational

---

## Best Practices

### 1. Regular Reviews
Run `scf_load_project.py` at the start of each session:
```bash
# Morning standup
python3 scf_load_project.py my-project --since-hours 24

# After team updates
python3 scf_load_project.py my-project --since-hours 48

# Weekly review
python3 scf_load_project.py my-project --since-hours 168
```

### 2. Impact Scoring Guidelines
When adding decisions to buildstate:
- **10**: Architectural changes, major dependencies
- **7-9**: Feature additions, significant refactoring
- **4-6**: Bug fixes, minor enhancements
- **1-3**: Documentation, style changes

### 3. Explicit Approvals
Always require LLM to:
- Present full assessment first
- Ask for specific approval
- List what will be implemented
- Confirm before proceeding

### 4. Iterative Implementation
For multiple high-impact changes:
- Approve one at a time
- Verify each before moving to next
- Update buildstate after completion

---

## Troubleshooting

### No Changes Detected
**Problem**: `scf_load_project.py` shows "No recent changes"

**Solutions**:
- Check `since_hours` parameter (may be too short)
- Verify dates in buildstate.json are in `YYYY-MM-DD` format
- Ensure decisions have `date` field
- Check that buildstate.json exists (not just .scf/buildstate.library.json)

### Changes Not Showing
**Problem**: Recent decisions missing from notification

**Solutions**:
- Verify decision has `date` field matching today
- Check impact score is set
- Ensure decision is in main `buildstate.json`, not library file
- Run with `--since-hours 0` to see all decisions

### Prompt Too Long
**Problem**: Generated prompt exceeds context limits

**Solutions**:
- Use `--changes-only` to skip full context
- Reduce `since_hours` to shorter time window
- Implement multiple sessions for different change types

---

## Future Enhancements

### Planned Features
- 🔄 **Change categories**: Group by type (architecture, features, bugs)
- 🔄 **Dependency graphs**: Show what depends on what
- 🔄 **Risk scoring**: Automated risk level calculation
- 🔄 **Team notifications**: Slack/email alerts for high-impact changes
- 🔄 **Change history**: Track what was reviewed and when
- 🔄 **Auto-prioritization**: ML-based priority suggestions

### Integration Opportunities
- GitHub Actions integration for PR reviews
- VS Code extension with change notifications
- Slack bot for team updates
- Email digests of pending changes

---

## Related Documentation

- [GitHub Copilot Integration](./GITHUB_COPILOT_INTEGRATION.md)
- [SCF LLM Integration Guide](./SCF_LLM_Integration_Guide.md)
- [SCF Core Tenants](./SCF_CORE_TENANTS.md)
- [Session Resume](../SESSION_RESUME.md)

---

**Summary**: The Change Notification System ensures LLMs never miss important updates and always assess risks before implementing changes. It's the safety net for rapid development with AI assistance. 🛡️
