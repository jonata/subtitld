#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
from bisect import bisect
from PyQt5.QtWidgets import QPushButton, QLabel, QFileDialog, QLineEdit, QDoubleSpinBox
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, Qt, pyqtSignal, QSize, QPropertyAnimation, QSize
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
    self.add_subtitle_button.setObjectName('button_dark_no_right_no_top')
    self.add_subtitle_button.clicked.connect(lambda:add_subtitle_button_clicked(self))

    self.remove_selected_subtitle_button = QPushButton('REMOVE', parent=self.playercontrols_widget)
    self.remove_selected_subtitle_button.setIcon(QIcon(os.path.join(PATH_SUBTITLD_GRAPHICS, 'remove_selected_subtitle_icon.png')))
    self.remove_selected_subtitle_button.setIconSize(QSize(20,20))
    self.remove_selected_subtitle_button.setObjectName('button_dark_no_left_no_top')
    self.remove_selected_subtitle_button.clicked.connect(lambda:remove_selected_subtitle_button_clicked(self))

    self.merge_back_selected_subtitle_button = QPushButton(parent=self.playercontrols_widget)
    self.merge_back_selected_subtitle_button.setIcon(QIcon(os.path.join(PATH_SUBTITLD_GRAPHICS, 'merge_back_selected_subtitle_icon.png')))
    self.merge_back_selected_subtitle_button.setIconSize(QSize(20,20))
    self.merge_back_selected_subtitle_button.setObjectName('button_dark')
    self.merge_back_selected_subtitle_button.setStyleSheet('QPushButton {border-top:0; border-right:0;}')
    self.merge_back_selected_subtitle_button.clicked.connect(lambda:merge_back_selected_subtitle_button_clicked(self))

    self.slice_selected_subtitle_button = QPushButton(parent=self.playercontrols_widget)
    self.slice_selected_subtitle_button.setIcon(QIcon(os.path.join(PATH_SUBTITLD_GRAPHICS, 'slice_selected_subtitle_icon.png')))
    self.slice_selected_subtitle_button.setIconSize(QSize(20,20))
    self.slice_selected_subtitle_button.setObjectName('button_dark')
    self.slice_selected_subtitle_button.setStyleSheet('QPushButton {border-top:0; border-left:0; border-right:0;}')
    self.slice_selected_subtitle_button.clicked.connect(lambda:slice_selected_subtitle_button_clicked(self))

    self.merge_next_selected_subtitle_button = QPushButton(parent=self.playercontrols_widget)
    self.merge_next_selected_subtitle_button.setIcon(QIcon(os.path.join(PATH_SUBTITLD_GRAPHICS, 'merge_next_selected_subtitle_icon.png')))
    self.merge_next_selected_subtitle_button.setIconSize(QSize(20,20))
    self.merge_next_selected_subtitle_button.setObjectName('button_dark')
    self.merge_next_selected_subtitle_button.setStyleSheet('QPushButton {border-top:0; border-left:0;}')
    self.merge_next_selected_subtitle_button.clicked.connect(lambda:merge_next_selected_subtitle_button_clicked(self))

    self.playercontrols_timecode_label = QLabel(parent=self.playercontrols_widget_central_bottom)
    self.playercontrols_timecode_label.setObjectName('playercontrols_timecode_label')

    self.zoomin_button = QPushButton(parent=self.playercontrols_widget)
    self.zoomin_button.setIcon(QIcon(os.path.join(PATH_SUBTITLD_GRAPHICS, 'zoom_in_icon.png')))
    self.zoomin_button.setIconSize(QSize(20,20))
    self.zoomin_button.setObjectName('button_no_left_no_bottom')
    self.zoomin_button.clicked.connect(lambda:zoomin_button_clicked(self))

    self.zoomout_button = QPushButton(parent=self.playercontrols_widget)
    self.zoomout_button.setIcon(QIcon(os.path.join(PATH_SUBTITLD_GRAPHICS, 'zoom_out_icon.png')))
    self.zoomout_button.setIconSize(QSize(20,20))
    self.zoomout_button.setObjectName('button_no_right_no_bottom')
    self.zoomout_button.clicked.connect(lambda:zoomout_button_clicked(self))

    self.next_start_to_current_position_button = QPushButton(parent=self.playercontrols_widget)
    self.next_start_to_current_position_button.setIcon(QIcon(os.path.join(PATH_SUBTITLD_GRAPHICS, 'next_start_to_current_position_icon.png')))
    self.next_start_to_current_position_button.setIconSize(QSize(20,20))
    self.next_start_to_current_position_button.setObjectName('button_dark')
    self.next_start_to_current_position_button.setStyleSheet('QPushButton {border-top:0; border-right:0;}')
    self.next_start_to_current_position_button.clicked.connect(lambda:next_start_to_current_position_button_clicked(self))

    self.last_end_to_current_position_button = QPushButton(parent=self.playercontrols_widget)
    self.last_end_to_current_position_button.setIcon(QIcon(os.path.join(PATH_SUBTITLD_GRAPHICS, 'last_end_to_current_position_icon.png')))
    self.last_end_to_current_position_button.setIconSize(QSize(20,20))
    self.last_end_to_current_position_button.setObjectName('button_dark')
    self.last_end_to_current_position_button.setStyleSheet('QPushButton {border-top:0; border-left:0;}')
    self.last_end_to_current_position_button.clicked.connect(lambda:last_end_to_current_position_button_clicked(self))

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
    self.mediaplayer_is_playing = False
    self.playercontrols_playpause_button.setChecked(False)
    playercontrols_playpause_button_update(self)

def playercontrols_playpause_button_clicked(self):
    self.player.playpause(self)
    playercontrols_playpause_button_update(self)

def playercontrols_playpause_button_update(self):
    self.playercontrols_playpause_button.setIcon(QIcon(os.path.join(PATH_SUBTITLD_GRAPHICS, 'pause_icon.png')) if self.playercontrols_playpause_button.isChecked() else QIcon(os.path.join(PATH_SUBTITLD_GRAPHICS, 'play_icon.png')) )

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
    self.playercontrols_stop_button.setGeometry((self.playercontrols_widget_central_top.width()*.5)-55,11,50,43)
    self.playercontrols_playpause_button.setGeometry((self.playercontrols_widget_central_top.width()*.5)-5,11,60,43)
    self.playercontrols_play_from_last_start_button.setGeometry(self.playercontrols_stop_button.x()-50,11,50,43)
    self.playercontrols_play_from_next_start_button.setGeometry(self.playercontrols_playpause_button.x()+self.playercontrols_playpause_button.width(),11,50,43)

    self.add_subtitle_button.setGeometry(self.playercontrols_widget_central_top.x()-310,7,80,40)
    self.remove_selected_subtitle_button.setGeometry(self.add_subtitle_button.x() + self.add_subtitle_button.width(),7,100,40)

    self.merge_back_selected_subtitle_button.setGeometry(self.remove_selected_subtitle_button.x() + self.remove_selected_subtitle_button.width() + 5,7,40,40)
    self.slice_selected_subtitle_button.setGeometry(self.merge_back_selected_subtitle_button.x() + self.merge_back_selected_subtitle_button.width(),7,40,40)
    self.merge_next_selected_subtitle_button.setGeometry(self.slice_selected_subtitle_button.x() + self.slice_selected_subtitle_button.width(),7,40,40)

    self.next_start_to_current_position_button.setGeometry(self.playercontrols_widget_central_top.x()+self.playercontrols_widget_central_top.width()+10,7,40,40)
    self.last_end_to_current_position_button.setGeometry(self.next_start_to_current_position_button.x()+self.next_start_to_current_position_button.width(),7,40,40)

    self.zoomout_button.setGeometry(20,44,40,40)
    self.zoomin_button.setGeometry(60,44,40,40)

    self.snap_button.setGeometry(self.playercontrols_widget.width()-210,54,100,30)
    self.snap_value.setGeometry(self.snap_button.width()-50,4,46,self.snap_button.height()-8)
    self.snap_limits_button.setGeometry(self.snap_button.x()+self.snap_button.width(),self.snap_button.y(),self.snap_button.height(),self.snap_button.height())
    self.snap_move_button.setGeometry(self.snap_limits_button.x()+self.snap_limits_button.width(),self.snap_button.y(),self.snap_button.height(),self.snap_button.height())
    self.snap_grid_button.setGeometry(self.snap_move_button.x()+self.snap_move_button.width(),self.snap_button.y(),self.snap_button.height(),self.snap_button.height())

    self.grid_button.setGeometry(self.playercontrols_widget.width()-410,54,50,30)
    self.grid_frames_button.setGeometry(self.grid_button.x()+self.grid_button.width(),self.grid_button.y(),self.grid_button.height(),self.grid_button.height())
    self.grid_seconds_button.setGeometry(self.grid_frames_button.x()+self.grid_frames_button.width(),self.grid_button.y(),self.grid_button.height(),self.grid_button.height())
    self.grid_scenes_button.setGeometry(self.grid_seconds_button.x()+self.grid_seconds_button.width(),self.grid_button.y(),self.grid_button.height(),self.grid_button.height())

def show(self):
    self.generate_effect(self.playercontrols_widget_animation, 'geometry', 1000, [self.playercontrols_widget.x(),self.playercontrols_widget.y(),self.playercontrols_widget.width(),self.playercontrols_widget.height()], [self.playercontrols_widget.x(), self.height()-200, self.playercontrols_widget.width(),self.playercontrols_widget.height()])
    update_snap_buttons(self)
    update_grid_buttons(self)

def zoomin_button_clicked(self):
    self.mediaplayer_zoom += 5.0
    zoom_buttons_update(self)

def zoomout_button_clicked(self):
    self.mediaplayer_zoom -= 5.0
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
    self.selected_subtitle = subtitles.add_subtitle(subtitles=self.subtitles_list, position=self.current_timeline_position)
    self.subtitleslist.update_subtitles_list_qlistwidget(self)
    self.timeline.update(self)
    self.update_things()
    self.properties.update_properties_widget(self)

def remove_selected_subtitle_button_clicked(self):
    subtitles.remove_subtitle(subtitles=self.subtitles_list, selected_subtitle=self.selected_subtitle)
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
        self.subtitleslist.update_subtitles_list_qlistwidget(self)
        self.timeline.update(self)
        self.update_things()
        self.properties.update_properties_widget(self)

def merge_back_selected_subtitle_button_clicked(self):
    if self.selected_subtitle:
        self.selected_subtitle = subtitles.merge_back_subtitle(subtitles=self.subtitles_list, selected_subtitle=self.selected_subtitle)
        self.subtitleslist.update_subtitles_list_qlistwidget(self)
        self.timeline.update(self)
        self.update_things()
        self.properties.update_properties_widget(self)

def merge_next_selected_subtitle_button_clicked(self):
    if self.selected_subtitle:
        self.selected_subtitle = subtitles.merge_next_subtitle(subtitles=self.subtitles_list, selected_subtitle=self.selected_subtitle)
        self.subtitleslist.update_subtitles_list_qlistwidget(self)
        self.timeline.update(self)
        self.update_things()
        self.properties.update_properties_widget(self)

def next_start_to_current_position_button_clicked(self):
    subtitles.next_start_to_current_position(subtitles=self.subtitles_list, position=self.current_timeline_position)
    self.subtitleslist.update_subtitles_list_qlistwidget(self)
    self.timeline.update(self)
    self.update_things()
    self.properties.update_properties_widget(self)

def last_end_to_current_position_button_clicked(self):
    subtitles.last_end_to_current_position(subtitles=self.subtitles_list, position=self.current_timeline_position)
    self.subtitleslist.update_subtitles_list_qlistwidget(self)
    self.timeline.update(self)
    self.update_things()
    self.properties.update_properties_widget(self)
