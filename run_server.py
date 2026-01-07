#!/usr/bin/env python
"""
Simple script to run the Django development server
"""
import os
import sys
import subprocess

def main():
    # Set Django settings module
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
    
    print("Starting LuxeRooms Django Server...")
    print("=" * 50)
    
    try:
        # Run migrations first
        print("Running database migrations...")
        subprocess.run([sys.executable, 'manage.py', 'migrate'], check=True)
        
        # Create superuser if needed (optional)
        print("\nStarting development server...")
        print("Server will be available at: http://127.0.0.1:8000")
        print("Admin panel: http://127.0.0.1:8000/admin")
        print("Press Ctrl+C to stop the server")
        print("=" * 50)
        
        # Start the development server
        subprocess.run([sys.executable, 'manage.py', 'runserver'], check=True)
        
    except KeyboardInterrupt:
        print("\nServer stopped.")
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()