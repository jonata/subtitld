from PySide6.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QFrame, QStackedWidget, QPushButton
from PySide6.QtCore import QPropertyAnimation, QEasingCurve

from subtitld.interface import global_panel_general, global_panel_import, global_panel_interface, global_panel_keyboardshortcuts, global_panel_qualitycontrol, global_panel_translation, global_panel_transcription, global_panel_export

# from azure.cognitiveservices.speech import AudioDataStream, SpeechConfig, SpeechSynthesizer, SpeechSynthesisOutputFormat
# from azure.cognitiveservices.speech.audio import AudioOutputConfig
# from pydub import AudioSegment


def load(self):
    """Function to load subtitles panel widgets"""
    self.global_panel_widget = QLabel(parent=self)
    self.global_panel_widget.setLayout(QHBoxLayout())
    self.global_panel_widget.layout().setContentsMargins(0, 0, 0, 0)
    self.global_panel_widget.layout().setSpacing(0)
    self.global_panel_widget_animation = QPropertyAnimation(self.global_panel_widget, b'geometry')
    self.global_panel_widget_animation.setEasingCurve(QEasingCurve.OutCirc)

    self.global_panel_menu = QFrame()
    self.global_panel_menu.setObjectName('global_panel_menu')
    self.global_panel_menu.setFixedWidth(300)
    self.global_panel_menu.setLayout(QVBoxLayout())
    self.global_panel_menu.layout().setContentsMargins(0, 0, 0, 0)
    self.global_panel_menu.layout().setSpacing(0)

    global_panel_general.load_menu(self)
    global_panel_interface.load_menu(self)
    global_panel_keyboardshortcuts.load_menu(self)
    global_panel_qualitycontrol.load_menu(self)
    global_panel_transcription.load_menu(self)
    global_panel_translation.load_menu(self)
    global_panel_import.load_menu(self)
    global_panel_export.load_menu(self)

    self.global_panel_menu.layout().addStretch()
    self.global_panel_widget.layout().addWidget(self.global_panel_menu)

    self.global_panel_content = QFrame()
    self.global_panel_content.setObjectName('global_panel_content')
    self.global_panel_content.setLayout(QVBoxLayout())
    self.global_panel_content.layout().setContentsMargins(20, 20, 30, 20)
    self.global_panel_content.layout().setSpacing(0)

    self.global_panel_content_stacked_widgets = QStackedWidget()
    self.global_panel_content.layout().addWidget(self.global_panel_content_stacked_widgets)

    global_panel_general.load_widgets(self)
    global_panel_interface.load_widgets(self)
    global_panel_keyboardshortcuts.load_widgets(self)
    global_panel_qualitycontrol.load_widgets(self)
    global_panel_translation.load_widgets(self)
    global_panel_transcription.load_widgets(self)
    global_panel_import.load_widgets(self)
    global_panel_export.load_widgets(self)

    self.global_panel_widget.layout().addWidget(self.global_panel_content)

    global_panel_menu_changed(self, self.global_panel_general_menu_button, self.global_panel_general_content)


def resized(self):
    """Function on resizing widgets"""
    x = - self.width()
    if (self.subtitles_list or self.video_metadata):
        if self.subtitles_panel_toggle_button.isChecked():
            x = 0
        else:
            x = - self.width() + 20 + self.subtitles_panel_widget.width()
    self.global_panel_widget.setGeometry(x, 0, self.width() - 20, self.height())


def show_global_panel(self):
    """Function to show subtitlesvideo panel"""
    self.generate_effect(self.global_panel_widget_animation, 'geometry', 700, [self.global_panel_widget.x(), self.global_panel_widget.y(), self.global_panel_widget.width(), self.global_panel_widget.height()], [0, self.global_panel_widget.y(), self.global_panel_widget.width(), self.global_panel_widget.height()])
    self.generate_effect(self.player_border_transparency_animation, 'opacity', 200, 1.0, 0.0)
    self.global_panel_general_menu_button.setChecked(True)
    # self.player_widget.hold_update = True


def hide_global_panel(self):
    # self.player_widget.hold_update = False
    self.generate_effect(self.global_panel_widget_animation, 'geometry', 700, [self.global_panel_widget.x(), self.global_panel_widget.y(), self.global_panel_widget.width(), self.global_panel_widget.height()], [int(-self.global_panel_widget.width() + self.subtitles_panel_widget.width()), self.global_panel_widget.y(), self.global_panel_widget.width(), self.global_panel_widget.height()])
    self.generate_effect(self.player_border_transparency_animation, 'opacity', 200, 0.0, 1.0)


def global_panel_menu_changed(self, button, widget):
    for w in self.global_panel_menu.findChildren(QPushButton):
        if w != button:
            w.setChecked(False)
            w.setEnabled(True)
    self.global_panel_content_stacked_widgets.setCurrentWidget(widget)


def translate_widgets(self):
    global_panel_general.translate_widgets(self)
    global_panel_interface.translate_widgets(self)
    global_panel_keyboardshortcuts.translate_widgets(self)
    global_panel_qualitycontrol.translate_widgets(self)
    global_panel_translation.translate_widgets(self)
    global_panel_transcription.translate_widgets(self)
    global_panel_import.translate_widgets(self)
    global_panel_export.translate_widgets(self)