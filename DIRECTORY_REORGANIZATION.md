# Directory Reorganization Plan

## Current Issues:
- HTML files scattered in `/docs/`, `/output/`, and `/archived_old_structure/website/`
- Duplicate files with different versions
- Inconsistent file locations
- Scripts generating files in multiple locations

## New Organized Structure:

```
campusministrybadges/
├── README.md                           # Main project documentation
├── requirements.txt                    # Python dependencies
├── start_admin_server.sh              # Server startup script
├── admin_server.py                    # Backend API server
│
├── data/                              # All data files
│   ├── excel/
│   │   ├── BADGE_ASSIGNMENTS_FINAL.xlsx    # Main Excel file
│   │   └── backup/                         # Excel backups
│   └── csv/
│       └── badge_assignments.csv          # Main CSV file
│
├── templates/                         # PowerPoint templates
│   └── CAMPUSMINISTRYBADGE.pptx      # Main template
│
├── web/                              # All web files
│   ├── admin.html                    # Main admin panel
│   ├── checkin.html                  # Main check-in system
│   └── assets/                       # Images, CSS, JS
│       ├── mk-logo-300.png
│       └── qr-codes/
│           ├── admin_qr_code.png
│           └── checkin_qr_code.png
│
├── output/                           # Generated files
│   ├── badges/                       # Generated badges
│   ├── reports/                      # Analysis reports
│   └── exports/                      # Data exports
│
├── src/                              # Source code
│   ├── badge_generation/
│   └── utilities/
│
└── docs/                             # Documentation only
    ├── README_ADMIN_FEATURES.md
    └── setup/
```

## Files to Move:
- Move `/docs/admin.html` → `/web/admin.html`
- Move `/docs/index.html` → `/web/checkin.html`
- Move `/docs/assets/` → `/web/assets/`
- Move `/input_data/` → `/data/`
- Clean up `/output/` duplicates
- Archive old files properly