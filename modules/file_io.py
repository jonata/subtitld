#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import datetime
import numpy
import ass
import re
import pycaption
import subprocess

from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import QThread, pyqtSignal

from modules import waveform
from modules.paths import STARTUPINFO, FFMPEG_EXECUTABLE, LIST_OF_SUPPORTED_SUBTITLE_EXTENSIONS, LIST_OF_SUPPORTED_VIDEO_EXTENSIONS


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
    if not file_to_open:
        supported_subtitle_files = "Subtitle files ({})".format(" ".join(["*{}".format(fo) for fo in LIST_OF_SUPPORTED_SUBTITLE_EXTENSIONS]))
        supported_video_files = "Video files ({})".format(" ".join(["*{}".format(fo) for fo in LIST_OF_SUPPORTED_VIDEO_EXTENSIONS]))

        file_to_open = QFileDialog.getOpenFileName(self, "Select the video or subtitle file", os.path.expanduser("~"), supported_subtitle_files + ';;' + supported_video_files)[0]

    if file_to_open and os.path.isfile(file_to_open) and file_to_open.lower().endswith(LIST_OF_SUPPORTED_SUBTITLE_EXTENSIONS):
        self.subtitles_list = process_subtitles_file(file_to_open)
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
                self.subtitles_list = process_subtitles_file(self.video_metadata['subttiles'])

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


def process_subtitles_file(subtitle_file=False):
    final_subtitles = []

    if subtitle_file.lower().endswith('.srt'):
        with open(subtitle_file) as srt_file:
            srt_content = srt_file.read()

            if ' -> ' in srt_content:
                srt_content = srt_content.replace(' -> ', ' --> ')

            srt_reader = pycaption.SRTReader().read(srt_content)
            for caption in srt_reader.get_captions(list(srt_reader._captions.keys())[0]):
                final_subtitles.append([caption.start/1000000, (caption.end/1000000) - caption.start/1000000, caption.get_text()])

    elif subtitle_file.lower().endswith(('.vtt', '.webvtt')):
        with open(subtitle_file) as vtt_file:
            vtt_reader = pycaption.WebVTTReader().read(vtt_file.read())
            for caption in vtt_reader.get_captions(list(vtt_reader._captions.keys())[0]):
                final_subtitles.append([caption.start/1000000, (caption.end/1000000) - caption.start/1000000, caption.get_text()])

    elif subtitle_file.lower().endswith(('.ttml', '.dfxp')):
        with open(subtitle_file) as dfxp_file:
            dfxp_reader = pycaption.DFXPReader().read(dfxp_file.read())
            for caption in dfxp_reader.get_captions(list(dfxp_reader._captions.keys())[0]):
                final_subtitles.append([caption.start/1000000, (caption.end/1000000) - caption.start/1000000, caption.get_text()])

    elif subtitle_file.lower().endswith(('.sbv')):
        from captionstransformer.sbv import Reader as sbv_reader
        captions = sbv_reader(open(subtitle_file)).read()
        for caption in captions:
            final_subtitles.append([(caption.start-datetime.datetime(1900,1,1)).total_seconds(), caption.duration.total_seconds(), caption.text])

    elif subtitle_file.lower().endswith(( '.smi', '.sami')):
        with open(subtitle_file) as sami_file:
            sami_reader = pycaption.SAMIReader().read(sami_file.read())
            for caption in sami_reader.get_captions(list(sami_reader._captions.keys())[0]):
                final_subtitles.append([caption.start/1000000, (caption.end/1000000) - caption.start/1000000, caption.get_text()])

    elif subtitle_file.lower().endswith(( '.scc')):
        import scc2srt
        final_subtitles = scc2srt.get_list_of_captions(subtitle_file)

    elif subtitle_file.lower().endswith(('.xml')):
        if '<transcript>' in open(subtitle_file).read():
            from captionstransformer.transcript import Reader as transcript_reader
            import html
            captions = transcript_reader(open(subtitle_file)).read()
            for caption in captions:
                final_subtitles.append([(caption.start-datetime.datetime(1900,1,1)).total_seconds(), caption.duration.total_seconds(), html.unescape(caption.text)])
    elif subtitle_file.lower().endswith(('.ass')):
        def clean_text(text):
            clean = re.compile('{.*?}')
            result = re.sub(clean, '', text)
            if '\\' in result.split(' ')[-1]:
                result = result.rsplit(' ',1)[0]
            result = result.replace('\\N', '<br>')
            return result

        with open(subtitle_file, encoding='utf_8_sig') as f:
            assfile = ass.parse(f)
            last_start = None
            last_end = 0.0
            for event in assfile.events:
                start = event.start.total_seconds()
                end = event.end.total_seconds()
                duration = end - start
                if not last_start == None and last_start == start:
                    if last_end <= end:
                        final_subtitles[-1][2] += '<br>' + clean_text(event.text)
                    else:
                        duration = end - last_end - .001
                        final_subtitles.append([last_end + .001, duration, clean_text(event.text)])
                else:
                    final_subtitles.append([start, duration, clean_text(event.text)])
                last_start = start
                last_end = end
    return final_subtitles

def process_video_file(video_file=False):
    video_metadata = {}
    json_result = waveform.ffmpeg_load_metadata(video_file)
    video_metadata['audio'] = False #{0: False}
    video_metadata['waveform'] = {} #{0: False}
    video_metadata['duration'] =  float(json_result.get('format', {}).get('duration', '0.01'))
    for stream in json_result.get('streams', []):
        if stream.get('codec_type', '') == 'video' and not stream.get('codec_name', 'png') == 'png':
            video_metadata['width'] =  int(stream.get('width', 640))
            video_metadata['height'] =  int(stream.get('height', 480))
            video_metadata['framerate'] =  int(stream.get('time_base', '1/30').split('/',1)[-1])
        elif stream.get('codec_type', '') == 'subtitle':
            video_metadata['subttiles'] = waveform.ffmpeg_extract_subtitle(video_file, stream.get('index', 2))
    video_metadata['filepath'] = video_file
    video_metadata['scenes'] = []
    return video_metadata

def save_file(final_file, subtitles_list):
    if subtitles_list:
        if not final_file.lower().endswith('.srt'):
            final_file += '.srt'

        captions = pycaption.CaptionList()
        for sub in subtitles_list:
            # skip extra blank lines
            nodes = [pycaption.CaptionNode.create_text(sub[2])]
            caption = pycaption.Caption(sub[0]*1000000, (sub[0] + sub[1])*.1000000, nodes)
            captions.append(caption)
        caption_set = pycaption.CaptionSet({'en': captions})

        open(final_file, 'w').write(pycaption.SRTWriter().write(caption_set))
