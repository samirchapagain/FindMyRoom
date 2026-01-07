# LuxeRooms - Quick Setup Guide

## Prerequisites
- Python 3.8+ installed
- Redis server (for WebSocket functionality)

## Quick Start

### Option 1: Using Batch File (Windows)
```bash
# Double-click or run in command prompt
setup_and_run.bat
```

### Option 2: Manual Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Run database migrations
python manage.py migrate

# Create admin user (optional)
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

### Option 3: Using Python Script
```bash
python run_server.py
```

## Access the Website
- Main site: http://127.0.0.1:8000
- Admin panel: http://127.0.0.1:8000/admin

## Features Available
- Room listings and search
- User authentication (login/register)
- Client and Owner dashboards
- Chat functionality (requires Redis)
- Payment integration (Stripe/eSewa)

## Notes
- For chat functionality, install and start Redis server
- For payments, configure Stripe keys in settings.py
- Default database is SQLite (no additional setup needed)