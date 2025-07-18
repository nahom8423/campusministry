#!/usr/bin/env python3

def create_comparison_report():
    # Expected values from CSV
    expected_assignments = {
        "Slide 1": [
            ("BETHLEHEM ADUGNA", "SAT T30 | SUN T35"),
            ("PERCI WOLDAY", "SAT T2 | SUN T9"),
            ("BEZA ASHEBIR", "SAT T17 | SUN T24"),
            ("MEKDES ASSFAW", "SAT T23 | SUN T2")
        ],
        "Slide 2": [
            ("LUDIANA ATNAFU", "SAT T35 | SUN T11"),
            ("BEMNET HAILU", "SAT T25 | SUN T19"),
            ("MEKLIT ABERA", "SAT T22 | SUN T11"),
            ("ABYALTE BEKELE", "SAT T7 | SUN T29")
        ],
        "Slide 3": [
            ("BETHANY ESAYAS", "SAT T20 | SUN T11"),
            ("MERON BELAYNEH/AMSALU", "SAT T5 | SUN T7"),
            ("MAKIDA BEKELE", "SAT T6 | SUN T27"),
            ("BETEMARIAM MESFIN", "SAT T34 | SUN T32")
        ]
    }
    
    # Actual values found in PowerPoint
    actual_assignments = {
        "Slide 1": [
            ("BETHLEHEM ADUGNA", "SAT T17 | SUN T24"),
            ("PERCI WOLDAY", "SAT T17 | SUN T24"),
            ("BEZA ASHEBIR", "SAT T17 | SUN T24"),
            ("MEKDES ASSFAW", "SAT T17 | SUN T24")
        ],
        "Slide 2": [
            ("LUDIANA ATNAFU", "SAT T22 | SUN T11"),
            ("BEMNET HAILU", "SAT T22 | SUN T11"),
            ("MEKLIT ABERA", "SAT T22 | SUN T11"),
            ("ABYALTE BEKELE", "SAT T22 | SUN T11")
        ],
        "Slide 3": [
            ("BETHANY ESAYAS", "SAT T6 | SUN T27"),
            ("MERON BELAYNEH/AMSALU", "SAT T6 | SUN T27"),
            ("MAKIDA BEKELE", "SAT T6 | SUN T27"),
            ("BETEMARIAM MESFIN", "SAT T6 | SUN T27")
        ]
    }
    
    print("=== COMPARISON REPORT ===\n")
    
    for slide_name in expected_assignments:
        print(f"=== {slide_name.upper()} ===")
        expected = expected_assignments[slide_name]
        actual = actual_assignments[slide_name]
        
        for i in range(len(expected)):
            name, expected_table = expected[i]
            _, actual_table = actual[i]
            
            status = "✓ CORRECT" if expected_table == actual_table else "✗ INCORRECT"
            print(f"{name}:")
            print(f"  Expected: {expected_table}")
            print(f"  Actual:   {actual_table}")
            print(f"  Status:   {status}")
            print()
        
        print("-" * 50)

if __name__ == "__main__":
    create_comparison_report()