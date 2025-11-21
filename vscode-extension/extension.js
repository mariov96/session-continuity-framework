const vscode = require('vscode');
const fs = require('fs');
const path = require('path');

let scfStatusBarItem;

function activate(context) {
    console.log('Congratulations, your extension "scf-session-viewer" is now active!');

    // Create a command to show the session state
    let disposable = vscode.commands.registerCommand('scf-session-viewer.showSessionState', async () => {
        const sessionState = await getSessionState();
        if (sessionState) {
            const message = `SCF Session State:\n- Last Modified By: ${sessionState.last_modified_by}\n- At: ${sessionState.last_modified_at}\n- Reason: ${sessionState.review_reason}`;
            vscode.window.showInformationMessage(message);
        } else {
            vscode.window.showWarningMessage('No SCF buildstate.json found in the current workspace.');
        }
    });

    context.subscriptions.push(disposable);

    // Create and manage the status bar item
    scfStatusBarItem = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 100);
    scfStatusBarItem.command = 'scf-session-viewer.showSessionState';
    context.subscriptions.push(scfStatusBarItem);

    // Update status bar on startup and when the active editor changes
    context.subscriptions.push(vscode.window.onDidChangeActiveTextEditor(updateStatusBar));
    context.subscriptions.push(vscode.workspace.onDidSaveTextDocument(updateStatusBar));

    // Initial update
    updateStatusBar();
}

async function updateStatusBar() {
    const sessionState = await getSessionState();
    if (sessionState && sessionState.last_modified_by) {
        scfStatusBarItem.text = `$(sync~spin) SCF: ${sessionState.last_modified_by}`;
        scfStatusBarItem.tooltip = `Last modified at ${sessionState.last_modified_at}\nReason: ${sessionState.review_reason}`;
        if (sessionState.requires_review) {
            scfStatusBarItem.backgroundColor = new vscode.ThemeColor('statusBarItem.warningBackground');
        } else {
            scfStatusBarItem.backgroundColor = undefined;
        }
        scfStatusBarItem.show();
    } else {
        scfStatusBarItem.hide();
    }
}

async function getSessionState() {
    const workspaceFolders = vscode.workspace.workspaceFolders;
    if (!workspaceFolders) {
        return null;
    }

    const workspaceRoot = workspaceFolders[0].uri.fsPath;
    const buildstatePath = path.join(workspaceRoot, 'buildstate.json');

    try {
        const content = await fs.promises.readFile(buildstatePath, 'utf8');
        const buildstate = JSON.parse(content);
        return buildstate._session_state || null;
    } catch (error) {
        // Silently fail if file doesn't exist or is invalid JSON
        return null;
    }
}

function deactivate() {
    if (scfStatusBarItem) {
        scfStatusBarItem.dispose();
    }
}

module.exports = {
    activate,
    deactivate
};