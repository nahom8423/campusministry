import pandas as pd
import json

def update_main_admin_html():
    """Update the main admin.html file with current participant data"""
    
    # Read the CSV with correct participant data
    df = pd.read_csv('/Users/nahomnigatu/Downloads/campusministrybadges/data/csv/badge_assignments.csv')
    
    participants = []
    for _, row in df.iterrows():
        name = str(row['full_name']).strip()
        campus = str(row['campus']).strip() if pd.notna(row['campus']) else 'NEW'
        dorm = str(row['dorm']).strip() if pd.notna(row['dorm']) else 'N/A'
        table = str(row['table_assignment']).strip() if pd.notna(row['table_assignment']) else 'TBD'
        discussion = str(row['discussion_assignment']).strip() if pd.notna(row['discussion_assignment']) else 'TBD'
        
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
            'discussion': discussion
        }
        participants.append(participant)
    
    # Sort participants by name
    participants.sort(key=lambda x: x['name'])
    
    # Read the admin HTML template
    with open('/Users/nahomnigatu/Downloads/campusministrybadges/web/admin.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Convert participants to JavaScript format
    js_data = json.dumps(participants, indent=2, ensure_ascii=False)
    
    # Replace the placeholder with actual data
    html_content = html_content.replace('const PARTICIPANT_DATA = [];', f'const PARTICIPANT_DATA = {js_data};')
    
    # Write the updated HTML file
    with open('/Users/nahomnigatu/Downloads/campusministrybadges/web/admin.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ Updated /Users/nahomnigatu/Downloads/campusministrybadges/web/admin.html with {len(participants)} participants")
    print(f"📊 Sample Statistics:")
    print(f"   Total Participants: {len(participants)}")
    
    # Campus breakdown
    campus_counts = {}
    for p in participants:
        campus_counts[p['campus']] = campus_counts.get(p['campus'], 0) + 1
    
    top_campus = max(campus_counts.items(), key=lambda x: x[1])
    print(f"   Unique Campuses: {len(campus_counts)}")
    print(f"   Top Campus: {top_campus[0]} ({top_campus[1]} participants)")
    
    return len(participants)

if __name__ == "__main__":
    update_main_admin_html()