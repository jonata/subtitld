#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os

from modules import file_io

from PyQt5.QtWidgets import QPushButton, QLabel, QFileDialog, QSpinBox, QDoubleSpinBox, QListWidget, QListView
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, Qt, QSize

def load(self, path_catptilr_graphics):
    self.properties_widget = QLabel(parent=self)
    self.properties_widget.setObjectName('properties_widget')

    self.properties_widget_alert = QLabel('There is no subtitle to show. Please select a subtitle.', parent=self.properties_widget)
    self.properties_widget_alert.setWordWrap(True)
    self.properties_widget_alert.setObjectName('subtitles_list_widget_alert')

def resized(self):
    self.properties_widget.setGeometry((self.width()*.8)+15,0,(self.width()*.2)-15,self.height()-185)
    self.properties_widget_alert.setGeometry(2,0,self.subtitles_list_widget.width()-2, self.subtitles_list_widget.height())

def save_button_clicked(self):
    if not self.actual_subtitle_file:
        self.actual_subtitle_file = QFileDialog.getSaveFileName(self, "Select the srt file", os.path.join(os.environ.get('HOME', None), 'final.srt'), "SRT file (*.srt)")[0]
    if self.actual_subtitle_file:
        file_io.save_file(self.actual_subtitle_file, self.properties)

def open_button_clicked(self):
    file_to_open = QFileDialog.getOpenFileName(self, "Select the subtitle or video file", os.path.expanduser("~"), "SRT file (*.srt);;MP4 file (*.mp4)")[0]
    if file_to_open and os.path.isfile(file_to_open):
        self.properties = file_io.open_file(file_to_open)
        update_properties_widget(self)

def update_properties_widget(self):
    self.properties_widget_alert.setVisible(not bool(self.selected_subtitle))
