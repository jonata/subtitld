#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import datetime
import numpy
import pycaption
from pycaption.exceptions import CaptionReadSyntaxError
import chardet

from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import QThread, pyqtSignal

from modules import waveform
from modules.paths import LIST_OF_SUPPORTED_SUBTITLE_EXTENSIONS, LIST_OF_SUPPORTED_VIDEO_EXTENSIONS

from scenedetect.video_manager import VideoManager
from scenedetect.scene_manager import SceneManager
from scenedetect.stats_manager import StatsManager
from scenedetect.detectors import ContentDetector

list_of_supported_subtitle_extensions = []
for type in LIST_OF_SUPPORTED_SUBTITLE_EXTENSIONS.keys():
    for ext in LIST_OF_SUPPORTED_SUBTITLE_EXTENSIONS[type]['extensions']:
        list_of_supported_subtitle_extensions.append(ext)


class thread_extract_scene_time_positions(QThread):
    command = pyqtSignal(list)
    filepath = ''

    def run(self):
        if self.filepath:
            result = []
            video_manager = VideoManager([self.filepath])
            stats_manager = StatsManager()
            scene_manager = SceneManager(stats_manager)
            scene_manager.add_detector(ContentDetector())
            base_timecode = video_manager.get_base_timecode()
            try:
                video_manager.set_downscale_factor()
                video_manager.start()
                scene_manager.detect_scenes(frame_source=video_manager, show_progress=False)
                scene_list = scene_manager.get_scene_list(base_timecode)
                for i, scene in enumerate(scene_list):
                    result.append(scene[0].get_seconds())
            finally:
                video_manager.release()
            self.command.emit(result)


class thread_extract_waveform(QThread):
    command = pyqtSignal(numpy.ndarray)
    filepath = ''
    audio = ''
    duration = ''
    width = ''
    height = ''

    def run(self):
        if self.filepath:
            result = waveform.ffmpeg_load_audio(filepath=self.filepath)
            self.command.emit(result)


def load(self):
    def thread_extract_waveform_ended(command):
        self.video_metadata['audio'] = command
        self.timeline.zoom_update_waveform(self)
        self.videoinfo_label.setText(self.tr('Audio ffmpeg_extract_subtitleed'))

    self.thread_extract_waveform = thread_extract_waveform(self)
    self.thread_extract_waveform.command.connect(thread_extract_waveform_ended)

    def thread_extract_scene_time_positions_ended(command):
        self.video_metadata['scenes'] = command

    self.thread_extract_scene_time_positions = thread_extract_scene_time_positions(self)
    self.thread_extract_scene_time_positions.command.connect(thread_extract_scene_time_positions_ended)


def open_filepath(self, file_to_open=False):
    supported_subtitle_files = self.tr('Subtitle files') + ' ({})'.format(" ".join(["*.{}".format(fo) for fo in list_of_supported_subtitle_extensions]))
    supported_video_files = self.tr('Video files') + ' ({})'.format(" ".join(["*{}".format(fo) for fo in LIST_OF_SUPPORTED_VIDEO_EXTENSIONS]))
    if not file_to_open:
        file_to_open = QFileDialog.getOpenFileName(parent=self.parent(), caption=self.tr('Select the video or subtitle file'), directory=os.path.expanduser("~"), filter=supported_subtitle_files + ';;' + supported_video_files, options=QFileDialog.DontUseNativeDialog)[0]

    if file_to_open and os.path.isfile(file_to_open):
        if file_to_open.lower().endswith(tuple(list_of_supported_subtitle_extensions)):
            self.subtitles_list, self.format_to_save = process_subtitles_file(file_to_open)
            self.actual_subtitle_file = file_to_open

        elif file_to_open.lower().endswith(LIST_OF_SUPPORTED_VIDEO_EXTENSIONS):
            self.video_metadata = process_video_file(file_to_open)

        if not self.video_metadata and self.subtitles_list:
            for filename in os.listdir(os.path.dirname(file_to_open)):
                if filename.rsplit('.', 1)[0] == os.path.basename(file_to_open).rsplit('.', 1)[0] and filename.endswith(LIST_OF_SUPPORTED_VIDEO_EXTENSIONS):
                    self.video_metadata = process_video_file(os.path.join(os.path.dirname(file_to_open), filename))
                    break

        elif self.video_metadata and not self.subtitles_list:
            for filename in os.listdir(os.path.dirname(file_to_open)):
                if filename.rsplit('.', 1)[0] == os.path.basename(file_to_open).rsplit('.', 1)[0] and filename.endswith(tuple(list_of_supported_subtitle_extensions)):
                    self.subtitles_list, self.format_to_save = process_subtitles_file(os.path.join(os.path.dirname(file_to_open), filename))
                    self.actual_subtitle_file = os.path.join(os.path.dirname(file_to_open), filename)
                    break

    if not self.video_metadata:
        file_to_open = QFileDialog.getOpenFileName(parent=self.parent(), caption=self.tr('Select the video file'), directory=os.path.expanduser("~"), filter=supported_video_files, options=QFileDialog.DontUseNativeDialog)[0]
        if file_to_open and os.path.isfile(file_to_open) and file_to_open.lower().endswith(LIST_OF_SUPPORTED_VIDEO_EXTENSIONS):
            self.video_metadata = process_video_file(file_to_open)

    if self.video_metadata:
        self.actual_video_file = file_to_open
        self.thread_extract_waveform.filepath = self.video_metadata['filepath']
        self.thread_extract_waveform.start()
        self.videoinfo_label.setText(self.tr('Extracting audio...'))
        self.thread_extract_scene_time_positions.filepath = self.video_metadata['filepath']
        self.thread_extract_scene_time_positions.start()
        self.player.update(self)
        self.player_widget.loadfile(self.video_metadata['filepath'])
        self.player.resize_player_widget(self)
        if not self.actual_subtitle_file:
            if self.video_metadata.get('subttiles', ''):
                self.subtitles_list, self.format_to_save = process_subtitles_file(self.video_metadata['subttiles'])
        self.subtitleslist.update_subtitles_list_widget(self)
        self.timeline.update_timeline(self)
        self.startscreen.hide(self)
        self.playercontrols.show(self)
        self.properties.show(self)
        self.subtitleslist.show(self)
        self.global_subtitlesvideo_panel.hide_global_subtitlesvideo_panel(self)
        self.global_properties_panel.hide_global_properties_panel(self)
        self.settings['recent_files'][file_to_open] = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        self.autosave_timer.start()
    self.global_subtitlesvideo_panel.update_global_subtitlesvideo_save_as_combobox(self)


def process_subtitles_file(subtitle_file=False, format='SRT'):
    final_subtitles = []

    if subtitle_file and os.path.isfile(subtitle_file):
        if subtitle_file.lower().endswith(('.srt')):
            with open(subtitle_file, encoding='utf-8') as srt_file:
                srt_content = srt_file.read()

                if ' -> ' in srt_content:
                    srt_content = srt_content.replace(' -> ', ' --> ')

                srt_reader = pycaption.SRTReader().read(srt_content)
                for caption in srt_reader.get_captions(list(srt_reader._captions.keys())[0]):
                    final_subtitles.append([caption.start/1000000, (caption.end/1000000) - caption.start/1000000, caption.get_text()])

        elif subtitle_file.lower().endswith(('.vtt', '.webvtt')):
            format = 'VTT'
            with open(subtitle_file, encoding='utf-8') as vtt_file:
                try:
                    vtt_reader = pycaption.WebVTTReader().read(vtt_file.read())
                    for caption in vtt_reader.get_captions(list(vtt_reader._captions.keys())[0]):
                        final_subtitles.append([caption.start/1000000, (caption.end/1000000) - caption.start/1000000, caption.get_text()])
                except CaptionReadSyntaxError:
                    import pysubs2
                    with open(subtitle_file, encoding='utf-8') as f:
                        subfile = pysubs2.SSAFile.from_string(f.read())

                    for event in subfile.events:
                        start = event.start / 1000.0
                        duration = event.duration / 1000.0
                        text = event.plaintext
                        final_subtitles.append([start, duration, text])

                    # error_message = QMessageBox()
                    # error_message.setWindowTitle(self.tr('There is a problem with this file and can not be opened.'))

        elif subtitle_file.lower().endswith(('.ttml', '.dfxp')):
            format = 'DFXP'
            with open(subtitle_file, encoding='utf-8') as dfxp_file:
                dfxp_reader = pycaption.DFXPReader().read(dfxp_file.read())
                for caption in dfxp_reader.get_captions(list(dfxp_reader._captions.keys())[0]):
                    final_subtitles.append([caption.start/1000000, (caption.end/1000000) - caption.start/1000000, caption.get_text()])

        elif subtitle_file.lower().endswith(('.smi', '.sami')):
            format = 'SAMI'
            with open(subtitle_file, encoding='utf-8') as sami_file:
                sami_reader = pycaption.SAMIReader().read(sami_file.read())
                for caption in sami_reader.get_captions(list(sami_reader._captions.keys())[0]):
                    final_subtitles.append([caption.start/1000000, (caption.end/1000000) - caption.start/1000000, caption.get_text()])

        elif subtitle_file.lower().endswith(('.sbv')):
            format = 'SBV'
            from captionstransformer.sbv import Reader as sbv_reader
            with open(subtitle_file, encoding='utf-8') as sbv_file:
                captions = sbv_reader(sbv_file).read()
                for caption in captions:
                    final_subtitles.append([(caption.start-datetime.datetime(1900, 1, 1)).total_seconds(), caption.duration.total_seconds(), caption.text])

        elif subtitle_file.lower().endswith(('.xml')):
            format = 'XML'
            if '<transcript>' in open(subtitle_file).read():
                from captionstransformer.transcript import Reader as transcript_reader
                import html
                with open(subtitle_file, encoding='utf-8') as xml_file:
                    captions = transcript_reader(xml_file).read()
                    for caption in captions:
                        final_subtitles.append([(caption.start-datetime.datetime(1900, 1, 1)).total_seconds(), caption.duration.total_seconds(), html.unescape(caption.text)])

        elif subtitle_file.lower().endswith(('.ass', '.ssa', '.sub')):
            import pysubs2

            if subtitle_file.lower().endswith(('.ass', '.ssa')):
                format = 'ASS'
                with open(subtitle_file, encoding='utf-8') as f:
                    subfile = pysubs2.SSAFile.from_string(f.read())
            elif subtitle_file.lower().endswith(('.sub')):
                format = 'SUB'
                enc = chardet.detect(open(subtitle_file, 'rb').read())['encoding']
                subfile = pysubs2.SSAFile.from_string(open(subtitle_file, mode='rb').read().decode(enc, 'ignore'))

            for event in subfile.events:
                start = event.start / 1000.0
                duration = event.duration / 1000.0
                text = event.plaintext
                final_subtitles.append([start, duration, text])

        elif subtitle_file.lower().endswith(('.scc')):
            format = 'SCC'
            import scc2srt
            final_subtitles = scc2srt.get_list_of_captions(subtitle_file)

    return final_subtitles, format


def process_video_file(video_file=False):
    video_metadata = {}
    json_result = waveform.ffmpeg_load_metadata(video_file)
    video_metadata['audio'] = False
    video_metadata['waveform'] = {}
    video_metadata['duration'] = float(json_result.get('format', {}).get('duration', '0.01'))
    for stream in json_result.get('streams', []):
        if stream.get('codec_type', '') == 'video' and not stream.get('codec_name', 'png') in ['png', 'mjpeg']:
            video_metadata['width'] = int(stream.get('width', 640))
            video_metadata['height'] = int(stream.get('height', 480))
            video_metadata['framerate'] = int(stream.get('r_frame_rate', '1/30').split('/', 1)[0])/int(stream.get('r_frame_rate', '1/30').split('/', 1)[-1])
        elif stream.get('codec_type', '') in ['subtitle'] and not video_metadata.get('subttiles', False):
            video_metadata['subttiles'] = waveform.ffmpeg_extract_subtitle(video_file, stream.get('index', 2))
            # TODO: select what language if multiple embedded subtitles
    video_metadata['filepath'] = video_file
    video_metadata['scenes'] = []
    return video_metadata


def import_file(filename=False, format=False, fit_to_length=False, length=.01, distribute_fixed_duration=False):
    final_subtitles = []
    if filename:
        if filename.lower().endswith(('.txt')):
            from cleantext import clean

            format = 'TXT'
            with open(filename) as txt_file:
                # clean("some input",
                #     fix_unicode=True,               # fix various unicode errors
                #     to_ascii=True,                  # transliterate to closest ASCII representation
                #     lower=True,                     # lowercase text
                #     no_line_breaks=False,           # fully strip line breaks as opposed to only normalizing them
                #     no_urls=False,                  # replace all URLs with a special token
                #     no_emails=False,                # replace all email addresses with a special token
                #     no_phone_numbers=False,         # replace all phone numbers with a special token
                #     no_numbers=False,               # replace all numbers with a special token
                #     no_digits=False,                # replace all digits with a special token
                #     no_currency_symbols=False,      # replace all currency symbols with a special token
                #     no_punct=False,                 # fully remove punctuation
                #     replace_with_url="<URL>",
                #     replace_with_email="<EMAIL>",
                #     replace_with_phone_number="<PHONE>",
                #     replace_with_number="<NUMBER>",
                # replace_with_digit="0",
                # replace_with_currency_symbol="<CUR>",
                # lang="en"                       # set to 'de' for German special handling
                # )

                txt_content = clean(txt_file.read())
                pos = 0.0
                for phrase in txt_content.split('. '):
                    final_subtitles.append([pos, 5.0, phrase + '.'])
                    pos += 5.0
        elif filename.lower().endswith(('.srt')):
            format = 'SRT'
            final_subtitles += process_subtitles_file(subtitle_file=filename, format=format)[0]

    return final_subtitles, format


def export_file(filename=False, subtitles_list=False, format='TXT', options=False):
    if subtitles_list and filename:
        if format == 'TXT':
            final_txt = ''
            for sub in subtitles_list:
                final_txt += sub[2].replace('\n', ' ') + ' '
            if options:
                if options.get('new_line', False):
                    final_txt = final_txt.replace('. ', '.\n')
                    final_txt = final_txt.replace('! ', '!\n')
                    final_txt = final_txt.replace('? ', '?\n')
            with open(filename, mode='w', encoding='utf-8') as txt_file:
                txt_file.write(final_txt)


def save_file(final_file, subtitles_list, format='SRT', language='en'):
    if subtitles_list:
        # if not final_file.lower().endswith('.' + format.lower()):
        #     final_file += '.' + format.lower()

        if format in ['SRT', 'DFXP', 'SAMI', 'SCC', 'VTT']:
            captions = pycaption.CaptionList()
            for sub in subtitles_list:
                # skip extra blank lines
                nodes = [pycaption.CaptionNode.create_text(sub[2])]
                caption = pycaption.Caption(start=sub[0]*1000000, end=(sub[0] + sub[1])*1000000, nodes=nodes)
                captions.append(caption)
            caption_set = pycaption.CaptionSet({language: captions})

            if format == 'SRT':
                open(final_file, mode='w', encoding='utf-8').write(pycaption.SRTWriter().write(caption_set))
            elif format == 'DFXP':
                open(final_file, mode='w', encoding='utf-8').write(pycaption.DFXPWriter().write(caption_set))
            elif format == 'SAMI':
                open(final_file, mode='w', encoding='utf-8').write(pycaption.SAMIWriter().write(caption_set))
            elif format == 'SCC':
                open(final_file, mode='w', encoding='utf-8').write(pycaption.SCCWriter().write(caption_set))
            elif format == 'VTT':
                open(final_file, mode='w', encoding='utf-8').write(pycaption.WebVTTWriter().write(caption_set))

        elif format in ['ASS', 'SBV', 'XML', 'SUB']:
            if format in ['ASS', 'SUB']:
                import pysubs2
                assfile = pysubs2.SSAFile()
                index = 0
                for sub in reversed(sorted(subtitles_list)):
                    assfile.insert(index, pysubs2.SSAEvent(start=int(sub[0]*1000), end=int((sub[0]*1000)+(sub[1]*1000)), text=sub[2].replace('\n', ' ')))
                if format == 'SUB':
                    assfile.save(final_file, format='microdvd')
                else:
                    assfile.save(final_file)
            else:
                from captionstransformer.core import Caption, get_date

                if format == 'SBV':
                    from captionstransformer.sbv import Writer
                elif format == 'XML':
                    from captionstransformer.transcript import Writer

                writer = Writer(final_file)
                captions = []
                for caption in subtitles_list:
                    c = Caption()
                    c.start = get_date(second=caption[0])
                    c.duration = get_date(second=caption[1])
                    c.text = caption[2]
                    captions.append(c)
                writer.set_captions(captions)
                writer.write()
