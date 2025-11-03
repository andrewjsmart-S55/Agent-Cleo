"""
Create an X.com (Twitter) Profile Image for DecideWright
Profile image dimensions: 400 x 400 pixels (displays as circle)
"""

from PIL import Image, ImageDraw
import os

# Paths
marketing_dir = r"C:\Users\AndrewSmart\DecideWright Ltd\Marketing - General"
logo_path = os.path.join(marketing_dir, r"Logos\DecideWright_logo_files-2\Logo\PNG\DecideWright_logo.png")
logo_white_path = os.path.join(marketing_dir, r"Logos\DecideWright_logo_files-2\Logo\PNG\DecideWright_logo_white.png")
output_path = r"C:\Users\AndrewSmart\Claude_Projects\AAgents\DecideWright-EA\Output\DecideWright_X_Profile.png"

# X profile image dimensions
PROFILE_SIZE = 400

# Create a background with DecideWright brand colors
# Using the blue from the logo
background = Image.new('RGB', (PROFILE_SIZE, PROFILE_SIZE), (25, 68, 141))  # DecideWright blue

# Load logo
logo = Image.open(logo_white_path)

# Calculate logo size (make it fit nicely within the circular crop)
# Leave some padding so it doesn't get cut off when displayed as circle
padding_factor = 0.75  # Use 75% of the available space
logo_size = int(PROFILE_SIZE * padding_factor)
aspect_ratio = logo.height / logo.width
logo_height = int(logo_size * aspect_ratio)
logo = logo.resize((logo_size, logo_height), Image.Resampling.LANCZOS)

# Position logo in center
logo_x = (PROFILE_SIZE - logo_size) // 2
logo_y = (PROFILE_SIZE - logo_height) // 2

# Convert background to RGBA for transparency support
if background.mode != 'RGBA':
    background = background.convert('RGBA')

# Paste logo with transparency
if logo.mode == 'RGBA':
    background.paste(logo, (logo_x, logo_y), logo)
else:
    background.paste(logo, (logo_x, logo_y))

# Convert back to RGB for final save
final_image = Image.new('RGB', background.size, (255, 255, 255))
if background.mode == 'RGBA':
    final_image.paste(background, mask=background.split()[3] if len(background.split()) == 4 else None)
else:
    final_image = background

# Save the profile image
final_image.save(output_path, quality=95, optimize=True)
print(f"X.com profile image created successfully!")
print(f"Saved to: {output_path}")
print(f"Dimensions: {PROFILE_SIZE} x {PROFILE_SIZE} pixels")
print(f"Note: Image will display as a circle on X.com")
