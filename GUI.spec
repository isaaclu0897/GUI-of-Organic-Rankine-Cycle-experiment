# -*- mode: python ; coding: utf-8 -*-

import shutil
shutil.copyfile('config.json', '{0}/config.json'.format(DISTPATH))
shutil.copyfile('fig/500w_P&ID.png', '{0}/fig/500w_P&ID.png'.format(DISTPATH))

block_cipher = None


a = Analysis(['GUI.py'],
             pathex=['/home/wei/app/GUI-of-Organic-Rankine-Cycle-experiment'],
             binaries=[],
             datas=[],
             hiddenimports=[
                "PIL._tkinter_finder",
            ],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='GUI',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
