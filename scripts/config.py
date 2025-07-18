#!/usr/bin/env python3
"""
Configuration file for Campus Ministry Badge System
Contains all file paths and settings
"""

import os

# Base directory - parent of the scripts folder
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Data folder paths
DATA_DIR = os.path.join(BASE_DIR, 'data')
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')
WEBSITE_DIR = os.path.join(BASE_DIR, 'website')

# Data files
EXCEL_FILES = {
    'main': os.path.join(DATA_DIR, 'BADGE (CLEAN FILE).xlsx'),
    'dorm_assignment_1': os.path.join(DATA_DIR, 'General Assembly Dorm Assignment1.xlsx'),
    'dorm_assignment_2': os.path.join(DATA_DIR, 'General Assembly Dorm Assignment2.xlsx'),
    'dorm_assignment_main': os.path.join(DATA_DIR, 'General Assembly Dorm Assignment.xlsx'),
    'final_assignments': os.path.join(DATA_DIR, 'BADGE_ASSIGNMENTS_FINAL.xlsx'),
    'east_registration': os.path.join(DATA_DIR, 'East-registration .xlsx'),
    'badge_with_assignments': os.path.join(OUTPUT_DIR, 'BADGE_WITH_ASSIGNMENTS.xlsx')
}

# Template files
TEMPLATE_FILES = {
    'main_badge': os.path.join(TEMPLATES_DIR, 'CAMPUSMINISTRYBADGE.pptx'),
    'patched_badge': os.path.join(TEMPLATES_DIR, 'CAMPUSMINISTRYBADGE_PATCHED.pptx'),
    'mkdc_badge': os.path.join(TEMPLATES_DIR, 'mkdcbadges.pptx'),
    'filled_badges': os.path.join(OUTPUT_DIR, 'filled_badges.pptx')
}

# CSV files
CSV_FILES = {
    'badge_assignments': os.path.join(DATA_DIR, 'badge_assignments.csv')
}

# Website files
WEBSITE_FILES = {
    'checkin': os.path.join(WEBSITE_DIR, 'index.html'),
    'admin': os.path.join(WEBSITE_DIR, 'admin.html'),
    'assets': os.path.join(WEBSITE_DIR, 'assets')
}

# Output files
OUTPUT_FILES = {
    'filled_badges_pdf': os.path.join(OUTPUT_DIR, 'filled_badges.pdf'),
    'badges_pdf': os.path.join(OUTPUT_DIR, 'CAMPUSMINISTRYBADGES.pdf')
}

# Default admin password
ADMIN_PASSWORD = "campus2024"

def get_data_file(key):
    """Get the path to a data file"""
    return EXCEL_FILES.get(key, None)

def get_template_file(key):
    """Get the path to a template file"""
    return TEMPLATE_FILES.get(key, None)

def ensure_directories():
    """Ensure all necessary directories exist"""
    directories = [DATA_DIR, TEMPLATES_DIR, OUTPUT_DIR, WEBSITE_DIR, WEBSITE_FILES['assets']]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

if __name__ == "__main__":
    print("Campus Ministry Badge System Configuration")
    print(f"Base Directory: {BASE_DIR}")
    print(f"Data Directory: {DATA_DIR}")
    print(f"Templates Directory: {TEMPLATES_DIR}")
    print(f"Output Directory: {OUTPUT_DIR}")
    print(f"Website Directory: {WEBSITE_DIR}")
    
    print("\nEnsuring directories exist...")
    ensure_directories()
    print("✅ All directories ready!")
