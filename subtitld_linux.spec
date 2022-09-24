# -*- mode: python -*-
import os

VERSION = '20.07.0.0'
if 'VERSION_NUMBER' in [*os.environ] and not os.environ['VERSION_NUMBER'] == '':
    VERSION = os.environ['VERSION_NUMBER']

block_cipher = None

#                     ( '/usr/local/lib/python3.6/dist-packages/ftfy/char_classes.dat', 'ftfy' ),

a = Analysis(['subtitld/__main__.py'],
             pathex=[],
             binaries=[
                #  ('/usr/lib/x86_64-linux-gnu/libmpv.so', '.'),
                #  ('/usr/lib/x86_64-linux-gnu/libxcb.so.1', '.'),
                #  ('/usr/lib/x86_64-linux-gnu/libxcb-icccm.so.4', '.'),
                #  ('/usr/lib/x86_64-linux-gnu/libxcb-image.so.0', '.'),
                #  ('/usr/lib/x86_64-linux-gnu/libxcb-keysyms.so.1', '.'),
                #  ('/usr/lib/x86_64-linux-gnu/libxcb-render-util.so.0', '.'),
                #  ('/usr/lib/x86_64-linux-gnu/libxcb-xinerama.so.0', '.'),
                #  ('/usr/lib/x86_64-linux-gnu/libxcb-xkb.so.1', '.'),
                #  ('/usr/lib/x86_64-linux-gnu/libxkbcommon-x11.so.0', '.'),
                #  ('/usr/lib/x86_64-linux-gnu/libdrm.so.2', '.'),
                #  ('/usr/lib/x86_64-linux-gnu/libavresample.so.4', '.'),
                #  ('/usr/bin/ffmpeg', '.'),
                #  ('/usr/bin/ffprobe', '.'),
             ],
             datas=[
                     ( 'subtitld/graphics/*', 'graphics' ),
                     ( os.path.join(os.getenv('PYTHON_DIRECTORY'), '/Lib/site-packages/PySide6/plugins'), 'PySide6/plugins/')
                    #  ( 'subtitld/ftfy/char_classes.dat', 'ftfy' ),
                 ],
             hiddenimports=['PySide6'],
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
          exclude_binaries=True,
          name='subtitld',
          debug=False,
          strip=False,
          upx=True,
          console=True )

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='subtitld')

open('dist/subtitld/current_version', mode='w', encoding='utf-8').write(VERSION)
