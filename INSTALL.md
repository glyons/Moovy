# Installation Guide - Moovy

This guide provides step-by-step instructions to install and run Moovy on Windows, macOS, and Linux.

---

## 🪟 Windows

### Quick Start (Recommended)
1. Double-click **`run.bat`** in the project folder
2. The script will automatically:
   - Create virtual environment
   - Install dependencies
   - Check for FFmpeg
   - Launch Moovy

### Manual Setup

#### Step 1: Install FFmpeg

**Option A: Automated Script**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\setup_ffmpeg.ps1
```

**Option B: Chocolatey** (if installed)
```powershell
choco install ffmpeg
```

**Option C: Winget** (Windows 11+)
```powershell
winget install ffmpeg
```

**Option D: Manual**
- Download from: https://ffmpeg.org/download.html
- Extract to `C:\FFmpeg\bin`
- Add `C:\FFmpeg\bin` to Path environment variable

#### Step 2: Install Python Dependencies
```powershell
# Create virtual environment
python -m venv .venv

# Activate virtual environment
.venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

#### Step 3: Run Moovy
```powershell
python -m src.main
```

### Troubleshooting

**"FFmpeg not found"**
```powershell
ffmpeg -version  # Check if installed
.\setup_ffmpeg.ps1  # Install it
```

**"Python not found"**
- Download from: https://www.python.org/downloads/
- During installation, check "Add Python to PATH"

---

## 🍎 macOS

### Quick Start (Recommended)
1. Open Terminal in the project folder
2. Run:
   ```bash
   chmod +x run.sh
   ./run.sh
   ```
3. Moovy will launch automatically

### Manual Setup

#### Step 1: Install Homebrew (if not already installed)
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

#### Step 2: Install FFmpeg
```bash
brew install ffmpeg
```

Or use the automated script:
```bash
chmod +x setup_ffmpeg.sh
./setup_ffmpeg.sh
```

#### Step 3: Install Python Dependencies
```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate

# Install packages
pip install -r requirements.txt
```

#### Step 4: Run Moovy
```bash
python3 -m src.main
```

### Troubleshooting

**"FFmpeg not found"**
```bash
ffmpeg -version  # Check if installed
brew install ffmpeg  # Install it
```

**"Python not found"**
```bash
brew install python3
```

**"Permission denied" on scripts**
```bash
chmod +x run.sh
chmod +x setup_ffmpeg.sh
```

---

## 🐧 Linux

### Quick Start (Recommended)
1. Open Terminal in the project folder
2. Run:
   ```bash
   chmod +x run.sh
   ./run.sh
   ```
3. Moovy will launch automatically

### Manual Setup

#### Step 1: Install FFmpeg

**Ubuntu / Debian:**
```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

**Fedora / RHEL:**
```bash
sudo dnf install ffmpeg
```

**Arch Linux:**
```bash
sudo pacman -S ffmpeg
```

**Alpine Linux:**
```bash
sudo apk add ffmpeg
```

Or use the automated script:
```bash
chmod +x setup_ffmpeg.sh
./setup_ffmpeg.sh
```

#### Step 2: Install Python3
Most Linux distributions come with Python3 pre-installed. If not:

**Ubuntu / Debian:**
```bash
sudo apt-get install python3 python3-venv
```

**Fedora:**
```bash
sudo dnf install python3
```

**Arch:**
```bash
sudo pacman -S python
```

#### Step 3: Install Python Dependencies
```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate

# Install packages
pip install -r requirements.txt
```

#### Step 4: Run Moovy
```bash
python3 -m src.main
```

### Troubleshooting

**"FFmpeg not found"**
```bash
ffmpeg -version  # Check if installed
```

Install based on your distribution (see Step 1 above)

**"Python3 not found"**
See Step 2 above for your distribution

**"Permission denied" on scripts**
```bash
chmod +x run.sh
chmod +x setup_ffmpeg.sh
```

---

## ✅ Verify Installation

After installation, verify everything is working:

```bash
# Check Python
python --version        # Windows
python3 --version       # macOS/Linux

# Check FFmpeg
ffmpeg -version

# Check PyQt6 installation
python -c "import PyQt6.QtWidgets; print('PyQt6 OK')"
```

---

## 📋 System Requirements Summary

| Component | Windows | macOS | Linux |
|-----------|---------|-------|-------|
| Python | 3.8+ | 3.8+ | 3.8+ |
| FFmpeg | Latest | Latest | Latest |
| PyQt6 | 6.10+ | 6.10+ | 6.10+ |
| OS Version | 7+ | 10.13+ | Modern distro |

---

## 🚀 Launching Moovy

### Windows
- Double-click **`run.bat`**, or
- From PowerShell: `python -m src.main`

### macOS / Linux
- Terminal: `./run.sh` (after `chmod +x run.sh`), or
- Terminal: `python3 -m src.main`

---

## 📝 Virtual Environment

All platforms use Python virtual environments to isolate dependencies:

**Windows:**
```powershell
.venv\Scripts\activate      # Activate
.venv\Scripts\deactivate    # Deactivate
```

**macOS/Linux:**
```bash
source .venv/bin/activate   # Activate
deactivate                  # Deactivate
```

To reset:
```bash
# Windows
rmdir /s .venv

# macOS/Linux
rm -rf .venv
```

Then recreate and reinstall:
```bash
python -m venv .venv        # Windows
python3 -m venv .venv       # macOS/Linux

# Activate and install
pip install -r requirements.txt
```

---

## 🆘 Getting Help

1. **Check FFmpeg is in PATH:**
   ```bash
   ffmpeg -version
   ffprobe -version
   ```

2. **Check Python installation:**
   ```bash
   python --version
   python3 --version
   ```

3. **Check virtual environment:**
   - Ensure it's activated (should see `(.venv)` in terminal)
   - Reinstall dependencies: `pip install -r requirements.txt`

4. **Check file paths:**
   - Ensure project path doesn't have special characters or spaces

---

**Enjoy using Moovy!** 🎬
