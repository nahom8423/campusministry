# PowerPoint Template Analysis Report

## Template File: CAMPUSMINISTRYBADGE.pptx

### Template Structure
- **Number of slides**: 1
- **Number of shapes**: 28
- **Maximum people per slide**: 4

### Found Placeholders

#### NAME Placeholders
- {{NAME1}} ✓
- {{NAME2}} ✓
- {{NAME3}} ✓
- {{NAME4}} ✓

#### CAMPUS Placeholders
- {{CAMPUS1}} ✓
- {{CAMPUS2}} ✓
- {{CAMPUS3}} ✓
- {{CAMPUS4}} ✓

#### ROLE Placeholders
- {{ROLE1}} ✓
- {{ROLE2}} ✓
- {{ROLE3}} ✓
- {{ROLE4}} ✓

#### DORM Placeholders
- {{DORM1}} ✓
- {{DORM2}} ✓
- {{DORM3}} ✓
- {{DORM4}} ✓

#### TABLE Placeholders
- {{TABLE1}} ✗ (Missing)
- {{TABLE2}} ✗ (Missing)
- {{TABLE3}} ✓
- {{TABLE4}} ✗ (Missing)

#### DISCUSSION Placeholders
- {{DISCUSSION1}} ✓
- {{DISCUSSION2}} ✓
- {{DISCUSSION3}} ✓
- {{DISCUSSION4}} ✓

### Issues Found

1. **TABLE placeholders incomplete**: Only {{TABLE3}} is present in the template. Missing {{TABLE1}}, {{TABLE2}}, and {{TABLE4}}.

2. **6 people per slide not supported**: The template only supports 4 people per slide. Missing placeholders for positions 5 and 6:
   - {{NAME5}}, {{NAME6}}
   - {{CAMPUS5}}, {{CAMPUS6}}
   - {{ROLE5}}, {{ROLE6}}
   - {{DORM5}}, {{DORM6}}
   - {{TABLE5}}, {{TABLE6}}
   - {{DISCUSSION5}}, {{DISCUSSION6}}

### Recommendations

1. **Keep 4 people per slide**: The current template is designed for 4 people per slide maximum.

2. **Fix TABLE placeholders**: If the current code expects {{TABLE1}}, {{TABLE2}}, and {{TABLE4}}, the template should be updated to include these placeholders.

3. **Current code compatibility**: The existing Python scripts in the codebase are correctly configured for 4 people per slide, which matches the template's capabilities.

### Code Analysis

Based on the Python scripts in the codebase:
- `generate_badges.py`: Attempts to use 6 people per slide but falls back to 4 when placeholders are missing
- `generate_badges2.py`: Uses 4 people per slide
- `working.py`: Uses 4 people per slide
- `generate_badges_table_assignment.py`: Uses 4 people per slide
- `generate_east_badges.py`: Uses 4 people per slide (different template)

The code in `generate_badges.py` tries to use 6 people per slide but the template doesn't support it, so it should be updated to stick with 4 people per slide.