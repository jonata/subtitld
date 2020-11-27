#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os

from modules import file_io
from modules import subtitles

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton, QLabel, QFileDialog, QTextEdit
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, QSize


def load(self, PATH_SUBTITLD_GRAPHICS):
    self.properties_widget = QLabel(parent=self)
    self.properties_widget.setObjectName('properties_widget')
    self.properties_widget_animation = QPropertyAnimation(self.properties_widget, b'geometry')
    self.properties_widget_animation.setEasingCurve(QEasingCurve.OutCirc)

    self.properties_textedit = QTextEdit(parent=self.properties_widget)
    self.properties_textedit.setObjectName('properties_textedit')
    self.properties_textedit.textChanged.connect(lambda: properties_textedit_changed(self))

    self.send_text_to_next_subtitle_button = QPushButton(self.tr('Send to next').upper(), parent=self.properties_widget)
    self.send_text_to_next_subtitle_button.setIcon(QIcon(os.path.join(PATH_SUBTITLD_GRAPHICS, 'send_text_to_next_subtitle_icon.png')))
    self.send_text_to_next_subtitle_button.setIconSize(QSize(20, 20))
    self.send_text_to_next_subtitle_button.setObjectName('button_dark')
    self.send_text_to_next_subtitle_button.setStyleSheet('QPushButton {border-bottom:0; border-left:0;padding-bottom:3px;}')
    self.send_text_to_next_subtitle_button.clicked.connect(lambda: send_text_to_next_subtitle_button_clicked(self))

    self.send_text_to_last_subtitle_button = QPushButton(self.tr('Send to last').upper(), parent=self.properties_widget)
    self.send_text_to_last_subtitle_button.setIcon(QIcon(os.path.join(PATH_SUBTITLD_GRAPHICS, 'send_text_to_last_subtitle_icon.png')))
    self.send_text_to_last_subtitle_button.setIconSize(QSize(20, 20))
    self.send_text_to_last_subtitle_button.setObjectName('button_dark')
    self.send_text_to_last_subtitle_button.setStyleSheet('QPushButton {border-bottom:0; border-right:0;padding-bottom:3px;}')
    self.send_text_to_last_subtitle_button.clicked.connect(lambda: send_text_to_last_subtitle_button_clicked(self))

    self.properties_information = QLabel(parent=self.properties_widget)
    self.properties_information.setObjectName('properties_information')

    self.properties_toggle_button = QPushButton(parent=self)
    self.properties_toggle_button.clicked.connect(lambda: properties_toggle_button_clicked(self))
    self.properties_toggle_button.setCheckable(True)
    self.properties_toggle_button.setObjectName('properties_toggle_button')
    self.properties_toggle_button_animation = QPropertyAnimation(self.properties_toggle_button, b'geometry')
    self.properties_toggle_button_animation.setEasingCurve(QEasingCurve.OutCirc)


def resized(self):
    if self.subtitles_list or self.video_metadata:
        self.properties_widget.setGeometry((self.width()*.8)+15, 0, (self.width()*.2)-15, self.height())
    else:
        self.properties_widget.setGeometry(self.width(), 0, (self.width()*.2)-15, self.height())

    self.properties_textedit.setGeometry(20, self.properties_widget.height()-self.playercontrols_widget.height()-35-180, self.properties_widget.width()-40, 200)
    self.send_text_to_last_subtitle_button.setGeometry(self.properties_textedit.x(), self.properties_textedit.y()-40, self.properties_textedit.width()*.5, 40)
    self.send_text_to_next_subtitle_button.setGeometry(self.send_text_to_last_subtitle_button.x()+self.send_text_to_last_subtitle_button.width(), self.send_text_to_last_subtitle_button.y(), self.properties_textedit.width()*.5, 40)
    self.properties_information.setGeometry(30, 20, self.properties_widget.width()-40, 100)

    if (self.subtitles_list or self.video_metadata):
        self.properties_toggle_button.setGeometry(self.properties_widget.x()+5, 0, 25, 80)
    else:
        self.properties_toggle_button.setGeometry(self.width(), 0, 25, 80)


def properties_toggle_button_clicked(self):
    if self.properties_toggle_button.isChecked():
        hide(self)
        self.global_properties_panel.show_global_properties_panel(self)
        properties_toggle_button_to_end(self)
    else:
        show(self)
        self.global_properties_panel.hide_global_properties_panel(self)


def properties_toggle_button_to_end(self):
    self.generate_effect(self.properties_toggle_button_animation, 'geometry', 700, [self.properties_toggle_button.x(), self.properties_toggle_button.y(), self.properties_toggle_button.width(), self.properties_toggle_button.height()], [int(self.width()*.8), self.properties_toggle_button.y(), self.properties_toggle_button.width(), self.properties_toggle_button.height()])


def save_button_clicked(self):
    if not self.actual_subtitle_file:
        self.actual_subtitle_file = QFileDialog.getSaveFileName(self, self.tr('Select the srt file'), os.path.join(os.environ.get('HOME', None), 'final.srt'), "SRT file (*.srt)")[0]
    if self.actual_subtitle_file:
        file_io.save_file(self.actual_subtitle_file, self.properties)


def open_button_clicked(self):
    file_to_open = QFileDialog.getOpenFileName(self, self.tr('Select the subtitle or video file'), os.path.expanduser("~"), "SRT file (*.srt);;MP4 file (*.mp4)")[0]
    if file_to_open and os.path.isfile(file_to_open):
        self.properties = file_io.open_file(file_to_open)
        update_properties_widget(self)


def update_properties_widget(self):
    text = ''
    if self.selected_subtitle:
        self.properties_information.setText('<small>' + self.tr('Words').upper() + ':</small><br><big><b>' + str(len(self.selected_subtitle[2].replace('\n', ' ').split(' '))) + '</b></big><br><br><small>' + self.tr('Characters').upper() + ':</small><br><big><b>' + str(len(self.selected_subtitle[2].replace('\n', '').replace(' ', ''))) + '</b></big>')
        text = self.selected_subtitle[2]

    self.properties_information.setVisible(bool(self.selected_subtitle))
    self.properties_textedit.setVisible(bool(self.selected_subtitle))
    self.send_text_to_next_subtitle_button.setVisible(bool(self.selected_subtitle))
    self.send_text_to_last_subtitle_button.setVisible(bool(self.selected_subtitle))
    self.properties_textedit.setText(text)


def show(self):
    self.generate_effect(self.properties_widget_animation, 'geometry', 700, [self.properties_widget.x(), self.properties_widget.y(), self.properties_widget.width(), self.properties_widget.height()], [int((self.width()*.8)+15), self.properties_widget.y(), self.properties_widget.width(), self.properties_widget.height()])
    self.generate_effect(self.properties_toggle_button_animation, 'geometry', 700, [self.properties_toggle_button.x(), self.properties_toggle_button.y(), self.properties_toggle_button.width(), self.properties_toggle_button.height()], [int((self.width()*.8)+18), self.properties_toggle_button.y(), self.properties_toggle_button.width(), self.properties_toggle_button.height()])
    self.global_properties_panel.hide_global_properties_panel(self)

    # if not self.advanced_mode:
    #     self.properties_toggle_button.setEnabled(False)


def hide(self):
    self.generate_effect(self.properties_widget_animation, 'geometry', 700, [self.properties_widget.x(), self.properties_widget.y(), self.properties_widget.width(), self.properties_widget.height()], [int(self.width()), self.properties_widget.y(), self.properties_widget.width(), self.properties_widget.height()])


def properties_textedit_changed(self):
    old_selected_subtitle = self.selected_subtitle
    if old_selected_subtitle:
        counter = self.subtitles_list.index(old_selected_subtitle)
        self.subtitles_list[counter][2] = self.properties_textedit.toPlainText()
        self.subtitleslist.update_subtitles_list_qlistwidget(self)
        self.timeline.update(self)
        self.player.update_subtitle_layer(self)


def send_text_to_next_subtitle_button_clicked(self):
    pos = self.properties_textedit.textCursor().position()
    last_text = self.properties_textedit.toPlainText()[:pos]
    next_text = self.properties_textedit.toPlainText()[pos:]
    subtitles.send_text_to_next_subtitle(subtitles=self.subtitles_list, selected_subtitle=self.selected_subtitle, last_text=last_text, next_text=next_text)
    self.subtitleslist.update_subtitles_list_qlistwidget(self)
    self.timeline.update(self)
    self.properties.update_properties_widget(self)


def send_text_to_last_subtitle_button_clicked(self):
    pos = self.properties_textedit.textCursor().position()
    last_text = self.properties_textedit.toPlainText()[:pos]
    next_text = self.properties_textedit.toPlainText()[pos:]
    subtitles.send_text_to_last_subtitle(subtitles=self.subtitles_list, selected_subtitle=self.selected_subtitle, last_text=last_text, next_text=next_text)
    self.subtitleslist.update_subtitles_list_qlistwidget(self)
    self.timeline.update(self)
    self.properties.update_properties_widget(self)
