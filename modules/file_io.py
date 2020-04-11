#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import pysrt
import timecode
import datetime
import numpy
#from moviepy.editor import VideoFileClip
#from pymediainfo import MediaInfo

from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import QThread, pyqtSignal

from modules import waveform
from modules.paths import *

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
            p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            for line in p.stdout.read().decode().split('\n'):
                if line.startswith(('[')) and 'pts_time:' in line:
                    result.append(float(line.split('pts_time:',1)[-1].split(' ',1)[0]))

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
        #self.video_metadata['waveform'][0] = command
        self.video_metadata['audio'] = command
        self.timeline.zoom_update_waveform(self)
        self.toppanel_videoinfo_label.setText('Audio extracted')

    self.thread_extract_waveform = thread_extract_waveform(self)
    self.thread_extract_waveform.command.connect(thread_extract_waveform_ended)

    def thread_extract_scene_time_positions_ended(command):
        self.video_metadata['scenes'] = command

    self.thread_extract_scene_time_positions = thread_extract_scene_time_positions(self)
    self.thread_extract_scene_time_positions.command.connect(thread_extract_scene_time_positions_ended)

def open_filepath(self, file_to_open):
    self.subtitles_list, self.video_metadata = open_file(file_to_open)
    if not self.video_metadata:
        file_to_open = QFileDialog.getOpenFileName(self, "Select the video file", os.path.expanduser("~"), "MP4 file (*.mp4)")[0]
        if file_to_open and os.path.isfile(file_to_open):
            self.video_metadata = process_video_metadata(file_to_open)

    if self.video_metadata:
        self.thread_extract_waveform.filepath = self.video_metadata['filepath']
        self.thread_extract_waveform.start()
        self.toppanel_videoinfo_label.setText('Extracting audio...')
        self.thread_extract_scene_time_positions.filepath = self.video_metadata['filepath']
        self.thread_extract_scene_time_positions.start()


        #waveform.ffmpeg_load_audio(self, )
        #waveform.get_waveform_zoom(self, self.mediaplayer_zoom, self.video_metadata['duration'], self.video_metadata['waveform'][0], self.video_metadata.get('duration', 0.01)*self.mediaplayer_zoom, self.timeline_widget.height()-30)
        #t = threading.Thread(target=waveform.get_waveform_zoom, args=(self, self.mediaplayer_zoom, self.video_metadata['duration'], self.video_metadata['waveform'][0], self.video_metadata.get('duration', 0.01)*self.mediaplayer_zoom, self.timeline_widget.height()-30), daemon=True)
        #t = multiprocessing.Process(target=waveform.get_waveform_zoom, args=(self, self.mediaplayer_zoom, self.video_metadata['duration'], self.video_metadata['waveform'][0], self.video_metadata.get('duration', 0.01)*self.mediaplayer_zoom, self.timeline_widget.height()-30), daemon=True)
        # qth = waveform.generate_test(self)
        # qth.zoom = self.mediaplayer_zoom
        # qth.duration = self.video_metadata['duration']
        # qth.full_waveform = self.video_metadata['waveform'][0]
        # qth.widget_width = self.video_metadata.get('duration', 0.01)*self.mediaplayer_zoom
        #qth.widget_height = self.timeline_widget.height()-30

        #qth.qwidget.connect(self.update_things())
        #qth.start()
        #t.start()
        #print("imediato")
        self.player.update(self)
        self.player_widget.mpv.play(self.video_metadata['filepath'])
        self.player_widget.mpv.wait_for_property('seekable')
        self.player_widget.mpv.pause = True
        self.player.resize_player_widget(self)

    self.subtitleslist.update_subtitles_list_widget(self)
    self.timeline.update_timeline(self)
    self.actual_subtitle_file = file_to_open
    self.startscreen.hide(self)
    self.playercontrols.show(self)
    self.properties.show(self)
    self.subtitleslist.show(self)
    self.toppanel.show(self)
    self.toppanel_subtitle_file_info_label.setText('<b><snall>ACTUAL PROJECT</small></b><br><big>' + file_to_open + '</big>')

    self.settings['recent_files'][file_to_open] = datetime.datetime.now().strftime("%Y%m%d")

def open_file(filepath):
    final_subtitles = []
    if filepath:
        if filepath.lower().endswith('.srt'):
            with open(filepath) as srtfile:
                subs = pysrt.from_string(srtfile.read())
                for sub in subs:
                    start = (timecode.Timecode('ms', str(sub.start).replace(',','.')).frames/1000) - .001 # sugerir para o pessoal do timecode pra implementar virgula
                    duration = (timecode.Timecode('ms', str(sub.duration).replace(',','.')).frames/1000) - .001 # sugerir para o pessoal do timecode pra implementar virgula
                    final_subtitles.append([start, duration, str(sub.text)])
    video_metadata = {}
    mp4_file = os.path.join(os.path.dirname(filepath), os.path.basename(filepath).rsplit('.',1)[0] + '.mp4')
    if os.path.isfile(mp4_file):
        video_metadata = process_video_metadata(mp4_file)
    return final_subtitles, video_metadata

def process_video_metadata(mp4_file):
    video_metadata = {}
    json_result = waveform.ffmpeg_load_metadata(mp4_file)
    video_metadata['audio'] = False #{0: False}
    video_metadata['waveform'] = False #{0: False}
    video_metadata['duration'] =  float(json_result.get('format', {}).get('duration', '0.01'))
    video_metadata['width'] =  int(json_result.get('streams', [])[0].get('width', '640'))
    video_metadata['height'] =  int(json_result.get('streams', [])[0].get('height', '640'))
    video_metadata['framerate'] =  int(json_result.get('streams', [])[0].get('time_base', '1/30').split('/',1)[-1])
    video_metadata['filepath'] = mp4_file
    video_metadata['scenes'] = []
    return video_metadata

def save_file(final_file, subtitles_list):
    if subtitles_list:
        if final_file.lower().endswith('.srt'):

            def humanize_time(secs):
                secs, mils = divmod(secs, 1)
                mins, secs = divmod(secs, 60)
                hours, mins = divmod(mins, 60)
                return '%02d:%02d:%02d,%03d' % (hours, mins, secs, mils*1000)

            srtfile = pysrt.SubRipFile()
            counter = 1
            for sub in subtitles_list:
                sub = pysrt.SubRipItem(counter, start=humanize_time(sub[0]), end=humanize_time(sub[0] + sub[1]), text=sub[2])
                srtfile.append(sub)
                counter += 1
            srtfile.save(final_file)
