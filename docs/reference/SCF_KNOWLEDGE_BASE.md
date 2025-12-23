# SCF Knowledge Base - External Framework Tracking

## Purpose
Track competitive and complementary frameworks to continuously learn and improve SCF.
This KB enables periodic checks for new features, patterns, and innovations we can adopt.

## User's Active Toolchain (Priority Tracking)
**Primary Tools in Daily Use**:
- ✅ VS Code with Copilot Chat
- ✅ Cline (VS Code extension + CLI)
- ✅ Claude Code (Anthropic)
- ✅ Codex (OpenAI)
- ✅ GitHub Copilot

**Not Currently Used** (Lower priority tracking):
- ⏸️ Cursor IDE
- ⏸️ Zed Editor  
- ⏸️ Aider

---

## Tracked Frameworks

### VS Code + GitHub Copilot
**URL**: https://code.visualstudio.com/  
**Copilot Docs**: https://docs.github.com/en/copilot  
**Last Checked**: 2025-11-10 ✅ **DEEP DIVE COMPLETED**  
**Current Status**: Active daily use  
**Next Check**: 2025-12-10 (monthly - HIGH PRIORITY)

**Key Features**:
- Copilot Chat for conversational coding
- Inline suggestions and completions
- Coding agent for autonomous tasks
- **Custom Instructions** - Personal, Repository, Organization levels
- **AGENTS.md Support** - Full compatibility in Copilot Chat
- **Prompt Files** (`.prompt.md`) - Reusable workflow templates
- Extension ecosystem

**Custom Instructions System** (Critical Discovery):
1. **Personal instructions** - User-level preferences (GitHub.com only)
2. **Path-specific** - `.github/instructions/**/NAME.instructions.md` (per-directory context)
3. **Repository-wide** - `.github/copilot-instructions.md` (all Copilot features)
4. **AGENTS.md** - Lowest precedence but fully supported in Copilot Chat

**Precedence Order**:
```
Personal > Path-specific > .github/copilot-instructions.md > AGENTS.md > Organization
```

**What We Should Leverage**:
- ✅ **AGENTS.md** - Already implemented via symlink
- 🔥 **`.github/copilot-instructions.md`** - Generate from buildstate (HIGH VALUE)
- 🔥 **Path-specific instructions** - Generate from component/module context
- 🔥 **Prompt files** - SCF workflow templates (`scf-init.prompt.md`, `scf-update.prompt.md`)
- 🔄 VS Code extension for SCF (commands, status bar, quick actions)
- 🔄 Command palette integration (init/update SCF)
- 🔄 Workspace recommendations for SCF setup

**Immediate Integration Plan**:
1. **Generate `.github/copilot-instructions.md`** from buildstate
   - Project overview, folder structure, coding standards, tools/frameworks
   - Updates automatically with buildstate changes
   - 4000 char limit for code review, unlimited for Chat
2. **Create path-specific instructions** for key directories
   - `/src` → language/framework-specific rules
   - `/tests` → testing conventions and patterns
   - `/docs` → documentation standards
3. **Build prompt file library**:
   - `scf-init.prompt.md` - Initialize new project with SCF
   - `scf-update.prompt.md` - Update existing project
   - `scf-feature.prompt.md` - Add feature with context tracking
   - `scf-debug.prompt.md` - Debug with buildstate history

**Integration Opportunities**:
- ✅ AGENTS.md symlink (already working)
- 🔥 `.github/copilot-instructions.md` auto-generation (HIGH PRIORITY)
- 🔥 Path-specific instructions for modules (MEDIUM PRIORITY)
- 🔥 Prompt file templates for SCF workflows (MEDIUM PRIORITY)
- Extension for command palette and status bar (FUTURE)

**Version Tracking**:
- Watch for: Prompt files GA (currently preview), new instruction types
- Monitor: VS Code releases, Copilot changelog, custom instructions API
- Track: Extension API changes, context injection improvements

---

### Cline (VS Code Extension + CLI)
**GitHub**: https://github.com/cline/cline  
**Last Checked**: 2025-11-10  
**Current Status**: Active daily use  
**Next Check**: 2025-12-10 (monthly - HIGH PRIORITY)

**Key Features**:
- Terminal and VS Code integration
- CLI for automation
- Context-aware assistance
- File detection patterns

**What We Should Leverage**:
- 🔄 TODO: Check if Cline supports .clinerules (it should per Zed docs)
- ✅ AGENTS.md compatible (should work)
- 🔄 TODO: CLI integration for SCF workflows
- 🔄 TODO: Buildstate context injection

**Integration Opportunities**:
- .clinerules → AGENTS.md symlink (if supported)
- CLI commands for SCF operations
- Context injection from buildstate
- Workflow automation hooks

**Version Tracking**:
- Watch for: New rules file support, CLI features
- Monitor: GitHub releases
- Track: Context handling improvements

---

### Claude Code (Anthropic)
**URL**: https://claude.ai/  
**Last Checked**: 2025-11-10  
**Current Status**: Active daily use  
**Next Check**: 2025-12-10 (monthly - HIGH PRIORITY)

**Key Features**:
- Desktop application for coding
- Projects with custom knowledge
- Artifact generation
- Multi-file context handling

**What We Should Leverage**:
- 🔄 TODO: Project-level buildstate integration
- 🔄 TODO: Custom instructions from buildstate
- ✅ XML context format optimization (already done)
- 🔄 TODO: Artifact generation with SCF templates

**Integration Opportunities**:
- Project setup with buildstate as knowledge base
- Custom instructions generated from ai_rules
- Automatic context injection workflow
- Template generation for new projects

**Version Tracking**:
- Watch for: Desktop app features, Projects API
- Monitor: Anthropic blog and changelog
- Track: Context window increases, artifact improvements

---

### Codex (OpenAI)
**GitHub**: https://github.com/openai/codex  
**Last Checked**: 2025-11-10  
**Current Status**: Active daily use  
**Next Check**: 2025-12-10 (monthly - HIGH PRIORITY)

**Key Features**:
- CLI tool for AI coding agents
- Supports AGENTS.md (originator of standard!)
- General-purpose tooling
- Rust-based performance

**What We Should Leverage**:
- ✅ AGENTS.md support (fully compatible!)
- 🔄 TODO: Direct SCF integration hooks
- 🔄 TODO: Buildstate context loading
- 🔄 TODO: CLI workflow automation

**Integration Opportunities**:
- Natural AGENTS.md compatibility
- CLI commands for SCF operations
- Context injection pipelines
- Rust-based SCF utilities (future)

**Version Tracking**:
- Watch for: New features, file format support
- Monitor: GitHub releases, OpenAI announcements
- Track: Community adoption patterns

---

### agents.md Ecosystem
**URL**: https://agents.md/  
**Last Checked**: 2025-11-10  
**Current Status**: v1.0 (20,000+ projects using it)  
**Next Check**: 2025-12-10 (monthly)

**Key Features**:
- Static instruction file standard
- Universal ecosystem adoption
- 8 compatible file names (Zed editor)
- Aider, Cursor, Gemini CLI support

**What We Learned**:
- Symlink strategy for AGENTS.md → buildstate.md
- Ecosystem compatibility is critical
- Static files have massive adoption potential

**What We Could Adopt**:
- ✅ Implemented AGENTS.md generation (done 2025-11-10)
- ✅ Implemented automatic symlink creation (done 2025-11-10)
- Consider: Community-contributed conventions repository pattern

**Version Tracking**:
- Watch for: AGENTS.md v2.0, new supported tools
- Monitor GitHub: https://github.com/openai/agents.md
- Check community: https://github.com/Aider-AI/conventions

---

### AG2.ai (AutoGen)
**URL**: https://ag2.ai/  
**GitHub**: https://github.com/ag2ai/ag2  
**Last Checked**: 2025-11-10  
**Current Version**: v0.10.0  
**Next Check**: When v0.11.0 releases OR 2025-12-10

**Key Features**:
- Multi-agent orchestration
- Built-in conversation patterns
- Human-AI collaboration modes
- Group chat with dynamic speaker selection
- Sequential chats with context carryover

**What We Learned**:
- Real-time agent collaboration is valuable
- Conversation patterns can be standardized
- Human intervention points are important

**What We Could Adopt**:
- Consider: AG2 runtime integration with SCF context
- Consider: Multi-agent patterns for complex tasks
- Consider: Sequential chat with buildstate context carryover
- Future: SCF + AG2 hybrid architecture

**Version Tracking**:
- Watch for: New conversation patterns, marketplace launch
- Monitor releases: https://github.com/ag2ai/ag2/releases
- Community: https://discord.gg/pAbnFJrkgZ (20k+ members)

---

### Cursor IDE
**URL**: https://cursor.com/  
**Last Checked**: 2025-11-10  
**Current Version**: 2.0  
**Next Check**: 2026-02-10 (quarterly - LOWER PRIORITY)
**User Status**: ⏸️ Not currently used

**Key Features**:
- Agent mode, Tab autocomplete, .cursorrules support

**Tracking Rationale**: Monitor for innovations but lower priority since not in active toolchain.

---

### Zed Editor
**URL**: https://zed.dev/  
**Last Checked**: 2025-11-10  
**Next Check**: 2026-02-10 (quarterly - LOWER PRIORITY)
**User Status**: ⏸️ Not currently used

**Key Features**:
- 8 supported rules files, built-in rules library

**Tracking Rationale**: Documented 8 filename priority useful, but lower priority for integration.

---

### Aider
**URL**: https://aider.chat/  
**Last Checked**: 2025-11-10  
**Next Check**: 2026-02-10 (quarterly - LOWER PRIORITY)
**User Status**: ⏸️ Not currently used

**Key Features**:
- Terminal-based AI pair programming, CONVENTIONS.md support

**Tracking Rationale**: Community patterns valuable but lower priority for direct integration.

---

## Check Schedule

### High Priority - Monthly Checks (10th of each month)
**User's Active Toolchain**:
- ✅ VS Code + GitHub Copilot
- ✅ Cline (extension + CLI)
- ✅ Claude Code
- ✅ Codex
- ✅ agents.md ecosystem
- ✅ AG2.ai (if no version change)

### Lower Priority - Quarterly Checks (10th every 3 months)
**Not in active use but worth monitoring**:
- ⏸️ Cursor IDE
- ⏸️ Zed Editor
- ⏸️ Aider

### Version-Triggered Checks (Immediate)
- AG2.ai: When new version released (currently v0.10.0)
- VS Code: Major releases
- GitHub Copilot: Feature announcements
- Cline: GitHub releases
- Claude Code: Anthropic announcements
- Codex: OpenAI updates

**Next Monthly Check**: 2025-12-10  
**Next Quarterly Check**: 2026-02-10

---

## Immediate Action Items (High Priority)

### 1. GitHub Copilot Instructions Generator ✅ COMPLETE
**Status**: ✅ IMPLEMENTED (2025-11-10)  
**Priority**: 🔴 CRITICAL (daily use tool with clear API)  
**Effort**: Low  
**Impact**: VERY HIGH

**Completion Summary**:
- ✅ Added `generate_copilot_instructions()` to scf_llm_integration.py
- ✅ Added `generate_path_instructions()` for directory-specific context
- ✅ Added `generate_prompt_files()` for reusable workflow templates
- ✅ Integrated into `init_scf.py` (auto-generates on project init)
- ✅ Integrated into `update_scf.py` (regenerates on update)
- ✅ Tested on test-scf-app (all files generated successfully)
- ✅ Documentation: [GITHUB_COPILOT_INTEGRATION.md](GITHUB_COPILOT_INTEGRATION.md)

**Generated Files**:
- `.github/copilot-instructions.md` - Repository-wide context
- `.github/instructions/*.instructions.md` - Path-specific guidelines
- `.github/prompts/*.prompt.md` - SCF workflow templates

**Value Delivered**: Immediate productivity boost - Copilot now reads buildstate automatically!

---

### 2. VS Code Extension for SCF
**Status**: Not started  
**Priority**: 🔴 HIGH (daily use tool)  
**Effort**: Medium  
**Impact**: HIGH

**Features**:
- Command palette: "SCF: Initialize Project", "SCF: Update Project"
- Status bar: Show SCF state, balance score
- Context menu: Right-click folder → "Initialize with SCF"
- Auto-detect buildstate files
- Syntax highlighting for buildstate.json
- IntelliSense for SCF schemas
- Quick actions in Copilot Chat

---

### 3. Cline .clinerules Support
**Status**: Needs research  
**Priority**: 🔴 HIGH (daily use tool)  
**Effort**: Low  
**Impact**: MEDIUM

**Investigation**:
- Check if Cline actually supports .clinerules
- Test AGENTS.md compatibility
- Add symlink if supported
- Document in SCF setup

---

### 4. Claude Code Projects Integration
**Status**: Not started  
**Priority**: 🔴 HIGH (daily use tool)  
**Effort**: Low  
**Impact**: HIGH

**Implementation**:
- Add buildstate.json/md to Claude Projects as knowledge
- Generate custom instructions from ai_rules
- Template for project setup instructions
- Automated knowledge sync

---

### 5. Codex Direct Integration
**Status**: Not started  
**Priority**: 🔴 HIGH (daily use tool)  
**Effort**: Low  
**Impact**: MEDIUM

**Implementation**:
- Test Codex with AGENTS.md
- CLI automation examples
- Context injection patterns
- Document best practices

---

## Integration Opportunities Matrix

| Tool | Daily Use | Priority | Integration Status | Next Action |
|------|-----------|----------|-------------------|-------------|
| **VS Code + Copilot** | ✅ Yes | 🔴 CRITICAL | ✅ **COMPLETE** | 🎉 **Production ready!** |
| Cline | ✅ Yes | 🔴 HIGH | ⚠️ Partial | Check .clinerules |
| Claude Code | ✅ Yes | 🔴 HIGH | ✅ Good | Add Projects integration |
| Codex | ✅ Yes | 🔴 HIGH | ✅ Good | Test direct integration |
| agents.md | - | 🔴 HIGH | ✅ Complete | Maintain |
| AG2.ai | - | 🟡 MEDIUM | 🔄 Future | Prototype hybrid |
| Cursor | ❌ No | 🟢 LOW | ✅ Compatible | Monitor only |
| Zed | ❌ No | 🟢 LOW | ✅ Compatible | Monitor only |
| Aider | ❌ No | 🟢 LOW | ✅ Compatible | Monitor only |

**Integration Completeness**:
- ✅ **COMPLETE**: VS Code/Copilot (native instructions + AGENTS.md + prompts), agents.md, Cursor, Zed, Aider
- ✅ **Good**: Claude Code (XML format optimized), Codex (AGENTS.md originator)
- ⚠️ **Partial**: Cline (needs .clinerules check)
- 🔄 **Future**: AG2.ai (complementary architecture)

**Major Achievement**: GitHub Copilot integration complete - #1 priority from daily-use toolchain! 🎉

---

---

## Check Procedures

### Quick Check (Monthly)
1. Visit main URL
2. Check version/changelog
3. Scan for new features
4. Update this KB with findings
5. Flag items for "What We Could Adopt"

### Deep Check (Quarterly)
1. Review full documentation
2. Analyze community feedback
3. Test integration possibilities
4. Prototype potential adoptions
5. Update SCF roadmap

### Automated Checks (Future Enhancement)
```python
# scf_kb_monitor.py
def check_framework_updates():
    frameworks = load_kb()
    for framework in frameworks:
        if should_check(framework):
            updates = fetch_updates(framework)
            if updates.has_changes():
                notify_and_update_kb(updates)
```

---

## Integration Opportunities Matrix

| Framework | SCF Integration | Priority | Effort | Impact |
|-----------|----------------|----------|--------|--------|
| agents.md | ✅ Complete | - | - | HIGH |
| AG2.ai | 🔄 Possible | MEDIUM | HIGH | HIGH |
| Cursor | 🔄 Partial | LOW | MEDIUM | MEDIUM |
| Zed | ✅ Complete | - | - | MEDIUM |
| Aider | ✅ Complete | - | - | MEDIUM |

**Legend**:
- ✅ Complete: Fully compatible
- 🔄 Possible: Feasible with effort
- ❌ Not feasible: Technical/philosophical mismatch

---

## Learning Log

### 2025-11-10: Initial Analysis
**Frameworks Analyzed**: agents.md, AG2.ai, Cursor, Zed, Aider

**Key Insights**:
1. Static instruction files (agents.md) have massive adoption
2. Multi-agent orchestration (AG2) is complementary, not competitive
3. IDE integration is critical for user experience
4. Universal compatibility > vendor lock-in
5. Community contributions accelerate ecosystem growth

**Immediate Actions Taken**:
- Implemented AGENTS.md generation
- Created automatic symlink setup
- Positioned SCF as "AGENTS.md Plus Intelligence"
- Established session portability as core tenant

**Strategic Positioning**:
- SCF = Persistent intelligence layer
- agents.md = Static instructions (compatible)
- AG2.ai = Real-time orchestration (complementary)
- Cursor/Zed/Aider = Tool compatibility (enabled)

---

## Competitive Advantages Maintained

### vs agents.md
- ✅ Dynamic intelligence vs static instructions
- ✅ Session continuity vs one-time setup
- ✅ Cross-project learning vs isolated configs
- ✅ Built-in compatibility via symlinks

### vs AG2.ai
- ✅ Persistent context vs ephemeral sessions
- ✅ Universal LLM compatibility vs framework-specific
- ✅ Ecosystem learning vs conversation-focused
- ✅ Individual productivity vs orchestration focus

### Unique SCF Value
- Only framework with persistent + portable + intelligent context
- Only system with cross-project pattern learning
- Only solution with universal LLM optimization
- Only framework with session portability as core tenant

---

## Future Watch List

### Emerging Patterns
- [ ] Model Context Protocol (MCP) adoption
- [ ] Browser-based AI assistants
- [ ] Team collaboration patterns
- [ ] RAG integration approaches
- [ ] Multi-modal context handling

### Potential Threats
- [ ] Major IDE-specific solutions (vendor lock-in risk)
- [ ] Cloud-only platforms (portability concern)
- [ ] Proprietary context formats (compatibility issue)

### Opportunities
- [ ] Open-source collaborations
- [ ] Framework integrations (AG2 + SCF)
- [ ] IDE extensions (VS Code, Cursor, Zed)
- [ ] Community ecosystem growth

---

**Maintained by**: SCF Core Development  
**Last Updated**: 2025-11-10  
**Next Review**: 2025-12-10
