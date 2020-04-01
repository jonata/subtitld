#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
from PyQt5.QtGui import QIcon, QPainter, QPen, QColor, QPolygonF
from PyQt5.QtWidgets import QPushButton, QLabel, QFileDialog, QSpinBox, QDoubleSpinBox, QWidget, QScrollArea
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, Qt, QSize, QRect, QPointF

def load(self, PATH_SUBTITLD_GRAPHICS):
    class timeline(QWidget):
        subtitle_is_clicked = False
        subtitle_start_is_clicked = False
        subtitle_end_is_clicked = False
        width_proportion =  self.width()/self.video_metadata.get('duration', 0.01)
        subtitle_height = 80#height()-20
        subtitle_y = 35
        offset = 0.0
        show_limiters = False
        is_cursor_pressing = False
        def paintEvent(widget, paintEvent):
            painter = QPainter(widget)
            scroll_position = self.timeline_scroll.horizontalScrollBar().value()
            scroll_width = widget.width()

            painter.setRenderHint(QPainter.Antialiasing)
            if self.subtitles_list:
                if self.mediaplayer_view_mode and self.video_metadata.get('waveform', {}):
                    if self.mediaplayer_view_mode in ['waveform', 'verticalform']:
                        if len([*self.video_metadata.get('waveform', {})]) > 1:
                            if self.mediaplayer_zoom in [*self.video_metadata.get('waveform', {})]:
                                waveform = self.video_metadata.get('waveform', {})[self.mediaplayer_zoom]
                            else:
                                for zoom in sorted(self.video_metadata.get('waveform', {}).keys()):
                                    if zoom > self.mediaplayer_zoom:
                                        break
                                    else:
                                        last_zoom = zoom
                                    waveform = self.video_metadata.get('waveform', {})[last_zoom]

                            painter.setOpacity(self.mediaplayer_opacity)

                            painter.drawPixmap(0, 30, waveform)

                painter.setOpacity(1)

                painter.setPen(QPen(QColor.fromRgb(240,240,240,200), 1, Qt.SolidLine))
                painter.setBrush(QColor.fromRgb(240,240,240,alpha=50))

                for subtitle in self.subtitles_list:
                    if ((subtitle[0] / self.video_metadata.get('duration', 0.01)) > (scroll_position / widget.width()) or ((subtitle[0] + subtitle[1]) / self.video_metadata.get('duration', 0.01)) > (scroll_position / widget.width())) and ((subtitle[0] / self.video_metadata.get('duration', 0.01)) < ((scroll_position + scroll_width) / widget.width()) or ((subtitle[0] + subtitle[1]) / self.video_metadata.get('duration', 0.01)) < ((scroll_position + scroll_width) / widget.width())):
                        if self.selected_subtitle == subtitle:
                            painter.setPen(QColor.fromRgb(0,0,0,alpha=255))
                        else:
                            painter.setPen(QColor.fromRgb(255,255,255,alpha=255))

                        subtitle_rect = QRect(  subtitle[0] * widget.width_proportion ,
                                            widget.subtitle_y,
                                            subtitle[1] * widget.width_proportion,
                                            widget.subtitle_height
                                        )
                        painter.setBrush(QColor.fromRgb(200,200,200,alpha=200))

                        painter.drawRoundedRect(subtitle_rect,2.0,2.0,Qt.AbsoluteSize)
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


            painter.setPen(QPen(QColor.fromRgb(255,0,0,200), 4, Qt.SolidLine))

            cursor_pos = self.current_timeline_position * widget.width_proportion
            painter.drawLine(cursor_pos, 3, cursor_pos, widget.height())

            painter.end()

        def mousePressEvent(widget, event):
            widget.is_cursor_pressing = True
            scroll_position = self.timeline_scroll.horizontalScrollBar().value()

            self.selected_subtitle = False

            for subtitle in self.subtitles_list:
                if event.pos().y() > 40 and event.pos().y() < (widget.subtitle_height + 40) and (((event.pos().x())/widget.width_proportion) > subtitle[0] and ((event.pos().x())/widget.width_proportion) < (subtitle[0] + subtitle[1])):
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
            if event.pos().y() > 40 and event.pos().y() < (widget.subtitle_height + 40):# and (((event.pos().x())/widget.width_proportion) > subtitle[0] and ((event.pos().x())/widget.width_proportion) < (subtitle[0] + subtitle[1])):
                widget.show_limiters = True
            else:
                widget.show_limiters = False
            if widget.is_cursor_pressing and not (widget.subtitle_start_is_clicked or widget.subtitle_end_is_clicked or widget.subtitle_is_clicked):
                self.current_timeline_position = (event.pos().x() / widget.width())*self.video_metadata['duration']
                self.player_widget.mpv.wait_for_property('seekable')
                self.player_widget.mpv.seek(self.current_timeline_position, reference='absolute')#, precision='exact')
            widget.update()

        def mouseDoubleClickEvent(widget, event):
            #self.player_controls.new_note(self)
            widget.update()

        def resizeEvent(widget, event):
            widget.width_proportion =  widget.width()/self.video_metadata.get('duration', 0.01)
            widget.subtitle_height = widget.height()-40
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

    self.zoomin_button = QPushButton(parent=self.playercontrols_widget)
    self.zoomin_button.setIconSize(QSize(16,17))
    self.zoomin_button.setIcon(QIcon(os.path.join(PATH_SUBTITLD_GRAPHICS, 'zoom_in_icon.png')))
    self.zoomin_button.setObjectName('button_no_left_no_bottom')
    self.zoomin_button.clicked.connect(lambda:zoomin_button_clicked(self))

    self.zoomout_button = QPushButton(parent=self.playercontrols_widget)
    self.zoomout_button.setIconSize(QSize(16,17))
    self.zoomout_button.setIcon(QIcon(os.path.join(PATH_SUBTITLD_GRAPHICS, 'zoom_out_icon.png')))
    self.zoomout_button.setObjectName('button_no_right_no_bottom')
    self.zoomout_button.clicked.connect(lambda:zoomout_button_clicked(self))

def resized(self):

    self.timeline_scroll.setGeometry(0,100,self.playercontrols_widget.width(),self.playercontrols_widget.height()-100)
    update_timeline(self)
    #self.timeline_widget.setGeometry(0,0,self.timeline_scroll.width(),self.timeline_scroll.height())
    #self.timeline_widget.setGeometry(0,0,self.video_metadata.get('duration', 0.01)*self.mediaplayer_zoom,self.timeline_scroll.height()-20)


    self.zoomin_button.setGeometry(self.timeline_scroll.width() - 80,60,40,40)
    self.zoomout_button.setGeometry(self.timeline_scroll.width() - 120,60,40,40)

def update_timeline(self):
    self.timeline_widget.setGeometry(0,0,self.video_metadata.get('duration', 0.01)*self.mediaplayer_zoom,self.timeline_scroll.height()-20)

def update_scrollbar(self, position=False):
    offset = 0
    if position == 'middle':
        offset = self.timeline_scroll.width()*.5
    self.timeline_scroll.horizontalScrollBar().setValue(self.player_widget.mpv.time_pos * (self.timeline_widget.width()/self.video_metadata.get('duration', 0.01)) - offset)

def update(self):
    if self.player_widget.mpv.time_pos and self.mediaplayer_is_playing:
        self.current_timeline_position = self.player_widget.mpv.time_pos
        if (self.player_widget.mpv.time_pos * (self.timeline_widget.width()/self.video_metadata.get('duration', 0.01))) > self.timeline_scroll.width() + self.timeline_scroll.horizontalScrollBar().value():
            update_scrollbar(self)
    self.timeline_widget.update()


def zoomin_button_clicked(self):
    self.mediaplayer_zoom += 5.0
    #if not self.mediaplayer_zoom in self.video_metadata.get('waveform', {}).keys():
    #    threading.Thread(target=waveform.get_waveform_zoom(self, self.mediaplayer_zoom, self.video_metadata['duration'], self.video_metadata['waveform'][0], self.video_metadata.get('duration', 0.01)*self.mediaplayer_zoom, self.timeline_widget.height()-30), daemon=True).start()
    self.timeline_widget.setGeometry(0,0,int(round(self.video_metadata.get('duration', 0.01)*self.mediaplayer_zoom)),self.timeline_scroll.height()-20)
    zoom_buttons_update(self)

def zoomout_button_clicked(self):
    self.mediaplayer_zoom -= 5.0
    #if not self.mediaplayer_zoom in self.video_metadata.get('waveform', {}).keys():
    #    threading.Thread(target=waveform.get_waveform_zoom(self, self.mediaplayer_zoom, self.video_metadata['duration'], self.video_metadata['waveform'][0], self.video_metadata.get('duration', 0.01)*self.mediaplayer_zoom, self.timeline_widget.height()-30), daemon=True).start()
    self.timeline_widget.setGeometry(0,0,int(round(self.video_metadata.get('duration', 0.01)*self.mediaplayer_zoom)),self.timeline_scroll.height()-20)
    zoom_buttons_update(self)

def zoom_buttons_update(self):
    self.zoomout_button.setEnabled(True if self.mediaplayer_zoom - 5.0 > 0.0 else False)
    self.zoomin_button.setEnabled(True if self.mediaplayer_zoom + 5.0 < 500.0 else False)
