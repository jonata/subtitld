"""Subtitles Video panel

"""

import os
import subprocess
import json
import autosub

import speech_recognition as sr

from PySide6.QtWidgets import QComboBox, QPushButton, QWidget, QMessageBox, QGridLayout
from PySide6.QtCore import QThread, Signal, Qt
from subtitld.interface import global_panel

from subtitld.modules.paths import LANGUAGE_DICT_LIST, STARTUPINFO, path_tmp
from subtitld.modules import file_io
from subtitld.modules import utils

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
    self.global_panel_transcription_menu_button = QPushButton('Transcription')
    self.global_panel_transcription_menu_button.setCheckable(True)
    self.global_panel_transcription_menu_button.setProperty('class', 'global_panel_menu')
    self.global_panel_transcription_menu_button.clicked.connect(lambda: global_panel_menu_changed(self))
    self.global_panel_menu.layout().addWidget(self.global_panel_transcription_menu_button)


def global_panel_menu_changed(self):
    global_panel.global_panel_menu_changed(self, self.global_panel_transcription_menu_button, self.global_panel_transcription_content)


def load_widgets(self):
    """Function to load subtitles panel widgets"""

    self.global_panel_transcription_content = QWidget()
    self.global_panel_transcription_content.setLayout(QGridLayout())

    self.global_subtitlesvideo_autosync_lang_combobox = QComboBox()
    self.global_subtitlesvideo_autosync_lang_combobox.setProperty('class', 'button')
    self.global_subtitlesvideo_autosync_lang_combobox.addItems(LANGUAGE_DESCRIPTIONS)
    self.global_panel_transcription_content.layout().addWidget(self.global_subtitlesvideo_autosync_lang_combobox, 0, 0, Qt.AlignTop)

    self.global_subtitlesvideo_autosync_button = QPushButton(self.tr('AutoSync').upper())
    self.global_subtitlesvideo_autosync_button.setProperty('class', 'button')
    self.global_subtitlesvideo_autosync_button.clicked.connect(lambda: global_subtitlesvideo_autosync_button_clicked(self))
    # self.global_subtitlesvideo_autosync_button.setVisible(False)
    self.global_panel_transcription_content.layout().addWidget(self.global_subtitlesvideo_autosync_button, 1, 0, Qt.AlignTop)

    self.global_subtitlesvideo_autosub_button = QPushButton(self.tr('Auto Subtitle').upper())
    self.global_subtitlesvideo_autosub_button.setProperty('class', 'button')
    self.global_subtitlesvideo_autosub_button.clicked.connect(lambda: global_subtitlesvideo_autosub_button_clicked(self))
    self.global_panel_transcription_content.layout().addWidget(self.global_subtitlesvideo_autosub_button, 2, 0, Qt.AlignTop)

    self.global_subtitlesvideo_autotranscribe_button = QPushButton(self.tr('Transcribe').upper())
    self.global_subtitlesvideo_autotranscribe_button.setProperty('class', 'button')
    self.global_subtitlesvideo_autotranscribe_button.clicked.connect(lambda: global_subtitlesvideo_autotranscribe_button_clicked(self))
    self.global_subtitlesvideo_autotranscribe_button.setVisible(True)
    self.global_panel_transcription_content.layout().addWidget(self.global_subtitlesvideo_autotranscribe_button, 3, 0, Qt.AlignTop)

    self.global_panel_content_stacked_widgets.addWidget(self.global_panel_transcription_content)


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
            # update_widgets(self)


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

        # update_widgets(self)


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
        # splits = 60.0
        # actual_split = 0
        final_text = ''

        # while actual_split < self.video_metadata['duration']:

        subprocess.run(['ffmpeg', '-i', self.video_metadata['filepath'], '-y', os.path.join(path_tmp, 'transcribe.wav')])

        r = sr.Recognizer()
        with sr.AudioFile(os.path.join(path_tmp, 'transcribe.wav')) as source:
            audio = r.record(source)

        language = LANGUAGE_DICT_LIST[self.global_subtitlesvideo_autosync_lang_combobox.currentText()].split('-')[0]

        try:
            final_text = r.recognize_google(audio, language=language)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

        # actual_split += splits

        if final_text:
            self.subtitles_list = [[0.0, self.video_metadata['duration'], final_text]]
            # update_widgets(self)
