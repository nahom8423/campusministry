import pandas as pd
import json
import re

def update_checkin_data():
    """Update checkin.html with current participant data from CSV"""
    
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
    
    # Read the current checkin.html
    with open('/Users/nahomnigatu/Downloads/campusministrybadges/web/checkin.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Find and replace the participant data using regex
    # Look for the pattern: let participants = [... ];
    pattern = r'let participants = \[.*?\];'
    replacement = f'let participants = {js_data};'
    
    # Use DOTALL flag to match across lines
    html_content = re.sub(pattern, replacement, html_content, flags=re.DOTALL)
    
    # Write the updated HTML
    with open('/Users/nahomnigatu/Downloads/campusministrybadges/web/checkin.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f'✅ Updated checkin.html with {len(participants)} participants')
    print(f'📊 Role breakdown:')
    print(f'   Coordinators: {len([p for p in participants if p["role"] == "COORDINATOR"])}')
    print(f'   Participants: {len([p for p in participants if p["role"] == "PARTICIPANT"])}')
    
    # Show first few participants
    print(f'\\n🎯 First 3 participants:')
    for i, p in enumerate(participants[:3]):
        print(f'   {i+1}. {p["name"]} ({p["role"]})')
    
    return len(participants)

if __name__ == "__main__":
    update_checkin_data()