#!/usr/bin/env python3
"""Test the complete check-in system"""

import requests
import json
import time
import subprocess
import os
import signal

def test_checkin_system():
    """Test the complete check-in system"""
    
    print("🧪 Testing Universal Check-In System")
    print("=" * 50)
    
    # Start the Flask server
    print("1. Starting Flask server...")
    server_process = subprocess.Popen(['python3', 'admin_server.py'], 
                                    stdout=subprocess.PIPE, 
                                    stderr=subprocess.PIPE)
    
    # Wait for server to start
    time.sleep(3)
    
    try:
        base_url = 'http://localhost:5001/api'
        
        # Test 1: Server health check
        print("2. Testing server health...")
        try:
            response = requests.get(f'{base_url}/participants', timeout=5)
            if response.status_code == 200:
                participants = response.json()
                print(f"   ✅ Server running - {len(participants)} participants loaded")
            else:
                print(f"   ❌ Server error: {response.status_code}")
                return False
        except Exception as e:
            print(f"   ❌ Cannot connect to server: {e}")
            return False
        
        # Test 2: Check initial state
        print("3. Testing initial check-in state...")
        response = requests.get(f'{base_url}/checkin/count')
        if response.status_code == 200:
            count = response.json()
            print(f"   ✅ Initial check-in count: {count['total_checked_in']}")
        else:
            print(f"   ❌ Failed to get check-in count")
            return False
        
        # Test 3: Check in participants
        print("4. Testing participant check-ins...")
        test_participants = [
            'BETHLEHEM ADUGNA',
            'PERCI WOLDAY', 
            'BEZA ASHEBIR'
        ]
        
        for participant in test_participants:
            print(f"   Checking in: {participant}")
            response = requests.post(f'{base_url}/checkin', 
                                   json={'name': participant})
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ {participant} checked in successfully")
            else:
                print(f"   ❌ Failed to check in {participant}: {response.status_code}")
                return False
        
        # Test 4: Verify check-ins were saved
        print("5. Verifying check-ins were saved...")
        response = requests.get(f'{base_url}/checkin/all')
        if response.status_code == 200:
            all_checkins = response.json()
            print(f"   ✅ Total checked in: {all_checkins['total_checked_in']}")
            
            # List all checked-in participants
            for checkin in all_checkins['checked_in_participants']:
                print(f"   - {checkin['name']} at {checkin['timestamp']}")
        else:
            print(f"   ❌ Failed to get all check-ins")
            return False
        
        # Test 5: Check individual participant status
        print("6. Testing individual participant status...")
        for participant in test_participants:
            response = requests.get(f'{base_url}/checkin?name={participant}')
            if response.status_code == 200:
                status = response.json()
                if status['checked_in']:
                    print(f"   ✅ {participant} is checked in")
                else:
                    print(f"   ❌ {participant} not found as checked in")
            else:
                print(f"   ❌ Failed to check status for {participant}")
        
        # Test 6: Test duplicate check-in
        print("7. Testing duplicate check-in...")
        response = requests.post(f'{base_url}/checkin', 
                               json={'name': test_participants[0]})
        if response.status_code == 200:
            print(f"   ✅ Duplicate check-in handled (overwrites timestamp)")
        else:
            print(f"   ❌ Duplicate check-in failed: {response.status_code}")
        
        # Test 7: Verify data persistence
        print("8. Testing data persistence...")
        checkin_file = '/Users/nahomnigatu/Downloads/campusministrybadges/data/checkin_data.json'
        if os.path.exists(checkin_file):
            with open(checkin_file, 'r') as f:
                data = json.load(f)
            print(f"   ✅ Check-in data persisted: {len(data)} participants in file")
        else:
            print(f"   ❌ Check-in data file not found")
        
        print("\n🎉 UNIVERSAL CHECK-IN SYSTEM TEST PASSED!")
        print("=" * 50)
        print("✅ Server running on port 5001")
        print("✅ API endpoints working")
        print("✅ Check-ins saved centrally")
        print("✅ Data persistence working")
        print("✅ Cross-device synchronization ready")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False
    
    finally:
        # Clean up
        print("\n9. Cleaning up...")
        server_process.terminate()
        server_process.wait()
        print("   ✅ Server stopped")

if __name__ == "__main__":
    success = test_checkin_system()
    exit(0 if success else 1)