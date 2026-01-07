#!/usr/bin/env python
"""
Test script for eSewa payment integration
Run this after setting up the database and starting the server
"""

import requests
import json
import time

# Test configuration
BASE_URL = 'http://127.0.0.1:8000'
TEST_USER = {
    'username': 'testclient',
    'password': 'testpass123',
    'email': 'test@example.com'
}

def test_payment_flow():
    """Test the complete payment flow"""
    print("🧪 Testing eSewa Payment Integration")
    print("=" * 50)
    
    # Test 1: Create payment intent
    print("\n1. Testing payment intent creation...")
    
    session = requests.Session()
    
    # Login first (you'll need to implement this based on your auth)
    login_data = {
        'username': TEST_USER['username'],
        'password': TEST_USER['password']
    }
    
    try:
        # Test payment intent creation
        payment_data = {
            'room_id': 1  # Assuming room ID 1 exists
        }
        
        response = session.post(
            f'{BASE_URL}/create-payment-intent/',
            json=payment_data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Payment intent created: {data.get('transaction_id')}")
            transaction_id = data.get('transaction_id')
        else:
            print(f"❌ Payment intent failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error creating payment intent: {e}")
        return False
    
    # Test 2: Simulate eSewa webhook
    print("\n2. Testing eSewa webhook verification...")
    
    try:
        webhook_data = {
            'oid': transaction_id,
            'amt': '30',
            'refId': f'TEST_REF_{int(time.time())}'
        }
        
        response = session.post(
            f'{BASE_URL}/esewa-webhook/',
            data=webhook_data
        )
        
        if response.status_code == 200:
            print("✅ Webhook verification successful")
        else:
            print(f"❌ Webhook verification failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error testing webhook: {e}")
    
    # Test 3: Check room unlock status
    print("\n3. Testing room unlock status...")
    
    try:
        unlock_data = {'room_id': 1}
        
        response = session.post(
            f'{BASE_URL}/unlock/',
            json=unlock_data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("✅ Room successfully unlocked")
                print(f"   Contact details available: {data.get('contact_details', {}).keys()}")
            else:
                print(f"⚠️  Room unlock status: {data.get('error')}")
        else:
            print(f"❌ Room unlock check failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error checking room unlock: {e}")
    
    print("\n" + "=" * 50)
    print("🏁 Payment flow test completed")

def test_chat_api():
    """Test chat API endpoints"""
    print("\n🧪 Testing Chat API")
    print("=" * 30)
    
    session = requests.Session()
    
    # Test message sending
    try:
        message_data = {
            'room_id': 1,
            'content': 'Test message from API'
        }
        
        response = session.post(
            f'{BASE_URL}/api/messages/send/',
            json=message_data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            print("✅ Message sent successfully")
        else:
            print(f"❌ Message sending failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error sending message: {e}")
    
    # Test message retrieval
    try:
        response = session.get(f'{BASE_URL}/api/messages/?room_id=1')
        
        if response.status_code == 200:
            data = response.json()
            message_count = len(data.get('messages', []))
            print(f"✅ Retrieved {message_count} messages")
        else:
            print(f"❌ Message retrieval failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error retrieving messages: {e}")

if __name__ == '__main__':
    print("🚀 Starting Payment & Chat Integration Tests")
    print("Make sure your Django server is running on http://127.0.0.1:8000")
    print("Press Enter to continue or Ctrl+C to cancel...")
    
    try:
        input()
        test_payment_flow()
        test_chat_api()
        
        print("\n📋 Manual Testing Checklist:")
        print("□ Register as client and owner")
        print("□ Create a room as owner") 
        print("□ Browse rooms as client")
        print("□ Click unlock button")
        print("□ Complete eSewa payment")
        print("□ Verify chat unlock")
        print("□ Send messages in chat")
        print("□ Test push notifications")
        
    except KeyboardInterrupt:
        print("\n❌ Test cancelled by user")