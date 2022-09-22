"""Subtitles Video panel

"""
import os
import subprocess

from PySide6.QtWidgets import QLabel, QComboBox, QPushButton, QFileDialog, QSpinBox, QColorDialog, QWidget, QTableWidgetItem, QVBoxLayout, QStackedWidget
from PySide6.QtCore import QMargins, QSize, QThread, Signal, Qt
from PySide6.QtGui import QBrush, QColor, QFont, QFontDatabase, QPainter, QPen
from subtitld.interface import global_panel

from subtitld.modules.paths import LIST_OF_SUPPORTED_EXPORT_EXTENSIONS, STARTUPINFO, FFMPEG_EXECUTABLE, path_tmp
from subtitld.modules.shortcuts import shortcuts_dict
from subtitld.modules import file_io
from subtitld.modules import utils


class ThreadGeneratedBurnedVideo(QThread):
    """Thread to generate burned video"""
    response = Signal(str)
    commands = []

    def run(self):
        """Run function of thread to generate burned video"""
        if self.commands:
            proc = subprocess.Popen(self.commands, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, startupinfo=STARTUPINFO, bufsize=4096)
            number_of_steps = 0.001
            current_step = 0.0
            while proc.poll() is None:
                # for output in proc.stdout.read().decode().split('\n'):
                output = proc.stdout.readline()
                if 'Duration: ' in output:
                    duration = int(utils.convert_ffmpeg_timecode_to_seconds(output.split('Duration: ', 1)[1].split(',', 1)[0]))
                    if duration > number_of_steps:
                        number_of_steps = duration
                if output[:6] == 'frame=':
                    current_step = int(utils.convert_ffmpeg_timecode_to_seconds(output.split('time=', 1)[1].split(' ', 1)[0]))

                self.response.emit(str(current_step) + '|' + str(number_of_steps))
            self.response.emit('end')


def load_menu(self):
    """Function to load subtitles panel widgets"""
    self.global_panel_export_menu_button = QPushButton('Export')
    self.global_panel_export_menu_button.setCheckable(True)
    self.global_panel_export_menu_button.setProperty('class', 'global_panel_menu')
    self.global_panel_export_menu_button.clicked.connect(lambda: global_panel_menu_changed(self))
    self.global_panel_menu.layout().addWidget(self.global_panel_export_menu_button)


def global_panel_menu_changed(self):
    self.global_panel_export_menu_button.setEnabled(False)
    global_panel.global_panel_menu_changed(self, self.global_panel_export_menu_button, self.global_panel_export_content)


def load_widgets(self):
    """Function to load subtitles panel widgets"""

    self.global_panel_export_content = QWidget()
    self.global_panel_export_content.setLayout(QVBoxLayout())
    self.global_panel_export_content.layout().setContentsMargins(0, 0, 0, 0)

    self.global_panel_export_types_combobox = QComboBox()
    self.global_panel_export_types_combobox.addItems(
        [
            'txt',
            'mp4'
        ]
    )
    self.global_panel_export_types_combobox.activated.connect(lambda: global_panel_export_types_combobox_activated(self))
    self.global_panel_export_content.layout().addWidget(self.global_panel_export_types_combobox, 0, Qt.AlignLeft)

    self.global_panel_export_content_stackedwidgets = QStackedWidget()

    self.global_panel_export_content_txt_panel = QWidget()
    self.global_panel_export_content_txt_panel.setLayout(QVBoxLayout())

    self.global_panel_export_content_txt_panel_export_button = QPushButton(self.tr('Export').upper())
    self.global_panel_export_content_txt_panel_export_button.setProperty('class', 'button')
    self.global_panel_export_content_txt_panel_export_button.clicked.connect(lambda: global_subtitlesvideo_export_button_clicked(self))
    self.global_panel_export_content_txt_panel.layout().addWidget(self.global_panel_export_content_txt_panel_export_button)

    self.global_panel_export_content_stackedwidgets.addWidget(self.global_panel_export_content_txt_panel)

    self.global_panel_export_content_mp4_panel = QWidget()
    self.global_panel_export_content_mp4_panel.setLayout(QVBoxLayout())

    self.global_subtitlesvideo_export_button = QPushButton(self.tr('Export').upper())
    self.global_subtitlesvideo_export_button.setProperty('class', 'button')
    self.global_subtitlesvideo_export_button.clicked.connect(lambda: global_subtitlesvideo_export_button_clicked(self))
    self.global_panel_export_content_mp4_panel.layout().addWidget(self.global_subtitlesvideo_export_button)

    self.global_subtitlesvideo_video_burn_label = QLabel(self.tr('Export burned video').upper())
    self.global_subtitlesvideo_video_burn_label.setStyleSheet('QLabel { font-size:14px; font-weight:bold; }')
    self.global_panel_export_content_mp4_panel.layout().addWidget(self.global_subtitlesvideo_video_burn_label)

    self.global_subtitlesvideo_video_burn_fontname_label = QLabel(self.tr('Font name').upper())
    self.global_panel_export_content_mp4_panel.layout().addWidget(self.global_subtitlesvideo_video_burn_fontname_label)

    fonts = QFontDatabase().families()
    self.global_subtitlesvideo_video_burn_fontname = QComboBox(parent=self.global_panel_export_content)
    self.global_subtitlesvideo_video_burn_fontname.setProperty('class', 'button')
    self.global_subtitlesvideo_video_burn_fontname.addItems(fonts)
    self.global_panel_export_content_mp4_panel.layout().addWidget(self.global_subtitlesvideo_video_burn_fontname)
    # self.global_subtitlesvideo_video_burn_fontname.activated.connect(lambda: global_subtitlesvideo_save_as_combobox_activated(self))

    self.global_subtitlesvideo_video_burn_fontsize_label = QLabel(self.tr('Font size').upper())
    self.global_panel_export_content_mp4_panel.layout().addWidget(self.global_subtitlesvideo_video_burn_fontsize_label)

    self.global_subtitlesvideo_video_burn_fontsize = QSpinBox(parent=self.global_panel_export_content)
    self.global_subtitlesvideo_video_burn_fontsize.setMinimum(8)
    self.global_subtitlesvideo_video_burn_fontsize.setMaximum(200)
    self.global_subtitlesvideo_video_burn_fontsize.setValue(20)
    self.global_panel_export_content_mp4_panel.layout().addWidget(self.global_subtitlesvideo_video_burn_fontsize)

    self.global_subtitlesvideo_video_burn_shadowdistance_label = QLabel(self.tr('Shadow distance').upper())
    self.global_panel_export_content_mp4_panel.layout().addWidget(self.global_subtitlesvideo_video_burn_shadowdistance_label)

    self.global_subtitlesvideo_video_burn_shadowdistance = QSpinBox(parent=self.global_panel_export_content)
    self.global_subtitlesvideo_video_burn_shadowdistance.setMinimum(0)
    self.global_subtitlesvideo_video_burn_shadowdistance.setMaximum(20)
    self.global_subtitlesvideo_video_burn_shadowdistance.setValue(1)
    self.global_panel_export_content_mp4_panel.layout().addWidget(self.global_subtitlesvideo_video_burn_shadowdistance)

    self.global_subtitlesvideo_video_burn_outline_label = QLabel(self.tr('Outline').upper())
    self.global_panel_export_content_mp4_panel.layout().addWidget(self.global_subtitlesvideo_video_burn_outline_label)

    self.global_subtitlesvideo_video_burn_outline = QSpinBox(parent=self.global_panel_export_content)
    self.global_subtitlesvideo_video_burn_outline.setMinimum(0)
    self.global_subtitlesvideo_video_burn_outline.setMaximum(20)
    self.global_subtitlesvideo_video_burn_outline.setValue(2)
    self.global_panel_export_content_mp4_panel.layout().addWidget(self.global_subtitlesvideo_video_burn_outline)

    self.global_subtitlesvideo_video_burn_marvinv_label = QLabel(self.tr('Margin from bottom').upper())
    self.global_panel_export_content_mp4_panel.layout().addWidget(self.global_subtitlesvideo_video_burn_marvinv_label)

    self.global_subtitlesvideo_video_burn_marvinv = QSpinBox(parent=self.global_panel_export_content)
    self.global_subtitlesvideo_video_burn_marvinv.setMinimum(0)
    self.global_subtitlesvideo_video_burn_marvinv.setMaximum(500)
    self.global_subtitlesvideo_video_burn_marvinv.setValue(20)
    self.global_panel_export_content_mp4_panel.layout().addWidget(self.global_subtitlesvideo_video_burn_marvinv)

    self.global_subtitlesvideo_video_burn_marvinl_label = QLabel(self.tr('Margin from left').upper())
    self.global_panel_export_content_mp4_panel.layout().addWidget(self.global_subtitlesvideo_video_burn_marvinl_label)

    self.global_subtitlesvideo_video_burn_marvinl = QSpinBox(parent=self.global_panel_export_content)
    self.global_subtitlesvideo_video_burn_marvinl.setMinimum(0)
    self.global_subtitlesvideo_video_burn_marvinl.setMaximum(500)
    self.global_subtitlesvideo_video_burn_marvinl.setValue(50)
    self.global_panel_export_content_mp4_panel.layout().addWidget(self.global_subtitlesvideo_video_burn_marvinl)

    self.global_subtitlesvideo_video_burn_marvinr_label = QLabel(self.tr('Margin from right').upper())
    self.global_panel_export_content_mp4_panel.layout().addWidget(self.global_subtitlesvideo_video_burn_marvinr_label)

    self.global_subtitlesvideo_video_burn_marvinr = QSpinBox(parent=self.global_panel_export_content)
    self.global_subtitlesvideo_video_burn_marvinr.setMinimum(0)
    self.global_subtitlesvideo_video_burn_marvinr.setMaximum(500)
    self.global_subtitlesvideo_video_burn_marvinr.setValue(50)
    self.global_panel_export_content_mp4_panel.layout().addWidget(self.global_subtitlesvideo_video_burn_marvinr)

    self.global_subtitlesvideo_video_burn_pcolor_selected_color = '#ffffff'

    self.global_subtitlesvideo_video_burn_pcolor_label = QLabel(self.tr('Font color').upper())
    self.global_panel_export_content_mp4_panel.layout().addWidget(self.global_subtitlesvideo_video_burn_pcolor_label)

    self.global_subtitlesvideo_video_burn_pcolor = QPushButton(parent=self.global_panel_export_content)
    self.global_subtitlesvideo_video_burn_pcolor.clicked.connect(lambda: global_subtitlesvideo_video_burn_pcolor_clicked(self))
    self.global_subtitlesvideo_video_burn_pcolor.setStyleSheet('background-color:' + self.global_subtitlesvideo_video_burn_pcolor_selected_color)
    self.global_panel_export_content_mp4_panel.layout().addWidget(self.global_subtitlesvideo_video_burn_pcolor)

    self.global_subtitlesvideo_video_burn_convert = QPushButton(self.tr('Generate video').upper())
    self.global_subtitlesvideo_video_burn_convert.setProperty('class', 'button_dark')
    self.global_subtitlesvideo_video_burn_convert.clicked.connect(lambda: global_subtitlesvideo_video_burn_convert_clicked(self))
    self.global_panel_export_content_mp4_panel.layout().addWidget(self.global_subtitlesvideo_video_burn_convert)

    self.global_subtitlesvideo_video_generate_transparent_video_button = QPushButton(self.tr('Generate transparent video').upper())
    self.global_subtitlesvideo_video_generate_transparent_video_button.setProperty('class', 'button_dark')
    self.global_subtitlesvideo_video_generate_transparent_video_button.clicked.connect(lambda: global_subtitlesvideo_video_generate_transparent_video_button_clicked(self))
    self.global_panel_export_content_mp4_panel.layout().addWidget(self.global_subtitlesvideo_video_generate_transparent_video_button)
    # self.global_subtitlesvideo_video_generate_transparent_video_button.setVisible(False)

    def thread_generated_burned_video_ended(response):
        if '|' in response:
            self.global_subtitlesvideo_video_burn_convert.setText('GENERATING... (' + str(int((float(response.split('|')[0]) / float(response.split('|')[1])) * 100)) + '%)')
        elif 'end' in response:
            self.global_subtitlesvideo_video_burn_convert.setText(self.tr('Generate video').upper())
            self.global_subtitlesvideo_video_burn_convert.setEnabled(True)

    self.thread_generated_burned_video = ThreadGeneratedBurnedVideo(self)
    self.thread_generated_burned_video.response.connect(thread_generated_burned_video_ended)

    self.global_panel_export_content_stackedwidgets.addWidget(self.global_panel_export_content_mp4_panel)

    self.global_panel_export_content.layout().addWidget(self.global_panel_export_content_stackedwidgets)

    self.global_panel_content_stacked_widgets.addWidget(self.global_panel_export_content)


def global_panel_tabwidget_shortkeys_table_update(self):
    """Function to update subtitlesvideo panel shorkeys table"""
    self.global_panel_tabwidget_shortkeys_table.clear()
    self.global_panel_tabwidget_shortkeys_table.setRowCount(len(shortcuts_dict))
    inverted_shortcuts_dict = {value: key for key, value in shortcuts_dict.items()}
    i = 0
    for item in shortcuts_dict:
        item_name = QTableWidgetItem(shortcuts_dict[item])
        self.global_panel_tabwidget_shortkeys_table.setItem(i, 0, item_name)
        item_name = QTableWidgetItem(self.settings['shortcuts'].get(inverted_shortcuts_dict[shortcuts_dict[item]], [''])[0])
        self.global_panel_tabwidget_shortkeys_table.setItem(i, 1, item_name)
        i += 1


def global_subtitlesvideo_video_burn_convert_clicked(self):
    """Function to generate buned video"""
    suggested_path = os.path.dirname(self.video_metadata['filepath'])
    extformat = os.path.basename(self.video_metadata['filepath']).rsplit('.', 1)[1]
    save_formats = self.tr('Video file') + ' (.' + extformat + ')'
    suggested_name = os.path.basename(self.video_metadata['filepath']).rsplit('.', 1)[0] + '_subtitled.' + extformat

    generated_video_filepath = QFileDialog.getSaveFileName(parent=self, caption=self.tr('Select the subtitle file'), dir=os.path.join(suggested_path, suggested_name), filter=save_formats)[0]

    if generated_video_filepath:
        file_io.save_file(os.path.join(path_tmp, 'subtitle.srt'), self.subtitles_list, subtitle_format='SRT', language='en')

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
            '-crf', '15',
            generated_video_filepath
        ]

        self.thread_generated_burned_video.commands = commands
        self.thread_generated_burned_video.start()
        self.global_subtitlesvideo_video_burn_convert.setEnabled(False)


def global_subtitlesvideo_video_burn_pcolor_clicked(self):
    """Function to change color"""
    color = QColorDialog().getColor(options=QColorDialog.DontUseNativeDialog)
    if color.isValid():
        self.global_subtitlesvideo_video_burn_pcolor_selected_color = color.name()
    self.global_subtitlesvideo_video_burn_pcolor.setStyleSheet('background-color:' + self.global_subtitlesvideo_video_burn_pcolor_selected_color)


def global_subtitlesvideo_video_generate_transparent_video_button_clicked(self):
    suggested_path = os.path.dirname(self.video_metadata['filepath'])
    extformat = 'mov'  # os.path.basename(self.video_metadata['filepath']).rsplit('.', 1)[1]
    save_formats = self.tr('Video file') + ' (.' + extformat + ')'
    suggested_name = os.path.basename(self.video_metadata['filepath']).rsplit('.', 1)[0] + '_subtitled.' + extformat

    generated_video_filepath = QFileDialog.getSaveFileName(parent=self, caption=self.tr('Select the subtitle file'), dir=os.path.join(suggested_path, suggested_name), filter=save_formats)[0]

    # print(path_tmp)

    if generated_video_filepath:
        class layerWidget(QWidget):
            subtitle_text = ''
            font = 'Ubuntu'
            fontsize = 18

            def paintEvent(canvas, paintEvent):
                painter = QPainter(canvas)
                painter.setRenderHint(QPainter.Antialiasing)

                if canvas.subtitle_text:
                    font = QFont(canvas.font)
                    font.setPointSize(canvas.fontsize)
                    painter.setFont(font)

                    text_rect = painter.boundingRect(canvas.width() * .08, canvas.height() * .08, canvas.width() * .84, canvas.height() * .84, Qt.AlignBottom | Qt.AlignHCenter | Qt.TextWordWrap, canvas.subtitle_text)

                    painter.setPen(Qt.NoPen)
                    painter.setBrush(QBrush(QColor('#cc000000')))
                    painter.drawRoundedRect(text_rect.marginsAdded(QMargins(10, 10, 10, 10)), 5, 5)

                    painter.setPen(QPen(QColor('#fff')))
                    painter.drawText(text_rect.adjusted(0, 2, 0, 2), Qt.AlignCenter | Qt.TextWordWrap, canvas.subtitle_text)

                painter.end()

        layer = layerWidget(self)
        layer.setVisible(False)
        layer.setStyleSheet('background: transparent;')
        layer.resize(QSize(self.video_metadata.get('width', 1920), self.video_metadata.get('height', 1920)))
        layer.font = self.global_subtitlesvideo_video_burn_fontname.currentText()
        layer.fontsize = self.global_subtitlesvideo_video_burn_fontsize.value()
        final_text = ''

        i = 0
        last_position = .0
        # if not self.subtitles_list[0][0] == .0:
        #     filename = os.path.join(path_tmp, 'empty.png')
        #     layer.subtitle_text = ''
        #     layer.grab().save(filename, 'PNG')

        #     final_text += "file '" + filename + "'\n"
        #     final_text += 'duration {}\n'.format(self.subtitles_list[0][0])

        #     i += 1

        for subtitle in self.subtitles_list:
            if not last_position + .001 > subtitle[0] - .001:
                filename = os.path.join(path_tmp, 'empty.png')
                layer.subtitle_text = ''
                layer.grab().save(filename, 'PNG')

                final_text += "file '" + filename + "'\n"
                final_text += 'duration {}\n'.format(subtitle[0] - last_position)

            filename = os.path.join(path_tmp, '{}.png'.format(i))
            layer.subtitle_text = subtitle[2]
            layer.grab().save(filename, 'PNG')

            final_text += "file '" + filename + "'\n"
            final_text += 'duration {}\n'.format(subtitle[1])

            last_position = subtitle[0] + subtitle[1]
            i += 1
            print(i)

        if not self.subtitles_list[-1][0] + self.subtitles_list[-1][1] == self.video_metadata.get('duration', 60.0):
            filename = os.path.join(path_tmp, 'empty.png')
            layer.subtitle_text = ''
            layer.grab().save(filename, 'PNG')

            final_text += "file '" + filename + "'\n"
            final_text += 'duration {}\n'.format(self.subtitles_list[0][0])
            final_text += "file '" + filename + "'\n"

        open(os.path.join(path_tmp, 'subtitles.txt'), 'w').write(final_text)
        subprocess.Popen([FFMPEG_EXECUTABLE, '-y', '-f', 'concat', '-safe', '0', '-i', os.path.join(path_tmp, 'subtitles.txt'), '-r', str(self.video_metadata.get('framerate', 24)), '-c:v', 'qtrle', '-an', generated_video_filepath], startupinfo=STARTUPINFO, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.read()


def global_subtitlesvideo_export_button_clicked(self):
    """Function to export subtitles"""
    suggested_path = os.path.dirname(self.video_metadata['filepath'])
    suggested_name = os.path.basename(self.video_metadata['filepath']).rsplit('.', 1)[0] + '.txt'

    supported_export_files = ';;'.join(['{description} ({extension})'.format(extension=' '.join(['.{ext}'.format(ext=ext) for ext in LIST_OF_SUPPORTED_EXPORT_EXTENSIONS[export_format]['extensions']]), description=LIST_OF_SUPPORTED_EXPORT_EXTENSIONS[export_format]['description']) for export_format in LIST_OF_SUPPORTED_EXPORT_EXTENSIONS])

    filedialog = QFileDialog.getSaveFileName(parent=self, caption=self.tr('Export to file'), dir=os.path.join(suggested_path, suggested_name), filter=supported_export_files)

    if filedialog[0] and filedialog[1]:
        filename = filedialog[0]
        exts = []
        for extformat in filedialog[1].split('(', 1)[1].split(')', 1)[0].split('*'):
            if extformat:
                exts.append(extformat.strip())
        if not filename.endswith(tuple(exts)):
            filename += exts[0]
        format_to_export = filedialog[1].rsplit('(', 1)[-1].split(')', 1)[0]

        file_io.export_file(filename=filename, subtitles_list=self.subtitles_list, export_format=format_to_export)


def global_panel_export_types_combobox_activated(self):
    if self.global_panel_export_types_combobox.currentText() == 'txt':
        self.global_panel_export_content_stackedwidgets.setCurrentWidget(self.global_panel_export_content_txt_panel)
    elif self.global_panel_export_types_combobox.currentText() == 'mp4':
        self.global_panel_export_content_stackedwidgets.setCurrentWidget(self.global_panel_export_content_mp4_panel)

