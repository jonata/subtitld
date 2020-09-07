#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os

from modules import file_io
from modules.paths import LIST_OF_SUPPORTED_SUBTITLE_EXTENSIONS

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton, QLabel, QFileDialog, QListWidget, QListView, QMessageBox
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, Qt, QSize


def load(self, PATH_SUBTITLD_GRAPHICS):
    self.subtitles_list_widget = QLabel(parent=self)
    self.subtitles_list_widget.setObjectName('subtitles_list_widget')
    self.subtitles_list_widget_animation = QPropertyAnimation(self.subtitles_list_widget, b'geometry')
    self.subtitles_list_widget_animation.setEasingCurve(QEasingCurve.OutCirc)

    self.toppanel_save_button = QPushButton(parent=self.subtitles_list_widget)
    self.toppanel_save_button.clicked.connect(lambda: toppanel_save_button_clicked(self))
    self.toppanel_save_button.setIcon(QIcon(os.path.join(PATH_SUBTITLD_GRAPHICS, 'save_icon.png')))
    self.toppanel_save_button.setIconSize(QSize(20, 20))
    self.toppanel_save_button.setObjectName('button_dark')
    self.toppanel_save_button.setStyleSheet('QPushButton {padding-left:20px;border-left:0;border-right:0;}')

    self.toppanel_open_button = QPushButton(parent=self.subtitles_list_widget)
    self.toppanel_open_button.clicked.connect(lambda: toppanel_open_button_clicked(self))
    self.toppanel_open_button.setIcon(QIcon(os.path.join(PATH_SUBTITLD_GRAPHICS, 'open_icon.png')))
    self.toppanel_open_button.setIconSize(QSize(20, 20))
    self.toppanel_open_button.setObjectName('button')
    self.toppanel_open_button.setStyleSheet('QPushButton {border-left:0;}')

    self.toppanel_subtitle_file_info_label = QLabel(parent=self.subtitles_list_widget)
    self.toppanel_subtitle_file_info_label.setObjectName('toppanel_subtitle_file_info_label')

    self.subtitles_list_qlistwidget = QListWidget(parent=self.subtitles_list_widget)
    self.subtitles_list_qlistwidget.setViewMode(QListView.ListMode)
    self.subtitles_list_qlistwidget.setObjectName('subtitles_list_qlistwidget')
    self.subtitles_list_qlistwidget.setSpacing(5)
    self.subtitles_list_qlistwidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    self.subtitles_list_qlistwidget.setFocusPolicy(Qt.NoFocus)
    self.subtitles_list_qlistwidget.setIconSize(QSize(42, 42))
    self.subtitles_list_qlistwidget.clicked.connect(lambda: subtitles_list_qlistwidget_item_clicked(self))

    self.subtitles_list_toggle_button = QPushButton(parent=self)
    self.subtitles_list_toggle_button.clicked.connect(lambda: subtitles_list_toggle_button_clicked(self))
    self.subtitles_list_toggle_button.setCheckable(True)
    self.subtitles_list_toggle_button.setObjectName('subtitles_list_toggle_button')
    self.subtitles_list_toggle_button_animation = QPropertyAnimation(self.subtitles_list_toggle_button, b'geometry')
    self.subtitles_list_toggle_button_animation.setEasingCurve(QEasingCurve.OutCirc)


def resized(self):
    if self.subtitles_list or self.video_metadata:
        self.subtitles_list_widget.setGeometry(0, 0, (self.width()*.2)-15, self.height())
    else:
        self.subtitles_list_widget.setGeometry(-((self.width()*.2)-15), 0, (self.width()*.2)-15, self.height())

    self.toppanel_save_button.setGeometry(0, 20, 60, 40)
    self.toppanel_open_button.setGeometry(self.toppanel_save_button.x()+self.toppanel_save_button.width(), self.toppanel_save_button.y(), self.toppanel_save_button.height(), self.toppanel_save_button.height())
    self.toppanel_subtitle_file_info_label.setGeometry(self.toppanel_open_button.x()+self.toppanel_open_button.width()+10, self.toppanel_save_button.y(), self.subtitles_list_widget.width()-self.toppanel_open_button.x()-self.toppanel_open_button.width()-40, self.toppanel_save_button.height())

    self.subtitles_list_qlistwidget.setGeometry(20, 100, self.subtitles_list_widget.width()-40, self.subtitles_list_widget.height()-80-self.playercontrols_widget.height()-35)

    if (self.subtitles_list or self.video_metadata):
        if self.subtitles_list_toggle_button.isChecked():
            self.subtitles_list_toggle_button.setGeometry(self.global_subtitlesvideo_panel_widget.width()-25, 0, 25, 80)
        else:
            self.subtitles_list_toggle_button.setGeometry(self.subtitles_list_widget.width()-25, 0, 25, 80)
    else:
        self.subtitles_list_toggle_button.setGeometry(-25, 0, 25, 80)


def subtitles_list_toggle_button_clicked(self):
    if self.subtitles_list_toggle_button.isChecked():
        subtitleslist_toggle_button_to_end(self)
        self.global_subtitlesvideo_panel.show_global_subtitlesvideo_panel(self)
        hide(self)
    else:
        self.global_subtitlesvideo_panel.hide_global_subtitlesvideo_panel(self)
        show(self)


def subtitleslist_toggle_button_to_end(self):
    self.generate_effect(self.subtitles_list_toggle_button_animation, 'geometry', 700, [self.subtitles_list_toggle_button.x(), self.subtitles_list_toggle_button.y(), self.subtitles_list_toggle_button.width(), self.subtitles_list_toggle_button.height()], [self.global_subtitlesvideo_panel_widget.width()-25, self.subtitles_list_toggle_button.y(), self.subtitles_list_toggle_button.width(), self.subtitles_list_toggle_button.height()])


def update_subtitles_list_widget(self):
    # self.subtitles_list_qlistwidget.setVisible(bool(self.subtitles_list))
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
        if not (self.player_widget.position > self.selected_subtitle[0] and self.player_widget.position < self.selected_subtitle[0] + self.selected_subtitle[1]):
            self.player_widget.seek(self.selected_subtitle[0] + (self.selected_subtitle[1]*.5))

    self.properties.update_properties_widget(self)
    self.timeline.update(self)
    self.timeline.update_scrollbar(self, position='middle')


def show(self):
    self.generate_effect(self.subtitles_list_widget_animation, 'geometry', 700, [self.subtitles_list_widget.x(), self.subtitles_list_widget.y(), self.subtitles_list_widget.width(), self.subtitles_list_widget.height()], [0, self.subtitles_list_widget.y(), self.subtitles_list_widget.width(), self.subtitles_list_widget.height()])
    self.generate_effect(self.subtitles_list_toggle_button_animation, 'geometry', 700, [self.subtitles_list_toggle_button.x(), self.subtitles_list_toggle_button.y(), self.subtitles_list_toggle_button.width(), self.subtitles_list_toggle_button.height()], [self.subtitles_list_widget.width()-25, self.subtitles_list_toggle_button.y(), self.subtitles_list_toggle_button.width(), self.subtitles_list_toggle_button.height()])
    self.global_subtitlesvideo_panel.hide_global_subtitlesvideo_panel(self)
    update_toppanel_subtitle_file_info_label(self)

    if not self.advanced_mode:
        self.subtitles_list_toggle_button.setEnabled(False)


def hide(self):
    self.generate_effect(self.subtitles_list_widget_animation, 'geometry', 700, [self.subtitles_list_widget.x(), self.subtitles_list_widget.y(), self.subtitles_list_widget.width(), self.subtitles_list_widget.height()], [-int(self.width()*.2), self.subtitles_list_widget.y(), self.subtitles_list_widget.width(), self.subtitles_list_widget.height()])


def toppanel_save_button_clicked(self):
    actual_subtitle_file = False
    if self.actual_subtitle_file:
        for ext in LIST_OF_SUPPORTED_SUBTITLE_EXTENSIONS[self.format_to_save]['extensions']:
            if self.actual_subtitle_file.endswith(ext):
                actual_subtitle_file = self.actual_subtitle_file
                break

    if not actual_subtitle_file:
        suggested_path = os.path.dirname(self.video_metadata['filepath'])
        if self.advanced_mode:
            save_formats = self.format_to_save + ' ' + LIST_OF_SUPPORTED_SUBTITLE_EXTENSIONS[self.format_to_save]['description'] + ' ({})'.format(" ".join(["*.{}".format(fo) for fo in LIST_OF_SUPPORTED_SUBTITLE_EXTENSIONS[self.format_to_save]['extensions']]))

            for format in LIST_OF_SUPPORTED_SUBTITLE_EXTENSIONS:
                if not format == self.format_to_save:
                    save_formats += ';;' + format + ' ' + LIST_OF_SUPPORTED_SUBTITLE_EXTENSIONS[format]['description'] + ' ({})'.format(" ".join(["*.{}".format(fo) for fo in LIST_OF_SUPPORTED_SUBTITLE_EXTENSIONS[format]['extensions']]))
            suggested_name = os.path.basename(self.video_metadata['filepath']).rsplit('.', 1)[0]
        else:
            save_formats = self.tr('SRT file') + ' (.srt)'
            suggested_name = os.path.basename(self.video_metadata['filepath']).rsplit('.', 1)[0] + '.srt'
        # tem que reportar o bug que não retorna o selectedFilter se o dialogo for nativo
        filedialog = QFileDialog.getSaveFileName(self, self.tr('Select the subtitle file'), os.path.join(suggested_path, suggested_name), save_formats, options=QFileDialog.DontUseNativeDialog)

        if filedialog[0] and filedialog[1]:
            filename = filedialog[0]
            exts = []
            for ext in filedialog[1].split('(', 1)[1].split(')', 1)[0].split('*'):
                if ext:
                    exts.append(ext.strip())
            if not filename.endswith(tuple(exts)):
                filename += exts[0]
            if not self.format_to_save == filedialog[1].split(' ', 1)[0]:
                self.format_to_save = filedialog[1].split(' ', 1)[0]

            self.global_subtitlesvideo_panel.update_global_subtitlesvideo_save_as_combobox(self)

            self.actual_subtitle_file = filename

    if self.actual_subtitle_file:
        file_io.save_file(self.actual_subtitle_file, self.subtitles_list, self.format_to_save, self.selected_language)
        update_toppanel_subtitle_file_info_label(self)
        self.unsaved = False


def toppanel_open_button_clicked(self):
    if self.unsaved:
        save_message_box = QMessageBox(self)

        save_message_box.setWindowTitle(self.tr('Unsaved changes'))
        save_message_box.setText(
            self.tr('Do you want to save the changes you made on the subtitles?')
        )
        save_message_box.addButton(self.tr('Save'), QMessageBox.AcceptRole)
        save_message_box.addButton(self.tr("Don't save"), QMessageBox.RejectRole)
        ret = save_message_box.exec_()

        if ret == QMessageBox.AcceptRole:
            self.subttileslist.toppanel_save_button_clicked(self)
    file_io.open_filepath(self)


def update_toppanel_subtitle_file_info_label(self):
    text = self.tr('Actual video does not have saved subtitle file.')
    if self.actual_subtitle_file:
        text = '<b><snall>' + self.tr('Actual project').upper() + '</small></b><br><big>' + os.path.basename(self.actual_subtitle_file) + '</big>'
    self.toppanel_subtitle_file_info_label.setText(text)
