#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QLabel, QComboBox
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve

from modules.paths import LIST_OF_SUPPORTED_SUBTITLE_EXTENSIONS


def load(self, PATH_SUBTITLD_GRAPHICS):
    self.global_subtitlesvideo_panel_widget = QLabel(parent=self)
    self.global_subtitlesvideo_panel_widget_animation = QPropertyAnimation(self.global_subtitlesvideo_panel_widget, b'geometry')
    self.global_subtitlesvideo_panel_widget_animation.setEasingCurve(QEasingCurve.OutCirc)

    self.global_subtitlesvideo_panel_left = QLabel(parent=self.global_subtitlesvideo_panel_widget)
    self.global_subtitlesvideo_panel_left.setObjectName('global_subtitlesvideo_panel_left')
    self.global_subtitlesvideo_panel_right = QLabel(parent=self.global_subtitlesvideo_panel_widget)
    self.global_subtitlesvideo_panel_right.setObjectName('global_subtitlesvideo_panel_right')

    self.global_subtitlesvideo_save_as_label = QLabel(u'FORMAT TO SAVE:', parent=self.global_subtitlesvideo_panel_widget)

    list_of_subtitle_extensions = []
    for ext in LIST_OF_SUPPORTED_SUBTITLE_EXTENSIONS:
        list_of_subtitle_extensions.append(ext + ' - ' + LIST_OF_SUPPORTED_SUBTITLE_EXTENSIONS[ext]['description'])
    self.global_subtitlesvideo_save_as_combobox = QComboBox(parent=self.global_subtitlesvideo_panel_widget)
    self.global_subtitlesvideo_save_as_combobox.addItems(list_of_subtitle_extensions)
    self.global_subtitlesvideo_save_as_combobox.activated.connect(lambda: global_subtitlesvideo_save_as_combobox_activated(self))


def resized(self):
    if (self.subtitles_list or self.video_metadata):
        if self.subtitles_list_toggle_button.isChecked():
            self.global_subtitlesvideo_panel_widget.setGeometry(0, 0, self.width()*.8, self.height()-self.playercontrols_widget.height()+20)
        else:
            self.global_subtitlesvideo_panel_widget.setGeometry(-(self.width()*.6)-18, 0, self.width()*.8, self.height()-self.playercontrols_widget.height()+20)
    else:
        self.global_subtitlesvideo_panel_widget.setGeometry(-(self.width()*.8), 0, self.width()*.8, self.height()-self.playercontrols_widget.height()+20)

    self.global_subtitlesvideo_panel_left.setGeometry(0, 0, self.width()*.2, self.global_subtitlesvideo_panel_widget.height())
    self.global_subtitlesvideo_panel_right.setGeometry(self.global_subtitlesvideo_panel_left.width(), 0, self.global_subtitlesvideo_panel_widget.width()-self.global_subtitlesvideo_panel_left.width(), self.global_subtitlesvideo_panel_widget.height())

    self.global_subtitlesvideo_save_as_label.setGeometry(20, 20, self.global_subtitlesvideo_panel_left.width()-40, 20)
    self.global_subtitlesvideo_save_as_combobox.setGeometry(20, 40, self.global_subtitlesvideo_panel_left.width()-40, 30)


def show_global_subtitlesvideo_panel(self):
    self.generate_effect(self.global_subtitlesvideo_panel_widget_animation, 'geometry', 700, [self.global_subtitlesvideo_panel_widget.x(), self.global_subtitlesvideo_panel_widget.y(), self.global_subtitlesvideo_panel_widget.width(), self.global_subtitlesvideo_panel_widget.height()], [0, self.global_subtitlesvideo_panel_widget.y(), self.global_subtitlesvideo_panel_widget.width(), self.global_subtitlesvideo_panel_widget.height()])


def hide_global_subtitlesvideo_panel(self):
    self.generate_effect(self.global_subtitlesvideo_panel_widget_animation, 'geometry', 700, [self.global_subtitlesvideo_panel_widget.x(), self.global_subtitlesvideo_panel_widget.y(), self.global_subtitlesvideo_panel_widget.width(), self.global_subtitlesvideo_panel_widget.height()], [int(-(self.width()*.6))-18, self.global_subtitlesvideo_panel_widget.y(), self.global_subtitlesvideo_panel_widget.width(), self.global_subtitlesvideo_panel_widget.height()])


def update_global_subtitlesvideo_save_as_combobox(self):
    self.global_subtitlesvideo_save_as_combobox.setCurrentText(self.format_to_save + ' - ' + LIST_OF_SUPPORTED_SUBTITLE_EXTENSIONS[self.format_to_save]['description'])


def global_subtitlesvideo_save_as_combobox_activated(self):
    self.format_to_save = self.global_subtitlesvideo_save_as_combobox.currentText().split(' ', 1)[0]
