# Moovy - Movie Codec Analyzer

A desktop application for analyzing movie files, displaying codec information, and checking Samsung TV compatibility. Built with Python and PyQt6, using FFmpeg for codec detection.

## Features

- **Recursive folder scanning** to find all movie files
- **Codec detection** (audio and video) using FFmpeg
- **Samsung TV compatibility checking** for H.264 and H.265 video codecs with AAC audio
- **Grid display** with compatibility icons (✓ / ✗)
- **Context menu** for converting incompatible files to compatible formats
- **Real-time codec analysis** of media files
- **Multi-threaded** analysis to prevent UI freezing
- **Icon-based toolbar** with tooltips for easy navigation
- **Batch conversion** of multiple incompatible files at once
- **Windows standalone executable** (no Python installation needed)

## System Requirements

- **Operating System**: Windows 7+, macOS 10.13+, or Linux
- **Python**: 3.8 or later
- **FFmpeg**: (installed and in PATH)
- **PyQt6**: (automatically installed)

## Quick Start

### Windows

1. **Double-click `run.bat`** to launch the application
   - It will automatically set up the virtual environment
   - Install dependencies
   - Launch the application

### macOS / Linux

1. **Make the script executable:**
   ```bash
   chmod +x run.sh
   ```

2. **Run the application:**
   ```bash
   ./run.sh
   ```
   - It will automatically set up the virtual environment
   - Install dependencies
   - Launch the application

### Quick Reference Commands

| Task | Windows | macOS / Linux |
|------|---------|---------------|
| **Launch App** | Double-click `run.bat` | `./run.sh` |
| **Install FFmpeg** | `.\setup_ffmpeg.ps1` | `./setup_ffmpeg.sh` |
| **Create venv** | `python -m venv .venv` | `python3 -m venv .venv` |
| **Activate venv** | `.venv\Scripts\activate` | `source .venv/bin/activate` |
| **Install deps** | `pip install -r requirements.txt` | `pip install -r requirements.txt` |
| **Run app** | `python -m src.main` | `python3 -m src.main` |
| **Check FFmpeg** | `ffmpeg -version` | `ffmpeg -version` |

---

## Windows Standalone Distribution

For users who don't want to install Python or manage a virtual environment, you can create a standalone Windows executable:

### Building the Standalone Executable

**Option 1: Standard Distribution (Recommended)**
```batch
build_standalone.bat
```
Creates: `dist\Moovy\Moovy.exe` with all dependencies (~200 MB)

**Option 2: Single-File Executable**
```batch
build_standalone_onefile.bat
```
Creates: `dist\Moovy.exe` as a single file (~300+ MB)

### Distribution

1. Extract or copy the executable and supporting files
2. Share with users
3. Users can run directly (no Python installation needed)
4. Users still need FFmpeg installed on their system

See [DISTRIBUTION.md](DISTRIBUTION.md) for detailed instructions on building, packaging, and distributing the application.

---

## macOS Standalone Distribution

Create a professional macOS DMG (Disk Image) for easy distribution:

### Building the DMG

```bash
chmod +x build_macos.sh
./build_macos.sh
```

Creates:
- `dist/Moovy.app` - macOS application bundle
- `dist/Moovy.dmg` - Disk image for distribution (~250-350 MB)

### Users can install by:

1. Download `Moovy.dmg`
2. Open the DMG file
3. Drag `Moovy.app` to Applications folder
4. Launch from Applications or Spotlight

### Code Signing & Notarization

For App Store distribution or to remove Gatekeeper warnings (optional):

```bash
chmod +x build_macos_notarized.sh
./build_macos_notarized.sh
```

Requires Apple Developer account ($99/year).

See [MACOS_DISTRIBUTION.md](MACOS_DISTRIBUTION.md) for complete macOS build and distribution guide.

---

### Option 2: Manual Setup

#### 1. Install FFmpeg

**Windows:**

Choose one of these methods:

**Method A: Automatic PowerShell Script** (Recommended)
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\setup_ffmpeg.ps1
```

**Method B: Manual Download**
- Download from: https://ffmpeg.org/download.html
- Extract to `C:\FFmpeg` or another location
- Add the `bin` folder to your system PATH

**Method C: Package Manager**
```powershell
# Using Winget (Windows 11)
winget install ffmpeg

# Using Scoop
scoop install ffmpeg

# Using Chocolatey
choco install ffmpeg
```

---

**macOS:**

```bash
# Using Homebrew (recommended)
brew install ffmpeg

# Or using MacPorts
sudo port install ffmpeg +universal
```

---

**Linux:**

```bash
# Ubuntu / Debian
sudo apt-get update
sudo apt-get install ffmpeg

# Fedora / RHEL
sudo dnf install ffmpeg
# or (older versions)
sudo yum install ffmpeg

# Arch Linux
sudo pacman -S ffmpeg

# Alpine Linux
sudo apk add ffmpeg
```

---

Alternatively, for **all platforms**, run the automated setup script:

**Windows:**
```powershell
.\setup_ffmpeg.ps1
```

**macOS / Linux:**
```bash
chmod +x setup_ffmpeg.sh
./setup_ffmpeg.sh
```

#### 2. Install Python Dependencies

```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# macOS / Linux:
source .venv/bin/activate

# Install required packages
pip install -r requirements.txt
```

#### 3. Run the Application

**Windows:**
```bash
python -m src.main
```

**macOS / Linux:**
```bash
python3 -m src.main
```

## Usage

1. **Scan Folder**: Click "Scan Folder" and select a folder containing video files
   - The app will recursively scan all subfolders
   - Found video files will be displayed in the grid

2. **Scan Drive**: Click "Scan Drive" to scan an entire drive
   - Windows: Choose from available drive letters (C:, D:, E:, etc.)
   - macOS/Linux: Choose from mount points
   - Warning dialog will show before scan starts
   - Can take a while on large drives

3. **Analyze Codecs**: The app automatically analyzes each video file for codec information
   - Video codec (e.g., H.264, H.265, VP9, etc.)
   - Audio codec (e.g., AAC, MP3, AC3, etc.)

4. **Check Samsung TV Compatibility**: The compatibility icon shows:
   - **✓ (Green)**: File is compatible with Samsung TV
   - **✗ (Red)**: File needs conversion

5. **Convert Files**: 
   - **Individual**: Right-click on incompatible files to convert
     - Convert to Samsung TV compatible format (H.264 + AAC in MP4 container)
     - Choose output file location
     - Monitor conversion progress
   - **Batch**: Click "Batch Convert" to convert all incompatible files at once
     - Select output folder for all conversions
     - Files are converted sequentially
     - Progress dialog shows real-time status
     - All results displayed in summary

6. **View Details**: Right-click on any file to:
   - View full file details
   - Open file location in Explorer
   - See why a file is incompatible (if applicable)

## Project Structure

```
src/
├── main.py                      # Application entry point
├── ui/
│   ├── __init__.py
│   └── main_window.py          # Main GUI window and dialogs
├── utils/
│   ├── __init__.py
│   ├── ffmpeg_analyzer.py      # FFmpeg codec extraction & conversion
│   ├── samsung_compatibility.py # Samsung TV compatibility checking
│   └── file_scanner.py         # Recursive file scanning
├── models/
│   ├── __init__.py
│   └── movie.py                # Movie data model
└── icons/
    ├── __init__.py
    ├── icon.ico                # Windows icon file
    ├── icon_256.png            # 256x256 PNG icon
    ├── icon_128.png            # 128x128 PNG icon
    ├── icon_64.png             # 64x64 PNG icon
    └── icon_32.png             # 32x32 PNG icon
```

## Configuration

### Samsung TV Compatible Codecs

**Video Codecs:**
- H.264/AVC
- H.265/HEVC

**Audio Codecs:**
- AAC
- MP3
- AC3
- EAC3
- FLAC
- PCM

### Supported Video Formats

The application recognizes these file extensions:
- MP4, MKV, AVI, MOV, FLV, WMV, WebM
- M4V, MPG, MPEG, 3GP, OGV, TS, M2TS, MTS
- VOB, F4V, ASF, RM, RMVB, M3U8, and more

### Conversion Target Format

Incompatible files are converted to:
- **Container**: MP4
- **Video Codec**: H.264/AVC
- **Audio Codec**: AAC
- **Quality**: Medium preset

## Application Icon Design

The Moovy application features a professional, modern icon that represents its core functionality:

**Design Elements:**
- **Film Reels**: Left and right film reels represent video content and the legacy of cinema
- **Film Strip**: Vintage film frames between the reels symbolize media analysis
- **Green Play Button**: Central play button with a checkmark indicates compatibility checking
- **Checkmark**: Represents the compatibility verification feature
- **Color Scheme**: Professional blue background with green accent for "compatible" status

The icon is available in multiple formats:
- **icon.ico** - Windows application icon (multi-size)
- **icon_256.png** - Large desktop icon (256×256)
- **icon_128.png** - Medium icon (128×128)
- **icon_64.png** - Standard icon (64×64)
- **icon_32.png** - Taskbar icon (32×32)

## Troubleshooting

### "FFmpeg not found"

**Windows:**
- Check: Open PowerShell and run `ffmpeg -version`
- If not found, run `.\setup_ffmpeg.ps1` or install FFmpeg manually

**macOS:**
- Check: Open Terminal and run `ffmpeg -version`
- If not found, run `brew install ffmpeg`
- If Homebrew not found, install it from: https://brew.sh

**Linux:**
- Check: Open Terminal and run `ffmpeg -version`
- If not found, run `./setup_ffmpeg.sh` or install using your package manager:
  - `sudo apt-get install ffmpeg` (Ubuntu/Debian)
  - `sudo dnf install ffmpeg` (Fedora)
  - `sudo pacman -S ffmpeg` (Arch)

### "Python not found" or "Python 3 not found"

**Windows:**
- Install Python from: https://www.python.org/downloads/
- Make sure to check "Add Python to PATH" during installation

**macOS:**
- Check: Run `python3 --version`
- Install: `brew install python3`

**Linux:**
- Check: Run `python3 --version`
- Install: `sudo apt-get install python3 python3-venv` (Ubuntu/Debian)

### "DLL load failed" error (Windows)

- **Solution**: Reinstall PyQt6
  ```bash
  pip install --force-reinstall PyQt6
  ```

### Permission denied when running scripts (macOS/Linux)

- **Solution**: Make scripts executable
  ```bash
  chmod +x run.sh
  chmod +x setup_ffmpeg.sh
  ```

### "virtual environment script not found" (macOS/Linux)

- **Cause**: Virtual environment not created or corrupted
- **Solution**: Delete `.venv` folder and recreate it
  ```bash
  rm -rf .venv
  python3 -m venv .venv
  source .venv/bin/activate
  pip install -r requirements.txt
  ```

### Files not found during scan
- **Cause**: File extension is not recognized or folder permission issue
- **Solution**: 
  - Check that file extension is in the supported list
  - Ensure the user has read permissions for the folder

### Conversion fails
- **Cause**: FFmpeg path issue or corrupted video file
- **Solution**:
  - Verify FFmpeg is in PATH: `ffmpeg -version`
  - Test with a different video file
  - Check that the input file is not corrupted

## Technical Details

### Threading Model
- **File Scanning**: Runs in separate thread to prevent UI freezing
- **Codec Analysis**: Runs in separate thread for each movie
- **File Conversion**: Runs in separate thread with progress updates

### FFmpeg Commands Used
- **Analysis**: `ffprobe` to extract codec information
- **Conversion**: `ffmpeg` with libx264 encoder and AAC audio encoder

## License

This project is provided as-is for personal use.

## Requirements

- **PyQt6**: Desktop GUI framework
- **FFmpeg**: Media codec analysis and conversion
- **Python 3.8+**: Programming language

---

## Available Launcher Scripts

| Platform | Script | Command | Notes |
|----------|--------|---------|-------|
| **Windows** | `run.bat` | Double-click or `run.bat` | Easiest option |
| **macOS/Linux** | `run.sh` | `chmod +x run.sh && ./run.sh` | Requires execution permission |

Both scripts automatically:
- Create Python virtual environment (if needed)
- Install dependencies
- Check for FFmpeg
- Launch the application

---

## Cross-Platform Compatibility

Moovy is fully compatible with Windows, macOS, and Linux. The application has been designed with cross-platform considerations:

- **File Paths**: Automatically handles Windows (`\`) and Unix (`/`) path separators
- **Python 3**: Uses `python3` on macOS/Linux and `python` on Windows
- **Virtual Environments**: Properly configured for all platforms
- **GUI Framework**: PyQt6 is fully supported on all major operating systems
- **FFmpeg**: Available for all platforms through standard package managers

### Platform-Specific Differences

| Feature | Windows | macOS | Linux |
|---------|---------|-------|-------|
| Launcher | `run.bat` | `run.sh` | `run.sh` |
| FFmpeg Install | PowerShell script | `brew install` | Package manager |
| File Explorer | `os.startfile()` | `open` | `xdg-open` |
| Python Command | `python` | `python3` | `python3` |

---

**Have fun organizing your movie collection!** 🎬
