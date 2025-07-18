import pandas as pd

def add_remaining_coordinators():
    """Add the remaining coordinators and fix table/discussion assignments"""
    
    # Read the current CSV
    df = pd.read_csv('/Users/nahomnigatu/Downloads/campusministrybadges/data/csv/badge_assignments.csv')
    
    # Remaining coordinators to add
    remaining_coordinators = [
        "Rakeb Bonger",
        "Ananya Fikru Debebe", 
        "Tsega Tizazu"
    ]
    
    # Find the next available slide/slot
    max_slide = df['slide'].max()
    max_slot_for_max_slide = df[df['slide'] == max_slide]['slot'].max()
    
    # Add remaining coordinators
    for i, coordinator in enumerate(remaining_coordinators):
        # Calculate next slot
        if max_slot_for_max_slide < 3:  # Assuming 4 slots per slide (0-3)
            next_slide = max_slide
            next_slot = max_slot_for_max_slide + 1 + i
        else:
            next_slide = max_slide + 1
            next_slot = i
        
        new_row = {
            'slide': next_slide,
            'slot': next_slot,
            'full_name': coordinator,
            'role': 'COORDINATOR',
            'campus': 'NEW',
            'dorm': 'N/A',
            'table_assignment': '',  # Empty for coordinators
            'discussion_assignment': ''  # Empty for coordinators
        }
        
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    
    # Remove table and discussion assignments from ALL coordinators
    coordinator_mask = df['role'] == 'COORDINATOR'
    df.loc[coordinator_mask, 'table_assignment'] = ''
    df.loc[coordinator_mask, 'discussion_assignment'] = ''
    
    # Save the updated CSV
    df.to_csv('/Users/nahomnigatu/Downloads/campusministrybadges/data/csv/badge_assignments.csv', index=False)
    
    print(f"✅ Added {len(remaining_coordinators)} remaining coordinators")
    print(f"📊 Total participants: {len(df)}")
    print(f"👥 Total coordinators: {len(df[df['role'] == 'COORDINATOR'])}")
    print(f"🎯 All coordinators now have no table/discussion assignments")
    
    # Show the new coordinators
    print("\n📋 New coordinators added:")
    for coordinator in remaining_coordinators:
        print(f"   - {coordinator}")
    
    return len(df)

if __name__ == "__main__":
    add_remaining_coordinators()