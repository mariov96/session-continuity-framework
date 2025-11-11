sync_buildstate.py - Session Continuity Framework (SCF) Synchronization Tool
Overview
The sync_buildstate.py script is a critical component of the Session Continuity Framework (SCF) for the Vantaca Action Items Dashboard, a React-based analytics dashboard for property management. The SCF uses two files to manage project state:

buildstate.md: A Markdown file for ideation, planning, and narrative context, containing detailed user stories, decision rationale, and instructions.
buildstate.json: A JSON file for technical specifications, providing concise, machine-readable data for implementation and automation.

This script ensures that key data (e.g., features, bugs, next steps, decisions) remains consistent between buildstate.md and buildstate.json, enabling seamless collaboration across ideation and technical sessions. It is designed to be run before committing changes to version control to maintain synchronization.
Purpose
The sync_buildstate.py script:

Extracts structured data (e.g., features, bugs, next steps, decisions) from buildstate.md.
Updates buildstate.json with the extracted data, preserving its machine-readable format.
Logs synchronization events in buildstate.json's change_log for traceability.
Supports periodic rebalancing of the SCF to prevent divergence between the two files.

This ensures that both files remain aligned, allowing developers to use buildstate.md for planning and buildstate.json for coding/debugging without losing context.
Prerequisites

Python: Version 3.6 or higher.
Dependencies: Standard library (re, json, datetime)—no external packages required.
Files:
buildstate.md: Must exist in the project root with the expected SCF structure (e.g., Feature Requirements Table, Known Issues, Roadmap).
buildstate.json: Must exist in the project root with the expected SCF structure (e.g., features, bugs, next_steps).


Project Context: The script is tailored for the Vantaca Action Items Dashboard, a React 18+ application using Tailwind CSS, Lucide React, and a Vantaca REST API (see Swagger Docs).

Installation

Place sync_buildstate.py in the project root (same directory as buildstate.md and buildstate.json).
Ensure Python 3.6+ is installed:python --version


Verify that buildstate.md and buildstate.json are present and follow the SCF structure (see SCF documentation for details).

Usage
Run the script to sync data from buildstate.md to buildstate.json:
python sync_buildstate.py

What the Script Does

Reads buildstate.md: Parses sections like Feature Requirements Table, Known Issues, Roadmap, and Change Log using regular expressions.
Updates buildstate.json:
Syncs features with the Feature Requirements Table.
Syncs bugs with Known Issues.
Syncs next_steps with Roadmap’s next sprint.
Syncs decisions with Change Log entries.
Adds a change_log entry with the sync date and description.
Updates rebalanced_at with the current date.


Saves buildstate.json: Writes the updated JSON with proper formatting (indented for readability).

Output
Upon successful execution, the script prints:
Synced buildstate.md to buildstate.json

If errors occur (e.g., missing files, invalid JSON), the script will raise an exception with details.
Integration with Workflow
To ensure consistency, run sync_buildstate.py before committing changes to version control. You can automate this using a