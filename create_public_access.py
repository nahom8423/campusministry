#!/usr/bin/env python3
"""Create public access solution for all event attendees"""

import socket
import qrcode
import os

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

def create_public_qr_codes():
    """Create QR codes for public access"""
    
    laptop_ip = get_network_ip()
    if not laptop_ip:
        print('❌ Could not determine network IP')
        return False
    
    # URLs for public access
    checkin_url = f'http://{laptop_ip}:5001'
    admin_url = f'http://{laptop_ip}:5001/docs/admin_enhanced.html'
    
    print(f'🌐 CREATING PUBLIC ACCESS QR CODES')
    print(f'📱 Check-in URL: {checkin_url}')
    print(f'👥 Admin URL: {admin_url}')
    
    # Create QR codes
    qr_checkin = qrcode.QRCode(version=1, box_size=10, border=5)
    qr_checkin.add_data(checkin_url)
    qr_checkin.make(fit=True)
    
    qr_admin = qrcode.QRCode(version=1, box_size=10, border=5)
    qr_admin.add_data(admin_url)
    qr_admin.make(fit=True)
    
    # Save QR code images
    checkin_img = qr_checkin.make_image(fill_color="black", back_color="white")
    admin_img = qr_admin.make_image(fill_color="black", back_color="white")
    
    # Create output directory
    os.makedirs('public_access', exist_ok=True)
    
    checkin_img.save('public_access/checkin_qr_public.png')
    admin_img.save('public_access/admin_qr_public.png')
    
    print(f'✅ QR codes saved:')
    print(f'   📱 Check-in: public_access/checkin_qr_public.png')
    print(f'   👥 Admin: public_access/admin_qr_public.png')
    
    return laptop_ip

def create_event_instructions():
    """Create instructions for event setup"""
    
    laptop_ip = get_network_ip()
    if not laptop_ip:
        return None
    
    instructions = f"""
# 📱 CAMPUS MINISTRY CHECK-IN - PUBLIC ACCESS SETUP

## 🎯 FOR EVENT ORGANIZERS

### BEFORE THE EVENT:

1. **Setup Laptop Server:**
   ```bash
   python3 admin_server.py
   ```
   Keep this running throughout the event!

2. **Share WiFi Network:**
   - Make sure everyone connects to the same WiFi: [YOUR_WIFI_NAME]
   - Or set up laptop as hotspot (see instructions below)

3. **Print QR Codes:**
   - Print the QR codes from `public_access/` folder
   - Post them at entrance/registration tables

### DURING THE EVENT:

**For Attendees:**
- Scan QR code with phone camera
- Opens check-in page automatically
- Search their name and check in
- Works on ANY phone/device!

**For Staff/Volunteers:**
- Use admin QR code for managing check-ins
- View real-time attendance count
- Export data as needed

---

## 📱 ACCESS URLS:

**For Attendees (Check-in):**
🔗 http://{laptop_ip}:5001

**For Staff (Admin Panel):**
🔗 http://{laptop_ip}:5001/docs/admin_enhanced.html

---

## 🔧 SETUP OPTIONS:

### OPTION 1: Use Existing WiFi Network
- Connect laptop to venue WiFi
- All attendees connect to same WiFi
- Share QR codes for easy access

### OPTION 2: Laptop Hotspot (if no WiFi available)
1. **Windows:**
   - Settings → Network & Internet → Mobile hotspot
   - Turn on "Share my Internet connection"
   
2. **Mac:**
   - System Preferences → Sharing
   - Check "Internet Sharing"
   
3. **Share hotspot name/password with attendees**

### OPTION 3: Use Phone Hotspot
- Use your phone as hotspot
- Connect laptop to phone's hotspot
- All attendees connect to same hotspot

---

## ✅ BENEFITS:

✅ **Universal Access:** Any phone can check in
✅ **No App Required:** Works in any web browser
✅ **Real-time Sync:** All devices see updates instantly
✅ **Offline Backup:** Falls back to local storage if needed
✅ **Easy Setup:** Just scan QR code and go!

---

## 🆘 TROUBLESHOOTING:

**If attendees can't access:**
1. Check they're on same WiFi network
2. Try restarting the server
3. Share URL manually: http://{laptop_ip}:5001

**If sync not working:**
1. Check server is running
2. Verify network connectivity
3. Check browser console for errors

---

## 📊 EVENT DAY CHECKLIST:

□ Laptop server running (`python3 admin_server.py`)
□ QR codes printed and posted
□ WiFi network shared with attendees
□ Staff knows admin URL for monitoring
□ Backup plan ready (phone hotspot)

---

*Ready for {332} participants! 🎉*
"""
    
    return instructions

def create_html_landing_page():
    """Create a simple landing page for the event"""
    
    laptop_ip = get_network_ip()
    if not laptop_ip:
        return None
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Campus Ministry Check-In</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            text-align: center;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            min-height: 100vh;
            margin: 0;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }}
        .container {{
            max-width: 400px;
            margin: 0 auto;
            background: white;
            color: #333;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }}
        .logo {{
            font-size: 2.5em;
            margin-bottom: 10px;
            color: #667eea;
        }}
        h1 {{
            margin: 0 0 10px 0;
            color: #333;
        }}
        .subtitle {{
            color: #666;
            margin-bottom: 30px;
            font-size: 1.1em;
        }}
        .button {{
            display: inline-block;
            background: #667eea;
            color: white;
            text-decoration: none;
            padding: 15px 30px;
            border-radius: 25px;
            font-size: 1.2em;
            font-weight: bold;
            margin: 10px;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        }}
        .button:hover {{
            background: #5a67d8;
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
        }}
        .admin-button {{
            background: #48bb78;
            box-shadow: 0 4px 15px rgba(72, 187, 120, 0.4);
        }}
        .admin-button:hover {{
            background: #38a169;
            box-shadow: 0 6px 20px rgba(72, 187, 120, 0.6);
        }}
        .info {{
            background: #f7fafc;
            padding: 15px;
            border-radius: 10px;
            margin: 20px 0;
            border-left: 4px solid #667eea;
        }}
        .stats {{
            display: flex;
            justify-content: space-around;
            margin: 20px 0;
        }}
        .stat {{
            text-align: center;
        }}
        .stat-number {{
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
        }}
        .stat-label {{
            font-size: 0.9em;
            color: #666;
        }}
        @media (max-width: 480px) {{
            .container {{
                margin: 10px;
                padding: 20px;
            }}
            .button {{
                display: block;
                margin: 10px 0;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">📱</div>
        <h1>Campus Ministry</h1>
        <p class="subtitle">Welcome! Please check in below</p>
        
        <div class="stats">
            <div class="stat">
                <div class="stat-number" id="totalCount">332</div>
                <div class="stat-label">Total Registered</div>
            </div>
            <div class="stat">
                <div class="stat-number" id="checkedInCount">-</div>
                <div class="stat-label">Checked In</div>
            </div>
        </div>
        
        <a href="/" class="button">
            📝 Check In Here
        </a>
        
        <a href="/docs/admin_enhanced.html" class="button admin-button">
            👥 Staff/Admin Panel
        </a>
        
        <div class="info">
            <strong>Instructions:</strong><br>
            1. Click "Check In Here"<br>
            2. Search for your name<br>
            3. Tap your name to check in<br>
            4. You're done! ✅
        </div>
        
        <div class="info">
            <strong>Need Help?</strong><br>
            Ask any staff member or volunteer
        </div>
    </div>

    <script>
        // Load checked-in count
        async function loadStats() {{
            try {{
                const response = await fetch('/api/checkin/count');
                if (response.ok) {{
                    const data = await response.json();
                    document.getElementById('checkedInCount').textContent = data.count || 0;
                }}
            }} catch (e) {{
                document.getElementById('checkedInCount').textContent = '0';
            }}
        }}
        
        // Update stats every 10 seconds
        loadStats();
        setInterval(loadStats, 10000);
    </script>
</body>
</html>"""
    
    return html_content

if __name__ == "__main__":
    print('🎯 CREATING PUBLIC ACCESS SOLUTION')
    print('=' * 50)
    
    # Create QR codes
    laptop_ip = create_public_qr_codes()
    
    if laptop_ip:
        # Create instructions
        instructions = create_event_instructions()
        if instructions:
            with open('public_access/EVENT_SETUP_INSTRUCTIONS.md', 'w') as f:
                f.write(instructions)
            print(f'✅ Instructions saved: public_access/EVENT_SETUP_INSTRUCTIONS.md')
        
        # Create landing page
        landing_page = create_html_landing_page()
        if landing_page:
            with open('public_access/landing_page.html', 'w') as f:
                f.write(landing_page)
            print(f'✅ Landing page saved: public_access/landing_page.html')
        
        print(f'\n🎉 PUBLIC ACCESS READY!')
        print(f'📱 Anyone can scan QR codes to access check-in')
        print(f'🌐 Network IP: {laptop_ip}:5001')
        print(f'📋 Print QR codes from public_access/ folder')
        print(f'👥 Share with all {332} event attendees!')
        
    else:
        print('❌ Failed to create public access solution')
        print('   Check network connectivity')