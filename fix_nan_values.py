#!/usr/bin/env python3
import pandas as pd
import numpy as np

def fix_nan_values_in_csv():
    """Fix NaN values in CSV to be empty strings for better display"""
    
    csv_file = '/Users/nahomnigatu/Downloads/campusministrybadges/data/csv/badge_assignments.csv'
    df = pd.read_csv(csv_file)
    
    print(f"Before fix: {len(df)} participants")
    print(f"NaN table assignments: {df['table_assignment'].isna().sum()}")
    print(f"NaN discussion assignments: {df['discussion_assignment'].isna().sum()}")
    
    # Replace NaN values with empty strings
    df['table_assignment'] = df['table_assignment'].fillna('')
    df['discussion_assignment'] = df['discussion_assignment'].fillna('')
    df['dorm'] = df['dorm'].fillna('')
    
    # Save the updated CSV
    df.to_csv(csv_file, index=False)
    
    print(f"After fix: {len(df)} participants")
    print(f"Empty table assignments: {(df['table_assignment'] == '').sum()}")
    print(f"Empty discussion assignments: {(df['discussion_assignment'] == '').sum()}")
    print("✅ Fixed NaN values in CSV")

if __name__ == "__main__":
    fix_nan_values_in_csv()
