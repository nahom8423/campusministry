# 🚀 GitHub Pages Hosting Instructions

## Quick Setup for GitHub Pages

### Step 1: Push to GitHub
```bash
git add .
git commit -m "Organize project structure and setup GitHub Pages"
git push origin main
```

### Step 2: Enable GitHub Pages
1. Go to your repository on GitHub
2. Click on **Settings** tab
3. Scroll down to **Pages** section
4. Under **Source**, select **Deploy from a branch**
5. Choose **main** branch and **/docs** folder
6. Click **Save**

### Step 3: Access Your Website
Your website will be available at:
`https://[your-username].github.io/[repository-name]/`

- **Main Check-In**: `https://[your-username].github.io/[repository-name]/`
- **Admin Panel**: `https://[your-username].github.io/[repository-name]/admin.html`

## What's Fixed

✅ **Count Discrepancy**: Confirmed 315 participants (CSV has 316 lines including header)
✅ **Directory Organization**: Clean, logical folder structure
✅ **File Path Updates**: All scripts updated for new structure
✅ **GitHub Pages Ready**: Website files in `/docs` folder
✅ **GitHub Actions**: Automatic deployment workflow
✅ **Documentation**: Comprehensive README and setup guide

## Project Structure (New)

```
📁 campusministrybadges/
├── 🌐 docs/                     # GitHub Pages website
│   ├── index.html               # Main check-in page
│   ├── admin.html               # Admin panel
│   └── assets/                  # Images, QR codes
├── 🧪 src/                      # Source code
│   ├── badge_generation/        # Badge generators
│   └── utilities/               # Helper scripts
├── 📊 input_data/               # Excel/CSV files
├── 📄 templates/                # PowerPoint templates
├── 📦 output/                   # Generated files
└── 📚 archived_old_structure/   # Old files (backup)
```

## Admin Panel Password
Default password: `campus2024`

## Next Steps
1. Test the website locally by opening `docs/index.html`
2. Push to GitHub and enable Pages
3. Share the GitHub Pages URL with participants
4. Use admin panel for monitoring check-ins

The count shows exactly 315 participants as expected!
