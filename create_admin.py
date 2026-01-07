#!/usr/bin/env python
"""
Script to create admin user for Django
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.contrib.auth.models import User
from started.models import UserProfile, Owner

def create_admin():
    username = input("Enter admin username: ")
    email = input("Enter admin email: ")
    password = input("Enter admin password: ")
    
    if User.objects.filter(username=username).exists():
        print(f"User {username} already exists!")
        return
    
    user = User.objects.create_superuser(username=username, email=email, password=password)
    UserProfile.objects.create(user=user)
    
    print(f"Admin user '{username}' created successfully!")
    print(f"You can now login at: http://127.0.0.1:8000/admin")

if __name__ == '__main__':
    create_admin()