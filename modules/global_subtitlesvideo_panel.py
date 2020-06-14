#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os

from PyQt5.QtWidgets import QLabel, QComboBox, QPushButton, QFileDialog
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve

from modules.paths import LIST_OF_SUPPORTED_SUBTITLE_EXTENSIONS, LIST_OF_SUPPORTED_IMPORT_EXTENSIONS
from modules import file_io

list_of_supported_import_extensions = []
for type in LIST_OF_SUPPORTED_IMPORT_EXTENSIONS.keys():
    for ext in LIST_OF_SUPPORTED_IMPORT_EXTENSIONS[type]['extensions']:
        list_of_supported_import_extensions.append(ext)


def load(self, PATH_SUBTITLD_GRAPHICS):
    self.global_subtitlesvideo_panel_widget = QLabel(parent=self)
    self.global_subtitlesvideo_panel_widget_animation = QPropertyAnimation(self.global_subtitlesvideo_panel_widget, b'geometry')
    self.global_subtitlesvideo_panel_widget_animation.setEasingCurve(QEasingCurve.OutCirc)

    self.global_subtitlesvideo_panel_left = QLabel(parent=self.global_subtitlesvideo_panel_widget)
    self.global_subtitlesvideo_panel_left.setObjectName('global_subtitlesvideo_panel_left')
    self.global_subtitlesvideo_panel_right = QLabel(parent=self.global_subtitlesvideo_panel_widget)
    self.global_subtitlesvideo_panel_right.setObjectName('global_subtitlesvideo_panel_right')

    self.global_subtitlesvideo_save_as_label = QLabel(u'DEFAULT FORMAT TO SAVE:', parent=self.global_subtitlesvideo_panel_widget)

    list_of_subtitle_extensions = []
    for ext in LIST_OF_SUPPORTED_SUBTITLE_EXTENSIONS:
        list_of_subtitle_extensions.append(ext + ' - ' + LIST_OF_SUPPORTED_SUBTITLE_EXTENSIONS[ext]['description'])
    self.global_subtitlesvideo_save_as_combobox = QComboBox(parent=self.global_subtitlesvideo_panel_widget)
    self.global_subtitlesvideo_save_as_combobox.addItems(list_of_subtitle_extensions)
    self.global_subtitlesvideo_save_as_combobox.activated.connect(lambda: global_subtitlesvideo_save_as_combobox_activated(self))

    self.global_subtitlesvideo_import_button = QPushButton(u'IMPORT', parent=self.global_subtitlesvideo_panel_widget)
    self.global_subtitlesvideo_import_button.setObjectName('button')
    # self.global_subtitlesvideo_import_button.setCheckable(True)
    self.global_subtitlesvideo_import_button.clicked.connect(lambda: global_subtitlesvideo_import_button_clicked(self))

    # self.global_subtitlesvideo_import_panel = QLabel(parent=self.global_subtitlesvideo_panel_widget)
    # self.global_subtitlesvideo_import_panel.setVisible(False)

    # self.global_subtitlesvideo_import_panel_radiobox = QRadioBox(parent=self.global_subtitlesvideo_import_panel)

    self.global_subtitlesvideo_export_button = QPushButton(u'EXPORT', parent=self.global_subtitlesvideo_panel_widget)
    self.global_subtitlesvideo_export_button.setObjectName('button')
    self.global_subtitlesvideo_export_button.clicked.connect(lambda: global_subtitlesvideo_export_button_clicked(self))


def resized(self):
    if (self.subtitles_list or self.video_metadata):
        if self.subtitles_list_toggle_button.isChecked():
            self.global_subtitlesvideo_panel_widget.setGeometry(0, 0, self.width()*.8, self.height()-self.playercontrols_widget.height()+20)
        else:
            self.global_subtitlesvideo_panel_widget.setGeometry(-(self.width()*.6)-18, 0, self.width()*.8, self.height()-self.playercontrols_widget.height()+20)
    else:
        self.global_subtitlesvideo_panel_widget.setGeometry(-(self.width()*.8), 0, self.width()*.8, self.height()-self.playercontrols_widget.height()+20)

    self.global_subtitlesvideo_panel_left.setGeometry(0, 0, self.width()*.2, self.global_subtitlesvideo_panel_widget.height())
    self.global_subtitlesvideo_panel_right.setGeometry(self.global_subtitlesvideo_panel_left.width(), 0, self.global_subtitlesvideo_panel_widget.width()-self.global_subtitlesvideo_panel_left.width(), self.global_subtitlesvideo_panel_widget.height())

    self.global_subtitlesvideo_save_as_label.setGeometry(20, 20, self.global_subtitlesvideo_panel_left.width()-40, 20)
    self.global_subtitlesvideo_save_as_combobox.setGeometry(20, 40, self.global_subtitlesvideo_panel_left.width()-40, 30)

    self.global_subtitlesvideo_import_button.setGeometry(20, 80, self.global_subtitlesvideo_panel_left.width()-40, 30)
    # self.global_subtitlesvideo_import_panel.setGeometry(20, 110, self.global_subtitlesvideo_panel_left.width()-40, 100)
    self.global_subtitlesvideo_export_button.setGeometry(20, 120, self.global_subtitlesvideo_panel_left.width()-40, 30)


def show_global_subtitlesvideo_panel(self):
    self.generate_effect(self.global_subtitlesvideo_panel_widget_animation, 'geometry', 700, [self.global_subtitlesvideo_panel_widget.x(), self.global_subtitlesvideo_panel_widget.y(), self.global_subtitlesvideo_panel_widget.width(), self.global_subtitlesvideo_panel_widget.height()], [0, self.global_subtitlesvideo_panel_widget.y(), self.global_subtitlesvideo_panel_widget.width(), self.global_subtitlesvideo_panel_widget.height()])


def global_subtitlesvideo_import_button_clicked(self):
    # if self.global_subtitlesvideo_import_button.isChecked():
    #     self.global_subtitlesvideo_export_button.setGeometry(20, 200, self.global_subtitlesvideo_panel_left.width()-40, 30)
    # else:
    #     self.global_subtitlesvideo_export_button.setGeometry(20, 120, self.global_subtitlesvideo_panel_left.width()-40, 30)
    # self.global_subtitlesvideo_import_panel.setVisible(self.global_subtitlesvideo_import_button.isChecked())

    supported_import_files = "Text files ({})".format(" ".join(["*.{}".format(fo) for fo in list_of_supported_import_extensions]))
    file_to_open = QFileDialog.getOpenFileName(self, "Select the file to import", os.path.expanduser("~"), supported_import_files)[0]
    if file_to_open:
        self.subtitles_list += file_io.import_file(filename=file_to_open)[0]


def global_subtitlesvideo_export_button_clicked(self):
    suggested_path = os.path.dirname(self.video_metadata['filepath'])
    suggested_name = os.path.basename(self.video_metadata['filepath']).rsplit('.', 1)[0] + '.txt'
    save_formats = 'TXT file (.txt)'

    filedialog = QFileDialog.getSaveFileName(self, "Export to file", os.path.join(suggested_path, suggested_name), save_formats, options=QFileDialog.DontUseNativeDialog)

    if filedialog[0] and filedialog[1]:
        filename = filedialog[0]
        exts = []
        for ext in filedialog[1].split('(', 1)[1].split(')', 1)[0].split('*'):
            if ext:
                exts.append(ext.strip())
        if not filename.endswith(tuple(exts)):
            filename += exts[0]
        format_to_export = filedialog[1].split(' ', 1)[0]

        file_io.export_file(filename=filename, subtitles_list=self.subtitles_list, format=format_to_export)


def hide_global_subtitlesvideo_panel(self):
    self.generate_effect(self.global_subtitlesvideo_panel_widget_animation, 'geometry', 700, [self.global_subtitlesvideo_panel_widget.x(), self.global_subtitlesvideo_panel_widget.y(), self.global_subtitlesvideo_panel_widget.width(), self.global_subtitlesvideo_panel_widget.height()], [int(-(self.width()*.6))-18, self.global_subtitlesvideo_panel_widget.y(), self.global_subtitlesvideo_panel_widget.width(), self.global_subtitlesvideo_panel_widget.height()])


def update_global_subtitlesvideo_save_as_combobox(self):
    self.global_subtitlesvideo_save_as_combobox.setCurrentText(self.format_to_save + ' - ' + LIST_OF_SUPPORTED_SUBTITLE_EXTENSIONS[self.format_to_save]['description'])


def global_subtitlesvideo_save_as_combobox_activated(self):
    self.format_to_save = self.global_subtitlesvideo_save_as_combobox.currentText().split(' ', 1)[0]
