#!/usr/bin/python3
# -*- coding: utf-8 -*-

from bisect import bisect
import timecode
from PyQt5.QtGui import QPainter, QPen, QColor, QPolygonF, QFont, QPixmap
from PyQt5.QtWidgets import QWidget, QScrollArea
from PyQt5.QtCore import Qt, QRect, QPointF, QThread, pyqtSignal

from modules import waveform
from modules import history


class draw_qpixmap(QPixmap):
    waveform_up = []
    waveform_down = []
    x_offset = 0
    waveformsize = .7

    def paintEvent(widget, paintEvent):
        painter = QPainter(widget)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.setPen(QPen(QColor.fromRgb(21, 52, 80, 255), 1, Qt.SolidLine))
        painter.setBrush(QColor.fromRgb(21, 52, 80, alpha=200))

        x_position = 0
        polygon = QPolygonF()
        for point in widget.waveform_up:
            polygon.append(QPointF(x_position, (widget.height()*.5) + (point*(widget.waveformsize*100))))
            x_position += 1
        for point in reversed(widget.waveform_down):
            polygon.append(QPointF(x_position, (widget.height()*.5) + (point*(widget.waveformsize*100))))
            x_position -= 1
        painter.drawPolygon(polygon)

        painter.end()


class thread_get_waveform(QThread):
    command = pyqtSignal(list)
    zoom = False
    audio = False
    duration = False
    width = False
    height = False

    def run(self):
        positive_values, negative_values, blah = waveform.generate_waveform_zoom(zoom=self.zoom, duration=self.duration, waveform=self.audio)
        self.command.emit([self.zoom, [positive_values, negative_values]])


class thread_get_qimages(QThread):
    command = pyqtSignal(list)
    values_list = []
    zoom = 100.0
    width = 32767

    def run(self):
        final_list = []
        parser = 0
        while True:
            qpixmap = draw_qpixmap(self.width, 124)
            qpixmap.fill(QColor(0, 0, 0, 0))
            qpixmap.waveform_up = self.values_list[0][parser:parser+self.width]
            qpixmap.waveform_down = self.values_list[1][parser:parser+self.width]
            qpixmap.paintEvent(qpixmap)
            final_list.append(qpixmap.toImage())                # qpixmap.save('/tmp/teste.png')
            parser += self.width
            if parser > len(self.values_list[0]):
                break
        self.command.emit([self.zoom, final_list])


def get_timeline_time_str(seconds):
    secs = int(seconds % 60)
    mins = int((seconds / 60) % 60)
    hrs = int((seconds / 60) / 60)

    if hrs:
        return "{hh:02d}:{mm:02d}:{ss:02d}".format(hh=hrs, mm=mins, ss=secs)
    elif mins:
        return "{mm:02d}:{ss:02d}".format(mm=mins, ss=secs)
    else:
        return "{ss:02d}".format(ss=secs)


def load(self, PATH_SUBTITLD_GRAPHICS):
    class timeline(QWidget):
        subtitle_is_clicked = False
        subtitle_start_is_clicked = False
        subtitle_end_is_clicked = False
        width_proportion = self.width()/self.video_metadata.get('duration', 0.01)
        subtitle_height = 50
        subtitle_y = 55
        offset = 0.0
        y_waveform = 22
        h_waveform = 124
        show_limiters = False
        is_cursor_pressing = False
        waveformsize = .7

        def paintEvent(widget, paintEvent):
            painter = QPainter(widget)
            scroll_position = self.timeline_scroll.horizontalScrollBar().value()
            scroll_width = self.timeline_scroll.width()

            painter.setRenderHint(QPainter.Antialiasing)

            painter.setOpacity(self.mediaplayer_opacity)

            if self.mediaplayer_view_mode and self.video_metadata.get('waveform', {}):
                if self.mediaplayer_view_mode in ['waveform', 'verticalform']:
                    if self.video_metadata.get('waveform', {}):
                        x_factor = 1
                        available_zoom = self.mediaplayer_zoom
                        if available_zoom not in self.video_metadata['waveform'].keys():
                            available_zoom = sorted(self.video_metadata['waveform'].keys())[0]
                            x_factor = self.mediaplayer_zoom/available_zoom

                        w_factor = (self.video_metadata.get('duration', 0.01)*available_zoom)/len(self.video_metadata['waveform'][available_zoom]['points'][0])

                        if self.video_metadata['waveform'][available_zoom].get('qimages', []):
                            x = 0
                            for qimage in self.video_metadata['waveform'][available_zoom]['qimages']:
                                w = qimage.width()*w_factor*x_factor
                                if not x > scroll_position + scroll_width and not x + w < scroll_position:
                                    painter.drawImage(QRect(x, widget.y_waveform, w, widget.h_waveform), qimage)
                                x += w

                        elif self.video_metadata['waveform'][available_zoom].get('points', []):
                            painter.setPen(QPen(QColor.fromRgb(21, 52, 80, 255), 1, Qt.SolidLine))
                            painter.setBrush(QColor.fromRgb(21, 52, 80, alpha=200))

                            x_position = 0
                            polygon = QPolygonF()

                            for point in self.video_metadata['waveform'][available_zoom]['points'][0][int(scroll_position/(x_factor*w_factor)):int((scroll_position+scroll_width)/(x_factor*w_factor))]:
                                polygon.append(QPointF((x_position+scroll_position), widget.y_waveform + (widget.h_waveform*.5) + (point*(widget.waveformsize*100))))
                                x_position += (x_factor*w_factor)

                            for point in reversed(self.video_metadata['waveform'][available_zoom]['points'][1][int(scroll_position/(x_factor*w_factor)):int((scroll_position+scroll_width)/(x_factor*w_factor))]):
                                polygon.append(QPointF((x_position+scroll_position), widget.y_waveform + (widget.h_waveform*.5) + (point*(widget.waveformsize*100))))
                                x_position -= (x_factor*w_factor)

                            painter.drawPolygon(polygon)

            if self.subtitles_list:
                painter.setOpacity(1)
                painter.setPen(QPen(QColor.fromRgb(240, 240, 240, 200), 1, Qt.SolidLine))

                for subtitle in self.subtitles_list:
                    if (subtitle[0] / self.video_metadata.get('duration', 0.01)) > ((scroll_position + scroll_width) / widget.width()):
                        break
                    elif (subtitle[0] + subtitle[1]) / self.video_metadata.get('duration', 0.01) < (scroll_position / widget.width()):
                        continue
                    else:
                        if self.selected_subtitle == subtitle:
                            painter.setPen(QColor.fromRgb(48, 66, 81, alpha=255))
                            painter.setBrush(QColor.fromRgb(62, 83, 99, alpha=220))
                        else:
                            painter.setPen(QColor.fromRgb(106, 116, 131, alpha=255))
                            painter.setBrush(QColor.fromRgb(184, 206, 224, alpha=220))

                        subtitle_rect = QRect(subtitle[0] * widget.width_proportion,
                                              widget.subtitle_y,
                                              subtitle[1] * widget.width_proportion,
                                              widget.subtitle_height)

                        painter.drawRoundedRect(subtitle_rect, 2.0, 2.0, Qt.AbsoluteSize)

                        if self.selected_subtitle == subtitle:
                            painter.setPen(QColor.fromRgb(255, 255, 255, alpha=255))
                        else:
                            painter.setPen(QColor.fromRgb(48, 66, 81, alpha=255))

                        painter.drawText(subtitle_rect, Qt.AlignCenter | Qt.TextWrapAnywhere, subtitle[2])

                        if widget.show_limiters and (subtitle[1] * widget.width_proportion) > 40:
                            painter.setPen(Qt.NoPen)
                            lim_rect = QRect(
                                                (subtitle[0] * widget.width_proportion) + 2,
                                                widget.subtitle_y + 2,
                                                18,
                                                widget.subtitle_height - 4
                                            )

                            painter.drawRoundedRect(lim_rect, 1.0, 1.0, Qt.AbsoluteSize)
                            painter.setPen(QColor.fromRgb(150, 150, 150, alpha=255))
                            painter.drawText(lim_rect, Qt.AlignCenter, '❮')

                            painter.setPen(Qt.NoPen)
                            lim_rect = QRect(
                                                (subtitle[0] * widget.width_proportion) + (subtitle[1] * widget.width_proportion) - 20,
                                                widget.subtitle_y + 2,
                                                18,
                                                widget.subtitle_height - 4
                                            )

                            painter.drawRoundedRect(lim_rect, 1.0, 1.0, Qt.AbsoluteSize)
                            painter.setPen(QColor.fromRgb(150, 150, 150, alpha=255))
                            painter.drawText(lim_rect, Qt.AlignCenter, '❯')

                painter.setOpacity(1)

            grid_pen = QPen(QColor.fromRgb(106, 116, 131, 20), 1, Qt.SolidLine)
            painter.setFont(QFont('Ubuntu Mono', 8))
            x = 0
            for sec in range(int(self.video_metadata['duration'])):
                if x >= scroll_position and x <= (scroll_position + self.timeline_scroll.width()):
                    if (self.mediaplayer_zoom > 75) or (self.mediaplayer_zoom > 50 and self.mediaplayer_zoom <= 75 and not int((sec % 2))) or (self.mediaplayer_zoom > 25 and self.mediaplayer_zoom <= 50 and not int((sec % 4))) or (self.mediaplayer_zoom <= 25 and not int((sec % 8))):
                        lim_rect = QRect(
                                            x+3,
                                            27,
                                            50,
                                            20
                                        )
                        painter.setPen(QColor.fromRgb(106, 116, 131, alpha=50))
                        painter.drawText(lim_rect, Qt.AlignLeft, get_timeline_time_str(sec))
                    if self.timeline_show_grid and self.timeline_grid_type == 'seconds':
                        painter.setPen(grid_pen)
                        painter.drawLine(x, 0, x, widget.height())
                x += widget.width_proportion

            if self.timeline_show_grid and self.timeline_grid_type == 'frames':
                painter.setPen(grid_pen)
                x = 0
                for fr in range(int(self.video_metadata['duration']*self.video_metadata['framerate'])):
                    if x >= scroll_position and x <= (scroll_position + self.timeline_scroll.width()):
                        painter.drawLine(x, 0, x, widget.height())
                    x += int(widget.width_proportion/self.video_metadata['framerate'])
            elif self.timeline_show_grid and self.timeline_grid_type == 'scenes' and self.video_metadata['scenes']:
                painter.setPen(grid_pen)
                for scene in self.video_metadata['scenes']:
                    x = (scene*widget.width_proportion)
                    if x >= scroll_position and x <= (scroll_position + self.timeline_scroll.width()):
                        painter.drawLine(x, 0, x, widget.height())

            if self.player_widget.position is not None:
                painter.setPen(QPen(QColor.fromRgb(255, 0, 0, 200), 2, Qt.SolidLine))
                cursor_pos = self.player_widget.position * widget.width_proportion
                painter.drawLine(cursor_pos, 0, cursor_pos, widget.height())

            painter.end()

        def mousePressEvent(widget, event):
            widget.is_cursor_pressing = True

            self.selected_subtitle = False

            for subtitle in self.subtitles_list:
                if event.pos().y() > widget.subtitle_y and event.pos().y() < (widget.subtitle_height + widget.subtitle_y) and (((event.pos().x())/widget.width_proportion) > subtitle[0] and ((event.pos().x())/widget.width_proportion) < (subtitle[0] + subtitle[1])):
                    self.selected_subtitle = subtitle
                    if event.pos().x()/widget.width_proportion > (subtitle[0] + subtitle[1]) - (20/widget.width_proportion):
                        widget.subtitle_end_is_clicked = True
                        widget.offset = ((self.selected_subtitle[0] + self.selected_subtitle[1])*widget.width_proportion) - event.pos().x()
                    else:
                        widget.offset = event.pos().x() - self.selected_subtitle[0]*widget.width_proportion
                        if event.pos().x()/widget.width_proportion < subtitle[0] + (20/widget.width_proportion):
                            widget.subtitle_start_is_clicked = True
                        else:
                            widget.subtitle_is_clicked = True
                    break

            if not (widget.subtitle_end_is_clicked or widget.subtitle_start_is_clicked or widget.subtitle_is_clicked):
                self.player_widget.seek((event.pos().x() / widget.width())*self.video_metadata['duration'])
                update_timecode_label(self)

            self.properties.update_properties_widget(self)

            if (widget.subtitle_is_clicked or widget.subtitle_start_is_clicked or widget.subtitle_end_is_clicked):
                history.history_append(self.subtitles_list)
                self.unsaved = True

            widget.update()

        def mouseReleaseEvent(widget, event):
            widget.subtitle_is_clicked = False
            widget.subtitle_start_is_clicked = False
            widget.subtitle_end_is_clicked = False
            widget.is_cursor_pressing = False
            widget.update()

        def mouseMoveEvent(widget, event):
            if self.selected_subtitle:
                i = self.subtitles_list.index(self.selected_subtitle)
                last = self.subtitles_list[self.subtitles_list.index(self.selected_subtitle)-1] if self.subtitles_list.index(self.selected_subtitle) > 0 else [0, 0, '']
                next = self.subtitles_list[self.subtitles_list.index(self.selected_subtitle)+1] if self.subtitles_list.index(self.selected_subtitle) < len(self.subtitles_list) - 1 else [self.video_metadata['duration'], 0, '']
                scenes_list = self.video_metadata['scenes'] if len(self.video_metadata['scenes']) > 1 else [0.0]
                scenes_list.append(self.video_metadata['duration'])
                start_position = (event.pos().x() - widget.offset) / widget.width_proportion
                last_scene = scenes_list[bisect(scenes_list, start_position)-1]
                next_scene = scenes_list[bisect(scenes_list, start_position)]
                if widget.subtitle_start_is_clicked:
                    end = self.subtitles_list[i][0] + self.subtitles_list[i][1]
                    if not start_position > (end - self.minimum_subtitle_width):
                        if self.timeline_snap and self.timeline_snap_limits and (last[0] + last[1] + self.timeline_snap_value) > start_position:
                            self.subtitles_list[i][0] = last[0] + last[1] + 0.001
                        elif self.timeline_snap and self.timeline_snap_grid:
                            if self.timeline_grid_type == 'frames':
                                difference = start_position % (1.0/self.video_metadata['framerate'])
                                self.subtitles_list[i][0] = start_position - difference
                            elif self.timeline_grid_type == 'seconds' and float(start_position) > float(float(int(start_position)+1) - float(self.timeline_snap_value)):
                                self.subtitles_list[i][0] = float(int(start_position)+1)
                            elif self.timeline_grid_type == 'seconds' and float(start_position) < float(float(int(start_position)) + float(self.timeline_snap_value)):
                                self.subtitles_list[i][0] = float(int(start_position))
                            elif self.timeline_grid_type == 'scenes' and start_position > next_scene - self.timeline_snap_value:
                                self.subtitles_list[i][0] = next_scene
                            elif self.timeline_grid_type == 'scenes' and start_position < last_scene + self.timeline_snap_value:
                                self.subtitles_list[i][0] = last_scene
                            else:
                                self.subtitles_list[i][0] = start_position
                        else:
                            self.subtitles_list[i][0] = start_position
                        self.subtitles_list[i][1] = end - self.subtitles_list[i][0]
                elif widget.subtitle_end_is_clicked:
                    end_position = (event.pos().x() + widget.offset) / widget.width_proportion
                    if not end_position < (self.subtitles_list[i][0] + self.minimum_subtitle_width):
                        if self.timeline_snap and self.timeline_snap_limits and (next[0] - self.timeline_snap_value) < end_position:
                            self.subtitles_list[i][1] = (next[0] - 0.001) - self.subtitles_list[i][0]
                        elif self.timeline_snap and self.timeline_snap_grid:
                            if self.timeline_grid_type == 'frames':
                                difference = end_position % (1.0/self.video_metadata['framerate'])
                                self.subtitles_list[i][1] = end_position - self.subtitles_list[i][0] - difference
                            elif self.timeline_grid_type == 'seconds' and float(end_position) > float(float(int(end_position)+1) - float(self.timeline_snap_value)):
                                self.subtitles_list[i][1] = float(int(end_position)+1) - self.subtitles_list[i][0]
                            elif self.timeline_grid_type == 'seconds' and float(end_position) < float(float(int(end_position)) + float(self.timeline_snap_value)):
                                self.subtitles_list[i][1] = float(int(end_position)) - self.subtitles_list[i][0]
                            elif self.timeline_grid_type == 'scenes' and end_position > next_scene - self.timeline_snap_value:
                                self.subtitles_list[i][1] = next_scene - self.subtitles_list[i][0]
                            elif self.timeline_grid_type == 'scenes' and end_position < last_scene + self.timeline_snap_value:
                                self.subtitles_list[i][1] = last_scene - self.subtitles_list[i][0]
                            else:
                                self.subtitles_list[i][1] = end_position - self.subtitles_list[i][0]
                        else:
                            self.subtitles_list[i][1] = end_position - self.subtitles_list[i][0]
                elif widget.subtitle_is_clicked:
                    if self.timeline_snap and self.timeline_snap_moving and ((next[0] - self.timeline_snap_value) < (start_position + self.subtitles_list[i][1]) or (last[0] + last[1] + self.timeline_snap_value) > start_position):
                        if (next[0] - self.timeline_snap_value) < (start_position + self.subtitles_list[i][1]):
                            self.subtitles_list[i][0] = next[0] - self.subtitles_list[i][1] - 0.001
                        else:
                            self.subtitles_list[i][0] = last[0] + last[1] + 0.001
                    elif self.timeline_snap and self.timeline_snap_grid:
                        if self.timeline_grid_type == 'frames':
                            difference = start_position % (1.0/self.video_metadata['framerate'])
                            self.subtitles_list[i][0] = start_position - difference
                        elif self.timeline_grid_type == 'seconds' and float(start_position) > float(float(int(start_position)+1) - float(self.timeline_snap_value)):
                            self.subtitles_list[i][0] = float(int(start_position)+1)
                        elif self.timeline_grid_type == 'seconds' and float(start_position) < float(float(int(start_position)) + float(self.timeline_snap_value)):
                            self.subtitles_list[i][0] = float(int(start_position))
                        elif self.timeline_grid_type == 'scenes' and start_position > next_scene - self.timeline_snap_value:
                            self.subtitles_list[i][0] = next_scene
                        elif self.timeline_grid_type == 'scenes' and start_position < last_scene + self.timeline_snap_value:
                            self.subtitles_list[i][0] = last_scene
                        else:
                            self.subtitles_list[i][0] = start_position
                    else:
                        self.subtitles_list[i][0] = start_position
            if event.pos().y() > widget.subtitle_y and event.pos().y() < (widget.subtitle_height + widget.subtitle_y):
                widget.show_limiters = True
            else:
                widget.show_limiters = False
            if widget.is_cursor_pressing and not (widget.subtitle_start_is_clicked or widget.subtitle_end_is_clicked or widget.subtitle_is_clicked):
                self.player_widget.seek((event.pos().x() / widget.width())*self.video_metadata['duration'])
                update_timecode_label(self)
            widget.update()

        def mouseDoubleClickEvent(widget, event):
            widget.update()

        def resizeEvent(widget, event):
            widget.width_proportion = widget.width()/self.video_metadata.get('duration', 0.01)
            widget.subtitle_height = widget.height()-65

    self.timeline_widget = timeline(self)
    self.timeline_widget.setObjectName('timeline_widget')
    self.timeline_widget.setMouseTracking(True)

    class timeline_scroll(QScrollArea):
        def enterEvent(widget, event):
            None

        def leaveEvent(widget, event):
            None

        def wheelEvent(widget, event):
            self.timeline_scroll.horizontalScrollBar().setValue(self.timeline_scroll.horizontalScrollBar().value() + event.angleDelta().y())

    self.timeline_scroll = timeline_scroll(parent=self.playercontrols_widget)
    self.timeline_scroll.setObjectName('timeline_scroll')
    self.timeline_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    self.timeline_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
    self.timeline_scroll.setWidget(self.timeline_widget)

    def thread_get_waveform_ended(command):
        self.video_metadata['waveform'][command[0]] = {'points': command[1], 'qimages': []}
        self.videoinfo_label.setText('Waveform updated')
        self.timeline_widget.update()
        self.thread_get_qimages.values_list = command[1]
        self.thread_get_qimages.zoom = command[0]
        self.thread_get_qimages.width = self.timeline_scroll.width()
        self.thread_get_qimages.start(QThread.IdlePriority)

    self.thread_get_waveform = thread_get_waveform(self)
    self.thread_get_waveform.command.connect(thread_get_waveform_ended)

    def thread_get_qimages_ended(command):
        self.video_metadata['waveform'][command[0]]['qimages'] = command[1]
        self.videoinfo_label.setText('Waveform optimized')
        self.timeline_widget.update()

    self.thread_get_qimages = thread_get_qimages(self)
    self.thread_get_qimages.command.connect(thread_get_qimages_ended)


def resized(self):
    self.timeline_scroll.setGeometry(0, self.playercontrols_widget_central_bottom_background.y(), self.playercontrols_widget.width(), self.playercontrols_widget.height()-self.playercontrols_widget_central_bottom_background.y())
    update_timeline(self)


def update_timeline(self):
    self.timeline_widget.setGeometry(0, -40, self.video_metadata.get('duration', 0.01)*self.mediaplayer_zoom, self.timeline_scroll.height()-15)


def update_scrollbar(self, position=0):
    if position == 'middle':
        offset = self.timeline_scroll.width()*.5
    elif type(position) == float:
        offset = self.timeline_scroll.width()*position
    elif type(position) == int:
        offset = position
    # self.timeline_scroll.horizontalScrollBar().setValue(self.player_widget.mpv.time_pos * (self.timeline_widget.width()/self.video_metadata.get('duration', 0.01)) - offset)
    self.timeline_scroll.horizontalScrollBar().setValue(self.player_widget.position * (self.timeline_widget.width()/self.video_metadata.get('duration', 0.01)) - offset)


def update_timecode_label(self):
    self.playercontrols_timecode_label.setText(str(timecode.Timecode('1000', start_seconds=self.player_widget.position, fractional=True)))


def update(self):
    self.player.update_subtitle_layer(self)
    if self.repeat_activated and not self.repeat_duration_tmp:
        self.repeat_duration_tmp = [[self.player_widget.position, self.player_widget.position + self.repeat_duration] for i in range(self.repeat_times)]
    if self.repeat_activated and self.repeat_duration_tmp and self.player_widget.position > self.repeat_duration_tmp[0][1]:
        self.player_widget.position = self.repeat_duration_tmp[0][0]
        self.player_widget.mpv.wait_for_property('seekable')
        self.player_widget.mpv.seek(self.player_widget.position, reference='absolute')
        pos = self.repeat_duration_tmp.pop(0)
        self.repeat_duration_tmp.append([pos[1], pos[1] + self.repeat_duration])
    if (self.player_widget.position * (self.timeline_widget.width()/self.video_metadata.get('duration', 0.01))) > self.timeline_scroll.width() + self.timeline_scroll.horizontalScrollBar().value():
        update_scrollbar(self)
    update_timecode_label(self)
    self.timeline_widget.update()


def zoom_update_waveform(self):
    if not type(self.video_metadata['audio']) == bool and self.mediaplayer_zoom not in self.video_metadata['waveform'].keys():
        self.videoinfo_label.setText('Generating waveform...')
        self.thread_get_waveform.audio = self.video_metadata['audio']
        self.thread_get_waveform.zoom = self.mediaplayer_zoom
        self.thread_get_waveform.duration = self.video_metadata.get('duration', 0.01)
        self.thread_get_waveform.start(QThread.IdlePriority)
