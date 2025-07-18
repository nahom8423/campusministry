#!/usr/bin/env python3
"""
QR Code Generator for Public Access Check-In System
This script generates QR codes that work with ANY WiFi/cellular connection
"""

import qrcode
import os
from PIL import Image, ImageDraw, ImageFont
import sys

def create_qr_code(url, filename, title, description):
    """Create a QR code with title and description"""
    
    # Create QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    # Create QR code image
    qr_img = qr.make_image(fill_color="black", back_color="white")
    
    # Create a larger image with text
    width = 800
    height = 1000
    
    # Create white background
    img = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(img)
    
    # Resize QR code to fit
    qr_size = 500
    qr_img = qr_img.resize((qr_size, qr_size), Image.Resampling.LANCZOS)
    
    # Position QR code in center
    qr_x = (width - qr_size) // 2
    qr_y = 200
    img.paste(qr_img, (qr_x, qr_y))
    
    # Try to load a nice font, fall back to default if not available
    try:
        title_font = ImageFont.truetype("Arial.ttf", 60)
        desc_font = ImageFont.truetype("Arial.ttf", 40)
        url_font = ImageFont.truetype("Arial.ttf", 24)
    except:
        try:
            title_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 60)
            desc_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 40)
            url_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 24)
        except:
            title_font = ImageFont.load_default()
            desc_font = ImageFont.load_default()
            url_font = ImageFont.load_default()
    
    # Add title
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    title_x = (width - title_width) // 2
    draw.text((title_x, 50), title, fill="black", font=title_font)
    
    # Add description
    desc_bbox = draw.textbbox((0, 0), description, font=desc_font)
    desc_width = desc_bbox[2] - desc_bbox[0]
    desc_x = (width - desc_width) // 2
    draw.text((desc_x, 130), description, fill="black", font=desc_font)
    
    # Add URL below QR code
    url_y = qr_y + qr_size + 30
    url_bbox = draw.textbbox((0, 0), url, font=url_font)
    url_width = url_bbox[2] - url_bbox[0]
    url_x = (width - url_width) // 2
    draw.text((url_x, url_y), url, fill="gray", font=url_font)
    
    # Add instructions
    instructions = [
        "1. Open your phone's camera app",
        "2. Point camera at this QR code",
        "3. Tap the notification that appears",
        "4. Search your name and check in!",
        "",
        "Works with ANY phone & internet connection!"
    ]
    
    inst_y = url_y + 50
    for instruction in instructions:
        if instruction:  # Skip empty lines
            inst_bbox = draw.textbbox((0, 0), instruction, font=desc_font)
            inst_width = inst_bbox[2] - inst_bbox[0]
            inst_x = (width - inst_width) // 2
            draw.text((inst_x, inst_y), instruction, fill="black", font=desc_font)
        inst_y += 45
    
    # Save the image
    img.save(filename, quality=95)
    print(f"✅ Created {filename}")

def main():
    """Main function to generate QR codes"""
    
    if len(sys.argv) != 2:
        print("❌ Usage: python3 generate_public_qr.py <public_url>")
        print("   Example: python3 generate_public_qr.py https://abc123.ngrok.io")
        sys.exit(1)
    
    public_url = sys.argv[1].rstrip('/')
    
    print("🎯 Generating QR codes for public access...")
    print(f"   Public URL: {public_url}")
    
    # Create output directory
    output_dir = "public_qr_codes"
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate check-in QR code
    checkin_url = public_url
    create_qr_code(
        checkin_url,
        f"{output_dir}/checkin_qr_public.png",
        "📱 CHECK IN",
        "Scan to check in to the event"
    )
    
    # Generate admin QR code
    admin_url = f"{public_url}/docs/admin.html"
    create_qr_code(
        admin_url,
        f"{output_dir}/admin_qr_public.png",
        "🔧 ADMIN PANEL",
        "Staff only - requires password"
    )
    
    print("")
    print("🎉 QR codes generated successfully!")
    print("="*50)
    print(f"📱 Check-in QR: {output_dir}/checkin_qr_public.png")
    print(f"🔧 Admin QR: {output_dir}/admin_qr_public.png")
    print("")
    print("✅ WHAT TO DO NEXT:")
    print("1. Print both QR codes")
    print("2. Post check-in QR at entrance/registration")
    print("3. Give admin QR to staff members")
    print("4. Attendees can now check in with their own phone/data!")
    print("")
    print("📊 FEATURES:")
    print("- Works with ANY smartphone")
    print("- No app downloads required")
    print("- Uses attendee's own internet connection")
    print("- Real-time sync across all devices")
    print("- Secure HTTPS connection")

if __name__ == "__main__":
    main()
