#!/usr/bin/env python3
"""
Add missing high priority participants to the main system while preserving existing assignments.
This script will:
1. Read the high priority missing participants
2. Add them to the main Excel file
3. Assign new table/discussion numbers for new people only
4. Preserve existing assignments
5. Regenerate all necessary files
"""

import pandas as pd
import os
import random
from datetime import datetime
import shutil

def clean_name_conservative(name):
    """Clean name by removing ONLY language indicators, keeping all letters intact"""
    if pd.isna(name) or str(name).strip() == '':
        return ''
    
    clean_name = str(name).strip()
    
    # Remove language indicators - be very specific and conservative
    language_indicators = [
        '&A', '&E', 
        ' -A', '- A', '-A', 
        ' -E', '- E', '-E',
        ' E&A', 'E&A',
        ' A&E', 'A&E',
        ' New', '-New', '- New',
        ' 1', '1'
    ]
    
    for indicator in language_indicators:
        clean_name = clean_name.replace(indicator, '')
    
    # Remove extra whitespace
    clean_name = ' '.join(clean_name.split())
    
    return clean_name.strip()

def extract_language_preference(name):
    """Extract language preference from name indicators"""
    if pd.isna(name) or str(name).strip() == '':
        return 'English'
    
    name_str = str(name).strip()
    
    # Check for Amharic indicators
    if any(indicator in name_str for indicator in [' -A', '- A', '-A', '&A']):
        return 'Amharic'
    
    # Everything else defaults to English
    return 'English'

def get_next_table_assignment(existing_assignments, language_pref):
    """Get next available table assignment"""
    # Find the highest table number used
    table_numbers = []
    for assignment in existing_assignments:
        if 'SAT T' in assignment and 'SUN T' in assignment:
            # Extract table numbers
            parts = assignment.split('|')
            if len(parts) >= 2:
                sat_part = parts[0].strip()
                sun_part = parts[1].strip()
                
                # Extract numbers
                sat_num = sat_part.replace('SAT T', '').strip()
                sun_num = sun_part.replace('SUN T', '').strip()
                
                try:
                    table_numbers.append(int(sat_num))
                    table_numbers.append(int(sun_num))
                except:
                    pass
    
    # Find max table number or default to 35
    max_table = max(table_numbers) if table_numbers else 35
    
    # Generate new assignment
    sat_table = random.randint(1, min(35, max_table))
    sun_table = random.randint(1, min(35, max_table))
    
    return f"SAT T{sat_table} | SUN T{sun_table}"

def get_next_discussion_assignment(existing_assignments, language_pref):
    """Get next available discussion assignment"""
    # Find the highest discussion number used
    discussion_numbers = []
    prefix = 'DA' if language_pref == 'Amharic' else 'DE'
    
    for assignment in existing_assignments:
        if assignment.startswith(prefix):
            try:
                num = int(assignment.split()[-1])
                discussion_numbers.append(num)
            except:
                pass
    
    # Find max discussion number or default to 25
    max_discussion = max(discussion_numbers) if discussion_numbers else 25
    next_discussion = min(max_discussion + 1, 35)
    
    return f"{prefix} {next_discussion}"

def add_missing_participants():
    """Add missing high priority participants to the main system"""
    
    print("🔄 Adding Missing High Priority Participants")
    print("=" * 60)
    
    # Find the high priority CSV file
    csv_files = [f for f in os.listdir('.') if f.startswith('high_priority_additions_') and f.endswith('.csv')]
    if not csv_files:
        print("❌ No high priority additions CSV found. Please run analyze_missing_names.py first.")
        return
    
    latest_csv = max(csv_files, key=os.path.getctime)
    print(f"📖 Reading high priority additions: {latest_csv}")
    
    # Read high priority missing participants
    missing_df = pd.read_csv(latest_csv)
    print(f"📊 Found {len(missing_df)} high priority missing participants")
    
    # Remove duplicates (same person in multiple files)
    missing_df = missing_df.drop_duplicates(subset=['clean_name'], keep='first')
    print(f"📊 After removing duplicates: {len(missing_df)} unique participants")
    
    # Read current main Excel file
    main_excel = 'input_data/BADGE (CLEAN FILE).xlsx'
    if not os.path.exists(main_excel):
        print(f"❌ Main Excel file not found: {main_excel}")
        return
    
    print(f"📖 Reading main Excel file: {main_excel}")
    main_df = pd.read_excel(main_excel)
    original_count = len(main_df)
    print(f"📊 Current participants in main file: {original_count}")
    
    # Read current CSV assignments to preserve them
    csv_file = 'input_data/badge_assignments.csv'
    existing_assignments = {}
    existing_table_assignments = []
    existing_discussion_assignments = []
    
    if os.path.exists(csv_file):
        print(f"📖 Reading existing assignments: {csv_file}")
        assignments_df = pd.read_csv(csv_file)
        
        for _, row in assignments_df.iterrows():
            name = row['full_name']
            existing_assignments[name] = {
                'table': row['table_assignment'],
                'discussion': row['discussion_assignment']
            }
            existing_table_assignments.append(row['table_assignment'])
            existing_discussion_assignments.append(row['discussion_assignment'])
        
        print(f"📊 Loaded {len(existing_assignments)} existing assignments")
    
    # Process each missing participant
    new_participants = []
    skipped_participants = []
    
    for _, row in missing_df.iterrows():
        raw_name = row['raw_name']
        clean_name = clean_name_conservative(raw_name)
        campus = row['campus']
        
        # Skip if already exists in main file
        name_parts = clean_name.split()
        if len(name_parts) >= 2:
            first_name = name_parts[0]
            last_name = ' '.join(name_parts[1:])
            
            # Check if already exists
            existing = main_df[
                (main_df['First Name '].str.upper().str.strip() == first_name.upper()) &
                (main_df['Last Name'].str.upper().str.strip() == last_name.upper())
            ]
            
            if not existing.empty:
                skipped_participants.append(raw_name)
                continue
            
            # Extract language preference
            language_pref = extract_language_preference(raw_name)
            
            # Assign table and discussion
            table_assignment = get_next_table_assignment(existing_table_assignments, language_pref)
            discussion_assignment = get_next_discussion_assignment(existing_discussion_assignments, language_pref)
            
            # Add to tracking lists
            existing_table_assignments.append(table_assignment)
            existing_discussion_assignments.append(discussion_assignment)
            
            # Create new participant record
            new_participant = {
                'First Name ': first_name,
                'Last Name': last_name,
                'Which campus ministry are you a part of? In case, you are not part of the listed campus ministries, it\'s open to you as well, and please come and join us! ': campus,
                'What is your preferred language for sermons and/or engaging in group discussions?': language_pref,
                'DORM NUMBER': 'N/A',  # Will be assigned later
                'TABLE #': table_assignment,
                'DISCUSSION #': discussion_assignment,
                'State you residence in': '',
                'If your are a College Student, which year are you?': '',
                'Gender': ''
            }
            
            new_participants.append(new_participant)
            print(f"  ✅ Added: {clean_name} -> {table_assignment} | {discussion_assignment}")
    
    print(f"\n📊 PROCESSING RESULTS:")
    print(f"  • New participants to add: {len(new_participants)}")
    print(f"  • Skipped (already exist): {len(skipped_participants)}")
    
    if skipped_participants:
        print(f"\n⚠️  SKIPPED PARTICIPANTS (already exist):")
        for name in skipped_participants:
            print(f"  • {name}")
    
    if new_participants:
        # Create backup of original file
        backup_file = f"{main_excel}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        shutil.copy2(main_excel, backup_file)
        print(f"\n💾 Created backup: {backup_file}")
        
        # Add new participants to main DataFrame
        new_df = pd.DataFrame(new_participants)
        updated_main_df = pd.concat([main_df, new_df], ignore_index=True)
        
        # Save updated main Excel file
        updated_main_df.to_excel(main_excel, index=False)
        print(f"✅ Updated main Excel file with {len(new_participants)} new participants")
        print(f"📊 Total participants now: {len(updated_main_df)} (was {original_count})")
        
        # Update CSV assignments
        print(f"\n🔄 Updating CSV assignments...")
        
        # Create new CSV records for new participants
        new_csv_records = []
        for i, participant in enumerate(new_participants):
            record = {
                'slide': 0,  # Will be updated by badge generation
                'slot': 0,   # Will be updated by badge generation
                'full_name': f"{participant['First Name ']} {participant['Last Name']}",
                'role': 'COORDINATOR' if any(keyword in participant['Which campus ministry are you a part of? In case, you are not part of the listed campus ministries, it\'s open to you as well, and please come and join us! '].lower() 
                                           for keyword in ['coordinator', 'head of', 'media']) else 'PARTICIPANT',
                'campus': participant['Which campus ministry are you a part of? In case, you are not part of the listed campus ministries, it\'s open to you as well, and please come and join us! '],
                'dorm': 'N/A',
                'table_assignment': participant['TABLE #'],
                'discussion_assignment': participant['DISCUSSION #']
            }
            new_csv_records.append(record)
        
        # Add to existing CSV
        if os.path.exists(csv_file):
            existing_csv_df = pd.read_csv(csv_file)
            new_csv_df = pd.DataFrame(new_csv_records)
            updated_csv_df = pd.concat([existing_csv_df, new_csv_df], ignore_index=True)
        else:
            updated_csv_df = pd.DataFrame(new_csv_records)
        
        updated_csv_df.to_csv(csv_file, index=False)
        print(f"✅ Updated CSV with {len(new_csv_records)} new assignments")
        
        print(f"\n🎯 SUMMARY:")
        print(f"  • {len(new_participants)} new participants added")
        print(f"  • All existing assignments preserved")
        print(f"  • New table assignments: {len(set(p['TABLE #'] for p in new_participants))}")
        print(f"  • New discussion assignments: {len(set(p['DISCUSSION #'] for p in new_participants))}")
        
        print(f"\n💡 NEXT STEPS:")
        print(f"  1. Run badge generation to create badges for all participants")
        print(f"  2. Update check-in system with new participants")
        print(f"  3. Regenerate admin panel with updated count")
        
        return True
    else:
        print(f"\n✅ No new participants to add - all were already in the system!")
        return False

def regenerate_system():
    """Regenerate badges and check-in system with updated participants"""
    print(f"\n🔄 Regenerating System Components...")
    
    # Regenerate badges
    print("🎨 Regenerating badges...")
    os.system("python3 src/badge_generation/generate_badges.py")
    
    # Regenerate check-in system
    print("📱 Regenerating check-in system...")
    os.system("python3 src/utilities/generate_checkin_data.py")
    
    # Regenerate admin panel
    print("🖥️ Regenerating admin panel...")
    os.system("python3 src/utilities/generate_admin_panel.py")
    
    print("✅ System regeneration complete!")

if __name__ == "__main__":
    success = add_missing_participants()
    
    if success:
        regenerate = input("\n🤔 Would you like to regenerate badges and check-in system now? (y/n): ")
        if regenerate.lower() in ['y', 'yes']:
            regenerate_system()
        else:
            print("\n💡 Don't forget to regenerate the system components when ready!")
    
    print("\n🎉 Process complete!")