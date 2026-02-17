#!/bin/bash
# Build standalone macOS application and create DMG

echo ""
echo "===================================================="
echo "Building Moovy - macOS Standalone Application"
echo "===================================================="
echo ""

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Error: Virtual environment not found!"
    echo "Please run: ./run.sh first"
    exit 1
fi

# Activate virtual environment
source .venv/bin/activate

echo "Cleaning previous builds..."
rm -rf build dist *.spec

echo ""
echo "Building macOS application bundle..."
echo "This may take a few minutes..."
echo ""

# Build using PyInstaller for macOS
python -m PyInstaller \
    --name Moovy \
    --icon=src/icons/icon.ico \
    --add-data "src/icons:src/icons" \
    --windowed \
    --osx-bundle-identifier "com.moovy.app" \
    --target-architecture universal2 \
    --noupx \
    src/main.py

if [ $? -ne 0 ]; then
    echo ""
    echo "===================================================="
    echo "Build FAILED!"
    echo "===================================================="
    exit 1
fi

echo ""
echo "===================================================="
echo "Build SUCCESSFUL!"
echo "===================================================="
echo ""
echo "Application bundle created at:"
echo "  $(pwd)/dist/Moovy.app"
echo ""

# Create DMG if create-dmg is available
if command -v create-dmg &> /dev/null; then
    echo "Creating DMG disk image..."
    
    # Remove old DMG if it exists
    rm -f dist/Moovy.dmg
    
    # Create DMG with nice layout
    create-dmg \
        --volname "Moovy" \
        --volicon "src/icons/icon.ico" \
        --window-pos 200 120 \
        --window-size 600 400 \
        --icon-size 100 \
        --icon "Moovy.app" 150 190 \
        --hide-extension "Moovy.app" \
        --app-drop-link 450 190 \
        "dist/Moovy.dmg" \
        "dist/"
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "✓ DMG created successfully!"
        echo "  $(pwd)/dist/Moovy.dmg"
    else
        echo ""
        echo "⚠️  DMG creation failed (create-dmg not available)"
        echo "Using hdiutil instead..."
        
        # Fallback to hdiutil
        hdiutil create -volname "Moovy" \
            -srcfolder "dist/Moovy.app" \
            -ov -format UDZO "dist/Moovy.dmg"
        
        echo ""
        echo "✓ DMG created with hdiutil"
        echo "  $(pwd)/dist/Moovy.dmg"
    fi
else
    echo ""
    echo "Creating DMG using hdiutil..."
    
    # Create temporary folder for DMG
    mkdir -p /tmp/Moovy_DMG
    cp -r dist/Moovy.app /tmp/Moovy_DMG/
    
    # Create a symlink to Applications folder
    ln -s /Applications /tmp/Moovy_DMG/Applications
    
    # Create DMG
    hdiutil create -volname "Moovy" \
        -srcfolder /tmp/Moovy_DMG \
        -ov -format UDZO "dist/Moovy.dmg"
    
    # Cleanup
    rm -rf /tmp/Moovy_DMG
    
    echo ""
    echo "✓ DMG created successfully!"
    echo "  $(pwd)/dist/Moovy.dmg"
fi

echo ""
echo "===================================================="
echo "macOS Distribution Package Ready!"
echo "===================================================="
echo ""
echo "Files created:"
echo "  • dist/Moovy.app - Application bundle"
echo "  • dist/Moovy.dmg - Disk image for distribution"
echo ""
echo "To distribute:"
echo "  1. Share the Moovy.dmg file"
echo "  2. Users can open it and drag Moovy.app to Applications"
echo ""
echo "NOTE: Users still need FFmpeg installed:"
echo "  brew install ffmpeg"
echo ""
