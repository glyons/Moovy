# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller spec file for macOS Moovy application bundle."""

import sys
import os

# Ensure we're using correct path separators for current OS
src_main = os.path.join('src', 'main.py')
icons_src = os.path.join('src', 'icons')
icons_dest = os.path.join('src', 'icons')

a = Analysis(
    [src_main],
    pathex=[],
    binaries=[],
    datas=[(icons_src, icons_dest)],
    hiddenimports=['PyQt6.QtSvg'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludedimports=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure, a.zipped_data)

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
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=os.path.join('src', 'icons', 'icon.ico'),
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Moovy.app',
)

info_plist = {
    'NSPrincipalClass': 'NSApplication',
}

app = BUNDLE(
    coll,
    name='Moovy.app',
    icon=os.path.join('src', 'icons', 'icon.ico'),
    bundle_identifier='com.moovy.app',
    info_plist=info_plist,
)
