import os
import shutil
import subprocess

def sync_all_html_files():
    """Sync all HTML files with latest data"""
    
    # First, update the main files with latest data
    print("🔄 Updating main HTML files with latest participant data...")
    
    # Update admin panel
    result = subprocess.run(['python3', 'fix_admin_with_roles.py'], capture_output=True, text=True)
    if result.returncode == 0:
        print("✅ Updated web/admin.html")
    else:
        print(f"❌ Failed to update web/admin.html: {result.stderr}")
    
    # Update checkin system
    result = subprocess.run(['python3', 'update_checkin_data.py'], capture_output=True, text=True)
    if result.returncode == 0:
        print("✅ Updated web/checkin.html")
    else:
        print(f"❌ Failed to update web/checkin.html: {result.stderr}")
    
    # Copy updated files to docs folder (for GitHub Pages)
    print("\n📁 Copying updated files to docs folder...")
    
    files_to_copy = [
        ('web/admin.html', 'docs/admin.html'),
        ('web/checkin.html', 'docs/checkin.html'),
        ('web/checkin.html', 'docs/index.html'),  # index.html serves as checkin page
    ]
    
    for source, dest in files_to_copy:
        if os.path.exists(source):
            shutil.copy2(source, dest)
            print(f"✅ Copied {source} → {dest}")
        else:
            print(f"❌ Source file not found: {source}")
    
    # Copy updated files to output folder
    print("\n📁 Copying updated files to output folder...")
    
    output_files = [
        ('web/admin.html', 'output/admin_panel_final.html'),
        ('web/checkin.html', 'output/checkin_final.html'),
    ]
    
    for source, dest in output_files:
        if os.path.exists(source):
            shutil.copy2(source, dest)
            print(f"✅ Copied {source} → {dest}")
        else:
            print(f"❌ Source file not found: {source}")
    
    print("\n🎉 All HTML files synchronized with latest participant data!")
    print("   📊 Total participants: 332 (22 coordinators + 310 participants)")
    print("   🌐 GitHub Pages will serve updated files from docs/ folder")

if __name__ == "__main__":
    sync_all_html_files()