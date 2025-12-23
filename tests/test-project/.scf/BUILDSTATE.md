# SCF Internal Test Project

## Purpose

This is an **internal testing project** used to validate SCF scripts and behaviors during development.

**DO NOT include this in spoke directory listings** - it's for internal use only.

## Use Cases

1. **Testing recon.py**
   - Verify project discovery
   - Test SCF version detection
   - Validate health metrics calculation

2. **Testing teach.py**
   - Test initialization on fresh projects
   - Test update operations
   - Validate template application

3. **Testing learn.py**
   - Verify learning extraction
   - Test pattern recognition
   - Validate offer creation

4. **Testing rebalance.py**
   - Test MD/JSON content balancing
   - Verify drift detection
   - Validate content migration

## Test Scenarios

### Scenario 1: New Project Discovery
- Remove `.scf/` directory
- Run `recon.py`
- Verify it's detected as new project
- Test opt-in/opt-out flow

### Scenario 2: SCF Initialization
- Start with empty project
- Run `teach.py --init`
- Verify proper setup

### Scenario 3: Learning Extraction
- Add high-impact decision
- Run `learn.py`
- Verify learning captured

### Scenario 4: Rebalancing
- Add content to wrong files
- Run `rebalance.py`
- Verify content moved correctly

## History

- 2025-11-30: Created for refactoring initiative
