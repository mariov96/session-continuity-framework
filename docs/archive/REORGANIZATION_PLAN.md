# Documentation Reorganization Plan

## Proposed Structure

```
docs/
├── guides/              # How-to guides for users
│   ├── getting-started.md         # Merge: START_HERE + New_User_Guide
│   ├── hub-operations.md          # NEW: recon, learn, teach, evolve
│   ├── spoke-integration.md       # How spokes work with hub
│   ├── llm-integration.md         # Rename: SCF_LLM_Integration_Guide
│   └── rebalancing.md             # Rename: scf_rebalancing_guide
│
├── reference/           # Technical reference
│   ├── commands.md                # Rename: SCF_COMMANDS_REFERENCE
│   ├── buildstate-spec.md         # Extract from SELF_AWARE_BUILDSTATE
│   ├── api.md                     # NEW: Python API reference
│   └── templates.md               # Template reference
│
├── architecture/        # Design & vision documents
│   ├── overview.md                # Merge: SCF_V2_VISION + CORE_TENANTS
│   ├── hub-spoke-model.md         # NEW: Hub/Spoke architecture
│   ├── inheritance.md             # Inheritance system docs
│   └── project-structure.md       # Merge: FOLDER_STRUCTURE + REPOSITORY
│
└── archive/             # Historical documents
    ├── migration-v1-v2.md         # Keep: MIGRATION_V1_TO_V2
    ├── session-notes/             # Session summaries
    └── implementation-notes/      # COMPLETE/OVERNIGHT docs
```

## Actions

### MERGE (Consolidate overlapping content)
1. START_HERE.md + SCF_New_User_Guide → guides/getting-started.md
2. SCF_V2_VISION + SCF_CORE_TENANTS → architecture/overview.md
3. SCF_FOLDER_STRUCTURE + REPOSITORY_STRUCTURE → architecture/project-structure.md

### MOVE (Relocate to correct category)
4. SCF_LLM_Integration_Guide → guides/llm-integration.md
5. scf_rebalancing_guide → guides/rebalancing.md
6. SCF_COMMANDS_REFERENCE → reference/commands.md
7. SELF_AWARE_BUILDSTATE → reference/buildstate-spec.md

### ARCHIVE (Historical value only)
8. SESSION_2025_11_10_SUMMARY → archive/session-notes/
9. IMPLEMENTATION_COMPLETE → archive/implementation-notes/
10. CLEANUP_COMPLETE → archive/implementation-notes/
11. SCF_V2_OVERNIGHT_PLAN → archive/implementation-notes/
12. MARIO_WORKFLOW_PREFERENCES → archive/ (or delete)

### DELETE (Obsolete/Redundant)
13. SCF_LLM_Enhancement_Summary (covered in llm-integration.md)
14. SCF_STATUS_CHECK_GUIDE (covered in commands.md)
15. SCF_WORKFLOW_GUIDE (covered in getting-started.md)

### CREATE NEW
16. guides/hub-operations.md - Document recon, learn, teach, evolve
17. guides/spoke-integration.md - How spokes interact with hub
18. architecture/hub-spoke-model.md - Technical architecture
19. reference/api.md - Python API documentation

## Root Level (Keep Simple)
- README.md - Main entry (update for new structure)
- INSTALLATION.md - Setup instructions
- CONTRIBUTING.md - Contribution guide
- CHANGELOG.md - NEW: Track version changes
