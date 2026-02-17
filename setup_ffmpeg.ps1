# FFmpeg Setup Script for Windows
# Install FFmpeg using available methods

Write-Host "`nFFmpeg Installation Script`n" -ForegroundColor Cyan

# Check if already installed
$FFmpeg = Get-Command ffmpeg -ErrorAction SilentlyContinue
if ($FFmpeg) {
    Write-Host "FFmpeg is already installed" -ForegroundColor Green
    & ffmpeg -version | Select-Object -First 1
    exit 0
}

Write-Host "Installation methods:" -ForegroundColor Yellow
Write-Host "1. Winget (Windows 11):  winget install ffmpeg" -ForegroundColor White
Write-Host "2. Scoop:                scoop install ffmpeg" -ForegroundColor White
Write-Host "3. Chocolatey:           choco install ffmpeg" -ForegroundColor White
Write-Host "4. Manual:               https://ffmpeg.org/download.html" -ForegroundColor White
Write-Host "`nAttempting automatic installation..." -ForegroundColor Cyan

# Try winget first
try {
    Write-Host "Trying winget..." -ForegroundColor Yellow
    $result = winget install ffmpeg --silent --accept-package-agreements --accept-source-agreements 2>$null
    if ($?) {
        Write-Host "Successfully installed with winget" -ForegroundColor Green
        $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
        $FFmpeg = Get-Command ffmpeg -ErrorAction SilentlyContinue
        if ($FFmpeg) {
            & ffmpeg -version | Select-Object -First 1
            exit 0
        }
    }
}
catch {
    Write-Host "Winget not available" -ForegroundColor Gray
}

# Try Chocolatey
try {
    Write-Host "Trying Chocolatey..." -ForegroundColor Yellow
    $result = choco install ffmpeg -y 2>$null
    if ($?) {
        Write-Host "Successfully installed with Chocolatey" -ForegroundColor Green
        $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
        $FFmpeg = Get-Command ffmpeg -ErrorAction SilentlyContinue
        if ($FFmpeg) {
            & ffmpeg -version | Select-Object -First 1
            exit 0
        }
    }
}
catch {
    Write-Host "Chocolatey not available" -ForegroundColor Gray
}

# Manual installation message
Write-Host "`nAutomatic installation failed." -ForegroundColor Yellow
Write-Host "Please install FFmpeg manually:" -ForegroundColor White
Write-Host "  1. Download from https://ffmpeg.org/download.html" -ForegroundColor White
Write-Host "  2. Extract to C:\FFmpeg" -ForegroundColor White
Write-Host "  3. Add C:\FFmpeg\bin to your system PATH" -ForegroundColor White
Write-Host "  4. Restart PowerShell" -ForegroundColor White
Write-Host "`nSetup `n" -ForegroundColor Cyan

