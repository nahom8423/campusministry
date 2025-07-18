#!/usr/bin/env python3
import pandas as pd
import json
import os

def update_admin_html_with_current_data():
    """Update admin.html with current participant data from CSV"""
    
    # Read the current CSV file
    csv_file = '/Users/nahomnigatu/Downloads/campusministrybadges/data/csv/badge_assignments.csv'
    df_csv = pd.read_csv(csv_file)
    
    print(f"Loading {len(df_csv)} participants from CSV")
    
    # Convert CSV data to the format expected by admin.html
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
    
    # Read the current admin.html file
    admin_file = '/Users/nahomnigatu/Downloads/campusministrybadges/docs/admin.html'
    with open(admin_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the start and end of the PARTICIPANT_DATA array
    start_marker = "const PARTICIPANT_DATA = ["
    end_marker = "];"
    
    start_pos = content.find(start_marker)
    if start_pos == -1:
        print("ERROR: Could not find PARTICIPANT_DATA start marker")
        return
    
    # Find the end position by looking for the closing ]; after the start
    temp_content = content[start_pos:]
    lines = temp_content.split('\n')
    
    end_line_idx = -1
    for i, line in enumerate(lines):
        if line.strip().startswith('];'):
            end_line_idx = i
            break
    
    if end_line_idx == -1:
        print("ERROR: Could not find PARTICIPANT_DATA end marker")
        return
    
    # Calculate the actual end position
    end_pos = start_pos + len('\n'.join(lines[:end_line_idx + 1]))
    
    # Generate the new participant data as a JavaScript array
    js_data = "const PARTICIPANT_DATA = " + json.dumps(participant_data, indent=2) + ";"
    
    # Replace the old data with new data
    new_content = content[:start_pos] + js_data + content[end_pos + 1:]
    
    # Write the updated content back
    with open(admin_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✅ Updated admin.html with {len(participant_data)} participants")
    print(f"   - {len([p for p in participant_data if p['role'] == 'COORDINATOR'])} coordinators")
    print(f"   - {len([p for p in participant_data if p['role'] == 'PARTICIPANT'])} regular participants")

if __name__ == "__main__":
    update_admin_html_with_current_data()
