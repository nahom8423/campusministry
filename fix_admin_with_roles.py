import pandas as pd
import json
import re

def fix_admin_with_roles():
    """Fix the admin panel to include role information"""
    
    # Read the CSV with correct participant data
    df = pd.read_csv('/Users/nahomnigatu/Downloads/campusministrybadges/data/csv/badge_assignments.csv')
    
    participants = []
    for _, row in df.iterrows():
        name = str(row['full_name']).strip()
        campus = str(row['campus']).strip() if pd.notna(row['campus']) else 'NEW'
        dorm = str(row['dorm']).strip() if pd.notna(row['dorm']) else 'N/A'
        table = str(row['table_assignment']).strip() if pd.notna(row['table_assignment']) else 'TBD'
        discussion = str(row['discussion_assignment']).strip() if pd.notna(row['discussion_assignment']) else 'TBD'
        role = str(row['role']).strip() if pd.notna(row['role']) else 'PARTICIPANT'
        
        # Clean up campus ministry names for display
        if campus == 'NEW':
            campus = 'New Participant'
        elif len(campus) > 50:
            campus = campus[:47] + '...'
        
        participant = {
            'name': name,
            'campus': campus,
            'dorm': dorm,
            'table': table,
            'discussion': discussion,
            'role': role
        }
        participants.append(participant)
    
    # Sort participants by name
    participants.sort(key=lambda x: x['name'])
    
    # Convert to JS format
    js_data = json.dumps(participants, indent=2, ensure_ascii=False)
    
    # Read the current admin.html
    with open('/Users/nahomnigatu/Downloads/campusministrybadges/web/admin.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Find and replace the participant data using regex
    pattern = r'const PARTICIPANT_DATA = \[.*?\];'
    replacement = f'const PARTICIPANT_DATA = {js_data};'
    
    # Use DOTALL flag to match across lines
    html_content = re.sub(pattern, replacement, html_content, flags=re.DOTALL)
    
    # Write the updated HTML
    with open('/Users/nahomnigatu/Downloads/campusministrybadges/web/admin.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f'✅ Updated admin.html with {len(participants)} participants including role information')
    print(f'📊 Role breakdown:')
    print(f'   Coordinators: {len([p for p in participants if p["role"] == "COORDINATOR"])}')
    print(f'   Participants: {len([p for p in participants if p["role"] == "PARTICIPANT"])}')
    
    # Show first coordinator example
    coordinator_example = next((p for p in participants if p["role"] == "COORDINATOR"), None)
    if coordinator_example:
        print(f'\n🎯 Example coordinator: {coordinator_example["name"]}')
    
    return len(participants)

if __name__ == "__main__":
    fix_admin_with_roles()