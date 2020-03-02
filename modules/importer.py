#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
from PyQt5.QtWidgets import QPushButton, QLabel, QTextEdit
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, Qt, QRect

def load(self, path_okp_graphics):
    self.importer.widget = QLabel(parent=self)
    #self.importer.widget.setAttribute(Qt.WA_TransparentForMouseEvents)
    self.importer.widget_animation = QPropertyAnimation(self.importer.widget, b'geometry')
    self.importer.widget_animation.setEasingCurve(QEasingCurve.OutCirc)

    self.importer.widget_bottom_background = QLabel(parent=self.importer.widget)
    self.importer.widget_bottom_background.setStyleSheet('QLabel { border-top: 18px; border-right: 0; border-bottom: 0; border-left: 48px; border-image: url("' + os.path.join(path_okp_graphics, "importer_background.png").replace('\\', '/') + '") 18 0 0 48 stretch stretch;}')

    self.importer.widget_top_background = QLabel(parent=self.importer.widget)
    #self.importer.widget_top_background.setAttribute(Qt.WA_TranslucentBackground, True)
    self.importer.widget_top_background.setStyleSheet('QLabel { border-top: 0; border-right: 0; border-bottom: 0; border-left: 48px; border-image: url("' + os.path.join(path_okp_graphics, "importer_background_top.png").replace('\\', '/') + '") 0 0 0 48 stretch stretch;}')

    self.importer.textedit = QTextEdit(parent=self.importer.widget)
    #self.importer.textedit.textChanged.connect(lambda:importer.textedit_changed(self))

    self.importer.import_button = QPushButton('IMPORT', parent=self.importer.widget)
    self.importer.import_button.clicked.connect(lambda:import_button_clicked(self))
    self.importer.import_button.setStyleSheet('    QPushButton { font-size:10px; color:white; border-left: 5px; border-top: 0; border-right: 5px; border-bottom: 5px; border-image: url("' + os.path.join(path_okp_graphics, 'button_3_normal.png').replace('\\', '/') + '") 5 5 5 5 stretch stretch; outline: none; } \
                                                            QPushButton:checked { border-left: 5px; border-top: 0; border-right: 5px; border-bottom: 5px; border-image: url("' + os.path.join(path_okp_graphics, 'button_3_pressed.png').replace('\\', '/') + '") 5 5 5 5 stretch stretch; outline: none; } \
                                                            QPushButton:hover:pressed { border-left: 5px; border-top: 0; border-right: 5px; border-bottom: 5px; border-image: url("' + os.path.join(path_okp_graphics, 'button_3_pressed.png').replace('\\', '/') + '") 5 5 5 5 stretch stretch; outline: none; } \
                                                            QPushButton:disabled { border-left: 5px; border-top: 0; border-right: 5px; border-bottom: 5px; border-image: url("' + os.path.join(path_okp_graphics, 'button_3_disabled.png').replace('\\', '/') + '") 5 5 5 5 stretch stretch; outline: none; } \
                                                            QPushButton:hover { border-left: 5px; border-top: 0; border-right: 5px; border-bottom: 5px; border-image: url("' + os.path.join(path_okp_graphics, 'button_3_hover.png').replace('\\', '/') + '") 5 5 5 5 stretch stretch; outline: none; } ')

def resized(self):
    if self.show_importer_panel_button.isChecked():
        self.importer.widget.setGeometry(self.width()-300,0,300,self.height())
    else:
        self.importer.widget.setGeometry(self.width(),0,300,self.height())

    self.importer.widget_top_background.setGeometry(0,0,self.importer.widget.width(),self.importer.widget.height()-60)
    self.importer.widget_bottom_background.setGeometry(0,self.importer.widget.height()-60,self.importer.widget.width(), 60)

    self.importer.textedit.setGeometry(50,10,self.importer.widget.width()-60,self.importer.widget.height()-50)

    self.importer.import_button.setGeometry(50,self.importer.widget.height()-40,self.importer.widget.width()-60,30)

def import_button_clicked(self):
    lines = self.importer.textedit.toPlainText().split('\n')
    start_in = 0
    note = 0
    if len(self.lyrics_notes) > 0:
        start_in = int(self.lyrics_notes[-1][0] + self.lyrics_notes[-1][1])

    left_music = (self.lyrics_metadata['duration'] - (self.lyrics_metadata['gap']*.0001)) / 60.0
    proportion = int((left_music * self.lyrics_metadata['bpm']) /  len(lines))*3

    for line in lines:
        self.lyrics_notes.append([start_in,proportion-1,note,line,':'])
        start_in += proportion-1
        self.lyrics_notes.append([start_in,'-'])
        start_in += 1
