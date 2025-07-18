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

## 📞 Support

For technical issues or questions about the badge system, contact the development team.
