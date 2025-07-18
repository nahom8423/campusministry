import pandas as pd
import json
import html

def generate_checkin_data():
    """Generate participant data for the check-in system from the CSV file"""
    
    # Read the badge assignments CSV
    df = pd.read_csv('../../input_data/badge_assignments.csv')
    
    participants = []
    
    for _, row in df.iterrows():
        # Clean and format the data
        name = str(row['full_name']).strip()
        campus = str(row['campus']).strip() if pd.notna(row['campus']) else 'NEW'
        dorm = str(row['dorm']).strip() if pd.notna(row['dorm']) else 'N/A'
        table = str(row['table_assignment']).strip() if pd.notna(row['table_assignment']) else 'TBD'
        discussion = str(row['discussion_assignment']).strip() if pd.notna(row['discussion_assignment']) else 'TBD'
        
        # Clean up campus ministry names for display
        if campus == 'NEW':
            campus = 'New Participant'
        elif len(campus) > 50:
            # Truncate very long campus names
            campus = campus[:47] + '...'
        
        participant = {
            'name': name,
            'campus': campus,
            'dorm': dorm,
            'table': table,
            'discussion': discussion
        }
        
        participants.append(participant)
    
    # Sort participants by name for easier searching
    participants.sort(key=lambda x: x['name'])
    
    print(f"Generated data for {len(participants)} participants")
    
    return participants

def create_checkin_page_with_data():
    """Create the final check-in HTML page with embedded participant data"""
    
    # Generate participant data
    participants = generate_checkin_data()
    
    # Read the HTML template
    with open('../../docs/index.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Convert participants to JavaScript format
    js_data = json.dumps(participants, indent=2, ensure_ascii=False)
    
    # Replace the placeholder with actual data
    html_content = html_content.replace('PARTICIPANT_DATA; // Will be injected', js_data + ';')
    
    # Write the final HTML file
    with open('../../output/checkin_final.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"Created ../../output/checkin_final.html with {len(participants)} participants")
    print("\nFirst 5 participants:")
    for i, p in enumerate(participants[:5]):
        print(f"{i+1}. {p['name']} - {p['campus']} - {p['table']}")
    
    return len(participants)

if __name__ == "__main__":
    create_checkin_page_with_data()