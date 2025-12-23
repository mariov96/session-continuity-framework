# SCF Architecture: Framework, Hub, and Spokes

This document explains SCF's three-tier architecture and how the components interact.

---

## Overview

SCF separates concerns into three distinct components:

```
┌─────────────────────────────────────────────────────────────┐
│  SCF FRAMEWORK (this repository)                            │
│  The "brains" - code, templates, tooling                    │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ User runs: scf hub create
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  YOUR HUB (user-chosen location, e.g., ~/scf-hub/)          │
│  Your personal data - profile, learnings, project registry  │
└─────────────────────────────────────────────────────────────┘
                              │
            ┌─────────────────┼─────────────────┐
            ▼                 ▼                 ▼
      ┌──────────┐      ┌──────────┐      ┌──────────┐
      │ Project A│      │ Project B│      │ Project C│
      │  (spoke) │      │  (spoke) │      │  (spoke) │
      └──────────┘      └──────────┘      └──────────┘
```

---

## 1. SCF Framework (This Repository)

**Purpose:** The intelligence layer - provides code, templates, and tooling.

**Location:** `github.com/mariov96/session-continuity-framework` (or your fork)

**Contains:**
```
session-continuity-framework/
├── scf                      # Unified CLI
├── teach.py                 # Push learnings to spokes
├── recon.py                 # Discover projects
├── init_scf.py              # Initialize spokes
├── update_scf.py            # Update spokes
├── templates/
│   └── spoke/               # Clean templates for new projects
│       ├── BUILDSTATE.json
│       ├── BUILDSTATE.md
│       ├── SCF_README.md
│       ├── kb-sync.json
│       └── spoke-signals.jsonl
├── docs/                    # Documentation
└── .scf/                    # SCF's own spoke files (dogfooding)
```

**Key Points:**
- This repo is ALSO a spoke project (dogfooding)
- Its `.scf/` folder tracks SCF's own development
- Users clone/fork this to get the framework
- Does NOT contain your personal hub data

---

## 2. Your Hub (User-Created)

**Purpose:** Your personal SCF home - stores your identity, preferences, and cross-project learnings.

**Location:** User-chosen (default: `~/scf-hub/`)

**Created via:** `scf hub create`

**Contains:**
```
~/scf-hub/
├── .scf/                    # Hub is also a spoke (tracks itself)
│   ├── BUILDSTATE.json
│   └── BUILDSTATE.md
├── hub-profile.json         # Your name, preferences, coding style
├── .scf-registry/           # Discovered spoke projects
│   ├── spoke-projects.json
│   └── spokes/              # Individual spoke metadata
├── learnings/               # Cross-project patterns (extracted)
└── signals/                 # Pulled signals from spokes
```

**Key Points:**
- Created once per user/machine
- Stores YOUR personal preferences
- Knows about all YOUR projects
- Propagates learnings across YOUR projects
- Never committed to the framework repo

### Hub Profile Example

```json
{
  "user": {
    "name": "Your Name",
    "github": "your-username"
  },
  "work_style": {
    "preferred_ais": ["Claude", "GitHub Copilot"],
    "coding_preferences": {
      "languages": ["Python", "TypeScript"],
      "avoid": ["Over-engineering"]
    }
  },
  "learning_philosophy": {
    "share_threshold": 8,
    "description": "Only share high-impact learnings"
  }
}
```

---

## 3. Spoke Projects (Your Work)

**Purpose:** Individual projects that benefit from SCF context persistence.

**Location:** Anywhere on your system

**Created via:** `scf init` (in any project directory)

**Contains:**
```
your-project/
├── .scf/
│   ├── BUILDSTATE.json      # Technical state + foundation
│   ├── BUILDSTATE.md        # Strategic context
│   ├── SCF_README.md        # AI instructions
│   ├── kb-sync.json         # Hub sync status
│   └── spoke-signals.jsonl  # High-impact learnings to share
├── ... (your project files)
```

**Key Points:**
- Each project has its own `.scf/` folder
- Tracks its own decisions, features, bugs
- Signals high-impact learnings back to hub
- Receives learnings from hub via `scf sync`

---

## How They Interact

### 1. Initialization Flow

```
User                    Framework                Hub                  Spoke
  │                         │                     │                     │
  │── scf hub create ──────>│                     │                     │
  │                         │── creates ─────────>│                     │
  │                         │                     │                     │
  │── cd my-project ───────>│                     │                     │
  │── scf init ────────────>│                     │                     │
  │                         │── creates ──────────────────────────────>│
  │                         │── registers ───────>│                     │
```

### 2. Learning Flow

```
Spoke A                  Hub                    Spoke B
   │                      │                        │
   │── high-impact ──────>│                        │
   │   decision           │                        │
   │   (spoke-signals)    │                        │
   │                      │                        │
   │                      │── scf sync ───────────>│
   │                      │   (propagates          │
   │                      │    learning)           │
```

### 3. Sync Flow

```
User                    Framework                Hub                  Spoke
  │                         │                     │                     │
  │── scf sync ────────────>│                     │                     │
  │   (in spoke dir)        │                     │                     │
  │                         │── pull signals ─────────────────────────>│
  │                         │<─ signals ──────────────────────────────│
  │                         │── aggregate ───────>│                     │
  │                         │                     │                     │
  │                         │── push learnings ──────────────────────>│
  │                         │── update kb-sync ──────────────────────>│
```

---

## Why This Separation?

### 1. Clean Adoption
Users get the framework without inheriting the creator's personal data.

### 2. Privacy
Your hub profile, project registry, and learnings stay on your machine.

### 3. Modularity
- Update framework independently
- Hub persists across framework updates
- Spokes evolve at their own pace

### 4. Team Flexibility
- Personal hubs for individuals
- Team hubs possible for shared learnings
- Framework stays universal

---

## Quick Reference

| Component | What It Is | Where It Lives | Who Creates It |
|-----------|-----------|----------------|----------------|
| Framework | Code + templates | Git repo (clone) | Maintained by SCF |
| Hub | Your profile + registry | `~/scf-hub/` (configurable) | You, via `scf hub create` |
| Spoke | Project context | `.scf/` in each project | You, via `scf init` |

---

## Commands

```bash
# Framework (run from framework directory)
./scf                        # CLI entry point

# Hub management (run from anywhere)
scf hub create               # Create your personal hub
scf hub locate               # Find/configure hub location
scf projects scan            # Discover spoke projects
scf learn                    # Extract cross-project learnings

# Spoke operations (run from project directory)
scf init                     # Initialize project as spoke
scf init --guided            # With foundation questions
scf sync                     # Sync with hub
scf status                   # Check SCF health
```

---

## Migration Notes

### Moving from Mixed Architecture

If your framework repo currently contains hub data (`.scf-registry/`, hub-profile, etc.):

1. **Create your hub:**
   ```bash
   scf hub create ~/scf-hub
   ```

2. **Move hub data:**
   ```bash
   mv .scf-registry/* ~/scf-hub/.scf-registry/
   ```

3. **Update spoke references:**
   - Each spoke's `_scf_metadata.hub_reference.hub_location` should point to your hub

4. **Keep framework's `.scf/`:**
   - This is the framework's OWN spoke files (dogfooding)
   - Don't delete - it's a living example

---

*This architecture enables SCF to scale from individual use to team collaboration while maintaining clean separation of concerns.*
