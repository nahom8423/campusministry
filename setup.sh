#!/bin/bash
# Setup script for Campus Ministry Badge System

echo "🌟 Campus Ministry Badge System Setup"
echo "======================================"

# Check if we're in the right directory
if [ ! -d "src" ] || [ ! -d "input_data" ] || [ ! -d "docs" ]; then
    echo "❌ Error: Please run this script from the campusministrybadges root directory"
    exit 1
fi

echo "✅ Directory structure looks good!"

# Check Python dependencies
echo "🔍 Checking Python dependencies..."

python3 -c "import pandas, pptx" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "✅ Python dependencies are installed"
else
    echo "⚠️  Installing required Python packages..."
    pip3 install pandas python-pptx openpyxl
fi

echo ""
echo "🚀 Setup complete! You can now:"
echo ""
echo "1. Generate badges:"
echo "   cd src/badge_generation && python3 generate_badges.py"
echo ""
echo "2. Host website on GitHub Pages:"
echo "   - Push to GitHub"
echo "   - Enable Pages in repository settings"
echo "   - Point to /docs folder"
echo ""
echo "3. Access website files:"
echo "   - Main check-in: docs/index.html"
echo "   - Admin panel: docs/admin.html (password: campus2024)"
echo ""
echo "📁 Project structure is now organized and ready to use!"
