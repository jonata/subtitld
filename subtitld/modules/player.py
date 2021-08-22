"""MPV Player

"""

import os

from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QRect, QMargins, QMetaObject
from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtWidgets import QOpenGLWidget, QLabel, QWidget
from PyQt5.QtOpenGL import QGLContext

from subtitld.mpv import MPV, _mpv_get_sub_api, _mpv_opengl_cb_set_update_callback, _mpv_opengl_cb_init_gl, OpenGlCbGetProcAddrFn, _mpv_opengl_cb_draw, _mpv_opengl_cb_report_flip, MpvSubApi, OpenGlCbUpdateFn, _mpv_opengl_cb_uninit_gl


def get_proc_addr(_, name):
    """Function needed for mpv"""
    glctx = QGLContext.currentContext()
    if glctx is None:
        return 0
    addr = int(glctx.getProcAddress(name.decode('utf-8')))
    return addr


class MpvWidget(QOpenGLWidget):
    """Main MPV widget class"""
    positionChanged = pyqtSignal(float, int)
    durationChanged = pyqtSignal(float, int)
    initialized = pyqtSignal(str)

    def __init__(self, parent=None):
        super(MpvWidget, self).__init__(parent)
        self.parent = parent
        self.mpv = MPV(vo='opengl-cb',
                       ytdl=False,
                       osd_level=0,
                       sub_auto=False,
                       sub_ass=False,
                       sub_visibility=False,
                       keep_open=True,
                       idle=True,
                       cursor_autohide=False,
                       input_cursor=False,
                       input_default_bindings=False,
                       stop_playback_on_init_failure=False,

                    #    cache=True,

                       #vd_queue_enable='yes',
                    #    demuxer_max_bytes=41943040,
                    #    demuxer_max_back_bytes=41943040,
                    #    hr_seek=True,
                    #    hr_seek_framedrop=False,
                       input_vo_keyboard=False,
                       sid=False,
                       #video_sync='display-vdrop',
                       audio_file_auto=False,
                       quiet=True,
                       hwdec=('auto'))
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
        """Initialize GL function"""
        _mpv_opengl_cb_init_gl(self.mpv_gl, None, self.get_proc_addr_c, None)

    def paintGL(self):
        """Paint GL function, compatible with HiDPI display"""
        ratio = self.parent.parent().windowHandle().devicePixelRatio()
        width = int(self.width() * ratio)
        height = int(self.height() * ratio)
        _mpv_opengl_cb_draw(self.mpv_gl, self.defaultFramebufferObject(), width, -height)

    @pyqtSlot()
    def maybe_update(self):
        """Maybeupdate function"""
        if self.window().isMinimized():
            self.makeCurrent()
            self.paintGL()
            self.context().swapBuffers(self.context().surface())
            self.swapped()
            self.doneCurrent()
        else:
            self.update()

    def on_update(self, ctx=None):
        """On update function"""
        QMetaObject.invokeMethod(self, 'maybe_update')

    def on_update_fake(self, ctx=None):
        """Fake on update function"""
        pass

    def swapped(self):
        """Swap function"""
        _mpv_opengl_cb_report_flip(self.mpv_gl, 0)

    def closeEvent(self, _):
        """On close player function"""
        self.makeCurrent()
        if self.mpv_gl:
            _mpv_opengl_cb_set_update_callback(self.mpv_gl, self.on_update_fake_c, None)
        _mpv_opengl_cb_uninit_gl(self.mpv_gl)
        self.mpv.terminate()

    def position_changed(self, _, pos):
        """Position changed function. It calls update timeline paint."""
        if pos:
            self.position = pos
        if pos is not None:
            self.parent.parent().timeline.update(self.parent.parent())

    def loadfile(self, filepath) -> None:
        """Function to load a media file"""
        if os.path.isfile(filepath):
            self.mpv.command('loadfile', filepath, 'replace')
            self.mpv.wait_for_property('seekable')
        self.mpv.pause = True

    def frameStep(self) -> None:
        """Function to move forward one step (frame)"""
        self.mpv.command('frame-step')

    def frameBackStep(self) -> None:
        """Function to move backward one step (frame)"""
        self.mpv.command('frame-back-step')

    def seek(self, pos=0.0, method='absolute+exact') -> None:
        """Function to seek at some position"""
        self.mpv.seek(pos, method)

    def stop(self) -> None:
        """Function to stop playback (fake stop, it is pause + position 0)"""
        self.mpv.pause = True
        # self.position = 0.0
        self.seek()

    def pause(self) -> None:
        """Function to pause playback (fake pause, it just changes actual playback status)"""
        self.mpv.pause = not self.mpv.pause

    def play(self) -> None:
        """Function to play (fake play, it just changes actual playback status)"""
        if self.mpv.pause:
            self.mpv.pause = False

    def mute(self) -> None:
        """Function to mute"""
        self.property('mute', not self.property('mute'))

    def volume(self, vol: int) -> None:
        """Function to change volume"""
        self.property('volume', vol)


class PlayerSubtitleLayer(QLabel):
    """Lass of subtitle layer"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.subtitle_text = ''
        self.action_safe_margin = .9
        self.title_safe_margin = .8
        self.show_action_safe_margin = False
        self.show_title_safe_margin = False

    def paintEvent(self, event):
        """Function to paint subtitle layer"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        if self.show_title_safe_margin or self.subtitle_text:
            title_safe_margin_qrect = QRect(self.width()*((1.0-self.title_safe_margin)*.5),
                                            self.height()*((1.0-self.title_safe_margin)*.5),
                                            self.width()*(self.title_safe_margin),
                                            self.height()*(self.title_safe_margin)
                                            )
        if self.subtitle_text:
            painter.setPen(QPen(QColor.fromRgb(0, 0, 0, 200)))
            painter.drawText(title_safe_margin_qrect - QMargins(2, 2, -2, -2), Qt.AlignHCenter | Qt.AlignBottom | Qt.TextWordWrap, self.subtitle_text)
            painter.setPen(QPen(QColor.fromRgb(255, 255, 255)))
            painter.drawText(title_safe_margin_qrect, Qt.AlignHCenter | Qt.AlignBottom | Qt.TextWordWrap, self.subtitle_text)

        if self.show_action_safe_margin:
            action_safe_margin_qrect = QRect(self.width()*((1.0-self.action_safe_margin)*.5),
                                                self.height()*((1.0-self.action_safe_margin)*.5),
                                                self.width()*(self.action_safe_margin),
                                                self.height()*(self.action_safe_margin)
                                                )
            painter.setPen(QPen(QColor.fromRgb(103, 255, 77, 240), 1, Qt.SolidLine))
            painter.drawRect(action_safe_margin_qrect)
            painter.drawLine(self.width()*.5,
                                action_safe_margin_qrect.y(),
                                self.width()*.5,
                                action_safe_margin_qrect.y() + (self.height()*.025))
            painter.drawLine(self.width()*.5,
                                action_safe_margin_qrect.y() + action_safe_margin_qrect.height(),
                                self.width()*.5,
                                action_safe_margin_qrect.y() + action_safe_margin_qrect.height() - (self.height()*.025))
            painter.drawLine(action_safe_margin_qrect.x(),
                                self.height()*.5,
                                action_safe_margin_qrect.x() + (self.width()*.025),
                                self.height()*.5)
            painter.drawLine(action_safe_margin_qrect.x() + action_safe_margin_qrect.width(),
                                self.height()*.5,
                                action_safe_margin_qrect.x() + action_safe_margin_qrect.width() - (self.width()*.025),
                                self.height()*.5)

        if self.show_title_safe_margin:
            painter.setPen(QPen(QColor.fromRgb(255, 0, 0, 240), 1, Qt.SolidLine))
            painter.drawRect(title_safe_margin_qrect)

        painter.end()
        event.accept()

    def setSubtitleText(self, text):
        """Function to change subtitle layer text"""
        self.subtitle_text = text


class PlayerWidgetArea(QWidget):
    """Class to reimplement enter and leave events on subtitle layer"""
    def enterEvent(self, event):
        """Function to call when cursor enter player widget area"""
        event.accept()

    def leaveEvent(self, event):
        """Function to call when cursor leave player widget area"""
        event.accept()


def load(self):
    """Function to load player widgets"""
    self.player_widget_area = PlayerWidgetArea(self)

    self.player_border = QLabel(self.player_widget_area)
    self.player_border.setObjectName('player_border')

    self.player_widget = MpvWidget(parent=self.player_widget_area)

    self.player_widget.positionChanged.connect(lambda: self.timeline.update(self))

    self.player_subtitle_layer = PlayerSubtitleLayer(parent=self.player_widget_area)
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
    """Function to update player widgets"""
    self.player_widget_area.setVisible(bool(self.video_metadata))
    self.player_border.setVisible(bool(self.video_metadata))
    update_safety_margins_subtitle_layer(self)


def resized(self):
    """Function to resize player widgets"""
    self.player_widget_area.setGeometry(self.width()*.2, 0, self.width()*.6, self.height()-self.playercontrols_widget.height())
    self.videoinfo_label.setGeometry(self.player_widget_area.x(), 20, self.player_widget_area.width(), 50)
    resize_player_widget(self)


def update_safety_margins_subtitle_layer(self):
    """Function to update margins preferences"""
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
    """Function to change playback speed"""
    self.player_widget.mpv.speed = self.playback_speed


def update_subtitle_layer(self):
    """Function to update subtitle layer"""
    text = ''
    for subtitle in self.subtitles_list:
        if self.player_widget.position and (self.player_widget.position > subtitle[0] and self.player_widget.position < subtitle[0] + subtitle[1]):
            text = subtitle[2]
            break
    self.player_subtitle_layer.setSubtitleText(text)
    self.player_subtitle_layer.update()


def resize_player_widget(self):
    """Function to resize player widget (to accomodate video ratio inside screen space)"""
    if self.video_metadata.get('width', 640) > self.video_metadata.get('height', 480):
        heigth_proportion = (self.player_widget_area.width()-6) / self.video_metadata.get('width', 640)
        self.player_widget.setGeometry(3, (self.player_widget_area.height()*.5)-((heigth_proportion*self.video_metadata.get('height', 480))*.5), self.player_widget_area.width()-6, self.video_metadata.get('height', 480)*heigth_proportion)
    else:
        width_proportion = (self.player_widget_area.height()-6) / self.video_metadata.get('height', 480)
        self.player_widget.setGeometry((self.player_widget_area.width()*.5)-((width_proportion*self.video_metadata.get('width', 640))*.5), 3, self.video_metadata.get('width', 640)*width_proportion, self.player_widget_area.height()-6)
    self.player_border.setGeometry(self.player_widget.x()-3, self.player_widget.y()-3, self.player_widget.width()+6, self.player_widget.height()+6)
    self.player_subtitle_layer.setGeometry(self.player_widget.x(), self.player_widget.y(), self.player_widget.width(), self.player_widget.height())
    # self.player_subtitle_textedit.setGeometry(self.player_widget.x()+(self.player_widget.width()*.1), self.player_widget.y()+(self.player_widget.height()*.5), self.player_widget.width()*.8, self.player_widget.height()*.4)
