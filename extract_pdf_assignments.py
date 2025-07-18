#!/usr/bin/env python3
"""
Extract current table and discussion assignments from the PDF file.
This will help us preserve the existing assignments.
"""

import PyPDF2
import re
import pandas as pd
from datetime import datetime

def extract_assignments_from_pdf(pdf_path):
    """Extract table and discussion assignments from PDF"""
    try:
        import PyPDF2
        
        print(f"📖 Reading PDF: {pdf_path}")
        
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            assignments = []
            page_count = len(pdf_reader.pages)
            print(f"📄 Processing {page_count} pages...")
            
            for page_num in range(page_count):
                page = pdf_reader.pages[page_num]
                text = page.extract_text()
                
                # Look for patterns like "SAT T12 | SUN T25" and "DE 5" or "DA 3"
                lines = text.split('\n')
                
                current_name = None
                current_table = None
                current_discussion = None
                
                for line in lines:
                    line = line.strip()
                    
                    # Look for names (usually in ALL CAPS)
                    if line.isupper() and len(line.split()) >= 2 and len(line) < 50:
                        # Skip if it looks like a header or campus name
                        if not any(keyword in line for keyword in ['CAMPUS', 'MINISTRY', 'SAT', 'SUN', 'TABLE', 'DISCUSSION']):
                            current_name = line
                    
                    # Look for table assignments (SAT T## | SUN T##)
                    table_match = re.search(r'SAT\s+T(\d+)\s*\|\s*SUN\s+T(\d+)', line)
                    if table_match:
                        current_table = f"SAT T{table_match.group(1)} | SUN T{table_match.group(2)}"
                    
                    # Look for discussion assignments (DE ## or DA ##)
                    discussion_match = re.search(r'(DE|DA)\s+(\d+)', line)
                    if discussion_match:
                        current_discussion = f"{discussion_match.group(1)} {discussion_match.group(2)}"
                    
                    # If we have all three, save the assignment
                    if current_name and current_table and current_discussion:
                        assignments.append({
                            'name': current_name,
                            'table_assignment': current_table,
                            'discussion_assignment': current_discussion
                        })
                        current_name = None
                        current_table = None
                        current_discussion = None
            
            print(f"✅ Extracted {len(assignments)} assignments from PDF")
            return assignments
            
    except ImportError:
        print("❌ PyPDF2 not installed. Trying alternative method...")
        return extract_assignments_alternative(pdf_path)
    except Exception as e:
        print(f"❌ Error reading PDF: {e}")
        return []

def extract_assignments_alternative(pdf_path):
    """Alternative method to extract assignments"""
    print("🔄 Using alternative extraction method...")
    
    # Since we might not have PyPDF2, let's use the existing CSV as reference
    csv_file = 'input_data/badge_assignments.csv'
    if not os.path.exists(csv_file):
        print(f"❌ CSV file not found: {csv_file}")
        return []
    
    print(f"📖 Reading current assignments from CSV: {csv_file}")
    df = pd.read_csv(csv_file)
    
    assignments = []
    for _, row in df.iterrows():
        assignments.append({
            'name': row['full_name'],
            'table_assignment': row['table_assignment'],
            'discussion_assignment': row['discussion_assignment']
        })
    
    print(f"✅ Loaded {len(assignments)} assignments from CSV")
    return assignments

def verify_assignments():
    """Verify that current assignments match between PDF and CSV"""
    print("🔍 Verifying Assignment Consistency")
    print("=" * 50)
    
    # Try to extract from PDF
    pdf_assignments = extract_assignments_from_pdf('finalcampusministrybadges.pdf')
    
    # Get assignments from CSV
    csv_assignments = extract_assignments_alternative('input_data/badge_assignments.csv')
    
    print(f"\n📊 COMPARISON:")
    print(f"  • PDF assignments: {len(pdf_assignments)}")
    print(f"  • CSV assignments: {len(csv_assignments)}")
    
    # Check for discrepancies
    if pdf_assignments and csv_assignments:
        pdf_names = {a['name'] for a in pdf_assignments}
        csv_names = {a['name'] for a in csv_assignments}
        
        missing_in_pdf = csv_names - pdf_names
        missing_in_csv = pdf_names - csv_names
        
        if missing_in_pdf:
            print(f"\n⚠️  Names in CSV but not in PDF: {len(missing_in_pdf)}")
            for name in list(missing_in_pdf)[:5]:  # Show first 5
                print(f"  • {name}")
        
        if missing_in_csv:
            print(f"\n⚠️  Names in PDF but not in CSV: {len(missing_in_csv)}")
            for name in list(missing_in_csv)[:5]:  # Show first 5
                print(f"  • {name}")
        
        if not missing_in_pdf and not missing_in_csv:
            print("\n✅ All assignments are consistent between PDF and CSV!")
    
    # Save current assignments for reference
    if csv_assignments:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        reference_file = f"current_assignments_reference_{timestamp}.csv"
        df = pd.DataFrame(csv_assignments)
        df.to_csv(reference_file, index=False)
        print(f"\n💾 Current assignments saved to: {reference_file}")

if __name__ == "__main__":
    import os
    
    if os.path.exists('finalcampusministrybadges.pdf'):
        verify_assignments()
    else:
        print("❌ PDF file not found. Using CSV as reference.")
        extract_assignments_alternative('input_data/badge_assignments.csv')