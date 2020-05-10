#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
from bisect import bisect
from PyQt5.QtWidgets import QPushButton, QLabel, QFileDialog, QLineEdit, QDoubleSpinBox, QSlider, QSpinBox
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, Qt, pyqtSignal, QSize, QPropertyAnimation
from PyQt5.QtGui import QIcon

from modules import waveform
from modules import subtitles
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

    self.playercontrols_play_from_last_start_button = QPushButton(parent=self.playercontrols_widget_central_top)
    self.playercontrols_play_from_last_start_button.setObjectName('player_controls_button')
    self.playercontrols_play_from_last_start_button.setIcon(QIcon(os.path.join(PATH_SUBTITLD_GRAPHICS, 'play_from_last_start_icon.png')))
    self.playercontrols_play_from_last_start_button.setIconSize(QSize(24,24))
    #self.playercontrols_play_from_last_start_button.setStyleSheet('QPushButton {image: url(' + os.path.join(PATH_SUBTITLD_GRAPHICS, 'play_from_last_start_icon.png') + ');}')
    self.playercontrols_play_from_last_start_button.clicked.connect(lambda:playercontrols_play_from_last_start_button_clicked(self))

    self.playercontrols_stop_button = QPushButton(parent=self.playercontrols_widget_central_top)
    self.playercontrols_stop_button.setObjectName('player_controls_button')
    self.playercontrols_stop_button.setIcon(QIcon(os.path.join(PATH_SUBTITLD_GRAPHICS, 'stop_icon.png')))
    self.playercontrols_stop_button.setIconSize(QSize(15,15))
    self.playercontrols_stop_button.clicked.connect(lambda:playercontrols_stop_button_clicked(self))

    self.playercontrols_playpause_button = QPushButton(parent=self.playercontrols_widget_central_top)
    self.playercontrols_playpause_button.setObjectName('player_controls_button')
    self.playercontrols_playpause_button.setCheckable(True)
    self.playercontrols_playpause_button.setIcon(QIcon(os.path.join(PATH_SUBTITLD_GRAPHICS, 'play_icon.png')))
    self.playercontrols_playpause_button.setIconSize(QSize(20,20))
    self.playercontrols_playpause_button.clicked.connect(lambda:playercontrols_playpause_button_clicked(self))

    self.playercontrols_play_from_next_start_button = QPushButton(parent=self.playercontrols_widget_central_top)
    self.playercontrols_play_from_next_start_button.setObjectName('player_controls_button')
    self.playercontrols_play_from_next_start_button.setIcon(QIcon(os.path.join(PATH_SUBTITLD_GRAPHICS, 'play_from_next_start_icon.png')))
    self.playercontrols_play_from_next_start_button.setIconSize(QSize(24,24))
    self.playercontrols_play_from_next_start_button.clicked.connect(lambda:playercontrols_play_from_next_start_button_clicked(self))

    self.add_subtitle_button = QPushButton('ADD', parent=self.playercontrols_widget)
    self.add_subtitle_button.setIcon(QIcon(os.path.join(PATH_SUBTITLD_GRAPHICS, 'add_subtitle_icon.png')))
    self.add_subtitle_button.setIconSize(QSize(20,20))
    self.add_subtitle_button.setObjectName('button_dark')
    self.add_subtitle_button.setStyleSheet('QPushButton {padding-right:50px; border-right:0; border-bottom:0;}')
    self.add_subtitle_button.clicked.connect(lambda:add_subtitle_button_clicked(self))

    self.add_subtitle_duration = QDoubleSpinBox(parent=self.add_subtitle_button)
    self.add_subtitle_duration.setMinimum(.1)
    self.add_subtitle_duration.setMaximum(60.)
    self.add_subtitle_duration.valueChanged.connect(lambda:add_subtitle_duration_changed(self))

    self.remove_selected_subtitle_button = QPushButton('REMOVE', parent=self.playercontrols_widget)
    self.remove_selected_subtitle_button.setIcon(QIcon(os.path.join(PATH_SUBTITLD_GRAPHICS, 'remove_selected_subtitle_icon.png')))
    self.remove_selected_subtitle_button.setIconSize(QSize(20,20))
    self.remove_selected_subtitle_button.setObjectName('button_dark')
    self.remove_selected_subtitle_button.setStyleSheet('QPushButton { border-left:0; border-bottom:0;}')
    self.remove_selected_subtitle_button.clicked.connect(lambda:remove_selected_subtitle_button_clicked(self))

    self.merge_back_selected_subtitle_button = QPushButton(parent=self.playercontrols_widget)
    self.merge_back_selected_subtitle_button.setIcon(QIcon(os.path.join(PATH_SUBTITLD_GRAPHICS, 'merge_back_selected_subtitle_icon.png')))
    self.merge_back_selected_subtitle_button.setIconSize(QSize(20,20))
    self.merge_back_selected_subtitle_button.setObjectName('button_dark')
    self.merge_back_selected_subtitle_button.setStyleSheet('QPushButton {border-bottom:0; border-right:0;}')
    self.merge_back_selected_subtitle_button.clicked.connect(lambda:merge_back_selected_subtitle_button_clicked(self))

    self.slice_selected_subtitle_button = QPushButton(parent=self.playercontrols_widget)
    self.slice_selected_subtitle_button.setIcon(QIcon(os.path.join(PATH_SUBTITLD_GRAPHICS, 'slice_selected_subtitle_icon.png')))
    self.slice_selected_subtitle_button.setIconSize(QSize(20,20))
    self.slice_selected_subtitle_button.setObjectName('button_dark')
    self.slice_selected_subtitle_button.setStyleSheet('QPushButton {border-bottom:0; border-left:0; border-right:0;}')
    self.slice_selected_subtitle_button.clicked.connect(lambda:slice_selected_subtitle_button_clicked(self))

    self.merge_next_selected_subtitle_button = QPushButton(parent=self.playercontrols_widget)
    self.merge_next_selected_subtitle_button.setIcon(QIcon(os.path.join(PATH_SUBTITLD_GRAPHICS, 'merge_next_selected_subtitle_icon.png')))
    self.merge_next_selected_subtitle_button.setIconSize(QSize(20,20))
    self.merge_next_selected_subtitle_button.setObjectName('button_dark')
    self.merge_next_selected_subtitle_button.setStyleSheet('QPushButton {border-bottom:0; border-left:0;}')
    self.merge_next_selected_subtitle_button.clicked.connect(lambda:merge_next_selected_subtitle_button_clicked(self))

    self.playercontrols_timecode_label = QLabel(parent=self.playercontrols_widget_central_bottom)
    self.playercontrols_timecode_label.setObjectName('playercontrols_timecode_label')

    self.zoomin_button = QPushButton(parent=self.playercontrols_widget)
    self.zoomin_button.setIcon(QIcon(os.path.join(PATH_SUBTITLD_GRAPHICS, 'zoom_in_icon.png')))
    self.zoomin_button.setIconSize(QSize(20,20))
    self.zoomin_button.setObjectName('button_dark')
    self.zoomin_button.setStyleSheet('QPushButton {border-bottom:0; border-left:0;}')
    self.zoomin_button.clicked.connect(lambda:zoomin_button_clicked(self))

    self.zoomout_button = QPushButton(parent=self.playercontrols_widget)
    self.zoomout_button.setIcon(QIcon(os.path.join(PATH_SUBTITLD_GRAPHICS, 'zoom_out_icon.png')))
    self.zoomout_button.setIconSize(QSize(20,20))
    self.zoomout_button.setObjectName('button_dark')
    self.zoomout_button.setStyleSheet('QPushButton {border-bottom:0; border-right:0;}')
    self.zoomout_button.clicked.connect(lambda:zoomout_button_clicked(self))

    self.next_start_to_current_position_button = QPushButton(parent=self.playercontrols_widget)
    self.next_start_to_current_position_button.setIcon(QIcon(os.path.join(PATH_SUBTITLD_GRAPHICS, 'next_start_to_current_position_icon.png')))
    self.next_start_to_current_position_button.setIconSize(QSize(20,20))
    self.next_start_to_current_position_button.setObjectName('button_dark')
    self.next_start_to_current_position_button.setStyleSheet('QPushButton {border-bottom:0; border-right:0;}')
    self.next_start_to_current_position_button.clicked.connect(lambda:next_start_to_current_position_button_clicked(self))

    self.last_start_to_current_position_button = QPushButton(parent=self.playercontrols_widget)
    self.last_start_to_current_position_button.setIcon(QIcon(os.path.join(PATH_SUBTITLD_GRAPHICS, 'last_start_to_current_position_icon.png')))
    self.last_start_to_current_position_button.setIconSize(QSize(20,20))
    self.last_start_to_current_position_button.setObjectName('button_dark')
    self.last_start_to_current_position_button.setStyleSheet('QPushButton {border-bottom:0; border-right:0; border-left:0;}')
    self.last_start_to_current_position_button.clicked.connect(lambda:last_start_to_current_position_button_clicked(self))

    self.last_end_to_current_position_button = QPushButton(parent=self.playercontrols_widget)
    self.last_end_to_current_position_button.setIcon(QIcon(os.path.join(PATH_SUBTITLD_GRAPHICS, 'last_end_to_current_position_icon.png')))
    self.last_end_to_current_position_button.setIconSize(QSize(20,20))
    self.last_end_to_current_position_button.setObjectName('button_dark')
    self.last_end_to_current_position_button.setStyleSheet('QPushButton {border-bottom:0; border-left:0;}')
    self.last_end_to_current_position_button.clicked.connect(lambda:last_end_to_current_position_button_clicked(self))

    self.next_end_to_current_position_button = QPushButton(parent=self.playercontrols_widget)
    self.next_end_to_current_position_button.setIcon(QIcon(os.path.join(PATH_SUBTITLD_GRAPHICS, 'next_end_to_current_position_icon.png')))
    self.next_end_to_current_position_button.setIconSize(QSize(20,20))
    self.next_end_to_current_position_button.setObjectName('button_dark')
    self.next_end_to_current_position_button.setStyleSheet('QPushButton {border-bottom:0; border-left:0; border-right:0;}')
    self.next_end_to_current_position_button.clicked.connect(lambda:next_end_to_current_position_button_clicked(self))

    self.change_playback_speed = QPushButton(parent=self.playercontrols_widget)
    self.change_playback_speed.setObjectName('button')
    self.change_playback_speed.setCheckable(True)
    self.change_playback_speed.setStyleSheet('QPushButton {border-top:0; padding-left:36px; text-align:left;}')
    self.change_playback_speed.clicked.connect(lambda:change_playback_speed_clicked(self))

    self.change_playback_speed_icon_label = QLabel(parent=self.change_playback_speed)
    self.change_playback_speed_icon_label.setStyleSheet('QLabel { image: url(' + os.path.join(PATH_SUBTITLD_GRAPHICS, 'playback_speed_icon.png') + ')}')

    self.change_playback_speed_decrease = QPushButton('-', parent=self.change_playback_speed)
    self.change_playback_speed_decrease.setObjectName('button')
    self.change_playback_speed_decrease.setStyleSheet('QPushButton {border-top:5px; padding-left:5px; border-right:0;}')
    self.change_playback_speed_decrease.clicked.connect(lambda:change_playback_speed_decrease_clicked(self))

    self.change_playback_speed_slider = QSlider(orientation=Qt.Horizontal, parent=self.change_playback_speed)
    self.change_playback_speed_slider.setMinimum(5)
    self.change_playback_speed_slider.setMaximum(300)
    self.change_playback_speed_slider.setPageStep(10)
    self.change_playback_speed_slider.sliderReleased.connect(lambda:change_playback_speed_slider(self))

    self.change_playback_speed_increase = QPushButton('+', parent=self.change_playback_speed)
    self.change_playback_speed_increase.setObjectName('button')
    self.change_playback_speed_increase.setStyleSheet('QPushButton {border-top:5px; padding-left:5px; border-left:0;}')
    self.change_playback_speed_increase.clicked.connect(lambda:change_playback_speed_increase_clicked(self))

    self.repeat_playback = QPushButton(parent=self.playercontrols_widget)
    self.repeat_playback.setObjectName('button')
    self.repeat_playback.setCheckable(True)
    self.repeat_playback.setStyleSheet('QPushButton {border-top:0; }')
    self.repeat_playback.clicked.connect(lambda:repeat_playback_clicked(self))

    self.repeat_playback_icon_label = QLabel(parent=self.repeat_playback)
    self.repeat_playback_icon_label.setStyleSheet('QLabel { image: url(' + os.path.join(PATH_SUBTITLD_GRAPHICS, 'playback_repeat_icon.png') + ')}')

    self.repeat_playback_duration = QDoubleSpinBox(parent=self.repeat_playback)
    self.repeat_playback_duration.setMinimum(.1)
    self.repeat_playback_duration.setMaximum(60.)
    self.repeat_playback_duration.valueChanged.connect(lambda:repeat_playback_duration_changed(self))

    self.repeat_playback_x_label = QLabel('x', parent=self.repeat_playback)
    #self.repeat_playback_x_label.setObjectName('start_screen_recent_label')
    self.repeat_playback_x_label.setStyleSheet('QLabel {qproperty-alignment:AlignCenter; font-weight:bold; color:rgb(184,206,224); }')

    self.repeat_playback_times = QSpinBox(parent=self.repeat_playback)
    self.repeat_playback_times.setMinimum(1)
    self.repeat_playback_times.setMaximum(20)
    self.repeat_playback_times.valueChanged.connect(lambda:repeat_playback_times_changed(self))

    self.grid_button = QPushButton('GRID', parent=self.playercontrols_widget)
    self.grid_button.setObjectName('subbutton_no_bottom_no_right')
    self.grid_button.setCheckable(True)
    self.grid_button.clicked.connect(lambda:grid_button_clicked(self))

    self.grid_frames_button = QPushButton(parent=self.playercontrols_widget)
    self.grid_frames_button.setObjectName('subbutton_no_bottom_no_right')
    self.grid_frames_button.setIcon(QIcon(os.path.join(PATH_SUBTITLD_GRAPHICS, 'grid_frames_icon.png')))
    self.grid_frames_button.setCheckable(True)
    self.grid_frames_button.clicked.connect(lambda:grid_type_changed(self, 'frames'))

    self.grid_seconds_button = QPushButton(parent=self.playercontrols_widget)
    self.grid_seconds_button.setObjectName('subbutton_no_bottom_no_right')
    self.grid_seconds_button.setCheckable(True)
    self.grid_seconds_button.setIcon(QIcon(os.path.join(PATH_SUBTITLD_GRAPHICS, 'grid_seconds_icon.png')))
    self.grid_seconds_button.clicked.connect(lambda:grid_type_changed(self, 'seconds'))

    self.grid_scenes_button = QPushButton(parent=self.playercontrols_widget)
    self.grid_scenes_button.setObjectName('subbutton_no_bottom')
    self.grid_scenes_button.setCheckable(True)
    self.grid_scenes_button.setIcon(QIcon(os.path.join(PATH_SUBTITLD_GRAPHICS, 'grid_scenes_icon.png')))
    self.grid_scenes_button.clicked.connect(lambda:grid_type_changed(self, 'scenes'))

    self.snap_button = QPushButton('SNAP', parent=self.playercontrols_widget)
    self.snap_button.setObjectName('subbutton_no_bottom_no_right')
    self.snap_button.setCheckable(True)
    self.snap_button.clicked.connect(lambda:snap_button_clicked(self))

    self.snap_value = QDoubleSpinBox(parent=self.snap_button)
    self.snap_value.valueChanged.connect(lambda:snap_value_changed(self))

    self.snap_limits_button = QPushButton(parent=self.playercontrols_widget)
    self.snap_limits_button.setObjectName('subbutton_no_bottom_no_right')
    self.snap_limits_button.setIcon(QIcon(os.path.join(PATH_SUBTITLD_GRAPHICS, 'snap_limits_icon.png')))
    self.snap_limits_button.setCheckable(True)
    self.snap_limits_button.clicked.connect(lambda:snap_limits_button_clicked(self))

    self.snap_move_button = QPushButton(parent=self.playercontrols_widget)
    self.snap_move_button.setObjectName('subbutton_no_bottom_no_right')
    self.snap_move_button.setCheckable(True)
    self.snap_move_button.setIcon(QIcon(os.path.join(PATH_SUBTITLD_GRAPHICS, 'snap_moving_icon.png')))
    self.snap_move_button.clicked.connect(lambda:snap_move_button_clicked(self))

    self.snap_grid_button = QPushButton(parent=self.playercontrols_widget)
    self.snap_grid_button.setObjectName('subbutton_no_bottom')
    self.snap_grid_button.setCheckable(True)
    self.snap_grid_button.setIcon(QIcon(os.path.join(PATH_SUBTITLD_GRAPHICS, 'snap_grid_icon.png')))
    self.snap_grid_button.clicked.connect(lambda:snap_grid_button_clicked(self))

def playercontrols_stop_button_clicked(self):
    self.player_widget.mpv.pause = True
    self.player_widget.mpv.wait_for_property('seekable')
    self.player_widget.mpv.seek(0, reference='absolute')#, precision='exact')
    self.repeat_duration_tmp = []
    self.mediaplayer_is_playing = False
    self.playercontrols_playpause_button.setChecked(False)
    playercontrols_playpause_button_update(self)

def playercontrols_playpause_button_clicked(self):
    self.player.playpause(self)
    playercontrols_playpause_button_update(self)

def playercontrols_playpause_button_update(self):
    self.playercontrols_playpause_button.setIcon(QIcon(os.path.join(PATH_SUBTITLD_GRAPHICS, 'pause_icon.png')) if self.playercontrols_playpause_button.isChecked() else QIcon(os.path.join(PATH_SUBTITLD_GRAPHICS, 'play_icon.png')) )

def resized(self):
    if self.subtitles_list or self.video_metadata:
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
    self.playercontrols_stop_button.setGeometry((self.playercontrols_widget_central_top.width()*.5)-55,11,50,43)
    self.playercontrols_playpause_button.setGeometry((self.playercontrols_widget_central_top.width()*.5)-5,11,60,43)
    self.playercontrols_play_from_last_start_button.setGeometry(self.playercontrols_stop_button.x()-50,11,50,43)
    self.playercontrols_play_from_next_start_button.setGeometry(self.playercontrols_playpause_button.x()+self.playercontrols_playpause_button.width(),11,50,43)

    self.add_subtitle_button.setGeometry(self.playercontrols_widget_top_left.width()-405,44,120,40)
    self.add_subtitle_duration.setGeometry(68,8,46,self.add_subtitle_button.height()-14)
    self.remove_selected_subtitle_button.setGeometry(self.add_subtitle_button.x() + self.add_subtitle_button.width(),self.add_subtitle_button.y(),100,40)

    self.merge_back_selected_subtitle_button.setGeometry(self.remove_selected_subtitle_button.x() + self.remove_selected_subtitle_button.width() + 5,44,40,40)
    self.slice_selected_subtitle_button.setGeometry(self.merge_back_selected_subtitle_button.x() + self.merge_back_selected_subtitle_button.width(),self.merge_back_selected_subtitle_button.y(),40,40)
    self.merge_next_selected_subtitle_button.setGeometry(self.slice_selected_subtitle_button.x() + self.slice_selected_subtitle_button.width(),self.merge_back_selected_subtitle_button.y(),40,40)

    self.change_playback_speed.setGeometry(self.playercontrols_widget_central_top.x()-182,7,180,36)
    self.change_playback_speed_icon_label.setGeometry(0,0,self.change_playback_speed.height(),self.change_playback_speed.height())
    self.change_playback_speed_decrease.setGeometry(70,10,20,20)
    self.change_playback_speed_slider.setGeometry(90,10,60,20)
    self.change_playback_speed_increase.setGeometry(150,10,20,20)

    self.repeat_playback.setGeometry(self.playercontrols_widget_central_top.x()+self.playercontrols_widget_central_top.width()+2,7,150,36)
    self.repeat_playback_icon_label.setGeometry(0,0,self.repeat_playback.height(),self.repeat_playback.height())
    self.repeat_playback_duration.setGeometry(self.repeat_playback_icon_label.x()+self.repeat_playback_icon_label.width(),6,46,self.repeat_playback.height()-14)
    self.repeat_playback_x_label.setGeometry(self.repeat_playback_duration.x()+self.repeat_playback_duration.width(),0,15,self.repeat_playback.height())
    self.repeat_playback_times.setGeometry(self.repeat_playback_x_label.x()+self.repeat_playback_x_label.width(),6,40,self.repeat_playback.height()-14)

    self.next_start_to_current_position_button.setGeometry(self.playercontrols_widget_top_right.x()+110,44,40,40)
    self.last_start_to_current_position_button.setGeometry(self.next_start_to_current_position_button.x()+self.next_start_to_current_position_button.width(),self.next_start_to_current_position_button.y(),40,40)
    self.next_end_to_current_position_button.setGeometry(self.last_start_to_current_position_button.x()+self.last_start_to_current_position_button.width(),self.next_start_to_current_position_button.y(),40,40)
    self.last_end_to_current_position_button.setGeometry(self.next_end_to_current_position_button.x()+self.next_end_to_current_position_button.width(),self.next_start_to_current_position_button.y(),40,40)

    self.zoomout_button.setGeometry(self.last_end_to_current_position_button.x() + self.last_end_to_current_position_button.width() + 5,44,40,40)
    self.zoomin_button.setGeometry(self.zoomout_button.x() + self.zoomout_button.width(),44,40,40)

    self.snap_button.setGeometry(self.playercontrols_widget_central_top.x()+215,60,100,24)
    self.snap_value.setGeometry(self.snap_button.width()-50,4,46,self.snap_button.height()-8)
    self.snap_limits_button.setGeometry(self.snap_button.x()+self.snap_button.width(),self.snap_button.y(),30,self.snap_button.height())
    self.snap_move_button.setGeometry(self.snap_limits_button.x()+self.snap_limits_button.width(),self.snap_button.y(),30,self.snap_button.height())
    self.snap_grid_button.setGeometry(self.snap_move_button.x()+self.snap_move_button.width(),self.snap_button.y(),30,self.snap_button.height())

    self.grid_button.setGeometry(self.playercontrols_widget_central_top.x()-55,60,50,24)
    self.grid_frames_button.setGeometry(self.grid_button.x()+self.grid_button.width(),self.grid_button.y(),30,self.grid_button.height())
    self.grid_seconds_button.setGeometry(self.grid_frames_button.x()+self.grid_frames_button.width(),self.grid_button.y(),30,self.grid_button.height())
    self.grid_scenes_button.setGeometry(self.grid_seconds_button.x()+self.grid_seconds_button.width(),self.grid_button.y(),30,self.grid_button.height())

def show(self):
    self.generate_effect(self.playercontrols_widget_animation, 'geometry', 1000, [self.playercontrols_widget.x(),self.playercontrols_widget.y(),self.playercontrols_widget.width(),self.playercontrols_widget.height()], [self.playercontrols_widget.x(), self.height()-200, self.playercontrols_widget.width(),self.playercontrols_widget.height()])
    update_snap_buttons(self)
    update_grid_buttons(self)
    update_playback_speed_buttons(self)
    self.add_subtitle_duration.setValue(self.default_new_subtitle_duration)
    self.repeat_playback_duration.setValue(self.repeat_duration)
    self.repeat_playback_times.setValue(self.repeat_times)

    if not self.advanced_mode:
        self.change_playback_speed.setVisible(False)
        self.change_playback_speed_icon_label.setVisible(False)
        self.change_playback_speed_decrease.setVisible(False)
        self.change_playback_speed_slider.setVisible(False)
        self.change_playback_speed_increase.setVisible(False)

        self.repeat_playback.setVisible(False)
        self.repeat_playback_icon_label.setVisible(False)
        self.repeat_playback_duration.setVisible(False)
        self.repeat_playback_x_label.setVisible(False)
        self.repeat_playback_times.setVisible(False)

def zoomin_button_clicked(self):
    self.mediaplayer_zoom += 10.0
    zoom_buttons_update(self)

def zoomout_button_clicked(self):
    self.mediaplayer_zoom -= 10.0
    zoom_buttons_update(self)

def zoom_buttons_update(self):
    self.zoomout_button.setEnabled(True if self.mediaplayer_zoom - 5.0 > 0.0 else False)
    self.zoomin_button.setEnabled(True if self.mediaplayer_zoom + 5.0 < 500.0 else False)
    proportion = ((self.current_timeline_position*self.timeline_widget.width_proportion)-self.timeline_scroll.horizontalScrollBar().value())/self.timeline_scroll.width()
    self.timeline_widget.setGeometry(0,0,int(round(self.video_metadata.get('duration', 0.01)*self.mediaplayer_zoom)),self.timeline_scroll.height()-20)
    #self.timeline.zoom_update_waveform(self)
    self.timeline.update_scrollbar(self, position=proportion)

def snap_button_clicked(self):
    self.timeline_snap = self.snap_button.isChecked()
    update_snap_buttons(self)

def snap_move_button_clicked(self):
    self.timeline_snap_moving = self.snap_move_button.isChecked()

def snap_limits_button_clicked(self):
    self.timeline_snap_limits = self.snap_limits_button.isChecked()

def snap_grid_button_clicked(self):
    self.timeline_snap_grid = self.snap_grid_button.isChecked()

def snap_value_changed(self):
    self.timeline_snap_value = self.snap_value.value() if self.snap_value.value() else .1

def add_subtitle_duration_changed(self):
    self.default_new_subtitle_duration = self.add_subtitle_duration.value()

def update_snap_buttons(self):
    self.snap_button.setChecked(bool(self.timeline_snap))
    self.snap_limits_button.setEnabled(self.snap_button.isChecked())
    self.snap_limits_button.setChecked(bool(self.timeline_snap_limits))
    self.snap_move_button.setEnabled(self.snap_button.isChecked())
    self.snap_move_button.setChecked(bool(self.timeline_snap_moving))
    self.snap_grid_button.setEnabled(self.snap_button.isChecked())
    self.snap_grid_button.setChecked(bool(self.timeline_snap_grid))
    self.snap_value.setEnabled(self.snap_button.isChecked())
    self.snap_value.setValue(self.timeline_snap_value if self.timeline_snap_value else .1)
    self.timeline_widget.update()

def update_playback_speed_buttons(self):
    self.change_playback_speed_icon_label.setEnabled(self.change_playback_speed.isChecked())
    self.change_playback_speed_decrease.setEnabled(self.change_playback_speed.isChecked())
    self.change_playback_speed_slider.setEnabled(self.change_playback_speed.isChecked())
    self.change_playback_speed_increase.setEnabled(self.change_playback_speed.isChecked())
    self.change_playback_speed.setText('x' + str(self.playback_speed))
    self.change_playback_speed_slider.setValue(self.playback_speed*100)

def grid_button_clicked(self):
    self.timeline_show_grid = self.grid_button.isChecked()
    if not self.timeline_grid_type:
        self.timeline_grid_type = 'seconds'
    update_grid_buttons(self)

def grid_type_changed(self, type):
    self.timeline_grid_type = type
    update_grid_buttons(self)

def update_grid_buttons(self):
    self.grid_button.setChecked(self.timeline_show_grid)
    self.grid_frames_button.setEnabled(self.timeline_show_grid)
    self.grid_frames_button.setChecked(True if self.timeline_grid_type == 'frames' else False)
    self.grid_seconds_button.setEnabled(self.timeline_show_grid)
    self.grid_seconds_button.setChecked(True if self.timeline_grid_type == 'seconds' else False)
    self.grid_scenes_button.setEnabled(self.timeline_show_grid)
    self.grid_scenes_button.setChecked(True if self.timeline_grid_type == 'scenes' else False)
    self.timeline_widget.update()

def playercontrols_play_from_last_start_button_clicked(self):
    subt = [item[0] for item in self.subtitles_list]
    last_subtitle = self.subtitles_list[bisect(subt, self.current_timeline_position)-1]
    self.current_timeline_position = last_subtitle[0]
    self.player_widget.mpv.wait_for_property('seekable')
    self.player_widget.mpv.seek(self.current_timeline_position, reference='absolute')#, precision='exact')
    self.timeline.update_scrollbar(self)
    self.timeline.update(self)

def playercontrols_play_from_next_start_button_clicked(self):
    subt = [item[0] for item in self.subtitles_list]
    last_subtitle = self.subtitles_list[bisect(subt, self.current_timeline_position)]
    self.current_timeline_position = last_subtitle[0]
    self.player_widget.mpv.wait_for_property('seekable')
    self.player_widget.mpv.seek(self.current_timeline_position, reference='absolute')#, precision='exact')
    self.timeline.update_scrollbar(self)
    self.timeline.update(self)

def add_subtitle_button_clicked(self):
    self.selected_subtitle = subtitles.add_subtitle(subtitles=self.subtitles_list, position=self.current_timeline_position, duration=self.default_new_subtitle_duration)
    self.unsaved = True
    self.subtitleslist.update_subtitles_list_qlistwidget(self)
    self.timeline.update(self)
    self.update_things()
    self.properties.update_properties_widget(self)
    self.properties_textedit.setFocus(Qt.TabFocusReason)

def remove_selected_subtitle_button_clicked(self):
    subtitles.remove_subtitle(subtitles=self.subtitles_list, selected_subtitle=self.selected_subtitle)
    self.unsaved = True
    self.selected_subtitle = False
    self.subtitleslist.update_subtitles_list_qlistwidget(self)
    self.timeline.update(self)
    self.update_things()
    self.properties.update_properties_widget(self)

def slice_selected_subtitle_button_clicked(self):
    if self.selected_subtitle:
        pos = self.properties_textedit.textCursor().position()
        last_text = self.properties_textedit.toPlainText()[:pos]
        next_text = self.properties_textedit.toPlainText()[pos:]
        self.selected_subtitle = subtitles.slice_subtitle(subtitles=self.subtitles_list, selected_subtitle=self.selected_subtitle, position=self.current_timeline_position, next_text=next_text, last_text=last_text)
        self.unsaved = True
        self.subtitleslist.update_subtitles_list_qlistwidget(self)
        self.timeline.update(self)
        self.update_things()
        self.properties.update_properties_widget(self)

def merge_back_selected_subtitle_button_clicked(self):
    if self.selected_subtitle:
        self.selected_subtitle = subtitles.merge_back_subtitle(subtitles=self.subtitles_list, selected_subtitle=self.selected_subtitle)
        self.unsaved = True
        self.subtitleslist.update_subtitles_list_qlistwidget(self)
        self.timeline.update(self)
        self.update_things()
        self.properties.update_properties_widget(self)

def merge_next_selected_subtitle_button_clicked(self):
    if self.selected_subtitle:
        self.selected_subtitle = subtitles.merge_next_subtitle(subtitles=self.subtitles_list, selected_subtitle=self.selected_subtitle)
        self.unsaved = True
        self.subtitleslist.update_subtitles_list_qlistwidget(self)
        self.timeline.update(self)
        self.update_things()
        self.properties.update_properties_widget(self)

def next_start_to_current_position_button_clicked(self):
    subtitles.next_start_to_current_position(subtitles=self.subtitles_list, position=self.current_timeline_position)
    self.unsaved = True
    self.subtitleslist.update_subtitles_list_qlistwidget(self)
    self.timeline.update(self)
    self.update_things()
    self.properties.update_properties_widget(self)

def last_end_to_current_position_button_clicked(self):
    subtitles.last_end_to_current_position(subtitles=self.subtitles_list, position=self.current_timeline_position)
    self.unsaved = True
    self.subtitleslist.update_subtitles_list_qlistwidget(self)
    self.timeline.update(self)
    self.update_things()
    self.properties.update_properties_widget(self)

def last_start_to_current_position_button_clicked(self):
    subtitles.last_start_to_current_position(subtitles=self.subtitles_list, position=self.current_timeline_position)
    self.unsaved = True
    self.subtitleslist.update_subtitles_list_qlistwidget(self)
    self.timeline.update(self)
    self.update_things()
    self.properties.update_properties_widget(self)

def next_end_to_current_position_button_clicked(self):
    subtitles.next_end_to_current_position(subtitles=self.subtitles_list, position=self.current_timeline_position)
    self.unsaved = True
    self.subtitleslist.update_subtitles_list_qlistwidget(self)
    self.timeline.update(self)
    self.update_things()
    self.properties.update_properties_widget(self)

def change_playback_speed_clicked(self):
    if not self.change_playback_speed.isChecked():
        self.playback_speed = 1.0
        self.player.update_speed(self)
    update_playback_speed_buttons(self)

def change_playback_speed_decrease_clicked(self):
    self.change_playback_speed_slider.setValue(self.change_playback_speed_slider.value()-10)
    self.playback_speed = self.change_playback_speed_slider.value()/100.0
    self.player.update_speed(self)
    update_playback_speed_buttons(self)

def change_playback_speed_slider(self):
    self.playback_speed = self.change_playback_speed_slider.value()/100.0
    self.player.update_speed(self)
    update_playback_speed_buttons(self)

def change_playback_speed_increase_clicked(self):
    self.change_playback_speed_slider.setValue(self.change_playback_speed_slider.value()+10)
    self.playback_speed = self.change_playback_speed_slider.value()/100.0
    self.player.update_speed(self)
    update_playback_speed_buttons(self)

def repeat_playback_clicked(self):
    self.repeat_activated = self.repeat_playback.isChecked()

def repeat_playback_duration_changed(self):
    self.repeat_duration = self.repeat_playback_duration.value()

def repeat_playback_times_changed(self):
    self.repeat_times = self.repeat_playback_times.value()
