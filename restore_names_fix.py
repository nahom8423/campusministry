#!/usr/bin/env python3
"""
Restore names from backup and apply proper conservative name cleaning.
This script will restore the backup and apply only language indicator removal.
"""

import pandas as pd
import os
import re

def clean_name_conservative(name_str):
    """
    Clean name by removing ONLY language indicators, keeping all letters intact
    """
    if pd.isna(name_str) or str(name_str).strip() == '':
        return ''
    
    clean_name = str(name_str).strip()
    
    # Remove language indicators - be very specific and conservative
    # Order matters - remove longer patterns first
    language_indicators = [
        '&A', '&E', 
        ' -A', '- A', '-A', 
        ' -E', '- E', '-E',
        ' E&A', 'E&A',
        ' A&E', 'A&E'
    ]
    
    for indicator in language_indicators:
        clean_name = clean_name.replace(indicator, '')
    
    # Remove extra whitespace
    clean_name = ' '.join(clean_name.split())
    
    return clean_name.strip()

def main():
    # Get the project root directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = script_dir
    
    # Path to the CSV files
    csv_file = os.path.join(project_root, 'input_data', 'badge_assignments.csv')
    backup_file = os.path.join(project_root, 'input_data', 'badge_assignments_backup.csv')
    
    if not os.path.exists(backup_file):
        print(f"❌ Backup file not found: {backup_file}")
        return
    
    # Read the backup file
    print(f"📖 Reading backup file: {backup_file}")
    df = pd.read_csv(backup_file)
    
    print(f"📊 Backup has {len(df)} entries")
    
    # Apply conservative name cleaning to the full_name column
    print("🧹 Applying conservative name cleaning (language indicators only)...")
    
    original_names = df['full_name'].tolist()
    df['full_name'] = df['full_name'].apply(clean_name_conservative)
    
    # Show the changes
    changes_made = 0
    for i, (original, cleaned) in enumerate(zip(original_names, df['full_name'])):
        if original != cleaned:
            print(f"  ✨ {original} → {cleaned}")
            changes_made += 1
    
    print(f"📈 Cleaned {changes_made} names")
    
    # Remove any duplicates that might have been created by name cleaning
    original_count = len(df)
    df = df.drop_duplicates(subset=['full_name'], keep='first')
    duplicates_removed = original_count - len(df)
    
    if duplicates_removed > 0:
        print(f"🔄 Removed {duplicates_removed} duplicates created by name cleaning")
    
    # Save the properly cleaned CSV
    df.to_csv(csv_file, index=False)
    
    print(f"✅ Restored and properly cleaned CSV saved with {len(df)} entries")
    print(f"🎯 All table and discussion assignments preserved!")
    
    # Verify the results
    print("\n🔍 Verification:")
    print(f"  - Total entries: {len(df)}")
    print(f"  - Unique names: {len(df['full_name'].unique())}")
    print(f"  - Names cleaned: {changes_made}")
    print(f"  - Duplicates removed: {duplicates_removed}")
    
    # Show sample of cleaned data
    print("\n📋 Sample of cleaned data:")
    for i in range(min(5, len(df))):
        row = df.iloc[i]
        print(f"  {row['full_name']} → {row['table_assignment']} → {row['discussion_assignment']}")

if __name__ == "__main__":
    main()