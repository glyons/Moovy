#!/usr/bin/env python3
"""Create a cow-themed application icon for Moovy."""

from PIL import Image, ImageDraw
import math

def create_cow_icon(size=256):
    """Create a cute cow icon."""
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Background circle (light blue)
    bg_color = (230, 242, 255)
    draw.ellipse([(5, 5), (size-5, size-5)], fill=bg_color, outline=(100, 150, 200), width=2)
    
    # Cow body (white)
    body_x = size // 2
    body_y = size * 0.55
    body_width = size * 0.4
    body_height = size * 0.35
    
    draw.ellipse(
        [(body_x - body_width/2, body_y - body_height/2),
         (body_x + body_width/2, body_y + body_height/2)],
        fill=(255, 255, 255),
        outline=(200, 200, 200),
        width=2
    )
    
    # Cow head (white)
    head_x = size // 2
    head_y = size * 0.25
    head_size = size * 0.25
    
    draw.ellipse(
        [(head_x - head_size, head_y - head_size),
         (head_x + head_size, head_y + head_size)],
        fill=(255, 255, 255),
        outline=(200, 200, 200),
        width=2
    )
    
    # Left ear
    ear_size = size * 0.08
    ear_x_left = head_x - head_size + size * 0.04
    ear_y = head_y - head_size - size * 0.03
    
    draw.ellipse(
        [(ear_x_left - ear_size, ear_y - ear_size * 1.2),
         (ear_x_left + ear_size, ear_y + ear_size * 0.8)],
        fill=(255, 200, 200),
        outline=(200, 150, 150),
        width=1
    )
    
    # Right ear
    ear_x_right = head_x + head_size - size * 0.04
    draw.ellipse(
        [(ear_x_right - ear_size, ear_y - ear_size * 1.2),
         (ear_x_right + ear_size, ear_y + ear_size * 0.8)],
        fill=(255, 200, 200),
        outline=(200, 150, 150),
        width=1
    )
    
    # Left horn
    horn_size = size * 0.05
    draw.arc(
        [(ear_x_left - horn_size * 1.5, ear_y - horn_size * 2.5),
         (ear_x_left + horn_size * 0.5, ear_y - horn_size * 0.5)],
        0, 90,
        fill=(100, 80, 60),
        width=2
    )
    
    # Right horn
    draw.arc(
        [(ear_x_right - horn_size * 0.5, ear_y - horn_size * 2.5),
         (ear_x_right + horn_size * 1.5, ear_y - horn_size * 0.5)],
        90, 180,
        fill=(100, 80, 60),
        width=2
    )
    
    # Left eye
    eye_x_left = head_x - head_size * 0.4
    eye_y = head_y - head_size * 0.2
    eye_size = size * 0.04
    
    draw.ellipse(
        [(eye_x_left - eye_size, eye_y - eye_size),
         (eye_x_left + eye_size, eye_y + eye_size)],
        fill=(0, 0, 0)
    )
    
    # Left pupil shine
    draw.ellipse(
        [(eye_x_left - eye_size * 0.3, eye_y - eye_size * 0.3),
         (eye_x_left + eye_size * 0.3, eye_y + eye_size * 0.3)],
        fill=(255, 255, 255)
    )
    
    # Right eye
    eye_x_right = head_x + head_size * 0.4
    draw.ellipse(
        [(eye_x_right - eye_size, eye_y - eye_size),
         (eye_x_right + eye_size, eye_y + eye_size)],
        fill=(0, 0, 0)
    )
    
    # Right pupil shine
    draw.ellipse(
        [(eye_x_right - eye_size * 0.3, eye_y - eye_size * 0.3),
         (eye_x_right + eye_size * 0.3, eye_y + eye_size * 0.3)],
        fill=(255, 255, 255)
    )
    
    # Snout (pink)
    snout_size = size * 0.08
    draw.ellipse(
        [(head_x - snout_size, head_y + head_size * 0.3),
         (head_x + snout_size, head_y + head_size * 0.6)],
        fill=(255, 200, 200),
        outline=(200, 150, 150),
        width=1
    )
    
    # Nose (black)
    nose_size = size * 0.04
    draw.ellipse(
        [(head_x - nose_size * 1.5, head_y + head_size * 0.4),
         (head_x - nose_size * 0.5, head_y + head_size * 0.55)],
        fill=(0, 0, 0)
    )
    draw.ellipse(
        [(head_x + nose_size * 0.5, head_y + head_size * 0.4),
         (head_x + nose_size * 1.5, head_y + head_size * 0.55)],
        fill=(0, 0, 0)
    )
    
    # Smile
    mouth_y = head_y + head_size * 0.75
    draw.arc(
        [(head_x - snout_size * 0.8, mouth_y),
         (head_x + snout_size * 0.8, mouth_y + snout_size * 0.6)],
        0, 180,
        fill=(0, 0, 0),
        width=1
    )
    
    # Spots on body (brown patches)
    # Left spot
    spot_x_left = body_x - body_width * 0.25
    spot_y_top = body_y - body_height * 0.2
    spot_size = size * 0.08
    
    draw.ellipse(
        [(spot_x_left - spot_size, spot_y_top - spot_size),
         (spot_x_left + spot_size, spot_y_top + spot_size)],
        fill=(100, 50, 50),
        outline=(80, 30, 30),
        width=1
    )
    
    # Right spot
    spot_x_right = body_x + body_width * 0.25
    draw.ellipse(
        [(spot_x_right - spot_size, spot_y_top - spot_size),
         (spot_x_right + spot_size, spot_y_top + spot_size)],
        fill=(100, 50, 50),
        outline=(80, 30, 30),
        width=1
    )
    
    # Udder (pink)
    udder_x = body_x
    udder_y = body_y + body_height * 0.35
    udder_size = size * 0.06
    
    # Udder rear quarters
    draw.ellipse(
        [(udder_x - udder_size * 1.5, udder_y - udder_size),
         (udder_x - udder_size * 0.5, udder_y + udder_size)],
        fill=(255, 150, 180),
        outline=(200, 100, 150),
        width=1
    )
    
    draw.ellipse(
        [(udder_x + udder_size * 0.5, udder_y - udder_size),
         (udder_x + udder_size * 1.5, udder_y + udder_size)],
        fill=(255, 150, 180),
        outline=(200, 100, 150),
        width=1
    )
    
    # Tail
    tail_start_x = body_x + body_width * 0.45
    tail_start_y = body_y + body_height * 0.15
    tail_end_x = tail_start_x + size * 0.1
    tail_end_y = tail_start_y - size * 0.15
    
    draw.line(
        [(tail_start_x, tail_start_y), (tail_end_x, tail_end_y)],
        fill=(100, 100, 100),
        width=3
    )
    
    # Add a heart next to the cow (representing videos/media)
    heart_x = size * 0.85
    heart_y = size * 0.2
    heart_size = size * 0.06
    
    # Heart shape
    draw.ellipse(
        [(heart_x - heart_size * 1.2, heart_y - heart_size),
         (heart_x - heart_size * 0.2, heart_y)],
        fill=(255, 100, 100)
    )
    draw.ellipse(
        [(heart_x + heart_size * 0.2, heart_y - heart_size),
         (heart_x + heart_size * 1.2, heart_y)],
        fill=(255, 100, 100)
    )
    draw.polygon(
        [(heart_x - heart_size * 0.8, heart_y + heart_size * 0.3),
         (heart_x, heart_y + heart_size * 1.2),
         (heart_x + heart_size * 0.8, heart_y + heart_size * 0.3)],
        fill=(255, 100, 100)
    )
    
    return img

# Create cow icon
print("Creating cow icon...")
icon_256 = create_cow_icon(256)
icon_256.save('src/icons/icon_256.png')
print("✓ Created src/icons/icon_256.png (256x256)")

# Create smaller sizes
icon_128 = icon_256.resize((128, 128), Image.Resampling.LANCZOS)
icon_128.save('src/icons/icon_128.png')
print("✓ Created src/icons/icon_128.png (128x128)")

icon_64 = icon_256.resize((64, 64), Image.Resampling.LANCZOS)
icon_64.save('src/icons/icon_64.png')
print("✓ Created src/icons/icon_64.png (64x64)")

icon_32 = icon_256.resize((32, 32), Image.Resampling.LANCZOS)
icon_32.save('src/icons/icon_32.png')
print("✓ Created src/icons/icon_32.png (32x32)")

# Create Windows ICO file
icon_256.save('src/icons/icon.ico', sizes=[(256, 256), (128, 128), (64, 64), (32, 32)])
print("✓ Created src/icons/icon.ico")

print("\n✅ Cow icon created successfully!")
