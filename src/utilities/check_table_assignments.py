import pandas as pd

# Read the Excel file
excel_path = '/Users/nahomnigatu/Downloads/campusministrybadges/BADGE_ASSIGNMENTS_FINAL.xlsx'
df = pd.read_excel(excel_path)

print("First 10 rows with table assignments:")
print(df[['First Name ', 'Last Name', 'TABLE #']].head(10))

print("\nTable assignment distribution:")
if 'TABLE #' in df.columns:
    print(df['TABLE #'].value_counts().sort_index())

print("\nChecking specific people from slide 1:")
slide1_names = ['BETHLEHEM', 'PERCI', 'BEZA', 'MEKDES']
for name in slide1_names:
    person_row = df[df['First Name '].str.strip() == name]
    if not person_row.empty:
        table_num = person_row['TABLE #'].iloc[0]
        print(f"{name}: Table {table_num}")
    else:
        print(f"{name}: Not found in Excel file")

print("\nChecking specific people from slide 2:")
slide2_names = ['LUDIANA', 'BEMNET', 'MEKLIT', 'ABYALTE']
for name in slide2_names:
    person_row = df[df['First Name '].str.strip() == name]
    if not person_row.empty:
        table_num = person_row['TABLE #'].iloc[0]
        print(f"{name}: Table {table_num}")
    else:
        print(f"{name}: Not found in Excel file")

print("\nChecking specific people from slide 3:")
slide3_names = ['BETHANY', 'MERON', 'MAKIDA', 'BETEMARIAM']
for name in slide3_names:
    person_row = df[df['First Name '].str.strip() == name]
    if not person_row.empty:
        table_num = person_row['TABLE #'].iloc[0]
        print(f"{name}: Table {table_num}")
    else:
        print(f"{name}: Not found in Excel file")