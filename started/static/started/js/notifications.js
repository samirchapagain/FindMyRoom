// Push Notifications Service Worker Registration
class NotificationManager {
    constructor() {
        this.init();
    }
    
    async init() {
        if ('serviceWorker' in navigator && 'PushManager' in window) {
            try {
                const registration = await navigator.serviceWorker.register('/static/started/js/sw.js');
                console.log('Service Worker registered:', registration);
                
                // Request notification permission
                await this.requestNotificationPermission();
                
            } catch (error) {
                console.error('Service Worker registration failed:', error);
            }
        }
    }
    
    async requestNotificationPermission() {
        if (Notification.permission === 'default') {
            const permission = await Notification.requestPermission();
            
            if (permission === 'granted') {
                console.log('Notification permission granted');
                this.showWelcomeNotification();
            } else {
                console.log('Notification permission denied');
            }
        }
    }
    
    showWelcomeNotification() {
        if (Notification.permission === 'granted') {
            new Notification('Chat Notifications Enabled', {
                body: 'You will receive notifications for new messages',
                icon: '/static/started/images/chat-icon.png',
                tag: 'welcome'
            });
        }
    }
    
    async showNotification(title, options = {}) {
        if ('serviceWorker' in navigator && Notification.permission === 'granted') {
            const registration = await navigator.serviceWorker.ready;
            
            const defaultOptions = {
                body: '',
                icon: '/static/started/images/chat-icon.png',
                badge: '/static/started/images/badge-icon.png',
                tag: 'chat-message',
                requireInteraction: true,
                actions: [
                    {
                        action: 'open',
                        title: 'Open Chat'
                    },
                    {
                        action: 'close',
                        title: 'Dismiss'
                    }
                ]
            };
            
            const finalOptions = { ...defaultOptions, ...options };
            
            registration.showNotification(title, finalOptions);
        }
    }
}

// Initialize notification manager
document.addEventListener('DOMContentLoaded', () => {
    window.notificationManager = new NotificationManager();
});

// Handle notification clicks
if ('serviceWorker' in navigator) {
    navigator.serviceWorker.addEventListener('message', event => {
        if (event.data && event.data.type === 'NOTIFICATION_CLICK') {
            // Open chat when notification is clicked
            if (window.chatManager) {
                window.chatManager.openChat();
            }
        }
    });
}