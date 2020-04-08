#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os

from modules import file_io

from PyQt5.QtWidgets import QPushButton, QLabel, QFileDialog, QSpinBox, QDoubleSpinBox, QListWidget, QListView, QTextEdit
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, Qt, QSize

def load(self, path_catptilr_graphics):
    self.properties_widget = QLabel(parent=self)
    self.properties_widget.setObjectName('properties_widget')
    self.properties_widget_animation = QPropertyAnimation(self.properties_widget, b'geometry')
    self.properties_widget_animation.setEasingCurve(QEasingCurve.OutCirc)

    # class properties_textedit(QTextEdit):
    #     def keyPressEvent(self, e):
    #         print("event", e)
    #         if e.key()  == Qt.Key_Return :
    #             print(' return')
    #         elif e.key() == Qt.Key_Enter :
    #             print(' enter')

    self.properties_textedit = QTextEdit(parent=self.properties_widget)
    #self.properties_textedit.setAttribute(Qt.WA_AlwaysStackOnTop)
    #self.properties_textedit.setVisible(False)
    #self.properties_textedit.setWordWrap(True)
    self.properties_textedit.setObjectName('properties_textedit')
    self.properties_textedit.textChanged.connect(lambda:properties_textedit_changed(self))

    self.properties_information = QLabel(parent=self.properties_widget)
    self.properties_information.setObjectName('properties_information')

def resized(self):
    if self.subtitles_list:
        self.properties_widget.setGeometry((self.width()*.8)+15,0,(self.width()*.2)-15,self.height())
    else:
        self.properties_widget.setGeometry(self.width(),0,(self.width()*.2)-15,self.height())
    self.properties_textedit.setGeometry(20,20,self.properties_widget.width()-40,200)
    self.properties_information.setGeometry(20,220,self.properties_widget.width()-40,self.properties_widget.height()-400)

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
    text = ''
    if self.selected_subtitle:
        self.properties_information.setText('<small>WORDS:</small><br><big><b>' + str(len(self.selected_subtitle[2].replace('\n', ' ').split(' '))) + '</b></big><br><br><small>CHARACTERS:</small><br><big><b>' + str(len(self.selected_subtitle[2].replace('\n', '').replace(' ', ''))) + '</b></big>')
        text = self.selected_subtitle[2]


    self.properties_information.setVisible(bool(self.selected_subtitle))
    self.properties_textedit.setVisible(bool(text))
    #self.properties_textedit.textChanged.disconnect()
    self.properties_textedit.setText(text)
    #self.properties_textedit.textChanged.connect()


def show(self):
    self.generate_effect(self.properties_widget_animation, 'geometry', 700, [self.properties_widget.x(),self.properties_widget.y(),self.properties_widget.width(),self.properties_widget.height()], [int((self.width()*.8)+15), self.properties_widget.y(), self.properties_widget.width(),self.properties_widget.height()])

def properties_textedit_changed(self):
    old_selected_subtitle = self.selected_subtitle
    if old_selected_subtitle:
        counter = self.subtitles_list.index(old_selected_subtitle)
        self.subtitles_list[counter][2] = self.properties_textedit.toPlainText()
        self.subtitleslist.update_subtitles_list_qlistwidget(self)
        self.timeline.update(self)
        self.player.update_subtitle_layer(self)
