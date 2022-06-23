"""Waveform module

"""

import os
import subprocess
import json
from PySide6.QtCore import QPointF, QThread, Signal, Qt
from PySide6.QtGui import QColor, QPainter, QPen, QPixmap, QPolygonF
import numpy
import ffms2
import asyncio

from subtitld.modules.paths import STARTUPINFO, FFMPEG_EXECUTABLE, path_tmp, FFPROBE_EXECUTABLE


def return_audio_numpy(self, audionp):
    """Function to return waveform's numpy"""
    self.video_metadata['waveform'][0] = audionp


def ffmpeg_load_audio(filepath, samplerate=48000, mono=True, normalize=True, in_type=numpy.int16, out_type=numpy.float32):
    """Function to call ffmpeg and return numpy"""
    channels = 1 if mono else 2
    format_strings = {
        numpy.float64: 'f64le',
        numpy.float32: 'f32le',
        numpy.int16: 's16le',
        numpy.int32: 's32le',
        numpy.uint32: 'u32le'
    }
    print('ffmpeg load audio started')
    format_string = format_strings[in_type]
    command = [
        FFMPEG_EXECUTABLE,
        '-loglevel', 'quiet',
        '-i', filepath,
        '-f', format_string,
        '-acodec', 'pcm_' + format_string,
        '-ar', str(samplerate),
        '-ac', str(channels),
        '-']
    print('ffmpeg load will start')
    # proc = asyncio.subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, startupinfo=STARTUPINFO)#, bufsize=64)
    async def runcmd(command):
        proc = await asyncio.create_subprocess_shell(command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.DEVNULL, startupinfo=STARTUPINFO)#, bufsize=64)
        stdout, _ = await proc.communicate()

    # bytes_per_sample = numpy.dtype(in_type).itemsize
    # frame_size = bytes_per_sample * channels
    # chunk_size = frame_size * sr

    # print('ffmpeg load audio subprocess started')
    # with proc.stdout as stdout:
        # raw = stdout.read()
        raw = stdout
        # print(type(raw))
        audio = numpy.frombuffer(raw)#, dtype=in_type).astype(out_type)
        return audio

    audio = asyncio.run(runcmd(' '.join(command)))

    print('ffmpeg load ended')
    # p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, bufsize=4096, startupinfo=STARTUPINFO) # creationflags=subprocess.CREATE_NO_WINDOW,
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
        return audio, samplerate
    if issubclass(out_type, numpy.floating):
        if normalize:
            peak = numpy.abs(audio).max()
            if peak > 0:
                audio /= peak
        elif issubclass(in_type, numpy.integer):
            audio /= numpy.iinfo(in_type).max
    print(len(audio))
    return audio


def ffms2_load_audio(filepath, samplerate=48000, mono=True, normalize=True, in_type=numpy.int16, out_type=numpy.float32):
    # asource = ffms2.AudioSource(filepath)
    # asource.init_buffer(asource.properties.NumSamples)
    # print(asource.properties.NumSamples)
    # print(4096*64000)
    # asource.init_buffer((4096*64000))
    # sound_np = asource.get_audio(0)
    # start = (4096*64)
    # while start < asource.properties.NumSamples:
    #     if start + (4096*64) > asource.properties.NumSamples:
    #         asource.init_buffer((4096*64) % ((start + (4096*64)) - asource.properties.NumSamples))

    #     sound_np = numpy.append(sound_np, asource.get_audio(start), axis=0)
    #     start += (4096*64)
    # # print(sound_np)
    # print(sound_np.shape)
    return []#sound_np


def ffmpeg_extract_subtitle(filepath, index):
    """Function to extract subtitle from video using ffmpeg"""
    command = [
        FFMPEG_EXECUTABLE,
        '-i',
        filepath,
        '-map',
        '0:' + str(index),
        os.path.join(path_tmp, 'subtitle.vtt')]
    subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, startupinfo=STARTUPINFO).wait()
    print('subtitle extracted')
    return os.path.join(path_tmp, 'subtitle.vtt')


def ffmpeg_load_metadata(filepath):
    """Function to read video's metadata"""
    command = [
        FFPROBE_EXECUTABLE,
        '-v',
        'quiet',
        '-print_format',
        'json',
        '-show_format',
        '-show_streams',
        filepath]
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, startupinfo=STARTUPINFO)
    json_file = False
    with proc.stdout as stdout:
        # test = stdout.read()
        # print(test)
        json_file = json.loads(stdout.read())

    return json_file


def generate_waveform_zoom(zoom, duration, waveform):
    """Function to calculate waveform from numpy"""
    positive_values = []
    negative_values = []
    parser = 0
    while parser < len(waveform):
        positive_values.append(numpy.amax(waveform[parser:parser+int(len(waveform) / (duration * zoom))]))
        negative_values.append(numpy.amin(waveform[parser:parser+int(len(waveform) / (duration * zoom))]))
        parser += int(len(waveform) / (duration * zoom))
    average = False
    parser = 0

    # bps = 120/60
    # chunk = int(44100/bps)
    # chunk = 4096

    return positive_values, negative_values, average


def generate_waveform_zoom2(zoom, duration, filepath):
    positive_values = []
    negative_values = []
    average = False

    asource = ffms2.AudioSource(filepath)

    parser = 0
    chunk = int(asource.properties.NumSamples / (duration * zoom))
    print(chunk)
    while parser < asource.properties.NumSamples:
        if parser + chunk > asource.properties.NumSamples:
            chunk = (asource.properties.NumSamples - parser)

        asource.init_buffer(chunk)
        sound_np = asource.get_audio(parser)

        if sound_np.ndim > 1:
            sound_np = numpy.mean(sound_np, axis=1)

        positive_values.append(numpy.amax(sound_np))
        negative_values.append(numpy.amin(sound_np))

        parser += chunk




    # counter = 0
    # chunk = asource.properties.SampleRate * 60
    # while counter < asource.properties.NumSamples:
    #     if counter + chunk > asource.properties.NumSamples:
    #         chunk = (asource.properties.NumSamples - counter)

    #     asource.init_buffer(chunk)
    #     sound_np = asource.get_audio(counter)

    #     if sound_np.ndim > 1:
    #         sound_np = numpy.mean(sound_np, axis=1)

    #     parser = 0
    #     while parser < len(sound_np):
    #         positive_values.append(numpy.amax(sound_np[parser:parser + int(len(sound_np) / (duration * zoom))]))
    #         negative_values.append(numpy.amin(sound_np[parser:parser + int(len(sound_np) / (duration * zoom))]))
    #         parser += int(asource.properties.NumSamples / (duration * zoom))

    #     counter += chunk

    return positive_values, negative_values, average


def return_waveform_zoom(self, qpixmap):
    """Function to return waveform's zoom"""
    self.video_metadata['waveform'][qpixmap[0]] = qpixmap[1]


class ThreadExtractWaveform2(QThread):
    """Thread to extract waveform"""
    command = Signal(list)
    filepath = ''
    duration = 60
    zoom = 100
    border_color = '#ff153450'
    fill_color = '#cc153450'

    class DrawPixmap(QPixmap):
        waveform_up = []
        waveform_down = []
        x_offset = 0
        waveformsize = .7
        border_color = '#ff153450'
        fill_color = '#cc153450'

        def paintEvent(self):
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)

            painter.setPen(QPen(QColor(self.border_color), 1, Qt.SolidLine))
            painter.setBrush(QColor(self.fill_color))

            x_position = 0
            polygon = QPolygonF()
            for point in self.waveform_up:
                polygon.append(QPointF(x_position, (self.height() * .5) + (point * (self.waveformsize * 100))))
                x_position += 1
            for point in reversed(self.waveform_down):
                polygon.append(QPointF(x_position, (self.height() * .5) + (point * (self.waveformsize * 100))))
                x_position -= 1
            painter.drawPolygon(polygon)

            painter.end()

    def run(self):
        """Run function of thread to extract waveform"""
        if self.filepath:
            asource = ffms2.AudioSource(self.filepath)
            counter = 0
            chunk = 4096*100
            while counter < asource.properties.NumSamples:
                asource.init_buffer(chunk)
                sound_np = asource.get_audio(counter)

                positive_values = []
                negative_values = []
                parser = 0
                while parser < len(sound_np):
                    positive_values.append(numpy.amax(sound_np[parser:parser + int(len(sound_np) / (self.duration * self.zoom))]))
                    negative_values.append(numpy.amin(sound_np[parser:parser + int(len(sound_np) / (self.duration * self.zoom))]))
                    parser += int(len(sound_np) / (self.duration * self.zoom))


                # bps = 120/60
                # chunk = int(44100/bps)
                # chunk = 4096

                pixmap_width = len(positive_values)
                qpixmap = self.DrawPixmap(pixmap_width, 124)
                qpixmap.fill(QColor(0, 0, 0, 0))
                qpixmap.waveform_up = positive_values[parser:parser + pixmap_width]
                qpixmap.waveform_down = negative_values[parser:parser + pixmap_width]
                qpixmap.border_color = self.border_color
                qpixmap.fill_color = self.fill_color
                qpixmap.paintEvent()

                self.command.emit([self.zoom, qpixmap.toImage()])

                counter += chunk - (((asource.properties.NumSamples - (counter + chunk)) - chunk) if (counter + chunk) > asource.properties.NumSamples else 0)
