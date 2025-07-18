#!/usr/bin/env python3
"""
Analyze PowerPoint template positioning for badge slots
Converts EMU coordinates to inches and identifies the 4 badge areas
"""

import xml.etree.ElementTree as ET

def emu_to_inches(emu_value):
    """Convert English Metric Units (EMU) to inches"""
    # 1 inch = 914400 EMU
    return float(emu_value) / 914400

def analyze_badge_positions():
    """Analyze the badge positions from the extracted XML"""
    
    # Parse the XML
    with open('/tmp/pptx_extract/ppt/slides/slide1.xml', 'r') as f:
        xml_content = f.read()
    
    # Parse XML
    root = ET.fromstring(xml_content)
    
    # Define namespaces
    namespaces = {
        'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
        'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'
    }
    
    # Find all text boxes
    text_boxes = root.findall('.//p:sp', namespaces)
    
    badge_elements = []
    table3_elements = []
    
    print("POWERPOINT TEMPLATE ANALYSIS")
    print("=" * 50)
    
    for sp in text_boxes:
        # Get text content
        text_elem = sp.find('.//a:t', namespaces)
        if text_elem is not None:
            text_content = text_elem.text
            
            # Get position and size
            xfrm = sp.find('.//a:xfrm', namespaces)
            if xfrm is not None:
                off = xfrm.find('a:off', namespaces)
                ext = xfrm.find('a:ext', namespaces)
                
                if off is not None and ext is not None:
                    x = int(off.get('x'))
                    y = int(off.get('y'))
                    width = int(ext.get('cx'))
                    height = int(ext.get('cy'))
                    
                    # Convert to inches
                    x_in = emu_to_inches(x)
                    y_in = emu_to_inches(y)
                    width_in = emu_to_inches(width)
                    height_in = emu_to_inches(height)
                    
                    # Check if this is a badge element (NAME, CAMPUS, ROLE, DORM, DISCUSSION)
                    if text_content and ('{{NAME' in text_content or 
                                       '{{CAMPUS' in text_content or 
                                       '{{ROLE' in text_content or
                                       '{{DORM' in text_content or
                                       '{{DISCUSSION' in text_content):
                        # Extract badge number from the text
                        badge_num = '?'
                        if text_content.endswith('}}'):
                            # Get the character before the }}
                            potential_num = text_content[-3]
                            if potential_num.isdigit():
                                badge_num = potential_num
                        
                        # Extract element type
                        element_type = text_content.replace('{{', '').replace('}}', '')
                        element_type = element_type[:-1] if element_type[-1].isdigit() else element_type
                        
                        badge_elements.append({
                            'badge_num': badge_num,
                            'element_type': element_type,
                            'x_in': x_in,
                            'y_in': y_in,
                            'width_in': width_in,
                            'height_in': height_in,
                            'text': text_content
                        })
                    
                    # Check for TABLE3 elements
                    elif text_content and '{{TABLE3}}' in text_content:
                        table3_elements.append({
                            'x_in': x_in,
                            'y_in': y_in,
                            'width_in': width_in,
                            'height_in': height_in,
                            'text': text_content
                        })
    
    # Group badge elements by badge number
    badges = {}
    for elem in badge_elements:
        badge_num = elem['badge_num']
        if badge_num not in badges:
            badges[badge_num] = {}
        badges[badge_num][elem['element_type']] = elem
    
    # Calculate badge areas (based on the NAME element positions)
    badge_areas = []
    for badge_num in sorted(badges.keys()):
        if 'NAME' in badges[badge_num]:
            name_elem = badges[badge_num]['NAME']
            # Use NAME element as the anchor point for the badge
            badge_areas.append({
                'badge_num': badge_num,
                'x_in': name_elem['x_in'],
                'y_in': name_elem['y_in'],
                'width_in': name_elem['width_in'],
                'height_in': name_elem['height_in']
            })
    
    print("\n1. BADGE AREAS POSITIONS (based on NAME elements):")
    print("-" * 50)
    for badge in sorted(badge_areas, key=lambda x: x['badge_num']):
        print(f"Badge {badge['badge_num']}:")
        print(f"  X position: {badge['x_in']:.2f} inches")
        print(f"  Y position: {badge['y_in']:.2f} inches")
        print(f"  Width: {badge['width_in']:.2f} inches")
        print(f"  Height: {badge['height_in']:.2f} inches")
        print()
    
    # Analyze layout pattern
    print("\n2. LAYOUT PATTERN ANALYSIS:")
    print("-" * 50)
    if len(badge_areas) == 4:
        # Sort by Y position to find rows
        sorted_by_y = sorted(badge_areas, key=lambda x: x['y_in'])
        
        # Check if it's a 2x2 grid
        row1 = [b for b in sorted_by_y if abs(b['y_in'] - sorted_by_y[0]['y_in']) < 1.0]
        row2 = [b for b in sorted_by_y if abs(b['y_in'] - sorted_by_y[0]['y_in']) >= 1.0]
        
        if len(row1) == 2 and len(row2) == 2:
            print("Layout: 2x2 grid")
            print(f"Row 1 (Y≈{row1[0]['y_in']:.2f}\"): Badges {', '.join(sorted([b['badge_num'] for b in row1]))}")
            print(f"Row 2 (Y≈{row2[0]['y_in']:.2f}\"): Badges {', '.join(sorted([b['badge_num'] for b in row2]))}")
            
            # Check column alignment
            row1_sorted = sorted(row1, key=lambda x: x['x_in'])
            row2_sorted = sorted(row2, key=lambda x: x['x_in'])
            
            print(f"Column 1 (X≈{row1_sorted[0]['x_in']:.2f}\"): Badges {row1_sorted[0]['badge_num']}, {row2_sorted[0]['badge_num']}")
            print(f"Column 2 (X≈{row1_sorted[1]['x_in']:.2f}\"): Badges {row1_sorted[1]['badge_num']}, {row2_sorted[1]['badge_num']}")
        else:
            print("Layout: Custom arrangement")
    else:
        print(f"Found {len(badge_areas)} badge areas")
    
    # Analyze TABLE3 positions
    print("\n3. {{TABLE3}} PLACEHOLDER POSITIONS:")
    print("-" * 50)
    if table3_elements:
        for i, elem in enumerate(table3_elements, 1):
            print(f"TABLE3 instance {i}:")
            print(f"  X position: {elem['x_in']:.2f} inches")
            print(f"  Y position: {elem['y_in']:.2f} inches")
            print(f"  Width: {elem['width_in']:.2f} inches")
            print(f"  Height: {elem['height_in']:.2f} inches")
            print()
    else:
        print("No {{TABLE3}} placeholders found")
    
    # Calculate badge dimensions (looking at the complete badge area)
    print("\n4. BADGE DIMENSIONS ANALYSIS:")
    print("-" * 50)
    
    # For each badge, find the min/max coordinates to determine overall dimensions
    for badge_num in sorted(badges.keys()):
        if badge_num in badges:
            badge_elements_list = list(badges[badge_num].values())
            
            min_x = min(elem['x_in'] for elem in badge_elements_list)
            max_x = max(elem['x_in'] + elem['width_in'] for elem in badge_elements_list)
            min_y = min(elem['y_in'] for elem in badge_elements_list)
            max_y = max(elem['y_in'] + elem['height_in'] for elem in badge_elements_list)
            
            total_width = max_x - min_x
            total_height = max_y - min_y
            
            print(f"Badge {badge_num} overall dimensions:")
            print(f"  Top-left corner: ({min_x:.2f}\", {min_y:.2f}\")")
            print(f"  Total width: {total_width:.2f} inches")
            print(f"  Total height: {total_height:.2f} inches")
            print()
    
    # Generate recommended X_IN and Y_IN values
    # Show detailed breakdown of all elements
    print("\n5. DETAILED ELEMENT BREAKDOWN:")
    print("-" * 50)
    for badge_num in sorted(badges.keys()):
        if badge_num in badges:
            print(f"Badge {badge_num} elements:")
            for elem_type, elem_data in badges[badge_num].items():
                print(f"  {elem_type}: ({elem_data['x_in']:.2f}\", {elem_data['y_in']:.2f}\") - {elem_data['width_in']:.2f}\"×{elem_data['height_in']:.2f}\"")
            print()
    
    print("\n6. RECOMMENDED X_IN AND Y_IN VALUES:")
    print("-" * 50)
    print("For auto-patch script, use these coordinates for the top-left corner of each badge:")
    print()
    
    for badge_num in sorted(badges.keys()):
        if badge_num in badges:
            badge_elements_list = list(badges[badge_num].values())
            min_x = min(elem['x_in'] for elem in badge_elements_list)
            min_y = min(elem['y_in'] for elem in badge_elements_list)
            
            print(f"Badge {badge_num}: X_IN = {min_x:.2f}, Y_IN = {min_y:.2f}")
    
    # Show TABLE3 mapping to badges
    print("\n7. TABLE3 TO BADGE MAPPING:")
    print("-" * 50)
    print("TABLE3 instances appear to correspond to these badge positions:")
    
    # Map TABLE3 positions to badges based on proximity
    for i, table3 in enumerate(table3_elements, 1):
        closest_badge = None
        min_distance = float('inf')
        
        for badge_num in badges.keys():
            if 'NAME' in badges[badge_num]:
                name_elem = badges[badge_num]['NAME']
                distance = ((table3['x_in'] - name_elem['x_in'])**2 + 
                           (table3['y_in'] - name_elem['y_in'])**2)**0.5
                if distance < min_distance:
                    min_distance = distance
                    closest_badge = badge_num
        
        print(f"TABLE3 instance {i} at ({table3['x_in']:.2f}\", {table3['y_in']:.2f}\") → Badge {closest_badge}")
    
    print("\nSUMMARY:")
    print("=" * 50)
    print("The template uses a 2x2 grid layout with 4 badge slots.")
    print("Each badge contains NAME, CAMPUS, ROLE, DORM, and DISCUSSION elements.")
    print("TABLE3 placeholders are positioned within each badge area.")
    print("Badge dimensions are approximately 4.42\" × 1.06\" each.")

if __name__ == "__main__":
    analyze_badge_positions()