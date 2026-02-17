#!/usr/bin/env python3
"""Create application icon for Moovy."""

from PIL import Image, ImageDraw
import os

def create_icon(size=256):
    """Create application icon."""
    # Create a new image with gradient background
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Background: Modern gradient-like color (deep blue/purple)
    bg_color = (30, 90, 150)  # Professional blue
    
    # Draw rounded rectangle background
    margin = 5
    draw.rectangle(
        [(margin, margin), (size - margin, size - margin)],
        fill=bg_color,
        outline=(60, 140, 200)
    )
    
    # Draw film reel circles (left and right)
    reel_radius = size // 6
    center_y = size // 2
    
    # Left reel
    left_reel_x = size // 5
    draw.ellipse(
        [(left_reel_x - reel_radius, center_y - reel_radius),
         (left_reel_x + reel_radius, center_y + reel_radius)],
        fill=(100, 160, 220),
        outline=(200, 220, 255),
        width=2
    )
    
    # Add spokes to left reel
    spoke_count = 6
    for i in range(spoke_count):
        angle = (360 / spoke_count) * i
        import math
        rad = math.radians(angle)
        x_end = left_reel_x + reel_radius * 0.7 * math.cos(rad)
        y_end = center_y + reel_radius * 0.7 * math.sin(rad)
        draw.line([(left_reel_x, center_y), (x_end, y_end)], fill=(200, 220, 255), width=2)
    
    # Right reel
    right_reel_x = int(size * 0.8)
    draw.ellipse(
        [(right_reel_x - reel_radius, center_y - reel_radius),
         (right_reel_x + reel_radius, center_y + reel_radius)],
        fill=(100, 160, 220),
        outline=(200, 220, 255),
        width=2
    )
    
    # Add spokes to right reel
    for i in range(spoke_count):
        angle = (360 / spoke_count) * i
        import math
        rad = math.radians(angle)
        x_end = right_reel_x + reel_radius * 0.7 * math.cos(rad)
        y_end = center_y + reel_radius * 0.7 * math.sin(rad)
        draw.line([(right_reel_x, center_y), (x_end, y_end)], fill=(200, 220, 255), width=2)
    
    # Draw film strip between reels
    strip_y = center_y
    strip_width = int(size * 0.35)
    strip_x_start = left_reel_x + reel_radius + 5
    strip_x_end = right_reel_x - reel_radius - 5
    
    # Film frames
    frame_width = 15
    frame_height = 25
    frame_spacing = 3
    
    x = strip_x_start
    while x < strip_x_end:
        draw.rectangle(
            [(x, strip_y - frame_height // 2),
             (x + frame_width, strip_y + frame_height // 2)],
            fill=(0, 0, 0),
            outline=(200, 220, 255),
            width=1
        )
        x += frame_width + frame_spacing
    
    # Draw play button overlay (center)
    play_size = size // 3
    play_x = size // 2
    play_y = size // 2
    
    # Play button background circle
    play_circle_radius = play_size // 2
    draw.ellipse(
        [(play_x - play_circle_radius, play_y - play_circle_radius),
         (play_x + play_circle_radius, play_y + play_circle_radius)],
        fill=(76, 175, 80),  # Green for compatibility
        outline=(255, 255, 255),
        width=2
    )
    
    # Draw play triangle (white)
    triangle_size = play_circle_radius // 2
    play_triangle = [
        (play_x - triangle_size // 2, play_y - triangle_size),
        (play_x - triangle_size // 2, play_y + triangle_size),
        (play_x + triangle_size, play_y)
    ]
    draw.polygon(play_triangle, fill=(255, 255, 255))
    
    # Draw checkmark overlay
    check_size = play_circle_radius // 3
    check_x = play_x + play_circle_radius - check_size
    check_y = play_y - play_circle_radius + check_size
    
    # Checkmark (white)
    check_start_x = check_x - check_size // 3
    check_start_y = check_y
    check_mid_x = check_x - check_size // 6
    check_mid_y = check_y + check_size // 3
    check_end_x = check_x + check_size // 2
    check_end_y = check_y - check_size // 4
    
    draw.line([(check_start_x, check_start_y), (check_mid_x, check_mid_y)], 
              fill=(255, 255, 255), width=2)
    draw.line([(check_mid_x, check_mid_y), (check_end_x, check_end_y)], 
              fill=(255, 255, 255), width=2)
    
    return img

# Create icons of different sizes
print("Creating application icons...")

# 256x256 PNG
icon_256 = create_icon(256)
icon_256.save('src/icons/icon_256.png')
print("✓ Created src/icons/icon_256.png (256x256)")

# 128x128 PNG
icon_128 = icon_256.resize((128, 128), Image.Resampling.LANCZOS)
icon_128.save('src/icons/icon_128.png')
print("✓ Created src/icons/icon_128.png (128x128)")

# 64x64 PNG
icon_64 = icon_256.resize((64, 64), Image.Resampling.LANCZOS)
icon_64.save('src/icons/icon_64.png')
print("✓ Created src/icons/icon_64.png (64x64)")

# 32x32 PNG
icon_32 = icon_256.resize((32, 32), Image.Resampling.LANCZOS)
icon_32.save('src/icons/icon_32.png')
print("✓ Created src/icons/icon_32.png (32x32)")

# Create Windows ICO file
print("✓ Creating Windows icon (icon.ico)...")
icon_256.save('src/icons/icon.ico', sizes=[(256, 256), (128, 128), (64, 64), (32, 32)])
print("✓ Created src/icons/icon.ico")

print("\n✅ All icons created successfully!")
