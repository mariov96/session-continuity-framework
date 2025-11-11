# SCF Repository Structure

This document describes the clean, organized structure of the Session Continuity Framework repository after consolidation.

## Core Framework Files

### Primary Tools
- **`buildstate_hunter_learner.py`** - Main ecosystem intelligence system with discovery, learning, inheritance updates, and rebalancing
- **`scf_inheritance.py`** - Four-level inheritance hierarchy management system
- **`scf_rebalancer.py`** - Intelligent content optimization between .md/.json files

### Master Templates
- **`templates/buildstate.json`** - Unified technical buildstate template
- **`templates/buildstate.md`** - Unified strategic buildstate template

## Documentation Structure

### Main Documentation
- **`README.md`** - Primary repository documentation with quick start and usage examples
- **`CONTRIBUTING.md`** - Contribution guidelines and code of conduct
- **`LICENSE`** - MIT license file

### Detailed Guides
- **`docs/scf_rebalancing_guide.md`** - Comprehensive guide to content rebalancing features
- **`docs/IMPLEMENTATION_COMPLETE.md`** - Complete implementation summary and capabilities

## Example and Test Files

### Working Example
- **`test-scf-app/`** - Clean test project demonstrating SCF usage with inheritance setup

### Legacy Support
- **`examples/`** - Usage examples and demo scripts
- **`sync_buildstate/`** - Legacy synchronization utilities (maintained for compatibility)

## Development Infrastructure

### Version Control
- **`.git/`** - Git repository data
- **`.github/`** - GitHub workflows and templates
- **`.evolution/`** - SCF evolutionary tracking

### Development Environment
- **`.vscode/`** - VS Code configuration for optimal SCF development
- **`__pycache__/`** - Python bytecode cache

## What Was Removed

### Consolidated Templates
- ❌ `claude-style/` → Consolidated into `templates/`
- ❌ `grok-style/` → Consolidated into `templates/`  
- ❌ `tests/` → Replaced by `test-scf-app/`
- ❌ `test-scf-project/` → Kept `test-scf-app/` as main example

### Legacy Documentation Files
- ❌ `HUNTER_LEARNER_*.md` → Consolidated into main `README.md`
- ❌ `SCF_*.md` → Key content moved to `docs/`
- ❌ `sc_*.md` → Legacy files from earlier versions
- ❌ `_SC-*.md` → Template files superseded by new system

### Legacy Scripts
- ❌ `hunter_learner_config.py` → Configuration integrated into main scripts
- ❌ `run_example.py` → Example usage covered in documentation
- ❌ `scf_ecosystem_learner.py` → Functionality integrated into hunter_learner
- ❌ `scf_growth_framework.py` → Growth patterns integrated into main system
- ❌ `scf_project_starter.py` → Project setup handled by inheritance system
- ❌ `scf_surgical.py` → Surgical operations integrated into main tools
- ❌ `test_windows_paths.py` → Testing integrated into main system
- ❌ `update_sc_files.py` → Legacy file from earlier framework versions

### System Files
- ❌ `*Zone.Identifier` → Windows security identifier files removed
- ❌ `ecosystem_insights_*.json` → Temporary insight files cleaned up

## Benefits of Clean Structure

### 🎯 **Focused Core**
- Only 3 essential Python files for all functionality
- Clear separation of concerns between discovery, inheritance, and rebalancing
- Single set of master templates with consolidated best practices

### 📖 **Clear Documentation**
- Main README covers all essential usage
- Detailed guides in organized `docs/` folder
- Working example project demonstrating real usage

### 🚀 **Easy Onboarding**
- New users see only what they need
- Clear file structure matches documentation
- No confusion from legacy or duplicate files

### 🛠️ **Maintainable Codebase**
- Consolidated functionality reduces maintenance overhead
- Clear ownership of features across minimal files
- Testing focused on core functionality rather than scattered scripts

## Usage After Cleanup

### For New Users
1. Read main `README.md` for overview and quick start
2. Use `templates/` files to create new projects
3. Run core tools for ecosystem management

### For Advanced Users
1. Refer to `docs/` for detailed guides
2. Examine `test-scf-app/` for real-world usage patterns
3. Extend functionality in the 3 core framework files

### For Contributors
1. Follow `CONTRIBUTING.md` guidelines
2. Focus changes on the 3 core Python files
3. Update documentation in `docs/` as needed

This clean structure eliminates confusion while preserving all essential functionality, making SCF more accessible and maintainable for all users.