#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import subprocess

from PyQt5.QtWidgets import QLabel, QComboBox, QPushButton, QFileDialog, QSpinBox, QColorDialog, QTabWidget, QWidget, QTableWidget, QAbstractItemView, QLineEdit, QTableWidgetItem, QHeaderView, QMessageBox
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, QThread, pyqtSignal, QEvent, Qt
from PyQt5.QtGui import QFontDatabase, QKeySequence

from modules.paths import LIST_OF_SUPPORTED_SUBTITLE_EXTENSIONS, LIST_OF_SUPPORTED_IMPORT_EXTENSIONS, STARTUPINFO, FFMPEG_EXECUTABLE, path_tmp
from modules import file_io
from modules.shortcuts import shortcuts_dict
from modules.paths import LANGUAGE_DICT_LIST

LANGUAGE_DESCRIPTIONS = LANGUAGE_DICT_LIST.keys()

list_of_supported_import_extensions = []
for type in LIST_OF_SUPPORTED_IMPORT_EXTENSIONS.keys():
    for ext in LIST_OF_SUPPORTED_IMPORT_EXTENSIONS[type]['extensions']:
        list_of_supported_import_extensions.append(ext)


def convert_ffmpeg_timecode_to_seconds(timecode):
    if timecode:
        final_value = float(timecode.split(':')[-1])
        final_value += int(timecode.split(':')[-2])*60.0
        final_value += int(timecode.split(':')[-3])*3600.0
        return final_value
    else:
        return False


class thread_generated_burned_video(QThread):
    response = pyqtSignal(str)
    commands = []

    def run(self):
        if self.commands:
            p = subprocess.Popen(self.commands, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, startupinfo=STARTUPINFO, bufsize=4096)
            number_of_steps = 0.001
            current_step = 0.0
            while p.poll() is None:
                # for output in p.stdout.read().decode().split('\n'):
                output = p.stdout.readline()
                if 'Duration: ' in output:
                    duration = int(convert_ffmpeg_timecode_to_seconds(output.split('Duration: ', 1)[1].split(',', 1)[0]))
                    if duration > number_of_steps:
                        number_of_steps = duration
                if output[:6] == 'frame=':
                    current_step = int(convert_ffmpeg_timecode_to_seconds(output.split('time=', 1)[1].split(' ', 1)[0]))

                self.response.emit(str(current_step) + '|' + str(number_of_steps))
            self.response.emit('end')


def load(self, PATH_SUBTITLD_GRAPHICS):
    self.global_subtitlesvideo_panel_widget = QLabel(parent=self)
    self.global_subtitlesvideo_panel_widget_animation = QPropertyAnimation(self.global_subtitlesvideo_panel_widget, b'geometry')
    self.global_subtitlesvideo_panel_widget_animation.setEasingCurve(QEasingCurve.OutCirc)

    self.global_subtitlesvideo_panel_left = QLabel(parent=self.global_subtitlesvideo_panel_widget)
    self.global_subtitlesvideo_panel_left.setObjectName('global_subtitlesvideo_panel_left')
    self.global_subtitlesvideo_panel_right = QLabel(parent=self.global_subtitlesvideo_panel_widget)
    self.global_subtitlesvideo_panel_right.setObjectName('global_subtitlesvideo_panel_right')

    self.global_subtitlesvideo_save_as_label = QLabel(self.tr('Default format to save:').upper(), parent=self.global_subtitlesvideo_panel_widget)

    list_of_subtitle_extensions = []
    for ext in LIST_OF_SUPPORTED_SUBTITLE_EXTENSIONS:
        list_of_subtitle_extensions.append(ext + ' - ' + LIST_OF_SUPPORTED_SUBTITLE_EXTENSIONS[ext]['description'])
    self.global_subtitlesvideo_save_as_combobox = QComboBox(parent=self.global_subtitlesvideo_panel_widget)
    self.global_subtitlesvideo_save_as_combobox.setObjectName('button')
    self.global_subtitlesvideo_save_as_combobox.addItems(list_of_subtitle_extensions)
    self.global_subtitlesvideo_save_as_combobox.activated.connect(lambda: global_subtitlesvideo_save_as_combobox_activated(self))

    self.global_subtitlesvideo_import_button = QPushButton(u'IMPORT', parent=self.global_subtitlesvideo_panel_widget)
    self.global_subtitlesvideo_import_button.setObjectName('button')
    # self.global_subtitlesvideo_import_button.setCheckable(True)
    self.global_subtitlesvideo_import_button.clicked.connect(lambda: global_subtitlesvideo_import_button_clicked(self))

    # self.global_subtitlesvideo_import_panel = QLabel(parent=self.global_subtitlesvideo_panel_widget)
    # self.global_subtitlesvideo_import_panel.setVisible(False)

    # self.global_subtitlesvideo_import_panel_radiobox = QRadioBox(parent=self.global_subtitlesvideo_import_panel)

    self.global_subtitlesvideo_export_button = QPushButton(self.tr('Export').upper(), parent=self.global_subtitlesvideo_panel_widget)
    self.global_subtitlesvideo_export_button.setObjectName('button')
    self.global_subtitlesvideo_export_button.clicked.connect(lambda: global_subtitlesvideo_export_button_clicked(self))

    self.global_subtitlesvideo_autosync_lang_combobox = QComboBox(parent=self.global_subtitlesvideo_panel_widget)
    self.global_subtitlesvideo_autosync_lang_combobox.setObjectName('button')
    self.global_subtitlesvideo_autosync_lang_combobox.addItems(LANGUAGE_DESCRIPTIONS)

    self.global_subtitlesvideo_autosync_button = QPushButton(self.tr('AutoSync').upper(), parent=self.global_subtitlesvideo_panel_widget)
    self.global_subtitlesvideo_autosync_button.setObjectName('button')
    self.global_subtitlesvideo_autosync_button.clicked.connect(lambda: global_subtitlesvideo_autosync_button_clicked(self))

    self.global_subtitlesvideo_autosub_button = QPushButton(self.tr('Auto Subtitle').upper(), parent=self.global_subtitlesvideo_panel_widget)
    self.global_subtitlesvideo_autosub_button.setObjectName('button')
    self.global_subtitlesvideo_autosub_button.clicked.connect(lambda: global_subtitlesvideo_autosub_button_clicked(self))

    self.global_subtitlesvideo_panel_tabwidget = QTabWidget(parent=self.global_subtitlesvideo_panel_widget)

    self.global_subtitlesvideo_panel_tabwidget_export_panel = QWidget()

    self.global_subtitlesvideo_video_burn_label = QLabel(self.tr('Export burned video').upper(), parent=self.global_subtitlesvideo_panel_tabwidget_export_panel)
    self.global_subtitlesvideo_video_burn_label.setStyleSheet('QLabel { font-size:14px; font-weight:bold; }')

    self.global_subtitlesvideo_video_burn_fontname_label = QLabel(self.tr('Font name').upper(), parent=self.global_subtitlesvideo_panel_tabwidget_export_panel)

    fonts = QFontDatabase().families()
    self.global_subtitlesvideo_video_burn_fontname = QComboBox(parent=self.global_subtitlesvideo_panel_tabwidget_export_panel)
    self.global_subtitlesvideo_video_burn_fontname.setObjectName('button')
    self.global_subtitlesvideo_video_burn_fontname.addItems(fonts)
    # self.global_subtitlesvideo_video_burn_fontname.activated.connect(lambda: global_subtitlesvideo_save_as_combobox_activated(self))

    self.global_subtitlesvideo_video_burn_fontsize_label = QLabel(self.tr('Font size').upper(), parent=self.global_subtitlesvideo_panel_tabwidget_export_panel)

    self.global_subtitlesvideo_video_burn_fontsize = QSpinBox(parent=self.global_subtitlesvideo_panel_tabwidget_export_panel)
    self.global_subtitlesvideo_video_burn_fontsize.setMinimum(8)
    self.global_subtitlesvideo_video_burn_fontsize.setMaximum(200)
    self.global_subtitlesvideo_video_burn_fontsize.setValue(20)

    self.global_subtitlesvideo_video_burn_shadowdistance_label = QLabel(self.tr('Shadow distance').upper(), parent=self.global_subtitlesvideo_panel_tabwidget_export_panel)

    self.global_subtitlesvideo_video_burn_shadowdistance = QSpinBox(parent=self.global_subtitlesvideo_panel_tabwidget_export_panel)
    self.global_subtitlesvideo_video_burn_shadowdistance.setMinimum(0)
    self.global_subtitlesvideo_video_burn_shadowdistance.setMaximum(20)
    self.global_subtitlesvideo_video_burn_shadowdistance.setValue(1)

    self.global_subtitlesvideo_video_burn_outline_label = QLabel(self.tr('Outline').upper(), parent=self.global_subtitlesvideo_panel_tabwidget_export_panel)

    self.global_subtitlesvideo_video_burn_outline = QSpinBox(parent=self.global_subtitlesvideo_panel_tabwidget_export_panel)
    self.global_subtitlesvideo_video_burn_outline.setMinimum(0)
    self.global_subtitlesvideo_video_burn_outline.setMaximum(20)
    self.global_subtitlesvideo_video_burn_outline.setValue(2)

    self.global_subtitlesvideo_video_burn_marvinv_label = QLabel(self.tr('Margin from bottom').upper(), parent=self.global_subtitlesvideo_panel_tabwidget_export_panel)

    self.global_subtitlesvideo_video_burn_marvinv = QSpinBox(parent=self.global_subtitlesvideo_panel_tabwidget_export_panel)
    self.global_subtitlesvideo_video_burn_marvinv.setMinimum(0)
    self.global_subtitlesvideo_video_burn_marvinv.setMaximum(500)
    self.global_subtitlesvideo_video_burn_marvinv.setValue(20)

    self.global_subtitlesvideo_video_burn_marvinl_label = QLabel(self.tr('Margin from left').upper(), parent=self.global_subtitlesvideo_panel_tabwidget_export_panel)

    self.global_subtitlesvideo_video_burn_marvinl = QSpinBox(parent=self.global_subtitlesvideo_panel_tabwidget_export_panel)
    self.global_subtitlesvideo_video_burn_marvinl.setMinimum(0)
    self.global_subtitlesvideo_video_burn_marvinl.setMaximum(500)
    self.global_subtitlesvideo_video_burn_marvinl.setValue(50)

    self.global_subtitlesvideo_video_burn_marvinr_label = QLabel(self.tr('Margin from right').upper(), parent=self.global_subtitlesvideo_panel_tabwidget_export_panel)

    self.global_subtitlesvideo_video_burn_marvinr = QSpinBox(parent=self.global_subtitlesvideo_panel_tabwidget_export_panel)
    self.global_subtitlesvideo_video_burn_marvinr.setMinimum(0)
    self.global_subtitlesvideo_video_burn_marvinr.setMaximum(500)
    self.global_subtitlesvideo_video_burn_marvinr.setValue(50)

    self.global_subtitlesvideo_video_burn_pcolor_selected_color = '#ffffff'

    self.global_subtitlesvideo_video_burn_pcolor_label = QLabel(self.tr('Font color').upper(), parent=self.global_subtitlesvideo_panel_tabwidget_export_panel)

    self.global_subtitlesvideo_video_burn_pcolor = QPushButton(parent=self.global_subtitlesvideo_panel_tabwidget_export_panel)
    self.global_subtitlesvideo_video_burn_pcolor.clicked.connect(lambda: global_subtitlesvideo_video_burn_pcolor_clicked(self))
    self.global_subtitlesvideo_video_burn_pcolor.setStyleSheet('background-color:' + self.global_subtitlesvideo_video_burn_pcolor_selected_color)

    self.global_subtitlesvideo_video_burn_convert = QPushButton(self.tr('Generate video').upper(), parent=self.global_subtitlesvideo_panel_tabwidget_export_panel)
    self.global_subtitlesvideo_video_burn_convert.setObjectName('button_dark')
    self.global_subtitlesvideo_video_burn_convert.clicked.connect(lambda: global_subtitlesvideo_video_burn_convert_clicked(self))

    def thread_generated_burned_video_ended(response):
        if '|' in response:
            self.global_subtitlesvideo_video_burn_convert.setText('GENERATING... (' + str(int((float(response.split('|')[0]) / float(response.split('|')[1])) * 100)) + '%)')
        elif 'end' in response:
            self.global_subtitlesvideo_video_burn_convert.setText(self.tr('Generate video').upper())
            self.global_subtitlesvideo_video_burn_convert.setEnabled(True)

    self.thread_generated_burned_video = thread_generated_burned_video(self)
    self.thread_generated_burned_video.response.connect(thread_generated_burned_video_ended)

    self.global_subtitlesvideo_panel_tabwidget.addTab(self.global_subtitlesvideo_panel_tabwidget_export_panel, self.tr('Export burned-in subtitles').upper())

    self.global_subtitlesvideo_panel_tabwidget_shortkeys_panel = QWidget()

    class global_subtitlesvideo_panel_tabwidget_shortkeys_editbox(QLineEdit):
        # def __init__(self, keySequence, *args):
        #     super(global_subtitlesvideo_panel_tabwidget_shortkeys_editbox, self).__init__(*args)
        #
        #     self.keySequence = keySequence
        #     self.setKeySequence(keySequence)

        def setKeySequence(self, keySequence):
            self.keySequence = keySequence
            self.setText(self.keySequence.toString(QKeySequence.NativeText))

        def keyPressEvent(self, e):
            if e.type() == QEvent.KeyPress:
                key = e.key()

                if key == Qt.Key_unknown:
                    return

                if(key == Qt.Key_Control
                   or key == Qt.Key_Shift
                   or key == Qt.Key_Alt
                   or key == Qt.Key_Meta):
                    return

                modifiers = e.modifiers()
                # keyText = e.text()

                if modifiers & Qt.ShiftModifier:
                    key += Qt.SHIFT
                if modifiers & Qt.ControlModifier:
                    key += Qt.CTRL
                if modifiers & Qt.AltModifier:
                    key += Qt.ALT
                if modifiers & Qt.MetaModifier:
                    key += Qt.META

                self.setKeySequence(QKeySequence(key))

    self.global_subtitlesvideo_panel_tabwidget_shortkeys_editbox = global_subtitlesvideo_panel_tabwidget_shortkeys_editbox(parent=self.global_subtitlesvideo_panel_tabwidget_shortkeys_panel)
    self.global_subtitlesvideo_panel_tabwidget_shortkeys_editbox.setStyleSheet('QLineEdit { background-color:rgb(255, 255, 255); border: 1px solid silver; border-radius: 5px; padding: 5px 5px 5px 5px; font-size:16px; color:black; qproperty-alignment: "AlignCenter";}')

    self.global_subtitlesvideo_panel_tabwidget_shortkeys_editbox_confirm = QPushButton(self.tr('Confirm').upper(), parent=self.global_subtitlesvideo_panel_tabwidget_shortkeys_panel)
    self.global_subtitlesvideo_panel_tabwidget_shortkeys_editbox_confirm.setObjectName('button_dark')
    self.global_subtitlesvideo_panel_tabwidget_shortkeys_editbox_confirm.clicked.connect(lambda: global_subtitlesvideo_panel_tabwidget_shortkeys_editbox_confirm_clicked(self))

    self.global_subtitlesvideo_panel_tabwidget_shortkeys_editbox_cancel = QPushButton(self.tr('Cancel').upper(), parent=self.global_subtitlesvideo_panel_tabwidget_shortkeys_panel)
    self.global_subtitlesvideo_panel_tabwidget_shortkeys_editbox_cancel.setObjectName('button_dark')
    self.global_subtitlesvideo_panel_tabwidget_shortkeys_editbox_cancel.clicked.connect(lambda: global_subtitlesvideo_panel_tabwidget_shortkeys_editbox_cancel_clicked(self))

    self.global_subtitlesvideo_panel_tabwidget_shortkeys_table = QTableWidget(parent=self.global_subtitlesvideo_panel_tabwidget_shortkeys_panel)
    self.global_subtitlesvideo_panel_tabwidget_shortkeys_table.setColumnCount(2)
    self.global_subtitlesvideo_panel_tabwidget_shortkeys_table.verticalHeader().setVisible(False)
    self.global_subtitlesvideo_panel_tabwidget_shortkeys_table.horizontalHeader().setVisible(False)
    self.global_subtitlesvideo_panel_tabwidget_shortkeys_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    # self.global_subtitlesvideo_panel_tabwidget_shortkeys_table.setShowGrid(False)
    self.global_subtitlesvideo_panel_tabwidget_shortkeys_table.setSelectionBehavior(QAbstractItemView.SelectRows)
    # self.global_subtitlesvideo_panel_tabwidget_shortkeys_table.clicked.connect(lambda:project_new_panel_info_panel_options_pmaterials_panel_files_clicked(self))
    global_subtitlesvideo_panel_tabwidget_shortkeys_table_update(self)

    self.global_subtitlesvideo_panel_tabwidget_shortkeys_set_button = QPushButton(self.tr('Set shortcut').upper(), parent=self.global_subtitlesvideo_panel_tabwidget_shortkeys_panel)
    # self.global_subtitlesvideo_panel_tabwidget_shortkeys_set_button.setCheckable(True)
    self.global_subtitlesvideo_panel_tabwidget_shortkeys_set_button.setObjectName('button_dark')
    self.global_subtitlesvideo_panel_tabwidget_shortkeys_set_button.clicked.connect(lambda: global_subtitlesvideo_panel_tabwidget_shortkeys_set_button_clicked(self))

    self.global_subtitlesvideo_panel_tabwidget.addTab(self.global_subtitlesvideo_panel_tabwidget_shortkeys_panel, self.tr('Keyboard shortcuts').upper())


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
    self.global_subtitlesvideo_autosync_lang_combobox.setGeometry(20, 160, 75, 30)
    self.global_subtitlesvideo_autosync_button.setGeometry(100, 160, self.global_subtitlesvideo_panel_left.width()-120, 30)
    self.global_subtitlesvideo_autosub_button.setGeometry(100, 200, self.global_subtitlesvideo_panel_left.width()-120, 30)

    self.global_subtitlesvideo_panel_tabwidget.setGeometry(self.global_subtitlesvideo_panel_right.x()+20, 20, self.global_subtitlesvideo_panel_right.width()-50, self.global_subtitlesvideo_panel_right.height()-50)

    self.global_subtitlesvideo_video_burn_label.setGeometry(20, 20, 200, 20)
    self.global_subtitlesvideo_video_burn_fontname_label.setGeometry(20, 50, 200, 20)
    self.global_subtitlesvideo_video_burn_fontname.setGeometry(20, 70, 300, 30)

    self.global_subtitlesvideo_video_burn_fontsize_label.setGeometry(20, 110, 150, 20)
    self.global_subtitlesvideo_video_burn_fontsize.setGeometry(20, 130, 150, 30)
    self.global_subtitlesvideo_video_burn_shadowdistance_label.setGeometry(20+150+10, 110, 150, 20)
    self.global_subtitlesvideo_video_burn_shadowdistance.setGeometry(20+150+10, 130, 150, 30)
    self.global_subtitlesvideo_video_burn_outline_label.setGeometry(20+150+150+20, 110, 150, 20)
    self.global_subtitlesvideo_video_burn_outline.setGeometry(20+150+150+20, 130, 150, 30)
    self.global_subtitlesvideo_video_burn_marvinv_label.setGeometry(20, 170, 150, 20)
    self.global_subtitlesvideo_video_burn_marvinv.setGeometry(20, 190, 150, 30)
    self.global_subtitlesvideo_video_burn_marvinl_label.setGeometry(20+150+10, 170, 150, 20)
    self.global_subtitlesvideo_video_burn_marvinl.setGeometry(20+150+10, 190, 150, 30)
    self.global_subtitlesvideo_video_burn_marvinr_label.setGeometry(20+150+150+20, 170, 150, 20)
    self.global_subtitlesvideo_video_burn_marvinr.setGeometry(20+150+150+20, 190, 150, 30)
    self.global_subtitlesvideo_video_burn_pcolor_label.setGeometry(20+150+150+20+150+10, 170, 150, 20)
    self.global_subtitlesvideo_video_burn_pcolor.setGeometry(20+150+150+20+150+10, 190, 150, 30)
    self.global_subtitlesvideo_video_burn_convert.setGeometry(20, 240, 200, 40)

    self.global_subtitlesvideo_panel_tabwidget_shortkeys_panel.setGeometry(0, 0, self.global_subtitlesvideo_panel_tabwidget.width(), self.global_subtitlesvideo_panel_tabwidget.height())

    self.global_subtitlesvideo_panel_tabwidget_shortkeys_editbox.setGeometry((self.global_subtitlesvideo_panel_tabwidget_shortkeys_panel.width()*.5)-100, (self.global_subtitlesvideo_panel_tabwidget_shortkeys_panel.height()*.5)-50, 200, 60)
    self.global_subtitlesvideo_panel_tabwidget_shortkeys_editbox_confirm.setGeometry(self.global_subtitlesvideo_panel_tabwidget_shortkeys_editbox.x() + 20, self.global_subtitlesvideo_panel_tabwidget_shortkeys_editbox.y()+self.global_subtitlesvideo_panel_tabwidget_shortkeys_editbox.height(), 80, 40)
    self.global_subtitlesvideo_panel_tabwidget_shortkeys_editbox_cancel.setGeometry(self.global_subtitlesvideo_panel_tabwidget_shortkeys_editbox.x() + (self.global_subtitlesvideo_panel_tabwidget_shortkeys_editbox.width()*.5), self.global_subtitlesvideo_panel_tabwidget_shortkeys_editbox.y()+self.global_subtitlesvideo_panel_tabwidget_shortkeys_editbox.height(), 80, 40)

    self.global_subtitlesvideo_panel_tabwidget_shortkeys_table.setGeometry(20, 20, self.global_subtitlesvideo_panel_tabwidget_shortkeys_panel.width()-40, self.global_subtitlesvideo_panel_tabwidget_shortkeys_panel.height()-100)
    self.global_subtitlesvideo_panel_tabwidget_shortkeys_set_button.setGeometry(20+(self.global_subtitlesvideo_panel_tabwidget_shortkeys_table.width()*.5)-80, 20+self.global_subtitlesvideo_panel_tabwidget_shortkeys_table.height()+5, 160, 30)


def show_global_subtitlesvideo_panel(self):
    self.generate_effect(self.global_subtitlesvideo_panel_widget_animation, 'geometry', 700, [self.global_subtitlesvideo_panel_widget.x(), self.global_subtitlesvideo_panel_widget.y(), self.global_subtitlesvideo_panel_widget.width(), self.global_subtitlesvideo_panel_widget.height()], [0, self.global_subtitlesvideo_panel_widget.y(), self.global_subtitlesvideo_panel_widget.width(), self.global_subtitlesvideo_panel_widget.height()])


def global_subtitlesvideo_panel_tabwidget_shortkeys_table_update(self):
    self.global_subtitlesvideo_panel_tabwidget_shortkeys_table.clear()
    self.global_subtitlesvideo_panel_tabwidget_shortkeys_table.setRowCount(len(shortcuts_dict))
    inverted_shortcuts_dict = {value: key for key, value in shortcuts_dict.items()}
    i = 0
    for item in shortcuts_dict:
        item_name = QTableWidgetItem(shortcuts_dict[item])
        self.global_subtitlesvideo_panel_tabwidget_shortkeys_table.setItem(i, 0, item_name)
        item_name = QTableWidgetItem(self.settings['shortcuts'].get(inverted_shortcuts_dict[shortcuts_dict[item]], [''])[0])
        self.global_subtitlesvideo_panel_tabwidget_shortkeys_table.setItem(i, 1, item_name)
        i += 1


def global_subtitlesvideo_panel_tabwidget_shortkeys_set_button_clicked(self):
    self.global_subtitlesvideo_panel_tabwidget_shortkeys_set_button.setVisible(not self.global_subtitlesvideo_panel_tabwidget_shortkeys_set_button.isVisible())
    self.global_subtitlesvideo_panel_tabwidget_shortkeys_editbox.setVisible(not self.global_subtitlesvideo_panel_tabwidget_shortkeys_set_button.isVisible())
    self.global_subtitlesvideo_panel_tabwidget_shortkeys_editbox_confirm.setVisible(not self.global_subtitlesvideo_panel_tabwidget_shortkeys_set_button.isVisible())
    self.global_subtitlesvideo_panel_tabwidget_shortkeys_editbox_cancel.setVisible(not self.global_subtitlesvideo_panel_tabwidget_shortkeys_set_button.isVisible())
    self.global_subtitlesvideo_panel_tabwidget_shortkeys_table.setVisible(self.global_subtitlesvideo_panel_tabwidget_shortkeys_set_button.isVisible())


def global_subtitlesvideo_panel_tabwidget_shortkeys_editbox_cancel_clicked(self):
    # self.global_subtitlesvideo_panel_tabwidget_shortkeys_set_button.setVisible(True)
    global_subtitlesvideo_panel_tabwidget_shortkeys_set_button_clicked(self)


def global_subtitlesvideo_panel_tabwidget_shortkeys_editbox_confirm_clicked(self):
    inverted_shortcuts_dict = {value: key for key, value in shortcuts_dict.items()}
    self.settings['shortcuts'][inverted_shortcuts_dict[self.global_subtitlesvideo_panel_tabwidget_shortkeys_table.item(self.global_subtitlesvideo_panel_tabwidget_shortkeys_table.currentRow(), 0).text()]] = [self.global_subtitlesvideo_panel_tabwidget_shortkeys_editbox.text()]
    self.shortcuts.load(self, self.settings['shortcuts'])
    global_subtitlesvideo_panel_tabwidget_shortkeys_table_update(self)
    global_subtitlesvideo_panel_tabwidget_shortkeys_editbox_cancel_clicked(self)


def global_subtitlesvideo_import_button_clicked(self):
    # if self.global_subtitlesvideo_import_button.isChecked():
    #     self.global_subtitlesvideo_export_button.setGeometry(20, 200, self.global_subtitlesvideo_panel_left.width()-40, 30)
    # else:
    #     self.global_subtitlesvideo_export_button.setGeometry(20, 120, self.global_subtitlesvideo_panel_left.width()-40, 30)
    # self.global_subtitlesvideo_import_panel.setVisible(self.global_subtitlesvideo_import_button.isChecked())

    supported_import_files = self.tr('Text files') + ' ({})'.format(" ".join(["*.{}".format(fo) for fo in list_of_supported_import_extensions]))
    file_to_open = QFileDialog.getOpenFileName(self, self.tr('Select the file to import'), os.path.expanduser("~"), supported_import_files, options=QFileDialog.DontUseNativeDialog)[0]
    if file_to_open:
        self.subtitles_list += file_io.import_file(filename=file_to_open)[0]
        self.subtitles_list.sort()


def global_subtitlesvideo_video_burn_convert_clicked(self):
    suggested_path = os.path.dirname(self.video_metadata['filepath'])
    ext = os.path.basename(self.video_metadata['filepath']).rsplit('.', 1)[1]
    save_formats = self.tr('Video file') + ' (.' + ext + ')'
    suggested_name = os.path.basename(self.video_metadata['filepath']).rsplit('.', 1)[0] + '_subtitled.' + ext

    generated_video_filepath = QFileDialog.getSaveFileName(self, self.tr('Select the subtitle file'), os.path.join(suggested_path, suggested_name), save_formats, options=QFileDialog.DontUseNativeDialog)[0]

    if generated_video_filepath:
        file_io.save_file(os.path.join(path_tmp, 'subtitle.srt'), self.subtitles_list, format='SRT', language='en')

        vf_string = 'subtitles=filename=' + os.path.join(path_tmp, 'subtitle.srt').replace('\\', '\\\\\\\\').replace(':', '\\\:') + ":force_style='"
        vf_string += 'FontName=' + self.global_subtitlesvideo_video_burn_fontname.currentText() + ','
        vf_string += 'FontSize=' + str(self.global_subtitlesvideo_video_burn_fontsize.value()) + ','
        vf_string += 'Shadow=' + str(self.global_subtitlesvideo_video_burn_shadowdistance.value()) + ','
        vf_string += 'Outline=' + str(self.global_subtitlesvideo_video_burn_outline.value()) + ','
        vf_string += 'MarginV=' + str(self.global_subtitlesvideo_video_burn_marvinv.value()) + ','
        vf_string += 'MarginL=' + str(self.global_subtitlesvideo_video_burn_marvinl.value()) + ','
        vf_string += 'MarginR=' + str(self.global_subtitlesvideo_video_burn_marvinr.value()) + ','
        pcolor = self.global_subtitlesvideo_video_burn_pcolor_selected_color.replace('#', '&H')
        pcolor = pcolor[:2] + pcolor[-2:] + pcolor[-4:-2] + pcolor[-6:-4]
        vf_string += 'PrimaryColour=' + pcolor + "'"

        commands = [
            FFMPEG_EXECUTABLE,
            '-i', self.video_metadata['filepath'],
            '-y',
            '-vf',
            vf_string,
            generated_video_filepath
            ]

        self.thread_generated_burned_video.commands = commands
        self.thread_generated_burned_video.start()
        self.global_subtitlesvideo_video_burn_convert.setEnabled(False)


def global_subtitlesvideo_video_burn_pcolor_clicked(self):
    color = QColorDialog().getColor()
    if color.isValid():
        self.global_subtitlesvideo_video_burn_pcolor_selected_color = color.name()
    self.global_subtitlesvideo_video_burn_pcolor.setStyleSheet('background-color:' + self.global_subtitlesvideo_video_burn_pcolor_selected_color)


def global_subtitlesvideo_export_button_clicked(self):
    suggested_path = os.path.dirname(self.video_metadata['filepath'])
    suggested_name = os.path.basename(self.video_metadata['filepath']).rsplit('.', 1)[0] + '.txt'
    save_formats = self.tr('TXT file') + ' (.txt)'

    filedialog = QFileDialog.getSaveFileName(self, self.tr('Export to file'), os.path.join(suggested_path, suggested_name), save_formats, options=QFileDialog.DontUseNativeDialog)

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


def global_subtitlesvideo_autosync_button_clicked(self):
    run_command = False

    if bool(self.subtitles_list):
        are_you_sure_message = QMessageBox(self)
        are_you_sure_message.setWindowTitle(self.tr('Are you sure?'))
        are_you_sure_message.setText(self.tr('This will overwrite your actual subtitle set. New timings will be applied. Are you sure you want to replace your actual subtitles?'))
        are_you_sure_message.addButton(self.tr('Yes'), QMessageBox.AcceptRole)
        are_you_sure_message.addButton(self.tr('No'), QMessageBox.RejectRole)
        ret = are_you_sure_message.exec_()

        if ret == QMessageBox.AcceptRole:
            run_command = True
    else:
        run_command = True

    if run_command:
        from ffsubsync import ffsubsync

        file_io.save_file(os.path.join(path_tmp, 'subtitle_original.srt'), self.subtitles_list, 'SRT')
        sub = os.path.join(path_tmp, 'subtitle_final.srt')

        unparsed_args = [self.video_metadata['filepath'], "-i", os.path.join(path_tmp, 'subtitle_original.srt'), "-o", sub]

        parser = ffsubsync.make_parser()
        args = parser.parse_args(unparsed_args)

        ffsubsync.run(args)

        if os.path.isfile(sub):
            self.subtitles_list = file_io.process_subtitles_file(sub)[0]
            self.unsaved = True
            self.selected_subtitle = False
            self.subtitleslist.update_subtitles_list_qlistwidget(self)
            self.timeline.update(self)
            self.properties.update_properties_widget(self)

def global_subtitlesvideo_autosub_button_clicked(self):
    run_command = False

    if bool(self.subtitles_list):
        are_you_sure_message = QMessageBox(self)
        are_you_sure_message.setWindowTitle(self.tr('Are you sure?'))
        are_you_sure_message.setText(self.tr('This will overwrite your actual subtitle set. New timings will be applied. Are you sure you want to replace your actual subtitles?'))
        are_you_sure_message.addButton(self.tr('Yes'), QMessageBox.AcceptRole)
        are_you_sure_message.addButton(self.tr('No'), QMessageBox.RejectRole)
        ret = are_you_sure_message.exec_()

        if ret == QMessageBox.AcceptRole:
            run_command = True
    else:
        run_command = True

    if run_command:
        def read_json_subtitles(filename='', transcribed=False):
            final_subtitles = []
            if filename:
                with open(filename, encoding='utf-8') as json_file:
                    data = json.loads(json_file.read())
                    if transcribed:
                        for fragment in data:
                            subtitle = []
                            subtitle.append(float(fragment['start']))
                            subtitle.append(float(fragment['end']) - subtitle[0])
                            subtitle.append(str(fragment['content']))
                            final_subtitles.append(subtitle)
                    else:
                        for fragment in data['fragments']:
                            subtitle = []
                            subtitle.append(float(fragment['begin']))
                            subtitle.append(float(fragment['end']) - float(fragment['begin']))
                            # subtitle.append(codecs.decode(fragment['lines'][0], 'unicode-escape'))
                            # print(fragment['lines'][0])
                            subtitle.append(str(fragment['lines'][0]))
                            final_subtitles.append(subtitle)

            return final_subtitles

        import autosub
        import json

        language = LANGUAGE_DICT_LIST[self.global_subtitlesvideo_autosync_lang_combobox.currentText()]
        #
        # command = [
        #     FFMPEG_EXECUTABLE,
        #     '-y',
        #     '-f', 'f32le',
        #     '-ac', '1',
        #     '-ar', '48000',
        #     '-i', '-',
        #     '-vn',
        #     os.path.join(path_tmp, 'subtitle.opus')]
        #
        # audio_out = subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.PIPE, startupinfo=STARTUPINFO)
        # audio_out.stdin.write(self.video_metadata['audio'].tobytes())
        # audio_out.stdin.close()
        # audio_out.wait()

        # autosub.generate_subtitles(os.path.join(path_tmp, 'subtitle.opus'), output=os.path.join(path_tmp, 'subtitle.json'), src_language=language, dst_language=language, subtitle_file_format='json')
        test = autosub.generate_subtitles(self.video_metadata['filepath'], output=os.path.join(path_tmp, 'subtitle.json'), src_language=language, dst_language=language, subtitle_file_format='json')

        if os.path.isfile(os.path.join(path_tmp, 'subtitle.json')):
            final_subtitles = read_json_subtitles(filename=os.path.join(path_tmp, 'subtitle.json'), transcribed=True)
            if final_subtitles:
                self.subtitles_list = final_subtitles

        self.unsaved = True
        self.selected_subtitle = False
        self.subtitleslist.update_subtitles_list_qlistwidget(self)
        self.timeline.update(self)
        self.properties.update_properties_widget(self)
