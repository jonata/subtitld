#######################################################################
#
# Subtitld setup.py
#
#######################################################################

import os
import sys
import pydoc

from setuptools import setup, find_packages

import subtitld


def get_description(filename='README.md'):
    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), filename), encoding='utf-8') as f:
        file = list(f)
    desc = ''
    for item in file[11: len(file)]:
        desc += item
    return desc


def get_data_files():
    files = []
    if sys.platform.startswith('linux') and 'QT_APPIMAGE' not in os.environ.keys():
        # appid = subtitld.__desktopid__
        files = [
            # ('share/icons/hicolor/16x16/apps', ['data/icons/hicolor/16x16/apps/{}.png'.format(appid)]),
            # ('share/icons/hicolor/16x16/apps', ['data/icons/hicolor/16x16/apps/{}.png'.format(appid)]),
            # ('share/icons/hicolor/22x22/apps', ['data/icons/hicolor/22x22/apps/{}.png'.format(appid)]),
            # ('share/icons/hicolor/24x24/apps', ['data/icons/hicolor/24x24/apps/{}.png'.format(appid)]),
            # ('share/icons/hicolor/32x32/apps', ['data/icons/hicolor/32x32/apps/{}.png'.format(appid)]),
            # ('share/icons/hicolor/48x48/apps', ['data/icons/hicolor/48x48/apps/{}.png'.format(appid)]),
            # ('share/icons/hicolor/64x64/apps', ['data/icons/hicolor/64x64/apps/{}.png'.format(appid)]),
            # ('share/icons/hicolor/128x128/apps', ['data/icons/hicolor/128x128/apps/{}.png'.format(appid)]),
            # ('share/icons/hicolor/256x256/apps', ['data/icons/hicolor/256x256/apps/{}.png'.format(appid)]),
            # ('share/icons/hicolor/512x512/apps', ['data/icons/hicolor/512x512/apps/{}.png'.format(appid)]),
            # ('share/icons/hicolor/scalable/apps', ['subtitld/graphics/subtitld.svg']),
            ('share/icons/hicolor/512x512/apps', ['subtitld/graphics/subtitld.png']),
            ('share/metainfo/org.subtitld.Subtitld.metainfo.xml', ['org.subtitld.Subtitld.metainfo.xml']),
            ('share/applications', ['subtitld.desktop']),
            # ('share/metainfo', ['data/appdata/{}.appdata.xml'.format(appid)]),
            # ('share/mime/packages', ['data/mime/{}.xml'.format(appid)]),
            # ('share/doc/subtitld', ['CHANGELOG', 'LICENSE', 'README.md'])
        ]

    return files


def get_package_files():
    files = {}

    files['subtitld'] = [
        'locale/*',
        'graphics/*',
    ]

    return files


def pip_notes():
    os.system('cls' if sys.platform == 'win32' else 'clear')
    pydoc.pager('''
    If installing via PyPi (Python Pip) on Linux then you need to know that subtitld
    depends on the following packages and distros. Install using your distro's
    software packager for a noticeably better integrated experience.

        ---[Ubuntu/Debian/Mint/etc]--------------------------

            python3-dev libmpv1 libmpv-dev python3-pyqt5
            python3-pyqt5.qtopengl python3-pyqt5.qtx11extras
            ffmpeg mediainfo python3-opengl

        ---[Arch Linux]--------------------------------------

            python mpv python-pyqt5 ffmpeg mediainfo

        ---[Fedora]------------------------------------------

            python3-devel mpv-libs mpv-libs-devel python3-qt5
            ffmpeg mediainfo python3-pyopengl

        ---[openSUSE]----------------------------------------

            python3-devel libmpv1 mpv-devel python3-qt5
            ffmpeg mediainfo

    You need to build a Python extension module before you can run the
    app directly from source code. This is done for you automatically by
    the package installers but if you wish to simply run the app direct
    from source without having to install it (i.e. python3 setup.py install)
    you can do so by building the extension module with the following
    setuptools command, run from the top-most extracted source code folder:

        $ python3 setup.py build_ext -i

    And to then run the app directly from source, from the same top-most
    source code folder:

        $ python3 -m subtitld

    To view all console output for debugging or general interest then
    append the debug parameter:

        $ python3 -m subtitld --debug

    Make sure you build the extension module AFTER installing the
    dependencies covered above, in particular libmpv and the mpv + python3
    dev headers are all needed for it to compile successfully. Compiled
    extension modules under subtitld/libs will look like:

        mpv.cpython-36m-x86_64-linux-gnu.so [linux]
        mpv.cp36-win_amd64.pyd              [win32]


    Get more information on:

    https://subtitld.org
''')


# --------------------------------------------------------------------------- #

setup_requires = ['setuptools']
install_requires = [
    'PySide6==6.4.0',
    'pyopengl',
    'python-mpv==0.5.2',
    'ffms2',
    'numpy',
    'cffi',
    'requests',
    'pycaption',
    # 'captionstransformer @ git+ssh://git@github.com/toutpt/captionstransformer',
    'pysubs2',
    'clean-text[gpl]',
    'html5lib==1.0b8',
    # 'scenedetect',
    # 'opencv-python',
    # 'autosub3',
    'translate',
    'SpeechRecognition',
    'beautifulsoup4<4.10,>=4.8.1',
    'python-docx',
    'chardet',
    'google-api-python-client',
    'pysrt',
    'certifi',
    'python-i18n',
    'google-cloud-core'
]

# --------------------------------------------------------------------------- #

try:
    # begin setuptools installer
    result = setup(
        app=['subtitld/__main__.py'],
        name=subtitld.__appname__.lower(),
        version=subtitld.__version__,
        author=subtitld.__author__,
        author_email=subtitld.__email__,
        description='Subtitld',
        long_description=get_description(),
        url=subtitld.__website__,
        license='GPL3',
        packages=find_packages(include=['subtitld', 'subtitld.*']),
        setup_requires=setup_requires,
        install_requires=install_requires,
        data_files=get_data_files(),
        package_data=get_package_files(),
        include_package_data=True,
        entry_points={'gui_scripts': ['subtitld = subtitld.__main__:main']},
        keywords='subtitld',
        classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Environment :: X11 Applications :: Qt',
            'Intended Audience :: End Users/Desktop',
            'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
            'Natural Language :: English',
            'Operating System :: POSIX',
            'Topic :: Multimedia',
            'Programming Language :: Python :: 3 :: Only'
        ],
        options={'py2app': {
            'argv_emulation': True,
            # 'iconfile': 'src/Icon.icns',  # optional
            # 'plist': 'src/Info.plist',    # optional
        }},
    )
except BaseException:
    if subtitld.__ispypi__:
        pip_notes()
    raise
