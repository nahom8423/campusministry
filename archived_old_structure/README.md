# Campus Ministry Badge Management System

A comprehensive system for managing campus ministry badges, check-ins, and participant data.

## Project Structure

```
campusministrybadges/
├── website/              # Website files for GitHub Pages
│   ├── index.html       # Main check-in page (checkin_final.html)
│   ├── admin.html       # Admin panel (admin_panel_final.html)
│   └── assets/          # Images, QR codes, etc.
├── scripts/             # Python scripts for badge generation
├── data/                # Excel and CSV data files
├── templates/           # PowerPoint badge templates
├── output/              # Generated PDFs and other outputs
└── README.md           # This file
```

## Live Website

The check-in system is hosted on GitHub Pages at:
`https://[your-username].github.io/[repository-name]/`

## Features

### Check-In System (`website/index.html`)
- **315 total participants** registered
- Real-time participant search and check-in
- Mobile-friendly interface
- Discussion group assignments (DA/DE)
- Table assignments for Saturday and Sunday

### Admin Panel (`website/admin.html`)
- Password protected admin interface (default: `campus2024`)
- Real-time statistics dashboard
- Participant management and manual check-in/out
- Export functionality
- Search and filter capabilities

## Usage

### For Participants
1. Open the check-in website
2. Type your name to search
3. Confirm your details
4. Complete check-in

### For Administrators
1. Navigate to `/admin.html`
2. Enter password: `campus2024`
3. Monitor check-ins and manage participants

## Setup for Development

1. Clone this repository
2. Data files are in the `data/` folder
3. Scripts for badge generation are in `scripts/`
4. PowerPoint templates are in `templates/`

## Badge Generation Scripts

Located in `scripts/` folder:
- `generate_badges.py` - Main badge generation script
- `generate_badges2.py` - Alternative badge generator
- `analyze_*.py` - Analysis and verification scripts
- `check_*.py` - Data validation scripts

## Data Files

Located in `data/` folder:
- `BADGE (CLEAN FILE).xlsx` - Main participant data
- `BADGE_ASSIGNMENTS_FINAL.xlsx` - Final assignments
- `badge_assignments.csv` - Processed CSV data
- Various dorm assignment files

## Deployment

### GitHub Pages Setup
1. Push this repository to GitHub
2. Go to Settings > Pages
3. Select "Deploy from a branch"
4. Choose "main" branch and "/ (root)" folder
5. Your site will be available at `https://[username].github.io/[repo-name]/`

### Custom Domain (Optional)
1. Add a `CNAME` file to the website folder with your domain
2. Configure DNS settings with your domain provider

## Security Notes

- Change the admin password in `website/admin.html`
- The current password is: `campus2024`
- Consider implementing server-side authentication for production use

## Statistics

- **Total Participants**: 315
- **Discussion Groups**: DA (Amharic), DE (English)
- **Tables**: 35 tables for Saturday and Sunday sessions
- **Campuses**: Multiple campus ministries represented

## Support

For technical issues or questions about the badge system, contact the development team.
