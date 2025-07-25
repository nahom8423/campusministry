from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
import pandas as pd
import os
import json
from datetime import datetime
import re

app = Flask(__name__)
CORS(app)

# File paths
BADGE_ASSIGNMENTS_CSV = '/Users/nahomnigatu/Downloads/campusministrybadges/data/csv/badge_assignments.csv'
BADGE_ASSIGNMENTS_XLSX = '/Users/nahomnigatu/Downloads/campusministrybadges/data/excel/BADGE_ASSIGNMENTS_FINAL.xlsx'
CHECKIN_DATA_JSON = '/Users/nahomnigatu/Downloads/campusministrybadges/data/checkin_data.json'

def load_checkin_data():
    """Load check-in data from JSON file"""
    try:
        if os.path.exists(CHECKIN_DATA_JSON):
            with open(CHECKIN_DATA_JSON, 'r') as f:
                return json.load(f)
        return {}
    except Exception as e:
        print(f"Error loading check-in data: {e}")
        return {}

def save_checkin_data(data):
    """Save check-in data to JSON file"""
    try:
        # Ensure directory exists
        os.makedirs(os.path.dirname(CHECKIN_DATA_JSON), exist_ok=True)
        
        with open(CHECKIN_DATA_JSON, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving check-in data: {e}")
        return False

def get_next_table_assignment():
    """Get the next available table assignment"""
    try:
        df = pd.read_csv(BADGE_ASSIGNMENTS_CSV)
        
        # Extract table numbers from existing assignments
        table_counts = {}
        for _, row in df.iterrows():
            table_assignment = str(row['table_assignment'])
            if pd.notna(table_assignment) and 'SAT T' in table_assignment:
                # Extract Saturday table number
                sat_match = re.search(r'SAT T(\d+)', table_assignment)
                if sat_match:
                    table_num = int(sat_match.group(1))
                    table_counts[table_num] = table_counts.get(table_num, 0) + 1
        
        # Find the table with the least assignments (up to table 35)
        min_count = float('inf')
        best_table = 1
        
        for table_num in range(1, 36):  # Tables 1-35
            count = table_counts.get(table_num, 0)
            if count < min_count:
                min_count = count
                best_table = table_num
        
        # Generate assignment in the same format
        return f"SAT T{best_table} | SUN T{best_table}"
    
    except Exception as e:
        print(f"Error getting table assignment: {e}")
        return "SAT T1 | SUN T1"

def get_next_discussion_assignment():
    """Get the next available discussion assignment"""
    try:
        df = pd.read_csv(BADGE_ASSIGNMENTS_CSV)
        
        # Extract discussion numbers from existing assignments
        discussion_counts = {}
        for _, row in df.iterrows():
            discussion_assignment = str(row['discussion_assignment'])
            if pd.notna(discussion_assignment):
                # Extract discussion number
                if 'DE' in discussion_assignment:
                    de_match = re.search(r'DE (\d+)', discussion_assignment)
                    if de_match:
                        disc_num = int(de_match.group(1))
                        discussion_counts[f'DE {disc_num}'] = discussion_counts.get(f'DE {disc_num}', 0) + 1
                elif 'DA' in discussion_assignment:
                    da_match = re.search(r'DA (\d+)', discussion_assignment)
                    if da_match:
                        disc_num = int(da_match.group(1))
                        discussion_counts[f'DA {disc_num}'] = discussion_counts.get(f'DA {disc_num}', 0) + 1
        
        # Find the discussion with the least assignments
        min_count = float('inf')
        best_discussion = 'DE 1'
        
        # Check DE discussions (1-35)
        for disc_num in range(1, 36):
            de_key = f'DE {disc_num}'
            count = discussion_counts.get(de_key, 0)
            if count < min_count:
                min_count = count
                best_discussion = de_key
        
        # Check DA discussions (1-9)
        for disc_num in range(1, 10):
            da_key = f'DA {disc_num}'
            count = discussion_counts.get(da_key, 0)
            if count < min_count:
                min_count = count
                best_discussion = da_key
        
        return best_discussion
    
    except Exception as e:
        print(f"Error getting discussion assignment: {e}")
        return "DE 1"

def get_next_slide_and_slot():
    """Get the next available slide and slot"""
    try:
        df = pd.read_csv(BADGE_ASSIGNMENTS_CSV)
        
        # Find the maximum slide number
        max_slide = df['slide'].max() if not df.empty else 0
        
        # Check if current slide has room (max 4 slots per slide)
        current_slide_count = len(df[df['slide'] == max_slide])
        
        if current_slide_count < 4:
            return max_slide, current_slide_count
        else:
            return max_slide + 1, 0
    
    except Exception as e:
        print(f"Error getting slide/slot: {e}")
        return 1, 0

@app.route('/api/participants', methods=['GET'])
def get_participants():
    """Get all participants"""
    try:
        df = pd.read_csv(BADGE_ASSIGNMENTS_CSV)
        participants = []
        
        for _, row in df.iterrows():
            participant = {
                'name': str(row['full_name']),
                'campus': str(row['campus']) if pd.notna(row['campus']) else 'NEW',
                'dorm': str(row['dorm']) if pd.notna(row['dorm']) else 'N/A',
                'table': str(row['table_assignment']) if pd.notna(row['table_assignment']) else 'TBD',
                'discussion': str(row['discussion_assignment']) if pd.notna(row['discussion_assignment']) else 'TBD',
                'role': str(row['role']) if pd.notna(row['role']) else 'PARTICIPANT'
            }
            participants.append(participant)
        
        return jsonify(participants)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/participants', methods=['POST'])
def add_participant():
    """Add a new participant"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['full_name', 'campus', 'dorm', 'role']
        for field in required_fields:
            if field not in data or not data[field].strip():
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Read current CSV
        df = pd.read_csv(BADGE_ASSIGNMENTS_CSV)
        
        # Check if participant already exists
        if data['full_name'].strip().upper() in df['full_name'].str.upper().values:
            return jsonify({'error': 'Participant already exists'}), 400
        
        # Get next assignments
        slide, slot = get_next_slide_and_slot()
        table_assignment = get_next_table_assignment()
        discussion_assignment = get_next_discussion_assignment()
        
        # Create new participant data
        new_participant = {
            'slide': slide,
            'slot': slot,
            'full_name': data['full_name'].strip(),
            'role': data['role'].strip(),
            'campus': data['campus'].strip(),
            'dorm': data['dorm'].strip(),
            'table_assignment': table_assignment,
            'discussion_assignment': discussion_assignment
        }
        
        # Add to dataframe
        new_df = pd.concat([df, pd.DataFrame([new_participant])], ignore_index=True)
        
        # Save to CSV
        new_df.to_csv(BADGE_ASSIGNMENTS_CSV, index=False)
        
        # Also update the Excel file
        try:
            # Read existing Excel file
            xlsx_df = pd.read_excel(BADGE_ASSIGNMENTS_XLSX)
            
            # Add new participant to Excel (using correct column names for BADGE_ASSIGNMENTS_FINAL.xlsx)
            excel_new_participant = {
                'First Name ': data['full_name'].split()[0] if data['full_name'].split() else data['full_name'],
                'Last Name': ' '.join(data['full_name'].split()[1:]) if len(data['full_name'].split()) > 1 else '',
                'DORM NUMBER': data['dorm'].strip(),
                'TABLE #': table_assignment,
                'DISCUSSION #': discussion_assignment,
                'What is your preferred language for sermons and/or engaging in group discussions?': 'English',
                'Which campus ministry are you a part of? In case, you are not part of the listed campus ministries, it\'s open to you as well, and please come and join us! ': data['campus'].strip(),
                'State you residence in': 'United States',
                'If your are a College Student, which year are you?': 'N/A',
                'Gender': 'N/A'
            }
            
            xlsx_new_df = pd.concat([xlsx_df, pd.DataFrame([excel_new_participant])], ignore_index=True)
            xlsx_new_df.to_excel(BADGE_ASSIGNMENTS_XLSX, index=False)
            
        except Exception as excel_error:
            print(f"Warning: Could not update Excel file: {excel_error}")
        
        return jsonify({
            'success': True,
            'participant': {
                'name': new_participant['full_name'],
                'campus': new_participant['campus'],
                'dorm': new_participant['dorm'],
                'table': new_participant['table_assignment'],
                'discussion': new_participant['discussion_assignment'],
                'role': new_participant['role']
            }
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/export/excel', methods=['GET'])
def export_excel():
    """Export current participants to Excel"""
    try:
        # Create a timestamped filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'participants_export_{timestamp}.xlsx'
        export_path = f'/Users/nahomnigatu/Downloads/campusministrybadges/output/{filename}'
        
        # Read current CSV data
        df = pd.read_csv(BADGE_ASSIGNMENTS_CSV)
        
        # Create Excel-formatted data
        excel_data = []
        for _, row in df.iterrows():
            full_name = str(row['full_name'])
            name_parts = full_name.split()
            first_name = name_parts[0] if name_parts else full_name
            last_name = ' '.join(name_parts[1:]) if len(name_parts) > 1 else ''
            
            excel_row = {
                'First Name ': first_name,
                'Last Name': last_name,
                'DORM NUMBER': str(row['dorm']) if pd.notna(row['dorm']) else 'N/A',
                'TABLE #': str(row['table_assignment']) if pd.notna(row['table_assignment']) else 'TBD',
                'DISCUSSION #': str(row['discussion_assignment']) if pd.notna(row['discussion_assignment']) else 'TBD',
                'What is your preferred language for sermons and/or engaging in group discussions?': 'English',
                'Which campus ministry are you a part of? In case, you are not part of the listed campus ministries, it\'s open to you as well, and please come and join us! ': str(row['campus']) if pd.notna(row['campus']) else 'NEW',
                'State you residence in': 'United States',
                'If your are a College Student, which year are you?': 'N/A',
                'Gender': 'N/A'
            }
            excel_data.append(excel_row)
        
        # Create Excel file
        excel_df = pd.DataFrame(excel_data)
        excel_df.to_excel(export_path, index=False)
        
        return send_file(export_path, as_attachment=True, download_name=filename)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get participant statistics"""
    try:
        df = pd.read_csv(BADGE_ASSIGNMENTS_CSV)
        
        stats = {
            'total_participants': len(df),
            'campus_breakdown': df['campus'].value_counts().to_dict(),
            'table_usage': {},
            'discussion_usage': {}
        }
        
        # Table usage stats
        for _, row in df.iterrows():
            table_assignment = str(row['table_assignment'])
            if pd.notna(table_assignment) and 'SAT T' in table_assignment:
                sat_match = re.search(r'SAT T(\d+)', table_assignment)
                if sat_match:
                    table_num = f"Table {sat_match.group(1)}"
                    stats['table_usage'][table_num] = stats['table_usage'].get(table_num, 0) + 1
        
        # Discussion usage stats
        for _, row in df.iterrows():
            discussion_assignment = str(row['discussion_assignment'])
            if pd.notna(discussion_assignment):
                stats['discussion_usage'][discussion_assignment] = stats['discussion_usage'].get(discussion_assignment, 0) + 1
        
        return jsonify(stats)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Check-in API endpoints
@app.route('/api/checkin', methods=['POST'])
def checkin_participant():
    """Check in a participant"""
    try:
        data = request.get_json()
        
        if 'name' not in data:
            return jsonify({'error': 'Name is required'}), 400
        
        participant_name = data['name'].strip()
        
        # Load current check-in data
        checkin_data = load_checkin_data()
        
        # Add timestamp for this check-in
        checkin_data[participant_name] = {
            'timestamp': datetime.now().isoformat(),
            'ip_address': request.remote_addr
        }
        
        # Save updated data
        if save_checkin_data(checkin_data):
            return jsonify({
                'success': True,
                'message': f'{participant_name} checked in successfully',
                'timestamp': checkin_data[participant_name]['timestamp']
            })
        else:
            return jsonify({'error': 'Failed to save check-in data'}), 500
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/checkin', methods=['GET'])
def get_checkin_status():
    """Get check-in status for a specific participant"""
    try:
        participant_name = request.args.get('name')
        
        if not participant_name:
            return jsonify({'error': 'Name parameter is required'}), 400
        
        checkin_data = load_checkin_data()
        
        if participant_name in checkin_data:
            return jsonify({
                'checked_in': True,
                'timestamp': checkin_data[participant_name]['timestamp']
            })
        else:
            return jsonify({'checked_in': False})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/checkin/all', methods=['GET'])
def get_all_checkins():
    """Get all checked-in participants"""
    try:
        checkin_data = load_checkin_data()
        
        # Convert to list format for frontend
        checked_in_list = []
        for name, info in checkin_data.items():
            checked_in_list.append({
                'name': name,
                'timestamp': info['timestamp'],
                'ip_address': info.get('ip_address', 'unknown')
            })
        
        # Sort by timestamp (most recent first)
        checked_in_list.sort(key=lambda x: x['timestamp'], reverse=True)
        
        return jsonify({
            'checked_in_participants': checked_in_list,
            'total_checked_in': len(checked_in_list)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/checkin/count', methods=['GET'])
def get_checkin_count():
    """Get total check-in count"""
    try:
        checkin_data = load_checkin_data()
        return jsonify({
            'total_checked_in': len(checkin_data)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Serve the landing page
@app.route('/')
def landing_page():
    """Serve the landing page for easy access"""
    try:
        with open('/Users/nahomnigatu/Downloads/campusministrybadges/public_access/landing_page.html', 'r') as f:
            return f.read()
    except:
        # Fallback to main check-in page
        return send_from_directory('/Users/nahomnigatu/Downloads/campusministrybadges/docs', 'index.html')

# Serve the check-in page
@app.route('/checkin')
def checkin_page():
    """Serve the main check-in page with search functionality"""
    return send_from_directory('/Users/nahomnigatu/Downloads/campusministrybadges/docs', 'index.html')

# Serve static files
@app.route('/docs/<path:filename>')
def serve_docs(filename):
    """Serve files from docs directory"""
    return send_from_directory('/Users/nahomnigatu/Downloads/campusministrybadges/docs', filename)

@app.route('/assets/<path:filename>')
def serve_assets(filename):
    """Serve asset files"""
    return send_from_directory('/Users/nahomnigatu/Downloads/campusministrybadges/docs/assets', filename)

if __name__ == '__main__':
    print("Starting Admin Server...")
    print("Admin panel will be available at: http://localhost:5001")
    print("API endpoints:")
    print("  GET /api/participants - Get all participants")
    print("  POST /api/participants - Add new participant")
    print("  GET /api/export/excel - Export participants to Excel")
    print("  GET /api/stats - Get participant statistics")
    print("  POST /api/checkin - Check in a participant")
    print("  GET /api/checkin?name=NAME - Get check-in status for participant")
    print("  GET /api/checkin/all - Get all checked-in participants")
    print("  GET /api/checkin/count - Get total check-in count")
    print("  GET / - Landing page for public access")
    print("  GET /docs/<file> - Serve check-in and admin pages")
    
    app.run(debug=True, port=5001, host='0.0.0.0')