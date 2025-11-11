// SCF Browser Extension - Background Service Worker
// Manages extension state and communication between content scripts and local SCF

class SCFBackground {
    constructor() {
        this.syncEnabled = false;
        this.connectedTabs = new Map();
        this.localServerStatus = 'unknown';
        
        this.init();
    }
    
    init() {
        console.log('🎼 SCF Background Service Worker - Starting...');
        
        // Load saved settings
        this.loadSettings();
        
        // Set up message listeners
        chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
            this.handleMessage(message, sender, sendResponse);
            return true; // Keep message channel open for async responses
        });
        
        // Handle tab updates
        chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
            this.handleTabUpdate(tabId, changeInfo, tab);
        });
        
        // Handle tab removal
        chrome.tabs.onRemoved.addListener((tabId) => {
            this.connectedTabs.delete(tabId);
        });
        
        // Periodic health check
        setInterval(() => {
            this.checkLocalServerHealth();
        }, 60000); // Check every minute
        
        // Initial server check
        this.checkLocalServerHealth();
    }
    
    async loadSettings() {
        try {
            const result = await chrome.storage.sync.get(['scfSyncEnabled', 'scfServerPort']);
            this.syncEnabled = result.scfSyncEnabled || false;
            this.serverPort = result.scfServerPort || 8765;
            
            console.log('📋 SCF Settings loaded:', {
                syncEnabled: this.syncEnabled,
                serverPort: this.serverPort
            });
            
        } catch (error) {
            console.error('❌ Error loading SCF settings:', error);
        }
    }
    
    async saveSettings() {
        try {
            await chrome.storage.sync.set({
                scfSyncEnabled: this.syncEnabled,
                scfServerPort: this.serverPort
            });
        } catch (error) {
            console.error('❌ Error saving SCF settings:', error);
        }
    }
    
    async handleMessage(message, sender, sendResponse) {
        console.log('📨 SCF Background received message:', message.action);
        
        switch (message.action) {
            case 'toggleSync':
                await this.toggleSync(message.enabled);
                sendResponse({ success: true, enabled: this.syncEnabled });
                break;
                
            case 'getSyncStatus':
                sendResponse({
                    syncEnabled: this.syncEnabled,
                    serverStatus: this.localServerStatus,
                    connectedTabs: this.connectedTabs.size
                });
                break;
                
            case 'exportAllConversations':
                await this.exportAllConversations(sendResponse);
                break;
                
            case 'getConnectedTabs':
                const tabData = Array.from(this.connectedTabs.entries()).map(([tabId, data]) => ({
                    tabId,
                    ...data
                }));
                sendResponse(tabData);
                break;
                
            case 'serverHealthCheck':
                await this.checkLocalServerHealth();
                sendResponse({ status: this.localServerStatus });
                break;
                
            default:
                console.log('❓ Unknown message action:', message.action);
                sendResponse({ error: 'Unknown action' });
        }
    }
    
    async toggleSync(enabled) {
        this.syncEnabled = enabled !== undefined ? enabled : !this.syncEnabled;
        await this.saveSettings();
        
        // Notify all content scripts
        const tabs = await chrome.tabs.query({});
        for (const tab of tabs) {
            if (this.isSupportedUrl(tab.url)) {
                try {
                    await chrome.tabs.sendMessage(tab.id, {
                        action: 'toggleSync',
                        enabled: this.syncEnabled
                    });
                } catch (error) {
                    // Tab might not have content script loaded
                    console.log('Could not notify tab:', tab.id);
                }
            }
        }
        
        console.log('🔄 SCF Sync toggled:', this.syncEnabled ? 'ON' : 'OFF');
        
        // Update badge
        this.updateBadge();
    }
    
    handleTabUpdate(tabId, changeInfo, tab) {
        if (changeInfo.status === 'complete' && this.isSupportedUrl(tab.url)) {
            // Track supported tabs
            this.connectedTabs.set(tabId, {
                url: tab.url,
                title: tab.title,
                provider: this.detectProvider(tab.url),
                lastActivity: new Date().toISOString()
            });
            
            console.log('📝 SCF Tab registered:', tab.title, tab.url);
            
            // Inject content script if sync is enabled
            if (this.syncEnabled) {
                this.injectContentScript(tabId);
            }
        }
    }
    
    isSupportedUrl(url) {
        if (!url) return false;
        
        const supportedDomains = [
            'claude.ai',
            'chat.openai.com',
            'perplexity.ai',
            'gemini.google.com'
        ];
        
        return supportedDomains.some(domain => url.includes(domain));
    }
    
    detectProvider(url) {
        if (url.includes('claude.ai')) return 'claude_web';
        if (url.includes('chat.openai.com')) return 'chatgpt_web';
        if (url.includes('perplexity.ai')) return 'perplexity_web';
        if (url.includes('gemini.google.com')) return 'gemini_web';
        return 'unknown';
    }
    
    async injectContentScript(tabId) {
        try {
            await chrome.scripting.executeScript({
                target: { tabId },
                files: ['content-script.js']
            });
            console.log('✅ Content script injected into tab:', tabId);
        } catch (error) {
            console.error('❌ Failed to inject content script:', error);
        }
    }
    
    async checkLocalServerHealth() {
        try {
            const response = await fetch(`http://localhost:${this.serverPort}/health`, {
                method: 'GET',
                timeout: 5000
            });
            
            if (response.ok) {
                this.localServerStatus = 'online';
            } else {
                this.localServerStatus = 'error';
            }
            
        } catch (error) {
            this.localServerStatus = 'offline';
        }
        
        console.log('🏥 SCF Server health:', this.localServerStatus);
        this.updateBadge();
    }
    
    updateBadge() {
        let badgeText = '';
        let badgeColor = '#6b7280';
        
        if (!this.syncEnabled) {
            badgeText = 'OFF';
            badgeColor = '#ef4444';
        } else if (this.localServerStatus === 'offline') {
            badgeText = '⚠';
            badgeColor = '#f59e0b';
        } else if (this.connectedTabs.size > 0) {
            badgeText = this.connectedTabs.size.toString();
            badgeColor = '#22c55e';
        } else {
            badgeText = 'ON';
            badgeColor = '#3b82f6';
        }
        
        chrome.action.setBadgeText({ text: badgeText });
        chrome.action.setBadgeBackgroundColor({ color: badgeColor });
    }
    
    async exportAllConversations(sendResponse) {
        const allConversations = [];
        
        // Get conversation data from all connected tabs
        for (const [tabId, tabData] of this.connectedTabs) {
            try {
                const conversationData = await chrome.tabs.sendMessage(tabId, {
                    action: 'exportConversation'
                });
                
                if (conversationData) {
                    allConversations.push({
                        tabId,
                        tabData,
                        conversation: conversationData
                    });
                }
                
            } catch (error) {
                console.log('Could not get conversation from tab:', tabId);
            }
        }
        
        // Create export package
        const exportPackage = {
            exportDate: new Date().toISOString(),
            conversations: allConversations,
            metadata: {
                totalTabs: this.connectedTabs.size,
                syncEnabled: this.syncEnabled,
                serverStatus: this.localServerStatus
            }
        };
        
        sendResponse(exportPackage);
    }
}

// Initialize background service worker
const scfBackground = new SCFBackground();