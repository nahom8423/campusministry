#!/usr/bin/env python3
"""Test the cross-device check-in fix"""

import requests
import subprocess
import time
import socket
import json

def get_network_ip():
    """Get the laptop's network IP address"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return None

def test_cross_device_checkin():
    """Test cross-device check-in functionality"""
    
    print('🧪 TESTING CROSS-DEVICE CHECK-IN FIX')
    print('=' * 50)
    
    # Get network IP
    laptop_ip = get_network_ip()
    if not laptop_ip:
        print('❌ Could not determine network IP')
        return False
    
    print(f'📱 Laptop IP: {laptop_ip}')
    print(f'💻 Laptop URL: http://localhost:5001')
    print(f'📱 Phone URL: http://{laptop_ip}:5001')
    
    # Start Flask server
    print('\n🔄 Starting Flask server...')
    try:
        server_process = subprocess.Popen(['python3', 'admin_server.py'], 
                                        stdout=subprocess.PIPE, 
                                        stderr=subprocess.PIPE)
        time.sleep(3)  # Wait for server to start
        
        # Test 1: Laptop check-in via localhost
        print('\n💻 TEST 1: Laptop check-in (localhost)')
        test_participant_1 = 'BETHLEHEM ADUGNA'
        
        try:
            checkin_data = {'name': test_participant_1}
            response = requests.post('http://localhost:5001/api/checkin', 
                                   json=checkin_data, timeout=5)
            if response.status_code == 200:
                print(f'   ✅ Laptop check-in successful: {test_participant_1}')
            else:
                print(f'   ❌ Laptop check-in failed: {response.status_code}')
                return False
        except Exception as e:
            print(f'   ❌ Laptop check-in error: {e}')
            return False
        
        # Test 2: Phone can see laptop check-in via network IP
        print(f'\n📱 TEST 2: Phone sees laptop check-in (network IP)')
        try:
            response = requests.get(f'http://{laptop_ip}:5001/api/checkin/all', timeout=5)
            if response.status_code == 200:
                checkins = response.json()
                if any(p['name'] == test_participant_1 for p in checkins['checked_in_participants']):
                    print(f'   ✅ Phone can see laptop check-in: {test_participant_1}')
                else:
                    print(f'   ❌ Phone cannot see laptop check-in')
                    return False
            else:
                print(f'   ❌ Phone cannot access check-in list: {response.status_code}')
                return False
        except Exception as e:
            print(f'   ❌ Phone access error: {e}')
            return False
        
        # Test 3: Phone check-in via network IP
        print(f'\n📱 TEST 3: Phone check-in (network IP)')
        test_participant_2 = 'PERCI WOLDAY'
        
        try:
            checkin_data = {'name': test_participant_2}
            response = requests.post(f'http://{laptop_ip}:5001/api/checkin', 
                                   json=checkin_data, timeout=5)
            if response.status_code == 200:
                print(f'   ✅ Phone check-in successful: {test_participant_2}')
            else:
                print(f'   ❌ Phone check-in failed: {response.status_code}')
                return False
        except Exception as e:
            print(f'   ❌ Phone check-in error: {e}')
            return False
        
        # Test 4: Laptop can see phone check-in via localhost
        print(f'\n💻 TEST 4: Laptop sees phone check-in (localhost)')
        try:
            response = requests.get('http://localhost:5001/api/checkin/all', timeout=5)
            if response.status_code == 200:
                checkins = response.json()
                phone_checkin_visible = any(p['name'] == test_participant_2 for p in checkins['checked_in_participants'])
                laptop_checkin_visible = any(p['name'] == test_participant_1 for p in checkins['checked_in_participants'])
                
                if phone_checkin_visible and laptop_checkin_visible:
                    print(f'   ✅ Laptop can see both check-ins:')
                    print(f'      - {test_participant_1} (from laptop)')
                    print(f'      - {test_participant_2} (from phone)')
                    print(f'   ✅ UNIVERSAL SYNC WORKING!')
                    return True
                else:
                    print(f'   ❌ Laptop cannot see all check-ins')
                    print(f'      - Laptop checkin visible: {laptop_checkin_visible}')
                    print(f'      - Phone checkin visible: {phone_checkin_visible}')
                    return False
            else:
                print(f'   ❌ Laptop cannot access check-in list: {response.status_code}')
                return False
        except Exception as e:
            print(f'   ❌ Laptop access error: {e}')
            return False
            
    finally:
        # Clean up
        print('\n🧹 Cleaning up...')
        try:
            server_process.terminate()
            server_process.wait()
        except:
            pass
    
    return False

def create_setup_instructions():
    """Create setup instructions for the user"""
    laptop_ip = get_network_ip()
    if not laptop_ip:
        return None
    
    instructions = f"""
🎉 CROSS-DEVICE CHECK-IN SETUP COMPLETE!

📋 HOW TO USE UNIVERSAL CHECK-IN:

1. 🖥️  LAPTOP SETUP:
   - Start Flask server: python3 admin_server.py
   - Access check-in: http://localhost:5001
   - Access admin: http://localhost:5001/docs/admin_enhanced.html

2. 📱 PHONE SETUP:
   - Connect to same WiFi as laptop
   - Access check-in: http://{laptop_ip}:5001
   - Access admin: http://{laptop_ip}:5001/docs/admin_enhanced.html

3. ✅ UNIVERSAL SYNC:
   - Check-ins from laptop will appear on phone
   - Check-ins from phone will appear on laptop
   - Real-time sync every 10 seconds
   - All data stored centrally on laptop server

🔗 DEVICE URLS:
   💻 Laptop: http://localhost:5001
   📱 Phone: http://{laptop_ip}:5001

⚠️  REQUIREMENTS:
   - Both devices on same WiFi network
   - Flask server running on laptop
   - Laptop firewall allows port 5001
   """
    
    return instructions

if __name__ == "__main__":
    print('🧪 TESTING CROSS-DEVICE CHECK-IN FIX')
    success = test_cross_device_checkin()
    
    print('\n' + '=' * 50)
    if success:
        print('🎉 CROSS-DEVICE CHECK-IN FIX SUCCESSFUL!')
        instructions = create_setup_instructions()
        if instructions:
            print(instructions)
    else:
        print('❌ CROSS-DEVICE CHECK-IN FIX FAILED')
        print('   Please check network connectivity and server status')
    
    print(f'\n🏁 TEST {"PASSED" if success else "FAILED"}')