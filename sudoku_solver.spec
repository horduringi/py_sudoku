# -*- mode: python -*-

block_cipher = None


a = Analysis(['sudoku_solver.py'],
             pathex=['/Users/hordur/Dev/Qlik/py_sudoku'],
             binaries=None,
             datas=[('easy.txt',    '.'),
                    ('medium.txt',  '.'),
                    ('hard.txt',    '.'),
                    ('samurai.txt', '.')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='sudoku_solver',
          debug=False,
          strip=False,
          upx=True,
          console=True )
