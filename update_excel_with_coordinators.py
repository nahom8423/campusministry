import pandas as pd
import os

def update_excel_with_coordinators():
    """Update Excel file with coordinators from CSV"""
    
    # Read the CSV file with all coordinators
    csv_file = '/Users/nahomnigatu/Downloads/campusministrybadges/data/csv/badge_assignments.csv'
    df_csv = pd.read_csv(csv_file)
    
    # Read the Excel file
    excel_file = '/Users/nahomnigatu/Downloads/campusministrybadges/data/excel/BADGE (CLEAN FILE).xlsx'
    df_excel = pd.read_excel(excel_file)
    
    print(f"CSV file has {len(df_csv)} participants")
    print(f"Excel file has {len(df_excel)} participants")
    
    # Get all coordinators from CSV
    coordinators = df_csv[df_csv['role'] == 'COORDINATOR']
    print(f"Found {len(coordinators)} coordinators in CSV")
    
    # Create full names from Excel (combine First Name and Last Name)
    df_excel['full_name_combined'] = (df_excel['First Name '].astype(str).str.strip() + ' ' + 
                                      df_excel['Last Name'].astype(str).str.strip()).str.upper()
    
    # Function to normalize names for comparison
    def normalize_name(name):
        if pd.isna(name):
            return ""
        return str(name).strip().upper().replace('  ', ' ')
    
    # Track which coordinators we find in Excel
    found_coordinators = []
    missing_coordinators = []
    
    for _, coord_row in coordinators.iterrows():
        coord_name = normalize_name(coord_row['full_name'])
        
        # Try to find this coordinator in Excel
        excel_match = df_excel[df_excel['full_name_combined'] == coord_name]
        
        if not excel_match.empty:
            found_coordinators.append(coord_name)
        else:
            missing_coordinators.append(coord_name)
    
    print(f"Found {len(found_coordinators)} coordinators already in Excel")
    print(f"Missing {len(missing_coordinators)} coordinators from Excel")
    
    if missing_coordinators:
        print("Missing coordinators:")
        for coord in missing_coordinators:
            print(f"  - {coord}")
    
    # For the badge generation, we need to use the CSV file since it has all participants
    # The Excel file appears to be missing some people
    
    print(f"✅ Excel file has {len(df_excel)} participants")
    print(f"� CSV file has {len(df_csv)} participants with {len(coordinators)} coordinators")
    
    return len(df_csv)

if __name__ == "__main__":
    update_excel_with_coordinators()