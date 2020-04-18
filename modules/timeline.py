#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
from bisect import bisect
import timecode
from PyQt5.QtGui import QIcon, QPainter, QPen, QColor, QPolygonF, QPixmap, QFont, QImage
from PyQt5.QtWidgets import QPushButton, QLabel, QFileDialog, QSpinBox, QDoubleSpinBox, QWidget, QScrollArea
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, Qt, QSize, QRect, QPointF, QThread, pyqtSignal

from modules import waveform
from modules import history

class thread_get_waveform(QThread):
    command = pyqtSignal(QImage)
    zoom = False
    audio = False
    duration = False
    width = False
    height = False
    def run(self):
        #if self.audio.any() and not self.zoom == False and not self.duration == False and not self.audio == False and not self.width == False and not self.height == False:
        #result = {self.zoom : waveform.get_waveform_zoom(zoom=self.zoom, duration=self.duration, audio=self.audio, width=self.width, height=self.height)}
        self.command.emit(waveform.get_waveform_zoom(zoom=self.zoom, duration=self.duration, audio=self.audio, width=self.width, height=self.height))

def get_timeline_time_str(seconds):
    secs = int(seconds % 60)
    mins = int((seconds / 60) % 60)
    hrs = int((seconds / 60) / 60)

    if hrs:
        return "{hh:02d}:{mm:02d}:{ss:02d}".format(hh=hrs, mm=mins, ss=secs )
    elif mins:
        return "{mm:02d}:{ss:02d}".format(mm=mins, ss=secs )
    else:
        return "{ss:02d}".format(ss=secs )


def load(self, PATH_SUBTITLD_GRAPHICS):
    class timeline(QWidget):
        subtitle_is_clicked = False
        subtitle_start_is_clicked = False
        subtitle_end_is_clicked = False
        width_proportion =  self.width()/self.video_metadata.get('duration', 0.01)
        subtitle_height = 50#height()-20
        subtitle_y = 55
        offset = 0.0
        show_limiters = False
        is_cursor_pressing = False
        def paintEvent(widget, paintEvent):
            painter = QPainter(widget)
            scroll_position = self.timeline_scroll.horizontalScrollBar().value()
            scroll_width = widget.width()

            painter.setRenderHint(QPainter.Antialiasing)

            painter.setOpacity(self.mediaplayer_opacity)
            if self.mediaplayer_view_mode and self.video_metadata.get('waveform', {}):
                if self.mediaplayer_view_mode in ['waveform', 'verticalform']:
                    if self.video_metadata.get('waveform', False):
                        p = self.video_metadata['waveform'].width()/widget.width()
                        painter.drawPixmap(scroll_position, 43, scroll_width, widget.height() - 40, QPixmap(self.video_metadata['waveform'].copy(scroll_position*p, 0, scroll_width*p, widget.height() - 40))) #
                    # zoom_values = sorted(self.video_metadata.get('waveform', {}).keys())[1:]
                    # if len(zoom_values) > 0:
                    #     if self.mediaplayer_zoom in zoom_values:
                    #         waveform = self.video_metadata.get('waveform', {})[self.mediaplayer_zoom]
                    #         #painter.drawPixmap(0, 40, waveform)
                    #     #else:
                    #     #    waveform = self.video_metadata.get('waveform', {})[zoom_values[bisect(zoom_values, self.mediaplayer_zoom)]]
                    #         p = waveform.width()/widget.width()
                    #         painter.drawPixmap(scroll_position, 43, scroll_width, widget.height() - 40, QPixmap(waveform.copy(scroll_position*p, 0, scroll_width*p, widget.height() - 40))) #

            if self.subtitles_list:
                painter.setOpacity(1)
                painter.setPen(QPen(QColor.fromRgb(240,240,240,200), 1, Qt.SolidLine))
                for subtitle in self.subtitles_list:
                    if ((subtitle[0] / self.video_metadata.get('duration', 0.01)) > (scroll_position / widget.width()) or ((subtitle[0] + subtitle[1]) / self.video_metadata.get('duration', 0.01)) > (scroll_position / widget.width())) and ((subtitle[0] / self.video_metadata.get('duration', 0.01)) < ((scroll_position + scroll_width) / widget.width()) or ((subtitle[0] + subtitle[1]) / self.video_metadata.get('duration', 0.01)) < ((scroll_position + scroll_width) / widget.width())):
                        if self.selected_subtitle == subtitle:
                            painter.setPen(QColor.fromRgb(48,66,81,alpha=255))
                            painter.setBrush(QColor.fromRgb(62,83,99,alpha=220))
                        else:
                            painter.setPen(QColor.fromRgb(106,116,131,alpha=255))
                            painter.setBrush(QColor.fromRgb(184,206,224,alpha=220))

                        subtitle_rect = QRect(  subtitle[0] * widget.width_proportion ,
                                            widget.subtitle_y,
                                            subtitle[1] * widget.width_proportion,
                                            widget.subtitle_height
                                        )
                        #painter.setBrush(QColor.fromRgb(200,200,200,alpha=200))

                        painter.drawRoundedRect(subtitle_rect,2.0,2.0,Qt.AbsoluteSize)

                        if self.selected_subtitle == subtitle:
                            painter.setPen(QColor.fromRgb(255,255,255,alpha=255))
                            #painter.setBrush(QColor.fromRgb(62,83,99,alpha=220))
                        else:
                            painter.setPen(QColor.fromRgb(48,66,81,alpha=255))
                            #painter.setBrush(QColor.fromRgb(184,206,224,alpha=220))

                        painter.drawText(subtitle_rect,Qt.AlignCenter | Qt.TextWrapAnywhere,subtitle[2])

                        if widget.show_limiters and (subtitle[1] * widget.width_proportion) > 40:
                            painter.setPen(Qt.NoPen)
                            lim_rect = QRect(  (subtitle[0] * widget.width_proportion) + 2 ,
                                                widget.subtitle_y + 2,
                                                18,
                                                widget.subtitle_height - 4
                                            )

                            painter.drawRoundedRect(lim_rect,1.0,1.0,Qt.AbsoluteSize)
                            painter.setPen(QColor.fromRgb(150,150,150,alpha=255))
                            painter.drawText(lim_rect,Qt.AlignCenter, '❮')

                            painter.setPen(Qt.NoPen)
                            lim_rect = QRect(  (subtitle[0] * widget.width_proportion) + (subtitle[1] * widget.width_proportion) - 20,
                                                widget.subtitle_y + 2,
                                                18,
                                                widget.subtitle_height - 4
                                            )

                            painter.drawRoundedRect(lim_rect,1.0,1.0,Qt.AbsoluteSize)
                            painter.setPen(QColor.fromRgb(150,150,150,alpha=255))
                            painter.drawText(lim_rect,Qt.AlignCenter, '❯')
                painter.setOpacity(1)

            grid_pen = QPen(QColor.fromRgb(106,116,131,20), 1, Qt.SolidLine)
            painter.setFont(QFont('Ubuntu Mono', 8))
            x = 0
            for sec in range(int(self.video_metadata['duration'])):
                if x >= scroll_position and x <= (scroll_position + self.timeline_scroll.width()):
                    if (self.mediaplayer_zoom > 75) or (self.mediaplayer_zoom > 50 and self.mediaplayer_zoom <= 75 and not int((sec % 2))) or (self.mediaplayer_zoom > 25 and self.mediaplayer_zoom <= 50 and not int((sec % 4))) or (self.mediaplayer_zoom <= 25 and not int((sec % 8))):
                        lim_rect = QRect(  x+3,
                                            27,
                                            50,
                                            20
                                        )
                        painter.setPen(QColor.fromRgb(106,116,131,alpha=50))
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

            painter.setPen(QPen(QColor.fromRgb(255,0,0,200), 2, Qt.SolidLine))
            cursor_pos = self.current_timeline_position * widget.width_proportion
            painter.drawLine(cursor_pos, 0, cursor_pos, widget.height())

            painter.end()

        def mousePressEvent(widget, event):
            widget.is_cursor_pressing = True
            scroll_position = self.timeline_scroll.horizontalScrollBar().value()

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
                self.current_timeline_position = (event.pos().x() / widget.width())*self.video_metadata['duration']
                self.player_widget.mpv.wait_for_property('seekable')
                self.player_widget.mpv.seek(self.current_timeline_position, reference='absolute')#, precision='exact')
                update_timecode_label(self)

            self.properties.update_properties_widget(self)

            if (widget.subtitle_is_clicked or widget.subtitle_start_is_clicked or widget.subtitle_end_is_clicked):
                history.history_append(self.subtitles_list)

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
                last = self.subtitles_list[self.subtitles_list.index(self.selected_subtitle)-1] if self.subtitles_list.index(self.selected_subtitle) > 0 else [0,0,'']
                next = self.subtitles_list[self.subtitles_list.index(self.selected_subtitle)+1] if self.subtitles_list.index(self.selected_subtitle) < len(self.subtitles_list) - 1 else [self.video_metadata['duration'],0,'']
                scenes_list = self.video_metadata['scenes'] if len(self.video_metadata['scenes']) > 1 else [0.0]
                scenes_list.append(self.video_metadata['duration'])
                start_position = (event.pos().x() - widget.offset) / widget.width_proportion
                last_scene = scenes_list[bisect(scenes_list, start_position)-1]
                next_scene = scenes_list[bisect(scenes_list, start_position)]
                #print('mouse moved ' + str(event.pos().x()) + ' x ' + str(event.pos().y()))
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
            if event.pos().y() > widget.subtitle_y and event.pos().y() < (widget.subtitle_height + widget.subtitle_y):# and (((event.pos().x())/widget.width_proportion) > subtitle[0] and ((event.pos().x())/widget.width_proportion) < (subtitle[0] + subtitle[1])):
                widget.show_limiters = True
            else:
                widget.show_limiters = False
            if widget.is_cursor_pressing and not (widget.subtitle_start_is_clicked or widget.subtitle_end_is_clicked or widget.subtitle_is_clicked):
                self.current_timeline_position = (event.pos().x() / widget.width())*self.video_metadata['duration']
                self.player_widget.mpv.wait_for_property('seekable')
                self.player_widget.mpv.seek(self.current_timeline_position, reference='absolute')#, precision='exact')
                update_timecode_label(self)
            widget.update()

        def mouseDoubleClickEvent(widget, event):
            #self.player_controls.new_note(self)
            widget.update()

        def resizeEvent(widget, event):
            widget.width_proportion =  widget.width()/self.video_metadata.get('duration', 0.01)
            widget.subtitle_height = widget.height()-65
            #widget.subtitle_height = widget.height()-20

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
    #self.timeline_scroll.horizontalScrollBar().valueChanged.connect(lambda:timeline_scroll_updated(self))


    def thread_get_waveform_ended(command):
        #zoom = [*command.keys()][0]
        self.video_metadata['waveform'] = command
        self.videoinfo_label.setText('Waveform updated')
        self.timeline_widget.update()

    self.thread_get_waveform = thread_get_waveform(self)
    self.thread_get_waveform.command.connect(thread_get_waveform_ended)

def resized(self):
    self.timeline_scroll.setGeometry(0,self.playercontrols_widget_central_bottom_background.y(),self.playercontrols_widget.width(),self.playercontrols_widget.height()-self.playercontrols_widget_central_bottom_background.y())
    update_timeline(self)
    #self.timeline_widget.setGeometry(0,0,self.timeline_scroll.width(),self.timeline_scroll.height())
    #self.timeline_widget.setGeometry(0,0,self.video_metadata.get('duration', 0.01)*self.mediaplayer_zoom,self.timeline_scroll.height()-20)

def update_timeline(self):
    self.timeline_widget.setGeometry(0,-40,self.video_metadata.get('duration', 0.01)*self.mediaplayer_zoom,self.timeline_scroll.height()-15)

def update_scrollbar(self, position=0):
    if position == 'middle':
        offset = self.timeline_scroll.width()*.5
    elif type(position) == float:
        offset = self.timeline_scroll.width()*position
    elif type(position) == int:
        offset = position
    self.timeline_scroll.horizontalScrollBar().setValue(self.player_widget.mpv.time_pos * (self.timeline_widget.width()/self.video_metadata.get('duration', 0.01)) - offset)

def update_timecode_label(self):
    self.playercontrols_timecode_label.setText(str(timecode.Timecode('1000', start_seconds=self.current_timeline_position, fractional=True)))

def update(self):
    if self.player_widget.mpv.time_pos and self.mediaplayer_is_playing:
        self.current_timeline_position = self.player_widget.mpv.time_pos
        if (self.player_widget.mpv.time_pos * (self.timeline_widget.width()/self.video_metadata.get('duration', 0.01))) > self.timeline_scroll.width() + self.timeline_scroll.horizontalScrollBar().value():
            update_scrollbar(self)
    update_timecode_label(self)
    self.timeline_widget.update()

def zoom_update_waveform(self):
    #if not type(self.video_metadata['waveform'][0]) == bool and not self.mediaplayer_zoom in self.video_metadata.get('waveform', {}).keys():
    if not type(self.video_metadata['audio']) == bool:
        self.videoinfo_label.setText('Generating waveform...')
        #self.thread_get_waveform.audio = self.video_metadata['waveform'][0]
        self.thread_get_waveform.audio = self.video_metadata['audio']
        self.thread_get_waveform.zoom = self.mediaplayer_zoom
        self.thread_get_waveform.duration = self.video_metadata.get('duration', 0.01)
        self.thread_get_waveform.width = self.timeline_widget.width()
        self.thread_get_waveform.height = self.timeline_widget.height()-40
        self.thread_get_waveform.start(QThread.IdlePriority)
