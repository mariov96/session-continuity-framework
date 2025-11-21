# SCF Public/Private Fork Strategy

## Overview

The Session Continuity Framework (SCF) is designed to support a common enterprise workflow where a public, open-source project is forked into a private repository for internal development. This strategy allows teams to benefit from community contributions while keeping proprietary code, configurations, and sensitive information secure.

SCF's inheritance system, particularly the `private-overrides.json` feature, is the cornerstone of this workflow.

## Core Concepts

- **Upstream Public Repo**: The original, open-source SCF project that your team tracks.
- **Private Fork**: Your team's internal, private copy of the repository where proprietary development occurs.
- **One-Way Sync**: Changes from the public repo are periodically merged into the private fork. The private fork is never merged back into the public repo.
- **Private Overrides**: Sensitive information such as API keys, internal endpoints, or proprietary patterns are stored in a `.scf/private/private-overrides.json` file. This file is gitignored and never committed to either the private or public repository.

## The Inheritance Chain in a Private Fork

When using a private fork, the SCF inheritance chain provides a clear separation between public, private, and local configurations:

1.  **`private-overrides.json` (Level -1)**: Highest priority. Contains secrets and proprietary configurations. **Never committed to Git.**
2.  **`buildstate.json` (Level 0)**: Your project's main configuration file. Contains public-safe project details. Committed to your private fork.
3.  **`.scf/buildstate.library.json` (Level 1)**: Project-level patterns specific to your private fork.
4.  **`org-standards.json` (Level 2)**: Your organization's shared standards. Can be managed in a separate, private repository.
5.  **`global-defaults.json` (Level 3)**: Global defaults from the public SCF framework.

## Workflow Example

1.  **Fork the Repository**: Create a private fork of the public SCF-enabled project on your Git platform.

2.  **Set Up the Private Directory**: After cloning your private fork, run the `init_scf.py` script. It will automatically create the `.scf/private/` directory and a `.gitignore` file to protect it.

3.  **Add Private Configurations**: Create a `private-overrides.json` file inside the `.scf/private/` directory. Add any sensitive information here.

    **Example `private-overrides.json`:**
    ```json
    {
      "api_keys": {
        "internal_service": "your-secret-api-key"
      },
      "dev_environment": {
        "proxy": "http://internal.proxy.yourcompany.com"
      }
    }
    ```

4.  **Sync with Upstream**: To pull in updates from the public repository:
    ```bash
    # Add the public repo as an upstream remote
    git remote add upstream https://github.com/public-repo/scf-project.git

    # Fetch the latest changes from upstream
    git fetch upstream

    # Merge the changes into your main branch
    git merge upstream/main
    ```

5.  **Resolve Conflicts**: If there are merge conflicts, resolve them, keeping your private fork's changes where necessary. Your `private-overrides.json` will never be part of a conflict because it is not tracked by Git.

## Benefits of This Strategy

- **Security**: Sensitive data is never committed to any repository, public or private.
- **Collaboration**: Your team can work freely in the private fork without risk of exposing proprietary information.
- **Maintainability**: You can easily pull in updates, bug fixes, and new features from the public project without overwriting your private configurations.
- **Clean Separation**: The inheritance system provides a clear and logical separation between different layers of configuration.

By following this strategy, you can leverage the power of open-source collaboration while maintaining the security and integrity of your internal development process.