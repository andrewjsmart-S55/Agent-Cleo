"""
Create Business Execution Canvas Framework
"""

from PIL import Image, ImageDraw, ImageFont
import os

# Canvas dimensions
CANVAS_WIDTH = 2000
CANVAS_HEIGHT = 800

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (230, 230, 230)
LINE_COLOR = (0, 0, 0)

# Create image
canvas = Image.new('RGB', (CANVAS_WIDTH, CANVAS_HEIGHT), WHITE)
draw = ImageDraw.Draw(canvas)

# Try to load fonts
try:
    title_font = ImageFont.truetype("arialbd.ttf", 20)
    header_font = ImageFont.truetype("arialbd.ttf", 16)
    text_font = ImageFont.truetype("arial.ttf", 14)
except:
    try:
        title_font = ImageFont.truetype("C:\\Windows\\Fonts\\arialbd.ttf", 20)
        header_font = ImageFont.truetype("C:\\Windows\\Fonts\\arialbd.ttf", 16)
        text_font = ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", 14)
    except:
        title_font = ImageFont.load_default()
        header_font = ImageFont.load_default()
        text_font = ImageFont.load_default()

# Layout parameters
margin = 20
top_section_height = 480
bottom_section_height = CANVAS_HEIGHT - top_section_height - margin

# Main column widths for top section
enablers_width = 600
execution_width = 800
value_width = CANVAS_WIDTH - enablers_width - execution_width

# Draw main sections outline
line_width = 2

# Top section - Main headers
# ENABLERS section
draw.rectangle([0, 0, enablers_width, 50], fill=GRAY, outline=LINE_COLOR, width=line_width)
draw.text((enablers_width//2, 25), "ENABLERS", fill=BLACK, font=title_font, anchor="mm")

# EXECUTION section
draw.rectangle([enablers_width, 0, enablers_width + execution_width, 50], fill=GRAY, outline=LINE_COLOR, width=line_width)
draw.text((enablers_width + execution_width//2, 25), "EXECUTION", fill=BLACK, font=title_font, anchor="mm")

# VALUE section
draw.rectangle([enablers_width + execution_width, 0, CANVAS_WIDTH, 50], fill=GRAY, outline=LINE_COLOR, width=line_width)
draw.text((enablers_width + execution_width + value_width//2, 25), "VALUE", fill=BLACK, font=title_font, anchor="mm")

# ENABLERS sub-columns
enablers_sub_width = enablers_width // 3
# BRAND
draw.rectangle([0, 50, enablers_sub_width, 100], outline=LINE_COLOR, width=line_width)
draw.text((enablers_sub_width//2, 75), "BRAND", fill=BLACK, font=header_font, anchor="mm")

# CULTURE
draw.rectangle([enablers_sub_width, 50, enablers_sub_width*2, 100], outline=LINE_COLOR, width=line_width)
draw.text((enablers_sub_width + enablers_sub_width//2, 75), "CULTURE", fill=BLACK, font=header_font, anchor="mm")

# TECHNOLOGY
draw.rectangle([enablers_sub_width*2, 50, enablers_width, 100], outline=LINE_COLOR, width=line_width)
draw.text((enablers_sub_width*2 + enablers_sub_width//2, 75), "TECHNOLOGY", fill=BLACK, font=header_font, anchor="mm")

# Large empty areas under BRAND, CULTURE, TECHNOLOGY
draw.rectangle([0, 100, enablers_sub_width, 240], outline=LINE_COLOR, width=line_width)
draw.rectangle([enablers_sub_width, 100, enablers_sub_width*2, 240], outline=LINE_COLOR, width=line_width)
draw.rectangle([enablers_sub_width*2, 100, enablers_width, 240], outline=LINE_COLOR, width=line_width)

# PEOPLE and THIRD PARTIES
draw.rectangle([0, 240, enablers_sub_width, 290], outline=LINE_COLOR, width=line_width)
draw.text((enablers_sub_width//2, 265), "PEOPLE", fill=BLACK, font=header_font, anchor="mm")

draw.rectangle([enablers_sub_width, 240, enablers_sub_width*2, 290], outline=LINE_COLOR, width=line_width)
draw.text((enablers_sub_width + enablers_sub_width//2, 265), "THIRD PARTIES", fill=BLACK, font=header_font, anchor="mm")

# Empty space next to PEOPLE and THIRD PARTIES
draw.rectangle([enablers_sub_width*2, 240, enablers_width, 290], outline=LINE_COLOR, width=line_width)

# Large empty areas at the bottom of enablers
draw.rectangle([0, 290, enablers_sub_width, top_section_height], outline=LINE_COLOR, width=line_width)
draw.rectangle([enablers_sub_width, 290, enablers_sub_width*2, top_section_height], outline=LINE_COLOR, width=line_width)
draw.rectangle([enablers_sub_width*2, 290, enablers_width, top_section_height], outline=LINE_COLOR, width=line_width)

# EXECUTION section - PROCESSES and PRODUCTS & SERVICES
execution_sub_width = execution_width // 2

# PROCESSES column
draw.rectangle([enablers_width, 50, enablers_width + execution_sub_width, 100], outline=LINE_COLOR, width=line_width)
draw.text((enablers_width + execution_sub_width//2, 75), "PROCESSES", fill=BLACK, font=header_font, anchor="mm")

# PRODUCTS & SERVICES column
draw.rectangle([enablers_width + execution_sub_width, 50, enablers_width + execution_width, 100], outline=LINE_COLOR, width=line_width)
draw.text((enablers_width + execution_sub_width + execution_sub_width//2, 75), "PRODUCTS & SERVICES", fill=BLACK, font=header_font, anchor="mm")

# Empty space in PRODUCTS & SERVICES
draw.rectangle([enablers_width + execution_sub_width, 100, enablers_width + execution_width, top_section_height], outline=LINE_COLOR, width=line_width)

# PROCESSES sub-sections: CHANGE, INNOVATION
draw.rectangle([enablers_width, 100, enablers_width + execution_sub_width, 190], outline=LINE_COLOR, width=line_width)

draw.rectangle([enablers_width, 190, enablers_width + execution_sub_width, 240], outline=LINE_COLOR, width=line_width)
draw.text((enablers_width + execution_sub_width//2, 215), "CHANGE", fill=BLACK, font=header_font, anchor="mm")

draw.rectangle([enablers_width, 240, enablers_width + execution_sub_width, 290], outline=LINE_COLOR, width=line_width)

draw.rectangle([enablers_width, 290, enablers_width + execution_sub_width, 340], outline=LINE_COLOR, width=line_width)
draw.text((enablers_width + execution_sub_width//2, 315), "INNOVATION", fill=BLACK, font=header_font, anchor="mm")

draw.rectangle([enablers_width, 340, enablers_width + execution_sub_width, top_section_height], outline=LINE_COLOR, width=line_width)

# VALUE section - ANNUAL RESULTS, STRATEGIC GOALS, REPUTATION
value_sub_width = value_width // 3

# ANNUAL RESULTS
draw.rectangle([enablers_width + execution_width, 50, enablers_width + execution_width + value_sub_width, 100], outline=LINE_COLOR, width=line_width)
draw.text((enablers_width + execution_width + value_sub_width//2, 75), "ANNUAL RESULTS", fill=BLACK, font=header_font, anchor="mm")

# STRATEGIC GOALS
draw.rectangle([enablers_width + execution_width + value_sub_width, 50, enablers_width + execution_width + value_sub_width*2, 100], outline=LINE_COLOR, width=line_width)
draw.text((enablers_width + execution_width + value_sub_width + value_sub_width//2, 75), "STRATEGIC GOALS", fill=BLACK, font=header_font, anchor="mm")

# REPUTATION
draw.rectangle([enablers_width + execution_width + value_sub_width*2, 50, CANVAS_WIDTH, 100], outline=LINE_COLOR, width=line_width)
draw.text((enablers_width + execution_width + value_sub_width*2 + value_sub_width//2, 75), "REPUTATION", fill=BLACK, font=header_font, anchor="mm")

# Empty spaces under VALUE columns
draw.rectangle([enablers_width + execution_width, 100, enablers_width + execution_width + value_sub_width, top_section_height], outline=LINE_COLOR, width=line_width)
draw.rectangle([enablers_width + execution_width + value_sub_width, 100, enablers_width + execution_width + value_sub_width*2, top_section_height], outline=LINE_COLOR, width=line_width)
draw.rectangle([enablers_width + execution_width + value_sub_width*2, 100, CANVAS_WIDTH, top_section_height], outline=LINE_COLOR, width=line_width)

# Bottom section - ECONOMICS
economics_y = top_section_height + 20
draw.rectangle([0, economics_y, CANVAS_WIDTH, economics_y + 50], fill=GRAY, outline=LINE_COLOR, width=line_width)
draw.text((CANVAS_WIDTH//2, economics_y + 25), "ECONOMICS", fill=BLACK, font=title_font, anchor="mm")

# ECONOMICS sub-sections
economics_sub_width = CANVAS_WIDTH // 4

# FINANCIALS
draw.rectangle([0, economics_y + 50, economics_sub_width, economics_y + 100], outline=LINE_COLOR, width=line_width)
draw.text((economics_sub_width//2, economics_y + 75), "FINANCIALS", fill=BLACK, font=header_font, anchor="mm")

# BUSINESS MODEL
draw.rectangle([economics_sub_width, economics_y + 50, economics_sub_width*2, economics_y + 100], outline=LINE_COLOR, width=line_width)
draw.text((economics_sub_width + economics_sub_width//2, economics_y + 75), "BUSINESS MODEL", fill=BLACK, font=header_font, anchor="mm")

# EXTERNAL ENVIRONMENT
draw.rectangle([economics_sub_width*2, economics_y + 50, economics_sub_width*3, economics_y + 100], outline=LINE_COLOR, width=line_width)
draw.text((economics_sub_width*2 + economics_sub_width//2, economics_y + 75), "EXTERNAL ENVIRONMENT", fill=BLACK, font=header_font, anchor="mm")

# GOVERNANCE
draw.rectangle([economics_sub_width*3, economics_y + 50, CANVAS_WIDTH, economics_y + 100], outline=LINE_COLOR, width=line_width)
draw.text((economics_sub_width*3 + economics_sub_width//2, economics_y + 75), "GOVERNANCE", fill=BLACK, font=header_font, anchor="mm")

# Empty spaces under ECONOMICS columns
draw.rectangle([0, economics_y + 100, economics_sub_width, CANVAS_HEIGHT], outline=LINE_COLOR, width=line_width)
draw.rectangle([economics_sub_width, economics_y + 100, economics_sub_width*2, CANVAS_HEIGHT], outline=LINE_COLOR, width=line_width)
draw.rectangle([economics_sub_width*2, economics_y + 100, economics_sub_width*3, CANVAS_HEIGHT], outline=LINE_COLOR, width=line_width)
draw.rectangle([economics_sub_width*3, economics_y + 100, CANVAS_WIDTH, CANVAS_HEIGHT], outline=LINE_COLOR, width=line_width)

# Save the canvas
output_path = r"C:\Users\AndrewSmart\Claude_Projects\AAgents\DecideWright-EA\Output\Business_Execution_Canvas.png"
canvas.save(output_path, quality=95, optimize=True)
print(f"Business Execution Canvas created successfully!")
print(f"Saved to: {output_path}")
print(f"Dimensions: {CANVAS_WIDTH} x {CANVAS_HEIGHT} pixels")
