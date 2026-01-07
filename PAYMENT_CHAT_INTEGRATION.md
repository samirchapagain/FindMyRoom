# eSewa Payment & Real-Time Chat Integration

## Overview
Complete payment-gated chat system with eSewa integration, real-time messaging, and secure verification.

## Features Implemented

### 1. Payment System
- **eSewa Integration**: Test mode with QR code payment
- **Fixed Amount**: Rs. 30 for room unlock
- **Server-side Verification**: Webhook validates payment with eSewa API
- **Database Tracking**: ClientPayment model tracks all transactions

### 2. Real-Time Chat
- **WebSocket Integration**: Django Channels for instant messaging
- **Payment-Gated Access**: Chat only available after successful payment
- **Push Notifications**: Browser notifications for offline users
- **Message History**: Persistent chat storage

### 3. Security
- **Payment Verification**: Cross-checks with eSewa API before approval
- **Access Control**: Only paid clients can chat with specific owners
- **Transaction Tracking**: Unique transaction IDs prevent replay attacks

## Database Schema

### ClientPayment Model
```python
class ClientPayment(models.Model):
    client = ForeignKey(Client)
    owner = ForeignKey(Owner) 
    room = ForeignKey(Room)
    amount = DecimalField(default=30.00)
    status = CharField(choices=['pending', 'success', 'failed'])
    transaction_id = CharField(unique=True)
    esewa_ref_id = CharField()
    paid_at = DateTimeField()
    created_at = DateTimeField()
```

### Message Model
```python
class Message(models.Model):
    sender = ForeignKey(User, related_name='sent_messages')
    receiver = ForeignKey(User, related_name='received_messages')
    room = ForeignKey(Room)
    content = TextField()
    image = ImageField()
    read_status = BooleanField(default=False)
    timestamp = DateTimeField()
```

## API Endpoints

### Payment Endpoints
- `POST /create-payment-intent/` - Initialize payment
- `GET /esewa-success/` - Payment success callback
- `GET /esewa-failure/` - Payment failure callback
- `POST /esewa-webhook/` - Server verification webhook

### Chat Endpoints
- `GET /api/messages/?room_id=X` - Get message history
- `POST /api/messages/send/` - Send message
- `POST /api/messages/read/` - Mark messages as read
- `GET /api/unread-count/` - Get unread count

### WebSocket Routes
- `ws/chat/{room_id}/` - Real-time chat
- `ws/payment/` - Payment notifications

## Integration Steps

### 1. Database Migration
```bash
py manage.py makemigrations started
py manage.py migrate
```

### 2. Settings Configuration
```python
# settings.py
INSTALLED_APPS = [
    'channels',
    'started',
]

ASGI_APPLICATION = 'myproject.asgi.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer'
    }
}
```

### 3. URL Configuration
```python
# urls.py - Already updated with all endpoints
```

### 4. Template Integration
- Payment modal included in client dashboard
- Chat interface component with Tailwind CSS
- Push notification service

## Testing Instructions

### 1. Development Setup
```bash
# Install dependencies
pip install channels requests

# Run migrations
py manage.py makemigrations started
py manage.py migrate

# Start development server
py manage.py runserver
```

### 2. Test Payment Flow
1. **Register as Client**: Create client account
2. **Browse Rooms**: View available rooms
3. **Click Unlock**: Triggers payment modal
4. **eSewa Payment**: 
   - Use test credentials: `9806800001` / `Nepal@123`
   - Or scan QR code with eSewa app
5. **Verify Success**: Room unlocks with contact details
6. **Start Chat**: Click "Start Chat" button

### 3. Test Chat System
1. **Open Chat Interface**: Click chat button on unlocked room
2. **Send Messages**: Type and send messages
3. **Real-time Updates**: Messages appear instantly
4. **Push Notifications**: Test with browser tab in background
5. **Message History**: Refresh and verify persistence

### 4. Test Security
1. **Access Control**: Try accessing chat without payment
2. **Payment Verification**: Check database for correct status
3. **Cross-Client Security**: Ensure clients can't access other's chats

## eSewa Test Environment

### Test Credentials
- **Merchant Code**: `EPAYTEST`
- **Test URL**: `https://uat.esewa.com.np/epay/main`
- **Verification URL**: `https://uat.esewa.com.np/epay/transrec`

### Test User Account
- **Phone**: `9806800001`
- **Password**: `Nepal@123`
- **PIN**: `1234`

## Production Deployment

### 1. eSewa Production Setup
```python
# Change to production URLs
ESEWA_PAYMENT_URL = 'https://esewa.com.np/epay/main'
ESEWA_VERIFICATION_URL = 'https://esewa.com.np/epay/transrec'
ESEWA_MERCHANT_CODE = 'YOUR_MERCHANT_CODE'
```

### 2. WebSocket Configuration
```python
# Use Redis for production
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('127.0.0.1', 6379)],
        },
    },
}
```

### 3. Security Headers
```python
# Add CSRF exemption for webhooks
CSRF_TRUSTED_ORIGINS = ['https://esewa.com.np']
```

## File Structure
```
started/
├── models.py              # ClientPayment, Message models
├── views.py               # Payment & chat views
├── consumers.py           # WebSocket consumers
├── urls.py                # API endpoints
├── admin.py               # Admin interface
├── templates/started/
│   ├── payment_modal.html # Payment interface
│   ├── chat_interface.html # Chat component
│   └── client_dashboard.html # Updated dashboard
└── static/started/js/
    └── push-notifications.js # Browser notifications
```

## Key Features Summary

✅ **eSewa Payment Integration** - Test mode with QR code
✅ **Payment Verification** - Server-side webhook validation  
✅ **Real-time Chat** - WebSocket messaging system
✅ **Push Notifications** - Browser notifications for offline users
✅ **Security Controls** - Payment-gated access with verification
✅ **Tailwind CSS UI** - Modern, responsive interface
✅ **Message Persistence** - Chat history storage
✅ **Transaction Tracking** - Complete payment audit trail

The system is now ready for testing and can be easily switched to production mode by updating the eSewa URLs and merchant credentials.