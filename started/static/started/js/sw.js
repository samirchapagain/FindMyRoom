// Service Worker for Push Notifications
const CACHE_NAME = 'chat-notifications-v1';

self.addEventListener('install', event => {
    console.log('Service Worker installing');
    self.skipWaiting();
});

self.addEventListener('activate', event => {
    console.log('Service Worker activating');
    event.waitUntil(self.clients.claim());
});

self.addEventListener('push', event => {
    console.log('Push event received:', event);
    
    let data = {};
    if (event.data) {
        data = event.data.json();
    }
    
    const title = data.title || 'New Message';
    const options = {
        body: data.body || 'You have a new message',
        icon: data.icon || '/static/started/images/chat-icon.png',
        badge: data.badge || '/static/started/images/badge-icon.png',
        tag: data.tag || 'chat-message',
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
        ],
        data: {
            url: data.url || '/',
            room_id: data.room_id
        }
    };
    
    event.waitUntil(
        self.registration.showNotification(title, options)
    );
});

self.addEventListener('notificationclick', event => {
    console.log('Notification clicked:', event);
    
    event.notification.close();
    
    if (event.action === 'open' || !event.action) {
        // Open the chat or focus existing window
        event.waitUntil(
            clients.matchAll({ type: 'window' }).then(clientList => {
                // Check if there's already a window open
                for (let client of clientList) {
                    if (client.url.includes(event.notification.data.url) && 'focus' in client) {
                        // Send message to open chat
                        client.postMessage({
                            type: 'NOTIFICATION_CLICK',
                            room_id: event.notification.data.room_id
                        });
                        return client.focus();
                    }
                }
                
                // Open new window if none exists
                if (clients.openWindow) {
                    return clients.openWindow(event.notification.data.url);
                }
            })
        );
    }
});

self.addEventListener('notificationclose', event => {
    console.log('Notification closed:', event);
});

// Handle background sync for offline message sending
self.addEventListener('sync', event => {
    if (event.tag === 'background-sync-messages') {
        event.waitUntil(syncMessages());
    }
});

async function syncMessages() {
    // Implementation for syncing messages when back online
    console.log('Syncing messages...');
}