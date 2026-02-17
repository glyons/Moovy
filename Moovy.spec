# -*- mode: python ; coding: utf-8 -*-

import sys
from pathlib import Path

# Get the path to the current Python installation
python_path = Path(sys.executable).parent.parent

a = Analysis(
    ['src\\main.py'],
    pathex=[str(python_path / 'Lib' / 'site-packages')],
    binaries=[],
    datas=[('src/icons', 'src/icons')],
    hiddenimports=[
        'PyQt6',
        'PyQt6.QtCore',
        'PyQt6.QtGui',
        'PyQt6.QtWidgets',
        'PyQt6.QtPrintSupport',
        'PyQt6.sip',
        'pathlib',
        'threading',
        'subprocess',
        'platform',
        'string',
        'logging',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['matplotlib', 'numpy', 'scipy', 'pandas', 'sklearn', 'tcl', 'tk'],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Moovy',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['src\\icons\\icon.ico'],
)
