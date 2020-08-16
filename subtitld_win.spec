# -*- mode: python -*-

VERSION = '20.07.0.0'
if 'VERSION_NUMBER' in [*os.environ] and not os.environ['VERSION_NUMBER'] == '':
    VERSION = os.environ['VERSION_NUMBER']

a = Analysis(['subtitld.py'],
    pathex=['/Users/admin/Documents/subtitld', 'C:\Python36\Lib\site-packages\scipy\extra-dll'],
    binaries=[
        ( 'mpv/x86_64/mpv-1.dll', '.')
    ],
    datas=[
        ( 'graphics/*.png', 'graphics' ),
        ( 'graphics/*.ttf', 'graphics' ),
        ( 'ffmpeg-latest-win64-static/bin/ffmpeg.exe', '.'),
        ( 'ffmpeg-latest-win64-static/bin/ffprobe.exe', '.'),
        ( 'ftfy/char_classes.dat', 'ftfy' ),
    ],
    hiddenimports=['_cffi_backend', 'cleantext', 'scc2srt', 'pysubs2', 'ftfy'],
    hookspath=[],
    runtime_hooks=[] )

pyz = PYZ(a.pure)

exe = EXE(pyz,
    a.scripts,
    exclude_binaries=True,
    name='Subtitld.exe',
    strip=False,
    upx=True,
    console=True,
    debug=True,
    icon='graphics/subtitld.ico' )

coll = COLLECT( exe,
                a.binaries,
                a.zipfiles,
                a.datas,
                strip=False,
                upx=True,
                name='Subtitld')

open('dist/subtitld/current_version', mode='w', encoding='utf-8').write(VERSION)
