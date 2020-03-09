#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import pysrt
import timecode
import datetime
#from moviepy.editor import VideoFileClip
#from pymediainfo import MediaInfo

from modules import waveform

def open_filepath(self, file_to_open):
    self.subtitles_list, self.video_metadata = open_file(file_to_open)
    if not self.video_metadata:
        file_to_open = QFileDialog.getOpenFileName(self, "Select the video file", os.path.expanduser("~"), "MP4 file (*.mp4)")[0]
        if file_to_open and os.path.isfile(file_to_open):
            self.video_metadata = process_video_metadata(file_to_open)


    if self.video_metadata:
        #waveform.ffmpeg_load_audio(self, self.video_metadata['filepath'])
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

    self.settings['recent_files'][datetime.datetime.now().strftime("%Y%m%d")] = file_to_open

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
    video_metadata['waveform'] = {0: []}
    video_metadata['duration'] =  float(json_result.get('format', {}).get('duration', '0.01'))
    video_metadata['width'] =  int(json_result.get('streams', [])[0].get('width', '640'))
    video_metadata['height'] =  int(json_result.get('streams', [])[0].get('height', '640'))
    video_metadata['filepath'] = mp4_file
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
