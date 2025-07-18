#!/usr/bin/env python3
"""
Generate QR codes for GitHub Pages hosting
"""

import qrcode
from PIL import Image, ImageDraw, ImageFont
import os

def create_github_qr(page_name, title, instructions, output_filename):
    """Create a QR code for GitHub Pages hosting"""
    
    # You'll need to replace this with your actual GitHub Pages URL
    github_url = f"https://YOUR-USERNAME.github.io/campusministrybadges/{page_name}"
    
    # Create QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    
    qr.add_data(github_url)
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
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    title_x = (img_width - title_width) // 2
    draw.text((title_x, 20), title, fill="black", font=title_font)
    
    # Add instructions
    instruction_y = qr_y + qr_size + 20
    for instruction in instructions:
        bbox = draw.textbbox((0, 0), instruction, font=instruction_font)
        text_width = bbox[2] - bbox[0]
        text_x = (img_width - text_width) // 2
        draw.text((text_x, instruction_y), instruction, fill="black", font=instruction_font)
        instruction_y += 25
    
    # Save both to output and docs/assets
    output_path = f"output/{output_filename}"
    docs_path = f"docs/assets/{output_filename}"
    
    final_img.save(output_path, 'PNG')
    final_img.save(docs_path, 'PNG')
    
    print(f"✅ Created {output_filename} in both output/ and docs/assets/")
    print(f"📱 URL: {github_url}")

def main():
    print("🔗 Generating GitHub Pages QR Codes...")
    print("⚠️  Remember to update YOUR-USERNAME in the script with your actual GitHub username!")
    
    # Create check-in QR code
    create_github_qr(
        page_name="",  # Root page
        title="🎯 Campus Ministry Check-In",
        instructions=[
            "1. Scan this QR code with your phone",
            "2. Type your name to search",
            "3. Confirm your details",
            "4. Check in successfully!"
        ],
        output_filename="github_checkin_qr.png"
    )
    
    # Create simple check-in QR code
    create_github_qr(
        page_name="",
        title="",
        instructions=[],
        output_filename="github_checkin_qr_simple.png"
    )
    
    # Create admin QR code  
    create_github_qr(
        page_name="admin.html",
        title="🔐 Admin Panel Access",
        instructions=[
            "1. Scan QR code for admin access",
            "2. Enter password: campus2024",
            "3. Monitor check-ins in real-time",
            "4. Export data and manage participants"
        ],
        output_filename="github_admin_qr.png"
    )
    
    # Create simple admin QR code
    create_github_qr(
        page_name="admin.html",
        title="",
        instructions=[],
        output_filename="github_admin_qr_simple.png"
    )
    
    print("\n📋 Next Steps:")
    print("1. Update YOUR-USERNAME in this script with your GitHub username")
    print("2. Run the script again to generate updated QR codes")
    print("3. Push to GitHub and enable Pages")
    print("4. Print the QR codes for participants and staff")

if __name__ == "__main__":
    main()