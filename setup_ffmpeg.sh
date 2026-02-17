#!/bin/bash
# FFmpeg Setup Script for macOS and Linux

echo ""
echo "========================================"
echo " FFmpeg Installation Script"
echo "========================================"
echo ""

# Detect OS
if [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macOS"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="Linux"
else
    echo "❌ Unsupported operating system: $OSTYPE"
    exit 1
fi

echo "Detected OS: $OS"
echo ""

if [ "$OS" = "macOS" ]; then
    # Check if Homebrew is installed
    if ! command -v brew &> /dev/null; then
        echo "❌ Homebrew is not installed!"
        echo ""
        echo "Please install Homebrew first:"
        echo "  /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
        exit 1
    fi
    
    echo "Installing FFmpeg via Homebrew..."
    brew install ffmpeg
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "✓ FFmpeg installed successfully!"
        ffmpeg -version | head -n 1
    else
        echo "❌ Failed to install FFmpeg"
        exit 1
    fi

elif [ "$OS" = "Linux" ]; then
    # Detect Linux distribution
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        DISTRO=$ID
    else
        echo "❌ Unable to detect Linux distribution"
        exit 1
    fi
    
    echo "Detected Linux distribution: $DISTRO"
    echo ""
    
    case $DISTRO in
        ubuntu|debian)
            echo "Installing FFmpeg via apt..."
            sudo apt-get update
            sudo apt-get install -y ffmpeg
            ;;
        fedora)
            echo "Installing FFmpeg via dnf..."
            sudo dnf install -y ffmpeg
            ;;
        rhel|centos)
            echo "Installing FFmpeg via yum..."
            sudo yum install -y ffmpeg
            ;;
        arch|manjaro)
            echo "Installing FFmpeg via pacman..."
            sudo pacman -S --noconfirm ffmpeg
            ;;
        alpine)
            echo "Installing FFmpeg via apk..."
            sudo apk add ffmpeg
            ;;
        *)
            echo "❌ Unsupported distribution: $DISTRO"
            echo ""
            echo "Please install FFmpeg manually using your package manager:"
            echo "  - apt-get (Debian/Ubuntu)"
            echo "  - dnf (Fedora)"
            echo "  - pacman (Arch)"
            echo "  - apk (Alpine)"
            echo "  - brew (macOS)"
            echo ""
            echo "Or download from: https://ffmpeg.org/download.html"
            exit 1
            ;;
    esac
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "✓ FFmpeg installed successfully!"
        ffmpeg -version | head -n 1
    else
        echo "❌ Failed to install FFmpeg"
        exit 1
    fi
fi

echo ""
echo "✓ FFmpeg setup complete!"
echo ""
echo "You can now run: python3 -m src.main"
echo "Or: ./run.sh"
echo ""
