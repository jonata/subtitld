# -*- mode: python -*-

from PyInstaller.utils.hooks import copy_metadata
print(copy_metadata('google-api-python-client'))

VERSION = '20.07.0.0'
if 'VERSION_NUMBER' in [*os.environ] and not os.environ['VERSION_NUMBER'] == '':
    VERSION = os.environ['VERSION_NUMBER']

a = Analysis(['subtitld.py'],
    pathex=['/Users/admin/Documents/subtitld', 'C:\Python36\Lib\site-packages\scipy\extra-dll'],
    excludes=['FixTk', 'tcl', 'tk', '_tkinter', 'tkinter', 'Tkinter'],
    binaries=[
        ( 'mpv/x86_64/mpv-1.dll', '.')
    ],
    datas=[
        copy_metadata('google-api-python-client'),
        ( 'graphics/*.png', 'graphics' ),
        ( 'graphics/*.ttf', 'graphics' ),
        ( 'ffmpeg-*/bin/ffmpeg.exe', '.'),
        ( 'ffmpeg-*/bin/ffprobe.exe', '.'),
        ( 'ftfy/char_classes.dat', 'ftfy' ),
    ],
    hiddenimports=['_cffi_backend',
                   'cleantext',
                   'scc2srt',
                   'pysubs2',
                   'ftfy',
                   'autosub'],
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
    icon='graphics/subtitld.ico' )

exe_cmd = EXE(pyz,
    a.scripts,
    exclude_binaries=True,
    name='Subtitldc.exe',
    strip=False,
    upx=True,
    console=True,
    debug=True,
    icon='graphics/subtitld.ico' )

coll = COLLECT( exe, exe_cmd,
                a.binaries,
                a.zipfiles,
                a.datas,
                strip=False,
                upx=True,
                name='Subtitld')

open('dist/subtitld/current_version', mode='w', encoding='utf-8').write(VERSION)
