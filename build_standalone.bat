@echo off
REM Build standalone Windows executable for Moovy

echo.
echo ====================================================
echo Building Moovy - Windows Standalone Executable
echo ====================================================
echo.

REM Check if venv exists
if not exist ".venv" (
    echo Error: Virtual environment not found!
    echo Please run: run.bat first
    pause
    exit /b 1
)

REM Activate virtual environment
call .venv\Scripts\activate.bat

echo Cleaning previous builds...
if exist "build" rmdir /s /q build
if exist "dist" rmdir /s /q dist
if exist "*.spec.bak" del *.spec.bak

echo.
echo Building standalone executable...
echo This may take a few minutes...
echo.

REM Build using PyInstaller with spec file
.venv\Scripts\pyinstaller.exe Moovy.spec

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ====================================================
    echo Build FAILED!
    echo ====================================================
    pause
    exit /b 1
)

echo.
echo ====================================================
echo Build SUCCESSFUL!
echo ====================================================
echo.
echo Executable location:
echo   %CD%\dist\Moovy\Moovy.exe
echo.
echo To run the application:
echo   1. Copy the entire 'dist\Moovy' folder to desired location
echo   2. Double-click Moovy.exe to launch
echo.
echo NOTE: The application requires FFmpeg to be installed
echo On Windows, you can install it using:
echo   - winget install ffmpeg
echo   - scoop install ffmpeg
echo   - choco install ffmpeg
echo.
pause
