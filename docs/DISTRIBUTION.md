# Moovy - Standalone Application Distribution

This guide explains how to build and distribute standalone Moovy applications for Windows, macOS, and Linux.

---

# Windows

## Building the Executable

### Option 1: Standard Distribution (Recommended)

Run the build script:
```batch
build_standalone.bat
```

This creates a folder `dist\Moovy\` containing:
- `Moovy.exe` - The application executable
- Supporting DLL files and libraries
- Resource files (icons, etc.)

**File size**: ~200-300 MB (includes Python runtime)

### Option 2: Single-File Executable

For a single-file executable:
```batch
build_standalone_onefile.bat
```

This creates `dist\Moovy.exe` as a standalone executable.

**Pros:**
- Single file to distribute
- Easy to share and deploy

**Cons:**
- Larger file size (~300-400 MB)
- Slower startup time (extracts on first run)

## Distribution Options

### Method A: Folder Distribution (Recommended)

1. Navigate to `dist\Moovy\`
2. Create a ZIP archive of the entire folder
3. Share the ZIP file

Recipients:
1. Extract the ZIP
2. Run `Moovy.exe`
3. Install FFmpeg (if not already installed)

### Method B: Installer Creation

Create a Windows installer using NSIS or InnoSetup:

1. **Install InnoSetup** (free): https://jrsoftware.org/isdl.php

2. Create installer script (`moovy_installer.iss`):
```ini
[Setup]
AppName=Moovy
AppVersion=1.0
DefaultDirName={pf}\Moovy
DefaultGroupName=Moovy
OutputDir=dist
OutputBaseFilename=Moovy-Installer

[Files]
Source: "dist\Moovy\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs

[Icons]
Name: "{group}\Moovy"; Filename: "{app}\Moovy.exe"
Name: "{group}\Uninstall Moovy"; Filename: "{uninstallexe}"
Name: "{userdesktop}\Moovy"; Filename: "{app}\Moovy.exe"

[Run]
Filename: "{app}\Moovy.exe"; Description: "Launch Moovy"; Flags: nowait postinstall skipifsilent
```

3. Build installer with InnoSetup

### Method C: Single EXE Distribution

Simply share `dist\Moovy.exe` (from onefile build)

Recipients can move it anywhere and run directly.

---

# macOS

## Building the DMG Application

### Prerequisites

- macOS 10.13 or later
- Python 3.8+
- Homebrew (optional, for create-dmg)

### Standard Approach (Recommended)

Run the build script:
```bash
chmod +x build_macos.sh
./build_macos.sh
```

This creates:
- `dist/Moovy.app` - macOS application bundle
- `dist/Moovy.dmg` - Disk image for distribution

**File size**: ~250-350 MB (includes Python runtime)

### What Gets Created

The DMG contains a professional installer with:
- Moovy.app bundle
- Easy drag-and-drop installation to Applications
- Nice visual layout with application icon
- Shortcut to Applications folder

### Installation Instructions for Users

Users can install Moovy by:

1. Download `Moovy.dmg`
2. Open the DMG file (double-click)
3. Drag `Moovy.app` to the `Applications` folder
4. Eject the DMG
5. Launch from Applications or Spotlight search

### Code Signing and Notarization (Optional)

For distribution via App Store or to remove Gatekeeper warnings:

```bash
chmod +x build_macos_notarized.sh
./build_macos_notarized.sh
```

This script:
- Requires Apple Developer account and signing certificate
- Signs the application with your developer certificate
- Creates a notarized DMG
- Provides instructions for Apple notarization process

**Benefits:**
- Users won't see "unknown developer" warning
- App passes App Store checks
- Professional distribution

**Requirements:**
- Apple Developer membership ($99/year)
- Signing certificate installed on Mac
- App-specific password for notarization

### Building Without create-dmg

If `create-dmg` is not installed, the build script automatically falls back to using `hdiutil`:

```bash
hdiutil create -volname "Moovy" \
    -srcfolder dist/Moovy.app \
    -ov -format UDZO "dist/Moovy.dmg"
```

## macOS System Requirements

- **OS**: macOS 10.13 or later
- **Processor**: Intel or Apple Silicon (M1/M2/M3+)
- **RAM**: 2 GB minimum
- **Storage**: 300+ MB for installation
- **FFmpeg**: Required (users install via Homebrew)

## Installing create-dmg (Optional)

For nicer DMG appearance with custom background and layout:

```bash
brew install create-dmg
```

## Distribution

### Method A: Direct DMG Distribution (Recommended)

1. Build the DMG: `./build_macos.sh`
2. Test on macOS system
3. Share `dist/Moovy.dmg` file
4. Users open DMG and drag app to Applications

Advantages:
- Professional appearance
- Easy installation
- Familiar to macOS users

### Method B: Archive Distribution

```bash
# Create app bundle (without DMG)
./build_macos.sh  # Creates dist/Moovy.app

# Zip the app
cd dist
zip -r Moovy.zip Moovy.app

# Share Moovy.zip
```

Users:
1. Download and extract Moovy.zip
2. Move Moovy.app to Applications
3. Launch from Launchpad

### Method C: Web Distribution

1. Build DMG with `./build_macos.sh`
2. Upload `dist/Moovy.dmg` (~250-350 MB) to web server
3. Provide download link to users

## Troubleshooting macOS

### "macOS cannot verify the developer" Warning

**Cause**: Application not code-signed

**Solutions:**
1. Use notarized build: `./build_macos_notarized.sh`
2. Or temporariliy bypass: Right-click app → Open (one-time approval)

### Application Won't Launch

**Check these:**
- Ensure you're on macOS 10.13+
- Try launching from Spotlight search
- Check Console.app for error messages
- Ensure FFmpeg is installed: `brew install ffmpeg`

### FFmpeg Not Found

```bash
brew install ffmpeg
```

The app will automatically detect FFmpeg from Homebrew installation.

### App is Slow to Start

First launch extracts Python runtime from app bundle. This is normal and takes 5-10 seconds on first run.

---

## FFmpeg Dependency

The application requires FFmpeg to analyze video codecs.

### For Users

Installation options on Windows:

**Using WinGet (Recommended - Windows 11):**
```powershell
winget install ffmpeg
```

**Using Scoop:**
```powershell
scoop install ffmpeg
```

**Using Chocolatey:**
```powershell
choco install ffmpeg
```

**Manual Installation:**
1. Download from: https://ffmpeg.org/download.html
2. Extract to a folder (e.g., `C:\FFmpeg`)
3. Add the `bin` folder to system PATH

### For Customized Distribution

To bundle FFmpeg with the application:

1. Download FFmpeg binaries
2. Copy to `dist\Moovy\ffmpeg\`
3. Modify `FFmpegAnalyzer._find_ffprobe()` to check this location first

## System Requirements

- **Windows**: 7 SP1 or later (64-bit recommended)
- **RAM**: 2 GB minimum
- **Storage**: 300+ MB for installation
- **FFmpeg**: Required (the application will guide users to install it)

## Troubleshooting

### App Won't Start
- Ensure .NET Framework 4.5+ is installed
- Check Windows event logs for errors
- Try running as administrator

### FFmpeg Not Found
- Install FFmpeg using one of the methods above
- Restart the application

### File Dialog Crashes
- Update Windows to latest version
- Try running in compatibility mode (Windows 10)

### Icons Not Displaying
- Ensure `src/icons` folder is included in distribution
- Check folder structure is intact

## Development vs Distribution

**Development:**
- Use `run.bat` to run from source
- Direct access to code for debugging

**Distribution:**
- Use `build_standalone.bat` to create executable
- Single-click launch
- No development environment needed

## Build Details

The build process (PyInstaller):

1. Analyzes dependencies from `src/main.py`
2. Bundles Python runtime (3.13+)
3. Includes PyQt6 framework
4. Packages icon and data files
5. Creates executable with launcher

Result: Fully standalone application that works on any Windows PC (no Python installation needed)

## Version Updating

When you update the application:

1. Make code changes
2. Run `build_standalone.bat` to rebuild
3. Increment version in documentation
4. Create new release/distribution package

## Additional Resources

- **PyInstaller Docs**: https://pyinstaller.readthedocs.io/
- **FFmpeg Downloads**: https://ffmpeg.org/download.html
- **Python Packaging**: https://packaging.python.org/
