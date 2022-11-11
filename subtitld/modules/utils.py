import ctypes
import platform

from subtitld.modules.paths import LIST_OF_SUPPORTED_SUBTITLE_EXTENSIONS


def is_float(element: str) -> bool:
    try:
        float(element)
        return True
    except ValueError:
        return False


def get_timeline_time_str(seconds, ms=False):
    """Function to return timecode from seconds"""
    secs = int(seconds % 60)
    mins = int((seconds / 60) % 60)
    hrs = int((seconds / 60) / 60)
    mss = int(round(float('0.' + str(seconds).split('.', 1)[-1]), 3) * 1000)

    if ms:
        if hrs:
            return "{hh:02d}:{mm:02d}:{ss:02d}.{mss:03d}".format(hh=hrs, mm=mins, ss=secs, mss=mss)
        elif mins:
            return "{mm:02d}:{ss:02d}.{mss:03d}".format(mm=mins, ss=secs, mss=mss)
        else:
            return "{ss:02d}.{mss:03d}".format(ss=secs, mss=mss)
    else:
        if hrs:
            return "{hh:02d}:{mm:02d}:{ss:02d}".format(hh=hrs, mm=mins, ss=secs)
        elif mins:
            return "{mm:02d}:{ss:02d}".format(mm=mins, ss=secs)
        else:
            return "{ss:02d}".format(ss=secs)


def convert_ffmpeg_timecode_to_seconds(timecode):
    """Function to convert ffmpeg timecode to seconds"""
    if timecode:
        final_value = float(timecode.split(':')[-1])
        if timecode.count(':') > 2:
            final_value += int(timecode.split(':')[-2]) * 60.0
        if timecode.count(':') > 3:
            final_value += int(timecode.split(':')[-3]) * 3600.0
        if timecode.count(':') > 4:
            final_value += int(timecode.split(':')[-4]) * 3600.0
        return final_value
    else:
        return False


class GetProcAddressGetter:
    """ fixme: Class gets obsolete once https://bugreports.qt.io/browse/PYSIDE-971 gets fixed """

    def __init__(self):
        self._func = self._find_platform_wrapper()

    def _find_platform_wrapper(self):
        operating_system = platform.system()
        if operating_system == 'Linux':
            return self._init_linux()
        elif operating_system == 'Windows':
            return self._init_windows()
        raise f'Platform {operating_system} not supported yet'

    def _init_linux(self):
        try:
            from OpenGL import GLX
            return self._glx_impl
        except AttributeError:
            pass
        try:
            from OpenGL import EGL
            return self._egl_impl
        except AttributeError:
            pass
        raise 'Cannot initialize OpenGL'

    def _init_windows(self):
        import glfw
        from PySide6.QtGui import QOffscreenSurface, QOpenGLContext

        self.surface = QOffscreenSurface()
        self.surface.create()

        if not glfw.init():
            raise 'Cannot initialize OpenGL'

        glfw.window_hint(glfw.VISIBLE, glfw.FALSE)
        window = glfw.create_window(1, 1, "mpvQC-OpenGL", None, None)

        glfw.make_context_current(window)
        # QOpenGLContext.currentContext().makeCurrent(self.surface)
        return self._windows_impl

    def wrap(self, _, name: bytes):
        address = self._func(name)
        return ctypes.cast(address, ctypes.c_void_p).value

    @staticmethod
    def _glx_impl(name: bytes):
        from OpenGL import GLX
        return GLX.glXGetProcAddress(name.decode("utf-8"))

    @staticmethod
    def _egl_impl(name: bytes):
        from OpenGL import EGL
        return EGL.eglGetProcAddress(name.decode("utf-8"))

    @staticmethod
    def _windows_impl(name: bytes):
        import glfw
        return glfw.get_proc_address(name.decode('utf8'))


def get_subtitle_format(subtitle_filepath):
    subtitle_format = False
    if subtitle_filepath:
        for formt in LIST_OF_SUPPORTED_SUBTITLE_EXTENSIONS:
            for ext in LIST_OF_SUPPORTED_SUBTITLE_EXTENSIONS[formt]['extensions']:
                if subtitle_filepath.endswith(ext):
                    return formt
    return subtitle_format


def get_format_from_extension(extension):
    for formt in LIST_OF_SUPPORTED_SUBTITLE_EXTENSIONS:
        for ext in LIST_OF_SUPPORTED_SUBTITLE_EXTENSIONS[formt]['extensions']:
            if extension == ext:
                return formt
    return 'USF'
