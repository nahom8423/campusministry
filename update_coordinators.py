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
    name = name.replace('(', '').replace(')', '')
    
    return name

def update_coordinators():
    """Update coordinators in the CSV file"""
    
    # List of coordinators from the user
    new_coordinators = [
        "Yeabsera Deressa",
        "Rakeb Bonger", 
        "Niert ( menen)Atenafu",
        "Bezawit Mezretab",
        "Kidus Daniel",
        "Nahom Teshome",
        "Rahel Abebe",
        "Ananya Fikru Debebe",
        "Barok Haile",
        "Tsega Tizazu",
        "Bemnet Hailu",
        "Kalabe deressa( host)",
        "Arsema Abate",
        "Meklit Abera"
    ]
    
    # Read the current CSV
    df = pd.read_csv('/Users/nahomnigatu/Downloads/campusministrybadges/data/csv/badge_assignments.csv')
    
    # Create backup
    backup_file = '/Users/nahomnigatu/Downloads/campusministrybadges/data/csv/badge_assignments_backup_before_coordinator_update.csv'
    df.to_csv(backup_file, index=False)
    print(f"Created backup: {backup_file}")
    
    # Track updates
    updated_count = 0
    not_found = []
    
    for coord_name in new_coordinators:
        coord_clean = clean_name_for_comparison(coord_name)
        
        # Find matching participants
        found = False
        for idx, row in df.iterrows():
            participant_clean = clean_name_for_comparison(row['full_name'])
            
            # Check for exact match or partial match
            if coord_clean == participant_clean or coord_clean in participant_clean or participant_clean in coord_clean:
                # Update role to COORDINATOR
                old_role = df.at[idx, 'role']
                df.at[idx, 'role'] = 'COORDINATOR'
                print(f"Updated {row['full_name']}: {old_role} -> COORDINATOR")
                updated_count += 1
                found = True
                break
        
        if not found:
            not_found.append(coord_name)
    
    # Save updated CSV
    df.to_csv('/Users/nahomnigatu/Downloads/campusministrybadges/data/csv/badge_assignments.csv', index=False)
    
    print(f"\n✅ Updated {updated_count} participants to COORDINATOR role")
    print(f"Total coordinators now: {len(df[df['role'] == 'COORDINATOR'])}")
    
    if not_found:
        print(f"\n⚠️  Could not find matches for {len(not_found)} names:")
        for name in not_found:
            print(f"  - {name}")
            
            # Show potential matches
            name_clean = clean_name_for_comparison(name)
            potential_matches = []
            for _, row in df.iterrows():
                participant_clean = clean_name_for_comparison(row['full_name'])
                # Check if any word from the coordinator name appears in participant name
                coord_words = name_clean.split()
                participant_words = participant_clean.split()
                
                for coord_word in coord_words:
                    if len(coord_word) > 3:  # Only check words longer than 3 characters
                        for participant_word in participant_words:
                            if coord_word in participant_word or participant_word in coord_word:
                                potential_matches.append(row['full_name'])
                                break
            
            if potential_matches:
                print(f"    Potential matches: {potential_matches[:3]}")
    
    # Show final role breakdown
    print(f"\n📊 Final role breakdown:")
    print(df['role'].value_counts())
    
    return updated_count

if __name__ == "__main__":
    update_coordinators()