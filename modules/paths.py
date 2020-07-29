#!/usr/bin/env python3

import os
import sys
import tempfile
import random
import subprocess

PATH_SUBTITLD = os.path.abspath(os.path.dirname(sys.argv[0]))
PATH_SUBTITLD_GRAPHICS = os.path.join(PATH_SUBTITLD, 'graphics')

PATH_HOME = os.path.expanduser("~")
REAL_PATH_HOME = PATH_HOME

FFMPEG_EXECUTABLE = 'ffmpeg'
FFPROBE_EXECUTABLE = 'ffprobe'

STARTUPINFO = None

ACTUAL_OS = 'linux'

path_tmp = os.path.join(tempfile.gettempdir(), 'subtitld-' + str(random.randint(1000, 9999)))
if sys.platform == 'darwin':
    ACTUAL_OS = 'macos'
    PATH_SUBTITLD_USER_CONFIG = os.path.join(PATH_HOME, 'Library', 'Application Support', 'subtitld')
    FFMPEG_EXECUTABLE = os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), 'ffmpeg')
    FFPROBE_EXECUTABLE = os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), 'ffprobe')
    try:
        from Foundation import NSURL
    except ImportError:
        sys.path.append('/System/Library/Frameworks/Python.framework/Versions/2.7/Extras/lib/python/PyObjC')
        from Foundation import NSURL
elif sys.platform == 'win32' or os.name == 'nt':
    ACTUAL_OS = 'windows'
    PATH_SUBTITLD_USER_CONFIG = os.path.join(os.getenv('LOCALAPPDATA'), 'subtitld')
    FFMPEG_EXECUTABLE = os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), 'ffmpeg.exe')
    FFPROBE_EXECUTABLE = os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), 'ffprobe.exe')
    STARTUPINFO = subprocess.STARTUPINFO()
    STARTUPINFO.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    STARTUPINFO.wShowWindow = subprocess.SW_HIDE
else:
    REAL_PATH_HOME = subprocess.Popen(['getent', 'passwd', str(os.getuid())], stdout=subprocess.PIPE).stdout.read().decode().split(':')[5]
    if not os.path.isdir(os.path.join(PATH_HOME, '.config')):
        os.mkdir(os.path.join(PATH_HOME, '.config'))
    PATH_SUBTITLD_USER_CONFIG = os.path.join(PATH_HOME, '.config', 'subtitld')

PATH_SUBTITLD_DATA_BACKUP = os.path.join(PATH_SUBTITLD_USER_CONFIG, 'backup')
PATH_SUBTITLD_DATA_AUTH = os.path.join(PATH_SUBTITLD_USER_CONFIG, 'authentications')

os.mkdir(path_tmp)

if not os.path.isdir(PATH_SUBTITLD_USER_CONFIG):
    os.mkdir(PATH_SUBTITLD_USER_CONFIG)

if not os.path.isdir(PATH_SUBTITLD_DATA_BACKUP):
    os.mkdir(PATH_SUBTITLD_DATA_BACKUP)

if not os.path.isdir(PATH_SUBTITLD_DATA_AUTH):
    os.mkdir(PATH_SUBTITLD_DATA_AUTH)

PATH_SUBTITLD_USER_CONFIG_FILE = os.path.join(PATH_SUBTITLD_USER_CONFIG, 'subtitld.config')


def get_graphics_path(filename):
    final_path = os.path.join(PATH_SUBTITLD_GRAPHICS, filename)
    if sys.platform == 'win32' or os.name == 'nt':
        final_path = final_path.replace('\\', '/')
    return final_path


VERSION_NUMBER = '20.07.0.0'
if os.path.isfile(os.path.join(PATH_SUBTITLD, 'current_version')):
    VERSION_NUMBER = open(os.path.join(PATH_SUBTITLD, 'current_version')).read().strip()

LIST_OF_SUPPORTED_VIDEO_EXTENSIONS = (('.mp4', '.mkv', '.mov', '.mpg', '.webm', '.ogv'))

LIST_OF_SUPPORTED_SUBTITLE_EXTENSIONS = {
    'SRT': {'description': 'SubRip Subtitle format', 'extensions': ['srt']},
    'DFXP': {'description': 'Subtitle format', 'extensions': ['ttml', 'dfxp']},
    'SAMI': {'description': 'Subtitle format', 'extensions': ['smi', 'sami']},
    'SCC': {'description': 'Subtitle format', 'extensions': ['scc']},
    'VTT': {'description': 'Subtitle format', 'extensions': ['webvtt', 'vtt']},
    'ASS': {'description': 'SubStation Alpha Subtitle format', 'extensions': ['ass', 'ssa']},
    'SBV': {'description': 'Subtitle format', 'extensions': ['sbv']},
    'SUB': {'description': 'MicroDVD Subtitle format', 'extensions': ['sub']},
    'XML': {'description': 'Subtitle format', 'extensions': ['xml']}
}

LIST_OF_SUPPORTED_IMPORT_EXTENSIONS = {
    'TXT': {'description': 'Simple TXT file', 'extensions': ['txt']}
}
