# -*- mode: python -*-

VERSION = '20.07.0.0'
if 'VERSION_NUMBER' in [*os.environ] and not os.environ['VERSION_NUMBER'] == '':
    VERSION = os.environ['VERSION_NUMBER']

block_cipher = None

#                     ( '/usr/local/lib/python3.6/dist-packages/ftfy/char_classes.dat', 'ftfy' ),

a = Analysis(['subtitld.py'],
             pathex=['/home/jonata/Projetos/subtitld'],
             binaries=[],
             datas=[
                     ( 'graphics/*.png', 'graphics' ),
                     ( 'graphics/*.svg', 'graphics' ),
                     ( 'graphics/*.ttf', 'graphics' ),
                     ( 'ftfy/char_classes.dat', 'ftfy' ),
                 ],
             hiddenimports=['sip',
                            '_cffi_backend',
                            'cleantext',
                            'scc2srt',
                            'pysubs2',
                            'autosub',
                            'googleapiclient'
                            'ffsubsync'],
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
