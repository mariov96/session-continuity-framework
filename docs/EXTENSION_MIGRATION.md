# Extension Migration Guide

This document describes how to move the VS Code and Browser extensions to their own repositories.

## Why Separate Repos?

1. **Independent release cycles** - Extensions evolve differently than core framework
2. **Cleaner architecture** - Framework is framework, extensions are extensions
3. **Easier contribution** - Contributors can focus on specific areas
4. **Marketplace requirements** - VS Code extensions often need dedicated repos

---

## VS Code Extension Migration

### Current Location
```
session-continuity-framework/vscode-extension/
```

### Target Repository
```
scf-vscode-extension/
```

### Migration Steps

```bash
# 1. Create new repository
mkdir ~/projects/scf-vscode-extension
cd ~/projects/scf-vscode-extension
git init

# 2. Copy extension files
cp -r ~/projects/session-continuity-framework/vscode-extension/* .

# 3. Initialize as SCF spoke
cd ~/projects/session-continuity-framework
./scf init --guided ~/projects/scf-vscode-extension

# 4. Clean up node_modules (regenerate in new repo)
cd ~/projects/scf-vscode-extension
rm -rf node_modules .venv
npm install

# 5. Update package.json repository field
# Edit package.json to point to new repo

# 6. Initial commit
git add .
git commit -m "Initial commit: SCF VS Code Extension

Migrated from session-continuity-framework monorepo.
Now a standalone spoke project with its own release cycle.

🤖 Generated with Claude Code"

# 7. Create GitHub repo and push
gh repo create scf-vscode-extension --public --source=. --push
```

### Post-Migration Cleanup

In the main SCF repo:
```bash
# Remove vscode-extension directory
rm -rf vscode-extension/

# Update .gitignore if needed
echo "vscode-extension/" >> .gitignore

# Commit removal
git add -A
git commit -m "chore: Move vscode-extension to separate repo

Extension now lives at: github.com/mariov96/scf-vscode-extension
This keeps the core framework lean and focused."
```

---

## Browser Extension Migration

### Current Location
```
session-continuity-framework/browser-extension/
```

### Target Repository
```
scf-browser-extension/
```

### Migration Steps

```bash
# 1. Create new repository
mkdir ~/projects/scf-browser-extension
cd ~/projects/scf-browser-extension
git init

# 2. Copy extension files
cp -r ~/projects/session-continuity-framework/browser-extension/* .

# 3. Initialize as SCF spoke
cd ~/projects/session-continuity-framework
./scf init --guided ~/projects/scf-browser-extension

# 4. Initial commit
git add .
git commit -m "Initial commit: SCF Browser Extension

Migrated from session-continuity-framework monorepo.
Captures web LLM conversations for local SCF integration.

🤖 Generated with Claude Code"

# 5. Create GitHub repo and push
gh repo create scf-browser-extension --public --source=. --push
```

### Post-Migration Cleanup

Same as VS Code extension - remove directory and commit.

---

## Recommended Foundation for Extensions

When running `scf init --guided` for extensions, use these answers:

### VS Code Extension
- **Type:** Code
- **One-liner:** VS Code extension providing SCF integration and context panel
- **In scope:** Extension UI, SCF file reading, context display, health checks
- **Out of scope:** Core SCF logic (uses framework), server-side features
- **AI style:** Collaborative

### Browser Extension
- **Type:** Code
- **One-liner:** Browser extension capturing web LLM conversations for SCF
- **In scope:** Conversation capture, local storage, popup UI, content scripts
- **Out of scope:** Core SCF logic, desktop features
- **AI style:** Collaborative

---

## Linking Extensions Back to Hub

After migration, extensions become spoke projects:

```
Your Hub (~/scf-hub/)
├── .scf-registry/
│   └── spoke-projects.json  ← Register extensions here
│
└── Connected Spokes:
    ├── ~/projects/scf-vscode-extension/
    ├── ~/projects/scf-browser-extension/
    └── ~/projects/other-projects/
```

Extensions can signal learnings back to hub, receive updates, etc.

---

## Timeline

This migration can happen anytime. The extensions work independently and can be moved when convenient:

1. **Now:** Extensions continue working in monorepo
2. **When ready:** Follow steps above to migrate
3. **After migration:** Extensions are independent spokes

No rush - this is about clean architecture, not urgent functionality.
