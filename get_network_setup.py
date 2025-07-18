#!/usr/bin/env python3
"""Get network setup for universal check-in"""

import socket
import requests
import subprocess
import time

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

def test_cross_device_setup():
    """Test and set up cross-device check-in system"""
    
    print('🌐 UNIVERSAL CHECK-IN SETUP')
    print('=' * 50)
    
    # Get network IP
    laptop_ip = get_network_ip()
    if not laptop_ip:
        print('❌ Could not determine network IP')
        return False
    
    print(f'✅ Laptop Network IP: {laptop_ip}')
    print(f'📱 Phone should connect to: http://{laptop_ip}:5001')
    
    # Start Flask server in background
    print('\n🔄 Starting Flask server...')
    try:
        server_process = subprocess.Popen(['python3', 'admin_server.py'], 
                                        stdout=subprocess.PIPE, 
                                        stderr=subprocess.PIPE)
        time.sleep(3)  # Wait for server to start
        
        # Test localhost connection (laptop)
        print('\n💻 Testing laptop connection (localhost)...')
        try:
            response = requests.get('http://localhost:5001/api/participants', timeout=5)
            if response.status_code == 200:
                participants = response.json()
                print(f'   ✅ Laptop connection: {len(participants)} participants loaded')
            else:
                print(f'   ❌ Laptop connection failed: {response.status_code}')
        except Exception as e:
            print(f'   ❌ Laptop connection error: {e}')
        
        # Test network IP connection (phone simulation)
        print(f'\n📱 Testing phone connection (network IP)...')
        try:
            response = requests.get(f'http://{laptop_ip}:5001/api/participants', timeout=5)
            if response.status_code == 200:
                participants = response.json()
                print(f'   ✅ Phone connection: {len(participants)} participants loaded')
                print(f'   ✅ Cross-device communication WORKING!')
            else:
                print(f'   ❌ Phone connection failed: {response.status_code}')
        except Exception as e:
            print(f'   ❌ Phone connection error: {e}')
            print(f'   💡 Phone may not be able to reach laptop')
        
        # Test check-in sync
        print(f'\n🔄 Testing check-in synchronization...')
        test_participant = 'BETHLEHEM ADUGNA'
        
        # Simulate laptop check-in
        try:
            checkin_data = {'name': test_participant}
            response = requests.post('http://localhost:5001/api/checkin', json=checkin_data, timeout=5)
            if response.status_code == 200:
                print(f'   ✅ Laptop check-in: {test_participant}')
                
                # Check if phone can see the check-in
                response = requests.get(f'http://{laptop_ip}:5001/api/checkin/all', timeout=5)
                if response.status_code == 200:
                    checkins = response.json()
                    if any(p['name'] == test_participant for p in checkins['checked_in_participants']):
                        print(f'   ✅ Phone can see laptop check-in: SYNC WORKING!')
                        return True
                    else:
                        print(f'   ❌ Phone cannot see laptop check-in')
                else:
                    print(f'   ❌ Phone cannot get check-in list')
            else:
                print(f'   ❌ Laptop check-in failed')
        except Exception as e:
            print(f'   ❌ Check-in test error: {e}')
        
    finally:
        # Clean up
        print('\n🧹 Cleaning up...')
        try:
            server_process.terminate()
            server_process.wait()
        except:
            pass
    
    return False

def create_network_config():
    """Create configuration for network setup"""
    laptop_ip = get_network_ip()
    if not laptop_ip:
        return None
    
    config = {
        'laptop_ip': laptop_ip,
        'laptop_url': 'http://localhost:5001/api',
        'phone_url': f'http://{laptop_ip}:5001/api',
        'instructions': [
            '1. Start Flask server on laptop: python3 admin_server.py',
            f'2. Laptop accesses: http://localhost:5001/web/checkin.html',
            f'3. Phone accesses: http://{laptop_ip}:5001/web/checkin.html',
            '4. Both devices will sync check-ins through the server',
            '5. Make sure both devices are on the same WiFi network'
        ]
    }
    
    return config

if __name__ == "__main__":
    print('🧪 TESTING CROSS-DEVICE CHECK-IN SYSTEM')
    success = test_cross_device_setup()
    
    print('\n' + '=' * 50)
    if success:
        print('🎉 CROSS-DEVICE CHECK-IN WORKING!')
    else:
        print('❌ CROSS-DEVICE CHECK-IN NEEDS SETUP')
    
    config = create_network_config()
    if config:
        print('\n📋 SETUP INSTRUCTIONS:')
        for instruction in config['instructions']:
            print(f'   {instruction}')
        
        print(f'\n🔗 DEVICE URLS:')
        print(f'   💻 Laptop: {config["laptop_url"]}')
        print(f'   📱 Phone: {config["phone_url"]}')