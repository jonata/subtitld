#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton, QLabel, QFileDialog, QSpinBox, QDoubleSpinBox, QWidget, QScrollArea
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, Qt, QSize

def load(self, PATH_SUBTITLD_GRAPHICS):

            self.start_screen = QLabel(parent=self)

            self.start_screen_background = QLabel(parent=self.start_screen)
            self.start_screen_background.setStyleSheet('QLabel { border-left: 80px; border-top:80px; border-image: url("' + os.path.join(PATH_SUBTITLD_GRAPHICS, 'start_screen_background.png').replace('\\', '/') + '") 1 1 0 1 stretch stretch; \
                                                        image: url("' + os.path.join(PATH_SUBTITLD_GRAPHICS, 'start_screen_logo.png').replace('\\', '/') + '"); qproperty-alignment: "AlignCenter";}')

            self.start_screen_right = QLabel(parent=self.start_screen)
            self.start_screen_right.setStyleSheet('QLabel { border-top:80px; border-image: url("' + os.path.join(PATH_SUBTITLD_GRAPHICS, 'start_screen_background.png').replace('\\', '/') + '") 1 0 0 49 stretch stretch; }')

            self.start_screen_open_text = QLabel('Open a karaoke txt file or a mp3/oga file to start.', parent=self.start_screen)
            #self.start_screen_open_text.setWordWrap(True)
            self.start_screen_open_text.setStyleSheet('QLabel { font-size:12px; color:gray; qproperty-alignment: "AlignVCenter | AlignLeft"; qproperty-wordWrap: true}')

            self.start_screen_open_button = QPushButton('OPEN', parent=self.start_screen)
            self.start_screen_open_button.clicked.connect(lambda:self.top_bar.open_button_clicked(self))
            self.start_screen_open_button.setStyleSheet('QPushButton { font-size:12px; color:white; border-left: 5px; border-top: 5px; border-right: 5px; border-bottom: 5px; border-image: url("' + os.path.join(PATH_SUBTITLD_GRAPHICS, 'button_4_normal.png').replace('\\', '/') + '") 5 5 5 5 stretch stretch; outline: none; } QPushButton:hover:pressed { border-left: 5px; border-top: 5px; border-right: 5px; border-bottom: 5px; border-image: url("' + os.path.join(PATH_SUBTITLD_GRAPHICS, 'button_4_pressed.png').replace('\\', '/') + '") 5 5 5 5 stretch stretch; outline: none;  } QPushButton:hover { border-left: 5px; border-top: 5px; border-right: 5px; border-bottom: 5px; border-image: url("' + os.path.join(PATH_SUBTITLD_GRAPHICS, 'button_4_hover.png').replace('\\', '/') + '") 5 5 5 5 stretch stretch; outline: none; } ')

            self.start_screen_instructions = QLabel(parent=self.start_screen)
            self.start_screen_instructions.setStyleSheet('QLabel { padding-top: 20px; padding-left: 20px; image: url("' + os.path.join(PATH_SUBTITLD_GRAPHICS, 'start_screen_instructions.png').replace('\\', '/') + '"); qproperty-alignment: "AlignLeft";}')


def resized(self):
    self.start_screen.setGeometry(0,0,self.width(),self.height())
    self.start_screen_background.setGeometry(0,0,680,280)
    self.start_screen_right.setGeometry(self.start_screen_background.x()+self.start_screen_background.width(),self.start_screen_background.y(),self.start_screen.width()-(self.start_screen_background.x()+self.start_screen_background.width()),self.start_screen_background.height())
    self.start_screen_open_text.setGeometry(120,self.start_screen_background.height(),200,60)
    self.start_screen_open_button.setGeometry(self.start_screen_open_text.x(),self.start_screen_open_text.y() + self.start_screen_open_text.height(),200,60)
    self.start_screen_instructions.setGeometry(self.start_screen_open_text.x()+self.start_screen_open_text.width()+20,self.start_screen_open_text.y(),400,180)
