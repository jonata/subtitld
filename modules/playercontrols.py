#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
from PyQt5.QtWidgets import QPushButton, QLabel, QFileDialog, QLineEdit
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, Qt, QThread, pyqtSignal, QSize, QPropertyAnimation
from PyQt5.QtGui import QIcon

from modules import waveform
from modules.paths import *

def load(self, PATH_SUBTITLD_GRAPHICS):
    self.playercontrols_widget = QLabel(parent=self)
    self.playercontrols_widget.setObjectName('playercontrols_widget')
    self.playercontrols_widget_animation = QPropertyAnimation(self.playercontrols_widget, b'geometry')
    self.playercontrols_widget_animation.setEasingCurve(QEasingCurve.OutCirc)

    self.timeline.load(self, PATH_SUBTITLD_GRAPHICS)

    self.playercontrols_widget_central_top_background = QLabel(parent=self.playercontrols_widget)
    self.playercontrols_widget_central_top_background.setObjectName('playercontrols_widget_central_top_background')

    self.playercontrols_widget_central_bottom_background = QLabel(parent=self.playercontrols_widget)
    self.playercontrols_widget_central_bottom_background.setObjectName('playercontrols_widget_central_bottom_background')

    self.playercontrols_widget_central_top = QLabel(parent=self.playercontrols_widget)
    self.playercontrols_widget_central_top.setObjectName('playercontrols_widget_central_top')

    self.playercontrols_widget_central_bottom = QLabel(parent=self.playercontrols_widget)
    self.playercontrols_widget_central_bottom.setObjectName('playercontrols_widget_central_bottom')

    self.playercontrols_widget_top_right = QLabel(parent=self.playercontrols_widget)
    self.playercontrols_widget_top_right.setObjectName('playercontrols_widget_top_right')

    self.playercontrols_widget_top_left = QLabel(parent=self.playercontrols_widget)
    self.playercontrols_widget_top_left.setObjectName('playercontrols_widget_top_left')

    self.playercontrols_widget_bottom_right = QLabel(parent=self.playercontrols_widget)
    self.playercontrols_widget_bottom_right.setObjectName('playercontrols_widget_bottom_right')

    self.playercontrols_widget_bottom_left = QLabel(parent=self.playercontrols_widget)
    self.playercontrols_widget_bottom_left.setObjectName('playercontrols_widget_bottom_left')

    self.playercontrols_stop_button = QPushButton(parent=self.playercontrols_widget_central_top)
    self.playercontrols_stop_button.setObjectName('player_controls_button')
    self.playercontrols_stop_button.setIcon(QIcon(os.path.join(PATH_SUBTITLD_GRAPHICS, 'stop_icon.png')))
    self.playercontrols_stop_button.clicked.connect(lambda:playercontrols_stop_button_clicked(self))

    self.playercontrols_playpayse_button = QPushButton(parent=self.playercontrols_widget_central_top)
    self.playercontrols_playpayse_button.setObjectName('player_controls_button')
    self.playercontrols_playpayse_button.setCheckable(True)
    self.playercontrols_playpayse_button.setIcon(QIcon(os.path.join(PATH_SUBTITLD_GRAPHICS, 'play_icon.png')))
    self.playercontrols_playpayse_button.clicked.connect(lambda:playercontrols_playpause_button_clicked(self))

    self.playercontrols_timecode_label = QLabel(parent=self.playercontrols_widget_central_bottom)
    self.playercontrols_timecode_label.setObjectName('playercontrols_timecode_label')

    self.zoomin_button = QPushButton(parent=self.playercontrols_widget)
    self.zoomin_button.setIconSize(QSize(16,17))
    self.zoomin_button.setIcon(QIcon(os.path.join(PATH_SUBTITLD_GRAPHICS, 'zoom_in_icon.png')))
    self.zoomin_button.setObjectName('button_no_left_no_bottom')
    self.zoomin_button.clicked.connect(lambda:zoomin_button_clicked(self))

    self.zoomout_button = QPushButton(parent=self.playercontrols_widget)
    self.zoomout_button.setIconSize(QSize(16,17))
    self.zoomout_button.setIcon(QIcon(os.path.join(PATH_SUBTITLD_GRAPHICS, 'zoom_out_icon.png')))
    self.zoomout_button.setObjectName('button_no_right_no_bottom')
    self.zoomout_button.clicked.connect(lambda:zoomout_button_clicked(self))

def playercontrols_stop_button_clicked(self):
    self.player_widget.mpv.pause = True
    self.player_widget.mpv.wait_for_property('seekable')
    self.player_widget.mpv.seek(0, reference='absolute')#, precision='exact')
    self.mediaplayer_is_playing = False
    self.playercontrols_playpayse_button.setChecked(False)
    playercontrols_playpause_button_update(self)

def playercontrols_playpause_button_clicked(self):
    self.player.playpause(self)
    playercontrols_playpause_button_update(self)

def playercontrols_playpause_button_update(self):
    self.playercontrols_playpayse_button.setIcon(QIcon(os.path.join(PATH_SUBTITLD_GRAPHICS, 'pause_icon.png')) if self.playercontrols_playpayse_button.isChecked() else QIcon(os.path.join(PATH_SUBTITLD_GRAPHICS, 'play_icon.png')) )

def resized(self):
    if self.subtitles_list:
        self.playercontrols_widget.setGeometry(0,self.height()-200,self.width(),200)
    else:
        self.playercontrols_widget.setGeometry(0,self.height(),self.width(),200)
    #top_width = 400
    top_width = 300
    bottom_width = 120
    self.playercontrols_widget_central_top_background.setGeometry((self.playercontrols_widget.width()*.5)-(top_width*.5),10,top_width,45)
    self.playercontrols_widget_central_bottom_background.setGeometry((self.playercontrols_widget.width()*.5)-(bottom_width*.5),62,bottom_width,22)
    self.playercontrols_widget_central_top.setGeometry((self.playercontrols_widget.width()*.5)-(top_width*.5),0,top_width,60)
    self.playercontrols_widget_central_bottom.setGeometry((self.playercontrols_widget.width()*.5)-(bottom_width*.5),60,bottom_width,26)
    self.playercontrols_timecode_label.setGeometry(0,0,self.playercontrols_widget_central_bottom.width(),self.playercontrols_widget_central_bottom.height())

    self.playercontrols_widget_top_right.setGeometry(self.playercontrols_widget_central_top.x() + self.playercontrols_widget_central_top.width(),self.playercontrols_widget_central_top.y(),self.playercontrols_widget.width()-(self.playercontrols_widget_central_top.x() + self.playercontrols_widget_central_top.width()),self.playercontrols_widget_central_top.height())
    self.playercontrols_widget_top_left.setGeometry(0,self.playercontrols_widget_central_top.y(),self.playercontrols_widget.width()-(self.playercontrols_widget_central_top.x() + self.playercontrols_widget_central_top.width()),self.playercontrols_widget_central_top.height())
    self.playercontrols_widget_bottom_right.setGeometry(self.playercontrols_widget_central_bottom.x() + self.playercontrols_widget_central_bottom.width(),self.playercontrols_widget_central_bottom.y(),self.playercontrols_widget.width()-(self.playercontrols_widget_central_bottom.x() + self.playercontrols_widget_central_bottom.width()),self.playercontrols_widget_central_bottom.height())
    self.playercontrols_widget_bottom_left.setGeometry(0,self.playercontrols_widget_central_bottom.y(),self.playercontrols_widget_central_bottom.x(),self.playercontrols_widget_central_bottom.height())


    #self.playercontrols_widget_central.setGeometry((self.playercontrols_widget.width()*.5)-(top_width*.5),0,top_width,self.playercontrols_widget.height())
    #self.playercontrols_widget_right.setGeometry((self.playercontrols_widget.width()*.5)+(top_width*.5),0,(self.playercontrols_widget.width()*.5)-(top_width*.5),self.playercontrols_widget.height())
    #self.playercontrols_widget_left.setGeometry(0,0,(self.playercontrols_widget.width()*.5)-(top_width*.5),self.playercontrols_widget.height())
    self.playercontrols_stop_button.setGeometry((self.playercontrols_widget_central_top.width()*.5)-80,11,50,43)
    self.playercontrols_playpayse_button.setGeometry((self.playercontrols_widget_central_top.width()*.5)-30,11,60,43)


    self.zoomin_button.setGeometry(self.timeline_scroll.width() - 80,44,40,40)
    self.zoomout_button.setGeometry(self.timeline_scroll.width() - 120,44,40,40)

def show(self):
    self.generate_effect(self.playercontrols_widget_animation, 'geometry', 1000, [self.playercontrols_widget.x(),self.playercontrols_widget.y(),self.playercontrols_widget.width(),self.playercontrols_widget.height()], [self.playercontrols_widget.x(), self.height()-200, self.playercontrols_widget.width(),self.playercontrols_widget.height()])


def zoomin_button_clicked(self):
    self.mediaplayer_zoom += 5.0
    self.timeline_widget.setGeometry(0,0,int(round(self.video_metadata.get('duration', 0.01)*self.mediaplayer_zoom)),self.timeline_scroll.height()-20)
    self.timeline.zoom_update_waveform(self)
    zoom_buttons_update(self)

def zoomout_button_clicked(self):
    self.mediaplayer_zoom -= 5.0
    self.timeline_widget.setGeometry(0,0,int(round(self.video_metadata.get('duration', 0.01)*self.mediaplayer_zoom)),self.timeline_scroll.height()-20)
    self.timeline.zoom_update_waveform(self)
    zoom_buttons_update(self)

def zoom_buttons_update(self):
    self.zoomout_button.setEnabled(True if self.mediaplayer_zoom - 5.0 > 0.0 else False)
    self.zoomin_button.setEnabled(True if self.mediaplayer_zoom + 5.0 < 500.0 else False)
