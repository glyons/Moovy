#!/bin/bash
# Build notarized macOS application for official App Store / Gatekeeper approval

echo ""
echo "===================================================="
echo "Building Notarized Moovy - macOS App"
echo "===================================================="
echo ""
echo "NOTE: This script requires:"
echo "  • Apple Developer account"
echo "  • Valid signing certificate"
echo "  • App-specific password"
echo ""

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Error: Virtual environment not found!"
    echo "Please run: ./run.sh first"
    exit 1
fi

# Activate virtual environment
source .venv/bin/activate

# Get signing identity
echo "Available signing identities:"
security find-identity -v -p codesigning | grep -i "Mac Developer"
echo ""
read -p "Enter signing identity (or press Enter to skip signing): " SIGNING_IDENTITY

echo ""
echo "Building application bundle..."

# Build using PyInstaller
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
    echo "Build FAILED!"
    exit 1
fi

echo "✓ Application bundle created"

# Sign the app if identity provided
if [ -n "$SIGNING_IDENTITY" ]; then
    echo ""
    echo "Signing application..."
    
    # Sign all frameworks first
    find "dist/Moovy.app/Contents/Frameworks" -type f -name "*.dylib" \
        -exec codesign --force --verify --verbose --timestamp \
        --options=runtime \
        --entitlements entitlements.plist \
        -s "$SIGNING_IDENTITY" {} \;
    
    # Sign the main executable
    codesign --force --verify --verbose --timestamp \
        --options=runtime \
        --entitlements entitlements.plist \
        -s "$SIGNING_IDENTITY" \
        "dist/Moovy.app"
    
    echo "✓ Application signed"
    
    # Create DMG
    echo ""
    echo "Creating DMG..."
    
    mkdir -p /tmp/Moovy_DMG
    cp -r dist/Moovy.app /tmp/Moovy_DMG/
    ln -s /Applications /tmp/Moovy_DMG/Applications
    
    hdiutil create -volname "Moovy" \
        -srcfolder /tmp/Moovy_DMG \
        -ov -format UDZO "dist/Moovy.dmg"
    
    rm -rf /tmp/Moovy_DMG
    
    # Sign the DMG
    echo ""
    echo "Signing DMG..."
    codesign --force --verify --verbose --timestamp \
        -s "$SIGNING_IDENTITY" \
        "dist/Moovy.dmg"
    
    echo ""
    echo "===================================================="
    echo "Notarization Process"
    echo "===================================================="
    echo ""
    echo "To notarize your app for Gatekeeper approval:"
    echo ""
    echo "1. Request app-specific password:"
    echo "   xcrun notarytool store-credentials"
    echo ""
    echo "2. Submit DMG for notarization:"
    echo "   xcrun notarytool submit dist/Moovy.dmg --wait"
    echo ""
    echo "3. Staple the notarization ticket:"
    echo "   xcrun stapler staple dist/Moovy.dmg"
    echo ""
    echo "For more info:"
    echo "   https://developer.apple.com/documentation/security/notarizing_macos_software_before_distribution"
    echo ""
else
    echo ""
    echo "Skipping code signing (unsigned app)"
    echo ""
    echo "Creating DMG..."
    
    mkdir -p /tmp/Moovy_DMG
    cp -r dist/Moovy.app /tmp/Moovy_DMG/
    ln -s /Applications /tmp/Moovy_DMG/Applications
    
    hdiutil create -volname "Moovy" \
        -srcfolder /tmp/Moovy_DMG \
        -ov -format UDZO "dist/Moovy.dmg"
    
    rm -rf /tmp/Moovy_DMG
    
    echo "✓ DMG created (unsigned)"
fi

echo ""
echo "===================================================="
echo "Build Complete!"
echo "===================================================="
echo ""
echo "Output files:"
echo "  • dist/Moovy.app - Application bundle"
echo "  • dist/Moovy.dmg - Disk image"
echo ""
