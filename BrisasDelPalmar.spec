# -*- mode: python ; coding: utf-8 -*-
import os
import customtkinter
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

block_cipher = None

ctk_path = os.path.dirname(customtkinter.__file__)

datas = [
    (ctk_path, 'customtkinter'),
    ('assets', 'assets'),
    (os.path.join('database', 'schema.sql'), 'database'),
    (os.path.join('database', 'seeds.sql'), 'database'),
]

# Recolectar recursos adicionales de reportlab si existen
datas += collect_data_files('reportlab')

hiddenimports = [
    'PIL._tkinter_finder',
    'customtkinter',
    'darkdetect',
    'openpyxl',
    'reportlab',
    'sqlite3',
    'tkinter',
    'tkinter.ttk',
    'tkinter.messagebox',
    'tkinter.filedialog',
]
hiddenimports += collect_submodules('reportlab.graphics.barcode')

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['unittest', 'test'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='BrisasDelPalmar',
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
    icon=os.path.join('assets', 'icono_empresa.ico'),
)

