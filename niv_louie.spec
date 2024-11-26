# -*- mode: python ; coding: utf-8 -*-

import os
import site


# Find site-packages directory
site_packages=os.path.join(site.getsitepackages()[0],"Lib","site-packages")

a = Analysis(
    ['gui.py'],
    pathex=[],
    binaries=[],
    datas=[
        (os.path.join(site_packages,'nicegui'), 'nicegui'),
        (os.path.join(site_packages,'pandas'), 'pandas'),
        (os.path.join(site_packages,'docx'), 'docx'),
        (os.path.join(site_packages,'webview'), 'webview'),
        ('utils/braille_test_converter.json','utils'),
        ('utils/braille_converter.json','utils'),
        ('utils/braille_to_numbers.json','utils'),
        ('utils/extentions_file.json','utils'),
        ('utils/languages_file.json','utils')
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='niv_louie',
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
)
