#!/usr/bin/env python3
"""
Comprehensive Excel Cross-Reference Checker
Identifies missing names across all Excel sheets to ensure no one is left out.
"""

import pandas as pd
import os
from datetime import datetime

def clean_name_for_comparison(name):
    """Clean and normalize names for comparison"""
    if pd.isna(name) or str(name).strip() == '':
        return ''
    
    clean_name = str(name).strip().upper()
    
    # Remove language indicators and prefixes
    indicators_to_remove = [
        '&A', '&E', ' &A', ' &E', '&A ', '&E ', 
        ' -A', '- A', '-A', ' -E', '- E', '-E',
        ' E&A', 'E&A', ' E&A ', 'E&A ',
        ' E', 'E', ' A', 'A',
        ' -New', '- New', '-New', ' New', 'New',
        ' 1', '1'  # Remove number prefixes
    ]
    
    for indicator in indicators_to_remove:
        clean_name = clean_name.replace(indicator, '')
    
    # Remove extra whitespace
    clean_name = ' '.join(clean_name.split())
    
    return clean_name.strip()

def extract_names_from_excel(file_path, sheet_name=None):
    """Extract names from an Excel file"""
    if not os.path.exists(file_path):
        print(f"⚠️  File not found: {file_path}")
        return []
    
    try:
        print(f"📖 Reading: {file_path}")
        # Try to read Excel file, handling different sheet scenarios
        try:
            df = pd.read_excel(file_path, sheet_name=sheet_name)
        except Exception as e:
            # Try reading with different sheet name or first sheet
            try:
                df = pd.read_excel(file_path, sheet_name=0)
            except Exception as e2:
                print(f"  ❌ Error reading Excel file: {e2}")
                return []
        
        # Handle case where df might be a dict (multiple sheets)
        if isinstance(df, dict):
            # Take the first sheet
            df = list(df.values())[0]
        
        # Find potential name columns
        name_columns = []
        for col in df.columns:
            col_lower = str(col).lower()
            if any(keyword in col_lower for keyword in ['name', 'first', 'last', 'participant']):
                name_columns.append(col)
        
        if not name_columns:
            print(f"  ⚠️  No name columns found in {file_path}")
            return []
        
        print(f"  📋 Found name columns: {name_columns}")
        
        names = []
        for _, row in df.iterrows():
            # Try to construct full names from available columns
            if 'First Name' in df.columns and 'Last Name' in df.columns:
                first = str(row.get('First Name', '')).strip()
                last = str(row.get('Last Name', '')).strip()
                if first and last:
                    full_name = f"{first} {last}"
                    names.append({
                        'raw_name': full_name,
                        'clean_name': clean_name_for_comparison(full_name),
                        'first_name': first,
                        'last_name': last,
                        'source_file': os.path.basename(file_path),
                        'campus': row.get('Campus Minstry', row.get('Which campus ministry are you a part of? In case, you are not part of the listed campus ministries, it\'s open to you as well, and please come and join us! ', 'Unknown'))
                    })
            elif 'First Name ' in df.columns and 'Last Name' in df.columns:  # Note the space
                first = str(row.get('First Name ', '')).strip()
                last = str(row.get('Last Name', '')).strip()
                if first and last:
                    full_name = f"{first} {last}"
                    names.append({
                        'raw_name': full_name,
                        'clean_name': clean_name_for_comparison(full_name),
                        'first_name': first,
                        'last_name': last,
                        'source_file': os.path.basename(file_path),
                        'campus': row.get('Campus Minstry', row.get('Which campus ministry are you a part of? In case, you are not part of the listed campus ministries, it\'s open to you as well, and please come and join us! ', 'Unknown'))
                    })
            else:
                # Try to find any name column
                for col in name_columns:
                    name_value = str(row.get(col, '')).strip()
                    if name_value and name_value.lower() not in ['nan', 'none', '']:
                        names.append({
                            'raw_name': name_value,
                            'clean_name': clean_name_for_comparison(name_value),
                            'first_name': name_value.split()[0] if name_value.split() else '',
                            'last_name': ' '.join(name_value.split()[1:]) if len(name_value.split()) > 1 else '',
                            'source_file': os.path.basename(file_path),
                            'campus': row.get('Campus Minstry', row.get('Which campus ministry are you a part of? In case, you are not part of the listed campus ministries, it\'s open to you as well, and please come and join us! ', 'Unknown'))
                        })
                        break
        
        # Remove duplicates and empty names
        unique_names = []
        seen_names = set()
        for name_info in names:
            if name_info['clean_name'] and name_info['clean_name'] not in seen_names:
                unique_names.append(name_info)
                seen_names.add(name_info['clean_name'])
        
        print(f"  ✅ Found {len(unique_names)} unique names")
        return unique_names
        
    except Exception as e:
        print(f"  ❌ Error reading {file_path}: {e}")
        return []

def main():
    print("🔍 Campus Ministry Excel Cross-Reference Checker")
    print("=" * 50)
    
    # Define all Excel files to check
    excel_files = [
        'input_data/BADGE (CLEAN FILE).xlsx',
        'input_data/BADGE_ASSIGNMENTS_FINAL.xlsx',
        'input_data/General Assembly Dorm Assignment.xlsx',
        'input_data/General Assembly Dorm Assignment1.xlsx',
        'input_data/General Assembly Dorm Assignment2.xlsx',
        'input_data/East-registration .xlsx'
    ]
    
    # Also check CSV for current assignments
    csv_file = 'input_data/badge_assignments.csv'
    
    all_names = {}  # Dictionary to store names by source file
    
    # Read all Excel files
    for file_path in excel_files:
        if os.path.exists(file_path):
            names = extract_names_from_excel(file_path)
            if names:
                all_names[file_path] = names
        else:
            print(f"⚠️  File not found: {file_path}")
    
    # Read CSV file (current assignments)
    if os.path.exists(csv_file):
        print(f"📖 Reading: {csv_file}")
        try:
            df_csv = pd.read_csv(csv_file)
            csv_names = []
            for _, row in df_csv.iterrows():
                full_name = str(row.get('full_name', '')).strip()
                if full_name:
                    csv_names.append({
                        'raw_name': full_name,
                        'clean_name': clean_name_for_comparison(full_name),
                        'first_name': full_name.split()[0] if full_name.split() else '',
                        'last_name': ' '.join(full_name.split()[1:]) if len(full_name.split()) > 1 else '',
                        'source_file': 'badge_assignments.csv',
                        'campus': row.get('campus', 'Unknown')
                    })
            all_names[csv_file] = csv_names
            print(f"  ✅ Found {len(csv_names)} names in CSV")
        except Exception as e:
            print(f"  ❌ Error reading CSV: {e}")
    
    # Create master list from current assignments (CSV)
    master_names = set()
    if csv_file in all_names:
        master_names = {name['clean_name'] for name in all_names[csv_file]}
        print(f"\n📋 Master list has {len(master_names)} names from badge_assignments.csv")
    
    # Find missing names
    missing_names = []
    duplicate_sources = {}
    
    for file_path, names in all_names.items():
        if file_path == csv_file:
            continue  # Skip the master list
        
        print(f"\n🔍 Checking {os.path.basename(file_path)}...")
        file_missing = []
        
        for name_info in names:
            clean_name = name_info['clean_name']
            
            if clean_name not in master_names:
                file_missing.append(name_info)
                missing_names.append(name_info)
                print(f"  ❌ Missing: {name_info['raw_name']} ({name_info['campus']})")
            else:
                # Track duplicates across files
                if clean_name not in duplicate_sources:
                    duplicate_sources[clean_name] = []
                duplicate_sources[clean_name].append(file_path)
        
        if not file_missing:
            print(f"  ✅ All names from {os.path.basename(file_path)} are in the master list")
        else:
            print(f"  📊 Found {len(file_missing)} missing names")
    
    # Generate comprehensive report
    print("\n" + "=" * 70)
    print("📊 COMPREHENSIVE ANALYSIS REPORT")
    print("=" * 70)
    
    print(f"\n📈 SUMMARY:")
    print(f"  • Total unique names in master list: {len(master_names)}")
    print(f"  • Total missing names found: {len(missing_names)}")
    print(f"  • Files analyzed: {len(excel_files)}")
    
    if missing_names:
        print(f"\n❌ MISSING NAMES ({len(missing_names)}):")
        print("-" * 40)
        
        # Group by source file
        missing_by_file = {}
        for name_info in missing_names:
            file_name = name_info['source_file']
            if file_name not in missing_by_file:
                missing_by_file[file_name] = []
            missing_by_file[file_name].append(name_info)
        
        for file_name, names in missing_by_file.items():
            print(f"\n📂 From {file_name}:")
            for name_info in names:
                print(f"  • {name_info['raw_name']}")
                print(f"    Campus: {name_info['campus']}")
                print(f"    Clean name: {name_info['clean_name']}")
                print()
    
    # Generate detailed report file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = f"missing_names_report_{timestamp}.txt"
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("CAMPUS MINISTRY MISSING NAMES REPORT\n")
        f.write("=" * 50 + "\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write("SUMMARY:\n")
        f.write(f"  • Total unique names in master list: {len(master_names)}\n")
        f.write(f"  • Total missing names found: {len(missing_names)}\n")
        f.write(f"  • Files analyzed: {len(excel_files)}\n\n")
        
        if missing_names:
            f.write("MISSING NAMES DETAILS:\n")
            f.write("-" * 30 + "\n")
            
            for file_name, names in missing_by_file.items():
                f.write(f"\nFrom {file_name}:\n")
                for name_info in names:
                    f.write(f"  • {name_info['raw_name']}\n")
                    f.write(f"    Campus: {name_info['campus']}\n")
                    f.write(f"    Clean name: {name_info['clean_name']}\n")
                    f.write(f"    First: {name_info['first_name']}\n")
                    f.write(f"    Last: {name_info['last_name']}\n\n")
        
        f.write("\nALL FILES ANALYZED:\n")
        for file_path in excel_files:
            if os.path.exists(file_path):
                count = len(all_names.get(file_path, []))
                f.write(f"  • {file_path}: {count} names\n")
            else:
                f.write(f"  • {file_path}: NOT FOUND\n")
    
    print(f"\n💾 Detailed report saved to: {report_file}")
    
    if missing_names:
        print(f"\n⚠️  ACTION REQUIRED:")
        print(f"   Found {len(missing_names)} people who might be missing from the main system!")
        print(f"   Review the report and consider adding them to the badge generation.")
    else:
        print(f"\n✅ SUCCESS:")
        print(f"   All names from additional Excel files are already in the main system!")
    
    # Create a CSV file with missing names for easy review
    if missing_names:
        missing_df = pd.DataFrame(missing_names)
        missing_csv = f"missing_names_{timestamp}.csv"
        missing_df.to_csv(missing_csv, index=False)
        print(f"📊 Missing names CSV saved to: {missing_csv}")

if __name__ == "__main__":
    main()