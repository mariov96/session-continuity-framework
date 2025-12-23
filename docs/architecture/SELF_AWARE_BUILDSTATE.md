# Self-Aware Buildstate Protocol

**Status**: ✅ COMPLETE  
**Date**: 2025-11-10  
**Purpose**: Enable buildstate files to detect when "another AI" made changes and trigger automatic review

---

## Problem Statement

When multiple AI sessions work on a project (or you switch between LLMs), each AI needs to know:
- Did another AI modify this project?
- What changed since I last worked on it?
- Should I review changes before implementing anything?

**Without external scripts**, the buildstate files themselves should be "self-aware" and trigger reviews.

---

## Solution: Self-Aware Buildstate

Buildstate files now track session state and automatically detect when another AI has made changes.

### How It Works

1. **Session Tracking** - Each AI logs its session ID when it opens buildstate
2. **Change Detection** - Next AI sees "last modified by different session" → triggers review
3. **Auto-Review Prompt** - Instructions embedded in buildstate.md guide the AI
4. **No External Scripts Required** - Works by reading buildstate files alone

---

## Implementation

### 1. Session State Tracking (buildstate.json)

Added `_session_state` object to track who modified the project:

```json
{
  "_session_state": {
    "last_session_id": "claude-session-001",
    "last_modified_by": "Claude-2025-11-10T10:00",
    "last_modified_at": "2025-11-10T10:00:00.000000",
    "session_count": 5,
    "requires_review": true,
    "review_reason": "Added GitHub Copilot integration"
  }
}
```

### 2. AI Rules with Self-Awareness (buildstate.json)

Enhanced `ai_rules` section with self-awareness protocol:

```json
{
  "ai_rules": {
    "session_start_protocol": "CRITICAL - Check _session_state first!",
    "self_awareness": {
      "check_session_state": "Read _session_state.last_modified_by on every session start",
      "detect_changes": "If last_modified_by != YOUR_SESSION_ID → another AI made changes",
      "trigger_review": "When changes detected → assess decisions[], next_steps[], features[]",
      "impact_assessment": "For HIGH IMPACT decisions (7+/10) → identify risks, dependencies",
      "approval_required": "DO NOT implement until user approves",
      "update_state": "Set _session_state with your session_id, timestamp",
      "mark_review": "Set requires_review=true before closing if significant changes"
    }
  }
}
```

### 3. Instructions in buildstate.md

Added prominent "AI Session Instructions - READ FIRST!" section:

```markdown
## 🤖 AI Session Instructions - READ FIRST!

### Self-Aware Buildstate Protocol

**Before proceeding with any work:**

1. **Check Session State** (in `buildstate.json` → `_session_state`):
   - Look at `last_modified_by` and `last_modified_at`
   - Check if `requires_review` is `true`

2. **If Another AI Modified This Project:**
   IF last_modified_by != YOUR_SESSION_ID AND last_modified_by != null:
      → STOP and trigger change review
      → Read all decisions[] added since last_modified_at
      → Assess impact and risks
      → Request user approval before implementing
```

---

## Usage

### For AI Sessions (Within Project)

**Automatic** - Just read buildstate.md first:

1. AI opens project
2. Reads buildstate.md → sees "AI Session Instructions - READ FIRST!"
3. Checks `_session_state` in buildstate.json
4. If another AI modified → triggers review automatically
5. No external scripts needed!

### For Users (With SCF Scripts)

**Enhanced** - Use scf_load_project.py with self-aware mode:

```bash
# Self-aware mode: automatically checks session state
python3 scf_load_project.py /path/to/project --self-aware --ai-name="Copilot"

# Update session state after loading
python3 scf_load_project.py /path/to/project --self-aware --update-state

# Specify custom session ID
python3 scf_load_project.py /path/to/project --self-aware --session-id="my-session-01"
```

### Programmatic Usage

```python
from scf_llm_integration import SCFLLMIntegrator
from pathlib import Path

# Initialize
integrator = SCFLLMIntegrator(Path('/path/to/project'))

# Check session state
state = integrator.check_session_state()
if state['requires_review']:
    print(f"⚠️ Review required: {state['review_reason']}")

# Generate self-aware context
context = integrator.generate_self_aware_context(
    session_id="my-session-123",
    ai_name="Claude"
)
print(context)

# Update session state at end
integrator.update_session_state(
    session_id="my-session-123",
    modified_by="Claude-2025-11-10T15:30",
    requires_review=True,
    review_reason="Implemented new features X, Y, Z"
)
```

---

## Workflow Example

### Scenario: Claude → Copilot Handoff

**Day 1 - Claude's Session:**

1. Claude opens project
2. Reads buildstate.md → First session, no prior changes
3. Implements GitHub Copilot integration
4. Before closing, updates session state:
   ```json
   {
     "_session_state": {
       "last_session_id": "claude-001",
       "last_modified_by": "Claude-2025-11-10T10:00",
       "last_modified_at": "2025-11-10T10:00:00",
       "session_count": 1,
       "requires_review": true,
       "review_reason": "Added GitHub Copilot integration and change notification system"
     }
   }
   ```

**Day 2 - Copilot's Session:**

1. Copilot opens project
2. Reads buildstate.md → Sees "Check Session State" instruction
3. Checks `_session_state`:
   - `last_modified_by`: "Claude-2025-11-10T10:00"
   - `requires_review`: true
4. **Triggers automatic review:**
   ```markdown
   ⚠️ ATTENTION: Changes detected from another AI session!
   
   Another AI (Claude) modified this project on 2025-11-10.
   
   ## Changes Found:
   - New decisions: 2 (High Impact: 1)
   - Reason: Added GitHub Copilot integration and change notification system
   
   ## Impact Assessment Required
   [Detailed review prompt]
   ```
5. Copilot assesses risks and asks for approval
6. User confirms → Copilot proceeds

---

## API Reference

### check_session_state()

Check if another AI session modified the project.

**Returns:**
```python
{
    'last_session_id': str or None,
    'last_modified_by': str or None,  # e.g., "Claude-2025-11-10T10:00"
    'last_modified_at': str or None,  # ISO timestamp
    'session_count': int,
    'requires_review': bool,
    'review_reason': str or None,
    'is_first_session': bool,
    'message': str  # Human-readable status
}
```

**Example:**
```python
state = integrator.check_session_state()
if state['requires_review']:
    print(f"⚠️ {state['review_reason']}")
```

### update_session_state()

Update session state after AI session (marks who modified buildstate).

**Parameters:**
- `session_id` (str): Unique session identifier
- `modified_by` (str): AI name and timestamp (e.g., "Claude-2025-11-10T14:30")
- `requires_review` (bool): Set true if significant changes made
- `review_reason` (str, optional): Brief description of changes

**Returns:** bool (success/failure)

**Example:**
```python
integrator.update_session_state(
    session_id="my-session-123",
    modified_by="GPT-4-2025-11-10T15:00",
    requires_review=True,
    review_reason="Refactored authentication system"
)
```

### generate_self_aware_context()

Generate context with self-awareness check (main entry point).

**Parameters:**
- `session_id` (str): Current AI session ID
- `ai_name` (str): Name of current AI (e.g., "Claude", "GPT-4", "Copilot")

**Returns:** str (formatted context with change notifications if needed)

**Example:**
```python
context = integrator.generate_self_aware_context(
    session_id="copilot-session-456",
    ai_name="GitHub Copilot"
)
print(context)
```

---

## CLI Reference

### scf_load_project.py --self-aware

**Synopsis:**
```bash
python3 scf_load_project.py PROJECT_PATH --self-aware [OPTIONS]
```

**Options:**
- `--self-aware` - Enable self-aware protocol (checks session state)
- `--ai-name NAME` - Name of AI (default: "AI")
- `--session-id ID` - Unique session ID (auto-generated if not provided)
- `--update-state` - Update session state after loading
- `--output FILE` - Save output to file

**Examples:**
```bash
# Basic self-aware load
python3 scf_load_project.py my-project --self-aware

# Specify AI name
python3 scf_load_project.py my-project --self-aware --ai-name="Claude"

# Update session state
python3 scf_load_project.py my-project --self-aware --update-state

# Custom session ID
python3 scf_load_project.py my-project --self-aware --session-id="sprint-23"

# Save to file
python3 scf_load_project.py my-project --self-aware --output context.md
```

---

## Benefits

### 🎯 True Portability
- **No external dependencies** - Buildstate files are self-contained
- **Works everywhere** - Any AI can detect changes by reading the files
- **Simple adoption** - Just read buildstate.md first

### 🛡️ Automatic Safety
- **Prevents conflicts** - AIs know when others have modified the project
- **Forces review** - High-impact changes must be assessed
- **Audit trail** - Complete history of who modified what

### 🔄 Multi-AI Collaboration
- **Seamless handoffs** - Switch between Claude, GPT, Copilot, etc.
- **Context preservation** - Each AI knows what the previous AI did
- **Coordinated updates** - No surprises or overlooked changes

### 💡 Zero Configuration
- **Automatic detection** - Just read buildstate files
- **Embedded instructions** - Protocol lives in the files themselves
- **Universal compatibility** - Works with any LLM that reads the files

---

## Comparison: With vs Without Scripts

### Without Scripts (Pure Buildstate)
**AI just reads files:**
1. Opens project
2. Reads buildstate.md → Sees "Check Session State" instruction
3. Manually checks `_session_state` in buildstate.json
4. If another AI modified → follows embedded review protocol
5. Manually updates `_session_state` before closing

**Pros:**
- ✅ No external dependencies
- ✅ Works anywhere buildstate files exist
- ✅ True portability

**Cons:**
- ⚠️ Relies on AI following instructions correctly
- ⚠️ Manual session state updates
- ⚠️ More prone to human/AI error

### With Scripts (scf_load_project.py)
**User runs script:**
```bash
python3 scf_load_project.py my-project --self-aware --ai-name="Copilot"
```

**Pros:**
- ✅ Automatic session state checking
- ✅ Structured output format
- ✅ Reliable state updates
- ✅ Better error handling

**Cons:**
- ⚠️ Requires SCF repository
- ⚠️ External script dependency

### Recommendation: Use Both!
- **Within project** (no scripts): AI reads buildstate.md first
- **From SCF repo** (with scripts): Use scf_load_project.py --self-aware

This gives you:
- Portability (works without scripts)
- Reliability (enhanced with scripts)
- Flexibility (choose based on context)

---

## Integration with Existing Systems

### Works With:
- ✅ init_scf.py - Templates include `_session_state`
- ✅ update_scf.py - Can update session state
- ✅ GitHub Copilot - Reads ai_rules and buildstate.md
- ✅ All LLMs - Universal protocol

### Updates to Templates:
- ✅ buildstate.json template includes `_session_state`
- ✅ buildstate.md template includes "AI Session Instructions"
- ✅ Both templates have self-awareness protocol

---

## Best Practices

### For AI Sessions:
1. **Always read buildstate.md first** - Before doing anything else
2. **Check session state** - Look at `_session_state` in buildstate.json
3. **Trigger review if needed** - Follow protocol if another AI modified
4. **Update state before closing** - Mark yourself as last modifier
5. **Set requires_review** - If you made significant changes

### For Users:
1. **Use --self-aware mode** - When loading projects with scf_load_project.py
2. **Specify AI name** - Makes audit trail clearer
3. **Review change notifications** - Don't skip impact assessments
4. **Update templates** - Ensure new projects have self-awareness

### For Multi-AI Teams:
1. **Clear session IDs** - Use descriptive names (e.g., "sprint-23-claude")
2. **Descriptive review reasons** - Help next AI understand what changed
3. **Consistent AI names** - Use standard names (Claude, GPT-4, Copilot)
4. **Regular reviews** - Check session history periodically

---

## Troubleshooting

### Problem: AI doesn't see changes
**Solution:** Ensure buildstate.md is read first. The instructions are at the top.

### Problem: Session state not updating
**Solution:** Use `--update-state` flag or manually update `_session_state` in buildstate.json

### Problem: False positives (always showing review)
**Solution:** Set `requires_review: false` after completing review

### Problem: Missing session history
**Solution:** Increment `session_count` to track total sessions

---

## Future Enhancements

### Planned:
- 🔄 Session diff viewer (show exactly what changed between sessions)
- 🔄 Multi-AI conflict resolution (handle simultaneous edits)
- 🔄 Session replay (review entire session history)
- 🔄 Automatic review summaries (AI generates session summaries)
- 🔄 Team dashboard (visualize who's working on what)

### Integration Opportunities:
- Git hooks to update session state on commit
- VS Code extension with session state visualization
- Slack notifications when AI sessions modify projects
- Web dashboard for session history

---

## Related Documentation

- [Change Notification System](./CHANGE_NOTIFICATION_SYSTEM.md)
- [GitHub Copilot Integration](./GITHUB_COPILOT_INTEGRATION.md)
- [SCF Core Tenants](./SCF_CORE_TENANTS.md)
- [Session Resume](../SESSION_RESUME.md)

---

**Summary**: Self-Aware Buildstate makes SCF truly portable. The intelligence lives in the files themselves, not external scripts. Any AI can detect changes from any other AI, just by reading buildstate files. 🧠✨
