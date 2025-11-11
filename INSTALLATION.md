# SCF Universal Context Sync - Installation Requirements

## Browser Extension Installation

### Chrome/Chromium Installation

1. **Enable Developer Mode**:
   - Open Chrome and go to `chrome://extensions/`
   - Toggle "Developer mode" in the top right corner

2. **Load Extension**:
   - Click "Load unpacked"
   - Select the `browser-extension` folder from your SCF directory
   - The SCF Universal Context Sync extension should appear in your extensions list

3. **Pin Extension**:
   - Click the extensions icon in Chrome toolbar (puzzle piece)
   - Pin the SCF extension for easy access

### Firefox Installation

1. **Temporary Installation** (Development):
   - Go to `about:debugging`
   - Click "This Firefox"
   - Click "Load Temporary Add-on"
   - Select the `manifest.json` file from the `browser-extension` folder

2. **Permanent Installation**:
   - Package the extension as a .xpi file
   - Install through Firefox Add-ons manager

## Local Server Installation

### Python Dependencies

The SCF local server requires Python 3.7+ and the following packages:

```bash
# Install required Python packages
pip install aiohttp aiohttp-cors aiofiles

# Or use the requirements file (if you create one)
pip install -r requirements.txt
```

### Requirements.txt Content

Create a `requirements.txt` file with:

```
aiohttp>=3.8.0
aiohttp-cors>=0.7.0
aiofiles>=23.0.0
```

### Virtual Environment Setup (Recommended)

```bash
# Create virtual environment
python -m venv scf-env

# Activate virtual environment
# On Linux/macOS:
source scf-env/bin/activate
# On Windows:
scf-env\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Quick Start Guide

### 1. Start Local Server

```bash
# Navigate to SCF directory
cd /path/to/session-continuity-framework

# Start the server (with virtual environment activated)
python scf_local_server.py --port 8765 --workspace .

# Or specify a custom workspace
python scf_local_server.py --workspace /path/to/your/project
```

### 2. Install Browser Extension

- Follow the browser-specific installation steps above
- The extension will automatically try to connect to `localhost:8765`

### 3. Enable Sync

1. **In Browser**:
   - Open a supported LLM platform (Claude.ai, ChatGPT, etc.)
   - Click the SCF extension icon
   - Click "Enable Sync"

2. **Verify Connection**:
   - The extension should show "Server: Online" and "Sync: Enabled"
   - Start a conversation - you should see activity in the server console

### 4. Check Buildstate

- Conversations will be automatically saved to `buildstate/` directory
- Files are named: `web_{provider}_{title}_{date}.md`
- Each file contains extracted insights, decisions, and conversation context

## Supported Platforms

The extension automatically detects and syncs with:

- **Claude.ai** (Anthropic)
- **ChatGPT** (OpenAI)
- **Perplexity.ai**
- **Gemini** (Google)

## Configuration Options

### Server Configuration

```bash
# Custom port
python scf_local_server.py --port 9000

# Custom workspace
python scf_local_server.py --workspace /path/to/project

# Both options
python scf_local_server.py --port 9000 --workspace /path/to/project
```

### Extension Configuration

- Server port can be configured in extension popup
- Sync can be toggled on/off per session
- Export conversations manually through extension popup

## Troubleshooting

### Server Not Starting

1. **Check Python version**: `python --version` (needs 3.7+)
2. **Install dependencies**: `pip install aiohttp aiohttp-cors aiofiles`
3. **Check port availability**: Make sure port 8765 (or custom) is not in use
4. **Firewall**: Ensure localhost connections are allowed

### Extension Not Connecting

1. **Server running**: Check if server is running and accessible at `localhost:8765/health`
2. **Browser permissions**: Ensure extension has permission to access the websites
3. **Extension reload**: Try reloading the extension in browser extensions manager
4. **Console errors**: Check browser developer console for error messages

### Conversations Not Syncing

1. **Enable sync**: Make sure sync is enabled in extension popup
2. **Supported site**: Only works on Claude.ai, ChatGPT, Perplexity, and Gemini
3. **Server logs**: Check server console for sync attempts and errors
4. **Buildstate directory**: Verify the `buildstate/` directory exists and is writable

### Manual Health Check

Test server directly:
```bash
# Test health endpoint
curl http://localhost:8765/health

# Expected response:
{
  "status": "healthy",
  "version": "2.0",
  "workspace": "/path/to/workspace",
  "buildstate_files": 0,
  "timestamp": "2024-01-01T12:00:00"
}
```

## Advanced Usage

### Custom Workspace Integration

Point the server to your existing project:

```bash
# For a specific project
python scf_local_server.py --workspace /path/to/my-project

# Server will create buildstate/ directory in your project
# Web conversations will be synced directly to your project context
```

### Team Collaboration

- Share buildstate files generated from web conversations
- Include web insights in your team's existing buildstate workflow
- Use SCF's team sharing features with web-captured context

### Integration with Existing Tools

The extension coexists with:
- Existing `claude.md` files (Claude projects)
- Custom `llm.md` files
- Other AI interaction tools

Web conversations supplement rather than replace existing workflows.

## Security Notes

- Server runs on localhost only (127.0.0.1)
- No external network access required
- Conversation data stays local
- Extension only accesses supported LLM platforms
- No data sent to external servers (except your chosen LLM platforms)

## Next Steps

Once installed and running:

1. **Test the sync**: Start a conversation on a supported platform
2. **Review buildstate**: Check the generated files in `buildstate/`
3. **Integrate insights**: Apply captured insights to your local development
4. **Customize workflow**: Adjust settings and workspace location as needed
5. **Share context**: Use team collaboration features to share valuable insights

The SCF Universal Context Sync bridges the gap between web LLM conversations and local development, ensuring no valuable insights or decisions are lost in the transition between different AI interaction surfaces.