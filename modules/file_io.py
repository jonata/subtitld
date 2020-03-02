#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import pysrt
import timecode
#from moviepy.editor import VideoFileClip
from pymediainfo import MediaInfo

from modules import waveform

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
    audio_np = waveform.ffmpeg_load_audio(mp4_file)
    json_result = waveform.ffmpeg_load_metadata(mp4_file)

    video_metadata['waveform'] = {0: audio_np}
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
