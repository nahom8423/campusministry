
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
🔗 http://10.1.10.150:5001

**For Staff (Admin Panel):**
🔗 http://10.1.10.150:5001/docs/admin_enhanced.html

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
3. Share URL manually: http://10.1.10.150:5001

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

*Ready for 332 participants! 🎉*
