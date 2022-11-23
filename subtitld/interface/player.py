import os
from mpv import MPV, MpvRenderContext, MpvGlGetProcAddressFn

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGraphicsOpacityEffect
from PySide6.QtCore import Signal, Qt, QRect, QPropertyAnimation, QEasingCurve, QMargins
from PySide6.QtGui import QPainter, QPen, QColor, QFont, QBrush
from PySide6.QtOpenGLWidgets import QOpenGLWidget

from subtitld.modules.utils import GetProcAddressGetter
from subtitld.modules.paths import ACTUAL_OS
from subtitld.interface import playercontrols, subtitles_panel


class MpvWidget(QOpenGLWidget):
    """Main MPV widget class"""
    positionChanged = Signal(float, int)
    eofReached = Signal()

    def __init__(widget, parent=None):
        super().__init__(parent)

        widget.mpv = MPV(
            # ytdl=False,
            loglevel='info',
            log_handler=print
        )

        widget.mpv_gl = None
        widget.get_proc_addr_c = MpvGlGetProcAddressFn(GetProcAddressGetter().wrap)
        widget.frameSwapped.connect(
            widget.swapped, Qt.ConnectionType.DirectConnection
        )

        options = {
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
            # "ytdl": False,
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
            # "hwdec": "vaapi",
            # "gpu-context": "x11egl"
        }

        if not ACTUAL_OS == 'windows':
            options["gpu-hwdec-interop"] = "vaapi-egl"

        for key, value in options.items():
            setattr(widget.mpv, key, value)

        widget.position = 0.0
        widget.mpv.observe_property('time-pos', widget.position_changed)
        widget.mpv.observe_property('eof-reached', widget.eof_reached)

    def initializeGL(widget):
        widget.mpv_gl = MpvRenderContext(
            widget.mpv,
            api_type="opengl",
            opengl_init_params={"get_proc_address": widget.get_proc_addr_c},
        )
        widget.mpv_gl.update_cb = widget.on_update

    def paintGL(widget):
        if widget.mpv_gl:
            ratio = widget.devicePixelRatioF()
            w = int(widget.width() * ratio)
            h = int(widget.height() * ratio)
            fbo = widget.defaultFramebufferObject()
            widget.mpv_gl.render(
                flip_y=True,
                opengl_fbo={
                    "fbo": fbo,
                    "w": w,
                    "h": h,
                },
            )

    # @Slot()
    # def maybe_update(widget):
    #     """Maybeupdate function"""
    #     if widget.window().isMinimized():
    #         widget.makeCurrent()
    #         widget.paintGL()
    #         widget.context().swapBuffers(widget.context().surface())
    #         widget.swapped()
    #         widget.doneCurrent()
    #     else:
    #         widget.update()

    def on_update(widget, ctx=None):
        widget.update()
        #  print(widget.width())
        #  print(widget.height())

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
            #  widget.parent.parent().timeline.update(widget.parent.parent())

    def eof_reached(widget, _, property):
        widget.eofReached.emit()

    def loadfile(widget, filepath) -> None:
        """Function to load a media file"""
        if os.path.isfile(filepath):
            widget.mpv.command('loadfile', filepath, 'replace')
            widget.mpv.wait_for_property('seekable')
        widget.mpv.pause = True

    def frameStep(widget) -> None:
        """Function to move forward one step (frame)"""
        widget.mpv.command('frame-step')

    def frameBackStep(widget) -> None:
        """Function to move backward one step (frame)"""
        widget.mpv.command('frame-back-step')

    def seek(widget, pos=0.0, method='absolute+exact') -> None:
        """Function to seek at some position"""
        widget.mpv.seek(pos, method)
        widget.position = pos

    def stop(widget) -> None:
        """Function to stop playback (fake stop, it is pause + position 0)"""
        widget.mpv.pause = True
        # print(dir(widget.mpv))
        if widget.mpv.filename:
            widget.position = 0.0
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

    # def resizeEvent(widget, event):
    #    event.accept()
    #    #print(widget.width())
    #    #print(widget.height())


class PlayerSubtitleLayer(QLabel):
    """Lass of subtitle layer"""
    def __init__(widget, parent=None):
        super().__init__(parent)
        widget.subtitle_text = ''
        widget.action_safe_margin = .9
        widget.title_safe_margin = .8
        widget.style = {}

    def paintEvent(widget, event):
        """Function to paint subtitle layer"""
        painter = QPainter(widget)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.setFont(QFont(widget.style.get('font_family', 'Ubuntu'), widget.style.get('font_size', 40)))

        title_safe_margin_qrect = widget.rect() - QMargins(
            (widget.style.get('safe_margin_title_x', 10) / 100) * widget.width(),
            (widget.style.get('safe_margin_title_y', 10) / 100) * widget.height(),
            (widget.style.get('safe_margin_title_x', 10) / 100) * widget.width(),
            (widget.style.get('safe_margin_title_y', 10) / 100) * widget.height()
        )

        # QRect(
        #     widget.width() * (widget.style.get('safe_margin_title_x', 10) / 100.0),
        #     widget.height() * (widget.style.get('safe_margin_title_y', 10) / 100.0),
        #     widget.width() * (1.0 - ((widget.style.get('safe_margin_title_x', 10) * 2) / 100)),
        #     widget.height() * (1.0 - ((widget.style.get('safe_margin_title_y', 10) * 2) / 100))
        # )

        if widget.subtitle_text:

            if widget.style.get('backgroundbox_enabled', True):
                text_rect = painter.boundingRect(title_safe_margin_qrect, Qt.AlignBottom | Qt.AlignHCenter | Qt.TextWordWrap, widget.subtitle_text)

                painter.setPen(Qt.NoPen)
                painter.setBrush(QBrush(QColor(widget.style.get('backgroundbox_color', '#55000000'))))

                if widget.style.get('backgroundbox_border_radius', 5):
                    painter.drawRoundedRect(text_rect.marginsAdded(QMargins(widget.style.get('backgroundbox_padding', 10), widget.style.get('backgroundbox_padding', 10), widget.style.get('backgroundbox_padding', 10), widget.style.get('backgroundbox_padding', 10))), widget.style.get('backgroundbox_border_radius', 5), widget.style.get('backgroundbox_border_radius', 5))
                else:
                    painter.drawRect(text_rect.marginsAdded(QMargins(widget.style.get('backgroundbox_padding', 10), widget.style.get('backgroundbox_padding', 10), widget.style.get('backgroundbox_padding', 10), widget.style.get('backgroundbox_padding', 10))))

                painter.setBrush(Qt.NoBrush)

            if widget.style.get('shadow_enabled', True):
                painter.setPen(QPen(widget.style.get('shadow_color', '#ff000000')))
                painter.drawText(title_safe_margin_qrect - QMargins(widget.style.get('shadow_x', 2), widget.style.get('shadow_y', 2), -widget.style.get('shadow_x', 2), -widget.style.get('shadow_y', 2)), Qt.AlignHCenter | Qt.AlignBottom | Qt.TextWordWrap, widget.subtitle_text)

            painter.setPen(QPen(widget.style.get('color', '#ffffffff')))
            painter.drawText(title_safe_margin_qrect, Qt.AlignHCenter | Qt.AlignBottom | Qt.TextWordWrap, widget.subtitle_text)

        if widget.style.get('safe_margin_action_enabled', False):
            action_safe_margin_qrect = widget.rect() - QMargins(
                (widget.style.get('safe_margin_action_x', 5) / 100) * widget.width(),
                (widget.style.get('safe_margin_action_y', 5) / 100) * widget.height(),
                (widget.style.get('safe_margin_action_x', 5) / 100) * widget.width(),
                (widget.style.get('safe_margin_action_y', 5) / 100) * widget.height()
            )

            painter.setPen(QPen(QColor(widget.style.get('safe_margin_action_color', '#dd67FF4D')), 1, Qt.SolidLine))
            painter.drawRect(action_safe_margin_qrect)

            painter.drawLine(
                widget.width() * .5,
                action_safe_margin_qrect.y(),
                widget.width() * .5,
                action_safe_margin_qrect.y() + (widget.height() * .025)
            )
            painter.drawLine(
                widget.width() * .5,
                action_safe_margin_qrect.y() + action_safe_margin_qrect.height(),
                widget.width() * .5,
                action_safe_margin_qrect.y() + action_safe_margin_qrect.height() - (widget.height() * .025)
            )
            painter.drawLine(
                action_safe_margin_qrect.x(),
                widget.height() * .5,
                action_safe_margin_qrect.x() + (widget.width() * .025),
                widget.height() * .5
            )
            painter.drawLine(
                action_safe_margin_qrect.x() + action_safe_margin_qrect.width(),
                widget.height() * .5,
                action_safe_margin_qrect.x() + action_safe_margin_qrect.width() - (widget.width() * .025),
                widget.height() * .5
            )

        if widget.style.get('safe_margin_title_enabled', False):
            painter.setPen(QPen(QColor(widget.style.get('safe_margin_title_color', '#ddff0000')), 1, Qt.SolidLine))
            painter.drawRect(title_safe_margin_qrect)

        painter.end()
        event.accept()

    def setSubtitleText(widget, text):
        """Function to change subtitle layer text"""
        widget.subtitle_text = text

    def update_style(widget, style):
        widget.style = style
        widget.update()


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
    # self.layer_player.setContentsMargins(self.subtitles_panel_width_proportion * self.width(), 20, 20, 200)
    # self.layer_player.layout().setSpacing(0)

    # self.layer_player_left_spacer = QWidget()
    # self.layer_player_left_spacer.setMaximumWidth(0)
    # # sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
    # # self.layer_player_left_spacer.setSizePolicy(sizePolicy)
    # self.layer_player_left_spacer_animation = QPropertyAnimation(self.layer_player_left_spacer, b'maximumWidth')
    # self.layer_player_left_spacer_animation.setEasingCurve(QEasingCurve.OutCirc)
    # self.layer_player_hbox.addWidget(self.layer_player_left_spacer)

    # self.layer_player_vbox = QVBoxLayout()
    # self.layer_player_vbox.setContentsMargins(0, 0, 0, 0)

    # self.videoinfo_label = QLabel()  # parent=self.layer_player
    # # self.videoinfo_label.setObjectName('videoinfo_label')
    # # self.videoinfo_label.setFixedHeight(20)
    # # sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
    # # self.videoinfo_label.setSizePolicy(sizePolicy)
    # # layer_player.layout().addWidget(self.videoinfo_label)

    self.player_widget = MpvWidget()
    # sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
    # sizePolicy.setWidthForHeight(self.player_widget.sizePolicy().hasWidthForHeight())
    # self.player_widget.setSizePolicy(sizePolicy)
    # self.player_widget_transparency = QGraphicsOpacityEffect()
    # self.player_widget.setGraphicsEffect(self.player_widget_transparency)
    # self.player_widget_transparency_animation = QPropertyAnimation(self.player_widget_transparency, b'opacity')
    # self.player_widget_transparency_animation.setEasingCurve(QEasingCurve.OutExpo)
    # self.player_widget_transparency.setOpacity(1)
    # self.player_widget_animation = QPropertyAnimation(self.player_widget, b'geometry')
    # self.player_widget_animation.setEasingCurve(QEasingCurve.OutCirc)
    self.player_widget.positionChanged.connect(lambda: update_timelines(self))
    self.player_widget.eofReached.connect(lambda: eof_reached(self))
    self.player_widget.setLayout(QVBoxLayout(self.player_widget))

    self.player_subtitle_layer = PlayerSubtitleLayer()
    self.player_subtitle_layer.setWordWrap(True)
    self.player_subtitle_layer.update_style(self.settings['videoplayer'])
    self.player_subtitle_layer.setObjectName('player_subtitle_layer')
    self.player_widget.layout().addWidget(self.player_subtitle_layer)

    # class player_border(QLabel):
    #     def resizeEvent(widget, e):
    #         if self.video_metadata:
    #             aspect_ratio = self.video_metadata.get('height', 1080) / self.video_metadata.get('width', 1920)
    #             widget.setFixedHeight(widget.height() * aspect_ratio) #self.video_metadata.get('width', 1920), self.video_metadata.get('height', 1080))
    #            # w = widget.width()
    #            # h = widget.height()
    #            # if w / h > aspect_ratio:  # too wide
    #            #     widget.setFixedHeight(h)
    #            #     widget.layout().setDirection(QBoxLayout.LeftToRight)
    #            #     widget_stretch = h * aspect_ratio
    #            #     outer_stretch = (w - widget_stretch) / 2 + 0.5
    #            # else:  # too tall
    #            #     widget.layout().setDirection(QBoxLayout.TopToBottom)
    #            #     widget_stretch = w / aspect_ratio
    #            #     outer_stretch = (h - widget_stretch) / 2 + 0.5

    self.player_border = QLabel(self)  # parent=self.layer_player
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

    # self.layer_player.layout().addWidget(self.player_border)

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

    # self.layer_player.layout().addWidget(self.player_ratio_widget)

    # self.layer_player_hbox.addLayout(self.layer_player_vbox)


def update(self):
    """Function to update player widgets"""
    # self.layer_player.setVisible(bool(self.video_metadata))
    # self.player_border.setVisible(bool(self.video_metadata))
    update_safety_margins_subtitle_layer(self)


def resized(self):
    """Function to resize player widgets"""
    # self.layer_player.setGeometry(0, 0, self.width(), self.height())
    # self.layer_player.layout().setContentsMargins(self.width()*self.subtitles_panel_width_proportion, 20, 20, 200)
    # TODO
    # self.layer_player_left_spacer.setMaximumWidth(self.width()*self.subtitles_panel_width_proportion)
    # self.player_widget_area.setGeometry(0, 0, self.width(), self.height()-self.playercontrols_widget.height())
    # self.videoinfo_label.setGeometry(self.player_widget_area.x(), 20, self.player_widget_area.width(), 50)

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
#     self.subtitles_panel.update_subtitles_panel_qlistwidget(self)
#     self.timeline.update(self)
#     update_subtitle_layer(self)


def eof_reached(self):
    self.player_widget.mpv.pause = True
    self.playercontrols_playpause_button.setChecked(False)
    # playercontrols.playercontrols_playpause_button_update(self)


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
        x = int(self.subtitles_panel_width_proportion * self.width())
        y = 20
        w = self.width() - x - 20
        h = self.height() - y - 20 - 200

        if w / h > self.video_metadata.get('width', 1920) / self.video_metadata.get('height', 1080):
            aspect_ratio = self.video_metadata.get('width', 1920) / self.video_metadata.get('height', 1080)
            new_h = h
            new_w = h * aspect_ratio
            qrect = QRect(int(x + (w - new_w) / 2), y, int(new_w), int(new_h))
        else:
            aspect_ratio = self.video_metadata.get('height', 1080) / self.video_metadata.get('width', 1920)
            new_h = w * aspect_ratio
            new_w = w
            qrect = QRect(x, int(y + ((h - new_h) / 2)), int(new_w), int(new_h))

        if just_get_qrect:
            return [int(qrect.x()), int(qrect.y()), int(qrect.width()), int(qrect.height())]
        else:
            self.player_border.setGeometry(qrect)

    # if self.video_metadata.get('width', 1920) > self.video_metadata.get('height', 1080):
    #     wp = 1
    #     hp = self.video_metadata.get('height', 1080) / self.video_metadata.get('width', 1920)
    # else:
    #     wp = self.video_metadata.get('width', 1920) / self.video_metadata.get('height', 1080)
    #     hp = 1

    # self.video_metadata.get('width', 1920) / self.video_metadata.get('height', 1080)
    # if self.video_metadata.get('width', 640) > self.video_metadata.get('height', 480):
    #    heigth_proportion = ((self.player_widget_area.width()*.7)-6) / self.video_metadata.get('width', 640)
    #    self.player_widget.setGeometry((self.width()*.2) + 3, (self.player_widget_area.height()*.5)-((heigth_proportion*self.video_metadata.get('height', 480))*.5), (self.player_widget_area.width()*.7)-6, self.video_metadata.get('height', 480)*heigth_proportion)
    # else:
    #    width_proportion = (self.player_widget_area.height()-7) / self.video_metadata.get('height', 480)
    #    self.player_widget.setGeometry((self.width()*.2) + ((self.player_widget_area.width()*.7)*.5)-((width_proportion*self.video_metadata.get('width', 640))*.5), 3, self.video_metadata.get('width', 640)*width_proportion, self.player_widget_area.height()-6)
    # self.player_border.setGeometry(self.player_widget.x()-3, self.player_widget.y()-3, self.player_widget.width()+6, self.player_widget.height()+6)
    # self.player_subtitle_layer.setGeometry(self.player_widget.x(), self.player_widget.y(), self.player_widget.width(), self.player_widget.height())
    # self.player_subtitle_textedit.setGeometry(self.player_widget.x()+(self.player_widget.width()*.1), self.player_widget.y()+(self.player_widget.height()*.5), self.player_widget.width()*.8, self.player_widget.height()*.4)


def update_controls(self):
    playercontrols.playercontrols_stop_button_clicked(self)


def update_timelines(self):
    self.timeline.update(self)
    if not self.subtitles_panel_findandreplace_panel.isVisible():
        subtitles_panel.update_subtitles_panel_widget_vision_content(self)
