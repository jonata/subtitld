#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import threading
import multiprocessing
import datetime

from modules import file_io
from modules import waveform

from PyQt5.QtWidgets import QPushButton, QLabel, QFileDialog, QSpinBox, QDoubleSpinBox, QListWidget, QListView
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, Qt, QSize

def load(self, path_catptilr_graphics):
    self.subtitles_list_widget = QLabel(parent=self)
    self.subtitles_list_widget.setObjectName('subtitles_list_widget')
    self.subtitles_list_widget_animation = QPropertyAnimation(self.subtitles_list_widget, b'geometry')
    self.subtitles_list_widget_animation.setEasingCurve(QEasingCurve.OutCirc)

    self.subtitles_list_widget_alert = QLabel('There is no subtitle to show. Please open a file or create a new one.', parent=self.subtitles_list_widget)
    self.subtitles_list_widget_alert.setWordWrap(True)
    self.subtitles_list_widget_alert.setObjectName('subtitles_list_widget_alert')

    self.save_button = QPushButton('SAVE', parent=self.subtitles_list_widget)
    self.save_button.clicked.connect(lambda:save_button_clicked(self))
    self.save_button.setObjectName('button_dark_no_left')

    self.open_button = QPushButton('OPEN', parent=self.subtitles_list_widget)
    self.open_button.clicked.connect(lambda:open_button_clicked(self))
    self.open_button.setObjectName('button_dark_no_right')

    self.subtitles_list_qlistwidget = QListWidget(parent=self.subtitles_list_widget)
    self.subtitles_list_qlistwidget.setViewMode(QListView.ListMode)
    self.subtitles_list_qlistwidget.setObjectName('subtitles_list_qlistwidget')
    self.subtitles_list_qlistwidget.setSpacing(5)
    self.subtitles_list_qlistwidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    self.subtitles_list_qlistwidget.setFocusPolicy(Qt.NoFocus)
    self.subtitles_list_qlistwidget.setIconSize(QSize(42,42))
    self.subtitles_list_qlistwidget.currentItemChanged.connect(lambda:subtitles_list_qlistwidget_item_clicked(self))

    self.subtitleslist_add_button = QPushButton('ADD', parent=self.subtitles_list_widget)
    self.subtitleslist_add_button.clicked.connect(lambda:subtitleslist_add_button_clicked(self))
    self.subtitleslist_add_button.setObjectName('button_no_right_top')

    self.subtitleslist_remove_button = QPushButton('REMOVE', parent=self.subtitles_list_widget)
    self.subtitleslist_remove_button.clicked.connect(lambda:subtitleslist_remove_button_clicked(self))
    self.subtitleslist_remove_button.setObjectName('button_no_left_top')

def resized(self):
    if self.subtitles_list:
        self.subtitles_list_widget.setGeometry(0,0,(self.width()*.2)-15,self.height())
    else:
        self.subtitles_list_widget.setGeometry(-((self.width()*.2)-15),0,(self.width()*.2)-15,self.height())
    self.open_button.setGeometry(20,20,100,30)
    self.save_button.setGeometry(120,20,100,30)
    self.subtitles_list_widget_alert.setGeometry(0,0,self.subtitles_list_widget.width()-2, self.subtitles_list_widget.height())
    self.subtitles_list_qlistwidget.setGeometry(20,60,self.subtitles_list_widget.width()-40,self.subtitles_list_widget.height()-80-self.playercontrols_widget.height()-15)
    self.subtitleslist_add_button.setGeometry(self.subtitles_list_qlistwidget.x()-2,self.subtitles_list_qlistwidget.y() + self.subtitles_list_qlistwidget.height(),(self.subtitles_list_qlistwidget.width()*.5)+2,30)
    self.subtitleslist_remove_button.setGeometry(self.subtitles_list_qlistwidget.x()+(self.subtitles_list_qlistwidget.width()*.5),self.subtitles_list_qlistwidget.y() + self.subtitles_list_qlistwidget.height(),(self.subtitles_list_qlistwidget.width()*.5)+2,30)

def save_button_clicked(self):
    if not self.actual_subtitle_file:
        self.actual_subtitle_file = QFileDialog.getSaveFileName(self, "Select the srt file", os.path.join(os.environ.get('HOME', None), 'final.srt'), "SRT file (*.srt)")[0]
    if self.actual_subtitle_file:
        file_io.save_file(self.actual_subtitle_file, self.subtitles_list)

def open_button_clicked(self):
    file_to_open = QFileDialog.getOpenFileName(self, "Select the subtitle or video file", os.path.expanduser("~"), "SRT file (*.srt);;MP4 file (*.mp4)")[0]
    if file_to_open and os.path.isfile(file_to_open):
        file_io.open_filepath(self, file_to_open)


def update_subtitles_list_widget(self):
    self.subtitles_list_widget_alert.setVisible(not bool(self.subtitles_list))
    self.subtitles_list_qlistwidget.setVisible(bool(self.subtitles_list))
    update_subtitles_list_qlistwidget(self)

def update_subtitles_list_qlistwidget(self):
    self.subtitles_list_qlistwidget.clear()
    if self.subtitles_list:
        counter = 1
        for sub in sorted(self.subtitles_list):
            self.subtitles_list_qlistwidget.addItem(str(counter) + ' - ' + sub[2])
            counter += 1
    if self.selected_subtitle:
        self.subtitles_list_qlistwidget.setCurrentRow(self.subtitles_list.index(self.selected_subtitle))

def subtitles_list_qlistwidget_item_clicked(self):
    if self.subtitles_list_qlistwidget.currentItem():
        sub_index = int(self.subtitles_list_qlistwidget.currentItem().text().split(' - ')[0]) - 1
        self.selected_subtitle = self.subtitles_list[sub_index]

    if self.selected_subtitle:
        if not (self.current_timeline_position > self.selected_subtitle[0] and self.current_timeline_position < self.selected_subtitle[0] + self.selected_subtitle[1]):
            self.current_timeline_position = self.selected_subtitle[0] + (self.selected_subtitle[1]*.5)
            self.player_widget.mpv.seek(self.current_timeline_position, reference='absolute', precision='exact')

    self.properties.update_properties_widget(self)
    self.timeline.update(self)
    self.timeline.update_scrollbar(self, position='middle')
    self.update_things()

def subtitleslist_add_button_clicked(self):
    current_index = 0

    for subtitle in self.subtitles_list:
        if subtitle[0] > self.current_timeline_position:
            break
        current_index += 1

    if current_index and self.subtitles_list[current_index - 1][0] + self.subtitles_list[current_index - 1][1] > self.current_timeline_position:
        self.subtitles_list[current_index - 1][1] -= (self.subtitles_list[current_index - 1][0] + self.subtitles_list[current_index - 1][1]) - self.current_timeline_position

    duration = 5.0

    if len(self.subtitles_list) - 1 > current_index and self.subtitles_list[current_index][0] - self.current_timeline_position < duration:
        duration = self.subtitles_list[current_index][0] - self.current_timeline_position

    self.subtitles_list.insert(current_index, [self.current_timeline_position,duration,'Text'])
    self.selected_subtitle = self.subtitles_list[current_index]
    update_subtitles_list_qlistwidget(self)
    self.timeline.update(self)
    self.update_things()

def subtitleslist_remove_button_clicked(self):
    self.subtitles_list.remove(self.selected_subtitle)
    self.selected_subtitle = False
    update_subtitles_list_qlistwidget(self)
    self.timeline.update(self)
    self.update_things()

def show(self):
    self.generate_effect(self.subtitles_list_widget_animation, 'geometry', 700, [self.subtitles_list_widget.x(),self.subtitles_list_widget.y(),self.subtitles_list_widget.width(),self.subtitles_list_widget.height()], [0, self.subtitles_list_widget.y(), self.subtitles_list_widget.width(),self.subtitles_list_widget.height()])
