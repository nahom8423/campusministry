#!/usr/bin/env python3
import pandas as pd
import os

def update_excel_with_roles():
    """Update Excel file with role information from CSV"""
    
    # Read the CSV file with role information
    csv_file = '/Users/nahomnigatu/Downloads/campusministrybadges/data/csv/badge_assignments.csv'
    df_csv = pd.read_csv(csv_file)
    
    # Read the Excel file
    excel_file = '/Users/nahomnigatu/Downloads/campusministrybadges/input_data/BADGE_ASSIGNMENTS_FINAL.xlsx'
    df_excel = pd.read_excel(excel_file)
    
    print(f"CSV file has {len(df_csv)} participants")
    print(f"Excel file has {len(df_excel)} participants")
    
    # Create a mapping of full names to roles from CSV
    role_mapping = {}
    for _, row in df_csv.iterrows():
        full_name = str(row['full_name']).strip().upper()
        role = str(row['role']).strip()
        role_mapping[full_name] = role
    
    # Create full names from Excel
    df_excel['full_name_excel'] = (df_excel['First Name '].astype(str).str.strip() + ' ' + 
                                   df_excel['Last Name'].astype(str).str.strip()).str.upper()
    
    # Add role column to Excel data
    df_excel['Role'] = df_excel['full_name_excel'].map(role_mapping).fillna('PARTICIPANT')
    
    # Count coordinators
    coordinators = df_excel[df_excel['Role'] == 'COORDINATOR']
    print(f"Found {len(coordinators)} coordinators in Excel")
    
    # Display coordinators
    print("Coordinators found:")
    for _, coord in coordinators.iterrows():
        print(f"  {coord['First Name ']} {coord['Last Name']} - Table: {coord['TABLE #']}, Discussion: {coord['DISCUSSION #']}")
    
    # Remove the helper column
    df_excel = df_excel.drop('full_name_excel', axis=1)
    
    # Save the updated Excel file
    df_excel.to_excel(excel_file, index=False)
    print(f"Updated Excel file saved: {excel_file}")
    
    return df_excel

if __name__ == "__main__":
    update_excel_with_roles()
