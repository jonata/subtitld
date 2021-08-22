"""All path definitions for Subtitld"""

import os
import sys
import tempfile
import subprocess
import subtitld

PATH_SUBTITLD = os.path.dirname(subtitld.__file__)
PATH_LOCALE = os.path.join(PATH_SUBTITLD, 'locale')
PATH_SUBTITLD_GRAPHICS = os.path.join(PATH_SUBTITLD, 'graphics')

PATH_HOME = os.path.expanduser("~")
REAL_PATH_HOME = PATH_HOME

FFMPEG_EXECUTABLE = 'ffmpeg'
FFPROBE_EXECUTABLE = 'ffprobe'

STARTUPINFO = None

ACTUAL_OS = 'linux'

tempdir = tempfile.TemporaryDirectory()
path_tmp  = tempdir.name

if sys.platform == 'darwin':
    ACTUAL_OS = 'macos'
    PATH_SUBTITLD_USER_CONFIG = os.path.join(PATH_HOME, 'Library', 'Application Support', 'subtitld')
    FFMPEG_EXECUTABLE = os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), 'ffmpeg')
    FFPROBE_EXECUTABLE = os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), 'ffprobe')
    # try:
    #     from Foundation import NSURL
    # except ImportError:
    #     sys.path.append('/System/Library/Frameworks/Python.framework/Versions/2.7/Extras/lib/python/PyObjC')
    #     from Foundation import NSURL
elif sys.platform == 'win32' or os.name == 'nt':
    ACTUAL_OS = 'windows'
    PATH_SUBTITLD_USER_CONFIG = os.path.join(os.getenv('LOCALAPPDATA'), 'subtitld')
    FFMPEG_EXECUTABLE = os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), 'ffmpeg.exe')
    FFPROBE_EXECUTABLE = os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), 'ffprobe.exe')
    PATH_SUBTITLD_GRAPHICS = os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), 'graphics')
    STARTUPINFO = subprocess.STARTUPINFO()
    STARTUPINFO.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    STARTUPINFO.wShowWindow = subprocess.SW_HIDE
else:
    try:
        REAL_PATH_HOME = subprocess.Popen(['getente', 'passwd', str(os.getuid())], stdout=subprocess.PIPE).stdout.read().decode().split(':')[5]
    except FileNotFoundError:
        pass
    if not os.path.isdir(os.path.join(PATH_HOME, '.config')):
        os.mkdir(os.path.join(PATH_HOME, '.config'))
    PATH_SUBTITLD_USER_CONFIG = os.path.join(PATH_HOME, '.config', 'subtitld')

PATH_SUBTITLD_DATA_BACKUP = os.path.join(PATH_SUBTITLD_USER_CONFIG, 'backup')

PATH_SUBTITLD_DATA_UPDATE = os.path.join(PATH_SUBTITLD_USER_CONFIG, 'update')

if not os.path.isdir(PATH_SUBTITLD_USER_CONFIG):
    os.mkdir(PATH_SUBTITLD_USER_CONFIG)

if not os.path.isdir(PATH_SUBTITLD_DATA_BACKUP):
    os.mkdir(PATH_SUBTITLD_DATA_BACKUP)

if not os.path.isdir(PATH_SUBTITLD_DATA_UPDATE):
    os.mkdir(PATH_SUBTITLD_DATA_UPDATE)

PATH_SUBTITLD_USER_CONFIG_FILE = os.path.join(PATH_SUBTITLD_USER_CONFIG, 'subtitld.config')


def get_graphics_path(filename):
    """Function to get graphics path. Windows have a problem with paths."""
    final_path = os.path.join(PATH_SUBTITLD_GRAPHICS, filename)
    if sys.platform == 'win32' or os.name == 'nt':
        final_path = final_path.replace('\\', '/')
    return final_path


VERSION_NUMBER = '20.07.0.0'
if os.path.isfile(os.path.join(PATH_SUBTITLD, 'current_version')):
    VERSION_NUMBER = open(os.path.join(PATH_SUBTITLD, 'current_version')).read().strip()

LIST_OF_SUPPORTED_VIDEO_EXTENSIONS = (('.mp4', '.mkv', '.mov', '.mpg', '.webm', '.ogv', '.m4v'))

LIST_OF_SUPPORTED_SUBTITLE_EXTENSIONS = {
    'SRT': {'description': 'SubRip Subtitle format', 'extensions': ['srt']},
    'DFXP': {'description': 'Subtitle format', 'extensions': ['ttml', 'dfxp']},
    'SAMI': {'description': 'Subtitle format', 'extensions': ['smi', 'sami']},
    'SCC': {'description': 'Subtitle format', 'extensions': ['scc']},
    'VTT': {'description': 'Subtitle format', 'extensions': ['webvtt', 'vtt']},
    'ASS': {'description': 'SubStation Alpha Subtitle format', 'extensions': ['ass', 'ssa']},
    'SBV': {'description': 'Subtitle format', 'extensions': ['sbv']},
    'SUB': {'description': 'MicroDVD Subtitle format', 'extensions': ['sub']},
    'XML': {'description': 'Subtitle format', 'extensions': ['xml']},
    'USF': {'description': 'Universal Subtitle format', 'extensions': ['usf']}
}

LIST_OF_SUPPORTED_IMPORT_EXTENSIONS = {
    'TXT': {'description': 'Simple TXT file', 'extensions': ['txt']},
    'SRT': {'description': 'SubRip Subtitle format', 'extensions': ['srt']}
}

LIST_OF_SUPPORTED_EXPORT_EXTENSIONS = {
    'TXT': {'description': 'Simple TXT file', 'extensions': ['txt']},
    'KDENLIVE': {'description': 'Kdenlive format', 'extensions': ['kdenlive']}
}

LANGUAGE_DICT_LIST = {
    'Afrikaans (South Africa)': 'af-za',
    'Amharic (Ethiopia)': 'am-et',
    'Arabic (United Arab Emirates)': 'ar-ae',
    'Arabic (Bahrain)': 'ar-bh',
    'Arabic (Algeria)': 'ar-dz',
    'Arabic (Egypt)': 'ar-eg',
    'Arabic (Israel)': 'ar-il',
    'Arabic (Iraq)': 'ar-iq',
    'Arabic (Jordan)': 'ar-jo',
    'Arabic (Kuwait)': 'ar-kw',
    'Arabic (Lebanon)': 'ar-lb',
    'Arabic (Morocco)': 'ar-ma',
    'Arabic (Oman)': 'ar-om',
    'Arabic (State of Palestine)': 'ar-ps',
    'Arabic (Qatar)': 'ar-qa',
    'Arabic (Saudi Arabia)': 'ar-sa',
    'Arabic (Tunisia)': 'ar-tn',
    'Azerbaijani (Azerbaijan)': 'az-az',
    'Bulgarian (Bulgaria)': 'bg-bg',
    'Bengali (Bangladesh)': 'bn-bd',
    'Bengali (India)': 'bn-in',
    'Catalan (Spain)': 'ca-es',
    'Chinese, Mandarin (Simplified, China)': 'cmn-hans-cn',
    'Chinese, Mandarin (Simplified, Hong Kong)': 'cmn-hans-hk',
    'Chinese, Mandarin (Traditional, Taiwan)': 'cmn-hant-tw',
    'Czech (Czech Republic)': 'cs-cz',
    'Danish (Denmark)': 'da-dk',
    'German (Germany)': 'de-de',
    'Greek (Greece)': 'el-gr',
    'English (Australia)': 'en-au',
    'English (Canada)': 'en-ca',
    'English (United Kingdom)': 'en-gb',
    'English (Ghana)': 'en-gh',
    'English (Ireland)': 'en-ie',
    'English (India)': 'en-in',
    'English (Kenya)': 'en-ke',
    'English (Nigeria)': 'en-ng',
    'English (New Zealand)': 'en-nz',
    'English (Philippines)': 'en-ph',
    'English (Singapore)': 'en-sg',
    'English (Tanzania)': 'en-tz',
    'English (United States)': 'en-us',
    'English (South Africa)': 'en-za',
    'Spanish (Argentina)': 'es-ar',
    'Spanish (Bolivia)': 'es-bo',
    'Spanish (Chile)': 'es-cl',
    'Spanish (Colombia)': 'es-co',
    'Spanish (Costa Rica)': 'es-cr',
    'Spanish (Dominican Republic)': 'es-do',
    'Spanish (Ecuador)': 'es-ec',
    'Spanish (Spain)': 'es-es',
    'Spanish (Guatemala)': 'es-gt',
    'Spanish (Honduras)': 'es-hn',
    'Spanish (Mexico)': 'es-mx',
    'Spanish (Nicaragua)': 'es-ni',
    'Spanish (Panama)': 'es-pa',
    'Spanish (Peru)': 'es-pe',
    'Spanish (Puerto Rico)': 'es-pr',
    'Spanish (Paraguay)': 'es-py',
    'Spanish (El Salvador)': 'es-sv',
    'Spanish (United States)': 'es-us',
    'Spanish (Uruguay)': 'es-uy',
    'Spanish (Venezuela)': 'es-ve',
    'Basque (Spain)': 'eu-es',
    'Persian (Iran)': 'fa-ir',
    'Finnish (Finland)': 'fi-fi',
    'Filipino (Philippines)': 'fil-ph',
    'French (Canada)': 'fr-ca',
    'French (France)': 'fr-fr',
    'Galician (Spain)': 'gl-es',
    'Gujarati (India)': 'gu-in',
    'Hebrew (Israel)': 'he-il',
    'Hindi (India)': 'hi-in',
    'Croatian (Croatia)': 'hr-hr',
    'Hungarian (Hungary)': 'hu-hu',
    'Armenian (Armenia)': 'hy-am',
    'Indonesian (Indonesia)': 'id-id',
    'Icelandic (Iceland)': 'is-is',
    'Italian (Italy)': 'it-it',
    'Japanese (Japan)': 'ja-jp',
    'Javanese (Indonesia)': 'jv-id',
    'Georgian (Georgia)': 'ka-ge',
    'Khmer (Cambodia)': 'km-kh',
    'Kannada (India)': 'kn-in',
    'Korean (South Korea)': 'ko-kr',
    'Lao (Laos)': 'lo-la',
    'Lithuanian (Lithuania)': 'lt-lt',
    'Latvian (Latvia)': 'lv-lv',
    'Malayalam (India)': 'ml-in',
    'Marathi (India)': 'mr-in',
    'Malay (Malaysia)': 'ms-my',
    'Norwegian Bokmal (Norway)': 'nb-no',
    'Nepali (Nepal)': 'ne-np',
    'Dutch (Netherlands)': 'nl-nl',
    'Polish (Poland)': 'pl-pl',
    'Portuguese (Brazil)': 'pt-br',
    'Portuguese (Portugal)': 'pt-pt',
    'Romanian (Romania)': 'ro-ro',
    'Russian (Russia)': 'ru-ru',
    'Sinhala (Sri Lanka)': 'si-lk',
    'Slovak (Slovakia)': 'sk-sk',
    'Slovenian (Slovenia)': 'sl-si',
    'Serbian (Serbia)': 'sr-rs',
    'Sundanese (Indonesia)': 'su-id',
    'Swedish (Sweden)': 'sv-se',
    'Swahili (Kenya)': 'sw-ke',
    'Swahili (Tanzania)': 'sw-tz',
    'Tamil (India)': 'ta-in',
    'Tamil (Sri Lanka)': 'ta-lk',
    'Tamil (Malaysia)': 'ta-my',
    'Tamil (Singapore)': 'ta-sg',
    'Telugu (India)': 'te-in',
    'Thai (Thailand)': 'th-th',
    'Turkish (Turkey)': 'tr-tr',
    'Ukrainian (Ukraine)': 'uk-ua',
    'Urdu (India)': 'ur-in',
    'Urdu (Pakistan)': 'ur-pk',
    'Vietnamese (Vietnam)': 'vi-vn',
    'Chinese, Cantonese (Traditional, Hong Kong)': 'yue-hant-hk',
    'Zulu (South Africa)': 'zu-za'
}
