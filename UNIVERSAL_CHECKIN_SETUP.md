# Universal Check-In System Setup

## How to Start the Universal Check-In System

### 1. Start the Backend Server

Open a terminal and run:

```bash
cd /Users/nahomnigatu/Downloads/campusministrybadges
python3 admin_server.py
```

You should see:
```
Starting Admin Server...
Admin panel will be available at: http://localhost:5000
API endpoints:
  GET /api/participants - Get all participants
  POST /api/participants - Add new participant
  GET /api/export/excel - Export participants to Excel
  GET /api/stats - Get participant statistics
  POST /api/checkin - Check in a participant
  GET /api/checkin?name=NAME - Get check-in status for participant
  GET /api/checkin/all - Get all checked-in participants
  GET /api/checkin/count - Get total check-in count
```

### 2. Access the Check-In System

**For Local Testing:**
- Open: http://localhost:5000/web/checkin.html
- Or use the HTML files directly

**For Public Access (GitHub Pages):**
- The system will work on GitHub Pages, but you'll need to host the backend server publicly
- For local events, run the server on the same network

### 3. How the Universal System Works

✅ **Central Storage**: All check-ins are stored on the server, not locally
✅ **Real-time Sync**: Every device syncs with the server every 10 seconds
✅ **Cross-Device**: Check-ins appear on ALL devices instantly
✅ **Offline Fallback**: If server is down, falls back to localStorage
✅ **Backup Storage**: All check-ins are saved to both server and localStorage

### 4. Features

- **Universal Check-In**: When someone checks in on ANY device, it appears on ALL devices
- **Real-time Updates**: Check-in counts update across all devices every 10 seconds
- **Offline Support**: Works even if server is temporarily unavailable
- **Persistent Storage**: Check-in data is saved to `data/checkin_data.json`
- **Admin Panel**: View all participants and check-in status
- **Export Data**: Export participant lists and check-in reports

### 5. Network Requirements

- All devices need to be on the same network as the server
- Or use a public server/cloud hosting for internet access
- Server runs on port 5000 by default

### 6. File Structure

```
campusministrybadges/
├── admin_server.py              # Backend server
├── web/checkin.html            # Updated check-in page
├── docs/checkin.html           # GitHub Pages version
├── data/checkin_data.json      # Check-in storage (auto-created)
└── data/csv/badge_assignments.csv  # Participant database
```

### 7. Troubleshooting

**If check-ins aren't syncing:**
1. Make sure the server is running on port 5000
2. Check browser console for API errors
3. Verify all devices are on the same network
4. Check firewall settings

**If server won't start:**
1. Make sure Python 3 is installed
2. Install required packages: `pip install flask flask-cors pandas`
3. Check if port 5000 is available

### 8. Admin Panel

Access the admin panel at: http://localhost:5000/web/admin.html
- View all 332 participants
- See check-in status
- Export data
- Add new participants