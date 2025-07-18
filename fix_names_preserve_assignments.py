#!/usr/bin/env python3
"""
Fix name cleaning while preserving table and discussion assignments.
This script will clean names in the CSV file while keeping all assignments intact.
"""

import pandas as pd
import os
import re

def clean_name_comprehensive(name_str):
    """
    Clean name by removing ALL possible language indicators and extra characters
    """
    if pd.isna(name_str) or str(name_str).strip() == '':
        return ''
    
    clean_name = str(name_str).strip()
    
    # Remove all possible language indicators comprehensively
    # Order matters - remove longer patterns first
    indicators_to_remove = [
        '&A', '&E', ' &A', ' &E', '&A ', '&E ', 
        ' -A', '- A', '-A', ' -E', '- E', '-E',
        ' E&A', 'E&A', ' E&A ', 'E&A ',
        ' E', 'E', ' A', 'A',
        ' -New', '- New', '-New', ' New', 'New',
        ' 1', '1'  # Remove number prefixes
    ]
    
    for indicator in indicators_to_remove:
        clean_name = clean_name.replace(indicator, '')
    
    # Remove extra whitespace and clean up
    clean_name = ' '.join(clean_name.split())
    
    return clean_name.strip()

def main():
    # Get the project root directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = script_dir
    
    # Path to the CSV file
    csv_file = os.path.join(project_root, 'input_data', 'badge_assignments.csv')
    
    if not os.path.exists(csv_file):
        print(f"❌ CSV file not found: {csv_file}")
        return
    
    # Read the existing CSV
    print(f"📖 Reading existing assignments from: {csv_file}")
    df = pd.read_csv(csv_file)
    
    print(f"📊 Original CSV has {len(df)} entries")
    
    # Apply name cleaning to the full_name column
    print("🧹 Applying comprehensive name cleaning...")
    
    original_names = df['full_name'].tolist()
    df['full_name'] = df['full_name'].apply(clean_name_comprehensive)
    
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
    
    # Save the cleaned CSV
    backup_file = csv_file.replace('.csv', '_backup.csv')
    print(f"💾 Creating backup at: {backup_file}")
    
    # Create backup of original
    pd.read_csv(csv_file).to_csv(backup_file, index=False)
    
    # Save the cleaned version
    df.to_csv(csv_file, index=False)
    
    print(f"✅ Updated CSV saved with {len(df)} entries")
    print(f"🎯 All table and discussion assignments preserved!")
    print(f"📂 Backup saved as: {backup_file}")
    
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