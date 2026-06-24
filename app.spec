# -*- mode: python ; coding: utf-8 -*-

import sys
import os

block_cipher = None

added_files = []
if os.path.exists('docs'):
    added_files.append(('docs', 'docs'))
if os.path.exists('.streamlit'):
    added_files.append(('.streamlit', '.streamlit'))

a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=[],
    datas=added_files,
    hiddenimports=[
        'streamlit',
        'langchain',
        'langchain_core',
        'langchain_community',
        'langchain_chroma',
        'langchain_ollama',
        'chromadb',
        'PyPDF2',
        'docx',
        'tiktoken',
        'ollama',
        'numpy',
        'pandas',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.symbols, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='RAG-QA-System',
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
    icon=None,
)
