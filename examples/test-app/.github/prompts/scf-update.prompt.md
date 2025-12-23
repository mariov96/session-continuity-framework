# Update SCF Buildstate

Your goal is to update and rebalance the buildstate for this project.

Check current balance:
```bash
python update_scf.py --path . --dry-run
```

If rebalancing needed:
```bash
python update_scf.py --path . --rebalance
```

Review changes and confirm updates to AGENTS.md and LLM context.
