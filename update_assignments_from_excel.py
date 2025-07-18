import pandas as pd
import re

def clean_name_for_comparison(name):
    """Clean name for comparison by removing extra spaces and normalizing"""
    if pd.isna(name):
        return ""
    
    # Convert to string and strip
    name = str(name).strip().upper()
    
    # Remove extra spaces
    name = re.sub(r'\s+', ' ', name)
    
    # Handle common variations
    name = name.replace('DN.', 'DN')
    name = name.replace('DR.', 'DR')
    
    return name

def update_assignments_from_excel():
    """Update CSV assignments with correct assignments from Excel file"""
    
    # Read the Excel file with correct assignments
    print("Reading Excel file with correct assignments...")
    excel_df = pd.read_excel('/Users/nahomnigatu/Downloads/campusministrybadges/campusministryfull.xlsx')
    
    # Create full name for Excel data
    excel_df['full_name'] = excel_df['First Name '].str.strip() + ' ' + excel_df['Last Name'].str.strip()
    excel_df['full_name_clean'] = excel_df['full_name'].apply(clean_name_for_comparison)
    
    # Read our current CSV
    print("Reading current CSV...")
    csv_df = pd.read_csv('/Users/nahomnigatu/Downloads/campusministrybadges/input_data/badge_assignments.csv')
    csv_df['full_name_clean'] = csv_df['full_name'].apply(clean_name_for_comparison)
    
    # Create backup
    backup_file = '/Users/nahomnigatu/Downloads/campusministrybadges/input_data/badge_assignments_backup_before_excel_update.csv'
    csv_df.to_csv(backup_file, index=False)
    print(f"Created backup: {backup_file}")
    
    # Update assignments for existing participants
    updated_count = 0
    
    for idx, csv_row in csv_df.iterrows():
        # Find matching row in Excel
        excel_matches = excel_df[excel_df['full_name_clean'] == csv_row['full_name_clean']]
        
        if not excel_matches.empty:
            excel_row = excel_matches.iloc[0]
            
            # Update table and discussion assignments
            old_table = csv_row['table_assignment']
            old_discussion = csv_row['discussion_assignment']
            
            new_table = str(excel_row['TABLE #']).strip()
            new_discussion = str(excel_row['DISCUSSION #']).strip()
            
            # Only update if different
            if old_table != new_table or old_discussion != new_discussion:
                csv_df.at[idx, 'table_assignment'] = new_table
                csv_df.at[idx, 'discussion_assignment'] = new_discussion
                updated_count += 1
                print(f"Updated {csv_row['full_name']}: {old_table} -> {new_table}, {old_discussion} -> {new_discussion}")
    
    # Save updated CSV
    csv_df.drop('full_name_clean', axis=1, inplace=True)
    csv_df.to_csv('/Users/nahomnigatu/Downloads/campusministrybadges/input_data/badge_assignments.csv', index=False)
    
    print(f"\n✅ Updated {updated_count} participants with correct table/discussion assignments")
    print(f"Total participants in CSV: {len(csv_df)}")
    print(f"Total participants in Excel: {len(excel_df)}")
    
    # Check for participants in CSV but not in Excel (new ones we added)
    csv_only = csv_df[~csv_df['full_name'].apply(clean_name_for_comparison).isin(excel_df['full_name_clean'])]
    if len(csv_only) > 0:
        print(f"\nNew participants added (not in Excel): {len(csv_only)}")
        for _, row in csv_only.iterrows():
            print(f"  - {row['full_name']}: {row['table_assignment']} | {row['discussion_assignment']}")
    
    return updated_count

if __name__ == "__main__":
    update_assignments_from_excel()