#!/usr/bin/env python3
"""
Final verification of table assignments in both PowerPoint and PDF files
"""

import csv
import pdfplumber
import zipfile
import xml.etree.ElementTree as ET
import re
import os

def load_csv_data():
    """Load expected data from CSV"""
    csv_path = '/Users/nahomnigatu/Downloads/campusministrybadges/badge_assignments.csv'
    assignments = {}
    
    with open(csv_path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            slide_num = int(row['slide'])
            if slide_num not in assignments:
                assignments[slide_num] = []
            
            assignments[slide_num].append({
                'name': row['full_name'],
                'table_assignment': row['table_assignment'],
                'slot': int(row['slot'])
            })
    
    return assignments

def check_pptx_assignments():
    """Check PowerPoint assignments"""
    print("POWERPOINT FILE ANALYSIS:")
    print("=" * 50)
    
    pptx_path = '/Users/nahomnigatu/Downloads/campusministrybadges/filled_badges.pptx'
    extract_path = '/tmp/pptx_extract'
    
    # Clean up any existing extraction
    if os.path.exists(extract_path):
        import shutil
        shutil.rmtree(extract_path)
    
    # Extract PowerPoint file
    with zipfile.ZipFile(pptx_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)
    
    pptx_results = {}
    
    for slide_num in range(1, 4):
        slide_path = f'{extract_path}/ppt/slides/slide{slide_num}.xml'
        
        if not os.path.exists(slide_path):
            print(f"Slide {slide_num}: FILE NOT FOUND")
            continue
        
        # Extract text from slide
        tree = ET.parse(slide_path)
        root = tree.getroot()
        
        namespaces = {
            'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
            'p': 'http://schemas.openxmlformats.org/presentationml/2006/main'
        }
        
        texts = []
        for t_elem in root.findall('.//a:t', namespaces):
            if t_elem.text:
                texts.append(t_elem.text.strip())
        
        # Look for table assignments
        table_assignments = []
        for text in texts:
            if re.search(r'SAT\s+T\d+\s*\|\s*SUN\s+T\d+', text):
                table_assignments.append(text)
        
        # Look for names
        names = []
        name_pattern = r'^[A-Z][A-Z\s/&()-]*[A-Z]$'
        for text in texts:
            if re.match(name_pattern, text) and len(text) > 2 and text != 'PARTICIPANT':
                names.append(text)
        
        pptx_results[slide_num] = {
            'names': names,
            'table_assignments': table_assignments
        }
        
        print(f"Slide {slide_num}:")
        print(f"  Names found: {names}")
        print(f"  Table assignments found: {table_assignments}")
        print()
    
    return pptx_results

def check_pdf_assignments():
    """Check PDF assignments"""
    print("PDF FILE ANALYSIS:")
    print("=" * 50)
    
    pdf_results = {}
    
    try:
        with pdfplumber.open('/Users/nahomnigatu/Downloads/campusministrybadges/filled_badges.pdf') as pdf:
            for page_num in range(min(3, len(pdf.pages))):
                page = pdf.pages[page_num]
                text = page.extract_text()
                
                # Look for table assignments
                table_assignments = []
                if text:
                    for line in text.split('\n'):
                        if re.search(r'SAT\s+T\d+\s*\|\s*SUN\s+T\d+', line):
                            table_assignments.append(line.strip())
                
                # Look for names
                names = []
                name_pattern = r'^[A-Z][A-Z\s/&()-]*[A-Z]$'
                if text:
                    for line in text.split('\n'):
                        line = line.strip()
                        if re.match(name_pattern, line) and len(line) > 2 and line != 'PARTICIPANT':
                            names.append(line)
                
                pdf_results[page_num + 1] = {
                    'names': names,
                    'table_assignments': table_assignments
                }
                
                print(f"Page {page_num + 1}:")
                print(f"  Names found: {names}")
                print(f"  Table assignments found: {table_assignments}")
                print()
    
    except Exception as e:
        print(f"Error reading PDF: {e}")
    
    return pdf_results

def main():
    print("FINAL VERIFICATION OF TABLE ASSIGNMENTS")
    print("=" * 80)
    
    # Load expected data from CSV
    csv_assignments = load_csv_data()
    
    print("EXPECTED ASSIGNMENTS FROM CSV:")
    print("=" * 50)
    for slide_num in range(1, 4):
        if slide_num in csv_assignments:
            print(f"Slide {slide_num}:")
            for person in csv_assignments[slide_num]:
                print(f"  {person['name']}: {person['table_assignment']}")
            print()
    
    # Check PowerPoint file
    pptx_results = check_pptx_assignments()
    
    # Check PDF file
    pdf_results = check_pdf_assignments()
    
    print("SUMMARY:")
    print("=" * 50)
    
    issues_found = False
    
    for slide_num in range(1, 4):
        print(f"Slide/Page {slide_num}:")
        
        # Expected
        expected = csv_assignments.get(slide_num, [])
        expected_names = [p['name'] for p in expected]
        expected_tables = [p['table_assignment'] for p in expected]
        
        print(f"  Expected: {len(expected)} people with unique table assignments")
        
        # PowerPoint
        pptx_data = pptx_results.get(slide_num, {})
        pptx_names = pptx_data.get('names', [])
        pptx_tables = pptx_data.get('table_assignments', [])
        
        print(f"  PowerPoint: {len(pptx_names)} names, {len(pptx_tables)} table assignments")
        if len(pptx_names) != len(expected) or len(pptx_tables) != len(expected):
            print(f"    ❌ ISSUE: Expected {len(expected)} people with table assignments")
            issues_found = True
        
        # PDF
        pdf_data = pdf_results.get(slide_num, {})
        pdf_names = pdf_data.get('names', [])
        pdf_tables = pdf_data.get('table_assignments', [])
        
        print(f"  PDF: {len(pdf_names)} names, {len(pdf_tables)} table assignments")
        if len(pdf_names) != len(expected) or len(pdf_tables) != len(expected):
            print(f"    ❌ ISSUE: Expected {len(expected)} people with table assignments")
            issues_found = True
        
        print()
    
    if issues_found:
        print("❌ VERIFICATION FAILED: Table assignments are NOT showing correctly in the files!")
        print("\nThe PowerPoint and PDF files do not contain the unique table assignments")
        print("that should be displayed for each person according to the CSV data.")
    else:
        print("✅ VERIFICATION PASSED: All table assignments are correctly displayed!")

if __name__ == "__main__":
    main()