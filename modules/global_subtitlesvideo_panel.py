#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import subprocess

from PyQt5.QtWidgets import QLabel, QComboBox, QPushButton, QFileDialog, QSpinBox, QColorDialog
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, QThread, pyqtSignal
from PyQt5.QtGui import QFontDatabase

from modules.paths import LIST_OF_SUPPORTED_SUBTITLE_EXTENSIONS, LIST_OF_SUPPORTED_IMPORT_EXTENSIONS, STARTUPINFO, FFMPEG_EXECUTABLE, path_tmp
from modules import file_io

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
                #for output in p.stdout.read().decode().split('\n'):
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

    self.global_subtitlesvideo_video_burn_label = QLabel('EXPORT BURNED VIDEO', parent=self.global_subtitlesvideo_panel_widget)
    self.global_subtitlesvideo_video_burn_label.setStyleSheet('QLabel { font-size:14px; font-weight:bold; }')

    self.global_subtitlesvideo_video_burn_fontname_label = QLabel('FONT NAME', parent=self.global_subtitlesvideo_panel_widget)

    fonts = QFontDatabase().families()
    self.global_subtitlesvideo_video_burn_fontname = QComboBox(parent=self.global_subtitlesvideo_panel_widget)
    self.global_subtitlesvideo_video_burn_fontname.addItems(fonts)
    # self.global_subtitlesvideo_video_burn_fontname.activated.connect(lambda: global_subtitlesvideo_save_as_combobox_activated(self))

    self.global_subtitlesvideo_video_burn_fontsize_label = QLabel('FONT SIZE', parent=self.global_subtitlesvideo_panel_widget)

    self.global_subtitlesvideo_video_burn_fontsize = QSpinBox(parent=self.global_subtitlesvideo_panel_widget)
    self.global_subtitlesvideo_video_burn_fontsize.setMinimum(8)
    self.global_subtitlesvideo_video_burn_fontsize.setMaximum(200)
    self.global_subtitlesvideo_video_burn_fontsize.setValue(20)

    self.global_subtitlesvideo_video_burn_shadowdistance_label = QLabel('SHADOW DISTANCE', parent=self.global_subtitlesvideo_panel_widget)

    self.global_subtitlesvideo_video_burn_shadowdistance = QSpinBox(parent=self.global_subtitlesvideo_panel_widget)
    self.global_subtitlesvideo_video_burn_shadowdistance.setMinimum(0)
    self.global_subtitlesvideo_video_burn_shadowdistance.setMaximum(20)
    self.global_subtitlesvideo_video_burn_shadowdistance.setValue(1)

    self.global_subtitlesvideo_video_burn_outline_label = QLabel('OUTLINE', parent=self.global_subtitlesvideo_panel_widget)

    self.global_subtitlesvideo_video_burn_outline = QSpinBox(parent=self.global_subtitlesvideo_panel_widget)
    self.global_subtitlesvideo_video_burn_outline.setMinimum(0)
    self.global_subtitlesvideo_video_burn_outline.setMaximum(20)
    self.global_subtitlesvideo_video_burn_outline.setValue(2)

    self.global_subtitlesvideo_video_burn_marvinv_label = QLabel('MARGIN FROM BOTTOM', parent=self.global_subtitlesvideo_panel_widget)

    self.global_subtitlesvideo_video_burn_marvinv = QSpinBox(parent=self.global_subtitlesvideo_panel_widget)
    self.global_subtitlesvideo_video_burn_marvinv.setMinimum(0)
    self.global_subtitlesvideo_video_burn_marvinv.setMaximum(500)
    self.global_subtitlesvideo_video_burn_marvinv.setValue(20)

    self.global_subtitlesvideo_video_burn_marvinl_label = QLabel('MARGIN FROM LEFT', parent=self.global_subtitlesvideo_panel_widget)

    self.global_subtitlesvideo_video_burn_marvinl = QSpinBox(parent=self.global_subtitlesvideo_panel_widget)
    self.global_subtitlesvideo_video_burn_marvinl.setMinimum(0)
    self.global_subtitlesvideo_video_burn_marvinl.setMaximum(500)
    self.global_subtitlesvideo_video_burn_marvinl.setValue(50)

    self.global_subtitlesvideo_video_burn_marvinr_label = QLabel('MARGIN FROM RIGHT', parent=self.global_subtitlesvideo_panel_widget)

    self.global_subtitlesvideo_video_burn_marvinr = QSpinBox(parent=self.global_subtitlesvideo_panel_widget)
    self.global_subtitlesvideo_video_burn_marvinr.setMinimum(0)
    self.global_subtitlesvideo_video_burn_marvinr.setMaximum(500)
    self.global_subtitlesvideo_video_burn_marvinr.setValue(50)

    self.global_subtitlesvideo_video_burn_pcolor_selected_color = ''

    self.global_subtitlesvideo_video_burn_pcolor_label = QLabel('FONT COLOR', parent=self.global_subtitlesvideo_panel_widget)

    self.global_subtitlesvideo_video_burn_pcolor = QPushButton(parent=self.global_subtitlesvideo_panel_widget)
    self.global_subtitlesvideo_video_burn_pcolor.clicked.connect(lambda: global_subtitlesvideo_video_burn_pcolor_clicked(self))
    self.global_subtitlesvideo_video_burn_pcolor.setStyleSheet('background-color:' + self.global_subtitlesvideo_video_burn_pcolor_selected_color)

    self.global_subtitlesvideo_video_burn_convert = QPushButton('GENERATE VIDEO', parent=self.global_subtitlesvideo_panel_widget)
    self.global_subtitlesvideo_video_burn_convert.setObjectName('button_dark')
    self.global_subtitlesvideo_video_burn_convert.clicked.connect(lambda: global_subtitlesvideo_video_burn_convert_clicked(self))

    def thread_generated_burned_video_ended(response):
        if '|' in response:
            self.global_subtitlesvideo_video_burn_convert.setText('GENERATING... (' + str(int((float(response.split('|')[0]) / float(response.split('|')[1])) * 100)) + '%)')
        elif 'end' in response:
            self.global_subtitlesvideo_video_burn_convert.setText('GENERATE VIDEO')
            self.global_subtitlesvideo_video_burn_convert.setEnabled(True)

    self.thread_generated_burned_video = thread_generated_burned_video(self)
    self.thread_generated_burned_video.response.connect(thread_generated_burned_video_ended)

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

    self.global_subtitlesvideo_video_burn_label.setGeometry(self.global_subtitlesvideo_panel_right.x()+20, 20, 200, 20)
    self.global_subtitlesvideo_video_burn_fontname_label.setGeometry(self.global_subtitlesvideo_panel_right.x()+20, 50, 200, 20)
    self.global_subtitlesvideo_video_burn_fontname.setGeometry(self.global_subtitlesvideo_panel_right.x()+20, 70, 300, 30)

    self.global_subtitlesvideo_video_burn_fontsize_label.setGeometry(self.global_subtitlesvideo_panel_right.x()+20, 110, 150, 20)
    self.global_subtitlesvideo_video_burn_fontsize.setGeometry(self.global_subtitlesvideo_panel_right.x()+20, 130, 150, 30)
    self.global_subtitlesvideo_video_burn_shadowdistance_label.setGeometry(self.global_subtitlesvideo_panel_right.x()+20+150+10, 110, 150, 20)
    self.global_subtitlesvideo_video_burn_shadowdistance.setGeometry(self.global_subtitlesvideo_panel_right.x()+20+150+10, 130, 150, 30)
    self.global_subtitlesvideo_video_burn_outline_label.setGeometry(self.global_subtitlesvideo_panel_right.x()+20+150+150+20, 110, 150, 20)
    self.global_subtitlesvideo_video_burn_outline.setGeometry(self.global_subtitlesvideo_panel_right.x()+20+150+150+20, 130, 150, 30)
    self.global_subtitlesvideo_video_burn_marvinv_label.setGeometry(self.global_subtitlesvideo_panel_right.x()+20, 170, 150, 20)
    self.global_subtitlesvideo_video_burn_marvinv.setGeometry(self.global_subtitlesvideo_panel_right.x()+20, 190, 150, 30)
    self.global_subtitlesvideo_video_burn_marvinl_label.setGeometry(self.global_subtitlesvideo_panel_right.x()+20+150+10, 170, 150, 20)
    self.global_subtitlesvideo_video_burn_marvinl.setGeometry(self.global_subtitlesvideo_panel_right.x()+20+150+10, 190, 150, 30)
    self.global_subtitlesvideo_video_burn_marvinr_label.setGeometry(self.global_subtitlesvideo_panel_right.x()+20+150+150+20, 170, 150, 20)
    self.global_subtitlesvideo_video_burn_marvinr.setGeometry(self.global_subtitlesvideo_panel_right.x()+20+150+150+20, 190, 150, 30)
    self.global_subtitlesvideo_video_burn_pcolor_label.setGeometry(self.global_subtitlesvideo_panel_right.x()+20+150+150+20+150+10, 170, 150, 20)
    self.global_subtitlesvideo_video_burn_pcolor.setGeometry(self.global_subtitlesvideo_panel_right.x()+20+150+150+20+150+10, 190, 150, 30)
    self.global_subtitlesvideo_video_burn_convert.setGeometry(self.global_subtitlesvideo_panel_right.x()+20, 240, 200, 40)


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


def global_subtitlesvideo_video_burn_convert_clicked(self):
    suggested_path = os.path.dirname(self.video_metadata['filepath'])
    ext = os.path.basename(self.video_metadata['filepath']).rsplit('.', 1)[1]
    save_formats = 'Video file (.' + ext + ')'
    suggested_name = os.path.basename(self.video_metadata['filepath']).rsplit('.', 1)[0] + '_subtitled.' + ext

    generated_video_filepath = QFileDialog.getSaveFileName(self, "Select the subtitle file", os.path.join(suggested_path, suggested_name), save_formats, options=QFileDialog.DontUseNativeDialog)[0]

    if generated_video_filepath:
        file_io.save_file(os.path.join(path_tmp, 'subtitle.srt'), self.subtitles_list, format='SRT', language='en')

        vf_string = 'subtitles=filename=' + os.path.join(path_tmp, 'subtitle.srt') + ":force_style='"
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
    print(self.global_subtitlesvideo_video_burn_pcolor_selected_color)


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
