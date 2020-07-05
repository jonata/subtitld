#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import numpy
import subprocess
import json

from modules.paths import STARTUPINFO, FFMPEG_EXECUTABLE, path_tmp, FFPROBE_EXECUTABLE


def return_audio_numpy(self, audionp):
    self.video_metadata['waveform'][0] = audionp


def ffmpeg_load_audio(filepath, sr=48000, mono=True, normalize=True, in_type=numpy.int16, out_type=numpy.float32):
    channels = 1 if mono else 2
    format_strings = {
        numpy.float64: 'f64le',
        numpy.float32: 'f32le',
        numpy.int16: 's16le',
        numpy.int32: 's32le',
        numpy.uint32: 'u32le'
    }
    format_string = format_strings[in_type]
    command = [
        FFMPEG_EXECUTABLE,
        '-i', filepath,
        '-f', format_string,
        '-acodec', 'pcm_' + format_string,
        '-ar', str(sr),
        '-ac', str(channels),
        '-']
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, startupinfo=STARTUPINFO)
    # bytes_per_sample = numpy.dtype(in_type).itemsize
    # frame_size = bytes_per_sample * channels
    # chunk_size = frame_size * sr

    with p.stdout as stdout:
        raw = stdout.read()
        audio = numpy.fromstring(raw, dtype=in_type).astype(out_type)

    # p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=4096, startupinfo=STARTUPINFO) # creationflags=subprocess.CREATE_NO_WINDOW,
    # bytes_per_sample = numpy.dtype(in_type).itemsize
    # frame_size = bytes_per_sample * channels
    # chunk_size = frame_size * sr # read in 1-second chunks
    # raw = b''
    # with p.stdout as stdout:
    #     while True:
    #         data = stdout.read(chunk_size)
    #         if data:
    #             raw += data
    #         else:
    #             break

    if channels > 1:
        audio = audio.reshape((-1, channels)).transpose()
    if audio.size == 0:
        return audio, sr
    if issubclass(out_type, numpy.floating):
        if normalize:
            peak = numpy.abs(audio).max()
            if peak > 0:
                audio /= peak
        elif issubclass(in_type, numpy.integer):
            audio /= numpy.iinfo(in_type).max
    return audio


def ffmpeg_extract_subtitle(filepath, index):
    command = [
        FFMPEG_EXECUTABLE,
        '-i',
        filepath,
        '-map',
        '0:' + str(index),
        os.path.join(path_tmp, 'subtitle.vtt')]
    subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, startupinfo=STARTUPINFO).wait()

    return os.path.join(path_tmp, 'subtitle.vtt')


def ffmpeg_load_metadata(filepath):
    command = [
        FFPROBE_EXECUTABLE,
        '-v',
        'quiet',
        '-print_format',
        'json',
        '-show_format',
        '-show_streams',
        filepath]
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, startupinfo=STARTUPINFO)
    json_file = False
    with p.stdout as stdout:
        json_file = json.loads(stdout.read())

    return json_file


def generate_waveform_zoom(zoom, duration, waveform):
    positive_values = []
    negative_values = []
    parser = 0
    while parser < len(waveform):
        positive_values.append(numpy.amax(waveform[parser:parser+int(len(waveform)/(duration*zoom))]))
        negative_values.append(numpy.amin(waveform[parser:parser+int(len(waveform)/(duration*zoom))]))
        parser += int(len(waveform)/(duration*zoom))
    average = False
    parser = 0

    # bps = 120/60
    # chunk = int(44100/bps)
    # chunk = 4096

    return positive_values, negative_values, average


def return_waveform_zoom(self, qpixmap):
    self.video_metadata['waveform'][qpixmap[0]] = qpixmap[1]
