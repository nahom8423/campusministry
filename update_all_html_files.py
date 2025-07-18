#!/usr/bin/env python3
import pandas as pd
import json
import os

def update_all_html_files():
    """Update all HTML files with current participant data from CSV"""
    
    # Read the current CSV file
    csv_file = '/Users/nahomnigatu/Downloads/campusministrybadges/data/csv/badge_assignments.csv'
    df_csv = pd.read_csv(csv_file)
    
    print(f"Loading {len(df_csv)} participants from CSV")
    
    # Convert CSV data to the format expected by HTML files
    participant_data = []
    for _, row in df_csv.iterrows():
        participant = {
            "name": row['full_name'],
            "campus": row['campus'],
            "dorm": row['dorm'],
            "table": row['table_assignment'],
            "discussion": row['discussion_assignment'],
            "role": row['role']
        }
        participant_data.append(participant)
    
    print(f"Converted {len(participant_data)} participants")
    
    # List of HTML files to update
    html_files = [
        '/Users/nahomnigatu/Downloads/campusministrybadges/docs/index.html',
        '/Users/nahomnigatu/Downloads/campusministrybadges/output/checkin.html',
        '/Users/nahomnigatu/Downloads/campusministrybadges/output/checkin_final.html',
        '/Users/nahomnigatu/Downloads/campusministrybadges/web/checkin.html',
    ]
    
    # Generate the JavaScript array string
    js_data = json.dumps(participant_data, indent=2)
    
    for html_file in html_files:
        if not os.path.exists(html_file):
            print(f"⚠️  File not found: {html_file}")
            continue
            
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find and replace participant data arrays
            # Look for various patterns of participant data
            patterns = [
                ('const participants = [', ']; // End of participants'),
                ('let participants = [', ']; // End of participants'),
                ('const PARTICIPANT_DATA = [', '];'),
                ('participants = [', '];'),
            ]
            
            updated = False
            for start_pattern, end_pattern in patterns:
                start_pos = content.find(start_pattern)
                if start_pos != -1:
                    # Find the end position
                    search_start = start_pos + len(start_pattern)
                    temp_content = content[search_start:]
                    
                    # Look for the end pattern
                    end_pos = temp_content.find(end_pattern)
                    if end_pos != -1:
                        # Replace the content
                        new_content = (content[:start_pos] + 
                                     start_pattern + '\n' + js_data + '\n' + end_pattern + 
                                     content[search_start + end_pos + len(end_pattern):])
                        
                        with open(html_file, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        
                        print(f"✅ Updated {html_file}")
                        updated = True
                        break
            
            if not updated:
                print(f"⚠️  No participant data pattern found in {html_file}")
                
        except Exception as e:
            print(f"❌ Error updating {html_file}: {e}")
    
    print(f"\n✅ Update complete! All HTML files now have {len(participant_data)} participants")

if __name__ == "__main__":
    update_all_html_files()
