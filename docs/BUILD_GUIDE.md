# Moovy - Build & Distribution Guide

Quick reference for building standalone applications for Windows, macOS, and Linux.

## Quick Start

### Windows

```batch
# Standard Distribution (Recommended)
build_standalone.bat
# Creates: dist\Moovy\Moovy.exe (~200-300 MB)

# Single-File Executable
build_standalone_onefile.bat
# Creates: dist\Moovy.exe (~300-400 MB)
```

### macOS

```bash
# Build DMG
chmod +x build_macos.sh
./build_macos.sh
# Creates: dist/Moovy.dmg (~250-350 MB)

# Code-signed & Notarized (Optional)
chmod +x build_macos_notarized.sh
./build_macos_notarized.sh
```

### Linux

```bash
# Build AppImage
chmod +x build_linux.sh
./build_linux.sh
# Creates: dist/Moovy-x86_64.AppImage (~200-300 MB)
```

## Documentation

| Platform | Main Guide | Details |
|----------|-----------|---------|
| **Windows** | [DISTRIBUTION.md](DISTRIBUTION.md) | Exe, installer, zip distribution |
| **macOS** | [MACOS_DISTRIBUTION.md](MACOS_DISTRIBUTION.md) | DMG, code signing, notarization |
| **Linux** | [LINUX_DISTRIBUTION.md](LINUX_DISTRIBUTION.md) | AppImage, Snap, deb/rpm |

## Build Scripts

| Script | Platform | Output | Size |
|--------|----------|--------|------|
| `build_standalone.bat` | Windows | `dist\Moovy\Moovy.exe` | 200-300 MB |
| `build_standalone_onefile.bat` | Windows | `dist\Moovy.exe` | 300-400 MB |
| `build_macos.sh` | macOS | `dist/Moovy.dmg` | 250-350 MB |
| `build_macos_notarized.sh` | macOS | `dist/Moovy.dmg` (signed) | 250-350 MB |
| `build_linux.sh` | Linux | `dist/Moovy-x86_64.AppImage` | 200-300 MB |

## PyInstaller Spec Files

| File | Purpose |
|------|---------|
| `Moovy.spec` | Windows build configuration |
| `Moovy_macos.spec` | macOS build configuration |
| `Moovy_linux.spec` | Linux build configuration |

## Key Features

✓ **Icon Buttons with Tooltips** - Professional icon-based toolbar
✓ **Menubar** - Tools and Help menus
✓ **About Dialog** - Application information
✓ **Cow Icon** - Custom application mascot
✓ **Cancel Scan Button** - Stop long-running operations
✓ **Batch Conversion** - Convert multiple files at once
✓ **Codec Detection** - FFmpeg-based analysis
✓ **Samsung TV Compatibility** - Check video/audio codec support

## FFmpeg Requirement

All platforms require FFmpeg installed by users:

```bash
# Windows
winget install ffmpeg

# macOS
brew install ffmpeg

# Linux
sudo apt install ffmpeg  # Ubuntu/Debian
sudo dnf install ffmpeg  # Fedora
```

## Distribution Checklist

- [ ] Application builds successfully
- [ ] All icons display correctly
- [ ] FFmpeg detection works
- [ ] Menubar functions properly
- [ ] Cancel button works during scans
- [ ] Batch conversion works
- [ ] Application closes cleanly
- [ ] All files properly packaged

## Version Management

When updating version:

1. Update version in documentation
2. Rebuild all platforms
3. Test on each OS
4. Update release notes
5. Create distribution packages
6. Upload to distribution channels

## Performance Notes

### Build Times

- **Windows**: 2-5 minutes
- **macOS**: 3-7 minutes (longer on M1/M2)
- **Linux**: 2-4 minutes

### First Launch

- **All platforms**: 5-10 seconds (Python runtime extraction)
- **Subsequent launches**: 1-2 seconds

### Large Operations

- **Folder scan**: Real-time, responsive (uses threading)
- **Drive scan**: 30+ minutes depending on drive size
- **Codec analysis**: Background processing, non-blocking
- **File conversion**: Depends on video size/codec

## System Requirements

### Windows
- Windows 7 SP1 or later (64-bit)
- 2 GB RAM minimum
- 300+ MB disk space
- FFmpeg required

### macOS
- macOS 10.13 or later
- 2 GB RAM minimum
- 300+ MB disk space
- Apple Silicon (M1/M2/M3+) supported
- FFmpeg required

### Linux
- Ubuntu 16.04+, Fedora 25+, Debian 9+
- 2 GB RAM minimum
- 300+ MB disk space
- FFmpeg required

## Troubleshooting

### General

- Ensure PyInstaller is installed: `pip install pyinstaller`
- Check Python version: `python --version` (3.8+)
- Verify FFmpeg: `ffmpeg -version`

### Windows

- Run scripts in PowerShell (not CMD.exe)
- If build fails, clean: `rmdir /s build dist`
- Check that no `Moovy.exe` is running

### macOS

- Make scripts executable: `chmod +x *.sh`
- If build fails, clean: `rm -rf build dist`
- For notarization, verify Apple Developer account

### Linux

- Make scripts executable: `chmod +x *.sh`
- Install dependencies: `apt-get install python3-dev`
- Check AppImage tool availability

## Support

For issues or questions:

1. Check platform-specific documentation
2. Review build script comments
3. Check PyInstaller documentation
4. Verify FFmpeg installation
5. Review application logs

## Additional Resources

- [PyInstaller Documentation](https://pyinstaller.readthedocs.io/)
- [FFmpeg Documentation](https://ffmpeg.org/documentation.html)
- [Qt Framework Docs](https://doc.qt.io/)

---

**Last Updated**: February 2026
**Version**: 1.0.0
