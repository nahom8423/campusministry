import qrcode
from PIL import Image, ImageDraw, ImageFont
import os

def create_checkin_qr_code(url="https://nahom8423.github.io/campusministry/"):
    """
    Create a QR code for the check-in system
    
    Args:
        url: The URL where the check-in page will be hosted
              For local testing, use a file:// URL
              For production, use your web server URL
    """
    
    # Create QR code instance
    qr = qrcode.QRCode(
        version=1,  # Controls the size of the QR code
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    
    # Add data to QR code
    qr.add_data(url)
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
        # Try to use a nice font
        title_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 24)
        subtitle_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 16)
        instruction_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 14)
    except:
        # Fallback to default font
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        instruction_font = ImageFont.load_default()
    
    # Add title
    title_text = "Campus Ministry Check-In"
    title_bbox = draw.textbbox((0, 0), title_text, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    title_x = (img_width - title_width) // 2
    draw.text((title_x, 20), title_text, fill="black", font=title_font)
    
    # Add instructions
    instructions = [
        "1. Scan this QR code with your phone",
        "2. Type your name to search",
        "3. Confirm your details",
        "4. Check in successfully!"
    ]
    
    instruction_y = qr_y + qr_size + 20
    for instruction in instructions:
        bbox = draw.textbbox((0, 0), instruction, font=instruction_font)
        text_width = bbox[2] - bbox[0]
        text_x = (img_width - text_width) // 2
        draw.text((text_x, instruction_y), instruction, fill="black", font=instruction_font)
        instruction_y += 25
    
    # Save the image
    final_img.save('../../docs/assets/github_checkin_qr.png', 'PNG')
    print("QR code saved as '../../docs/assets/github_checkin_qr.png'")
    
    # Also create a simple QR code without decorations
    qr_img_simple = qr.make_image(fill_color="black", back_color="white")
    qr_img_simple.save('../../docs/assets/github_checkin_qr_simple.png', 'PNG')
    print("Simple QR code saved as '../../docs/assets/github_checkin_qr_simple.png'")
    
    return final_img

def create_admin_qr_code(url="https://nahom8423.github.io/campusministry/admin.html"):
    """
    Create a QR code for the admin panel
    
    Args:
        url: The URL where the admin panel will be hosted
    """
    
    # Create QR code instance
    qr = qrcode.QRCode(
        version=1,  # Controls the size of the QR code
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    
    # Add data to QR code
    qr.add_data(url)
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
        # Try to use a nice font
        title_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 24)
        subtitle_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 16)
        instruction_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 14)
    except:
        # Fallback to default font
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        instruction_font = ImageFont.load_default()
    
    # Add title
    title_text = "Campus Ministry Admin Panel"
    title_bbox = draw.textbbox((0, 0), title_text, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    title_x = (img_width - title_width) // 2
    draw.text((title_x, 20), title_text, fill="black", font=title_font)
    
    # Add instructions
    instructions = [
        "1. Scan this QR code with your phone",
        "2. View real-time check-in statistics",
        "3. Monitor attendance data",
        "4. Staff use only"
    ]
    
    instruction_y = qr_y + qr_size + 20
    for instruction in instructions:
        bbox = draw.textbbox((0, 0), instruction, font=instruction_font)
        text_width = bbox[2] - bbox[0]
        text_x = (img_width - text_width) // 2
        draw.text((text_x, instruction_y), instruction, fill="black", font=instruction_font)
        instruction_y += 25
    
    # Save the image
    final_img.save('../../docs/assets/github_admin_qr.png', 'PNG')
    print("Admin QR code saved as '../../docs/assets/github_admin_qr.png'")
    
    # Also create a simple QR code without decorations
    qr_img_simple = qr.make_image(fill_color="black", back_color="white")
    qr_img_simple.save('../../docs/assets/github_admin_qr_simple.png', 'PNG')
    print("Simple admin QR code saved as '../../docs/assets/github_admin_qr_simple.png'")
    
    return final_img

def create_instruction_sheet():
    """Create a simple instruction sheet for staff"""
    
    instructions = """
CAMPUS MINISTRY CHECK-IN SYSTEM
===============================

SETUP INSTRUCTIONS:
1. Host the 'checkin_final.html' file on a web server
2. Update the URL in the QR code to point to your hosted file
3. Print the QR code and place at check-in stations
4. Ensure good Wi-Fi connectivity for participants

HOW IT WORKS:
- Participants scan QR code with their phone
- They type their name and see autocomplete suggestions
- They confirm their identity and check in
- System shows their table and discussion assignments
- Check-in status is saved on their device

STAFF FEATURES:
- Real-time check-in counter
- Prevents duplicate check-ins
- Works offline after initial load
- Mobile-friendly design

TROUBLESHOOTING:
- If someone can't find their name, check spelling
- Names are from the badge assignments CSV file
- System works on any modern smartphone browser
- For technical issues, refresh the page

For questions, contact the tech team.
"""
    
    with open('../../output/checkin_instructions.txt', 'w') as f:
        f.write(instructions)
    
    print("Created '../../output/checkin_instructions.txt'")

if __name__ == "__main__":
    # GitHub Pages URLs
    checkin_url = "https://nahom8423.github.io/campusministry/"
    admin_url = "https://nahom8423.github.io/campusministry/admin.html"
    
    print(f"Creating check-in QR code for: {checkin_url}")
    create_checkin_qr_code(checkin_url)
    
    print(f"Creating admin QR code for: {admin_url}")
    create_admin_qr_code(admin_url)
    
    create_instruction_sheet()
    
    print(f"\nFiles created:")
    print(f"- ../../docs/assets/github_checkin_qr.png (decorated QR code for check-in)")
    print(f"- ../../docs/assets/github_checkin_qr_simple.png (simple QR code for check-in)")
    print(f"- ../../docs/assets/github_admin_qr.png (decorated QR code for admin)")
    print(f"- ../../docs/assets/github_admin_qr_simple.png (simple QR code for admin)")
    print(f"- ../../output/checkin_instructions.txt (setup guide)")
    print(f"\nThese QR codes point to your live GitHub Pages site!")
    print(f"Check-in URL: {checkin_url}")
    print(f"Admin URL: {admin_url}")