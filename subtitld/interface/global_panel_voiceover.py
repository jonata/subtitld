"""Subtitles Video panel

"""
import subprocess

from PySide6.QtWidgets import QPushButton, QWidget
from PySide6.QtCore import QThread, Signal

from subtitld.modules.paths import STARTUPINFO
from subtitld.modules import utils
from subtitld.interface import global_panel
from subtitld.interface.translation import _


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
    self.global_panel_voiceover_menu_button = QPushButton()
    self.global_panel_voiceover_menu_button.setCheckable(True)
    self.global_panel_voiceover_menu_button.setProperty('class', 'global_panel_menu')
    self.global_panel_voiceover_menu_button.clicked.connect(lambda: global_panel_menu_changed(self))
    self.global_panel_menu.layout().addWidget(self.global_panel_voiceover_menu_button)


def global_panel_menu_changed(self):
    self.global_panel_voiceover_menu_button.setEnabled(False)
    global_panel.global_panel_menu_changed(self, self.global_panel_voiceover_menu_button, self.global_panel_voiceover_content)


def load_widgets(self):
    """Function to load subtitles panel widgets"""

    self.global_panel_voiceover_content = QWidget()

    self.global_subtitlesvideo_voiceover_button = QPushButton(parent=self.global_panel_voiceover_content)
    self.global_subtitlesvideo_voiceover_button.setProperty('class', 'button')
    self.global_subtitlesvideo_voiceover_button.clicked.connect(lambda: global_subtitlesvideo_autovoiceover_button_clicked(self))


def global_subtitlesvideo_autovoiceover_button_clicked(self):
    """Function to auto voiceover subtitles"""
    None
    # speech_config = SpeechConfig(subscription="", region="southcentralus")
    # speech_config.set_speech_synthesis_output_format(SpeechSynthesisOutputFormat["Riff24Khz16BitMonoPcm"])

    # audio_from_video = AudioSegment.from_file(self.video_metadata['filepath'])
    # final_audio = AudioSegment.empty()

    # audio_config = AudioOutputConfig(filename=os.path.join(path_tmp, 'voiceover.wav'))

    # audio_pieces = []
    # parser = 0
    # first = True
    # for subtitle in self.subtitles_list:
    #     # print(subtitle)

    #     ssml_content = '<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="https://www.w3.org/2001/mstts" xml:lang="en-US"><voice name="pt-BR-AntonioNeural">'
    #     ssml_content += subtitle[2] + '</voice></speak>'

    #     synthesizer = SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

    #     synthesizer.speak_ssml_async(ssml_content)
    #     audio_pieces.append([AudioSegment.from_file(os.path.join(path_tmp, 'voiceover.wav')), int(subtitle[0]*1000)])

    #     piece1 = audio_from_video[parser:int(subtitle[0]*1000)]
    #     if not first:
    #         piece1 = piece1.fade(from_gain=-25.0, start=0, duration=4000)
    #     piece1 = piece1.fade(to_gain=-25.0, end=int(piece1.duration_seconds*1000), duration=1200)
    #     final_audio += piece1
    #     parser = int(subtitle[0]*1000)

    #     piece2 = audio_from_video[parser:parser+int(subtitle[1]*1000)]
    #     piece2 = piece2 - 25.0
    #     final_audio += piece2
    #     parser += int(subtitle[1]*1000)
    #     first = False

    # final_piece = audio_from_video[parser:]
    # final_piece = final_piece.fade(from_gain=-25.0, start=0, duration=5000)
    # final_audio += final_piece

    # #new_audio = sum(audio_pieces)

    # for piece in audio_pieces:
    #     final_audio = final_audio.overlay(piece[0], position=piece[1])

    # final_audio.export(os.path.join(path_tmp, 'final_voiceover.wav'), format='wav')

    # subprocess.call(['ffmpeg', '-i', self.video_metadata['filepath'], '-i' , os.path.join(path_tmp, 'final_voiceover.wav'), '-c:v', 'copy', '-y', '-map', '0:v:0', '-map', '1:a:0', self.video_metadata['filepath'].rsplit('.', 1)[0] + '_voiceover.' + self.video_metadata['filepath'].rsplit('.', 1)[-1]])

    # # list_of_final_audiofiles = []
    # #     audio_config = AudioOutputConfig(filename="file.wav")
    # #     synthesizer = SpeechSynthesizer(speech_config=speech_config, audio_config=None)
    # #     synthesizer.speak_ssml_async(open('teste.ssml').read()))
    # #     File "<stdin>", line 1
    # #         synthesizer.speak_ssml_async(open('teste.ssml').read()))
    # #                                                             ^
    # #     SyntaxError: unmatched ')'
    # #

    # #     language = LANGUAGE_DICT_LIST[self.global_subtitlesvideo_autosync_lang_combobox.currentText()].split('-')[0]
    # #     translator = Translator(service_urls=['translate.googleapis.com'])

    # #         subtitle[2] = translator.translate(subtitle[2], dest=language).text

    # #     update_widgets(self)


def translate_widgets(self):
    self.global_panel_voiceover_menu_button.setText(_('global_panel_voiceover.title'))
    self.global_subtitlesvideo_voiceover_button.setText(_('global_panel_voiceover.voiceover'))