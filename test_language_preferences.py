#!/usr/bin/env python3
"""
Test script to verify language preference extraction from names with &A and &E indicators
"""

import pandas as pd

def extract_language_preference(first_name):
    """
    Extract language preference from first name field
    Examples: 
    - 'Solyana E' -> 'English'
    - 'Ruth -A' -> 'Amharic' 
    - 'NAHOM&A' -> 'Amharic'
    - 'SARA&E' -> 'English'
    - 'Miriam E&A' -> 'English' (E takes precedence)
    """
    if pd.isna(first_name) or str(first_name).strip() == '':
        return 'English'
    
    name_str = str(first_name).strip().upper()
    
    # Check for Amharic indicators (in order of priority)
    if '&A' in name_str and '&E' not in name_str:
        return 'Amharic'
    elif ' -A' in name_str or '- A' in name_str or '-A' in name_str:
        return 'Amharic'
    
    # Check for English indicators
    if '&E' in name_str:
        return 'English'
    elif ' E' in name_str or name_str.endswith('E'):
        return 'English'
    
    # Everything else defaults to English (including New, etc.)
    return 'English'

def test_language_preferences():
    """Test the extract_language_preference function with various name formats"""
    
    test_cases = [
        # Test cases with &A (should be Amharic)
        ("NAHOM&A", "Amharic"),
        ("SARA&A", "Amharic"),
        ("BETHLEHEM&A", "Amharic"),
        ("1RUTH&A", "Amharic"),  # With number prefix
        
        # Test cases with &E (should be English)
        ("JOHN&E", "English"),
        ("MARY&E", "English"),
        ("DAVID&E", "English"),
        ("1SARAH&E", "English"),  # With number prefix
        
        # Test cases with both &E and &A (English should take precedence)
        ("MIRIAM&E&A", "English"),
        ("HELEN&A&E", "English"),
        
        # Test cases with old format -A (should be Amharic)
        ("Ruth -A", "Amharic"),
        ("Solyana- A", "Amharic"),
        ("Mark-A", "Amharic"),
        
        # Test cases with old format E (should be English)
        ("Solyana E", "English"),
        ("Mark E", "English"),
        
        # Test cases with no indicators (should default to English)
        ("JOHN", "English"),
        ("MARY", "English"),
        ("", "English"),
        (None, "English"),
        
        # Test cases with 'New' indicator (should be English)
        ("1John New", "English"),
        ("1Mary -New", "English"),
    ]
    
    print("Testing language preference extraction:\n")
    print(f"{'Name':<20} {'Expected':<10} {'Actual':<10} {'Status'}")
    print("-" * 50)
    
    all_passed = True
    
    for name, expected in test_cases:
        actual = extract_language_preference(name)
        status = "✓ PASS" if actual == expected else "✗ FAIL"
        
        if actual != expected:
            all_passed = False
            
        # Handle None case for display
        display_name = str(name) if name is not None else "None"
        
        print(f"{display_name:<20} {expected:<10} {actual:<10} {status}")
    
    print("\n" + "="*50)
    
    if all_passed:
        print("🎉 All tests passed! Language preference extraction is working correctly.")
    else:
        print("❌ Some tests failed. Please review the extract_language_preference function.")
    
    return all_passed

if __name__ == "__main__":
    test_language_preferences()
