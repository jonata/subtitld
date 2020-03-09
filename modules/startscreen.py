#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton, QLabel, QFileDialog, QSpinBox, QDoubleSpinBox, QWidget, QScrollArea, QGraphicsOpacityEffect, QListWidget, QListView
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, Qt, QSize

from modules import file_io

def load(self):
    self.start_screen = QLabel(parent=self)
    self.start_screen_transparency = QGraphicsOpacityEffect()
    self.start_screen.setGraphicsEffect(self.start_screen_transparency)
    self.start_screen_transparency_animation = QPropertyAnimation(self.start_screen_transparency, b'opacity')
    self.start_screen_transparency.setOpacity(0)

    self.start_screen_recentfiles_background = QLabel(parent=self.start_screen)
    self.start_screen_recentfiles_background.setObjectName('start_screen_recentfiles_background')
    self.start_screen_recentfiles_background.setAutoFillBackground(True)

    self.start_screen_top_shadow = QLabel(parent=self.start_screen)
    self.start_screen_top_shadow.setObjectName('start_screen_top_shadow')

    self.start_screen_open_label = QLabel('OPEN A SUBTITLE OR A VIDEO', parent=self.start_screen)
    self.start_screen_open_label.setObjectName('start_screen_open_label')

    self.start_screen_open_button = QPushButton('OPEN', parent=self.start_screen)
    self.start_screen_open_button.clicked.connect(lambda:start_screen_open_button_clicked(self))
    self.start_screen_open_button.setObjectName('button_dark')

    self.start_screen_recent_label = QLabel('RECENT SUBTITLES', parent=self.start_screen)
    self.start_screen_recent_label.setObjectName('start_screen_recent_label')

    self.start_screen_recent_listwidget = QListWidget(parent=self.start_screen)
    self.start_screen_recent_listwidget.setObjectName('start_screen_recent_listwidget')
    # self.start_screen_recent_listwidget.setViewMode(QListView.ListMode)
    # self.start_screen_recent_listwidget.setSpacing(5)
    self.start_screen_recent_listwidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    self.start_screen_recent_listwidget.setFocusPolicy(Qt.NoFocus)
    # self.start_screen_recent_listwidget.setIconSize(QSize(42,42))
    self.start_screen_recent_listwidget.itemDoubleClicked.connect(lambda:start_screen_recent_listwidget_item_clicked(self))

    self.start_screen_recent_alert = QLabel('There is no recent file history.', parent=self.start_screen)
    self.start_screen_recent_alert.setWordWrap(True)
    self.start_screen_recent_alert.setObjectName('start_screen_recent_alert')

    self.start_screen_adver_label = QLabel('BASIC VERSION', parent=self.start_screen)
    self.start_screen_adver_label.setObjectName('start_screen_adver_label')

    self.start_screen_adver_label_details = QLabel('If you need more features,<br>enable the advanced version.<br>Visit <b>subtitld.jonata.org</b> for<br>more information.', parent=self.start_screen)
    self.start_screen_adver_label_details.setObjectName('start_screen_adver_label_details')

def resized(self):
    self.start_screen.setGeometry(0,self.height()-200,self.width(),200)
    self.start_screen_recentfiles_background.setGeometry((self.start_screen.width()*.5)-175, 0, 350, self.start_screen.height())
    self.start_screen_top_shadow.setGeometry(0, 0, self.start_screen.width(), 150)
    self.start_screen_open_label.setGeometry(0,20,(self.start_screen.width()*.5)-195,20)
    self.start_screen_recent_label.setGeometry((self.start_screen.width()*.5)-175,20,350,20)
    self.start_screen_adver_label.setGeometry((self.start_screen.width()*.5)+195,20,(self.start_screen.width()*.5)-185,20)
    self.start_screen_open_button.setGeometry((self.start_screen.width()*.5)-195-200,50,200,40)
    self.start_screen_recent_listwidget.setGeometry((self.start_screen.width()*.5)-155,50,310,self.start_screen.height()-50-20)
    self.start_screen_recent_alert.setGeometry((self.start_screen.width()*.5)-155,50,310,self.start_screen.height()-50-20)
    self.start_screen_adver_label_details.setGeometry((self.start_screen.width()*.5)+195, 50, (self.start_screen.width()*.5)-155, self.start_screen.height()-50-20)

def show(self):
    if self.settings['recent_files']:
        self.start_screen_recent_alert.setVisible(False)
        for date in reversed(sorted(self.settings['recent_files'].keys())):
            self.start_screen_recent_listwidget.addItem(self.settings['recent_files'][date])
    else:
        self.start_screen_recent_listwidget.setVisible(False)
    self.generate_effect(self.start_screen_transparency_animation, 'opacity', 2000, 0.0, 1.0)

def hide(self):
    self.generate_effect(self.start_screen_transparency_animation, 'opacity', 200, 1.0, 0.0)
    self.generate_effect(self.background_label2_transparency_animation, 'opacity', 500, 1.0, 0.0)

def start_screen_open_button_clicked(self):
    self.subtitleslist.open_button_clicked(self)

def start_screen_recent_listwidget_item_clicked(self):
    file_to_open = self.start_screen_recent_listwidget.currentItem().text()
    file_io.open_filepath(self, file_to_open)
