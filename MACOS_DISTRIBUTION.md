# Moovy macOS Distribution Guide

This guide covers building and distributing Moovy for macOS.

## Quick Start

### Build DMG (5 minutes)

```bash
# Navigate to Moovy folder
cd /path/to/Moovy

# Make script executable
chmod +x build_macos.sh

# Run build
./build_macos.sh
```

Output: `dist/Moovy.dmg` (~250-350 MB)

## System Requirements for Building

- macOS 10.13 or later
- Python 3.8+
- Homebrew (optional)
- Development tools installed via: `xcode-select --install`

## Pre-Build Setup

### 1. Create Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Install Optional DMG Creation Tool

```bash
brew install create-dmg
```

If not installed, the build script will automatically use `hdiutil` instead.

## Building Process

### Standard Build

```bash
./build_macos.sh
```

Creates:
- `dist/Moovy.app` - Application bundle
- `dist/Moovy.dmg` - Disk image

### Code-Signed & Notarized Build

For official App Store distribution or to remove Gatekeeper warnings:

```bash
./build_macos_notarized.sh
```

**Prerequisites:**
- Apple Developer account ($99/year)
- Developer certificate installed
- Provisioning profile (if needed)

### Manual Build (Debug/Development)

```bash
source .venv/bin/activate

python -m PyInstaller \
    --name Moovy \
    --icon src/icons/icon.ico \
    --add-data "src/icons:src/icons" \
    --windowed \
    --osx-bundle-identifier "com.moovy.app" \
    --target-architecture universal2 \
    Moovy_macos.spec
```

## Distribution Options

### Option 1: DMG File (Recommended)

**For Users:**
1. Download `Moovy.dmg`
2. Double-click to open
3. Drag `Moovy.app` to Applications folder
4. Eject DMG
5. Launch Moovy from Applications

**Advantages:**
- Professional appearance
- Easy to use
- Familiar macOS workflow
- Small download size

**Share via:**
- Email (if under size limit)
- File sharing services (Dropbox, Google Drive, OneDrive)
- Website download
- GitHub releases

### Option 2: ZIP Archive

```bash
cd dist
zip -r Moovy.zip Moovy.app
```

**For Users:**
1. Download `Moovy.zip`
2. Extract (usually automatic)
3. Move `Moovy.app` to Applications
4. Launch from Launchpad

### Option 3: Direct App Bundle

Share `dist/Moovy.app` directory directly.

Users can:
- Copy to Applications
- Run directly from any location
- Create alias/shortcut

## Installation Instructions for Users

### First Time Installation

```bash
1. Download Moovy.dmg
2. Open the file (double-click)
3. In the window that appears:
   • Left side: Moovy.app (the application)
   • Right side: Applications folder (your applications directory)
4. Drag Moovy.app to the Applications folder
5. Wait for copy to complete
6. Eject the DMG (drag to trash)
7. Open Applications (Cmd + Shift + A)
8. Double-click Moovy to launch
```

### Subsequent Launches

```bash
# From Spotlight (easiest)
Cmd + Space
Type: Moovy
Press: Enter

# Or from Applications folder
Cmd + Shift + A
Find Moovy
Double-click
```

### Uninstall

```bash
1. Open Applications folder (Cmd + Shift + A)
2. Find Moovy
3. Drag to Trash
4. Empty Trash
```

## FFmpeg Installation

Moovy requires FFmpeg. Users should install before running:

```bash
# Option 1: Homebrew (Recommended)
brew install ffmpeg

# Option 2: Download binary
# Visit https://ffmpeg.org/download.html
# Extract to /usr/local/bin/ or similar
```

The app will automatically find FFmpeg from:
- Homebrew installation
- System PATH
- Common installation directories

## Code Signing & Notarization

### For App Store Distribution

1. **Request signing certificate from Apple**
   - Visit Apple Developer Portal
   - Create signing certificate
   - Install on your Mac

2. **Code sign the app**
   ```bash
   codesign -s "Developer ID Application" dist/Moovy.app
   ```

3. **Submit for notarization**
   ```bash
   xcrun notarytool submit dist/Moovy.dmg
   xcrun notarytool info <submission-id>  # Check status
   xcrun stapler staple dist/Moovy.dmg   # Attach ticket
   ```

4. **Users can now install without warnings**

### For Simple Distribution (No Signing)

Users can bypass warning once:
- Right-click Moovy.app
- Select "Open"
- Click "Open" when prompted

## Troubleshooting

### Build Fails - "create-dmg not found"

This is normal. The script will use `hdiutil` instead.

### DMG Won't Open

- Try re-downloading
- Check macOS version (10.13+)
- Try from a different location (Desktop, Downloads)

### App Won't Launch

**Check FFmpeg:**
```bash
which ffmpeg    # Should show FFmpeg location
ffmpeg -version # Show version
```

If not found, install:
```bash
brew install ffmpeg
```

**Check Console for errors:**
1. Open Console.app
2. Search for "Moovy"
3. Look for error messages

### "macOS cannot verify the developer" Warning

**Cause**: App not signed by Apple-recognized certificate

**Solutions:**
1. Right-click → Open (bypass once)
2. Or: `xattr -d com.apple.quarantine /Applications/Moovy.app`
3. Or: Use signed/notarized build

### Application Behaves Strangely

1. Close Moovy completely
2. Clear cache:
   ```bash
   rm -rf ~/Library/Caches/Moovy
   ```
3. Restart Moovy

## Version Updates

### Update Users

1. Make code changes
2. Run `./build_macos.sh`
3. Update version in documentation
4. Upload new `dist/Moovy.dmg`

### In-App Version Check (Future)

Could add periodic check for updates:
```python
# Proposed feature
app_version = "1.0.0"
latest_version = check_github_releases()
if latest_version > app_version:
    notify_user("Update available")
```

## Performance Notes

- **First launch**: May take 5-10 seconds (Python runtime extraction)
- **Subsequent launches**: 1-2 seconds
- **Large drive scans**: May take 30+ minutes (depends on drive size)
- **Codec analysis**: Real-time, non-blocking (uses background threads)

## Compatibility

### Supported macOS Versions

| Version | Support | Notes |
|---------|---------|-------|
| Big Sur (11) | ✓ Full | Recommended minimum |
| Monterey (12) | ✓ Full | |
| Ventura (13) | ✓ Full | |
| Sonoma (14) | ✓ Full | Current |

### Apple Silicon (M1/M2/M3+)

The app includes universal2 support and runs natively on Apple Silicon Macs at full speed.

## Development Notes

### Build from Source

```bash
# Development install
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m src.main
```

### Modify Build Script

Edit `build_macos.sh` to customize:
- Application name
- Bundle identifier
- Target architectures
- Icons/resources

### Using Spec File

For advanced customization, use the spec file:

```bash
python -m PyInstaller Moovy_macos.spec
```

Edit `Moovy_macos.spec` to change build options.

## Additional Resources

- [PyInstaller Documentation](https://pyinstaller.readthedocs.io/)
- [macOS App Distribution](https://developer.apple.com/macos/distribution/)
- [Apple Notarization](https://developer.apple.com/documentation/security/notarizing_macos_software_before_distribution)
- [Code Signing Guide](https://developer.apple.com/library/archive/documentation/Security/Conceptual/CodeSigningGuide/)
- [Homebrew](https://brew.sh/)
