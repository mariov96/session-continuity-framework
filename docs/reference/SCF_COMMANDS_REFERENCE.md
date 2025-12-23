# SCF Commands Reference - `/scf_help`

## Quick Command Reference

This guide provides all SCF commands and capabilities you can invoke to maintain sync, learn from the SCF project, rebalance, and more.

---

## 📋 Core SCF Commands

### `/scf_help`
Show this help documentation with all available commands.

```bash
# In any AI session, just say:
/scf_help
```

---

### `/scf_status` - Check SCF Compliance
Verify if current project has all SCF features and is up-to-date.

```bash
# User prompt:
/scf_status
# Or: "Check my SCF status"
# Or: "Am I up to date with SCF?"

# What it checks:
# ✓ _session_state (self-aware buildstate)
# ✓ ai_rules.self_awareness (change detection protocol)
# ✓ AGENTS.md (ecosystem compatibility)
# ✓ .github/copilot-instructions.md (Copilot integration)
# ✓ .scf/buildstate.library.json (inheritance chain)

# Output:
# 🔍 SCF Status Check:
# ├─ Self-aware buildstate: ✅
# ├─ AI self-awareness rules: ✅
# ├─ AGENTS.md: ✅
# ├─ GitHub Copilot: ✅
# └─ Inheritance chain: ✅
# Score: 5/5 - 🟢 Up to date
```

**Manual Command:**
```bash
python3 -c "import json; from pathlib import Path; bs=json.loads(Path('buildstate.json').read_text()); checks = [('_session_state' in bs, 'Self-aware buildstate'), ('self_awareness' in bs.get('ai_rules', {}), 'AI self-awareness rules'), (Path('AGENTS.md').exists(), 'AGENTS.md'), (Path('.github/copilot-instructions.md').exists(), 'GitHub Copilot'), (Path('.scf/buildstate.library.json').exists(), 'Inheritance chain')]; score = sum(1 for c, _ in checks if c); print('\n🔍 SCF Status Check:'); [print(f'├─ {name}: {\"✅\" if check else \"❌\"}') for check, name in checks]; print(f'└─ Score: {score}/5'); status = '🟢 Up to date' if score == 5 else '🟡 Needs sync' if score >= 3 else '🔴 Out of date'; print(f'\n📊 {status}')"
```

---

### `/scf_sync` - Phone Home & Update
Sync project with latest SCF enhancements from framework repository.

```bash
# User prompt:
/scf_sync
# Or: "Sync with SCF"
# Or: "Update my SCF features"

# What it does:
# • Adds missing SCF features
# • Updates buildstate templates
# • Generates GitHub Copilot files
# • Creates AGENTS.md symlink
# • Sets up inheritance chain
# • Updates _session_state and _scf_metadata

# Auto-detected command:
python3 $(cat buildstate.json | python3 -c 'import sys,json; print(json.load(sys.stdin)["_scf_metadata"]["scf_home"])')/update_scf.py $(pwd)

# Or explicit path:
python3 /home/mario/projects/session-continuity-framework/update_scf.py $(pwd)
```

---

### `/scf_session` - Check Session State
Review current session state and detect cross-AI changes.

```bash
# User prompt:
/scf_session
# Or: "Who last modified this project?"
# Or: "Check session state"

# Reads from buildstate.json → _session_state:
{
  "last_session_id": "claude-20251110-1717",
  "last_modified_by": "Claude-2025-11-10T17:22",
  "last_modified_at": "2025-11-10T17:29:45.832975",
  "session_count": 2,
  "requires_review": false,
  "review_reason": null
}

# Output shows:
# • Which AI last worked on project
# • When they made changes
# • If review is required
# • Number of AI sessions
```

**With Self-Aware Detection:**
```bash
cd /home/mario/projects/session-continuity-framework
python3 scf_load_project.py /path/to/project \
    --self-aware \
    --ai-name="YourAI" \
    --session-id="yourai-$(date +%Y%m%d-%H%M)" \
    --output /tmp/project_context.md
```

---

### `/scf_update_state` - Mark Your Session
Update session state to mark yourself as the last modifier.

```bash
# User prompt:
/scf_update_state
# Or: "Update session state for my AI"

# Command:
cd /home/mario/projects/session-continuity-framework
python3 scf_load_project.py /path/to/project \
    --update-state \
    --session-id="yourai-$(date +%Y%m%d-%H%M)" \
    --ai-name="YourAI"

# Or inline Python:
python3 << 'PYTHON'
import json
from pathlib import Path
from datetime import datetime

bs = json.loads(Path('buildstate.json').read_text())
bs['_session_state'].update({
    'last_session_id': 'yourai-20251111-1200',
    'last_modified_by': 'YourAI-2025-11-11T12:00',
    'last_modified_at': datetime.now().isoformat(),
    'session_count': bs['_session_state']['session_count'] + 1,
    'requires_review': True,  # If you made significant changes
    'review_reason': 'Implemented X, Y, Z features'
})
Path('buildstate.json').write_text(json.dumps(bs, indent=2))
print('✅ Session state updated')
PYTHON
```

---

### `/scf_rebalance` - Sync JSON ↔ MD
Synchronize buildstate.json and buildstate.md after major changes.

```bash
# User prompt:
/scf_rebalance
# Or: "Rebalance buildstate files"
# Or: "Sync JSON and MD"

# Command:
cd /home/mario/projects/session-continuity-framework
python3 scf_rebalancer.py /path/to/project

# Triggers on:
# • Major feature completion
# • Architecture changes
# • Performance milestones
# • Phase transitions
# • Large decision batches

# What it does:
# • Syncs decisions, features, next_steps
# • Updates meta.last_sync
# • Reconciles strategic (MD) ↔ technical (JSON)
```

---

### `/scf_changes` - Detect Recent Changes
Review what changed since last session and assess impact.

```bash
# User prompt:
/scf_changes
# Or: "What changed since last session?"
# Or: "Review recent decisions"

# Uses scf_llm_integration.py functions:
from scf_llm_integration import detect_recent_changes, generate_change_review_prompt

# Analyzes:
# • decisions[] array
# • features[] status changes
# • bugs[] additions
# • next_immediate[] updates
# • _session_state changes

# Generates impact assessment:
# • Change summary
# • Impact scores (0-10)
# • Risk analysis
# • User approval prompt
```

---

### `/scf_copilot` - Generate Copilot Instructions
Create or update GitHub Copilot integration files.

```bash
# User prompt:
/scf_copilot
# Or: "Generate Copilot instructions"
# Or: "Update GitHub Copilot files"

# Command:
cd /home/mario/projects/session-continuity-framework
python3 -c "from scf_llm_integration import generate_copilot_instructions, generate_path_instructions, generate_prompt_files; import json; from pathlib import Path; bs=json.loads(Path('/path/to/project/buildstate.json').read_text()); generate_copilot_instructions(bs, Path('/path/to/project')); generate_path_instructions(bs, Path('/path/to/project')); generate_prompt_files(bs, Path('/path/to/project'))"

# Generates:
# • .github/copilot-instructions.md (main)
# • .github/copilot-instructions/src.md (path-specific)
# • .github/copilot-instructions/tests.md (path-specific)
# • .github/copilot-prompts/*.md (common tasks)

# Files created:
# ├── .github/
# │   ├── copilot-instructions.md
# │   ├── copilot-instructions/
# │   │   ├── src.md
# │   │   └── tests.md
# │   └── copilot-prompts/
# │       ├── implement-feature.md
# │       ├── fix-bug.md
# │       └── write-tests.md
```

---

### `/scf_init` - Initialize SCF in New Project
Set up SCF in a new project from scratch.

```bash
# User prompt:
/scf_init
# Or: "Initialize SCF in this project"
# Or: "Set up Session Continuity Framework"

# Command:
cd /home/mario/projects/session-continuity-framework
python3 init_scf.py /path/to/new/project

# What it does:
# • Copies buildstate.json and buildstate.md templates
# • Creates _session_state
# • Generates AGENTS.md symlink
# • Sets up .scf/ directory
# • Creates inheritance chain
# • Generates GitHub Copilot files
# • Initializes _scf_metadata with paths
```

---

## 🔧 Advanced Commands

### `/scf_context` - Load Full Project Context
Generate complete project context for AI session start.

```bash
# Command:
cd /home/mario/projects/session-continuity-framework
python3 scf_load_project.py /path/to/project --output /tmp/context.md

# Includes:
# • Full buildstate.json content
# • Full buildstate.md content
# • Session state analysis
# • Recent changes summary
# • GitHub Copilot instructions
# • Inheritance chain details
```

---

### `/scf_time` - Estimate Token Usage
Intelligent token usage estimate with capacity warnings.

```bash
# User prompt:
/scf_time
# Or: "How much context have I used?"
# Or: "Am I near token limit?"

# Monitors:
# • Current token count
# • Context window capacity
# • Remaining tokens
# • Warns at 80% threshold
# • Suggests rebalance when needed
```

---

### `/scf_rules` - Show Active AI Rules
List all active AI rules and behavioral guidelines.

```bash
# User prompt:
/scf_rules
# Or: "What are my AI rules?"
# Or: "Show SCF guidelines"

# Reads from buildstate.json → ai_rules:
# • Session start protocol
# • Self-awareness rules
# • SCF status check protocol
# • Change detection workflow
# • Update requirements
# • Rebalance triggers
```

---

### `/scf_closeout` - Session End Summary
Generate updated buildstate files for session end.

```bash
# User prompt:
/scf_closeout
# Or: "End my session"
# Or: "Close out and save state"

# What it does:
# • Updates _session_state
# • Sets requires_review if needed
# • Adds review_reason
# • Syncs JSON ↔ MD
# • Creates session summary
# • Commits changes (if --auto-commit)
# • Provides handoff context for next AI
```

---

### `/scf_learn` - Learn from SCF Repository
Study SCF repository patterns and best practices.

```bash
# User prompt:
/scf_learn
# Or: "What can I learn from SCF repo?"
# Or: "Show me SCF best practices"

# Key files to study:
# • docs/SCF_CORE_TENANTS.md (9 core principles)
# • docs/SCF_LLM_Integration_Guide.md (LLM capabilities)
# • docs/SCF_STATUS_CHECK_GUIDE.md (health checks)
# • scf_llm_integration.py (implementation patterns)
# • README.md (User Acceptance Tests)

# Learn about:
# • Self-aware buildstate pattern
# • Cross-AI coordination
# • Change detection & review
# • GitHub Copilot integration
# • Inheritance chain design
# • Atomic commits pattern
# • Public/private fork strategy
```

---

## 📊 SCF Workflow Commands

### Morning Routine - Start New Session
```bash
# 1. Load project context
/scf_context

# 2. Check session state
/scf_session

# 3. Verify SCF compliance
/scf_status

# 4. If changes detected, review
/scf_changes

# 5. Update state with your session
/scf_update_state
```

---

### During Work - Maintain Sync
```bash
# Track significant changes
/scf_rules  # Review guidelines

# Check token usage
/scf_time

# After major feature
/scf_rebalance
```

---

### Evening Routine - Close Session
```bash
# 1. Rebalance if needed
/scf_rebalance

# 2. Update session state
/scf_update_state

# 3. Mark review if significant changes
# (Set requires_review: true in _session_state)

# 4. Generate closeout summary
/scf_closeout

# 5. Commit changes
git add buildstate.json buildstate.md
git commit -m "Session closeout: <summary>"
```

---

## 🔍 Diagnostic Commands

### Check SCF Installation
```bash
# Verify SCF framework is accessible
ls /home/mario/projects/session-continuity-framework/

# Check Python path
which python3

# Test SCF tools
python3 /home/mario/projects/session-continuity-framework/scf_load_project.py --help
```

---

### Verify Project Setup
```bash
# Check required files exist
ls -la buildstate.json buildstate.md AGENTS.md
ls -la .github/copilot-instructions.md
ls -la .scf/buildstate.library.json

# Validate JSON syntax
python3 -c "import json; json.load(open('buildstate.json')); print('✅ Valid JSON')"

# Check session state
python3 -c "import json; print(json.load(open('buildstate.json'))['_session_state'])"
```

---

### Troubleshoot Issues
```bash
# If /scf_status shows missing features:
/scf_sync

# If session state conflicts:
/scf_session  # Review who last modified
/scf_changes  # See what changed
# Then update or resolve conflicts

# If JSON/MD out of sync:
/scf_rebalance

# If Copilot files missing:
/scf_copilot
```

---

## 📚 Documentation Commands

### Access SCF Guides
```bash
# Core principles
cat /home/mario/projects/session-continuity-framework/docs/SCF_CORE_TENANTS.md

# LLM integration
cat /home/mario/projects/session-continuity-framework/docs/SCF_LLM_Integration_Guide.md

# Status check guide
cat /home/mario/projects/session-continuity-framework/docs/SCF_STATUS_CHECK_GUIDE.md

# New user guide
cat /home/mario/projects/session-continuity-framework/docs/SCF_New_User_Guide.md
```

---

### Quick Reference
```bash
# This help file
/scf_help

# Repository structure
cat /home/mario/projects/session-continuity-framework/docs/REPOSITORY_STRUCTURE.md

# User Acceptance Tests
cat /home/mario/projects/session-continuity-framework/README.md
# (See UAT section)
```

---

## 🎯 Common Scenarios

### Scenario 1: New Project Setup
```bash
/scf_init                    # Initialize SCF
/scf_status                  # Verify setup (should be 5/5)
/scf_update_state           # Mark your first session
```

---

### Scenario 2: Taking Over from Another AI
```bash
/scf_session                # See who last worked here
/scf_changes                # Review what they did
# AI presents change assessment
# User approves
/scf_update_state          # Mark yourself as active
```

---

### Scenario 3: Project Needs Updates
```bash
/scf_status                 # Shows 3/5 - 🟡 Needs sync
/scf_sync                   # Phone home and update
/scf_status                 # Verify: 5/5 - 🟢 Up to date
```

---

### Scenario 4: Major Feature Complete
```bash
# Feature implemented
/scf_rebalance             # Sync JSON ↔ MD
/scf_update_state          # Mark session with changes
git commit -m "feat: <feature>"  # Atomic commit
```

---

### Scenario 5: Cross-AI Handoff
```bash
# AI #1 closing session:
/scf_update_state
# Set requires_review: true
# Set review_reason: "Implemented X, Y"
/scf_closeout

# AI #2 starting session:
/scf_session               # Detects AI #1's changes
/scf_changes               # Reviews decisions
# Presents assessment
# User approves
/scf_update_state         # Marks AI #2 active
```

---

## 🛠️ For AI Assistants

### Embedded Commands in ai_rules

All these commands are embedded in `buildstate.json` → `ai_rules`:

```json
{
  "ai_rules": {
    "scf_status_check": {
      "user_prompt": "User can ask: 'Check my SCF status' or '/scf_status'"
    },
    "scf_commands": {
      "time": "Intelligent token usage estimate with capacity warnings",
      "rules": "List active rules and behavioral guidelines",
      "closeout": "Provide updated buildstate file for session end",
      "status": "Check SCF compliance (5-point scoring)",
      "sync": "Phone home and update with latest SCF features",
      "session": "Review session state and detect cross-AI changes",
      "rebalance": "Sync buildstate.json ↔ buildstate.md",
      "changes": "Detect and assess recent changes"
    }
  }
}
```

### How to Respond to Commands

When user types `/scf_*` command:

1. **Recognize the command** from ai_rules
2. **Execute appropriate action** (run script, read file, analyze state)
3. **Present results** in clear format
4. **Offer next steps** if needed

Example:
```
User: /scf_status

AI Response:
🔍 SCF Status Check:
├─ Self-aware buildstate: ✅
├─ AI self-awareness rules: ✅
├─ AGENTS.md: ❌
├─ GitHub Copilot: ✅
└─ Inheritance chain: ✅
Score: 4/5 - 🟡 Needs sync

You're missing AGENTS.md. Would you like me to sync with SCF?
Run: /scf_sync
```

---

## 📖 Quick Reference Card

```
╔══════════════════════════════════════════════════════════════╗
║                    SCF COMMANDS CHEAT SHEET                  ║
╠══════════════════════════════════════════════════════════════╣
║  /scf_help          Show this help documentation             ║
║  /scf_status        Check SCF compliance (0-5 score)         ║
║  /scf_sync          Phone home & update features             ║
║  /scf_session       Check who last modified project          ║
║  /scf_update_state  Mark your session as active              ║
║  /scf_rebalance     Sync buildstate.json ↔ buildstate.md     ║
║  /scf_changes       Review recent changes & assess impact    ║
║  /scf_copilot       Generate GitHub Copilot instructions     ║
║  /scf_init          Initialize SCF in new project            ║
║  /scf_context       Load full project context                ║
║  /scf_time          Check token usage & capacity             ║
║  /scf_rules         Show active AI rules                     ║
║  /scf_closeout      Generate session end summary             ║
║  /scf_learn         Study SCF patterns & best practices      ║
╠══════════════════════════════════════════════════════════════╣
║  📚 Full docs: /home/mario/projects/                         ║
║     session-continuity-framework/docs/                       ║
╚══════════════════════════════════════════════════════════════╝
```

---

## 🚀 Next Steps

1. **Bookmark this file** for quick reference
2. **Try commands** in your current project
3. **Add shortcuts** to your AI workflow
4. **Share with team** for consistent usage
5. **Extend commands** as needed for your workflow

---

**Remember**: These commands are embedded in every SCF-enabled project's `ai_rules`. Just ask and your AI assistant will execute them!

**For full documentation, see:**
- [SCF_LLM_Integration_Guide.md](SCF_LLM_Integration_Guide.md)
- [SCF_STATUS_CHECK_GUIDE.md](SCF_STATUS_CHECK_GUIDE.md)
- [SCF_CORE_TENANTS.md](SCF_CORE_TENANTS.md)
