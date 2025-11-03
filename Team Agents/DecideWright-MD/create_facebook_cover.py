"""
Create a Facebook Cover Photo for DecideWright
Facebook cover dimensions: 1640 x 624 pixels (high resolution)
"""

from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageFilter
import os

# Paths
marketing_dir = r"C:\Users\AndrewSmart\DecideWright Ltd\Marketing - General"
logo_path = os.path.join(marketing_dir, r"Logos\DecideWright_logo_files-2\Logo\PNG\DecideWright_logo.png")
logo_white_path = os.path.join(marketing_dir, r"Logos\DecideWright_logo_files-2\Logo\PNG\DecideWright_logo_white.png")
background_path = os.path.join(marketing_dir, r"Brand\Images\Decidewright city.jpg")
output_path = r"C:\Users\AndrewSmart\Claude_Projects\AAgents\DecideWright-EA\Output\DecideWright_Facebook_Cover_02.png"

# Facebook cover dimensions
COVER_WIDTH = 1640
COVER_HEIGHT = 624

# Load and prepare background
background = Image.open(background_path)
background = background.resize((COVER_WIDTH, COVER_HEIGHT), Image.Resampling.LANCZOS)

# Apply blur to make text more readable
background = background.filter(ImageFilter.GaussianBlur(radius=3))

# Optional: Slightly darken the background for better logo visibility
# Cityscape is already dark, so keep it as is or slightly lighten
enhancer = ImageEnhance.Brightness(background)
background = enhancer.enhance(0.9)  # Keep mostly original

# Load logo (use white logo for dark cityscape background)
logo = Image.open(logo_white_path)

# Calculate logo size (make it prominent but not too large)
# Let's make the logo about 50% of the width
logo_width = int(COVER_WIDTH * 0.5)
aspect_ratio = logo.height / logo.width
logo_height = int(logo_width * aspect_ratio)
logo = logo.resize((logo_width, logo_height), Image.Resampling.LANCZOS)

# Position logo in center
logo_x = (COVER_WIDTH - logo_width) // 2
logo_y = (COVER_HEIGHT - logo_height) // 2

# Create the final image
cover = background.copy()

# Paste logo directly on the cityscape (white logo on dark background)
if logo.mode == 'RGBA':
    # Convert cover to RGBA if needed for transparency
    if cover.mode != 'RGBA':
        cover = cover.convert('RGBA')

    # Paste logo with transparency
    cover.paste(logo, (logo_x, logo_y), logo)
else:
    cover.paste(logo, (logo_x, logo_y))

# Add tagline "CLARITY IN UNCERTAINTY"
tagline = "CLARITY IN UNCERTAINTY"
draw = ImageDraw.Draw(cover)

# Try to use a nice font, fallback to default if not available
try:
    # Try common Windows fonts
    font_size = 36
    font = ImageFont.truetype("arial.ttf", font_size)
    # Smaller font for contact info
    contact_font_size = 20
    contact_font = ImageFont.truetype("arial.ttf", contact_font_size)
except:
    try:
        font = ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", font_size)
        contact_font = ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", contact_font_size)
    except:
        # Fallback to default font
        font = ImageFont.load_default()
        contact_font = ImageFont.load_default()

# Get text bounding box for positioning
bbox = draw.textbbox((0, 0), tagline, font=font)
text_width = bbox[2] - bbox[0]
text_height = bbox[3] - bbox[1]

# Position tagline below the logo, centered
text_x = (COVER_WIDTH - text_width) // 2
text_y = logo_y + logo_height + 30  # 30px below the logo

# Draw tagline with subtle white color
text_color = (255, 255, 255, 200)  # White with slight transparency
draw.text((text_x, text_y), tagline, font=font, fill=text_color)

# Add contact information at the bottom
contact_info = "www.decidewright.com  |  info@decidewright.com"
contact_bbox = draw.textbbox((0, 0), contact_info, font=contact_font)
contact_width = contact_bbox[2] - contact_bbox[0]

# Position contact info at the bottom, centered, with 20px margin from bottom
contact_x = (COVER_WIDTH - contact_width) // 2
contact_y = COVER_HEIGHT - 50  # 50px from bottom

# Draw contact info
draw.text((contact_x, contact_y), contact_info, font=contact_font, fill=text_color)

# Convert back to RGB for saving as JPG (or keep as PNG)
if cover.mode == 'RGBA':
    # Create white background
    final_cover = Image.new('RGB', cover.size, (255, 255, 255))
    final_cover.paste(cover, mask=cover.split()[3] if len(cover.split()) == 4 else None)
    cover = final_cover

# Save the cover photo
cover.save(output_path, quality=95, optimize=True)
print(f"Facebook cover photo created successfully!")
print(f"Saved to: {output_path}")
print(f"Dimensions: {COVER_WIDTH} x {COVER_HEIGHT} pixels")
