# 🏠 LuxeRooms - Real Estate Platform Documentation

## 📁 Project Structure Overview

```
myproject/
├── 🗂️ myproject/           # Django project configuration
├── 🗂️ started/             # Main application
├── 🗂️ media/               # User uploaded files (images)
├── 📄 db.sqlite3           # Database file
├── 📄 manage.py            # Django management script
└── 📄 requirements.txt     # Python dependencies
```

## 🎯 Core Features

### 1. **User Management System**
- **Authentication**: Login, Register, Logout
- **Role-based Access**: Clients and Property Owners
- **Profile Management**: Image upload, personal info editing

### 2. **Property Listings**
- **Room Management**: Add, edit, delete property listings
- **Search & Filter**: Location, price, room type filtering
- **Voice Search**: AI-powered voice commands

### 3. **Payment Integration**
- **Stripe Integration**: Secure payment processing
- **eSewa Integration**: Local payment gateway
- **Access Control**: Pay-to-unlock room details

### 4. **Real-time Chat System**
- **WebSocket Communication**: Live messaging
- **Push Notifications**: Browser notifications
- **Chat Access Control**: Payment-gated communication

---

## 📋 Database Models (models.py)

### **UserProfile Model**
```python
# Extends Django's built-in User model with additional profile information
class UserProfile(models.Model):
    user = models.OneToOneField(User)           # Links to Django User
    profile_image = models.ImageField()         # Profile picture upload
    phone_number = models.CharField()           # Contact number
    bio = models.TextField()                    # Personal description
```

### **Owner Model**
```python
# Represents property owners who list rooms
class Owner(models.Model):
    user = models.OneToOneField(User)           # Links to User account
    phone = models.CharField()                  # Contact phone
    address = models.TextField()                # Business address
    created_at = models.DateTimeField()         # Registration date
```

### **Client Model**
```python
# Represents clients looking for rooms
class Client(models.Model):
    user = models.OneToOneField(User)           # Links to User account
    phone = models.CharField()                  # Contact phone
    preferred_location = models.CharField()     # Preferred area
    created_at = models.DateTimeField()         # Registration date
```

### **Room Model**
```python
# Core model for property listings
class Room(models.Model):
    title = models.CharField()                  # Property title
    room_type = models.CharField()              # Private/Shared/Studio/etc
    location = models.CharField()               # Property location
    price = models.DecimalField()               # Monthly rent
    description = models.TextField()            # Detailed description
    contact_phone = models.CharField()          # Owner contact
    contact_email = models.EmailField()         # Owner email
    area_m2 = models.IntegerField()            # Room size
    beds = models.IntegerField()               # Number of bedrooms
    baths = models.IntegerField()              # Number of bathrooms
    image = models.ImageField()                # Property photo
    owner = models.ForeignKey(Owner)           # Property owner
    created_at = models.DateTimeField()        # Listing date
```

### **Payment Model**
```python
# Handles all payment transactions
class Payment(models.Model):
    user = models.ForeignKey(User)              # Who made payment
    room = models.ForeignKey(Room)              # Which room (optional)
    payment_type = models.CharField()           # chat_access/room_unlock
    stripe_payment_intent_id = models.CharField() # Stripe transaction ID
    amount = models.DecimalField()              # Payment amount
    status = models.CharField()                 # pending/success/failed
    created_at = models.DateTimeField()         # Payment date
```

### **Message Model**
```python
# Real-time chat messages between users
class Message(models.Model):
    sender = models.ForeignKey(User)            # Message sender
    receiver = models.ForeignKey(User)          # Message recipient
    room = models.ForeignKey(Room)              # Related property
    content = models.TextField()                # Message text
    image = models.ImageField()                 # Optional image
    read_status = models.BooleanField()         # Read/unread status
    timestamp = models.DateTimeField()          # Message time
```

---

## 🎨 Frontend Structure

### **Templates Directory**
```
templates/started/
├── 📄 base.html                    # Main layout template
├── 📄 login.html                   # User login page
├── 📄 register.html                # User registration
├── 📄 client_dashboard.html        # Client property search
├── 📄 owner_dashboard.html         # Owner property management
├── 📄 profile_settings.html        # User profile editing
├── 📄 chat_widget.html             # Floating chat interface
└── partials/
    ├── 📄 header.html              # Navigation header
    └── 📄 footer.html              # Page footer
```

### **Static Files**
```
static/started/
├── css/
│   ├── 📄 main.css                 # Main styling (theme, layout)
│   └── 📄 chat.css                 # Chat interface styles
└── js/
    ├── 📄 main.js                  # Core JavaScript functionality
    ├── 📄 chat.js                  # Real-time chat features
    ├── 📄 notifications.js         # Push notification system
    └── 📄 sw.js                    # Service worker for offline support
```

---

## 🔧 Backend Logic (views.py)

### **Authentication Views**
```python
def login_view(request):
    # Handles user login with username/password
    # Redirects to dashboard after successful authentication

def register_view(request):
    # Creates new user accounts
    # Automatically creates UserProfile for new users
    # Validates username/email uniqueness

def logout_view(request):
    # Logs out user and redirects to login page
```

### **Dashboard Views**
```python
def client_dashboard(request):
    # Main property search interface for clients
    # Handles search filters (location, price, type)
    # Checks chat access permissions (3+ rooms + payment)
    # Returns filtered room listings

def owner_dashboard(request):
    # Property management interface for owners
    # Handles room creation and editing
    # Shows owner's property listings
```

### **Profile Management**
```python
def profile_settings(request):
    # Complete profile editing functionality
    # Handles image upload, personal info updates
    # Password change with validation
    # Username/email uniqueness checking
```

### **Payment Processing**
```python
def create_payment_intent(request):
    # Creates Stripe payment session
    # Generates secure payment intent
    # Links payment to user account

def stripe_webhook(request):
    # Handles Stripe payment confirmations
    # Updates payment status in database
    # Grants chat access after successful payment
```

### **Chat System**
```python
def get_messages(request):
    # Retrieves chat messages for a room
    # Filters by user permissions
    # Returns JSON response for AJAX calls

def mark_messages_read(request):
    # Updates message read status
    # Used for unread message counters
```

---

## 🌐 Real-time Features (WebSocket)

### **Chat Consumer (consumers.py)**
```python
class ChatConsumer(AsyncWebsocketConsumer):
    # Handles WebSocket connections for real-time chat
    # Manages chat rooms and message broadcasting
    # Saves messages to database
    # Sends notifications to offline users
```

### **WebSocket Routing (routing.py)**
```python
# Defines WebSocket URL patterns
# Routes chat connections to appropriate consumers
# Handles authentication for WebSocket connections
```

---

## 💳 Payment Integration

### **Stripe Integration**
- **Payment Intent Creation**: Secure payment processing
- **Webhook Handling**: Automatic payment confirmation
- **Access Control**: Grants features after successful payment

### **eSewa Integration**
- **Local Payment Gateway**: Nepal-specific payment method
- **Transaction Verification**: Secure payment confirmation
- **Fallback Option**: Alternative to international cards

---

## 🔔 Notification System

### **Push Notifications**
```javascript
// Service Worker (sw.js)
// Handles background notifications
// Works even when browser is closed
// Manages notification clicks and actions
```

### **Real-time Updates**
```javascript
// Chat notifications for new messages
// Payment confirmation alerts
// System status updates
```

---

## 🎨 UI/UX Features

### **Theme System**
- **Light/Dark Mode**: Toggle between themes
- **CSS Variables**: Consistent color scheme
- **Responsive Design**: Mobile-friendly interface

### **Interactive Elements**
- **Voice Search**: Speech-to-text property search
- **Drag & Drop**: File upload interface
- **Real-time Chat**: Instant messaging
- **Profile Avatars**: Circular profile pictures

---

## 🔒 Security Features

### **Authentication & Authorization**
- **CSRF Protection**: All forms protected
- **Login Required**: Sensitive pages protected
- **Role-based Access**: Client/Owner permissions

### **Payment Security**
- **Stripe Security**: PCI-compliant processing
- **Webhook Validation**: Secure payment confirmation
- **Access Control**: Payment-gated features

### **Data Protection**
- **Input Validation**: Form data sanitization
- **File Upload Security**: Image validation
- **SQL Injection Prevention**: Django ORM protection

---

## 🚀 Key Workflows

### **1. User Registration Flow**
1. User fills registration form
2. System validates username/email uniqueness
3. Creates User and UserProfile records
4. Auto-login and redirect to dashboard

### **2. Property Search Flow**
1. Client accesses dashboard
2. Uses search filters or voice search
3. System queries database with filters
4. Returns paginated results
5. Pay-to-unlock contact details

### **3. Chat Access Flow**
1. Client views 3+ properties
2. Clicks chat button
3. Payment modal appears
4. Stripe processes payment
5. Webhook confirms payment
6. Chat access granted

### **4. Real-time Messaging Flow**
1. Users connect via WebSocket
2. Messages sent through WebSocket
3. Messages saved to database
4. Real-time delivery to recipient
5. Push notifications if offline

---

## 📱 Mobile Responsiveness

### **Responsive Breakpoints**
- **Desktop**: 1200px+ (Full layout)
- **Tablet**: 768px-1199px (Adapted layout)
- **Mobile**: <768px (Stacked layout)

### **Mobile Features**
- **Touch-friendly**: Large buttons and touch targets
- **Swipe Gestures**: Mobile navigation
- **Optimized Chat**: Mobile-first chat interface

---

## 🔧 Development Setup

### **Required Dependencies**
```
Django>=4.2              # Web framework
Pillow                   # Image processing
channels>=4.0.0          # WebSocket support
channels-redis>=4.1.0    # Redis for WebSocket
redis>=4.5.0             # In-memory database
stripe>=5.0.0            # Payment processing
```

### **Environment Setup**
1. Install Python 3.10+
2. Install Redis server
3. Run `pip install -r requirements.txt`
4. Configure Stripe API keys
5. Run migrations: `python manage.py migrate`
6. Start server: `python manage.py runserver`

---

## 🎯 Future Enhancements

### **Planned Features**
- **Advanced Search**: Map integration, radius search
- **Review System**: User ratings and reviews
- **Booking System**: Calendar-based room booking
- **Multi-language**: Internationalization support
- **Mobile App**: React Native mobile application

### **Performance Optimizations**
- **Database Indexing**: Query optimization
- **Caching**: Redis caching for frequent queries
- **CDN Integration**: Static file delivery
- **Image Optimization**: Automatic image compression

---

This documentation provides a comprehensive overview of the LuxeRooms platform architecture, helping you understand the codebase structure and functionality.