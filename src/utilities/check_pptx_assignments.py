#!/usr/bin/env python3
"""
Script to check table assignments in filled_badges.pptx
"""

import zipfile
import xml.etree.ElementTree as ET
import re
import os

def extract_text_from_slide(slide_path):
    """Extract all text from a slide XML file"""
    try:
        tree = ET.parse(slide_path)
        root = tree.getroot()
        
        # Define namespaces
        namespaces = {
            'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
            'p': 'http://schemas.openxmlformats.org/presentationml/2006/main'
        }
        
        texts = []
        
        # Find all text elements
        for t_elem in root.findall('.//a:t', namespaces):
            if t_elem.text:
                texts.append(t_elem.text.strip())
        
        return texts
    except Exception as e:
        print(f"Error processing slide: {e}")
        return []

def parse_slide_badges(texts):
    """Parse badge information from slide texts"""
    badges = []
    
    # Look for name patterns (all caps, potentially with spaces and special characters)
    name_pattern = r'^[A-Z][A-Z\s/&()-]*[A-Z]$'
    table_pattern = r'SAT\s+T\d+\s*\|\s*SUN\s+T\d+'
    
    print(f"DEBUG: Found {len(texts)} text elements")
    
    # Find all table assignments first
    table_assignments = []
    for text in texts:
        if re.search(table_pattern, text.strip()):
            table_assignments.append(text.strip())
    
    print(f"DEBUG: Found table assignments: {table_assignments}")
    
    # Find all names
    names = []
    for text in texts:
        clean_text = text.strip()
        if (re.match(name_pattern, clean_text) and 
            len(clean_text) > 2 and 
            clean_text not in ['PARTICIPANT', 'DORM']):
            names.append(clean_text)
    
    print(f"DEBUG: Found names: {names}")
    
    # Try to match names with table assignments
    # Since there should be 4 badges per slide, we'll try to find 4 names
    # and match them with available table assignments
    
    i = 0
    while i < len(texts):
        text = texts[i].strip()
        
        # Check if this looks like a name
        if re.match(name_pattern, text) and len(text) > 2 and text != 'PARTICIPANT' and text != 'DORM':
            name = text
            table_assignment = None
            
            # Look for table assignment in the next few elements
            for j in range(i + 1, min(i + 15, len(texts))):
                next_text = texts[j].strip()
                if re.search(table_pattern, next_text):
                    table_assignment = next_text
                    break
            
            if table_assignment:
                badges.append({
                    'name': name,
                    'table_assignment': table_assignment
                })
        
        i += 1
    
    return badges

def main():
    pptx_path = '/Users/nahomnigatu/Downloads/campusministrybadges/filled_badges.pptx'
    extract_path = '/tmp/pptx_extract'
    
    # Clean up any existing extraction
    if os.path.exists(extract_path):
        import shutil
        shutil.rmtree(extract_path)
    
    # Extract PowerPoint file
    with zipfile.ZipFile(pptx_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)
    
    # Expected assignments from CSV
    expected_assignments = {
        1: [
            ('BETHLEHEM ADUGNA', 'SAT T31 | SUN T30'),
            ('PERCI WOLDAY', 'SAT T30 | SUN T4'),
            ('BEZA ASHEBIR', 'SAT T34 | SUN T34'),
            ('MEKDES ASSFAW', 'SAT T33 | SUN T32')
        ],
        2: [
            ('LUDIANA ATNAFU', 'SAT T6 | SUN T30'),
            ('BEMNET HAILU', 'SAT T27 | SUN T25'),
            ('MEKLIT ABERA', 'SAT T24 | SUN T25'),
            ('ABYALTE BEKELE', 'SAT T31 | SUN T26')
        ],
        3: [
            ('BETHANY ESAYAS', 'SAT T1 | SUN T21'),
            ('MERON BELAYNEH/AMSALU', 'SAT T3 | SUN T5'),
            ('MAKIDA BEKELE', 'SAT T10 | SUN T13'),
            ('BETEMARIAM MESFIN', 'SAT T27 | SUN T22')
        ]
    }
    
    print("Checking first 3 slides of filled_badges.pptx for table assignments...")
    print("=" * 80)
    
    all_correct = True
    
    for slide_num in range(1, 4):
        slide_path = f'{extract_path}/ppt/slides/slide{slide_num}.xml'
        
        if not os.path.exists(slide_path):
            print(f"Slide {slide_num}: FILE NOT FOUND")
            all_correct = False
            continue
        
        print(f"\nSLIDE {slide_num}:")
        print("-" * 20)
        
        texts = extract_text_from_slide(slide_path)
        badges = parse_slide_badges(texts)
        
        if len(badges) == 0:
            print("ERROR: No badges found on this slide!")
            all_correct = False
            continue
        
        expected = expected_assignments[slide_num]
        
        if len(badges) != len(expected):
            print(f"ERROR: Expected {len(expected)} badges, found {len(badges)}")
            all_correct = False
        
        for i, badge in enumerate(badges):
            name = badge['name']
            table_assignment = badge['table_assignment']
            
            if i < len(expected):
                expected_name, expected_table = expected[i]
                
                name_match = name == expected_name
                table_match = table_assignment == expected_table
                
                status = "✓" if (name_match and table_match) else "✗"
                
                print(f"{status} {name}: {table_assignment}")
                
                if not name_match:
                    print(f"   Expected name: {expected_name}")
                    all_correct = False
                
                if not table_match:
                    print(f"   Expected table: {expected_table}")
                    all_correct = False
            else:
                print(f"✗ UNEXPECTED: {name}: {table_assignment}")
                all_correct = False
        
        # Check if any expected badges are missing
        for i in range(len(badges), len(expected)):
            expected_name, expected_table = expected[i]
            print(f"✗ MISSING: {expected_name}: {expected_table}")
            all_correct = False
    
    print("\n" + "=" * 80)
    if all_correct:
        print("✓ ALL ASSIGNMENTS ARE CORRECT!")
    else:
        print("✗ ISSUES FOUND - Table assignments do not match expected values")
    
    return all_correct

if __name__ == "__main__":
    main()