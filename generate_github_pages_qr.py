#!/usr/bin/env python3
"""
Generate QR codes for GitHub Pages deployment
"""
import qrcode
from PIL import Image, ImageDraw, ImageFont
import os

def create_qr_code_with_label(url, filename, label):
    """Create a QR code with a label"""
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
    
    # Convert to RGB if needed
    if qr_img.mode != 'RGB':
        qr_img = qr_img.convert('RGB')
    
    # Create a larger image to include the label
    img_width = qr_img.width
    img_height = qr_img.height + 100  # Extra space for label
    
    # Create new image with white background
    final_img = Image.new('RGB', (img_width, img_height), 'white')
    
    # Paste QR code
    final_img.paste(qr_img, (0, 0))
    
    # Add label
    draw = ImageDraw.Draw(final_img)
    try:
        font = ImageFont.truetype("Arial.ttf", 24)
    except:
        font = ImageFont.load_default()
    
    # Get text dimensions
    text_width = draw.textlength(label, font=font)
    text_x = (img_width - text_width) // 2
    text_y = qr_img.height + 20
    
    # Draw text
    draw.text((text_x, text_y), label, fill='black', font=font)
    
    # Save image
    final_img.save(filename)
    print(f"✅ Generated: {filename}")

def main():
    # GitHub Pages URL (replace with your actual username)
    github_pages_base = "https://nahom8423.github.io/campusministry"
    
    # Create QR codes directory
    os.makedirs("github_pages_qr", exist_ok=True)
    
    # Check-in QR code
    checkin_url = github_pages_base
    create_qr_code_with_label(
        checkin_url, 
        "github_pages_qr/checkin_qr.png", 
        "📱 CHECK IN HERE"
    )
    
    # Admin QR code
    admin_url = f"{github_pages_base}/admin.html"
    create_qr_code_with_label(
        admin_url, 
        "github_pages_qr/admin_qr.png", 
        "👥 ADMIN PANEL"
    )
    
    print("\n🎉 GitHub Pages QR Codes Generated!")
    print("=" * 50)
    print(f"📱 ATTENDEE CHECK-IN:")
    print(f"   URL: {checkin_url}")
    print(f"   QR Code: github_pages_qr/checkin_qr.png")
    print()
    print(f"👥 ADMIN PANEL:")
    print(f"   URL: {admin_url}")
    print(f"   QR Code: github_pages_qr/admin_qr.png")
    print()
    print("✅ Instructions:")
    print("   1. Print the QR codes")
    print("   2. Attendees scan the CHECK-IN QR code")
    print("   3. Staff uses the ADMIN QR code")
    print("   4. Check-ins are stored locally in browser")
    print()
    print("⚠️  KNOWN ISSUE:")
    print("   Check-ins only show on the same device where they were made")
    print("   This is because GitHub Pages is static and can't sync data between devices")
    print("   Each device stores its own check-in data locally")

if __name__ == "__main__":
    main()
