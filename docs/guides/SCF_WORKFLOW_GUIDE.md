# SCF Workflow Guide

This guide provides step-by-step instructions for common workflows within the Session Continuity Framework (SCF).

## 1. Initializing a New Project

To enable SCF for a new or existing project, use the `init_scf.py` script. This will copy the latest templates, set up the inheritance structure, and ensure your project is ready for intelligent context management.

**Command:**
```bash
python3 init_scf.py /path/to/your-project
```

**Options:**
- `--dry-run`: Preview the changes without modifying any files.
- `--force`: Overwrite existing SCF files if they are present.
- `--template-type <type>`: Specify a template type (e.g., `llm-enhanced`).

**Example:**
```bash
# Preview the initialization for a new web app
python3 init_scf.py /home/user/dev/my-new-app --dry-run

# Initialize the project
python3 init_scf.py /home/user/dev/my-new-app
```

## 2. Updating an Existing Project

To keep your SCF-enabled project up-to-date with the latest framework improvements, use the `update_scf.py` script. This script intelligently merges new template features, rebalances content, and syncs the inheritance chain without overwriting your project's specific customizations.

**Command:**
```bash
python3 update_scf.py /path/to/your-project
```

**Options:**
- `--dry-run`: Preview the updates that will be applied.
- `--force-rebalance`: Force content rebalancing even if the project is considered balanced.
- `--skip-inheritance`: Skip the inheritance chain synchronization.
- `--skip-rebalance`: Skip the content rebalancing step.

**Example:**
```bash
# Check for available updates in an existing project
python3 update_scf.py ./my-scf-project --dry-run

# Apply the updates
python3 update_scf.py ./my-scf-project
```

## 3. Leveraging the Analytics System

The SCF Analytics System is designed to track and measure the productivity gains from using the framework. It is automatically enabled in new projects and added to existing projects when you run the `update_scf.py` script.

### How it Works:
- **Automatic Tracking**: The `scf_llm_integration.py` module automatically starts and stops analytics sessions when you begin and end an AI interaction.
- **Metrics Captured**: The system tracks session count, time saved, context reuse, and more.
- **Data Storage**: All analytics data is stored within the `scf_analytics` section of your project's `buildstate.json` file.

### Viewing Analytics:
You can view the analytics for a project by inspecting its `buildstate.json` file. For more advanced reporting, you can use the `SCFAnalytics` class from `scf_analytics.py`.

**Example Snippet to Generate a Report:**
```python
from scf_analytics import SCFAnalytics

# Path to your project's buildstate.json
buildstate_path = './my-scf-project/buildstate.json'

# Initialize the analytics class and print a report
analytics = SCFAnalytics(buildstate_path)
print(analytics.get_report())
```

This workflow guide provides a starting point for using the core features of SCF. For more detailed information on specific components, please refer to the other documents in the `/docs` directory.