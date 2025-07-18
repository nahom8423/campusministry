import pandas as pd
import json

def create_admin_panel_with_data():
    """Create the admin panel HTML file with embedded participant data"""
    
    # Read the badge assignments CSV (this should have the most current data)
    df = pd.read_csv('/Users/nahomnigatu/Downloads/campusministrybadges/input_data/badge_assignments.csv')
    
    participants = []
    
    for _, row in df.iterrows():
        # Clean and format the data
        name = str(row['full_name']).strip()
        campus = str(row['campus']).strip() if pd.notna(row['campus']) else 'NEW'
        dorm = str(row['dorm']).strip() if pd.notna(row['dorm']) else 'N/A'
        table = str(row['table_assignment']).strip() if pd.notna(row['table_assignment']) else 'TBD'
        discussion = str(row['discussion_assignment']).strip() if pd.notna(row['discussion_assignment']) else 'TBD'
        
        # Clean up campus ministry names for display
        if campus == 'NEW':
            campus = 'New Participant'
        elif len(campus) > 50:
            # Truncate very long campus names
            campus = campus[:47] + '...'
        
        participant = {
            'name': name,
            'campus': campus,
            'dorm': dorm,
            'table': table,
            'discussion': discussion
        }
        
        participants.append(participant)
    
    # Sort participants by name for easier searching
    participants.sort(key=lambda x: x['name'])
    
    # Read the enhanced HTML template
    with open('/Users/nahomnigatu/Downloads/campusministrybadges/docs/admin_enhanced.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Convert participants to JavaScript format
    js_data = json.dumps(participants, indent=2, ensure_ascii=False)
    
    # Replace the placeholder with actual data
    html_content = html_content.replace('const PARTICIPANT_DATA = [];', f'const PARTICIPANT_DATA = {js_data};')
    
    # Write the final HTML file
    with open('/Users/nahomnigatu/Downloads/campusministrybadges/output/admin_panel_final.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ Created /Users/nahomnigatu/Downloads/campusministrybadges/output/admin_panel_final.html with {len(participants)} participants")
    print(f"\n📊 Admin Panel Features:")
    print(f"   - Password protected (default: campus2024)")
    print(f"   - Real-time statistics dashboard")
    print(f"   - Full participant list with search & filters")
    print(f"   - Manual check-in/check-out capability")
    print(f"   - Export to CSV functionality")
    print(f"   - Sortable columns")
    print(f"   - Live updates every 30 seconds")
    
    print(f"\n🔐 Login Credentials:")
    print(f"   Password: campus2024")
    print(f"   (You can change this in the HTML file)")
    
    print(f"\n📈 Sample Statistics:")
    campus_counts = {}
    for p in participants:
        campus_counts[p['campus']] = campus_counts.get(p['campus'], 0) + 1
    
    print(f"   Total Participants: {len(participants)}")
    print(f"   Unique Campuses: {len(campus_counts)}")
    print(f"   Top Campus: {max(campus_counts.items(), key=lambda x: x[1])}")
    
    return len(participants)

def create_admin_qr_code():
    """Create a QR code for the admin panel"""
    try:
        import qrcode
        from PIL import Image, ImageDraw, ImageFont
        import os
        
        # Create QR code for admin panel
        current_dir = os.getcwd()
        admin_url = f"file://{current_dir}/admin_panel_final.html"
        
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        
        qr.add_data(admin_url)
        qr.make(fit=True)
        
        # Create QR code image
        qr_img = qr.make_image(fill_color="black", back_color="white")
        
        # Create a larger image with text
        img_width = 400
        img_height = 500
        
        # Create white background
        final_img = Image.new('RGB', (img_width, img_height), 'white')
        
        # Resize QR code to fit nicely
        qr_size = 300
        qr_img = qr_img.resize((qr_size, qr_size), Image.Resampling.LANCZOS)
        
        # Paste QR code in center
        qr_x = (img_width - qr_size) // 2
        qr_y = 60
        final_img.paste(qr_img, (qr_x, qr_y))
        
        # Add text
        draw = ImageDraw.Draw(final_img)
        
        try:
            title_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 24)
            subtitle_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 16)
            instruction_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 14)
        except:
            title_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()
            instruction_font = ImageFont.load_default()
        
        # Add title
        title_text = "🔐 Admin Panel Access"
        title_bbox = draw.textbbox((0, 0), title_text, font=title_font)
        title_width = title_bbox[2] - title_bbox[0]
        title_x = (img_width - title_width) // 2
        draw.text((title_x, 20), title_text, fill="black", font=title_font)
        
        # Add instructions
        instructions = [
            "1. Scan QR code for admin access",
            "2. Enter password: campus2024",
            "3. Monitor check-ins in real-time",
            "4. Export data and manage participants"
        ]
        
        instruction_y = qr_y + qr_size + 20
        for instruction in instructions:
            bbox = draw.textbbox((0, 0), instruction, font=instruction_font)
            text_width = bbox[2] - bbox[0]
            text_x = (img_width - text_width) // 2
            draw.text((text_x, instruction_y), instruction, fill="black", font=instruction_font)
            instruction_y += 25
        
        final_img.save('admin_qr_code.png', 'PNG')
        print(f"✅ Created admin_qr_code.png")
        
    except ImportError:
        print("⚠️  QR code generation skipped (qrcode package not available)")

if __name__ == "__main__":
    create_admin_panel_with_data()
    create_admin_qr_code()
    
    print(f"\n🎯 Files Ready:")
    print(f"   - admin_panel_final.html (main admin interface)")
    print(f"   - admin_qr_code.png (QR code for admin access)")
    print(f"\n💡 Next Steps:")
    print(f"   1. Host admin_panel_final.html on a web server")
    print(f"   2. Update QR code URL for production")
    print(f"   3. Change admin password in HTML file")
    print(f"   4. Print QR codes for staff access")