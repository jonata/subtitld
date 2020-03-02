# -*- mode: python -*-

a = Analysis(['subtitld.py'],
    pathex=['/Users/admin/Documents/subtitld', 'C:\Python36\Lib\site-packages\scipy\extra-dll'],
    binaries=[],
    datas=[
        ( 'graphics/*.png', 'graphics' ),
        ( 'ffmpeg-latest-win64-static/bin/ffmpeg.exe', '.'),
    ],
    hiddenimports=[],
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

coll = COLLECT( exe,
                a.binaries,
                a.zipfiles,
                a.datas,
                strip=False,
                upx=True,
                name='Subtitld')
