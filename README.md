# Campus Ministry Badge Management System

A comprehensive badge generation and check-in system for campus ministry events.

## 🚀 Quick Start

### For GitHub Pages Hosting
1. Go to your repository settings
2. Navigate to "Pages" section
3. Set source to "Deploy from a branch"
4. Select "main" branch and "/docs" folder
5. Your website will be available at: `https://yourusername.github.io/campusministrybadges`

### Website Access
- **Main Check-In**: `/` - For participants to check in
- **Admin Panel**: `/admin.html` - For administrators (password: `campus2024`)

## 📁 Project Structure

```
campusministrybadges/
├── docs/                          # GitHub Pages website files
│   ├── index.html                 # Main check-in interface
│   ├── admin.html                 # Admin panel
│   ├── assets/                    # Website assets (images, QR codes)
│   └── _config.yml               # GitHub Pages configuration
├── src/                          # Source code
│   ├── badge_generation/         # Badge generation scripts
│   │   ├── generate_badges.py    # Main badge generator
│   │   └── generate_badges2.py   # Alternative badge generator
│   ├── utilities/                # Utility scripts
│   │   ├── analyze_*.py          # Analysis tools
│   │   ├── check_*.py            # Verification tools
│   │   └── generate_*.py         # Generation utilities
│   └── config.py                 # Configuration settings
├── input_data/                   # Input Excel/CSV files
│   ├── BADGE (CLEAN FILE).xlsx   # Main participant data
│   ├── badge_assignments.csv     # Generated assignments
│   └── *.xlsx                    # Additional registration files
├── templates/                    # PowerPoint templates
│   └── CAMPUSMINISTRYBADGE_PATCHED.pptx
├── output/                       # Generated files
│   ├── filled_badges.pptx       # Generated badges
│   ├── *.pdf                     # PDF outputs
│   └── *.html                    # Generated web pages
└── archived_old_structure/       # Old files (for reference)
```

## 🔧 Usage

### Badge Generation
```bash
cd src/badge_generation
python generate_badges.py
```

### Website Deployment
1. All website files are in the `docs/` folder
2. Enable GitHub Pages pointing to `/docs` folder
3. Website will be automatically deployed

## 📊 Features

### Check-In System
- **315 total participants** registered
- Real-time participant search and check-in
- Mobile-friendly interface
- Discussion group assignments (DA/DE)
- Table assignments for Saturday and Sunday

### Admin Panel
- Password protected admin interface (default: `campus2024`)
- Real-time statistics dashboard
- Participant management and manual check-in/out
- Export functionality
- Search and filter capabilities

## 🔐 Security Notes

- Change the admin password in `docs/admin.html`
- The current password is: `campus2024`
- Consider implementing server-side authentication for production use

## 📈 Statistics

- **Total Participants**: 315
- **Discussion Groups**: DA (Amharic), DE (English)
- **Tables**: 35 tables for Saturday and Sunday sessions
- **Campuses**: Multiple campus ministries represented

## 🛠️ Development

### File Path Updates
All scripts now use relative paths based on the new structure:
- Input files: `../../input_data/`
- Templates: `../../templates/`
- Output: `../../output/`

### Running Scripts
Scripts should be run from their respective directories:
```bash
cd src/badge_generation
python generate_badges.py
```

## 🚀 Deploy with Firebase

This system now uses Firebase Realtime Database for real-time check-in sync across all devices.

### 1. Create Firebase Project
1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Create a new project or select existing one
3. Enable **Realtime Database** (not Firestore)
4. Set database rules to the provided `database.rules.json`:
   ```json
   {
     "rules": {
       "checkins": {
         ".read": true,
         ".write": true
       }
     }
   }
   ```

### 2. Get Firebase Configuration
1. Go to Project Settings > General tab
2. Scroll down to "Your apps" section
3. Click "Add app" and select Web (</>) if not already created
4. Copy the Firebase config object

### 3. Update Configuration
The Firebase configuration is already set up in `/docs/scripts/env.js`:

```javascript
export const firebaseConfig = {
  apiKey: "AIzaSyAk7BBzX1FejPjW-d6QVz1G9T2E001RWeQ",
  authDomain: "campusministry-d8400.firebaseapp.com", 
  databaseURL: "https://campusministry-d8400-default-rtdb.firebaseio.com",
  projectId: "campusministry-d8400",
  storageBucket: "campusministry-d8400.appspot.com",
  messagingSenderId: "647659158955",
  appId: "1:647659158955:web:0dad448d9ad7ad7f6926ee"
};
```

### 4. Deploy
1. Commit and push your changes to GitHub
2. GitHub Pages will automatically serve the updated files
3. Firebase handles the real-time data synchronization

### 5. Test Real-time Sync
- Open check-in page on one device
- Open admin panel on another device  
- Check in a participant - it should appear instantly on the admin panel!

## 📞 Support

For technical issues or questions about the badge system, contact the development team.
