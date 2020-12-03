#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os

from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QRect, QMargins, QMetaObject
from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtWidgets import QOpenGLWidget, QLabel, QWidget
from PyQt5.QtOpenGL import QGLContext

from mpv import MPV, _mpv_get_sub_api, _mpv_opengl_cb_set_update_callback, _mpv_opengl_cb_init_gl, OpenGlCbGetProcAddrFn, _mpv_opengl_cb_draw, _mpv_opengl_cb_report_flip, MpvSubApi, OpenGlCbUpdateFn, _mpv_opengl_cb_uninit_gl


def get_proc_addr(_, name):
    glctx = QGLContext.currentContext()
    if glctx is None:
        return 0
    addr = int(glctx.getProcAddress(name.decode('utf-8')))
    return addr


class MpvWidget(QOpenGLWidget):
    positionChanged = pyqtSignal(float, int)
    durationChanged = pyqtSignal(float, int)
    initialized = pyqtSignal(str)

    def __init__(self, parent=None, file=None, **mpv_opts):
        super(MpvWidget, self).__init__(parent)
        self.parent = parent
        self.filename = file
        self.mpv = MPV(vo='opengl-cb',
                       ytdl=True,
                       osd_level=0,
                       sub_auto=False,
                       sub_ass=False,
                       sub_visibility=False,
                       keep_open=True,
                       )
        self.mpv_gl = _mpv_get_sub_api(self.mpv.handle, MpvSubApi.MPV_SUB_API_OPENGL_CB)
        self.on_update_c = OpenGlCbUpdateFn(self.on_update)
        self.on_update_fake_c = OpenGlCbUpdateFn(self.on_update_fake)
        self.get_proc_addr_c = OpenGlCbGetProcAddrFn(get_proc_addr)
        _mpv_opengl_cb_set_update_callback(self.mpv_gl, self.on_update_c, None)
        self.frameSwapped.connect(self.swapped, Qt.DirectConnection)

        self.position = 0.0

        self.mpv.observe_property('time-pos', self.position_changed)
        # self.mpv.observe_property('duration')
        # self.mpv.observe_property('eof-reached', self.eof_reached)

    def initializeGL(self):
        _mpv_opengl_cb_init_gl(self.mpv_gl, None, self.get_proc_addr_c, None)

    def paintGL(self):
        # compatible with HiDPI display
        ratio = self.parent.parent().windowHandle().devicePixelRatio()
        w = int(self.width() * ratio)
        h = int(self.height() * ratio)
        _mpv_opengl_cb_draw(self.mpv_gl, self.defaultFramebufferObject(), w, -h)

    @pyqtSlot()
    def maybe_update(self):
        if self.window().isMinimized():
            self.makeCurrent()
            self.paintGL()
            self.context().swapBuffers(self.context().surface())
            self.swapped()
            self.doneCurrent()
        else:
            self.update()

    def on_update(self, ctx=None):
        QMetaObject.invokeMethod(self, 'maybe_update')

    def on_update_fake(self, ctx=None):
        pass

    def swapped(self):
        _mpv_opengl_cb_report_flip(self.mpv_gl, 0)

    def closeEvent(self, _):
        self.makeCurrent()
        if self.mpv_gl:
            _mpv_opengl_cb_set_update_callback(self.mpv_gl, self.on_update_fake_c, None)
        _mpv_opengl_cb_uninit_gl(self.mpv_gl)
        self.mpv.terminate()

    def position_changed(self, property_change_event, pos):
        if pos:
            self.position = pos
        if pos is not None:
            self.parent.parent().timeline.update(self.parent.parent())

    def loadfile(self, filepath) -> None:
        if os.path.isfile(filepath):
            self.mpv.command('loadfile', filepath, 'replace')
        self.mpv.pause = True

    def frameStep(self) -> None:
        self.mpv.command('frame-step')

    def frameBackStep(self) -> None:
        self.mpv.command('frame-back-step')

    def seek(self, pos=0.0, method='absolute+exact') -> None:
        self.mpv.seek(pos, method)

    def stop(self) -> None:
        self.mpv.pause = True
        self.position = 0.0
        self.seek()

    def pause(self) -> None:
        self.mpv.pause = not self.mpv.pause

    def play(self) -> None:
        if self.mpv.pause:
            self.mpv.pause = False

    def mute(self) -> None:
        self.property('mute', not self.property('mute'))

    def volume(self, vol: int) -> None:
        self.property('volume', vol)

    # def codec(self, stream: str='video') -> str:
    #     return self.property('{}-codec'.format(stream))
    #
    # def format(self, stream: str='video') -> str:
    #     return self.property('audio-codec-name' if stream == 'audio' else 'video-format')
    #
    # def version(self) -> str:
    #     ver = self.mpv.api_version
    #     return '{0}.{1}'.format(ver[0], ver[1])
    #
    # def option(self, option: str, val):
    #     if isinstance(val, bool):
    #         val = 'yes' if val else 'no'
    #     return self.mpv.set_option(option, val)
    #
    # def property(self, prop: str, val=None):
    #     if val is None:
    #         return self.mpv.get_property(prop)
    #     else:
    #         if isinstance(val, bool):
    #             val = 'yes' if val else 'no'
    #         return self.mpv.set_property(prop, val)
    #
    # def changeEvent(self, event: QEvent) -> None:
    #     if event.type() == QEvent.WindowStateChange and self.isFullScreen():
    #         self.option('osd-align-x', 'center')
    #         self.showText('Press ESC or double mouse click to exit full screen')
    #         QTimer.singleShot(5000, self.resetOSD)
    #
    # def resetOSD(self) -> None:
    #     self.showText('')
    #     self.option('osd-align-x', 'left')
    #
    # def keyPressEvent(self, event: QKeyEvent) -> None:
    #     if event.key() in {Qt.Key_F, Qt.Key_Escape}:
    #         event.accept()
    #         if self.parent is None:
    #             self.originalParent.toggleFullscreen()
    #         else:
    #             self.parent.toggleFullscreen()
    #     elif self.isFullScreen():
    #         self.originalParent.keyPressEvent(event)
    #     else:
    #         super(MpvWidget, self).keyPressEvent(event)
    #
    # def mousePressEvent(self, event: QMouseEvent) -> None:
    #     event.accept()
    #     if event.button() == Qt.LeftButton:
    #         if self.parent is None:
    #             self.originalParent.playMedia()
    #         else:
    #             self.parent.playMedia()
    #
    # def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
    #     event.accept()
    #     if self.parent is None:
    #         self.originalParent.toggleFullscreen()
    #     else:
    #         self.parent.toggleFullscreen()
    #
    # def wheelEvent(self, event: QWheelEvent) -> None:
    #     self.parent.seekSlider.wheelEvent(event)


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
        def __init__(widget, parent=None):
            super().__init__(parent)
            widget.subtitle_text = ''
            widget.action_safe_margin = .9
            widget.title_safe_margin = .8
            widget.show_action_safe_margin = False
            widget.show_title_safe_margin = False

        def paintEvent(widget, paintEvent):
            painter = QPainter(widget)
            painter.setRenderHint(QPainter.Antialiasing)
            if widget.show_title_safe_margin or widget.subtitle_text:
                title_safe_margin_qrect = QRect(widget.width()*((1.0-widget.title_safe_margin)*.5),
                                                widget.height()*((1.0-widget.title_safe_margin)*.5),
                                                widget.width()*(widget.title_safe_margin),
                                                widget.height()*(widget.title_safe_margin)
                                                )
            if widget.subtitle_text:
                painter.setPen(QPen(QColor.fromRgb(0, 0, 0, 200)))
                painter.drawText(title_safe_margin_qrect - QMargins(2, 2, -2, -2), Qt.AlignCenter | Qt.AlignBottom | Qt.TextWordWrap, widget.subtitle_text)
                painter.setPen(QPen(QColor.fromRgb(255, 255, 255)))
                painter.drawText(title_safe_margin_qrect, Qt.AlignCenter | Qt.AlignBottom | Qt.TextWordWrap, widget.subtitle_text)

            if widget.show_action_safe_margin:
                action_safe_margin_qrect = QRect(widget.width()*((1.0-widget.action_safe_margin)*.5),
                                                 widget.height()*((1.0-widget.action_safe_margin)*.5),
                                                 widget.width()*(widget.action_safe_margin),
                                                 widget.height()*(widget.action_safe_margin)
                                                 )
                painter.setPen(QPen(QColor.fromRgb(103, 255, 77, 240), 1, Qt.SolidLine))
                painter.drawRect(action_safe_margin_qrect)
                painter.drawLine(widget.width()*.5,
                                 action_safe_margin_qrect.y(),
                                 widget.width()*.5,
                                 action_safe_margin_qrect.y() + (widget.height()*.025))
                painter.drawLine(widget.width()*.5,
                                 action_safe_margin_qrect.y() + action_safe_margin_qrect.height(),
                                 widget.width()*.5,
                                 action_safe_margin_qrect.y() + action_safe_margin_qrect.height() - (widget.height()*.025))
                painter.drawLine(action_safe_margin_qrect.x(),
                                 widget.height()*.5,
                                 action_safe_margin_qrect.x() + (widget.width()*.025),
                                 widget.height()*.5)
                painter.drawLine(action_safe_margin_qrect.x() + action_safe_margin_qrect.width(),
                                 widget.height()*.5,
                                 action_safe_margin_qrect.x() + action_safe_margin_qrect.width() - (widget.width()*.025),
                                 widget.height()*.5)

            if widget.show_title_safe_margin:
                painter.setPen(QPen(QColor.fromRgb(255, 0, 0, 240), 1, Qt.SolidLine))
                painter.drawRect(title_safe_margin_qrect)

            painter.end()

        def setSubtitleText(widget, text):
            widget.subtitle_text = text

    self.player_subtitle_layer = player_subtitle_layer(parent=self.player_widget_area)
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
    update_safety_margins_subtitle_layer(self)


def resized(self):
    self.player_widget_area.setGeometry(self.width()*.2, 0, self.width()*.6, self.height()-self.playercontrols_widget.height())
    self.videoinfo_label.setGeometry(self.player_widget_area.x(), 20, self.player_widget_area.width(), 50)
    resize_player_widget(self)


def update_safety_margins_subtitle_layer(self):
    self.player_subtitle_layer.show_action_safe_margin = self.settings['safety_margins'].get('show_action_safe_margins', False)
    self.player_subtitle_layer.show_title_safe_margin = self.settings['safety_margins'].get('show_title_safe_margins', False)
    self.player_subtitle_layer.update()

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
    self.player_widget.property('speed', self.playback_speed)


def update_subtitle_layer(self):
    text = ''
    for subtitle in self.subtitles_list:
        if self.player_widget.position and (self.player_widget.position > subtitle[0] and self.player_widget.position < subtitle[0] + subtitle[1]):
            text = subtitle[2]
            break

    self.player_subtitle_layer.setSubtitleText(text)
    self.player_subtitle_layer.update()


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
