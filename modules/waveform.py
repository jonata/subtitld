#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import numpy
import subprocess
import json

from modules.paths import *

from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QPen, QColor, QPolygonF, QPixmap, QImage
from PyQt5.QtCore import Qt, QPointF, pyqtSignal

def return_audio_numpy(self, audionp):
    self.video_metadata['waveform'][0] = audionp

def ffmpeg_load_audio(filepath, sr=1000, mono=True, normalize=True, in_type=numpy.int16, out_type=numpy.float32):
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
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, startupinfo=STARTUPINFO) # creationflags=subprocess.CREATE_NO_WINDOW,
    bytes_per_sample = numpy.dtype(in_type).itemsize
    frame_size = bytes_per_sample * channels
    chunk_size = frame_size * sr # read in 1-second chunks

    with p.stdout as stdout:
        raw = stdout.read()
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
    audio = numpy.fromstring(raw, dtype=in_type).astype(out_type)
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




    # channels = 1 if mono else 2
    # format_strings = {
    #     numpy.float64: 'f64le',
    #     numpy.float32: 'f32le',
    #     numpy.int16: 's16le',
    #     numpy.int32: 's32le',
    #     numpy.uint32: 'u32le'
    # }
    # format_string = format_strings[in_type]
    # command = [
    #     FFMPEG_EXECUTABLE,
    #     '-i', filepath,
    #     '-f', format_string,
    #     '-acodec', 'pcm_' + format_string,
    #     '-ar', str(sr),
    #     '-ac', str(channels),
    #     '-']
    # p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=4096) # creationflags=subprocess.CREATE_NO_WINDOW,
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
    # audio = numpy.fromstring(raw, dtype=in_type).astype(out_type)
    # if channels > 1:
    #     audio = audio.reshape((-1, channels)).transpose()
    # if audio.size == 0:
    #     return audio, sr
    # if issubclass(out_type, numpy.floating):
    #     if normalize:
    #         peak = numpy.abs(audio).max()
    #         if peak > 0:
    #             audio /= peak
    #     elif issubclass(in_type, numpy.integer):
    #         audio /= numpy.iinfo(in_type).max
    # return audio

def ffmpeg_extract_subtitle(filepath, index):
    command = [
        FFMPEG_EXECUTABLE,
        '-i',
        filepath,
        '-map',
        '0:' + str(index),
        os.path.join(path_tmp, 'subtitle.vtt')]
    p = subprocess.run(command, stdout=subprocess.PIPE, stderr=open(os.devnull,'w'), startupinfo=STARTUPINFO)
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
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=open(os.devnull,'w'), startupinfo=STARTUPINFO)
    json_file = False
    with p.stdout as stdout:
         json_file = json.loads(stdout.read())

    return json_file

def generate_waveform_zoom(zoom, duration, waveform):
    #waveform = self.audio_player_waveform['full']
    positive_values = []
    negative_values = []
    parser = 0
    while parser < len(waveform):
        positive_values.append(numpy.amax(waveform[parser:parser+int(len(waveform)/(duration*zoom))]))
        negative_values.append(numpy.amin(waveform[parser:parser+int(len(waveform)/(duration*zoom))]))
        #positive_values.append(max(waveform[parser:parser+int(len(waveform)/(duration*zoom))]))
        #negative_values.append(min(waveform[parser:parser+int(len(waveform)/(duration*zoom))]))
        parser += int(len(waveform)/(duration*zoom))

    #fft_waveform = numpy.fft.fft(waveform)
    #print(len(fft_waveform))
    #average = []
    average = False
    parser = 0

    bps = 120/60
    #chunk = int(44100/bps)
    chunk = 4096

    return positive_values, negative_values, average
#
# class waveform_qpixmap_widget(QImage):
#     view_mode = 'waveform'
#     full_waveform = []
#     waveformsize = .7
#
#     def paintEvent(widget, paintEvent):
#         painter = QPainter(widget)
#         painter.setRenderHint(QPainter.Antialiasing)
#         painter.setPen(QPen(QColor.fromRgb(21,52,80,255), 1, Qt.SolidLine))
#         painter.setBrush(QColor.fromRgb(21,52,80,alpha=200))
#
#         x_factor = 1
#
#         if widget.view_mode == 'waveform':
#             x_position = 0
#             polygon = QPolygonF()
#
#             for point in widget.full_waveform[0]:
#                 polygon.append(QPointF(x_position, (widget.height()*.5) + (point*(widget.waveformsize*100))))
#                 x_position += x_factor
#
#             for point in reversed(widget.full_waveform[1]):
#                 polygon.append(QPointF(x_position, (widget.height()*.5) + (point*(widget.waveformsize*100))))
#                 x_position -= x_factor
#
#             painter.drawPolygon(polygon)
#         elif widget.view_mode == 'verticalform':
#             polygon1 = QPolygonF()
#             polygon2 = QPolygonF()
#
#             x_position = 0
#             polygon1.append(QPointF(0, widget.height()))
#             for point in widget.full_waveform[0]:
#                 polygon1.append(QPointF(x_position, widget.height() + (-1.0*(point*(widget.waveformsize*200)))))
#                 x_position += x_factor
#             polygon1.append(QPointF(x_position, widget.height()))
#
#             x_position = 0
#             polygon2.append(QPointF(0, widget.height()))
#             for point in widget.full_waveform[1]:
#                 polygon2.append(QPointF(x_position, widget.height() + (point*(widget.waveformsize*200))))
#                 x_position += x_factor
#             polygon2.append(QPointF(x_position, widget.height()))
#
#             painter.drawPolygon(polygon1)
#             painter.drawPolygon(polygon2)
#         if widget.full_waveform[2]:
#             painter.setPen(QPen(QColor.fromRgb(0,200,240,50), 5, Qt.SolidLine))
#             x_position = 0
#             polygon = QPolygonF()
#             last_point = 0.0
#             for point in widget.full_waveform[2]:
#                 polygon.append(QPointF(x_position, widget.height() - (point*(widget.height()*.0008))))
#                 x_position += x_factor
#
#             painter.drawPolyline(polygon)
#             painter.setOpacity(1)
#
#         painter.end()

def get_waveform_zoom(zoom, duration, audio, width, height):
    # qpixmap_widget = waveform_qpixmap_widget()
    # qpixmap_widget.setStyleSheet("background-color: rgba(0,0,0,0)")
    # qpixmap_widget.zoom = zoom
    # qpixmap_widget.duration = duration
    # qpixmap_widget.full_waveform = generate_waveform_zoom(zoom, duration, audio)
    # qpixmap_widget.setGeometry(0,0,width, height)
    # qpixmap_widget.update()
    # return qpixmap_widget.grab()
    if width > 32767:
        x_factor = 32767/width
        width = 32767
    else:
        x_factor = 1
    widget = QImage(width, height, QImage.Format_ARGB32)
    widget.fill(Qt.transparent)
    widget.view_mode = 'waveform'
    widget.waveformsize = .7
    widget.full_waveform = generate_waveform_zoom(zoom, duration, audio)

    painter = QPainter(widget)
    painter.setRenderHint(QPainter.Antialiasing)
    painter.setPen(QPen(QColor.fromRgb(21,52,80,255), 1, Qt.SolidLine))
    painter.setBrush(QColor.fromRgb(21,52,80,alpha=200))


    if widget.view_mode == 'waveform':
        x_position = 0
        polygon = QPolygonF()

        for point in widget.full_waveform[0]:
            polygon.append(QPointF(x_position, (widget.height()*.5) + (point*(widget.waveformsize*100))))
            x_position += x_factor

        for point in reversed(widget.full_waveform[1]):
            polygon.append(QPointF(x_position, (widget.height()*.5) + (point*(widget.waveformsize*100))))
            x_position -= x_factor

        painter.drawPolygon(polygon)
    elif widget.view_mode == 'verticalform':
        polygon1 = QPolygonF()
        polygon2 = QPolygonF()

        x_position = 0
        polygon1.append(QPointF(0, widget.height()))
        for point in widget.full_waveform[0]:
            polygon1.append(QPointF(x_position, widget.height() + (-1.0*(point*(widget.waveformsize*200)))))
            x_position += x_factor
        polygon1.append(QPointF(x_position, widget.height()))

        x_position = 0
        polygon2.append(QPointF(0, widget.height()))
        for point in widget.full_waveform[1]:
            polygon2.append(QPointF(x_position, widget.height() + (point*(widget.waveformsize*200))))
            x_position += x_factor
        polygon2.append(QPointF(x_position, widget.height()))

        painter.drawPolygon(polygon1)
        painter.drawPolygon(polygon2)
    if widget.full_waveform[2]:
        painter.setPen(QPen(QColor.fromRgb(0,200,240,50), 5, Qt.SolidLine))
        x_position = 0
        polygon = QPolygonF()
        last_point = 0.0
        for point in widget.full_waveform[2]:
            polygon.append(QPointF(x_position, widget.height() - (point*(widget.height()*.0008))))
            x_position += x_factor

        painter.drawPolyline(polygon)
        painter.setOpacity(1)

    painter.end()

    #widget.setStyleSheet("background-color: rgba(0,0,0,0)")
    #widget.zoom = zoom
    #widget.duration = duration
    #widget.full_waveform = generate_waveform_zoom(zoom, duration, audio)
    #widget.setGeometry(0,0,)
    #widget.update()
    return widget

def return_waveform_zoom(self, qpixmap):
    self.video_metadata['waveform'][qpixmap[0]] = qpixmap[1]
