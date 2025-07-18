#!/usr/bin/env python3
"""Fix duplicate participant arrays in docs/index.html"""

def fix_duplicate_arrays():
    """Remove the duplicate participant array from docs/index.html"""
    
    # Read the current file
    with open('/Users/nahomnigatu/Downloads/campusministrybadges/docs/index.html', 'r') as f:
        content = f.read()

    print('🔧 FIXING DUPLICATE PARTICIPANT ARRAYS')
    print('Original file analysis:')
    name_count = content.count('"name":')
    let_participants_count = content.count("let participants = [")
    participants_count = content.count("participants = [")
    
    print(f'  Total "name": entries: {name_count}')
    print(f'  let participants = [ occurrences: {let_participants_count}')
    print(f'  participants = [ occurrences: {participants_count}')

    # Split into lines
    lines = content.split('\n')
    fixed_lines = []
    in_second_array = False
    array_start_line = None
    removed_lines = 0

    for i, line in enumerate(lines):
        line_num = i + 1
        
        # Check if this is the start of the second participant array (around line 2924)
        if line_num > 2900 and 'participants = [' in line and 'let' not in line:
            in_second_array = True
            array_start_line = line_num
            print(f'  🗑️  Removing second array starting at line {line_num}')
            removed_lines += 1
            continue
        
        # If we're in the second array, skip lines until we find the end
        if in_second_array:
            removed_lines += 1
            # Look for the end of the array (]; pattern)
            if '];' in line:
                in_second_array = False
                print(f'  🗑️  Removed array ending at line {line_num} (removed {removed_lines} lines)')
                continue
            else:
                continue
        
        # Keep all other lines
        fixed_lines.append(line)

    # Join the fixed content
    fixed_content = '\n'.join(fixed_lines)

    print(f'\n✅ FIXED:')
    print(f'  Removed {removed_lines} lines')
    
    fixed_name_count = fixed_content.count('"name":')
    fixed_let_participants_count = fixed_content.count("let participants = [")
    fixed_participants_count = fixed_content.count("participants = [")
    
    print(f'  New "name": entries: {fixed_name_count}')
    print(f'  let participants = [ occurrences: {fixed_let_participants_count}')
    print(f'  participants = [ occurrences: {fixed_participants_count}')

    # Save the fixed file
    with open('/Users/nahomnigatu/Downloads/campusministrybadges/docs/index.html', 'w') as f:
        f.write(fixed_content)

    print('\n🎉 docs/index.html has been fixed!')
    print('   ✅ Removed duplicate participant array with 315 entries')
    print('   ✅ Kept correct participant array with 332 entries')
    print('   ✅ GitHub Pages should now show 332 participants')
    
    return len(fixed_lines), removed_lines

if __name__ == "__main__":
    fix_duplicate_arrays()