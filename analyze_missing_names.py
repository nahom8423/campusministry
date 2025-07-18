#!/usr/bin/env python3
"""
Analyze and filter relevant missing participants from the cross-reference check.
This script focuses on the most important missing participants who should be added.
"""

import pandas as pd
import os
from datetime import datetime

def analyze_missing_names():
    """Analyze the missing names and identify the most relevant ones to add"""
    
    print("🔍 Analyzing Missing Names for Relevance")
    print("=" * 50)
    
    # Read the most recent missing names report
    try:
        # Find the most recent CSV file
        csv_files = [f for f in os.listdir('.') if f.startswith('missing_names_') and f.endswith('.csv')]
        if not csv_files:
            print("❌ No missing names CSV found. Please run check_missing_names.py first.")
            return
        
        latest_csv = max(csv_files, key=os.path.getctime)
        print(f"📖 Reading: {latest_csv}")
        
        df = pd.read_csv(latest_csv)
        print(f"📊 Total missing names: {len(df)}")
        
    except Exception as e:
        print(f"❌ Error reading CSV: {e}")
        return
    
    # Filter out irrelevant entries
    print("\n🔍 Filtering relevant missing names...")
    
    # Remove entries with missing/invalid names
    df = df[df['clean_name'].notna()]
    df = df[~df['clean_name'].str.contains('NN NN', na=False)]
    df = df[~df['clean_name'].str.contains('NAN', na=False)]
    
    print(f"📊 After removing invalid names: {len(df)}")
    
    # Group by source file for analysis
    relevant_missing = {
        'campus_ministry_participants': [],
        'coordinators_and_staff': [],
        'new_participants': [],
        'east_registration': []
    }
    
    for _, row in df.iterrows():
        source_file = row['source_file']
        campus = str(row['campus']).lower()
        name = row['raw_name']
        
        # Skip East registration for now (different event)
        if 'east-registration' in source_file.lower():
            relevant_missing['east_registration'].append(row)
            continue
        
        # Identify coordinators and staff
        if any(keyword in campus for keyword in ['coordinator', 'media', 'head of', 'staff']):
            relevant_missing['coordinators_and_staff'].append(row)
        # Identify new participants (those with "1" or "New" prefix)
        elif any(keyword in name for keyword in ['1', 'New', '-New', '- New']):
            relevant_missing['new_participants'].append(row)
        # Other campus ministry participants
        elif not any(keyword in campus for keyword in ['unknown', 'nan', 'i don\'t have']):
            relevant_missing['campus_ministry_participants'].append(row)
    
    print(f"\n📊 CATEGORIZED MISSING NAMES:")
    print(f"  • Campus Ministry Participants: {len(relevant_missing['campus_ministry_participants'])}")
    print(f"  • Coordinators & Staff: {len(relevant_missing['coordinators_and_staff'])}")
    print(f"  • New Participants: {len(relevant_missing['new_participants'])}")
    print(f"  • East Registration: {len(relevant_missing['east_registration'])}")
    
    # Generate focused report
    print(f"\n" + "=" * 60)
    print("🎯 PRIORITY MISSING PARTICIPANTS")
    print("=" * 60)
    
    # Priority 1: Coordinators and Staff
    if relevant_missing['coordinators_and_staff']:
        print(f"\n🔥 HIGH PRIORITY - Coordinators & Staff ({len(relevant_missing['coordinators_and_staff'])}):")
        print("-" * 50)
        for row in relevant_missing['coordinators_and_staff']:
            print(f"  • {row['raw_name']}")
            print(f"    Role: {row['campus']}")
            print(f"    Source: {row['source_file']}")
            print()
    
    # Priority 2: New Participants 
    if relevant_missing['new_participants']:
        print(f"\n📋 MEDIUM PRIORITY - New Participants ({len(relevant_missing['new_participants'])}):")
        print("-" * 50)
        for row in relevant_missing['new_participants']:
            print(f"  • {row['raw_name']}")
            print(f"    Campus: {row['campus']}")
            print(f"    Source: {row['source_file']}")
            print()
    
    # Priority 3: Campus Ministry Participants
    if relevant_missing['campus_ministry_participants']:
        print(f"\n👥 STANDARD PRIORITY - Campus Ministry Participants ({len(relevant_missing['campus_ministry_participants'])}):")
        print("-" * 50)
        for row in relevant_missing['campus_ministry_participants']:
            print(f"  • {row['raw_name']}")
            print(f"    Campus: {row['campus']}")
            print(f"    Source: {row['source_file']}")
            print()
    
    # Create actionable CSV files
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # High priority additions
    high_priority = relevant_missing['coordinators_and_staff'] + relevant_missing['new_participants']
    if high_priority:
        high_priority_df = pd.DataFrame(high_priority)
        high_priority_csv = f"high_priority_additions_{timestamp}.csv"
        high_priority_df.to_csv(high_priority_csv, index=False)
        print(f"\n💾 High priority additions saved to: {high_priority_csv}")
    
    # All relevant additions
    all_relevant = (relevant_missing['coordinators_and_staff'] + 
                   relevant_missing['new_participants'] + 
                   relevant_missing['campus_ministry_participants'])
    if all_relevant:
        all_relevant_df = pd.DataFrame(all_relevant)
        all_relevant_csv = f"all_relevant_additions_{timestamp}.csv"
        all_relevant_df.to_csv(all_relevant_csv, index=False)
        print(f"📊 All relevant additions saved to: {all_relevant_csv}")
    
    print(f"\n" + "=" * 60)
    print("📋 RECOMMENDATIONS")
    print("=" * 60)
    
    total_to_add = len(all_relevant)
    print(f"🎯 IMMEDIATE ACTION NEEDED:")
    print(f"  • {len(high_priority)} high priority people should be added immediately")
    print(f"  • {total_to_add} total relevant people found across all files")
    print(f"  • {len(relevant_missing['east_registration'])} East registration participants (different event)")
    
    if high_priority:
        print(f"\n🔥 HIGH PRIORITY ADDITIONS:")
        for person in high_priority:
            print(f"  • {person['raw_name']} ({person['campus']})")
    
    print(f"\n💡 NEXT STEPS:")
    print(f"  1. Review high_priority_additions_{timestamp}.csv")
    print(f"  2. Add these people to the main Excel file")
    print(f"  3. Regenerate badges with updated participant list")
    print(f"  4. Update check-in system with new participants")
    
    return len(high_priority), total_to_add

if __name__ == "__main__":
    analyze_missing_names()