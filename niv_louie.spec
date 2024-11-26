# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['gui.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('.venv/Lib/site-packages/nicegui', 'nicegui'),
        ('.venv/Lib/site-packages/pandas', 'pandas'),
        ('.venv/Lib/site-packages/docx', 'docx'),
        ('.venv/Lib/site-packages/webview', 'webview'),
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
