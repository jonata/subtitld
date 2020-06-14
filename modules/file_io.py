#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import datetime
import numpy
import pycaption
import subprocess
import pysubs2
from cleantext import clean

from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import QThread, pyqtSignal

from modules import waveform
from modules.paths import STARTUPINFO, FFMPEG_EXECUTABLE, LIST_OF_SUPPORTED_SUBTITLE_EXTENSIONS, LIST_OF_SUPPORTED_VIDEO_EXTENSIONS, LIST_OF_SUPPORTED_IMPORT_EXTENSIONS


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
            command = [
                FFMPEG_EXECUTABLE,
                '-i', self.filepath,
                '-vf', "select='gt(scene,0.4)',showinfo",
                '-f', 'null',
                '-']
            p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, startupinfo=STARTUPINFO)
            for line in p.stdout.read().decode().split('\n'):
                if line.startswith(('[')) and 'pts_time:' in line:
                    result.append(float(line.split('pts_time:', 1)[-1].split(' ', 1)[0]))

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
        self.videoinfo_label.setText('Audio extracted')

    self.thread_extract_waveform = thread_extract_waveform(self)
    self.thread_extract_waveform.command.connect(thread_extract_waveform_ended)

    def thread_extract_scene_time_positions_ended(command):
        self.video_metadata['scenes'] = command

    self.thread_extract_scene_time_positions = thread_extract_scene_time_positions(self)
    self.thread_extract_scene_time_positions.command.connect(thread_extract_scene_time_positions_ended)


def open_filepath(self, file_to_open=False):
    supported_subtitle_files = "Subtitle files ({})".format(" ".join(["*.{}".format(fo) for fo in list_of_supported_subtitle_extensions]))
    supported_video_files = "Video files ({})".format(" ".join(["*{}".format(fo) for fo in LIST_OF_SUPPORTED_VIDEO_EXTENSIONS]))
    if not file_to_open:
        file_to_open = QFileDialog.getOpenFileName(self, "Select the video or subtitle file", os.path.expanduser("~"), supported_subtitle_files + ';;' + supported_video_files)[0]

    if file_to_open and os.path.isfile(file_to_open) and file_to_open.lower().endswith(tuple(list_of_supported_subtitle_extensions)):
        self.subtitles_list, self.format_to_save = process_subtitles_file(file_to_open)
        self.actual_subtitle_file = file_to_open

    elif file_to_open and os.path.isfile(file_to_open) and file_to_open.lower().endswith(LIST_OF_SUPPORTED_VIDEO_EXTENSIONS):
        self.video_metadata = process_video_file(file_to_open)

    if not self.video_metadata:
        file_to_open = QFileDialog.getOpenFileName(self, "Select the video file", os.path.expanduser("~"), supported_video_files)[0]
        if file_to_open and os.path.isfile(file_to_open) and file_to_open.lower().endswith(LIST_OF_SUPPORTED_VIDEO_EXTENSIONS):
            self.video_metadata = process_video_file(file_to_open)

    if self.video_metadata:
        self.actual_video_file = file_to_open
        self.thread_extract_waveform.filepath = self.video_metadata['filepath']
        self.thread_extract_waveform.start()
        self.videoinfo_label.setText('Extracting audio...')
        self.thread_extract_scene_time_positions.filepath = self.video_metadata['filepath']

        self.player.update(self)
        self.player_widget.mpv.play(self.video_metadata['filepath'])
        self.player_widget.mpv.wait_for_property('seekable')
        self.player_widget.mpv.pause = True
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
        # if self.advanced_mode:
        #    self.global_subtitlesvideo_panel.hide_global_subtitlesvideo_panel(self)
        #    self.global_properties_panel.hide_global_properties_panel(self)

        self.settings['recent_files'][file_to_open] = datetime.datetime.now().strftime("%Y%m%d")
    self.global_subtitlesvideo_panel.update_global_subtitlesvideo_save_as_combobox(self)


def process_subtitles_file(subtitle_file=False, format=False):
    final_subtitles = []

    if subtitle_file.lower().endswith('.srt'):
        format = 'SRT'
        with open(subtitle_file) as srt_file:
            srt_content = srt_file.read()

            if ' -> ' in srt_content:
                srt_content = srt_content.replace(' -> ', ' --> ')

            srt_reader = pycaption.SRTReader().read(srt_content)
            for caption in srt_reader.get_captions(list(srt_reader._captions.keys())[0]):
                final_subtitles.append([caption.start/1000000, (caption.end/1000000) - caption.start/1000000, caption.get_text()])

    elif subtitle_file.lower().endswith(('.vtt', '.webvtt')):
        format = 'VTT'
        with open(subtitle_file) as vtt_file:
            vtt_reader = pycaption.WebVTTReader().read(vtt_file.read())
            for caption in vtt_reader.get_captions(list(vtt_reader._captions.keys())[0]):
                final_subtitles.append([caption.start/1000000, (caption.end/1000000) - caption.start/1000000, caption.get_text()])

    elif subtitle_file.lower().endswith(('.ttml', '.dfxp')):
        format = 'DFXP'
        with open(subtitle_file) as dfxp_file:
            dfxp_reader = pycaption.DFXPReader().read(dfxp_file.read())
            for caption in dfxp_reader.get_captions(list(dfxp_reader._captions.keys())[0]):
                final_subtitles.append([caption.start/1000000, (caption.end/1000000) - caption.start/1000000, caption.get_text()])

    elif subtitle_file.lower().endswith(('.sbv')):
        format = 'SBV'
        from captionstransformer.sbv import Reader as sbv_reader
        captions = sbv_reader(open(subtitle_file)).read()
        for caption in captions:
            final_subtitles.append([(caption.start-datetime.datetime(1900, 1, 1)).total_seconds(), caption.duration.total_seconds(), caption.text])

    elif subtitle_file.lower().endswith(('.smi', '.sami')):
        format = 'SAMI'
        with open(subtitle_file) as sami_file:
            sami_reader = pycaption.SAMIReader().read(sami_file.read())
            for caption in sami_reader.get_captions(list(sami_reader._captions.keys())[0]):
                final_subtitles.append([caption.start/1000000, (caption.end/1000000) - caption.start/1000000, caption.get_text()])

    elif subtitle_file.lower().endswith(('.scc')):
        format = 'SCC'
        import scc2srt
        final_subtitles = scc2srt.get_list_of_captions(subtitle_file)

    elif subtitle_file.lower().endswith(('.xml')):
        format = 'XML'
        if '<transcript>' in open(subtitle_file).read():
            from captionstransformer.transcript import Reader as transcript_reader
            import html
            captions = transcript_reader(open(subtitle_file)).read()
            for caption in captions:
                final_subtitles.append([(caption.start-datetime.datetime(1900, 1, 1)).total_seconds(), caption.duration.total_seconds(), html.unescape(caption.text)])

    elif subtitle_file.lower().endswith(('.ass', '.ssa')):
        fomat = 'ASS'
        with open(subtitle_file) as f:
            ssafile = pysubs2.SSAFile.from_string(f.read())
            for event in ssafile.events:
                start = event.start / 1000.0
                duration = event.duration / 1000.0
                text = event.plaintext
                final_subtitles.append([start, duration, text])

    return final_subtitles, format


def process_video_file(video_file=False):
    video_metadata = {}
    json_result = waveform.ffmpeg_load_metadata(video_file)
    video_metadata['audio'] = False
    video_metadata['waveform'] = {}
    video_metadata['duration'] = float(json_result.get('format', {}).get('duration', '0.01'))
    for stream in json_result.get('streams', []):
        if stream.get('codec_type', '') == 'video' and not stream.get('codec_name', 'png') == 'png':
            video_metadata['width'] = int(stream.get('width', 640))
            video_metadata['height'] = int(stream.get('height', 480))
            video_metadata['framerate'] = int(stream.get('time_base', '1/30').split('/', 1)[-1])
        elif stream.get('codec_type', '') == 'subtitle':
            video_metadata['subttiles'] = waveform.ffmpeg_extract_subtitle(video_file, stream.get('index', 2))
    video_metadata['filepath'] = video_file
    video_metadata['scenes'] = []
    return video_metadata


def import_file(filename=False, format=False, fit_to_length=False, length=.01, distribute_fixed_duration=False):
    final_subtitles = []
    if filename:
        if filename.lower().endswith(('.txt')):
            format = 'TXT'
            with open(filename) as txt_file:
                txt_content = clean(txt_file.read())
                pos = 0.0
                for phrase in txt_content.split('. '):
                    final_subtitles.append([pos, 5.0, phrase + '.'])
                    pos += 5.0
    return final_subtitles, format


def export_file(filename=False, subtitles_list=False, format='TXT'):
    if subtitles_list and filename:
        if format == 'TXT':
            final_txt = ''
            for sub in subtitles_list:
                final_txt += sub[2].replace('\n', ' ') + ' '
            with open(filename, 'w') as txt_file:
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
                open(final_file, 'w').write(pycaption.SRTWriter().write(caption_set))
            elif format == 'DFXP':
                open(final_file, 'w').write(pycaption.DFXPWriter().write(caption_set))
            elif format == 'SAMI':
                open(final_file, 'w').write(pycaption.SAMIWriter().write(caption_set))
            elif format == 'SCC':
                open(final_file, 'w').write(pycaption.SCCWriter().write(caption_set))
            elif format == 'VTT':
                open(final_file, 'w').write(pycaption.WebVTTWriter().write(caption_set))

        elif format in ['ASS', 'SBV', 'XML']:
            if format == 'ASS':
                assfile = pysubs2.SSAFile()
                index = 0
                for sub in subtitles_list:
                    assfile.insert(index, pysubs2.SSAEvent(start=int(sub[0]*1000), duration=int(sub[1]*1000), text=sub[2]))
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
