// SCF Browser Extension - Content Script
// Captures web LLM conversations and syncs with local buildstate

class SCFWebSync {
    constructor() {
        this.conversationData = {
            messages: [],
            title: '',
            provider: this.detectProvider(),
            url: window.location.href,
            startTime: new Date().toISOString()
        };
        
        this.observer = null;
        this.syncEnabled = false;
        this.localServerPort = 8765;
        
        this.init();
    }
    
    init() {
        console.log('🎼 SCF Universal Context Sync - Initializing...');
        
        // Check if SCF sync is enabled
        chrome.storage.sync.get(['scfSyncEnabled'], (result) => {
            this.syncEnabled = result.scfSyncEnabled || false;
            if (this.syncEnabled) {
                this.startMonitoring();
            }
        });
        
        // Listen for sync enable/disable
        chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
            if (message.action === 'toggleSync') {
                this.syncEnabled = message.enabled;
                if (this.syncEnabled) {
                    this.startMonitoring();
                } else {
                    this.stopMonitoring();
                }
            } else if (message.action === 'exportConversation') {
                sendResponse(this.conversationData);
            }
        });
    }
    
    detectProvider() {
        const hostname = window.location.hostname;
        
        if (hostname.includes('claude.ai')) return 'claude_web';
        if (hostname.includes('chat.openai.com')) return 'chatgpt_web';
        if (hostname.includes('perplexity.ai')) return 'perplexity_web';
        if (hostname.includes('gemini.google.com')) return 'gemini_web';
        
        return 'unknown';
    }
    
    startMonitoring() {
        console.log('🔍 SCF: Starting conversation monitoring...');
        
        // Get conversation title
        this.updateConversationTitle();
        
        // Monitor for new messages
        this.observeMessages();
        
        // Periodically sync with local SCF
        this.startPeriodicSync();
        
        // Show sync indicator
        this.showSyncIndicator();
    }
    
    stopMonitoring() {
        console.log('⏹️ SCF: Stopping conversation monitoring...');
        
        if (this.observer) {
            this.observer.disconnect();
        }
        
        this.hideSyncIndicator();
    }
    
    updateConversationTitle() {
        // Provider-specific title detection
        let titleSelector;
        
        switch (this.conversationData.provider) {
            case 'claude_web':
                titleSelector = 'h1, [data-testid="conversation-title"], .conversation-title';
                break;
            case 'chatgpt_web':
                titleSelector = 'h1, .conversation-header h1, [data-testid="conversation-turn-title"]';
                break;
            default:
                titleSelector = 'h1, title';
        }
        
        const titleElement = document.querySelector(titleSelector);
        if (titleElement) {
            this.conversationData.title = titleElement.textContent.trim();
        } else {
            this.conversationData.title = document.title;
        }
    }
    
    observeMessages() {
        // Provider-specific message container selectors
        let messageContainerSelector;
        let messageSelector;
        
        switch (this.conversationData.provider) {
            case 'claude_web':
                messageContainerSelector = '[data-testid="conversation"], .conversation-container';
                messageSelector = '[data-testid="message"], .message';
                break;
            case 'chatgpt_web':
                messageContainerSelector = '[data-testid="conversation-turn"], .conversation-content';
                messageSelector = '[data-message-author-role], .message-content';
                break;
            default:
                messageContainerSelector = 'body';
                messageSelector = '.message, [role="article"]';
        }
        
        const container = document.querySelector(messageContainerSelector);
        if (!container) {
            console.log('⚠️ SCF: Could not find message container');
            return;
        }
        
        // Observe for new messages
        this.observer = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                mutation.addedNodes.forEach((node) => {
                    if (node.nodeType === Node.ELEMENT_NODE) {
                        const messages = node.querySelectorAll(messageSelector);
                        messages.forEach((message) => {
                            this.processMessage(message);
                        });
                    }
                });
            });
        });
        
        this.observer.observe(container, {
            childList: true,
            subtree: true
        });
        
        // Process existing messages
        const existingMessages = container.querySelectorAll(messageSelector);
        existingMessages.forEach((message) => {
            this.processMessage(message);
        });
    }
    
    processMessage(messageElement) {
        // Extract message content and metadata
        const messageData = {
            content: this.extractMessageContent(messageElement),
            author: this.extractMessageAuthor(messageElement),
            timestamp: new Date().toISOString(),
            element_id: this.generateElementId(messageElement)
        };
        
        // Avoid duplicates
        if (!this.conversationData.messages.some(m => m.element_id === messageData.element_id)) {
            this.conversationData.messages.push(messageData);
            
            // Check if this message contains insights or decisions
            this.analyzeMessageForInsights(messageData);
        }
    }
    
    extractMessageContent(messageElement) {
        // Remove script tags and other non-content elements
        const cloned = messageElement.cloneNode(true);
        const scriptsAndStyles = cloned.querySelectorAll('script, style, .button, button');
        scriptsAndStyles.forEach(el => el.remove());
        
        return cloned.textContent.trim();
    }
    
    extractMessageAuthor(messageElement) {
        // Provider-specific author detection
        switch (this.conversationData.provider) {
            case 'claude_web':
                return messageElement.closest('[data-testid="message"]')?.getAttribute('data-author') || 
                       (messageElement.textContent.includes('Claude:') ? 'assistant' : 'user');
            case 'chatgpt_web':
                return messageElement.getAttribute('data-message-author-role') || 'unknown';
            default:
                return 'unknown';
        }
    }
    
    generateElementId(element) {
        // Generate unique ID for element to avoid duplicates
        const content = element.textContent.trim();
        return btoa(content.substring(0, 50)).replace(/[^a-zA-Z0-9]/g, '').substring(0, 12);
    }
    
    analyzeMessageForInsights(messageData) {
        const content = messageData.content.toLowerCase();
        
        // Look for insight patterns
        const insightPatterns = [
            /i learned that/i,
            /key insight/i,
            /this means/i,
            /important point/i,
            /conclusion:/i
        ];
        
        // Look for decision patterns
        const decisionPatterns = [
            /i'll|i will/i,
            /let's/i,
            /we should/i,
            /decision:/i,
            /going with/i
        ];
        
        if (insightPatterns.some(pattern => pattern.test(content))) {
            messageData.type = 'insight';
        } else if (decisionPatterns.some(pattern => pattern.test(content))) {
            messageData.type = 'decision';
        }
        
        // If it's an insight or decision, trigger immediate sync
        if (messageData.type) {
            this.triggerImmediateSync();
        }
    }
    
    startPeriodicSync() {
        // Sync every 30 seconds if there are new messages
        setInterval(() => {
            if (this.conversationData.messages.length > 0) {
                this.syncWithLocal();
            }
        }, 30000);
    }
    
    triggerImmediateSync() {
        console.log('⚡ SCF: Triggering immediate sync due to insight/decision...');
        this.syncWithLocal();
    }
    
    async syncWithLocal() {
        try {
            // Send conversation data to local SCF server
            const response = await fetch(`http://localhost:${this.localServerPort}/sync`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    action: 'sync_conversation',
                    data: this.conversationData
                })
            });
            
            if (response.ok) {
                const result = await response.json();
                console.log('✅ SCF: Synced with local buildstate', result);
                this.updateSyncStatus('synced');
            } else {
                console.log('⚠️ SCF: Sync failed', response.status);
                this.updateSyncStatus('failed');
            }
            
        } catch (error) {
            console.log('⚠️ SCF: Local server not available', error);
            this.updateSyncStatus('offline');
        }
    }
    
    showSyncIndicator() {
        // Create floating sync indicator
        const indicator = document.createElement('div');
        indicator.id = 'scf-sync-indicator';
        indicator.innerHTML = `
            <div style="
                position: fixed;
                top: 20px;
                right: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 8px 12px;
                border-radius: 20px;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui;
                font-size: 12px;
                font-weight: 500;
                box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
                z-index: 10000;
                cursor: pointer;
                transition: all 0.3s ease;
            " title="SCF Context Sync Active - Click for details">
                🎼 SCF Sync
                <span id="scf-status">●</span>
            </div>
        `;
        
        document.body.appendChild(indicator);
        
        // Add click handler
        indicator.addEventListener('click', () => {
            this.showSyncDetails();
        });
        
        this.updateSyncStatus('active');
    }
    
    hideSyncIndicator() {
        const indicator = document.getElementById('scf-sync-indicator');
        if (indicator) {
            indicator.remove();
        }
    }
    
    updateSyncStatus(status) {
        const statusElement = document.getElementById('scf-status');
        if (!statusElement) return;
        
        const colors = {
            'active': '#22c55e',    // Green
            'synced': '#3b82f6',    // Blue  
            'failed': '#ef4444',    // Red
            'offline': '#f59e0b'    // Orange
        };
        
        statusElement.style.color = colors[status] || '#6b7280';
        
        const titles = {
            'active': 'SCF monitoring active',
            'synced': 'Recently synced with buildstate',
            'failed': 'Sync failed - check connection',
            'offline': 'Local SCF server offline'
        };
        
        statusElement.parentElement.title = titles[status] || 'SCF Context Sync';
    }
    
    showSyncDetails() {
        // Show popup with sync details
        const popup = document.createElement('div');
        popup.innerHTML = `
            <div style="
                position: fixed;
                top: 60px;
                right: 20px;
                background: white;
                border: 1px solid #e5e7eb;
                border-radius: 12px;
                padding: 20px;
                box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
                z-index: 10001;
                width: 300px;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui;
            ">
                <h3 style="margin: 0 0 15px 0; color: #1f2937;">🎼 SCF Context Sync</h3>
                <div style="font-size: 14px; color: #6b7280; margin-bottom: 15px;">
                    <div><strong>Provider:</strong> ${this.conversationData.provider}</div>
                    <div><strong>Messages:</strong> ${this.conversationData.messages.length}</div>
                    <div><strong>Insights:</strong> ${this.conversationData.messages.filter(m => m.type === 'insight').length}</div>
                    <div><strong>Decisions:</strong> ${this.conversationData.messages.filter(m => m.type === 'decision').length}</div>
                </div>
                <button id="scf-export-btn" style="
                    background: #667eea;
                    color: white;
                    border: none;
                    padding: 8px 16px;
                    border-radius: 6px;
                    cursor: pointer;
                    font-size: 14px;
                    margin-right: 10px;
                ">Export Conversation</button>
                <button id="scf-close-btn" style="
                    background: #f3f4f6;
                    color: #374151;
                    border: none;
                    padding: 8px 16px;
                    border-radius: 6px;
                    cursor: pointer;
                    font-size: 14px;
                ">Close</button>
            </div>
        `;
        
        document.body.appendChild(popup);
        
        // Add event handlers
        popup.querySelector('#scf-export-btn').addEventListener('click', () => {
            this.exportConversation();
            popup.remove();
        });
        
        popup.querySelector('#scf-close-btn').addEventListener('click', () => {
            popup.remove();
        });
        
        // Auto-hide after 10 seconds
        setTimeout(() => {
            if (popup.parentNode) {
                popup.remove();
            }
        }, 10000);
    }
    
    exportConversation() {
        // Export conversation data as JSON file
        const dataStr = JSON.stringify(this.conversationData, null, 2);
        const dataBlob = new Blob([dataStr], { type: 'application/json' });
        
        const link = document.createElement('a');
        link.href = URL.createObjectURL(dataBlob);
        link.download = `scf-conversation-${this.conversationData.provider}-${new Date().toISOString().slice(0, 10)}.json`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        
        console.log('📁 SCF: Conversation exported');
    }
}

// Initialize SCF Web Sync when page loads
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        new SCFWebSync();
    });
} else {
    new SCFWebSync();
}