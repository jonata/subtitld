#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
from PyQt5.QtWidgets import QPushButton, QLabel, QFileDialog, QLineEdit
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, Qt, QThread, pyqtSignal, QSize, QPropertyAnimation
from PyQt5.QtGui import QIcon

from modules import waveform

def load(self, PATH_SUBTITLD_GRAPHICS):
    self.playercontrols_widget = QLabel(parent=self)
    self.playercontrols_widget_animation = QPropertyAnimation(self.playercontrols_widget, b'geometry')
    self.playercontrols_widget_animation.setEasingCurve(QEasingCurve.OutCirc)

    self.playercontrols_widget_central = QLabel(parent=self.playercontrols_widget)
    self.playercontrols_widget_central.setObjectName('playercontrols_widget_central')

    self.playercontrols_widget_right = QLabel(parent=self.playercontrols_widget)
    self.playercontrols_widget_right.setObjectName('playercontrols_widget_right')

    self.playercontrols_widget_left = QLabel(parent=self.playercontrols_widget)
    self.playercontrols_widget_left.setObjectName('playercontrols_widget_left')

    self.playercontrols_stop_button = QPushButton(parent=self.playercontrols_widget_central)
    self.playercontrols_stop_button.setObjectName('button_no_right')
    self.playercontrols_stop_button.setIcon(QIcon(os.path.join(PATH_SUBTITLD_GRAPHICS, 'stop_icon.png')))
    self.playercontrols_stop_button.clicked.connect(lambda:playercontrols_stop_button_clicked(self))

    self.playercontrols_playpayse_button = QPushButton(parent=self.playercontrols_widget_central)
    self.playercontrols_playpayse_button.setObjectName('button_no_left')
    self.playercontrols_playpayse_button.setIcon(QIcon(os.path.join(PATH_SUBTITLD_GRAPHICS, 'play_icon.png')))
    self.playercontrols_playpayse_button.clicked.connect(lambda:playercontrols_playpause_button_clicked(self))

def playercontrols_stop_button_clicked(self):
    self.player_widget.mpv.pause = True
    self.player_widget.mpv.seek(0, reference='absolute', precision='exact')
    self.mediaplayer_is_playing = False

def playercontrols_playpause_button_clicked(self):
    self.player.playpause(self)

def resized(self):
    if self.subtitles_list:
        self.playercontrols_widget.setGeometry(0,self.height()-200,self.width(),200)
    else:
        self.playercontrols_widget.setGeometry(0,self.height(),self.width(),200)
    pc_width = 400
    self.playercontrols_widget_central.setGeometry((self.playercontrols_widget.width()*.5)-(pc_width*.5),0,pc_width,self.playercontrols_widget.height())
    self.playercontrols_widget_right.setGeometry((self.playercontrols_widget.width()*.5)+(pc_width*.5),0,(self.playercontrols_widget.width()*.5)-(pc_width*.5),self.playercontrols_widget.height())
    self.playercontrols_widget_left.setGeometry(0,0,(self.playercontrols_widget.width()*.5)-(pc_width*.5),self.playercontrols_widget.height())
    self.playercontrols_stop_button.setGeometry((pc_width*.5)-45,28,45,45)
    self.playercontrols_playpayse_button.setGeometry((pc_width*.5),28,45,45)

def show(self):
    self.generate_effect(self.playercontrols_widget_animation, 'geometry', 1000, [self.playercontrols_widget.x(),self.playercontrols_widget.y(),self.playercontrols_widget.width(),self.playercontrols_widget.height()], [self.playercontrols_widget.x(), self.height()-200, self.playercontrols_widget.width(),self.playercontrols_widget.height()])
