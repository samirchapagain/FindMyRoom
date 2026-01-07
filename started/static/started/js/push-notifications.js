// Push Notifications Service
class PushNotificationService {
    constructor() {
        this.isSupported = 'Notification' in window;
        this.permission = this.isSupported ? Notification.permission : 'denied';
    }

    async requestPermission() {
        if (!this.isSupported) {
            console.warn('Push notifications not supported');
            return false;
        }

        if (this.permission === 'granted') {
            return true;
        }

        const permission = await Notification.requestPermission();
        this.permission = permission;
        return permission === 'granted';
    }

    showNotification(title, options = {}) {
        if (!this.isSupported || this.permission !== 'granted') {
            return;
        }

        const defaultOptions = {
            icon: '/static/started/images/notification-icon.png',
            badge: '/static/started/images/badge-icon.png',
            tag: 'chat-message',
            requireInteraction: false,
            silent: false
        };

        const notificationOptions = { ...defaultOptions, ...options };

        // Check if page is visible
        if (document.hidden) {
            new Notification(title, notificationOptions);
        }
    }

    showChatNotification(senderName, message, roomId) {
        this.showNotification(`New message from ${senderName}`, {
            body: message,
            tag: `chat-${roomId}`,
            data: { roomId, type: 'chat' },
            actions: [
                {
                    action: 'reply',
                    title: 'Reply'
                },
                {
                    action: 'view',
                    title: 'View Chat'
                }
            ]
        });
    }

    showPaymentNotification(message) {
        this.showNotification('Payment Successful', {
            body: message,
            tag: 'payment-success',
            data: { type: 'payment' },
            icon: '/static/started/images/success-icon.png'
        });
    }
}

// Initialize notification service
const notificationService = new PushNotificationService();

// Request permission on page load
document.addEventListener('DOMContentLoaded', function() {
    // Request notification permission after user interaction
    document.addEventListener('click', function requestNotificationPermission() {
        notificationService.requestPermission();
        // Remove listener after first click
        document.removeEventListener('click', requestNotificationPermission);
    }, { once: true });
});

// Export for global use
window.notificationService = notificationService;