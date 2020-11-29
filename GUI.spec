# -*- mode: python ; coding: utf-8 -*-
# pyinstaller -F GUI.spec
print("copy file")
from shutil import copyfile, copytree, ignore_patterns, rmtree

copyfile('config.json', '{0}/config.json'.format(DISTPATH))
copytree('fig', '{0}/fig'.format(DISTPATH), ignore=ignore_patterns('*'))
copyfile('fig/500w_P&ID.png', '{0}/fig/500w_P&ID.png'.format(DISTPATH))

print("start to build")

block_cipher = None


a = Analysis(['GUI.py'],
             pathex=['.'],
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

print("end to build")

print("remove build")
rmtree("./build")
