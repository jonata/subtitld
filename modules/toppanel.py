#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton, QLabel, QFileDialog, QSpinBox, QDoubleSpinBox, QListWidget, QListView
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, Qt, QSize

from modules.paths import *
from modules import file_io

def load(self, PATH_SUBTITLD_GRAPHICS):
    self.toppanel_widget = QLabel(parent=self)
    self.toppanel_widget.setObjectName('toppanel_widget')
    self.toppanel_widget_animation = QPropertyAnimation(self.toppanel_widget, b'geometry')
    self.toppanel_widget_animation.setEasingCurve(QEasingCurve.OutCirc)

    self.toppanel_widget_left = QLabel(parent=self.toppanel_widget)
    self.toppanel_widget_left.setObjectName('toppanel_widget_left')

    self.toppanel_subtitle_file_info_label = QLabel(parent=self.toppanel_widget_left)
    self.toppanel_subtitle_file_info_label.setObjectName('toppanel_subtitle_file_info_label')

    self.toppanel_widget_right = QLabel(parent=self.toppanel_widget)
    self.toppanel_widget_right.setObjectName('toppanel_widget_right')

    self.toppanel_toggle_button = QPushButton(parent=self.toppanel_widget_left)
    self.toppanel_toggle_button.setObjectName('toppanel_toggle_button')
    self.toppanel_toggle_button.setCheckable(True)
    self.toppanel_toggle_button.setIcon(QIcon(os.path.join(PATH_SUBTITLD_GRAPHICS, 'toppanel_button_switch_icon_down.png')))
    self.toppanel_toggle_button.clicked.connect(lambda: toppanel_toggle_button_clicked(self))

    self.toppanel_videoinfo_label = QLabel(parent=self.toppanel_widget_right)
    self.toppanel_videoinfo_label.setObjectName('toppanel_videoinfo_label')

    self.toppanel_save_button = QPushButton('SAVE', parent=self.toppanel_widget_left)
    self.toppanel_save_button.clicked.connect(lambda:toppanel_save_button_clicked(self))
    self.toppanel_save_button.setObjectName('button_dark_no_left')

    self.toppanel_open_button = QPushButton('OPEN', parent=self.toppanel_widget_left)
    self.toppanel_open_button.clicked.connect(lambda:toppanel_open_button_clicked(self))
    self.toppanel_open_button.setObjectName('button_dark_no_right')

    #self.toppanel_information = QLabel(parent=self.toppanel_widget)
    #self.toppanel_information.setObjectName('toppanel_information')

def resized(self):
    if self.subtitles_list:
        if self.toppanel_toggle_button.isChecked():
            self.toppanel_widget.setGeometry(0,0,(self.width()*.8)-10,self.height()-220)
        else:
            self.toppanel_widget.setGeometry(0,-(self.height()-269),(self.width()*.8)-10,self.height()-220)
    else:
        self.toppanel_widget.setGeometry(0,-(self.height()-220),(self.width()*.8)-10,self.height()-220)
    self.toppanel_widget_left.setGeometry(0,0,(self.width()*.2),self.toppanel_widget.height())
    self.toppanel_widget_right.setGeometry(self.toppanel_widget_left.width(),0,self.toppanel_widget.width()-self.toppanel_widget_left.width(),self.toppanel_widget.height())
    self.toppanel_toggle_button.setGeometry(self.toppanel_widget_left.width()-90,self.toppanel_widget_left.height()-35,80,30)
    self.toppanel_videoinfo_label.setGeometry(10,self.toppanel_widget_right.height()-50,self.toppanel_widget_right.width()-20,48)
    self.toppanel_open_button.setGeometry(20,20,100,30)
    self.toppanel_save_button.setGeometry(120,20,100,30)
    self.toppanel_subtitle_file_info_label.setGeometry(20,self.toppanel_widget_left.height()-50,self.toppanel_widget_left.width()-30,48)
    #self.toppanel_toggle_button.setGeometry(0,0,80,30)

    #self.toppanel_information.setGeometry(20,20,self.toppanel_widget.width()-40,self.toppanel_widget.height()-200)

def toppanel_toggle_button_clicked(self):
    if self.toppanel_toggle_button.isChecked():
        self.generate_effect(self.toppanel_widget_animation, 'geometry', 700, [self.toppanel_widget.x(),self.toppanel_widget.y(),self.toppanel_widget.width(),self.toppanel_widget.height()], [0, 0, self.toppanel_widget.width(),self.toppanel_widget.height()])
    else:
        show(self)
    self.toppanel_subtitle_file_info_label.setVisible(not self.toppanel_toggle_button.isChecked())
    self.toppanel_toggle_button.setIcon(QIcon(os.path.join(PATH_SUBTITLD_GRAPHICS, 'toppanel_button_switch_icon_up.png')) if self.toppanel_toggle_button.isChecked() else QIcon(os.path.join(PATH_SUBTITLD_GRAPHICS, 'toppanel_button_switch_icon_down.png')))

def show(self):
    self.generate_effect(self.toppanel_widget_animation, 'geometry', 700, [self.toppanel_widget.x(),self.toppanel_widget.y(),self.toppanel_widget.width(),self.toppanel_widget.height()], [self.toppanel_widget.x(), -(self.height()-269), self.toppanel_widget.width(),self.toppanel_widget.height()])

def toppanel_save_button_clicked(self):
    if not self.actual_subtitle_file:
        self.actual_subtitle_file = QFileDialog.getSaveFileName(self, "Select the srt file", os.path.join(os.environ.get('HOME', None), 'final.srt'), "SRT file (*.srt)")[0]
    if self.actual_subtitle_file:
        file_io.save_file(self.actual_subtitle_file, self.subtitles_list)

def toppanel_open_button_clicked(self):
    file_to_open = QFileDialog.getOpenFileName(self, "Select the subtitle or video file", os.path.expanduser("~"), "SRT file (*.srt);;MP4 file (*.mp4)")[0]
    if file_to_open and os.path.isfile(file_to_open):
        file_io.open_filepath(self, file_to_open)
