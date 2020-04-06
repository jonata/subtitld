#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import bisect
import timecode
from PyQt5.QtGui import QIcon, QPainter, QPen, QColor, QPolygonF, QPixmap
from PyQt5.QtWidgets import QPushButton, QLabel, QFileDialog, QSpinBox, QDoubleSpinBox, QWidget, QScrollArea
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, Qt, QSize, QRect, QPointF, QThread, pyqtSignal

from modules import waveform

class thread_get_waveform(QThread):
    command = pyqtSignal(dict)
    zoom = False
    audio = False
    duration = False
    width = False
    height = False
    def run(self):
        #if self.audio.any() and not self.zoom == False and not self.duration == False and not self.audio == False and not self.width == False and not self.height == False:
        result = {self.zoom : waveform.get_waveform_zoom(zoom=self.zoom, duration=self.duration, audio=self.audio, width=self.width, height=self.height)}
        self.command.emit(result)

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
                    zoom_values = sorted(self.video_metadata.get('waveform', {}).keys())[1:]
                    if len(zoom_values) > 0:
                        if self.mediaplayer_zoom in zoom_values:
                            waveform = self.video_metadata.get('waveform', {})[self.mediaplayer_zoom]
                            #painter.drawPixmap(0, 40, waveform)
                        else:
                            waveform = self.video_metadata.get('waveform', {})[zoom_values[bisect.bisect(zoom_values, self.mediaplayer_zoom)]]
                        painter.drawPixmap(0, 43, widget.width(), widget.height() - 40, waveform)

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

                        if widget.show_limiters:
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


            widget.update()

        def mouseReleaseEvent(widget, event):
            widget.subtitle_is_clicked = False
            widget.subtitle_start_is_clicked = False
            widget.subtitle_end_is_clicked = False
            widget.is_cursor_pressing = False
            widget.update()

        def mouseMoveEvent(widget, event):
            if self.selected_subtitle:
                slsub = self.subtitles_list.index(self.selected_subtitle)
                #print('mouse moved ' + str(event.pos().x()) + ' x ' + str(event.pos().y()))
                if widget.subtitle_start_is_clicked:
                    last_end = self.subtitles_list[slsub][0] + self.subtitles_list[slsub][1]
                    self.subtitles_list[slsub][0] = (event.pos().x() - widget.offset) / widget.width_proportion
                    self.subtitles_list[slsub][1] = last_end - self.subtitles_list[slsub][0]
                elif widget.subtitle_end_is_clicked:
                    self.subtitles_list[slsub][1] = ((event.pos().x() + widget.offset) / widget.width_proportion) - self.subtitles_list[slsub][0]
                elif widget.subtitle_is_clicked:
                    self.subtitles_list[slsub][0] = (event.pos().x() - widget.offset) / widget.width_proportion
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
        zoom = [*command.keys()][0]
        self.video_metadata['waveform'][zoom] = command[zoom]

    self.thread_get_waveform = thread_get_waveform(self)
    self.thread_get_waveform.command.connect(thread_get_waveform_ended)

def resized(self):
    self.timeline_scroll.setGeometry(0,self.playercontrols_widget_central_bottom_background.y(),self.playercontrols_widget.width(),self.playercontrols_widget.height()-self.playercontrols_widget_central_bottom_background.y())
    update_timeline(self)
    #self.timeline_widget.setGeometry(0,0,self.timeline_scroll.width(),self.timeline_scroll.height())
    #self.timeline_widget.setGeometry(0,0,self.video_metadata.get('duration', 0.01)*self.mediaplayer_zoom,self.timeline_scroll.height()-20)



def update_timeline(self):
    self.timeline_widget.setGeometry(0,-40,self.video_metadata.get('duration', 0.01)*self.mediaplayer_zoom,self.timeline_scroll.height()-15)

def update_scrollbar(self, position=False):
    offset = 0
    if position == 'middle':
        offset = self.timeline_scroll.width()*.5
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
    if not type(self.video_metadata['waveform'][0]) == bool and not self.mediaplayer_zoom in self.video_metadata.get('waveform', {}).keys():
        self.thread_get_waveform.audio = self.video_metadata['waveform'][0]
        self.thread_get_waveform.zoom = self.mediaplayer_zoom
        self.thread_get_waveform.duration = self.video_metadata.get('duration', 0.01)
        self.thread_get_waveform.width = self.timeline_widget.width()
        self.thread_get_waveform.height = self.timeline_widget.height()-40
        self.thread_get_waveform.start(QThread.IdlePriority)
