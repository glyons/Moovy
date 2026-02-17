@echo off
REM Build standalone one-file Windows executable for Moovy (requires more time/resources)

echo.
echo ====================================================
echo Building Moovy - One-File Executable
echo ====================================================
echo.
echo NOTE: This creates a single .exe file but may take
echo longer to build and start. Use build_standalone.bat
echo for a faster, more standard distribution.
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

echo.
echo Building standalone one-file executable...
echo This will take several minutes...
echo.

REM Build using PyInstaller with --onefile and comprehensive dependencies
.venv\Scripts\pyinstaller.exe --onefile ^
    --name Moovy ^
    --icon=src/icons/icon.ico ^
    --add-data "src/icons;src/icons" ^
    --windowed ^
    --noupx ^
    --collect-all PyQt6 ^
    --hidden-import=PyQt6.QtCore ^
    --hidden-import=PyQt6.QtGui ^
    --hidden-import=PyQt6.QtWidgets ^
    --hidden-import=PyQt6.sip ^
    src/main.py

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
echo   %CD%\dist\Moovy.exe
echo.
echo You can distribute this single executable file.
echo.
echo NOTE: The application requires FFmpeg to be installed
echo.
pause
