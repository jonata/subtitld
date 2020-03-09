#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import numpy
import subprocess
import json

from modules.paths import *

from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QPen, QColor, QPolygonF, QPixmap
from PyQt5.QtCore import Qt, QPointF, QThread, pyqtSignal



class generate_audio_numpy(QThread):
    audionp = pyqtSignal(numpy.ndarray)

    filename = ''
    sr = 44100
    mono = True
    normalize = True
    in_type = numpy.int16
    out_type = numpy.float32

    def run(self):
        channels = 1 if self.mono else 2
        format_strings = {
            numpy.float64: 'f64le',
            numpy.float32: 'f32le',
            numpy.int16: 's16le',
            numpy.int32: 's32le',
            numpy.uint32: 'u32le'
        }
        format_string = format_strings[self.in_type]
        command = [
            FFMPEG_EXECUTABLE,
            '-i', self.filename,
            '-f', format_string,
            '-acodec', 'pcm_' + format_string,
            '-ar', str(self.sr),
            '-ac', str(channels),
            '-']
        p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=4096) # creationflags=subprocess.CREATE_NO_WINDOW,
        bytes_per_sample = numpy.dtype(self.in_type).itemsize
        frame_size = bytes_per_sample * channels
        chunk_size = frame_size * self.sr # read in 1-second chunks
        raw = b''
        with p.stdout as stdout:
            while True:
                data = stdout.read(chunk_size)
                if data:
                    raw += data
                else:
                    break
        audio = numpy.fromstring(raw, dtype=self.in_type).astype(self.out_type)
        if channels > 1:
            audio = audio.reshape((-1, channels)).transpose()
        if audio.size == 0:
            return audio, self.sr
        if issubclass(self.out_type, numpy.floating):
            if self.normalize:
                peak = numpy.abs(audio).max()
                if peak > 0:
                    audio /= peak
            elif issubclass(self.in_type, numpy.integer):
                audio /= numpy.iinfo(self.in_type).max

        print('acabou')
        self.audionp.emit(audio)



class generate_test(QThread):
    qwidget = pyqtSignal(list)

    view_mode = 'waveform'
    full_waveform = []
    waveformsize = .7

    zoom = 0
    duration = 0
    full_waveform = 0
    widget_width = 0
    widget_height = 0

    class waveform_qpixmap_widget(QWidget):
        def paintEvent(widget, paintEvent):
            painter = QPainter(widget)
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setPen(QPen(QColor.fromRgb(21,52,80,255), 1, Qt.SolidLine))
            painter.setBrush(QColor.fromRgb(21,52,80,alpha=200))

            x_factor = 1

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

    def run(self):
        qpixmap_widget = waveform_qpixmap_widget()
        qpixmap_widget.setStyleSheet("background-color: rgba(0,0,0,0)")
        qpixmap_widget.zoom = self.zoom
        qpixmap_widget.duration = self.duration
        qpixmap_widget.full_waveform = generate_waveform_zoom(self.zoom, self.duration, self.full_waveform)
        qpixmap_widget.setGeometry(0,0,self.widget_width, self.widget_height)
        self.qwidget.emit([self.zoom, qpixmap_widget.grab()])

def return_audio_numpy(self, audionp):
    self.video_metadata['waveform'][0] = audionp

def ffmpeg_load_audio(self, filename, sr=44100, mono=True, normalize=True, in_type=numpy.int16, out_type=numpy.float32):
    qth = generate_audio_numpy(self)
    qth.filename = filename
    qth.audionp.connect(return_audio_numpy)
    qth.start()



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
    #     '-i', filename,
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

def ffmpeg_load_metadata(filename):
    command = [
        FFPROBE_EXECUTABLE,
        '-v',
        'quiet',
        '-print_format',
        'json',
        '-show_format',
        '-show_streams',
        filename]
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=open(os.devnull,'w'))
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

class waveform_qpixmap_widget(QWidget):
    view_mode = 'waveform'
    full_waveform = []
    waveformsize = .7

    def paintEvent(widget, paintEvent):
        painter = QPainter(widget)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(QColor.fromRgb(21,52,80,255), 1, Qt.SolidLine))
        painter.setBrush(QColor.fromRgb(21,52,80,alpha=200))

        x_factor = 1

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

def get_waveform_zoom(self, zoom, duration, full_waveform, widget_width, widget_height):
    qth = generate_test(self)
    qth.zoom = zoom
    qth.duration = duration
    qth.widget_width = widget_width
    qth.widget_height = widget_height
    while not self.video_metadata['waveform'][0]:
        qth.full_waveform = full_waveform
        qth.qwidget.connect(return_waveform_zoom)
        qth.start()

def return_waveform_zoom(self, qpixmap):
    self.video_metadata['waveform'][qpixmap[0]] = qpixmap[1]
