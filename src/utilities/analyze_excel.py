import pandas as pd
import numpy as np

def analyze_excel_file(file_path, file_description):
    """Analyze an Excel file and show its structure"""
    print(f"\n{'='*60}")
    print(f"ANALYZING: {file_description}")
    print(f"File: {file_path}")
    print(f"{'='*60}")
    
    try:
        df = pd.read_excel(file_path)
        
        print(f"Shape: {df.shape} (rows x columns)")
        print(f"\nColumn names:")
        for i, col in enumerate(df.columns, 1):
            print(f"  {i}. {col}")
        
        print(f"\nData types:")
        for col, dtype in df.dtypes.items():
            print(f"  {col}: {dtype}")
        
        print(f"\nFirst 5 rows:")
        print(df.head().to_string())
        
        print(f"\nSample of non-null values for each column:")
        for col in df.columns:
            non_null_values = df[col].dropna()
            if len(non_null_values) > 0:
                sample_value = non_null_values.iloc[0]
                print(f"  {col}: {sample_value}")
            else:
                print(f"  {col}: (all null)")
        
        print(f"\nNull value counts:")
        for col in df.columns:
            null_count = df[col].isnull().sum()
            print(f"  {col}: {null_count} null values")
        
        return df
        
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

def check_names_starting_with_numbers(df, first_name_col):
    """Check for names starting with numbers"""
    print(f"\n{'='*60}")
    print("CHECKING FOR NAMES STARTING WITH NUMBERS")
    print(f"{'='*60}")
    
    if first_name_col not in df.columns:
        print(f"Column '{first_name_col}' not found in the dataframe")
        return
    
    # Filter out null values
    df_filtered = df.dropna(subset=[first_name_col])
    
    # Check for names starting with numbers
    names_with_numbers = []
    for idx, row in df_filtered.iterrows():
        first_name = str(row[first_name_col]).strip()
        if first_name and first_name[0].isdigit():
            names_with_numbers.append({
                'index': idx,
                'first_name': first_name,
                'last_name': row.get('Last Name', 'N/A') if 'Last Name' in row else 'N/A'
            })
    
    if names_with_numbers:
        print(f"Found {len(names_with_numbers)} names starting with numbers:")
        for item in names_with_numbers:
            print(f"  Row {item['index']}: {item['first_name']} {item['last_name']}")
    else:
        print("No names starting with numbers found.")
    
    return names_with_numbers

# Analyze first Excel file
file1 = "/Users/nahomnigatu/Downloads/campusministrybadges/BADGE (CLEAN FILE).xlsx"
df1 = analyze_excel_file(file1, "BADGE (CLEAN FILE).xlsx")

# Analyze second Excel file
file2 = "/Users/nahomnigatu/Downloads/campusministrybadges/General Assembly Dorm Assignment1.xlsx"
df2 = analyze_excel_file(file2, "General Assembly Dorm Assignment1.xlsx")

# Check for names starting with numbers in the second file
if df2 is not None:
    names_with_numbers = check_names_starting_with_numbers(df2, 'First Name')