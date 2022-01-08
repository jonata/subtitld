"""MPV Player

"""

import os

from PyQt5.QtCore import QEasingCurve, QPropertyAnimation, QSize, pyqtSignal, pyqtSlot, Qt, QRect, QMargins, QMetaObject
from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtWidgets import QBoxLayout, QGraphicsOpacityEffect, QHBoxLayout, QOpenGLWidget, QLabel, QSizePolicy, QSpacerItem, QVBoxLayout, QWidget
from PyQt5.QtOpenGL import QGLContext

#from subtitld.mpv import MPV, _mpv_get_sub_api, _mpv_opengl_cb_set_update_callback, _mpv_opengl_cb_init_gl, OpenGlCbGetProcAddrFn, _mpv_opengl_cb_draw, _mpv_opengl_cb_report_flip, MpvSubApi, OpenGlCbUpdateFn, _mpv_opengl_cb_uninit_gl
#from subtitld.modules.mpv_widget import MpvWidget2

import mpv
from mpv import MPV, MpvRenderContext, OpenGlCbGetProcAddrFn

def get_proc_addr(_, name):
    glctx = QGLContext.currentContext()
    if glctx is None:
        return None
    addr = int(glctx.getProcAddress(name.decode("utf-8")))
    return addr


class MpvWidget(QOpenGLWidget):
    """Main MPV widget class"""
    positionChanged = pyqtSignal(float, int)

    def __init__(widget, parent=None):
        super().__init__(parent)

        #widget.setFixedSize(QSize(640,480))

        widget.mpv = MPV(
            ytdl=False,
            loglevel='info',
            log_handler=print
        )

        widget.mpv_gl = None
        widget.get_proc_addr_c = OpenGlCbGetProcAddrFn(get_proc_addr)
        widget.frameSwapped.connect(
           widget.swapped, Qt.ConnectionType.DirectConnection
        )

        for key, value in {
            # "config": False,
            'osd_level': 0,
            'sub_auto': False,
            'sub_ass': False,
            'sub_visibility': False,
            'keep_open': True,
            'cursor_autohide': False,
            'input_cursor': False,
            'input_default_bindings': False,
            'stop_playback_on_init_failure': False,
            'audio_file_auto': False,
            'input_vo_keyboard': False,
            'sid': False,
            "quiet": True,
            "msg-level": "all=info",
            "osc": False,
            "osd-bar": False,
            "input-cursor": False,
            "input-vo-keyboard": False,
            "input-default-bindings": False,
            "ytdl": False,
            "sub-auto": False,
            "audio-file-auto": False,
            "vo": "libmpv",
            "hwdec": "auto",
            "pause": True,
            "idle": True,
            "blend-subtitles": "video",
            "video-sync": "display-vdrop",
            "keepaspect": True,
            "stop-playback-on-init-failure": False,
            "keep-open": True,
            # "track-auto-selection": False,
        }.items():
            setattr(widget.mpv, key, value)

        widget.position = 0.0

        widget.mpv.observe_property('time-pos', widget.position_changed)

    def initializeGL(widget):
        widget.mpv_gl = MpvRenderContext(
            widget.mpv,
            "opengl",
            opengl_init_params={"get_proc_address": widget.get_proc_addr_c},
        )
        widget.mpv_gl.update_cb = widget.on_update

    def paintGL(widget):
        if widget.mpv_gl:
            ratio = widget.devicePixelRatioF()
            w = int(widget.width() * ratio)
            h = int(widget.height() * ratio)
            widget.mpv_gl.render(
                flip_y=True,
                opengl_fbo={
                    "fbo": widget.defaultFramebufferObject(),
                    "w": w,
                    "h": h,
                },
            )

    @pyqtSlot()
    def maybe_update(widget):
        """Maybeupdate function"""
        if widget.window().isMinimized():
            widget.makeCurrent()
            widget.paintGL()
            widget.context().swapBuffers(widget.context().surface())
            widget.swapped()
            widget.doneCurrent()
        else:
            widget.update()

    def on_update(widget, ctx=None):
        widget.update()
        # print(widget.width())
        # print(widget.height())

    def on_update_fake(widget, ctx=None):
        pass

    def swapped(widget):
        if widget.mpv_gl:
            widget.mpv_gl.report_swap()

    def closeEvent(widget, _):
        widget.makeCurrent()
        if widget.mpv_gl:
            widget.mpv_gl.update_cb = widget.on_update_fake
            widget.mpv_gl.free()

    def position_changed(widget, _, pos):
        """Position changed function. It calls update timeline paint."""
        if pos:
            widget.position = pos
        if pos is not None:
            widget.positionChanged.emit(pos, 1)
            #widget.parent.parent().timeline.update(widget.parent.parent())

    def loadfile(widget, filepath) -> None:
        """Function to load a media file"""
        if os.path.isfile(filepath):
            widget.mpv.command('loadfile', filepath, 'replace')
            widget.mpv.wait_for_property('seekable')
        widget.mpv.pause = True
        print('loaded')

    def frameStep(widget) -> None:
        """Function to move forward one step (frame)"""
        widget.mpv.command('frame-step')

    def frameBackStep(widget) -> None:
        """Function to move backward one step (frame)"""
        widget.mpv.command('frame-back-step')

    def seek(widget, pos=0.0, method='absolute+exact') -> None:
        """Function to seek at some position"""
        widget.mpv.seek(pos, method)

    def stop(widget) -> None:
        """Function to stop playback (fake stop, it is pause + position 0)"""
        widget.mpv.pause = True
        # widget.position = 0.0
        widget.seek()

    def pause(widget) -> None:
        """Function to pause playback (fake pause, it just changes actual playback status)"""
        widget.mpv.pause = not widget.mpv.pause

    def play(widget) -> None:
        """Function to play (fake play, it just changes actual playback status)"""
        if widget.mpv.pause:
            widget.mpv.pause = False

    def mute(widget) -> None:
        """Function to mute"""
        widget.property('mute', not widget.property('mute'))

    def volume(widget, vol: int) -> None:
        """Function to change volume"""
        widget.property('volume', vol)

    #def resizeEvent(widget, event):
    #    event.accept()
    #    #print(widget.width())
    #    #print(widget.height())

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

    # self.layer_player = QWidget(self)
    # self.layer_player.setLayout(QVBoxLayout())
    # self.layer_player.setContentsMargins(self.subtitleslist_width_proportion * self.width(), 20, 20, 200)
    #self.layer_player.layout().setSpacing(0)


    # self.layer_player_left_spacer = QWidget()
    # self.layer_player_left_spacer.setMaximumWidth(0)
    # # sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
    # # self.layer_player_left_spacer.setSizePolicy(sizePolicy)
    # self.layer_player_left_spacer_animation = QPropertyAnimation(self.layer_player_left_spacer, b'maximumWidth')
    # self.layer_player_left_spacer_animation.setEasingCurve(QEasingCurve.OutCirc)
    # self.layer_player_hbox.addWidget(self.layer_player_left_spacer)

    # self.layer_player_vbox = QVBoxLayout()
    # self.layer_player_vbox.setContentsMargins(0, 0, 0, 0)

    self.videoinfo_label = QLabel() # parent=self.layer_player
    #self.videoinfo_label.setObjectName('videoinfo_label')
    #self.videoinfo_label.setFixedHeight(20)
    #sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
    #self.videoinfo_label.setSizePolicy(sizePolicy)
    #layer_player.layout().addWidget(self.videoinfo_label)

    self.player_widget = MpvWidget()
    #sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
    #sizePolicy.setWidthForHeight(self.player_widget.sizePolicy().hasWidthForHeight())
    #self.player_widget.setSizePolicy(sizePolicy)
    #self.player_widget_transparency = QGraphicsOpacityEffect()
    #self.player_widget.setGraphicsEffect(self.player_widget_transparency)
    #self.player_widget_transparency_animation = QPropertyAnimation(self.player_widget_transparency, b'opacity')
    #self.player_widget_transparency_animation.setEasingCurve(QEasingCurve.OutExpo)
    #self.player_widget_transparency.setOpacity(1)
    #self.player_widget_animation = QPropertyAnimation(self.player_widget, b'geometry')
    #self.player_widget_animation.setEasingCurve(QEasingCurve.OutCirc)
    self.player_widget.positionChanged.connect(lambda: self.timeline.update(self))
    self.player_widget.setLayout(QVBoxLayout(self.player_widget))

    self.player_subtitle_layer = PlayerSubtitleLayer()
    self.player_subtitle_layer.setWordWrap(True)
    self.player_subtitle_layer.setObjectName('player_subtitle_layer')
    self.player_widget.layout().addWidget(self.player_subtitle_layer)

    # class player_border(QLabel):
    #     def resizeEvent(widget, e):
    #         if self.video_metadata:
    #             aspect_ratio = self.video_metadata.get('height', 1080) / self.video_metadata.get('width', 1920)
    #             widget.setFixedHeight(widget.height() * aspect_ratio) #self.video_metadata.get('width', 1920), self.video_metadata.get('height', 1080))
                # w = widget.width()
                # h = widget.height()
                # if w / h > aspect_ratio:  # too wide
                #     widget.setFixedHeight(h)
                #     widget.layout().setDirection(QBoxLayout.LeftToRight)
                #     widget_stretch = h * aspect_ratio
                #     outer_stretch = (w - widget_stretch) / 2 + 0.5
                # else:  # too tall
                #     widget.layout().setDirection(QBoxLayout.TopToBottom)
                #     widget_stretch = w / aspect_ratio
                #     outer_stretch = (h - widget_stretch) / 2 + 0.5


    self.player_border = QLabel(self) #parent=self.layer_player
    self.player_border_transparency = QGraphicsOpacityEffect()
    self.player_border.setGraphicsEffect(self.player_border_transparency)
    self.player_border_transparency_animation = QPropertyAnimation(self.player_border_transparency, b'opacity')
    self.player_border_transparency_animation.setEasingCurve(QEasingCurve.OutCirc)
    self.player_border_transparency.setOpacity(0)
    self.player_border_animation = QPropertyAnimation(self.player_border, b'geometry')
    self.player_border_animation.setEasingCurve(QEasingCurve.OutCirc)

    self.player_border.setObjectName('player_border')
    self.player_border.setLayout(QVBoxLayout(self.player_border))
    self.player_border.layout().setContentsMargins(1, 1, 1, 1)
    self.player_border.layout().addWidget(self.player_widget)

    #self.layer_player.layout().addWidget(self.player_border)

    # class player_ratio_widget(QLabel):
    #     def __init__(widget, child):
    #         super().__init__()
    #         widget.aspect_ratio = 1.77777#child.size().width() / child.size().height()
    #         widget.setLayout(QBoxLayout(QBoxLayout.LeftToRight))
    #         #  add spacer, then widget, then spacer
    #         widget.layout().addItem(QSpacerItem(0, 0))
    #         widget.layout().addWidget(child)
    #         widget.layout().addItem(QSpacerItem(0, 0))
    #         #sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
    #         #widget.setSizePolicy(sizePolicy)

    #     def resizeEvent(widget, e):
    #         w = e.size().width()
    #         h = e.size().height()
    #         if w / h > widget.aspect_ratio:  # too wide
    #             widget.layout().setDirection(QBoxLayout.LeftToRight)
    #             widget_stretch = h * widget.aspect_ratio
    #             outer_stretch = (w - widget_stretch) / 2 + 0.5
    #         else:  # too tall
    #             widget.layout().setDirection(QBoxLayout.TopToBottom)
    #             widget_stretch = w / widget.aspect_ratio
    #             outer_stretch = (h - widget_stretch) / 2 + 0.5

    #         widget.layout().setStretch(0, outer_stretch)
    #         widget.layout().setStretch(1, widget_stretch)
    #         widget.layout().setStretch(2, outer_stretch)

    # self.player_ratio_widget = player_ratio_widget(child=self.player_border)#QLabel()

    #self.layer_player.layout().addWidget(self.player_ratio_widget)

    #self.layer_player_hbox.addLayout(self.layer_player_vbox)



def update(self):
    """Function to update player widgets"""
    #self.layer_player.setVisible(bool(self.video_metadata))
    #self.player_border.setVisible(bool(self.video_metadata))
    update_safety_margins_subtitle_layer(self)


def resized(self):
    """Function to resize player widgets"""
    #self.layer_player.setGeometry(0, 0, self.width(), self.height())
    #self.layer_player.layout().setContentsMargins(self.width()*self.subtitleslist_width_proportion, 20, 20, 200)
    # TODO
    #self.layer_player_left_spacer.setMaximumWidth(self.width()*self.subtitleslist_width_proportion)
    #self.player_widget_area.setGeometry(0, 0, self.width(), self.height()-self.playercontrols_widget.height())
    #self.videoinfo_label.setGeometry(self.player_widget_area.x(), 20, self.player_widget_area.width(), 50)

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
    self.player_widget.mpv.speed = self.playback_speed if self.change_playback_speed.isChecked() else 1.0


def update_subtitle_layer(self):
    """Function to update subtitle layer"""
    text = ''
    for subtitle in self.subtitles_list:
        if self.player_widget.position and (self.player_widget.position > subtitle[0] and self.player_widget.position < subtitle[0] + subtitle[1]):
            text = subtitle[2]
            break
    self.player_subtitle_layer.setSubtitleText(text)
    self.player_subtitle_layer.update()


def resize_player_widget(self, just_get_qrect=False):
    """Function to resize player widget (to accomodate video ratio inside screen space)"""
    # None
    if self.video_metadata:
        x = self.subtitleslist_width_proportion * self.width()
        y = 20
        w = self.width() - x - 20
        h = self.height() - y - 20 - 200

        if w / h > self.video_metadata.get('width', 1920) / self.video_metadata.get('height', 1080):
            aspect_ratio = self.video_metadata.get('width', 1920) / self.video_metadata.get('height', 1080)
            new_h = h
            new_w = h * aspect_ratio
            qrect = QRect(x + (w - new_w) / 2, y, new_w, new_h)
        else:
            aspect_ratio = self.video_metadata.get('height', 1080) / self.video_metadata.get('width', 1920)
            new_h = w * aspect_ratio
            new_w = w
            qrect = QRect(x, y + ((h - new_h) / 2), new_w, new_h)

        if just_get_qrect:
            return [qrect.x(), qrect.y(), qrect.width(), qrect.height()]
        else:
            self.player_border.setGeometry(qrect)
    # if self.video_metadata.get('width', 1920) > self.video_metadata.get('height', 1080):
    #     wp = 1
    #     hp = self.video_metadata.get('height', 1080) / self.video_metadata.get('width', 1920)
    # else:
    #     wp = self.video_metadata.get('width', 1920) / self.video_metadata.get('height', 1080)
    #     hp = 1

    # self.video_metadata.get('width', 1920) / self.video_metadata.get('height', 1080)
    #if self.video_metadata.get('width', 640) > self.video_metadata.get('height', 480):
    #    heigth_proportion = ((self.player_widget_area.width()*.7)-6) / self.video_metadata.get('width', 640)
    #    self.player_widget.setGeometry((self.width()*.2) + 3, (self.player_widget_area.height()*.5)-((heigth_proportion*self.video_metadata.get('height', 480))*.5), (self.player_widget_area.width()*.7)-6, self.video_metadata.get('height', 480)*heigth_proportion)
    #else:
    #    width_proportion = (self.player_widget_area.height()-7) / self.video_metadata.get('height', 480)
    #    self.player_widget.setGeometry((self.width()*.2) + ((self.player_widget_area.width()*.7)*.5)-((width_proportion*self.video_metadata.get('width', 640))*.5), 3, self.video_metadata.get('width', 640)*width_proportion, self.player_widget_area.height()-6)
    #self.player_border.setGeometry(self.player_widget.x()-3, self.player_widget.y()-3, self.player_widget.width()+6, self.player_widget.height()+6)
    #self.player_subtitle_layer.setGeometry(self.player_widget.x(), self.player_widget.y(), self.player_widget.width(), self.player_widget.height())
    # self.player_subtitle_textedit.setGeometry(self.player_widget.x()+(self.player_widget.width()*.1), self.player_widget.y()+(self.player_widget.height()*.5), self.player_widget.width()*.8, self.player_widget.height()*.4)
