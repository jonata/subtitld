"""Subtitles Video panel

"""

import subprocess
from google_trans_new import google_translator

from PySide6.QtWidgets import QComboBox, QPushButton, QWidget, QMessageBox, QGridLayout
from PySide6.QtCore import QThread, Signal, Qt

from subtitld.modules.paths import LANGUAGE_DICT_LIST, STARTUPINFO
from subtitld.modules import utils
from subtitld.interface import global_panel


LANGUAGE_DESCRIPTIONS = LANGUAGE_DICT_LIST.keys()


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
    self.global_panel_translation_menu_button = QPushButton('Translation')
    self.global_panel_translation_menu_button.setCheckable(True)
    self.global_panel_translation_menu_button.setProperty('class', 'global_panel_menu')
    self.global_panel_translation_menu_button.clicked.connect(lambda: global_panel_menu_changed(self))
    self.global_panel_menu.layout().addWidget(self.global_panel_translation_menu_button)


def global_panel_menu_changed(self):
    self.global_panel_translation_menu_button.setEnabled(False)
    global_panel.global_panel_menu_changed(self, self.global_panel_translation_menu_button, self.global_panel_translation_content)


def load_widgets(self):
    """Function to load subtitles panel widgets"""

    self.global_panel_translation_content = QWidget()
    self.global_panel_translation_content.setLayout(QGridLayout())

    self.global_subtitlesvideo_autosync_lang_combobox = QComboBox()
    self.global_subtitlesvideo_autosync_lang_combobox.setProperty('class', 'button')
    self.global_subtitlesvideo_autosync_lang_combobox.addItems(LANGUAGE_DESCRIPTIONS)
    self.global_panel_translation_content.layout().addWidget(self.global_subtitlesvideo_autosync_lang_combobox, 0, 0, Qt.AlignTop)

    self.global_subtitlesvideo_translate_button = QPushButton(self.tr('Translate').upper())
    self.global_subtitlesvideo_translate_button.setProperty('class', 'button')
    self.global_subtitlesvideo_translate_button.clicked.connect(lambda: global_subtitlesvideo_translate_button_clicked(self))
    self.global_panel_translation_content.layout().addWidget(self.global_subtitlesvideo_translate_button, 0, 1, Qt.AlignTop)

    self.global_panel_content_stacked_widgets.addWidget(self.global_panel_translation_content)


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
        translator = google_translator()  # translator(service_urls=['translate.googleapis.com', 'translate.google.com','translate.google.co.kr'])
        for subtitle in self.subtitles_list:
            subtitle[2] = translator.translate(subtitle[2].replace('\n', ' ').replace('  ', ' '), lang_tgt=language)

        # update_widgets(self)
