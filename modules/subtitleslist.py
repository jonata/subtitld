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

    self.subtitles_list_qlistwidget = QListWidget(parent=self.subtitles_list_widget)
    self.subtitles_list_qlistwidget.setViewMode(QListView.ListMode)
    self.subtitles_list_qlistwidget.setObjectName('subtitles_list_qlistwidget')
    self.subtitles_list_qlistwidget.setSpacing(5)
    self.subtitles_list_qlistwidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    self.subtitles_list_qlistwidget.setFocusPolicy(Qt.NoFocus)
    self.subtitles_list_qlistwidget.setIconSize(QSize(42,42))
    self.subtitles_list_qlistwidget.clicked.connect(lambda:subtitles_list_qlistwidget_item_clicked(self))

def resized(self):
    if self.subtitles_list:
        self.subtitles_list_widget.setGeometry(0,0,(self.width()*.2)-15,self.height())
    else:
        self.subtitles_list_widget.setGeometry(-((self.width()*.2)-15),0,(self.width()*.2)-15,self.height())
    self.subtitles_list_widget_alert.setGeometry(0,0,self.subtitles_list_widget.width()-2, self.subtitles_list_widget.height())
    self.subtitles_list_qlistwidget.setGeometry(20,60,self.subtitles_list_widget.width()-40,self.subtitles_list_widget.height()-80-self.playercontrols_widget.height()-15)

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
            self.player_widget.mpv.wait_for_property('seekable')
            self.player_widget.mpv.seek(self.current_timeline_position, reference='absolute', precision='exact')

    self.properties.update_properties_widget(self)
    self.timeline.update(self)
    self.timeline.update_scrollbar(self, position='middle')
    self.update_things()

def show(self):
    self.generate_effect(self.subtitles_list_widget_animation, 'geometry', 700, [self.subtitles_list_widget.x(),self.subtitles_list_widget.y(),self.subtitles_list_widget.width(),self.subtitles_list_widget.height()], [0, self.subtitles_list_widget.y(), self.subtitles_list_widget.width(),self.subtitles_list_widget.height()])
