# Directory Reorganization Complete

## New Organized Structure

```
campusministrybadges/
├── 📁 web/                           # Main web files (USE THESE!)
│   ├── admin.html                    # 🎯 MAIN ADMIN PANEL (329 participants)
│   ├── checkin.html                  # 🎯 MAIN CHECK-IN SYSTEM  
│   └── assets/                       # Web assets
│       ├── mk-logo-300.png
│       └── qr-codes/
│           ├── admin_qr_code.png
│           └── checkin_qr_code.png
│
├── 📁 data/                          # All data files
│   ├── csv/
│   │   └── badge_assignments.csv    # 🎯 MAIN DATA FILE (329 participants)
│   └── excel/
│       ├── BADGE_ASSIGNMENTS_FINAL.xlsx  # 🎯 MAIN EXCEL FILE (329 participants)
│       └── backup/                   # Backup files
│
├── 📁 output/                        # Generated files
│   ├── badges/                       # All badge PDFs and PowerPoint files
│   ├── reports/                      # Analysis reports
│   └── exports/                      # Data exports
│
├── 📁 docs/                          # For GitHub Pages (auto-synced)
│   ├── admin.html                    # Same as web/admin.html
│   ├── index.html                    # Same as web/checkin.html
│   └── assets/                       # Same as web/assets/
│
├── 📁 src/                           # Source code
│   ├── badge_generation/
│   └── utilities/
│
├── 📁 templates/                     # PowerPoint templates
│   └── CAMPUSMINISTRYBADGE.pptx
│
├── admin_server.py                   # Backend API server
├── start_admin_server.sh             # Server startup script
└── requirements.txt                  # Dependencies
```

## Key Changes Made

### ✅ Files Updated with 329 Participants
- `web/admin.html` - Main admin panel with all features
- `docs/admin.html` - GitHub Pages version (auto-synced)
- All scripts now use organized file paths

### ✅ Path Updates
- `admin_server.py` - Updated to use `data/csv/` and `data/excel/`
- `src/utilities/generate_admin_panel.py` - Updated paths
- `src/utilities/generate_checkin_data.py` - Updated paths

### ✅ Clean Organization
- Web files in `/web/` directory
- Data files properly organized in `/data/`
- Output files categorized in `/output/`
- Backups safely stored in `/data/excel/backup/`

## Usage Instructions

### For Live Server
Use these files:
- **Admin Panel**: `web/admin.html`
- **Check-in System**: `web/checkin.html`
- **Assets**: `web/assets/`

### For GitHub Pages
Files are automatically synced to `/docs/` directory.

### For Local Development
```bash
# Start the enhanced admin server
./start_admin_server.sh

# Access at http://localhost:5000
# Password: campus2024
```

## What's Fixed

1. **Participant Count**: All systems now show 329 participants correctly
2. **File Organization**: Clear directory structure with proper separation
3. **Path Consistency**: All scripts use organized file paths
4. **Data Integrity**: Single source of truth for participant data
5. **Backup Safety**: All backup files preserved and organized

## File Locations Quick Reference

| What You Need | File Location |
|---------------|---------------|
| **Main Admin Panel** | `/web/admin.html` |
| **Check-in System** | `/web/checkin.html` |
| **Participant Data** | `/data/csv/badge_assignments.csv` |
| **Excel Source** | `/data/excel/BADGE_ASSIGNMENTS_FINAL.xlsx` |
| **Generated Badges** | `/output/badges/` |
| **QR Codes** | `/web/assets/qr-codes/` |

## Next Steps

1. **Upload to Live Server**: Use files from `/web/` directory
2. **Test Functionality**: Verify 329 participants appear correctly
3. **Optional**: Run `./start_admin_server.sh` for enhanced features
4. **Cleanup**: Remove old scattered files if everything works

The main admin panel (`web/admin.html`) now has all the enhanced features and shows the correct participant count of 329!