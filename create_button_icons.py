#!/usr/bin/env python3
"""Create button icons for the toolbar."""

from PIL import Image, ImageDraw
import os

def create_button_icon(size=48):
    """Create transparent icon with specific size."""
    return Image.new('RGBA', (size, size), (0, 0, 0, 0))

# Scan Folder Icon - Simple Magnifier
img = create_button_icon()
draw = ImageDraw.Draw(img)

# Draw magnifying glass
magnifier_x, magnifier_y = 24, 24
magnifier_color = (255, 120, 0)
# Glass circle
draw.ellipse([(magnifier_x-10, magnifier_y-10), (magnifier_x+10, magnifier_y+10)], outline=magnifier_color, width=3)
# Handle
draw.line([(magnifier_x+8, magnifier_y+8), (magnifier_x+16, magnifier_y+16)], fill=magnifier_color, width=3)

img.resize((64, 64), Image.Resampling.LANCZOS).save('src/icons/btn_scan_folder.png')
print("✓ Created scan_folder icon (magnifier)")

# Reload/Refresh Icon (for menu)
img = create_button_icon()
draw = ImageDraw.Draw(img)

# Draw circular arrows (refresh/reload symbol)
arc_color = (100, 180, 100)
# Top right arc
draw.arc([(12, 12), (36, 36)], 0, 180, fill=arc_color, width=3)
# Arrow head
draw.polygon([(32, 14), (38, 12), (35, 18)], fill=arc_color)
# Bottom left arc
draw.arc([(12, 12), (36, 36)], 180, 360, fill=arc_color, width=3)
# Arrow head
draw.polygon([(16, 34), (10, 36), (13, 30)], fill=arc_color)

img.resize((64, 64), Image.Resampling.LANCZOS).save('src/icons/btn_reload.png')
print("✓ Created reload icon")

# Batch Convert Icon (for menu)
img = create_button_icon()
draw = ImageDraw.Draw(img)

# Draw multiple files/layers
file_color = (70, 140, 200)
# File 1
draw.rectangle([(12, 20), (28, 34)], fill=file_color, outline=(40, 100, 160), width=1)
draw.line([(16, 24), (24, 24)], fill=(40, 100, 160), width=1)
draw.line([(16, 28), (24, 28)], fill=(40, 100, 160), width=1)

# File 2 (offset)
draw.rectangle([(18, 18), (34, 32)], fill=file_color, outline=(40, 100, 160), width=1)
draw.line([(22, 22), (30, 22)], fill=(40, 100, 160), width=1)
draw.line([(22, 26), (30, 26)], fill=(40, 100, 160), width=1)

# File 3 (offset)
draw.rectangle([(24, 16), (40, 30)], fill=file_color, outline=(40, 100, 160), width=1)
draw.line([(28, 20), (36, 20)], fill=(40, 100, 160), width=1)
draw.line([(28, 24), (36, 24)], fill=(40, 100, 160), width=1)

# Green checkmark overlay
check_x, check_y = 36, 36
check_size = 6
draw.line([(check_x-4, check_y), (check_x-1, check_y+3)], fill=(76, 175, 80), width=2)
draw.line([(check_x-1, check_y+3), (check_x+3, check_y-2)], fill=(76, 175, 80), width=2)

img.resize((96, 96), Image.Resampling.LANCZOS).save('src/icons/btn_batch_convert.png')
print("✓ Created batch_convert icon")

print("\n✅ All button icons created successfully!")

# Create cow patch background image
def create_cow_patch_background(width=1000, height=700):
    """Create a brown and white cow patch pattern background."""
    # Start with white background
    cow_bg = Image.new('RGB', (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(cow_bg)
    
    # Brown cow patch color
    brown = (101, 67, 33)  # Dark brown
    
    # Create irregular cow patches
    import random
    random.seed(42)  # For consistent patterns
    
    patches = [
        # Large patches
        {'bbox': [(50, 100), (250, 300)], 'shape': 'ellipse'},
        {'bbox': [(600, 50), (850, 200)], 'shape': 'ellipse'},
        {'bbox': [(100, 400), (350, 600)], 'shape': 'polygon'},
        {'bbox': [(700, 300), (950, 500)], 'shape': 'polygon'},
        {'bbox': [(350, 150), (500, 350)], 'shape': 'ellipse'},
        {'bbox': [(150, 550), (300, 650)], 'shape': 'polygon'},
    ]
    
    for patch in patches:
        bbox = patch['bbox']
        if patch['shape'] == 'ellipse':
            draw.ellipse(bbox, fill=brown)
        else:
            # Irregular polygon
            x1, y1 = bbox[0]
            x2, y2 = bbox[1]
            points = [
                (x1, y1),
                (x1 + (x2-x1)//3, y1),
                (x2, y1 + (y2-y1)//4),
                (x2, y2),
                (x1 + (x2-x1)//2, y2),
                (x1, y1 + (y2-y1)//2)
            ]
            draw.polygon(points, fill=brown)
    
    cow_bg.save('src/icons/cow_patch_bg.png')
    print("✓ Created cow patch background")

create_cow_patch_background()

