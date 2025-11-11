// SCF Browser Extension - Popup Script
// Manages the extension popup interface and user interactions

class SCFPopup {
    constructor() {
        this.syncStatus = null;
        this.connectedTabs = [];
        
        this.init();
    }
    
    init() {
        console.log('🎼 SCF Popup - Initializing...');
        
        // Load initial data
        this.loadStatus();
        this.loadConnectedTabs();
        
        // Set up event listeners
        this.setupEventListeners();
        
        // Refresh data periodically
        setInterval(() => {
            this.loadStatus();
            this.loadConnectedTabs();
        }, 3000);
    }
    
    setupEventListeners() {
        // Toggle sync button
        document.getElementById('toggle-sync').addEventListener('click', () => {
            this.toggleSync();
        });
        
        // Export all conversations
        document.getElementById('export-all').addEventListener('click', () => {
            this.exportAllConversations();
        });
        
        // Health check button
        document.getElementById('health-check').addEventListener('click', () => {
            this.performHealthCheck();
        });
    }
    
    async loadStatus() {
        try {
            const response = await chrome.runtime.sendMessage({
                action: 'getSyncStatus'
            });
            
            this.syncStatus = response;
            this.updateStatusDisplay();
            
        } catch (error) {
            console.error('Error loading status:', error);
            this.showError('Failed to load status');
        }
    }
    
    async loadConnectedTabs() {
        try {
            const tabs = await chrome.runtime.sendMessage({
                action: 'getConnectedTabs'
            });
            
            this.connectedTabs = tabs || [];
            this.updateTabsDisplay();
            
        } catch (error) {
            console.error('Error loading tabs:', error);
            this.showError('Failed to load tabs');
        }
    }
    
    updateStatusDisplay() {
        if (!this.syncStatus) return;
        
        // Update sync status
        const syncStatusElement = document.getElementById('sync-status');
        const syncIndicator = document.getElementById('sync-indicator');
        
        if (this.syncStatus.syncEnabled) {
            syncStatusElement.textContent = 'Enabled';
            syncIndicator.className = 'status-indicator status-online';
        } else {
            syncStatusElement.textContent = 'Disabled';
            syncIndicator.className = 'status-indicator status-offline';
        }
        
        // Update server status
        const serverStatusElement = document.getElementById('server-status');
        const serverIndicator = document.getElementById('server-indicator');
        
        switch (this.syncStatus.serverStatus) {
            case 'online':
                serverStatusElement.textContent = 'Online';
                serverIndicator.className = 'status-indicator status-online';
                break;
            case 'offline':
                serverStatusElement.textContent = 'Offline';
                serverIndicator.className = 'status-indicator status-offline';
                break;
            default:
                serverStatusElement.textContent = 'Unknown';
                serverIndicator.className = 'status-indicator status-warning';
        }
        
        // Update tab count
        document.getElementById('tab-count').textContent = this.syncStatus.connectedTabs || 0;
        
        // Update toggle button
        const toggleButton = document.getElementById('toggle-sync');
        if (this.syncStatus.syncEnabled) {
            toggleButton.textContent = '⏹️ Disable Sync';
            toggleButton.className = 'toggle-button toggle-enabled';
        } else {
            toggleButton.textContent = '▶️ Enable Sync';
            toggleButton.className = 'toggle-button toggle-disabled';
        }
    }
    
    updateTabsDisplay() {
        const container = document.getElementById('tabs-container');
        
        if (this.connectedTabs.length === 0) {
            container.innerHTML = `
                <div class="empty-state">
                    No LLM tabs connected.<br>
                    Open Claude, ChatGPT, or other supported platforms.
                </div>
            `;
            return;
        }
        
        container.innerHTML = this.connectedTabs.map(tab => {
            const provider = this.getProviderDisplayName(tab.provider);
            const providerColor = this.getProviderColor(tab.provider);
            
            return `
                <div class="tab-item">
                    <div class="tab-provider" style="color: ${providerColor};">
                        ${provider}
                    </div>
                    <div class="tab-title" title="${tab.title}">
                        ${tab.title || 'Untitled'}
                    </div>
                    <div class="tab-url" title="${tab.url}">
                        ${this.shortenUrl(tab.url)}
                    </div>
                </div>
            `;
        }).join('');
    }
    
    getProviderDisplayName(provider) {
        const names = {
            'claude_web': '🤖 Claude',
            'chatgpt_web': '💬 ChatGPT',
            'perplexity_web': '🔍 Perplexity',
            'gemini_web': '💎 Gemini'
        };
        
        return names[provider] || '❓ Unknown';
    }
    
    getProviderColor(provider) {
        const colors = {
            'claude_web': '#ff7b54',
            'chatgpt_web': '#10a37f',
            'perplexity_web': '#20b2aa',
            'gemini_web': '#4285f4'
        };
        
        return colors[provider] || '#fbbf24';
    }
    
    shortenUrl(url) {
        if (!url) return '';
        
        try {
            const urlObj = new URL(url);
            let shortened = urlObj.hostname;
            
            if (urlObj.pathname && urlObj.pathname !== '/') {
                const pathParts = urlObj.pathname.split('/').filter(p => p);
                if (pathParts.length > 0) {
                    shortened += '/' + pathParts[0];
                    if (pathParts.length > 1) {
                        shortened += '/...';
                    }
                }
            }
            
            return shortened;
        } catch {
            return url.substring(0, 30) + '...';
        }
    }
    
    async toggleSync() {
        const button = document.getElementById('toggle-sync');
        const originalText = button.textContent;
        
        button.textContent = '⏳ Updating...';
        button.disabled = true;
        
        try {
            const newState = !this.syncStatus.syncEnabled;
            
            const response = await chrome.runtime.sendMessage({
                action: 'toggleSync',
                enabled: newState
            });
            
            if (response.success) {
                // Update local state
                this.syncStatus.syncEnabled = response.enabled;
                this.updateStatusDisplay();
                
                // Show feedback
                this.showNotification(
                    response.enabled ? 'Sync enabled!' : 'Sync disabled!',
                    'success'
                );
            } else {
                throw new Error('Toggle failed');
            }
            
        } catch (error) {
            console.error('Error toggling sync:', error);
            this.showNotification('Failed to toggle sync', 'error');
            button.textContent = originalText;
        } finally {
            button.disabled = false;
        }
    }
    
    async exportAllConversations() {
        const button = document.getElementById('export-all');
        const originalText = button.textContent;
        
        button.textContent = '📦 Exporting...';
        button.disabled = true;
        
        try {
            const exportData = await chrome.runtime.sendMessage({
                action: 'exportAllConversations'
            });
            
            // Create and download export file
            const dataStr = JSON.stringify(exportData, null, 2);
            const dataBlob = new Blob([dataStr], { type: 'application/json' });
            
            const link = document.createElement('a');
            link.href = URL.createObjectURL(dataBlob);
            link.download = `scf-export-${new Date().toISOString().slice(0, 10)}.json`;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            
            this.showNotification('Export downloaded!', 'success');
            
        } catch (error) {
            console.error('Error exporting conversations:', error);
            this.showNotification('Export failed', 'error');
        } finally {
            button.textContent = originalText;
            button.disabled = false;
        }
    }
    
    async performHealthCheck() {
        const button = document.getElementById('health-check');
        const originalText = button.textContent;
        
        button.textContent = '🔄 Checking...';
        button.disabled = true;
        
        try {
            const response = await chrome.runtime.sendMessage({
                action: 'serverHealthCheck'
            });
            
            // Update server status display
            this.syncStatus.serverStatus = response.status;
            this.updateStatusDisplay();
            
            const messages = {
                'online': 'Server is healthy!',
                'offline': 'Server is offline',
                'error': 'Server error detected'
            };
            
            const type = response.status === 'online' ? 'success' : 'error';
            this.showNotification(messages[response.status] || 'Unknown status', type);
            
        } catch (error) {
            console.error('Error checking server health:', error);
            this.showNotification('Health check failed', 'error');
        } finally {
            button.textContent = originalText;
            button.disabled = false;
        }
    }
    
    showNotification(message, type = 'info') {
        // Create temporary notification
        const notification = document.createElement('div');
        notification.style.cssText = `
            position: fixed;
            top: 10px;
            left: 10px;
            right: 10px;
            padding: 12px;
            border-radius: 6px;
            color: white;
            font-size: 12px;
            font-weight: 500;
            z-index: 1000;
            text-align: center;
            ${type === 'success' ? 'background: #22c55e;' : 
              type === 'error' ? 'background: #ef4444;' : 
              'background: #3b82f6;'}
        `;
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        // Auto-remove after 3 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 3000);
    }
    
    showError(message) {
        console.error('SCF Popup Error:', message);
        this.showNotification(message, 'error');
    }
}

// Initialize popup when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new SCFPopup();
});