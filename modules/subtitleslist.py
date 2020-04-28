#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import threading
import multiprocessing
import datetime

from modules import file_io
from modules import waveform

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton, QLabel, QFileDialog, QSpinBox, QDoubleSpinBox, QListWidget, QListView
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, Qt, QSize

def load(self, PATH_SUBTITLD_GRAPHICS):
    self.subtitles_list_widget = QLabel(parent=self)
    self.subtitles_list_widget.setObjectName('subtitles_list_widget')
    self.subtitles_list_widget_animation = QPropertyAnimation(self.subtitles_list_widget, b'geometry')
    self.subtitles_list_widget_animation.setEasingCurve(QEasingCurve.OutCirc)

    self.subtitles_list_top_widget = QLabel(parent=self.subtitles_list_widget)
    self.subtitles_list_top_widget.setObjectName('subtitles_list_top_widget')

    self.toppanel_save_button = QPushButton(parent=self.subtitles_list_top_widget)
    self.toppanel_save_button.clicked.connect(lambda:toppanel_save_button_clicked(self))
    self.toppanel_save_button.setIcon(QIcon(os.path.join(PATH_SUBTITLD_GRAPHICS, 'save_icon.png')))
    self.toppanel_save_button.setIconSize(QSize(20,20))
    self.toppanel_save_button.setObjectName('button_dark')
    self.toppanel_save_button.setStyleSheet('QPushButton {padding-left:0px;border-left:0;border-right:0;}')

    self.toppanel_open_button = QPushButton(parent=self.subtitles_list_top_widget)
    self.toppanel_open_button.clicked.connect(lambda:toppanel_open_button_clicked(self))
    self.toppanel_open_button.setIcon(QIcon(os.path.join(PATH_SUBTITLD_GRAPHICS, 'open_icon.png')))
    self.toppanel_open_button.setIconSize(QSize(20,20))
    self.toppanel_open_button.setObjectName('button')
    self.toppanel_open_button.setStyleSheet('QPushButton {border-left:0;}')

    self.toppanel_subtitle_file_info_label = QLabel(parent=self.subtitles_list_top_widget)
    self.toppanel_subtitle_file_info_label.setObjectName('toppanel_subtitle_file_info_label')

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

    self.subtitles_list_top_widget.setGeometry(0,0,self.subtitles_list_widget.width()-2,80)
    self.toppanel_save_button.setGeometry(0,20,60,40)
    self.toppanel_open_button.setGeometry(self.toppanel_save_button.x()+self.toppanel_save_button.width(),self.toppanel_save_button.y(),self.toppanel_save_button.height(),self.toppanel_save_button.height())
    self.toppanel_subtitle_file_info_label.setGeometry(self.toppanel_open_button.x()+self.toppanel_open_button.width()+10,self.toppanel_save_button.y(),self.subtitles_list_top_widget.width()-self.toppanel_open_button.x()-self.toppanel_open_button.width()-20,self.toppanel_save_button.height())

    self.subtitles_list_qlistwidget.setGeometry(20,self.subtitles_list_top_widget.height() + 20,self.subtitles_list_widget.width()-40,self.subtitles_list_widget.height()-80-self.playercontrols_widget.height()-35)

def update_subtitles_list_widget(self):
    #self.subtitles_list_qlistwidget.setVisible(bool(self.subtitles_list))
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
    update_toppanel_subtitle_file_info_label(self)

def toppanel_save_button_clicked(self):
    if not self.actual_subtitle_file:

        suggested_path = os.path.dirname(actual_video_file)
        if self.advanced_mode:
            save_formats = 'SRT file (*.srt)'
            suggested_name = os.path.basename(actual_video_file).rsplit('.',1)[0]
        else:
            save_formats = 'SRT file (*.srt)'
            suggested_name = os.path.basename(actual_video_file).rsplit('.',1)[0] + '.srt'

        self.actual_subtitle_file = QFileDialog.getSaveFileName(self, "Select the srt file", os.path.join(suggested_path, suggested_path), save_formats)[0]

    if self.actual_subtitle_file:
        file_io.save_file(self.actual_subtitle_file, self.subtitles_list)
        update_toppanel_subtitle_file_info_label(self)
        self.unsaved = False

def toppanel_open_button_clicked(self):
    if self.unsaved:
        save_message_box = QMessageBox(self)

        save_message_box.setWindowTitle("Unsaved changes")
        save_message_box.setText(
            "Do you want to save the changes you made on the subtitles?"
        )
        save_message_box.addButton("Save", QMessageBox.AcceptRole)
        save_message_box.addButton("Don't save", QMessageBox.RejectRole)
        ret = save_message_box.exec_()

        if ret == QMessageBox.AcceptRole:
            self.subttileslist.toppanel_save_button_clicked(self)
    file_io.open_filepath(self)

def update_toppanel_subtitle_file_info_label(self):
    text = 'Actual video does not have saved subtitle file.'
    if self.actual_subtitle_file:
        text = '<b><snall>ACTUAL PROJECT</small></b><br><big>' + os.path.basename(self.actual_subtitle_file) + '</big>'
    self.toppanel_subtitle_file_info_label.setText(text)
