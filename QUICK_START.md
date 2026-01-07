# 🚀 LuxeRooms - Quick Start Guide

## Run Your Website in 3 Steps:

### Step 1: Start the Website
```bash
# Double-click this file or run in command prompt:
start_website.bat
```

### Step 2: Create Admin User (Optional)
```bash
python create_admin.py
```

### Step 3: Access Your Website
- **Main Website**: http://127.0.0.1:8000
- **Admin Panel**: http://127.0.0.1:8000/admin

## 🎯 What You Can Do:

### For Users:
- **Register** as Client or Owner
- **Browse** room listings
- **Search** rooms by location, price, type
- **Chat** with room owners (after payment)
- **Make payments** via eSewa

### For Owners:
- **Add** room listings
- **Manage** your rooms
- **Chat** with interested clients
- **View** payment notifications

### For Admins:
- **Manage** all users and rooms
- **View** payments and transactions
- **Monitor** system activity

## 🔧 Features Available:
- ✅ User Authentication (Login/Register)
- ✅ Room Listings & Search
- ✅ Real-time Chat (WebSocket)
- ✅ Payment Integration (eSewa)
- ✅ File Uploads (Room Images)
- ✅ Email Notifications
- ✅ Mobile Responsive Design

## 📝 Default Test Accounts:
After running the website, you can register new accounts or create admin users using the provided script.

## 🛠️ Troubleshooting:
- If port 8000 is busy, the server will automatically use another port
- For chat functionality, Redis server is recommended but not required for basic features
- Check console output for any error messages

**Enjoy your LuxeRooms platform! 🏠✨**