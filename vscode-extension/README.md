# SCF Session State Viewer

## Overview

This Visual Studio Code extension provides at-a-glance visibility into the session state of your Session Continuity Framework (SCF) enabled projects. It adds an item to the status bar that displays who last modified the project, helping to prevent context collisions and facilitate seamless collaboration between multiple developers or AI assistants.

## Features

- **Status Bar Display**: Shows the `last_modified_by` field from your project's `buildstate.json` directly in the VS Code status bar.
- **Review Indicator**: The status bar item will change color to indicate when `requires_review` is set to `true`, alerting you to significant changes made in the last session.
- **Detailed Information on Click**: Click the status bar item to see more detailed information about the last session, including the modification time and the reason for review.
- **Automatic Updates**: The display automatically updates when you save changes to `buildstate.json` or switch between open files.

## Usage

1.  **Install the Extension**: (Instructions to be added once published)
2.  **Open an SCF-enabled Project**: Make sure the project you open in VS Code contains a `buildstate.json` file with a `_session_state` block.
3.  **View the Status Bar**: The SCF session state will automatically appear in the bottom-left of your editor.

This extension is a crucial component of the SCF ecosystem, bringing the core principle of session continuity directly into the developer's daily workflow.