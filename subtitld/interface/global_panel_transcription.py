"""Subtitles Video panel

"""

import os
import subprocess
import json

import speech_recognition as sr

from PySide6.QtWidgets import QComboBox, QPushButton, QWidget, QMessageBox, QVBoxLayout, QTabWidget, QHBoxLayout, QLabel, QGroupBox, QProgressBar
from PySide6.QtCore import QThread, Signal, Qt, QSize, QRect, QMargins
from PySide6.QtGui import QPainter, QPen, QColor, QFont
from subtitld.interface import global_panel, subtitles_panel, player
from subtitld.interface.translation import _

from subtitld.modules.paths import LANGUAGE_DICT_LIST, STARTUPINFO, path_tmp, FFMPEG_EXECUTABLE
from subtitld.modules import file_io
from subtitld.modules import utils
from subtitld import autosub

LANGUAGE_DESCRIPTIONS = LANGUAGE_DICT_LIST.keys()


class global_panel_transcription_autosubtitles_thread(QThread):
    """Thread to generate burned video"""
    response = Signal(str)
    original_file = ''
    language = 'en'

    def run(self):
        if self.original_file:
            autosub.generate_subtitles(
                self.original_file,
                output=os.path.join(path_tmp, 'subtitle.json'),
                src_language=self.language,
                dst_language=self.language,
                subtitle_file_format='json',
                ffmpeg_executable=FFMPEG_EXECUTABLE
            )
            self.response.emit('end')


class global_panel_transcription_transcript_thread(QThread):
    """Class of qtread to get waveform data"""
    result = Signal(str)
    text = Signal(str)

    def __init__(self):
        super().__init__()
        self.metadata = {}
        self.selected_language = False

    def run(self):
        final_text = ''
        total_steps = int(self.metadata['duration'] / 60)

        actual_split = 0
        while actual_split < self.metadata['duration']:
            if self.metadata and self.selected_language:
                self.result.emit('{}/{}'.format(int(actual_split / 60), total_steps))
                subprocess.run(
                    [
                        FFMPEG_EXECUTABLE,
                        '-y',
                        '-i',
                        self.metadata['filepath'],
                        '-ss', str(actual_split),
                        '-t', '60',
                        os.path.join(path_tmp, 'transcribe.wav')
                    ]
                )

                r = sr.Recognizer()
                with sr.AudioFile(os.path.join(path_tmp, 'transcribe.wav')) as source:
                    audio = r.record(source)

                language = LANGUAGE_DICT_LIST[self.selected_language].split('-')[0]

                try:
                    final_text += r.recognize_google(audio, language=language)
                except sr.UnknownValueError:
                    print("Google Speech Recognition could not understand audio")
                except sr.RequestError as e:
                    print("Could not request results from Google Speech Recognition service; {0}".format(e))

                actual_split += 60

        if final_text:
            self.text.emit(final_text)


class global_panel_transcription_transcript_preview(QLabel):
    def __init__(widget):
        super().__init__()
        widget.text = ''
        widget.division_type = 'equal'

    def update_type(widget, slice_type):
        widget.division_type = slice_type
        widget.update()

    def update_text(widget, text):
        widget.text = text
        widget.update()

    def paintEvent(widget, event):
        """Function for paintEvent of Timeline"""
        painter = QPainter(widget)
        painter.setRenderHint(QPainter.Antialiasing)

        main_qrect = QRect(
            0,
            0,
            widget.width(),
            widget.height()
        )

        main_qrect -= QMargins(
            10,
            1,
            10,
            1
        )

        painter.setPen(QPen(QColor('#33304251'), 1, Qt.SolidLine))
        painter.setBrush(QColor('#ffffff'))
        painter.drawRoundedRect(main_qrect, 2, 2)

        text_qrect = main_qrect - QMargins(
            8,
            8,
            8,
            8
        )

        painter.setFont(QFont('Ubuntu', 5))
        painter.setBrush(Qt.NoBrush)
        painter.setPen(QColor('#ff304251'))

        if widget.text:
            painter.drawText(text_qrect, Qt.AlignLeft | Qt.AlignTop | Qt.TextWordWrap, widget.text)
            painter.drawText(text_qrect, Qt.AlignLeft | Qt.AlignTop | Qt.TextWordWrap, widget.text)

            painter.setBrush(QColor('#0f1519'))
            painter.setPen(Qt.NoPen)

            timeline_qrect = QRect(
                0,
                (widget.height() - 30) * .75,
                widget.width(),
                34,
            )

            painter.drawRoundedRect(timeline_qrect, 2, 2)

            timeline_qrect -= QMargins(10, 10, -10, 10)

            painter.setPen(QColor('#ff6a7483'))
            painter.setBrush(QColor('#ccb8cee0'))

            if widget.division_type == 'equal':
                ns = 5
                for s in range(ns):
                    painter.setPen(QPen(QColor('#ff6a7483'), 1, Qt.SolidLine))
                    srect = timeline_qrect - QMargins(s * (timeline_qrect.width() / ns), 0, ((ns - 1 - s) * (timeline_qrect.width() / ns) + 1), 0)
                    painter.drawRoundedRect(srect, 2, 2)
                    painter.setPen(QPen(QColor('#ff6a7483'), 5, Qt.SolidLine, Qt.RoundCap))
                    srect -= QMargins(5, 2, 5, 0)
                    painter.drawLine(srect.left(), srect.center().y(), srect.right(), srect.center().y())
            elif widget.division_type == 'phrase':
                ns = 5 if len(widget.text.split('. ')) > 4 else len(widget.text.split('. '))
                tl = len('.'.join(widget.text.split('. ')[:ns]))
                x = 0
                for s in range(ns):
                    painter.setPen(QPen(QColor('#ff6a7483'), 1, Qt.SolidLine))
                    cl = (len(widget.text.split('. ')[s]) / tl) * timeline_qrect.width()
                    srect = timeline_qrect - QMargins(x, 0, timeline_qrect.width() - x - cl + 1, 0)
                    painter.drawRoundedRect(srect, 2, 2)
                    painter.setPen(QPen(QColor('#ff6a7483'), 5, Qt.SolidLine, Qt.RoundCap))
                    srect -= QMargins(5, 2, 5, 0)
                    painter.drawLine(srect.left(), srect.center().y(), srect.right(), srect.center().y())
                    x += cl
            elif widget.division_type == 'words':
                wlist = widget.text.split(' ')
                while('' in wlist):
                    wlist.remove('')
                ns = 15 if len(wlist) > 14 else len(wlist)
                tl = len(' '.join(wlist[:ns])) + (3 * ns)
                x = 0
                for s in range(ns):
                    painter.setPen(QPen(QColor('#ff6a7483'), 1, Qt.SolidLine))
                    cl = ((len(wlist[s]) + 3) / tl) * (timeline_qrect.width() + 50)
                    srect = timeline_qrect - QMargins(x, 0, timeline_qrect.width() - x - cl + 1, 0)
                    painter.drawRoundedRect(srect, 2, 2)
                    painter.setPen(QPen(QColor('#ff6a7483'), 5, Qt.SolidLine, Qt.RoundCap))
                    srect -= QMargins(5, 2, 5, 0)
                    painter.drawLine(srect.left(), srect.center().y(), srect.right(), srect.center().y())
                    x += cl
        else:
            painter.drawText(text_qrect, Qt.AlignCenter | Qt.TextWordWrap, 'No transcription.')

        painter.end()
        event.accept()


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


def read_json_transcribed_subtitles(filename='', transcribed=False):
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



def load_menu(self):
    """Function to load subtitles panel widgets"""
    self.global_panel_transcription_menu_button = QPushButton()
    self.global_panel_transcription_menu_button.setCheckable(True)
    self.global_panel_transcription_menu_button.setProperty('class', 'global_panel_menu')
    self.global_panel_transcription_menu_button.clicked.connect(lambda: global_panel_menu_changed(self))
    self.global_panel_menu.layout().addWidget(self.global_panel_transcription_menu_button)


def global_panel_menu_changed(self):
    self.global_panel_transcription_menu_button.setEnabled(False)
    global_panel.global_panel_menu_changed(self, self.global_panel_transcription_menu_button, self.global_panel_transcription_content)


def load_widgets(self):
    """Function to load subtitles panel widgets"""

    self.global_panel_transcription_content = QWidget()
    self.global_panel_transcription_content.setLayout(QVBoxLayout())
    self.global_panel_transcription_content.layout().setContentsMargins(0, 0, 0, 0)
    self.global_panel_transcription_content.layout().setSpacing(10)

    self.global_panel_transcription_language_combobox = QComboBox()
    self.global_panel_transcription_language_combobox.setProperty('class', 'button')
    self.global_panel_transcription_language_combobox.addItems(LANGUAGE_DESCRIPTIONS)
    self.global_panel_transcription_content.layout().addWidget(self.global_panel_transcription_language_combobox, 0, Qt.AlignLeft)

    self.global_panel_transcription_tabwidget = QTabWidget()

    self.global_panel_transcription_autosubtitle_widget = QWidget()
    self.global_panel_transcription_autosubtitle_widget.setLayout(QVBoxLayout())
    self.global_panel_transcription_autosubtitle_widget.layout().setContentsMargins(10, 10, 10, 10)
    self.global_panel_transcription_autosubtitle_widget.layout().setSpacing(20)

    self.global_panel_transcription_autosubtitle_groupbox = QGroupBox()
    self.global_panel_transcription_autosubtitle_groupbox.setLayout(QHBoxLayout())
    self.global_panel_transcription_autosubtitle_groupbox.layout().setContentsMargins(10, 10, 10, 10)
    self.global_panel_transcription_autosubtitle_groupbox.layout().setSpacing(5)

    self.global_panel_transcription_autosubtitle_button = QPushButton()
    self.global_panel_transcription_autosubtitle_button.setProperty('class', 'button')
    self.global_panel_transcription_autosubtitle_button.clicked.connect(lambda: global_panel_transcription_autosubtitle_button_clicked(self))
    self.global_panel_transcription_autosubtitle_groupbox.layout().addWidget(self.global_panel_transcription_autosubtitle_button)

    self.global_panel_transcription_autosubtitle_label = QLabel()
    self.global_panel_transcription_autosubtitle_label.setProperty('class', 'units_label')
    self.global_panel_transcription_autosubtitle_groupbox.layout().addWidget(self.global_panel_transcription_autosubtitle_label)

    self.global_panel_transcription_autosubtitle_groupbox.layout().addStretch()

    self.global_panel_transcription_autosubtitle_widget.layout().addWidget(self.global_panel_transcription_autosubtitle_groupbox)

    self.global_panel_transcription_autosubtitle_widget.layout().addStretch()

    def global_panel_transcription_autosubtitles_thread_ended(response):
        if 'end' in response:
            if os.path.isfile(os.path.join(path_tmp, 'subtitle.json')):
                final_subtitles = read_json_transcribed_subtitles(filename=os.path.join(path_tmp, 'subtitle.json'), transcribed=True)
                if final_subtitles:
                    self.subtitles_list = final_subtitles
            subtitles_panel.update_processing_status(self, show_widgets=False, value=0)
            self.global_panel_transcription_autosubtitle_button.setEnabled(True)
            player.update_timelines(self)

    self.global_panel_transcription_autosubtitles_thread = global_panel_transcription_autosubtitles_thread(self)
    self.global_panel_transcription_autosubtitles_thread.response.connect(global_panel_transcription_autosubtitles_thread_ended)

    self.global_panel_transcription_tabwidget.addTab(self.global_panel_transcription_autosubtitle_widget, 'Autosubtitle')

    self.global_panel_transcription_transcript_widget = QWidget()
    self.global_panel_transcription_transcript_widget.setLayout(QHBoxLayout())
    self.global_panel_transcription_transcript_widget.layout().setContentsMargins(10, 10, 10, 10)
    self.global_panel_transcription_transcript_widget.layout().setSpacing(20)

    self.global_panel_transcription_transcript_column = QVBoxLayout()
    self.global_panel_transcription_transcript_column.setContentsMargins(0, 0, 0, 0)

    self.global_panel_transcription_transcript_groupbox = QGroupBox()
    self.global_panel_transcription_transcript_groupbox.setLayout(QHBoxLayout())
    self.global_panel_transcription_transcript_groupbox.layout().setContentsMargins(10, 10, 10, 10)
    self.global_panel_transcription_transcript_groupbox.layout().setSpacing(5)

    def global_panel_transcription_transcript_thread_text_emmited(result):
        self.global_panel_transcription_transcript_preview.update_text(text=result)
        self.global_panel_transcription_transcript_button.setVisible(True)
        self.global_panel_transcription_transcript_progress.setVisible(False)
        self.global_panel_transcription_transcript_apply_transcript_button.setVisible(True)

    def global_panel_transcription_transcript_thread_result_emmited(result):
        if '/' in result:
            self.global_panel_transcription_transcript_button.setVisible(False)
            self.global_panel_transcription_transcript_progress.setVisible(True)
            self.global_panel_transcription_transcript_progress.setMaximum(int(result.split('/')[1]))
            self.global_panel_transcription_transcript_progress.setValue(int(result.split('/')[0]))

    self.global_panel_transcription_transcript_thread = global_panel_transcription_transcript_thread()
    self.global_panel_transcription_transcript_thread.result.connect(lambda: global_panel_transcription_transcript_thread_result_emmited())
    self.global_panel_transcription_transcript_thread.text.connect(lambda: global_panel_transcription_transcript_thread_text_emmited())

    self.global_panel_transcription_transcript_button = QPushButton()
    self.global_panel_transcription_transcript_button.setProperty('class', 'button')
    self.global_panel_transcription_transcript_button.clicked.connect(lambda: global_panel_transcription_transcript_button_clicked(self))
    self.global_panel_transcription_transcript_groupbox.layout().addWidget(self.global_panel_transcription_transcript_button)

    self.global_panel_transcription_transcript_progress = QProgressBar()
    self.global_panel_transcription_transcript_progress.setVisible(False)
    self.global_panel_transcription_transcript_groupbox.layout().addWidget(self.global_panel_transcription_transcript_progress)

    self.global_panel_transcription_transcript_groupbox.layout().addStretch()

    self.global_panel_transcription_transcript_column.addWidget(self.global_panel_transcription_transcript_groupbox)

    self.global_panel_transcription_transcript_column.addStretch()

    self.global_panel_transcription_transcript_widget.layout().addLayout(self.global_panel_transcription_transcript_column)

    self.global_panel_transcription_transcript_preview_column = QVBoxLayout()
    self.global_panel_transcription_transcript_preview_column.setContentsMargins(0, 0, 0, 0)
    self.global_panel_transcription_transcript_preview_column.setSpacing(0)

    self.global_panel_transcription_transcript_preview = global_panel_transcription_transcript_preview()
    self.global_panel_transcription_transcript_preview.setFixedSize(QSize(200, 150))

    self.global_panel_transcription_transcript_preview_column.addWidget(self.global_panel_transcription_transcript_preview)

    self.global_panel_transcription_transcript_preview_column.addSpacing(10)

    self.global_panel_transcription_transcript_slice_label = QLabel()
    self.global_panel_transcription_transcript_slice_label.setProperty('class', 'widget_label')
    self.global_panel_transcription_transcript_preview_column.addWidget(self.global_panel_transcription_transcript_slice_label)

    self.global_panel_transcription_transcript_preview_column.addSpacing(2)

    self.global_panel_transcription_transcript_slice_combobox = QComboBox()
    self.global_panel_transcription_transcript_slice_combobox.activated.connect(lambda: global_panel_transcription_transcript_slice_combobox_activated(self))
    self.global_panel_transcription_transcript_preview_column.addWidget(self.global_panel_transcription_transcript_slice_combobox)

    self.global_panel_transcription_transcript_preview_column.addSpacing(10)

    self.global_panel_transcription_transcript_apply_transcript_button = QPushButton()
    self.global_panel_transcription_transcript_apply_transcript_button.setProperty('class', 'button')
    self.global_panel_transcription_transcript_apply_transcript_button.setVisible(False)
    self.global_panel_transcription_transcript_apply_transcript_button.clicked.connect(lambda: global_panel_transcription_transcript_apply_transcript_button_clicked(self))
    self.global_panel_transcription_transcript_preview_column.layout().addWidget(self.global_panel_transcription_transcript_apply_transcript_button)

    self.global_panel_transcription_transcript_preview_column.addStretch()

    self.global_panel_transcription_transcript_widget.layout().addLayout(self.global_panel_transcription_transcript_preview_column)

    self.global_panel_transcription_tabwidget.addTab(self.global_panel_transcription_transcript_widget, 'Transcript')

    self.global_panel_transcription_content.layout().addWidget(self.global_panel_transcription_tabwidget)

    self.global_panel_content_stacked_widgets.addWidget(self.global_panel_transcription_content)


def global_subtitlesvideo_autosync_button_clicked(self):
    """Function to run autosync"""
    run_command = False

    if bool(self.subtitles_list):
        are_you_sure_message = QMessageBox(self)
        are_you_sure_message.setWindowTitle('Are you sure?')
        are_you_sure_message.setText('This will overwrite your actual subtitle set. New timings will be applied. Are you sure you want to replace your actual subtitles?')
        are_you_sure_message.addButton('Yes', QMessageBox.AcceptRole)
        are_you_sure_message.addButton('No', QMessageBox.RejectRole)
        ret = are_you_sure_message.exec_()

        if ret == 0:
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


def global_panel_transcription_autosubtitle_button_clicked(self):
    """Function to run autosub"""
    run_command = False

    if bool(self.subtitles_list):
        are_you_sure_message = QMessageBox(self)
        are_you_sure_message.setWindowTitle('Are you sure?')
        are_you_sure_message.setText('This will overwrite your actual subtitle set. New timings will be applied. Are you sure you want to replace your actual subtitles?')
        are_you_sure_message.addButton('Yes', QMessageBox.AcceptRole)
        are_you_sure_message.addButton('No', QMessageBox.RejectRole)
        ret = are_you_sure_message.exec_()

        if ret == 0:
            run_command = True
    else:
        run_command = True

    if run_command:

        language = LANGUAGE_DICT_LIST[self.global_panel_transcription_language_combobox.currentText()]

        self.global_panel_transcription_autosubtitles_thread.original_file = self.video_metadata['filepath']
        self.global_panel_transcription_autosubtitles_thread.language = language
        self.global_panel_transcription_autosubtitles_thread.start()

        subtitles_panel.update_processing_status(self, show_widgets=True, value=33)
        self.global_panel_transcription_autosubtitle_button.setEnabled(False)


def global_panel_transcription_transcript_apply_transcript_button_clicked(self):
    """Function to transcribe using google speech"""
    run_command = False

    if bool(self.subtitles_list):
        are_you_sure_message = QMessageBox(self)
        are_you_sure_message.setWindowTitle(_('alert.are_you_sure'))
        are_you_sure_message.setText(_('alert.overwrite_warning'))
        are_you_sure_message.addButton('Yes', QMessageBox.AcceptRole)
        are_you_sure_message.addButton('No', QMessageBox.RejectRole)
        ret = are_you_sure_message.exec_()

        if ret == 0:
            run_command = True
    else:
        run_command = True

    if run_command and self.global_panel_transcription_transcript_preview.text:
        if self.global_panel_transcription_transcript_slice_combobox.currentIndex() == 0:
            self.subtitles_list = []
            ns = len(self.global_panel_transcription_transcript_preview.text.split('. '))
            ts = self.video_metadata['duration'] / ns
            c = 0.0
            for sub in self.global_panel_transcription_transcript_preview.text.split('. '):
                self.subtitles_list.append([c, ts, sub + '.'])
                c += ts
        elif self.global_panel_transcription_transcript_slice_combobox.currentIndex() == 1:
            self.subtitles_list = []
            ns = len(self.global_panel_transcription_transcript_preview.text)
            c = 0.0
            for sub in self.global_panel_transcription_transcript_preview.text.split('. '):
                ts = (len(sub + '.') / ns) * self.video_metadata['duration']
                self.subtitles_list.append([c, ts, sub + '.'])
                c += ts
        elif self.global_panel_transcription_transcript_slice_combobox.currentIndex() == 2:
            self.subtitles_list = []
            ns = len(self.global_panel_transcription_transcript_preview.text)
            c = 0.0
            for sub in self.global_panel_transcription_transcript_preview.text.split(' '):
                ts = (len(sub + ' ') / ns) * self.video_metadata['duration']
                self.subtitles_list.append([c, ts, sub])
                c += ts


def global_panel_transcription_transcript_button_clicked(self):
    self.global_panel_transcription_transcript_thread.metadata = self.video_metadata
    self.global_panel_transcription_transcript_thread.selected_language = self.global_panel_transcription_language_combobox.currentText()
    self.global_panel_transcription_transcript_thread.start()


def global_panel_transcription_transcript_slice_combobox_activated(self):
    if self.global_panel_transcription_transcript_slice_combobox.currentText() == 'Equal size':
        self.global_panel_transcription_transcript_preview.update_type('equal')
    elif self.global_panel_transcription_transcript_slice_combobox.currentText() == 'Phrase size':
        self.global_panel_transcription_transcript_preview.update_type('phrases')
    elif self.global_panel_transcription_transcript_slice_combobox.currentText() == 'Words':
        self.global_panel_transcription_transcript_preview.update_type('words')


def translate_widgets(self):
    self.global_panel_transcription_menu_button.setText(_('global_panel_transcription.title'))
    self.global_panel_transcription_autosubtitle_groupbox.setTitle(_('global_panel_transcription.google_web_speech_public_api'))
    self.global_panel_transcription_autosubtitle_button.setText(_('global_panel_transcription.auto_subtitle'))
    self.global_panel_transcription_autosubtitle_label.setText(_('global_panel_transcription.warning_overwrite'))
    self.global_panel_transcription_transcript_groupbox.setTitle(_('global_panel_transcription.google_web_speech_public_api'))
    self.global_panel_transcription_transcript_button.setText(_('global_panel_transcription.transcribe'))
    self.global_panel_transcription_transcript_slice_label.setText(_('global_panel_transcription.slicing_and_timing'))
    self.global_panel_transcription_transcript_slice_combobox.clear()
    self.global_panel_transcription_transcript_slice_combobox.addItems([
        _('global_panel_transcription.slice_combobox.equal_size'),
        _('global_panel_transcription.slice_combobox.phrase_size'),
        _('global_panel_transcription.slice_combobox.words')
    ])
    self.global_panel_transcription_transcript_apply_transcript_button.setText(_('global_panel_transcription.slice_to_subtitles'))
