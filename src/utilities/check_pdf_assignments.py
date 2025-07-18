#!/usr/bin/env python3
"""
Script to check table assignments in filled_badges.pdf
"""

import pdfplumber
import re

def extract_page_data(page_text):
    lines = page_text.split('\n')
    badges = []
    
    # Look for name and table assignment patterns
    name_pattern = r'^[A-Z][A-Z\s/&()-]*[A-Z]$'
    table_pattern = r'SAT\s+T\d+\s*\|\s*SUN\s+T\d+'
    
    for i, line in enumerate(lines):
        line = line.strip()
        if re.match(name_pattern, line) and len(line) > 2 and line != 'PARTICIPANT':
            # Look for table assignment in nearby lines
            for j in range(max(0, i-5), min(len(lines), i+5)):
                if re.search(table_pattern, lines[j]):
                    badges.append({
                        'name': line,
                        'table_assignment': lines[j].strip()
                    })
                    break
    
    return badges

def main():
    # Expected assignments from CSV
    expected_assignments = {
        1: [
            ('BETHLEHEM ADUGNA', 'SAT T26 | SUN T23'),
            ('PERCI WOLDAY', 'SAT T31 | SUN T14'),
            ('BEZA ASHEBIR', 'SAT T5 | SUN T32'),
            ('MEKDES ASSFAW', 'SAT T18 | SUN T33')
        ],
        2: [
            ('LUDIANA ATNAFU', 'SAT T35 | SUN T27'),
            ('BEMNET HAILU', 'SAT T11 | SUN T28'),
            ('MEKLIT ABERA', 'SAT T15 | SUN T10'),
            ('ABYALTE BEKELE', 'SAT T15 | SUN T23')
        ],
        3: [
            ('BETHANY ESAYAS', 'SAT T32 | SUN T2'),
            ('MERON BELAYNEH/AMSALU', 'SAT T28 | SUN T24'),
            ('MAKIDA BEKELE', 'SAT T29 | SUN T23'),
            ('BETEMARIAM MESFIN', 'SAT T26 | SUN T28')
        ]
    }
    
    try:
        with pdfplumber.open('/Users/nahomnigatu/Downloads/campusministrybadges/filled_badges.pdf') as pdf:
            print(f'PDF has {len(pdf.pages)} pages')
            print("Checking first 3 pages of filled_badges.pdf for table assignments...")
            print("=" * 80)
            
            all_correct = True
            
            # Extract data from first 3 pages
            for page_num in range(min(3, len(pdf.pages))):
                page = pdf.pages[page_num]
                text = page.extract_text()
                
                print(f'\nPAGE {page_num + 1}:')
                print("-" * 20)
                
                badges = extract_page_data(text)
                
                if badges:
                    for badge in badges:
                        print(f'{badge["name"]}: {badge["table_assignment"]}')
                else:
                    print('No badges found on this page')
                    # Show first 300 characters to debug
                    print('Text preview:')
                    print(repr(text[:300]))
                    all_correct = False
                
                # Check against expected
                expected = expected_assignments.get(page_num + 1, [])
                if expected:
                    print(f"\nExpected for page {page_num + 1}:")
                    for exp_name, exp_table in expected:
                        print(f"  {exp_name}: {exp_table}")
            
            print("\n" + "=" * 80)
            if all_correct:
                print("PDF analysis complete")
            else:
                print("Issues found in PDF analysis")
    
    except Exception as e:
        print(f'Error reading PDF: {e}')

if __name__ == "__main__":
    main()