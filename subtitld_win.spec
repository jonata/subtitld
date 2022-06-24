# -*- mode: python -*-

VERSION = '20.07.0.0'
if 'VERSION_NUMBER' in [*os.environ] and not os.environ['VERSION_NUMBER'] == '':
    VERSION = os.environ['VERSION_NUMBER']

a = Analysis(['subtitld/__main__.py'],
    pathex=['/Users/admin/Documents/subtitld', 'C:\Python36\Lib\site-packages\scipy\extra-dll'],
    excludes=['FixTk', 'tcl', 'tk', '_tkinter', 'tkinter', 'Tkinter'],
    binaries=[
        ( 'resources/mpv-1.dll', '.'),
    ],
    datas=[
        ( 'subtitld/graphics/*', 'graphics' ),
        ( 'ffmpeg-*/bin/ffmpeg.exe', '.'),
        ( 'ffmpeg-*/bin/ffprobe.exe', '.'),
        ( 'subtitld/ftfy/char_classes.dat', 'ftfy' ),
        ( 'c:/python39/Scripts/ffms2.dll', '.'),
        ( 'c:/python39/Scripts/ffms2.lib', '.'),
        ( 'c:/python39/lib/site-packages/glfw/glfw3.dll', '.'),
    ],
    hiddenimports=[
        'ffms2',
        'pythoncom'
    ],
    hookspath=[],
    runtime_hooks=[] )

pyz = PYZ(a.pure)

exe = EXE(pyz,
    a.scripts,
    exclude_binaries=True,
    name='Subtitld.exe',
    strip=False,
    upx=True,
    console=False,
    debug=False,
    icon='subtitld/graphics/subtitld.ico' )

coll = COLLECT( exe,
                a.binaries,
                a.zipfiles,
                a.datas,
                strip=False,
                upx=True,
                name='Subtitld')

open('dist/subtitld/current_version', mode='w', encoding='utf-8').write(VERSION)
