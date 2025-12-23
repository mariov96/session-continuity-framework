# SCF Test Suite

This directory contains test projects and test scripts for validating SCF functionality.

## Structure

```
tests/
├── test-project/          # Internal test project (not in spoke directory)
│   ├── .scf/             # SCF-enabled test project
│   ├── src/              # Mock source code
│   └── tests/            # Mock test files
├── test_recon.py         # Tests for recon.py
├── test_teach.py         # Tests for teach.py
├── test_learn.py         # Tests for learn.py
├── test_registry.py      # Tests for registry operations
└── README.md             # This file
```

## Running Tests

```bash
# Run all tests
pytest tests/

# Run specific test module
pytest tests/test_recon.py

# Verbose output
pytest tests/ -v
```

## Test Project

The `test-project/` directory is an **internal testing fixture**:

- **Purpose:** Validate SCF scripts in isolation
- **Status:** Should NOT appear in `.scf-registry/spokes/`
- **Usage:** Scripts can use this for testing without affecting real projects

## Adding New Tests

1. Create test file: `test_<feature>.py`
2. Import necessary SCF modules
3. Use `test-project/` as fixture
4. Clean up after tests (restore state)

## Test Guidelines

- Tests should be idempotent (can run multiple times)
- Clean up modifications to test-project after each test
- Don't modify real spoke projects in tests
- Use mocks for external dependencies
