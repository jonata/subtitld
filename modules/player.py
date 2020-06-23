#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import sys

from OpenGL import GL

from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QEvent, QTimer
from PyQt5.QtGui import QKeyEvent, QMouseEvent, QWheelEvent, QPainter
from PyQt5.QtWidgets import QOpenGLWidget, QLabel, QWidget

import mpv

if sys.platform == 'win32':
    from PyQt5.QtOpenGL import QGLContext
elif sys.platform == 'darwin':
    from OpenGL.GLUT import glutGetProcAddress
else:
    from OpenGL.platform import PLATFORM
    from ctypes import c_char_p, c_void_p


def getProcAddress(proc: bytes) -> int:
    if sys.platform == 'win32':
        _ctx = QGLContext.currentContext()
        if _ctx is None:
            return 0
        _gpa = (_ctx.getProcAddress, proc.decode())
    elif sys.platform == 'darwin':
        _gpa = (glutGetProcAddress, proc)
    else:
        # noinspection PyUnresolvedReferences
        _getProcAddress = PLATFORM.getExtensionProcedure
        _getProcAddress.argtypes = [c_char_p]
        _getProcAddress.restype = c_void_p
        _gpa = (_getProcAddress, proc)
    return _gpa[0](_gpa[1]).__int__()


class MpvWidget(QOpenGLWidget):
    positionChanged = pyqtSignal(float, int)
    durationChanged = pyqtSignal(float, int)
    initialized = pyqtSignal(str)

    def __init__(self, parent=None, file=None, **mpv_opts):
        super(MpvWidget, self).__init__(parent)
        self.parent = parent
        self.filename = file
        self.mpvError = mpv.MPVError
        self.originalParent = None
        self.position = 0.0
        self.mpv = mpv.Context()
        #print(dir(self.mpv))
        # self.mpv.command('no-osd')
        #self.mpv.autosub = False
        # self.mpv.sid = 'no'

        self.option('msg-level', self.msglevel)
        self.setLogLevel('terminal-default')
        self.option('config', 'no')

        def _istr(o):
            return ('yes' if o else 'no') if isinstance(o, bool) else str(o)

        # do not break on non-existant properties/options
        for opt, val in mpv_opts.items():
            try:
                self.option(opt.replace('_', '-'), _istr(val))
            except mpv.MPVError:
                print('error setting MPV option "%s" to value "%s"' % (opt, val))
                #self.logger.warning('error setting MPV option "%s" to value "%s"' % (opt, val))

        self.mpv.initialize()

        self.opengl = self.mpv.opengl_cb_api()
        self.opengl.set_update_callback(self.updateHandler)

        if sys.platform == 'win32':
            try:
                self.option('gpu-context', 'angle')
            except mpv.MPVError:
                self.option('opengl-backend', 'angle')

        self.frameSwapped.connect(self.swapped, Qt.DirectConnection)

        self.mpv.observe_property('time-pos')
        self.mpv.observe_property('duration')
        self.mpv.observe_property('eof-reached')
        self.mpv.set_wakeup_callback(self.eventHandler)

        if file is not None:
            self.initialized.connect(self.play)

    @property
    def msglevel(self):
        if os.getenv('DEBUG', False) or getattr(self.parent, 'verboseLogs', False):
            return 'all=v'
        else:
            return 'all=error'

    def setLogLevel(self, loglevel):
        self.mpv.set_log_level(loglevel)

    def shutdown(self):
        self.makeCurrent()
        if self.opengl:
            self.opengl.set_update_callback(None)
        self.opengl.uninit_gl()
        self.mpv.command('quit')

    def initializeGL(self):
        if self.opengl:
            self.opengl.init_gl(None, getProcAddress)
            if self.filename is not None:
                self.initialized.emit(self.filename)

    def paintGL(self):
        if self.opengl:
            GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
            self.opengl.draw(self.defaultFramebufferObject(), self.width(), -self.height())

    @pyqtSlot()
    def swapped(self):
        if self.opengl:
            self.opengl.report_flip(0)

    def updateHandler(self):
        # if self.window().isMinimized():
        #     self.makeCurrent()
        #     self.paintGL()
        #     self.context().swapBuffers(self.context().surface())
        #     self.swapped()
        #     self.doneCurrent()
        # else:
        self.update()

    def eventHandler(self):
        while self.mpv:
            try:
                event = self.mpv.wait_event(.01)
                if event.id in {mpv.Events.none, mpv.Events.shutdown}:
                    break
                elif event.id == mpv.Events.log_message:
                    event_log = event.data
                    log_msg = '[%s] %s' % (event_log.prefix, event_log.text.strip())
                    if event_log.level in (mpv.LogLevels.fatal, mpv.LogLevels.error):
                        # self.logger.critical(log_msg)
                        if event_log.level == mpv.LogLevels.fatal or 'file format' in event_log.text:
                            self.parent.errorOccurred.emit(log_msg)
                            self.parent.initMediaControls(False)
                    else:
                        print(log_msg)
                        # self.logger.info(log_msg)
                elif event.id == mpv.Events.property_change:
                    event_prop = event.data
                    if event_prop.name == 'eof-reached' and event_prop.data:
                        # self.parent.setPlayButton(False)
                        # self.parent.setPosition(0)
                        self.parent.parent().playercontrols.playercontrols_stop_button_clicked(self.parent.parent())
                        # self.durationChanged.emit(event_prop.data, self.property('estimated-frame-count'))
                    elif event_prop.name == 'time-pos':
                        # if os.getenv('DEBUG', False) or getattr(self.parent, 'verboseLogs', False):
                        #     self.logger.info('time-pos property event')
                        self.position = event_prop.data
                        self.positionChanged.emit(event_prop.data, self.property('estimated-frame-number'))
                    elif event_prop.name == 'duration':
                        # if os.getenv('DEBUG', False) or getattr(self.parent, 'verboseLogs', False):
                        #     self.logger.info('duration property event')
                        self.durationChanged.emit(event_prop.data, self.property('estimated-frame-count'))
            except mpv.MPVError as e:
                if e.code != -10:
                    raise e

    def showText(self, msg: str, duration: int=5, level: int=0):
        self.mpv.command('show-text', msg, duration * 1000, level)

    @pyqtSlot(str, name='ewewf', )
    def loadfile(self, filepath) -> None:
        if os.path.isfile(filepath):
            self.mpv.command('loadfile', filepath, 'replace')
        self.property('pause', True)

    def frameStep(self) -> None:
        self.mpv.command('frame-step')

    def frameBackStep(self) -> None:
        self.mpv.command('frame-back-step')

    def seek(self, pos, method='absolute+exact') -> None:
        self.mpv.command('seek', pos, method)

    def stop(self) -> None:
        self.property('pause', True)
        self.seek(pos=0.0)

    def pause(self) -> None:
        self.property('pause', not self.property('pause'))

    def play(self) -> None:
        if self.property('pause'):
            self.property('pause', False)

    def mute(self) -> None:
        self.property('mute', not self.property('mute'))

    def volume(self, vol: int) -> None:
        self.property('volume', vol)

    def codec(self, stream: str='video') -> str:
        return self.property('{}-codec'.format(stream))

    def format(self, stream: str='video') -> str:
        return self.property('audio-codec-name' if stream == 'audio' else 'video-format')

    def version(self) -> str:
        ver = self.mpv.api_version
        return '{0}.{1}'.format(ver[0], ver[1])

    def option(self, option: str, val):
        if isinstance(val, bool):
            val = 'yes' if val else 'no'
        return self.mpv.set_option(option, val)

    def property(self, prop: str, val=None):
        if val is None:
            return self.mpv.get_property(prop)
        else:
            if isinstance(val, bool):
                val = 'yes' if val else 'no'
            return self.mpv.set_property(prop, val)

    def changeEvent(self, event: QEvent) -> None:
        if event.type() == QEvent.WindowStateChange and self.isFullScreen():
            self.option('osd-align-x', 'center')
            self.showText('Press ESC or double mouse click to exit full screen')
            QTimer.singleShot(5000, self.resetOSD)

    def resetOSD(self) -> None:
        self.showText('')
        self.option('osd-align-x', 'left')

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() in {Qt.Key_F, Qt.Key_Escape}:
            event.accept()
            if self.parent is None:
                self.originalParent.toggleFullscreen()
            else:
                self.parent.toggleFullscreen()
        elif self.isFullScreen():
            self.originalParent.keyPressEvent(event)
        else:
            super(MpvWidget, self).keyPressEvent(event)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        event.accept()
        if event.button() == Qt.LeftButton:
            if self.parent is None:
                self.originalParent.playMedia()
            else:
                self.parent.playMedia()

    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
        event.accept()
        if self.parent is None:
            self.originalParent.toggleFullscreen()
        else:
            self.parent.toggleFullscreen()

    def wheelEvent(self, event: QWheelEvent) -> None:
        self.parent.seekSlider.wheelEvent(event)

























def load(self):
    class player_widget_area(QWidget):
        def enterEvent(widget, event):
            None

        def leaveEvent(widget, event):
            None

    self.player_widget_area = player_widget_area(self)

    self.player_border = QLabel(self.player_widget_area)
    self.player_border.setObjectName('player_border')

    self.player_widget = MpvWidget(
            parent=self.player_widget_area,
            # file=file,
            vo='opengl-cb',
            # pause=pause,
            # start=start,
            # mute=mute,
            keep_open='always',
            idle=True,
            # osd_font=self._osdfont,
            # osd_level=0,
            # osd_align_x='left',
            # osd_align_y='top',
            cursor_autohide=False,
            input_cursor=False,
            input_default_bindings=False,
            stop_playback_on_init_failure=False,
            input_vo_keyboard=False,
            sub_auto=False,
            sid=False,
            video_sync='display-vdrop',
            audio_file_auto=False,
            quiet=True,
            # volume=volume if volume is not None else self.parent.startupvol,
            # opengl_pbo=self.enablePBO,
            # keepaspect=self.keepRatio,
            #  if self.hardwareDecoding else 'no'))
            hwdec=('auto'))

    # self.player_widget = MpvWidget(parent=self.player_widget_area)
    self.player_widget.positionChanged.connect(lambda: self.timeline.update(self))

    class player_subtitle_layer(QLabel):
        def paintEvent(widget, paintEvent):
            painter = QPainter(widget)
            # painter.setRenderHint(QPainter.Antialiasing)
            painter.setCompositionMode(26)
            painter.drawRect(10, 10, 200, 200)
            painter.end()

    self.player_subtitle_layer = QLabel(parent=self.player_widget_area)
    # self.player_subtitle_layer = player_subtitle_layer(parent=self.player_widget_area)
    self.player_subtitle_layer.setWordWrap(True)
    self.player_subtitle_layer.setObjectName('player_subtitle_layer')

    # self.player_subtitle_textedit = QTextEdit(parent=self.player_widget_area)
    # self.player_subtitle_textedit.setVisible(False)
    # self.player_subtitle_textedit.setObjectName('player_subtitle_textedit')
    # self.player_subtitle_textedit.textChanged.connect(lambda: player_subtitle_textedit_changed(self))

    self.videoinfo_label = QLabel(parent=self)
    self.videoinfo_label.setObjectName('videoinfo_label')


def update(self):
    self.player_widget_area.setVisible(bool(self.video_metadata))
    self.player_border.setVisible(bool(self.video_metadata))


def resized(self):
    self.player_widget_area.setGeometry(self.width()*.2, 0, self.width()*.6, self.height()-self.playercontrols_widget.height())
    self.videoinfo_label.setGeometry(self.player_widget_area.x(), 20, self.player_widget_area.width(), 50)
    resize_player_widget(self)


# def player_subtitle_textedit_changed(self):
#     old_selected_subtitle = self.selected_subtitle
#     counter = self.subtitles_list.index(old_selected_subtitle)
#     self.subtitles_list[counter][2] = self.player_subtitle_textedit.toPlainText()
#     self.subtitleslist.update_subtitles_list_qlistwidget(self)
#     self.timeline.update(self)
#     update_subtitle_layer(self)


# def playpause(self):
#     self.player_widget.pause = not self.player_widget.pause


def update_speed(self):
    self.player_widget.speed = self.playback_speed


def update_subtitle_layer(self):
    text = ''
    for subtitle in self.subtitles_list:
        if self.player_widget.position and (self.player_widget.position > subtitle[0] and self.player_widget.position < subtitle[0] + subtitle[1]):
            text = subtitle[2]
            break

    self.player_subtitle_layer.setText(text)


def resize_player_widget(self):
    if self.video_metadata.get('width', 640) > self.video_metadata.get('height', 480):
        heigth_proportion = (self.player_widget_area.width()-6) / self.video_metadata.get('width', 640)
        self.player_widget.setGeometry(3, (self.player_widget_area.height()*.5)-((heigth_proportion*self.video_metadata.get('height', 480))*.5), self.player_widget_area.width()-6, self.video_metadata.get('height', 480)*heigth_proportion)
    else:
        width_proportion = (self.player_widget_area.height()-6) / self.video_metadata.get('height', 480)
        self.player_widget.setGeometry((self.player_widget_area.width()*.5)-((width_proportion*self.video_metadata.get('width', 640))*.5), 3, self.video_metadata.get('width', 640)*width_proportion, self.player_widget_area.height()-6)
    self.player_border.setGeometry(self.player_widget.x()-3, self.player_widget.y()-3, self.player_widget.width()+6, self.player_widget.height()+6)
    self.player_subtitle_layer.setGeometry(self.player_widget.x(), self.player_widget.y(), self.player_widget.width(), self.player_widget.height())
    # self.player_subtitle_textedit.setGeometry(self.player_widget.x()+(self.player_widget.width()*.1), self.player_widget.y()+(self.player_widget.height()*.5), self.player_widget.width()*.8, self.player_widget.height()*.4)
