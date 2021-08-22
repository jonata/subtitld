"""Subtitles Video panel

"""

import os
import subprocess
import json
import multiprocessing
import autosub
import speech_recognition as sr
from subtitld import timecode
#from googletrans import Translator
from google_trans_new import google_translator
# from ffsubsync import ffsubsync

from PyQt5.QtWidgets import QCheckBox, QDoubleSpinBox, QGridLayout, QLabel, QComboBox, QPushButton, QFileDialog, QSpinBox, QColorDialog, QTabWidget, QWidget, QTableWidget, QAbstractItemView, QLineEdit, QTableWidgetItem, QHeaderView, QMessageBox, QVBoxLayout, QCheckBox, QGridLayout, QSlider
from PyQt5.QtCore import QMargins, QPropertyAnimation, QEasingCurve, QSize, QThread, pyqtSignal, QEvent, Qt
from PyQt5.QtGui import QBrush, QColor, QFont, QFontDatabase, QKeySequence, QPainter, QPen

from subtitld.modules.paths import LIST_OF_SUPPORTED_SUBTITLE_EXTENSIONS, LIST_OF_SUPPORTED_IMPORT_EXTENSIONS, LIST_OF_SUPPORTED_EXPORT_EXTENSIONS, STARTUPINFO, FFMPEG_EXECUTABLE, path_tmp
from subtitld.modules.shortcuts import shortcuts_dict
from subtitld.modules.paths import LANGUAGE_DICT_LIST, path_tmp
from subtitld.modules import file_io

# from azure.cognitiveservices.speech import AudioDataStream, SpeechConfig, SpeechSynthesizer, SpeechSynthesisOutputFormat
# from azure.cognitiveservices.speech.audio import AudioOutputConfig
# from pydub import AudioSegment

multiprocessing.freeze_support()

LANGUAGE_DESCRIPTIONS = LANGUAGE_DICT_LIST.keys()

list_of_supported_import_extensions = []
for exttype in LIST_OF_SUPPORTED_IMPORT_EXTENSIONS:
    for ext in LIST_OF_SUPPORTED_IMPORT_EXTENSIONS[exttype]['extensions']:
        list_of_supported_import_extensions.append(ext)


def convert_ffmpeg_timecode_to_seconds(timecode):
    """Function to convert ffmpeg timecode to seconds"""
    if timecode:
        final_value = float(timecode.split(':')[-1])
        final_value += int(timecode.split(':')[-2])*60.0
        final_value += int(timecode.split(':')[-3])*3600.0
        return final_value
    else:
        return False


class ThreadGeneratedBurnedVideo(QThread):
    """Thread to generate burned video"""
    response = pyqtSignal(str)
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
                    duration = int(convert_ffmpeg_timecode_to_seconds(output.split('Duration: ', 1)[1].split(',', 1)[0]))
                    if duration > number_of_steps:
                        number_of_steps = duration
                if output[:6] == 'frame=':
                    current_step = int(convert_ffmpeg_timecode_to_seconds(output.split('time=', 1)[1].split(' ', 1)[0]))

                self.response.emit(str(current_step) + '|' + str(number_of_steps))
            self.response.emit('end')


class GlobalSubtitlesvideoPanelTabwidgetShortkeysEditbox(QLineEdit):
    """Class to reimplement QLineEdit in order to get shorkeys selection"""
    def __init__(self, *args, parent=None):
        super(GlobalSubtitlesvideoPanelTabwidgetShortkeysEditbox, self).__init__(*args)
        # self.set_key_sequence(key_sequence)

    def set_key_sequence(self, key_sequence):
        """Set text with the shortkey"""
        self.setText(key_sequence.toString(QKeySequence.NativeText))

    def keyPressEvent(self, event):
        """Function on keyPressEvent"""
        if event.type() == QEvent.KeyPress:
            key = event.key()

            if key == Qt.Key_unknown:
                return

            if(key == Qt.Key_Control
                or key == Qt.Key_Shift
                or key == Qt.Key_Alt
                or key == Qt.Key_Meta):
                return

            modifiers = event.modifiers()
            # keyText = event.text()

            if modifiers & Qt.ShiftModifier:
                key += Qt.SHIFT
            if modifiers & Qt.ControlModifier:
                key += Qt.CTRL
            if modifiers & Qt.AltModifier:
                key += Qt.ALT
            if modifiers & Qt.MetaModifier:
                key += Qt.META

            self.set_key_sequence(QKeySequence(key))


def load(self):
    """Function to load subtitles panel widgets"""
    self.global_subtitlesvideo_panel_widget = QLabel(parent=self)
    self.global_subtitlesvideo_panel_widget_animation = QPropertyAnimation(self.global_subtitlesvideo_panel_widget, b'geometry')
    self.global_subtitlesvideo_panel_widget_animation.setEasingCurve(QEasingCurve.OutCirc)

    self.global_subtitlesvideo_panel_left = QLabel(parent=self.global_subtitlesvideo_panel_widget)
    self.global_subtitlesvideo_panel_left.setObjectName('global_subtitlesvideo_panel_left')
    self.global_subtitlesvideo_panel_right = QLabel(parent=self.global_subtitlesvideo_panel_widget)
    self.global_subtitlesvideo_panel_right.setObjectName('global_subtitlesvideo_panel_right')

    self.global_subtitlesvideo_save_as_label = QLabel(self.tr('Default format to save:').upper(), parent=self.global_subtitlesvideo_panel_widget)

    list_of_subtitle_extensions = []
    for extformat in LIST_OF_SUPPORTED_SUBTITLE_EXTENSIONS:
        list_of_subtitle_extensions.append(extformat + ' - ' + LIST_OF_SUPPORTED_SUBTITLE_EXTENSIONS[extformat]['description'])
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
    self.global_subtitlesvideo_autosync_button.setVisible(False)

    self.global_subtitlesvideo_autosub_button = QPushButton(self.tr('Auto Subtitle').upper(), parent=self.global_subtitlesvideo_panel_widget)
    self.global_subtitlesvideo_autosub_button.setObjectName('button')
    self.global_subtitlesvideo_autosub_button.clicked.connect(lambda: global_subtitlesvideo_autosub_button_clicked(self))

    self.global_subtitlesvideo_translate_button = QPushButton(self.tr('Translate').upper(), parent=self.global_subtitlesvideo_panel_widget)
    self.global_subtitlesvideo_translate_button.setObjectName('button')
    self.global_subtitlesvideo_translate_button.clicked.connect(lambda: global_subtitlesvideo_translate_button_clicked(self))

    self.global_subtitlesvideo_autovoiceover_button = QPushButton(self.tr('Auto Voice-over').upper(), parent=self.global_subtitlesvideo_panel_widget)
    self.global_subtitlesvideo_autovoiceover_button.setObjectName('button')
    self.global_subtitlesvideo_autovoiceover_button.clicked.connect(lambda: global_subtitlesvideo_autovoiceover_button_clicked(self))
    self.global_subtitlesvideo_autovoiceover_button.setVisible(False)

    self.global_subtitlesvideo_autotranscribe_button = QPushButton(self.tr('Transcribe').upper(), parent=self.global_subtitlesvideo_panel_widget)
    self.global_subtitlesvideo_autotranscribe_button.setObjectName('button')
    self.global_subtitlesvideo_autotranscribe_button.clicked.connect(lambda: global_subtitlesvideo_autotranscribe_button_clicked(self))
    self.global_subtitlesvideo_autotranscribe_button.setVisible(True)

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

    self.global_subtitlesvideo_video_generate_transparent_video_button = QPushButton(self.tr('Generate transparent video').upper(), parent=self.global_subtitlesvideo_panel_tabwidget_export_panel)
    self.global_subtitlesvideo_video_generate_transparent_video_button.setObjectName('button_dark')
    self.global_subtitlesvideo_video_generate_transparent_video_button.clicked.connect(lambda: global_subtitlesvideo_video_generate_transparent_video_button_clicked(self))
    # self.global_subtitlesvideo_video_generate_transparent_video_button.setVisible(False)

    def thread_generated_burned_video_ended(response):
        if '|' in response:
            self.global_subtitlesvideo_video_burn_convert.setText('GENERATING... (' + str(int((float(response.split('|')[0]) / float(response.split('|')[1])) * 100)) + '%)')
        elif 'end' in response:
            self.global_subtitlesvideo_video_burn_convert.setText(self.tr('Generate video').upper())
            self.global_subtitlesvideo_video_burn_convert.setEnabled(True)

    self.thread_generated_burned_video = ThreadGeneratedBurnedVideo(self)
    self.thread_generated_burned_video.response.connect(thread_generated_burned_video_ended)

    self.global_subtitlesvideo_panel_tabwidget.addTab(self.global_subtitlesvideo_panel_tabwidget_export_panel, self.tr('Export burned-in subtitles').upper())

    self.global_subtitlesvideo_panel_tabwidget_shortkeys_panel = QWidget()

    self.global_subtitlesvideo_panel_tabwidget_shortkeys_editbox = GlobalSubtitlesvideoPanelTabwidgetShortkeysEditbox(parent=self.global_subtitlesvideo_panel_tabwidget_shortkeys_panel)
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

    self.global_subtitlesvideo_panel_tabwidget_quality_panel = QWidget()

    self.global_subtitlesvideo_panel_tabwidget_quality_panel_vbox = QVBoxLayout()

    self.global_subtitlesvideo_panel_tabwidget_quality_enable_checkbox = QCheckBox('Enable quality check')
    self.global_subtitlesvideo_panel_tabwidget_quality_enable_checkbox.setChecked(False)
    self.global_subtitlesvideo_panel_tabwidget_quality_enable_checkbox.stateChanged.connect(lambda: update_quality_settings(self))
    self.global_subtitlesvideo_panel_tabwidget_quality_panel_vbox.addWidget(self.global_subtitlesvideo_panel_tabwidget_quality_enable_checkbox)

    self.global_subtitlesvideo_panel_tabwidget_quality_forms_grid = QGridLayout()

    self.global_subtitlesvideo_panel_tabwidget_quality_readingspeed_vbox = QVBoxLayout()
    self.global_subtitlesvideo_panel_tabwidget_quality_readingspeed_label = QLabel(self.tr('Reading Speed (characters per second)').upper(), parent=self.global_subtitlesvideo_panel_tabwidget_quality_panel)
    self.global_subtitlesvideo_panel_tabwidget_quality_readingspeed_vbox.addWidget(self.global_subtitlesvideo_panel_tabwidget_quality_readingspeed_label)
    self.global_subtitlesvideo_panel_tabwidget_quality_readingspeed = QSpinBox(parent=self.global_subtitlesvideo_panel_tabwidget_quality_panel)
    self.global_subtitlesvideo_panel_tabwidget_quality_readingspeed.setMinimum(0)
    self.global_subtitlesvideo_panel_tabwidget_quality_readingspeed.setMaximum(999)
    self.global_subtitlesvideo_panel_tabwidget_quality_readingspeed.setValue(21)
    self.global_subtitlesvideo_panel_tabwidget_quality_readingspeed.valueChanged.connect(lambda: update_quality_settings(self))
    self.global_subtitlesvideo_panel_tabwidget_quality_readingspeed_vbox.addWidget(self.global_subtitlesvideo_panel_tabwidget_quality_readingspeed)
    self.global_subtitlesvideo_panel_tabwidget_quality_forms_grid.addLayout(self.global_subtitlesvideo_panel_tabwidget_quality_readingspeed_vbox, 0, 0)

    self.global_subtitlesvideo_panel_tabwidget_quality_minimumduration_vbox = QVBoxLayout()
    self.global_subtitlesvideo_panel_tabwidget_quality_minimumduration_label = QLabel(self.tr('Minimum subtitle duration (in seconds)').upper(), parent=self.global_subtitlesvideo_panel_tabwidget_quality_panel)
    self.global_subtitlesvideo_panel_tabwidget_quality_minimumduration_vbox.addWidget(self.global_subtitlesvideo_panel_tabwidget_quality_minimumduration_label)
    self.global_subtitlesvideo_panel_tabwidget_quality_minimumduration = QDoubleSpinBox(parent=self.global_subtitlesvideo_panel_tabwidget_quality_panel)
    self.global_subtitlesvideo_panel_tabwidget_quality_minimumduration.setMinimum(0.1)
    self.global_subtitlesvideo_panel_tabwidget_quality_minimumduration.setMaximum(999.999)
    self.global_subtitlesvideo_panel_tabwidget_quality_minimumduration.setValue(.7)
    self.global_subtitlesvideo_panel_tabwidget_quality_minimumduration.valueChanged.connect(lambda: update_quality_settings(self))
    self.global_subtitlesvideo_panel_tabwidget_quality_minimumduration_vbox.addWidget(self.global_subtitlesvideo_panel_tabwidget_quality_minimumduration)
    self.global_subtitlesvideo_panel_tabwidget_quality_forms_grid.addLayout(self.global_subtitlesvideo_panel_tabwidget_quality_minimumduration_vbox, 0, 1)

    self.global_subtitlesvideo_panel_tabwidget_quality_maximumduration_vbox = QVBoxLayout()
    self.global_subtitlesvideo_panel_tabwidget_quality_maximumduration_label = QLabel(self.tr('Maximum subtitle duration (in seconds)').upper(), parent=self.global_subtitlesvideo_panel_tabwidget_quality_panel)
    self.global_subtitlesvideo_panel_tabwidget_quality_maximumduration_vbox.addWidget(self.global_subtitlesvideo_panel_tabwidget_quality_maximumduration_label)
    self.global_subtitlesvideo_panel_tabwidget_quality_maximumduration = QDoubleSpinBox(parent=self.global_subtitlesvideo_panel_tabwidget_quality_panel)
    self.global_subtitlesvideo_panel_tabwidget_quality_maximumduration.setMinimum(0.2)
    self.global_subtitlesvideo_panel_tabwidget_quality_maximumduration.setMaximum(999.999)
    self.global_subtitlesvideo_panel_tabwidget_quality_maximumduration.setValue(7)
    self.global_subtitlesvideo_panel_tabwidget_quality_maximumduration.valueChanged.connect(lambda: update_quality_settings(self))
    self.global_subtitlesvideo_panel_tabwidget_quality_maximumduration_vbox.addWidget(self.global_subtitlesvideo_panel_tabwidget_quality_maximumduration)
    self.global_subtitlesvideo_panel_tabwidget_quality_forms_grid.addLayout(self.global_subtitlesvideo_panel_tabwidget_quality_maximumduration_vbox, 0, 2)

    self.global_subtitlesvideo_panel_tabwidget_quality_maximumlines_vbox = QVBoxLayout()
    self.global_subtitlesvideo_panel_tabwidget_quality_maximumlines_label = QLabel(self.tr('Maximum number of lines').upper(), parent=self.global_subtitlesvideo_panel_tabwidget_quality_panel)
    self.global_subtitlesvideo_panel_tabwidget_quality_maximumlines_vbox.addWidget(self.global_subtitlesvideo_panel_tabwidget_quality_maximumlines_label)
    self.global_subtitlesvideo_panel_tabwidget_quality_maximumlines = QSpinBox(parent=self.global_subtitlesvideo_panel_tabwidget_quality_panel)
    self.global_subtitlesvideo_panel_tabwidget_quality_maximumlines.setMinimum(1)
    self.global_subtitlesvideo_panel_tabwidget_quality_maximumlines.setMaximum(10)
    self.global_subtitlesvideo_panel_tabwidget_quality_maximumlines.setValue(2)
    self.global_subtitlesvideo_panel_tabwidget_quality_maximumlines.valueChanged.connect(lambda: update_quality_settings(self))
    self.global_subtitlesvideo_panel_tabwidget_quality_maximumlines_vbox.addWidget(self.global_subtitlesvideo_panel_tabwidget_quality_maximumlines)
    self.global_subtitlesvideo_panel_tabwidget_quality_forms_grid.addLayout(self.global_subtitlesvideo_panel_tabwidget_quality_maximumlines_vbox, 1, 0)

    self.global_subtitlesvideo_panel_tabwidget_quality_maximumcharactersperline_vbox = QVBoxLayout()
    self.global_subtitlesvideo_panel_tabwidget_quality_maximumcharactersperline_label = QLabel(self.tr('Maximum number characters per line').upper(), parent=self.global_subtitlesvideo_panel_tabwidget_quality_panel)
    self.global_subtitlesvideo_panel_tabwidget_quality_maximumcharactersperline_vbox.addWidget(self.global_subtitlesvideo_panel_tabwidget_quality_maximumcharactersperline_label)
    self.global_subtitlesvideo_panel_tabwidget_quality_maximumcharactersperline = QSpinBox(parent=self.global_subtitlesvideo_panel_tabwidget_quality_panel)
    self.global_subtitlesvideo_panel_tabwidget_quality_maximumcharactersperline.setMinimum(1)
    self.global_subtitlesvideo_panel_tabwidget_quality_maximumcharactersperline.setMaximum(999)
    self.global_subtitlesvideo_panel_tabwidget_quality_maximumcharactersperline.setValue(42)
    self.global_subtitlesvideo_panel_tabwidget_quality_maximumcharactersperline.valueChanged.connect(lambda: update_quality_settings(self))
    self.global_subtitlesvideo_panel_tabwidget_quality_maximumcharactersperline_vbox.addWidget(self.global_subtitlesvideo_panel_tabwidget_quality_maximumcharactersperline)
    self.global_subtitlesvideo_panel_tabwidget_quality_forms_grid.addLayout(self.global_subtitlesvideo_panel_tabwidget_quality_maximumcharactersperline_vbox, 1, 1)

    self.global_subtitlesvideo_panel_tabwidget_quality_panel_vbox.addLayout(self.global_subtitlesvideo_panel_tabwidget_quality_forms_grid)

    self.global_subtitlesvideo_panel_tabwidget_quality_prefercompact_checkbox = QCheckBox('Prefer compact subtitles')
    self.global_subtitlesvideo_panel_tabwidget_quality_prefercompact_checkbox.setChecked(False)
    self.global_subtitlesvideo_panel_tabwidget_quality_prefercompact_checkbox.stateChanged.connect(lambda: update_quality_settings(self))
    self.global_subtitlesvideo_panel_tabwidget_quality_panel_vbox.addWidget(self.global_subtitlesvideo_panel_tabwidget_quality_prefercompact_checkbox)

    self.global_subtitlesvideo_panel_tabwidget_quality_balanceratio_vbox = QVBoxLayout()
    self.global_subtitlesvideo_panel_tabwidget_quality_balanceratio_checkbox = QCheckBox('Balance line length ratio (percentage the shortest should be of the largest)')
    self.global_subtitlesvideo_panel_tabwidget_quality_balanceratio_checkbox.setChecked(False)
    self.global_subtitlesvideo_panel_tabwidget_quality_balanceratio_checkbox.stateChanged.connect(lambda: update_quality_settings(self))
    self.global_subtitlesvideo_panel_tabwidget_quality_balanceratio_vbox.addWidget(self.global_subtitlesvideo_panel_tabwidget_quality_balanceratio_checkbox)
    self.global_subtitlesvideo_panel_tabwidget_quality_balanceratio_slider = QSlider(orientation=Qt.Horizontal)
    self.global_subtitlesvideo_panel_tabwidget_quality_balanceratio_slider.setMinimum(0)
    self.global_subtitlesvideo_panel_tabwidget_quality_balanceratio_slider.setMaximum(100)
    self.global_subtitlesvideo_panel_tabwidget_quality_balanceratio_slider.setValue(50)
    self.global_subtitlesvideo_panel_tabwidget_quality_balanceratio_slider.valueChanged.connect(lambda: update_quality_settings(self))
    self.global_subtitlesvideo_panel_tabwidget_quality_balanceratio_vbox.addWidget(self.global_subtitlesvideo_panel_tabwidget_quality_balanceratio_slider)
    self.global_subtitlesvideo_panel_tabwidget_quality_panel_vbox.addLayout(self.global_subtitlesvideo_panel_tabwidget_quality_balanceratio_vbox)

    self.global_subtitlesvideo_panel_tabwidget_quality_panel_vbox.addStretch()
    self.global_subtitlesvideo_panel_tabwidget_quality_panel.setLayout(self.global_subtitlesvideo_panel_tabwidget_quality_panel_vbox)

    self.global_subtitlesvideo_panel_tabwidget.addTab(self.global_subtitlesvideo_panel_tabwidget_quality_panel, self.tr('Quality control').upper())

    update_global_subtitlesvideo_panel_tabwidget_quality_panel_widgets(self)

def resized(self):
    """Function on resizing widgets"""
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
    self.global_subtitlesvideo_autosync_lang_combobox.setGeometry(20, 160, self.global_subtitlesvideo_panel_left.width()-40, 30)
    # self.global_subtitlesvideo_autosync_button.setGeometry(100, 160, self.global_subtitlesvideo_panel_left.width()-120, 30)
    self.global_subtitlesvideo_autosub_button.setGeometry(100, 200, self.global_subtitlesvideo_panel_left.width()-120, 30)
    self.global_subtitlesvideo_translate_button.setGeometry(100, 240, self.global_subtitlesvideo_panel_left.width()-120, 30)
    self.global_subtitlesvideo_autovoiceover_button.setGeometry(100, 280, self.global_subtitlesvideo_panel_left.width()-120, 30)
    self.global_subtitlesvideo_autotranscribe_button.setGeometry(100, 280, self.global_subtitlesvideo_panel_left.width()-120, 30)

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
    """Function to show subtitlesvideo panel"""
    self.generate_effect(self.global_subtitlesvideo_panel_widget_animation, 'geometry', 700, [self.global_subtitlesvideo_panel_widget.x(), self.global_subtitlesvideo_panel_widget.y(), self.global_subtitlesvideo_panel_widget.width(), self.global_subtitlesvideo_panel_widget.height()], [0, self.global_subtitlesvideo_panel_widget.y(), self.global_subtitlesvideo_panel_widget.width(), self.global_subtitlesvideo_panel_widget.height()])


def global_subtitlesvideo_panel_tabwidget_shortkeys_table_update(self):
    """Function to update subtitlesvideo panel shorkeys table"""
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
    """Function to change button states"""
    self.global_subtitlesvideo_panel_tabwidget_shortkeys_set_button.setVisible(not self.global_subtitlesvideo_panel_tabwidget_shortkeys_set_button.isVisible())
    self.global_subtitlesvideo_panel_tabwidget_shortkeys_editbox.setVisible(not self.global_subtitlesvideo_panel_tabwidget_shortkeys_set_button.isVisible())
    self.global_subtitlesvideo_panel_tabwidget_shortkeys_editbox_confirm.setVisible(not self.global_subtitlesvideo_panel_tabwidget_shortkeys_set_button.isVisible())
    self.global_subtitlesvideo_panel_tabwidget_shortkeys_editbox_cancel.setVisible(not self.global_subtitlesvideo_panel_tabwidget_shortkeys_set_button.isVisible())
    self.global_subtitlesvideo_panel_tabwidget_shortkeys_table.setVisible(self.global_subtitlesvideo_panel_tabwidget_shortkeys_set_button.isVisible())


def global_subtitlesvideo_panel_tabwidget_shortkeys_editbox_cancel_clicked(self):
    """Function to cancel shortkeys editing"""
    # self.global_subtitlesvideo_panel_tabwidget_shortkeys_set_button.setVisible(True)
    global_subtitlesvideo_panel_tabwidget_shortkeys_set_button_clicked(self)


def global_subtitlesvideo_panel_tabwidget_shortkeys_editbox_confirm_clicked(self):
    """Function to confirm shortkey editing"""
    inverted_shortcuts_dict = {value: key for key, value in shortcuts_dict.items()}
    self.settings['shortcuts'][inverted_shortcuts_dict[self.global_subtitlesvideo_panel_tabwidget_shortkeys_table.item(self.global_subtitlesvideo_panel_tabwidget_shortkeys_table.currentRow(), 0).text()]] = [self.global_subtitlesvideo_panel_tabwidget_shortkeys_editbox.text()]
    self.shortcuts.load(self, self.settings['shortcuts'])
    global_subtitlesvideo_panel_tabwidget_shortkeys_table_update(self)
    global_subtitlesvideo_panel_tabwidget_shortkeys_editbox_cancel_clicked(self)


def global_subtitlesvideo_import_button_clicked(self):
    """Function to import file"""
    # if self.global_subtitlesvideo_import_button.isChecked():
    #     self.global_subtitlesvideo_export_button.setGeometry(20, 200, self.global_subtitlesvideo_panel_left.width()-40, 30)
    # else:
    #     self.global_subtitlesvideo_export_button.setGeometry(20, 120, self.global_subtitlesvideo_panel_left.width()-40, 30)
    # self.global_subtitlesvideo_import_panel.setVisible(self.global_subtitlesvideo_import_button.isChecked())

    supported_import_files = self.tr('Text files') + ' ({})'.format(" ".join(["*.{}".format(fo) for fo in list_of_supported_import_extensions]))
    file_to_open = QFileDialog.getOpenFileName(self, self.tr('Select the file to import'), os.path.expanduser("~"), supported_import_files)[0]
    if file_to_open:
        self.subtitles_list += file_io.import_file(filename=file_to_open)[0]
        self.subtitles_list.sort()
        update_widgets(self)


def global_subtitlesvideo_video_burn_convert_clicked(self):
    """Function to generate buned video"""
    suggested_path = os.path.dirname(self.video_metadata['filepath'])
    extformat = os.path.basename(self.video_metadata['filepath']).rsplit('.', 1)[1]
    save_formats = self.tr('Video file') + ' (.' + extformat + ')'
    suggested_name = os.path.basename(self.video_metadata['filepath']).rsplit('.', 1)[0] + '_subtitled.' + extformat

    generated_video_filepath = QFileDialog.getSaveFileName(self, self.tr('Select the subtitle file'), os.path.join(suggested_path, suggested_name), save_formats)[0]

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
    extformat = 'mov'#os.path.basename(self.video_metadata['filepath']).rsplit('.', 1)[1]
    save_formats = self.tr('Video file') + ' (.' + extformat + ')'
    suggested_name = os.path.basename(self.video_metadata['filepath']).rsplit('.', 1)[0] + '_subtitled.' + extformat

    generated_video_filepath = QFileDialog.getSaveFileName(self, self.tr('Select the subtitle file'), os.path.join(suggested_path, suggested_name), save_formats)[0]

    print(path_tmp)

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

                    text_rect = painter.boundingRect(canvas.width()*.08, canvas.height()*.08, canvas.width()*.84, canvas.height()*.84, Qt.AlignBottom | Qt.AlignHCenter | Qt.TextWordWrap, canvas.subtitle_text)

                    painter.setPen(Qt.NoPen)
                    painter.setBrush(QBrush(QColor('#cc000000')))
                    painter.drawRoundedRect(text_rect.marginsAdded(QMargins(10,10,10,10)), 5, 5)

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

    filedialog = QFileDialog.getSaveFileName(self, self.tr('Export to file'), os.path.join(suggested_path, suggested_name), supported_export_files)

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


def hide_global_subtitlesvideo_panel(self):
    """Function to hide subtitlesvideo panel"""
    self.generate_effect(self.global_subtitlesvideo_panel_widget_animation, 'geometry', 700, [self.global_subtitlesvideo_panel_widget.x(), self.global_subtitlesvideo_panel_widget.y(), self.global_subtitlesvideo_panel_widget.width(), self.global_subtitlesvideo_panel_widget.height()], [int(-(self.width()*.6))-18, self.global_subtitlesvideo_panel_widget.y(), self.global_subtitlesvideo_panel_widget.width(), self.global_subtitlesvideo_panel_widget.height()])


def update_global_subtitlesvideo_save_as_combobox(self):
    """Function to update saveas combobox"""
    self.global_subtitlesvideo_save_as_combobox.setCurrentText(self.format_to_save + ' - ' + LIST_OF_SUPPORTED_SUBTITLE_EXTENSIONS[self.format_to_save]['description'])


def global_subtitlesvideo_save_as_combobox_activated(self):
    """Function to change format as combobox selection"""
    self.format_to_save = self.global_subtitlesvideo_save_as_combobox.currentText().split(' ', 1)[0]


def global_subtitlesvideo_autosync_button_clicked(self):
    """Function to run autosync"""
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
        file_io.save_file(os.path.join(path_tmp, 'subtitle_original.srt'), self.subtitles_list, 'SRT')
        sub = os.path.join(path_tmp, 'subtitle_final.srt')

        # unparsed_args = [self.video_metadata['filepath'], "-i", os.path.join(path_tmp, 'subtitle_original.srt'), "-o", sub]

        # parser = ffsubsync.make_parser()
        # args = parser.parse_args(unparsed_args)

        # ffsubsync.run(args)

        if os.path.isfile(sub):
            self.subtitles_list = file_io.process_subtitles_file(sub)[0]
            update_widgets(self)


def global_subtitlesvideo_autosub_button_clicked(self):
    """Function to run autosub"""
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
        autosub.generate_subtitles(self.video_metadata['filepath'], output=os.path.join(path_tmp, 'subtitle.json'), src_language=language, dst_language=language, subtitle_file_format='json')

        if os.path.isfile(os.path.join(path_tmp, 'subtitle.json')):
            final_subtitles = read_json_subtitles(filename=os.path.join(path_tmp, 'subtitle.json'), transcribed=True)
            if final_subtitles:
                self.subtitles_list = final_subtitles

        update_widgets(self)

def update_widgets(self):
    self.unsaved = True
    self.selected_subtitle = False
    self.subtitleslist.update_subtitles_list_qlistwidget(self)
    self.timeline.update(self)
    self.properties.update_properties_widget(self)


def global_subtitlesvideo_translate_button_clicked(self):
    """Function to translate subtitles"""
    run_command = False

    if bool(self.subtitles_list):
        are_you_sure_message = QMessageBox(self)
        are_you_sure_message.setWindowTitle(self.tr('Are you sure?'))
        are_you_sure_message.setText(self.tr('This will overwrite your actual subtitle set. New text will be applied. Are you sure you want to replace your actual subtitles?'))
        are_you_sure_message.addButton(self.tr('Yes'), QMessageBox.AcceptRole)
        are_you_sure_message.addButton(self.tr('No'), QMessageBox.RejectRole)
        ret = are_you_sure_message.exec_()

        if ret == QMessageBox.AcceptRole:
            run_command = True
    else:
        run_command = True

    if run_command:

        language = LANGUAGE_DICT_LIST[self.global_subtitlesvideo_autosync_lang_combobox.currentText()].split('-')[0]
        translator = google_translator()  #translator(service_urls=['translate.googleapis.com', 'translate.google.com','translate.google.co.kr'])
        for subtitle in self.subtitles_list:
            subtitle[2] = translator.translate(subtitle[2].replace('\n', ' ').replace('  ', ' '), lang_tgt=language)

        update_widgets(self)

def global_subtitlesvideo_autotranscribe_button_clicked(self):
    """Function to transcribe using google speech"""
    run_command = False

    if bool(self.subtitles_list):
        are_you_sure_message = QMessageBox(self)
        are_you_sure_message.setWindowTitle(self.tr('Are you sure?'))
        are_you_sure_message.setText(self.tr('This will overwrite your actual subtitle set. New text will be applied. Are you sure you want to replace your actual subtitles?'))
        are_you_sure_message.addButton(self.tr('Yes'), QMessageBox.AcceptRole)
        are_you_sure_message.addButton(self.tr('No'), QMessageBox.RejectRole)
        ret = are_you_sure_message.exec_()

        if ret == QMessageBox.AcceptRole:
            run_command = True
    else:
        run_command = True

    if run_command:
        splits = 60.0
        actual_split = 0
        final_text = ''

        # while actual_split < self.video_metadata['duration']:

        subprocess.run(['ffmpeg', '-i', self.video_metadata['filepath'], '-y', os.path.join(path_tmp, 'transcribe.wav')])


        r = sr.Recognizer()
        with sr.AudioFile(os.path.join(path_tmp, 'transcribe.wav')) as source:
            audio = r.record(source)

        language = LANGUAGE_DICT_LIST[self.global_subtitlesvideo_autosync_lang_combobox.currentText()].split('-')[0]

        try:
            final_text =  r.recognize_google(audio, language=language)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

        # actual_split += splits

        if final_text:
            self.subtitles_list = [[0.0, self.video_metadata['duration'], final_text]]
            update_widgets(self)


def global_subtitlesvideo_autovoiceover_button_clicked(self):
    """Function to auto voiceover subtitles"""
    speech_config = SpeechConfig(subscription="", region="southcentralus")
    speech_config.set_speech_synthesis_output_format(SpeechSynthesisOutputFormat["Riff24Khz16BitMonoPcm"])

    audio_from_video = AudioSegment.from_file(self.video_metadata['filepath'])
    final_audio = AudioSegment.empty()

    audio_config = AudioOutputConfig(filename=os.path.join(path_tmp, 'voiceover.wav'))

    audio_pieces = []
    parser = 0
    first = True
    for subtitle in self.subtitles_list:
        # print(subtitle)

        ssml_content = '<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="https://www.w3.org/2001/mstts" xml:lang="en-US"><voice name="pt-BR-AntonioNeural">'
        ssml_content += subtitle[2] + '</voice></speak>'

        synthesizer = SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

        synthesizer.speak_ssml_async(ssml_content)
        audio_pieces.append([AudioSegment.from_file(os.path.join(path_tmp, 'voiceover.wav')), int(subtitle[0]*1000)])

        piece1 = audio_from_video[parser:int(subtitle[0]*1000)]
        if not first:
            piece1 = piece1.fade(from_gain=-25.0, start=0, duration=4000)
        piece1 = piece1.fade(to_gain=-25.0, end=int(piece1.duration_seconds*1000), duration=1200)
        final_audio += piece1
        parser = int(subtitle[0]*1000)

        piece2 = audio_from_video[parser:parser+int(subtitle[1]*1000)]
        piece2 = piece2 - 25.0
        final_audio += piece2
        parser += int(subtitle[1]*1000)
        first = False

    final_piece = audio_from_video[parser:]
    final_piece = final_piece.fade(from_gain=-25.0, start=0, duration=5000)
    final_audio += final_piece

    #new_audio = sum(audio_pieces)

    for piece in audio_pieces:
        final_audio = final_audio.overlay(piece[0], position=piece[1])

    final_audio.export(os.path.join(path_tmp, 'final_voiceover.wav'), format='wav')

    subprocess.call(['ffmpeg', '-i', self.video_metadata['filepath'], '-i' , os.path.join(path_tmp, 'final_voiceover.wav'), '-c:v', 'copy', '-y', '-map', '0:v:0', '-map', '1:a:0', self.video_metadata['filepath'].rsplit('.', 1)[0] + '_voiceover.' + self.video_metadata['filepath'].rsplit('.', 1)[-1]])





    # list_of_final_audiofiles = []
    #     audio_config = AudioOutputConfig(filename="file.wav")
    #     synthesizer = SpeechSynthesizer(speech_config=speech_config, audio_config=None)
    #     synthesizer.speak_ssml_async(open('teste.ssml').read()))
    #     File "<stdin>", line 1
    #         synthesizer.speak_ssml_async(open('teste.ssml').read()))
    #                                                             ^
    #     SyntaxError: unmatched ')'
    #


    #     language = LANGUAGE_DICT_LIST[self.global_subtitlesvideo_autosync_lang_combobox.currentText()].split('-')[0]
    #     translator = Translator(service_urls=['translate.googleapis.com'])

    #         subtitle[2] = translator.translate(subtitle[2], dest=language).text

    #     update_widgets(self)

def update_global_subtitlesvideo_panel_tabwidget_quality_panel_widgets(self):
    self.global_subtitlesvideo_panel_tabwidget_quality_enable_checkbox.setChecked(self.settings['quality_check'].get('enabled', False))
    self.global_subtitlesvideo_panel_tabwidget_quality_readingspeed.setValue(self.settings['quality_check'].get('reading_speed', 21))
    self.global_subtitlesvideo_panel_tabwidget_quality_minimumduration.setValue(self.settings['quality_check'].get('minimum_duration', .7))
    self.global_subtitlesvideo_panel_tabwidget_quality_maximumduration.setValue(self.settings['quality_check'].get('maximum_duration', 7))
    self.global_subtitlesvideo_panel_tabwidget_quality_maximumlines.setValue(self.settings['quality_check'].get('maximum_lines', 2))
    self.global_subtitlesvideo_panel_tabwidget_quality_maximumcharactersperline.setValue(self.settings['quality_check'].get('maximum_characters_per_line', 42))
    self.global_subtitlesvideo_panel_tabwidget_quality_prefercompact_checkbox.setChecked(self.settings['quality_check'].get('prefer_compact', False))
    self.global_subtitlesvideo_panel_tabwidget_quality_balanceratio_checkbox.setText('Balance line length ratio ({p}% the shortest should be of the largest)'.format(p=self.settings['quality_check'].get('balance_ratio', 50)))
    self.global_subtitlesvideo_panel_tabwidget_quality_balanceratio_checkbox.setChecked(self.settings['quality_check'].get('balance_ratio_enabled', False))
    self.global_subtitlesvideo_panel_tabwidget_quality_balanceratio_slider.setValue(self.settings['quality_check'].get('balance_ratio', 50))

def update_quality_settings(self):
    self.settings['quality_check']['enabled'] = self.global_subtitlesvideo_panel_tabwidget_quality_enable_checkbox.isChecked()
    self.settings['quality_check']['reading_speed'] = self.global_subtitlesvideo_panel_tabwidget_quality_readingspeed.value()
    self.settings['quality_check']['minimum_duration'] = self.global_subtitlesvideo_panel_tabwidget_quality_minimumduration.value()
    self.settings['quality_check']['maximum_duration'] = self.global_subtitlesvideo_panel_tabwidget_quality_maximumduration.value()
    self.settings['quality_check']['maximum_lines'] = self.global_subtitlesvideo_panel_tabwidget_quality_maximumlines.value()
    self.settings['quality_check']['maximum_characters_per_line'] = self.global_subtitlesvideo_panel_tabwidget_quality_maximumcharactersperline.value()
    self.settings['quality_check']['prefer_compact'] = self.global_subtitlesvideo_panel_tabwidget_quality_prefercompact_checkbox.isChecked()
    self.settings['quality_check']['balance_ratio_enabled'] = self.global_subtitlesvideo_panel_tabwidget_quality_balanceratio_checkbox.isChecked()
    self.settings['quality_check']['balance_ratio'] = self.global_subtitlesvideo_panel_tabwidget_quality_balanceratio_slider.value()
    update_global_subtitlesvideo_panel_tabwidget_quality_panel_widgets(self)
