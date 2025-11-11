# SCF Status Check & Phone Home Guide

## Overview

This guide explains how AI assistants and users can quickly verify if a project is up-to-date with the latest Session Continuity Framework (SCF) capabilities, and how to automatically sync when out of date.

## Core Concepts

### 1. Self-Checking Intelligence

Every SCF-enabled project contains the intelligence to check its own compliance status. This is embedded in:
- `buildstate.json` → `ai_rules.scf_status_check`
- `buildstate.md` → "🔍 SCF Status Check" section
- `_scf_metadata` → Contains SCF home path for phone home

### 2. The 5 Key Features

SCF status is based on presence of 5 core capabilities:

1. **Self-aware buildstate** (`_session_state` in buildstate.json)
   - Tracks which AI modified project last
   - Enables cross-AI coordination
   - Prevents conflicting changes

2. **AI self-awareness rules** (`ai_rules.self_awareness` in buildstate.json)
   - Protocol for change detection
   - Impact assessment workflow
   - Approval gates for high-impact changes

3. **AGENTS.md compatibility** (symlink to buildstate.md)
   - Works with agents.md ecosystem
   - Enables multi-AI workflows
   - Provides strategic context

4. **GitHub Copilot integration** (`.github/copilot-instructions.md`)
   - Custom instructions for Copilot
   - Path-specific context
   - Prompt files for common tasks

5. **Inheritance chain** (`.scf/buildstate.library.json`)
   - 4-level inheritance system
   - Local overrides without conflicts
   - Framework-level defaults

### 3. Phone Home Capability

When a project detects it's out of date, it can "phone home" to the SCF framework repository to sync latest enhancements.

**How it works:**
1. Project reads `_scf_metadata.scf_home` to find SCF installation path
2. Runs `update_scf.py` from SCF repo on current project
3. Syncs templates, adds missing features, updates buildstate files
4. User gets confirmation of what was updated

## For AI Assistants

### Quick Status Check Prompt

When user asks: **"Check my SCF status"** or **"Am I up to date with SCF?"**

**Step 1: Run the status check**
```bash
python3 -c "import json; from pathlib import Path; bs=json.loads(Path('buildstate.json').read_text()); checks = [('_session_state' in bs, 'Self-aware buildstate'), ('self_awareness' in bs.get('ai_rules', {}), 'AI self-awareness rules'), (Path('AGENTS.md').exists(), 'AGENTS.md'), (Path('.github/copilot-instructions.md').exists(), 'GitHub Copilot'), (Path('.scf/buildstate.library.json').exists(), 'Inheritance chain')]; score = sum(1 for c, _ in checks if c); print('\n🔍 SCF Status Check:'); [print(f'├─ {name}: {\"✅\" if check else \"❌\"}') for check, name in checks]; print(f'└─ Score: {score}/5'); status = '🟢 Up to date' if score == 5 else '🟡 Needs sync' if score >= 3 else '🔴 Out of date'; print(f'\n📊 {status}')"
```

**Step 2: Interpret results**
- **5/5 (🟢 Up to date)**: All SCF features present, project is current
- **3-4/5 (🟡 Needs sync)**: Missing some features, recommend sync
- **0-2/5 (🔴 Out of date)**: Major features missing, sync required

**Step 3: If score < 5, offer phone home**

Present to user:
```
📊 SCF Status: 3/5 - 🟡 Needs sync

Missing features:
❌ GitHub Copilot integration
❌ Inheritance chain

Would you like me to sync with the latest SCF enhancements? This will:
- Add missing features
- Update buildstate files
- Generate GitHub Copilot instructions
- Create AGENTS.md symlink

Run this command:
python3 /home/mario/projects/session-continuity-framework/update_scf.py $(pwd)
```

### Embedded in AI Rules

The status check is already embedded in `ai_rules.scf_status_check`. AIs should:

1. **On session start**: Check if user mentions "status", "up to date", "SCF check"
2. **On user request**: Run the quick command
3. **If low score**: Offer to run update_scf.py
4. **After sync**: Re-run check to verify 5/5

## For Users

### Manual Status Check

```bash
# Navigate to your project
cd /path/to/your/project

# Run status check
python3 -c "import json; from pathlib import Path; bs=json.loads(Path('buildstate.json').read_text()); checks = [('_session_state' in bs, 'Self-aware buildstate'), ('self_awareness' in bs.get('ai_rules', {}), 'AI self-awareness rules'), (Path('AGENTS.md').exists(), 'AGENTS.md'), (Path('.github/copilot-instructions.md').exists(), 'GitHub Copilot'), (Path('.scf/buildstate.library.json').exists(), 'Inheritance chain')]; score = sum(1 for c, _ in checks if c); print('\n🔍 SCF Status Check:'); [print(f'├─ {name}: {\"✅\" if check else \"❌\"}') for check, name in checks]; print(f'└─ Score: {score}/5'); status = '🟢 Up to date' if score == 5 else '🟡 Needs sync' if score >= 3 else '🔴 Out of date'; print(f'\n📊 {status}')"
```

### Phone Home to Sync

If status check shows < 5/5, sync with SCF:

```bash
# Auto-detect SCF home from buildstate.json and sync
python3 $(cat buildstate.json | python3 -c 'import sys,json; print(json.load(sys.stdin)["_scf_metadata"]["scf_home"])')/update_scf.py $(pwd)

# Or if you know SCF path:
python3 /home/mario/projects/session-continuity-framework/update_scf.py $(pwd)
```

### Simple AI Prompt

Just ask your AI assistant:
- "Check my SCF status"
- "Am I up to date with SCF?"
- "Run SCF health check"

The AI will run the check and offer to sync if needed.

## What Gets Synced

When you phone home to sync, `update_scf.py` will:

1. **Update buildstate files**
   - Add `_session_state` if missing
   - Add `_scf_metadata` if missing
   - Add `ai_rules.self_awareness` if missing
   - Add `ai_rules.scf_status_check` if missing

2. **Create AGENTS.md**
   - Symlink to buildstate.md
   - Enables agents.md ecosystem

3. **Generate GitHub Copilot files**
   - `.github/copilot-instructions.md` (main instructions)
   - `.github/copilot-instructions/src.md` (path-specific)
   - `.github/copilot-prompts/*.md` (common tasks)

4. **Set up inheritance chain**
   - Create `.scf/buildstate.library.json`
   - Link to framework templates
   - Enable local overrides

5. **Update AI rules**
   - Latest self-awareness protocol
   - Embedded status check capability
   - Phone home instructions

## Implementation Details

### _scf_metadata Structure

```json
{
  "_scf_metadata": {
    "scf_home": "/home/mario/projects/session-continuity-framework",
    "scf_version": "v2.1.0",
    "last_sync_date": "2025-11-10T18:30:00Z",
    "last_sync_from": "update_scf.py",
    "sync_status": "complete",
    "features_available": [
      "self_aware_buildstate",
      "github_copilot_integration", 
      "agents_md_compatibility",
      "inheritance_chain",
      "change_notifications"
    ],
    "phone_home_command": "python3 /home/mario/projects/session-continuity-framework/update_scf.py {project_path}",
    "health_check_command": "python3 -c \"import json; from pathlib import Path; bs=json.loads(Path('buildstate.json').read_text()); print('SCF Status:', '✅ Self-aware' if '_session_state' in bs else '❌ Needs update'); print('Copilot:', '✅' if Path('.github/copilot-instructions.md').exists() else '❌'); print('AGENTS.md:', '✅' if Path('AGENTS.md').exists() else '❌')\""
  }
}
```

### ai_rules.scf_status_check Structure

```json
{
  "ai_rules": {
    "scf_status_check": {
      "description": "Self-check to verify if this project has latest SCF capabilities",
      "user_prompt": "User can ask: 'Check my SCF status' or 'Am I up to date with SCF?'",
      "what_to_check": [
        "✓ _session_state exists in buildstate.json",
        "✓ self_awareness rules exist in ai_rules",
        "✓ AGENTS.md file exists (symlink to buildstate.md)",
        "✓ .github/copilot-instructions.md exists",
        "✓ .scf/buildstate.library.json exists (inheritance chain)"
      ],
      "scoring": "Count features present: 5/5 = 🟢 Up to date | 3-4/5 = 🟡 Needs sync | 0-2/5 = 🔴 Out of date",
      "quick_command": "python3 -c \"import json; from pathlib import Path; bs=json.loads(Path('buildstate.json').read_text()); checks = [('_session_state' in bs, 'Self-aware buildstate'), ('self_awareness' in bs.get('ai_rules', {}), 'AI self-awareness rules'), (Path('AGENTS.md').exists(), 'AGENTS.md'), (Path('.github/copilot-instructions.md').exists(), 'GitHub Copilot'), (Path('.scf/buildstate.library.json').exists(), 'Inheritance chain')]; score = sum(1 for c, _ in checks if c); print('\\n🔍 SCF Status Check:'); [print(f\\\"├─ {name}: {'✅' if check else '❌'}\\\" for check, name in checks]; print(f'└─ Score: {score}/5'); status = '🟢 Up to date' if score == 5 else '🟡 Needs sync' if score >= 3 else '🔴 Out of date'; print(f'\\n📊 {status}')\"",
      "phone_home_on_low_score": {
        "trigger": "If score < 5/5",
        "action": "Sync with latest SCF enhancements",
        "command_template": "python3 {scf_home}/update_scf.py {project_path}",
        "scf_home_from": "_scf_metadata.scf_home",
        "auto_sync": "python3 $(cat buildstate.json | python3 -c 'import sys,json; print(json.load(sys.stdin)[\"_scf_metadata\"][\"scf_home\"])')/update_scf.py $(pwd)"
      }
    }
  }
}
```

## Use Cases

### Use Case 1: User Asks for Status

**User:** "Check my SCF status"

**AI Response:**
```bash
🔍 SCF Status Check:
├─ Self-aware buildstate: ✅
├─ AI self-awareness rules: ✅
├─ AGENTS.md: ❌
├─ GitHub Copilot: ❌
├─ Inheritance chain: ✅
└─ Score: 3/5

📊 🟡 Needs sync

You're missing:
- AGENTS.md (enables agents.md ecosystem)
- GitHub Copilot integration (custom instructions)

Would you like me to sync with SCF? Run:
python3 /home/mario/projects/session-continuity-framework/update_scf.py $(pwd)
```

### Use Case 2: AI Detects Low Score Proactively

**AI (on session start):**
```
I notice this project is at 2/5 on SCF compliance. You're missing several important features:

❌ Self-aware buildstate (_session_state)
❌ AI self-awareness rules
❌ AGENTS.md
✅ GitHub Copilot integration
❌ Inheritance chain

📊 🔴 Out of date

I recommend syncing with the latest SCF enhancements. This will enable:
- Cross-AI coordination (prevent conflicting changes)
- Automatic change detection and review
- Multi-AI workflow support

Run: python3 /home/mario/projects/session-continuity-framework/update_scf.py $(pwd)

Shall I proceed with the sync?
```

### Use Case 3: After Major SCF Update

When SCF framework adds new features:

1. User runs status check on existing projects
2. Projects show lower scores (new features missing)
3. Phone home syncs latest templates
4. All projects get new capabilities automatically

## Benefits

### For Users
- **Simple verification**: One command to check project status
- **Automatic sync**: Phone home to get latest features
- **No manual updates**: SCF updates propagate automatically
- **Version control**: Track SCF version in _scf_metadata

### For AI Assistants  
- **Self-diagnostic**: Can check own capabilities
- **Proactive updates**: Recommend sync when needed
- **Embedded intelligence**: No external dependencies
- **Clear prompts**: "Check my SCF status" just works

### For Framework Evolution
- **Easy deployment**: New features sync to all projects
- **Version tracking**: Know which projects need updates
- **Backwards compatible**: Old projects work, just missing new features
- **Incremental adoption**: Users update when ready

## Next Steps

1. **Try it now**: Run status check on your project
2. **Sync if needed**: Phone home to get latest features
3. **Add to workflow**: Make it part of session start
4. **Share with team**: Everyone can verify SCF compliance

## Related Documentation

- [SCF_LLM_Integration_Guide.md](SCF_LLM_Integration_Guide.md) - Full LLM integration details
- [SCF_CORE_TENANTS.md](SCF_CORE_TENANTS.md) - Framework principles
- [SCF_New_User_Guide.md](SCF_New_User_Guide.md) - Getting started with SCF
- [REPOSITORY_STRUCTURE.md](REPOSITORY_STRUCTURE.md) - Project layout

---

**Remember**: Every SCF-enabled project has the intelligence to check itself and phone home for updates. No external scripts required - it's all embedded in the buildstate files.
