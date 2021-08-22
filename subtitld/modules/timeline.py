"""Timeline module

"""

from bisect import bisect

from PyQt5.QtGui import QPainter, QPen, QColor, QPolygonF, QFont, QPixmap
from PyQt5.QtWidgets import QWidget, QScrollArea
from PyQt5.QtCore import Qt, QRect, QPointF, QThread, pyqtSignal, QMargins

from subtitld import timecode

from subtitld.modules import waveform
from subtitld.modules import history
from subtitld.modules import subtitles
from subtitld.modules import quality_check


class DrawPixmap(QPixmap):
    """Class to generate pixmaps for timeline"""
    waveform_up = []
    waveform_down = []
    x_offset = 0
    waveformsize = .7
    border_color = '#ff153450'
    fill_color = '#cc153450'

    def paintEvent(self):
        """Function of paintEvent for DrawPixmap"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.setPen(QPen(QColor(self.border_color), 1, Qt.SolidLine))
        painter.setBrush(QColor(self.fill_color))

        x_position = 0
        polygon = QPolygonF()
        for point in self.waveform_up:
            polygon.append(QPointF(x_position, (self.height()*.5) + (point*(self.waveformsize*100))))
            x_position += 1
        for point in reversed(self.waveform_down):
            polygon.append(QPointF(x_position, (self.height()*.5) + (point*(self.waveformsize*100))))
            x_position -= 1
        painter.drawPolygon(polygon)

        painter.end()


class ThreadGetWaveform(QThread):
    """Class of qtread to get waveform data"""
    command = pyqtSignal(list)
    zoom = False
    audio = False
    duration = False
    width = False
    height = False

    def run(self):
        """Function to run QThread"""
        positive_values, negative_values, _ = waveform.generate_waveform_zoom(zoom=self.zoom, duration=self.duration, waveform=self.audio)
        self.command.emit([self.zoom, [positive_values, negative_values]])


class ThreadGetQImages(QThread):
    """Class to generate QThread for QImages"""
    command = pyqtSignal(list)
    values_list = []
    zoom = 100.0
    width = 32767
    border_color = '#ff153450'
    fill_color = '#cc153450'

    def run(self):
        """Function to run QThread"""
        final_list = []
        parser = 0
        while True:
            qpixmap = DrawPixmap(self.width, 124)
            qpixmap.fill(QColor(0, 0, 0, 0))
            qpixmap.waveform_up = self.values_list[0][parser:parser+self.width]
            qpixmap.waveform_down = self.values_list[1][parser:parser+self.width]
            qpixmap.border_color = self.border_color
            qpixmap.fill_color = self.fill_color
            qpixmap.paintEvent()
            final_list.append(qpixmap.toImage())                # qpixmap.save('/tmp/teste.png')
            parser += self.width
            if parser > len(self.values_list[0]):
                break
        self.command.emit([self.zoom, final_list])


class Timeline(QWidget):
    """Class for timeline QWidget"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.subtitle_is_clicked = False
        self.subtitle_start_is_clicked = False
        self.subtitle_end_is_clicked = False
        self.width_proportion = self.width()/self.parent.video_metadata.get('duration', 0.01)
        self.subtitle_height = 50
        self.subtitle_y = 55
        self.offset = 0.0
        self.y_waveform = 22
        self.h_waveform = 124
        self.show_limiters = False
        self.show_tug_of_war = False
        self.tug_of_war_pressed = False
        self.is_cursor_pressing = False
        self.waveformsize = .7

    def paintEvent(self, event):
        """Function for paintEvent of Timeline"""
        painter = QPainter(self)
        scroll_position = self.parent.timeline_scroll.horizontalScrollBar().value()
        scroll_width = self.parent.timeline_scroll.width()

        painter.setRenderHint(QPainter.Antialiasing)

        painter.setOpacity(self.parent.mediaplayer_opacity)

        if self.parent.mediaplayer_view_mode and self.parent.video_metadata.get('waveform', {}):
            if self.parent.mediaplayer_view_mode in ['waveform', 'verticalform']:
                if self.parent.video_metadata.get('waveform', {}):
                    x_factor = 1
                    available_zoom = self.parent.mediaplayer_zoom
                    if available_zoom not in self.parent.video_metadata['waveform'].keys():
                        available_zoom = sorted(self.parent.video_metadata['waveform'].keys())[0]
                        x_factor = self.parent.mediaplayer_zoom/available_zoom

                    w_factor = (self.parent.video_metadata.get('duration', 0.01)*available_zoom)/len(self.parent.video_metadata['waveform'][available_zoom]['points'][0])

                    if self.parent.video_metadata['waveform'][available_zoom].get('qimages', []):
                        xpos = 0
                        for qimage in self.parent.video_metadata['waveform'][available_zoom]['qimages']:
                            wid = qimage.width()*w_factor*x_factor
                            if not xpos > scroll_position + scroll_width and not xpos + wid < scroll_position:
                                painter.drawImage(QRect(xpos, self.y_waveform, wid, self.h_waveform), qimage)
                            xpos += wid

                    elif self.parent.video_metadata['waveform'][available_zoom].get('points', []):
                        painter.setPen(QPen(QColor(self.parent.settings['timeline'].get('waveform_border_color', '#ff153450')), 1, Qt.SolidLine))
                        painter.setBrush(QColor(self.parent.settings['timeline'].get('waveform_fill_color', '#cc153450')))

                        x_position = 0
                        polygon = QPolygonF()

                        for point in self.parent.video_metadata['waveform'][available_zoom]['points'][0][int(scroll_position/(x_factor*w_factor)):int((scroll_position+scroll_width)/(x_factor*w_factor))]:
                            polygon.append(QPointF((x_position+scroll_position), self.y_waveform + (self.h_waveform*.5) + (point*(self.waveformsize*100))))
                            x_position += (x_factor*w_factor)

                        for point in reversed(self.parent.video_metadata['waveform'][available_zoom]['points'][1][int(scroll_position/(x_factor*w_factor)):int((scroll_position+scroll_width)/(x_factor*w_factor))]):
                            polygon.append(QPointF((x_position+scroll_position), self.y_waveform + (self.h_waveform*.5) + (point*(self.waveformsize*100))))
                            x_position -= (x_factor*w_factor)

                        painter.drawPolygon(polygon)

        if self.parent.subtitles_list:
            painter.setOpacity(1)
            # painter.setPen(QPen(QColor.fromRgb(240, 240, 240, 200), 1, Qt.SolidLine))

            for subtitle in self.parent.subtitles_list:
                if (subtitle[0] / self.parent.video_metadata.get('duration', 0.01)) > ((scroll_position + scroll_width) / self.width()):
                    break
                elif (subtitle[0] + subtitle[1]) / self.parent.video_metadata.get('duration', 0.01) < (scroll_position / self.width()):
                    continue
                else:
                    if self.parent.selected_subtitle == subtitle:
                        painter.setPen(QColor(self.parent.settings['timeline'].get('selected_subtitle_border_color', '#ff304251')))
                        painter.setBrush(QColor(self.parent.settings['timeline'].get('selected_subtitle_fill_color', '#cc3e5363')))
                    else:
                        painter.setPen(QColor(self.parent.settings['timeline'].get('subtitle_border_color', '#ff6a7483')))
                        painter.setBrush(QColor(self.parent.settings['timeline'].get('subtitle_fill_color', '#ccb8cee0')))

                    subtitle_rect = QRect(subtitle[0] * self.width_proportion,
                                            self.subtitle_y,
                                            subtitle[1] * self.width_proportion,
                                            self.subtitle_height)

                    painter.drawRoundedRect(subtitle_rect, 2.0, 2.0, Qt.AbsoluteSize)

                    approved, _ = quality_check.check_subtitle(subtitle, self.parent.settings['quality_check'])
                    if self.parent.settings['quality_check'].get('enabled', False) and not approved:
                        painter.setPen(QColor('#9e1a1a'))
                    elif self.parent.selected_subtitle == subtitle:
                        painter.setPen(QColor(self.parent.settings['timeline'].get('selected_subtitle_text_color', '#ffffffff')))
                    else:
                        painter.setPen(QColor(self.parent.settings['timeline'].get('subtitle_text_color', '#ff304251')))

                    subtitle_rect -= QMargins(22, 2, 22, 2)
                    painter.drawText(subtitle_rect, Qt.AlignCenter | Qt.TextWordWrap, subtitle[2])

                    if self.show_limiters and (subtitle[1] * self.width_proportion) > 40:
                        painter.setPen(Qt.NoPen)
                        lim_rect = QRect(
                                            (subtitle[0] * self.width_proportion) + 2,
                                            self.subtitle_y + 2,
                                            18,
                                            self.subtitle_height - 4
                                        )

                        painter.drawRoundedRect(lim_rect, 1.0, 1.0, Qt.AbsoluteSize)

                        if self.parent.selected_subtitle == subtitle:
                            painter.setPen(QColor(self.parent.settings['timeline'].get('selected_subtitle_arrow_color', '#ff969696')))
                        else:
                            painter.setPen(QColor(self.parent.settings['timeline'].get('subtitle_arrow_color', '#ff969696')))

                        painter.drawText(lim_rect, Qt.AlignCenter, '❮')

                        painter.setPen(Qt.NoPen)
                        lim_rect = QRect(
                                            (subtitle[0] * self.width_proportion) + (subtitle[1] * self.width_proportion) - 20,
                                            self.subtitle_y + 2,
                                            18,
                                            self.subtitle_height - 4
                                        )

                        painter.drawRoundedRect(lim_rect, 1.0, 1.0, Qt.AbsoluteSize)

                        if self.parent.selected_subtitle == subtitle:
                            painter.setPen(QColor(self.parent.settings['timeline'].get('selected_subtitle_arrow_color', '#ff969696')))
                        else:
                            painter.setPen(QColor(self.parent.settings['timeline'].get('subtitle_arrow_color', '#ff969696')))

                        painter.drawText(lim_rect, Qt.AlignCenter, '❯')

            painter.setOpacity(1)

        grid_pen = QPen(QColor(self.parent.settings['timeline'].get('grid_color', '#336a7483')), 1, Qt.SolidLine)
        painter.setFont(QFont('Ubuntu Mono', 8))
        xpos = 0
        for sec in range(int(self.parent.video_metadata['duration'])):
            if xpos >= scroll_position and xpos <= (scroll_position + self.parent.timeline_scroll.width()):
                if (self.parent.mediaplayer_zoom > 75) or (self.parent.mediaplayer_zoom > 50 and self.parent.mediaplayer_zoom <= 75 and not int((sec % 2))) or (self.parent.mediaplayer_zoom > 25 and self.parent.mediaplayer_zoom <= 50 and not int((sec % 4))) or (self.parent.mediaplayer_zoom <= 25 and not int((sec % 8))):
                    lim_rect = QRect(
                                        xpos+3,
                                        27,
                                        50,
                                        20
                                    )
                    painter.setPen(QColor(self.parent.settings['timeline'].get('time_text_color', '#806a7483')))
                    painter.drawText(lim_rect, Qt.AlignLeft, get_timeline_time_str(sec))
                if self.parent.timeline_show_grid and self.parent.timeline_grid_type == 'seconds':
                    painter.setPen(grid_pen)
                    painter.drawLine(xpos, 0, xpos, self.height())
            xpos += self.width_proportion
        if self.parent.timeline_show_grid and self.parent.timeline_grid_type == 'frames':
            painter.setPen(grid_pen)
            xpos = 0.0
            for _ in range(int(self.parent.video_metadata['duration']*self.parent.video_metadata['framerate'])):
                if xpos >= scroll_position and xpos <= (scroll_position + self.parent.timeline_scroll.width()):
                    painter.drawLine(xpos, 0, xpos, self.height())
                xpos += self.width_proportion/self.parent.video_metadata['framerate']
        elif self.parent.timeline_show_grid and self.parent.timeline_grid_type == 'scenes' and self.parent.video_metadata['scenes']:
            painter.setPen(grid_pen)
            for scene in self.parent.video_metadata['scenes']:
                xpos = (scene*self.width_proportion)
                if xpos >= scroll_position and xpos <= (scroll_position + self.parent.timeline_scroll.width()):
                    painter.drawLine(xpos, 0, xpos, self.height())

        if bool(self.show_tug_of_war):
            tug_of_war_pen = QPen(QColor(self.parent.settings['timeline'].get('selected_subtitle_arrow_color', '#ff969696')), 4, Qt.SolidLine, Qt.RoundCap)
            painter.setPen(tug_of_war_pen)
            xpos = (self.show_tug_of_war * self.width_proportion) - 4
            y_tug_pos = 0
            for l in range(6):
                painter.drawLine(xpos, self.subtitle_y + 8 + y_tug_pos, xpos + 8, self.subtitle_y + 8 + y_tug_pos)
                # painter.drawLine(xpos, self.subtitle_y + 8 + y_tug_pos, xpos + 8, self.subtitle_y + self.subtitle_height - 8)
                y_tug_pos += (self.subtitle_height - 8)/6

        if self.parent.player_widget.position is not None:
            painter.setPen(QPen(QColor(self.parent.settings['timeline'].get('cursor_color', '#ccff0000')), 2, Qt.SolidLine))
            cursor_pos = self.parent.player_widget.position * self.width_proportion
            painter.drawLine(cursor_pos, 0, cursor_pos, self.height())

        painter.end()
        event.accept()

    def mousePressEvent(self, event):
        """Function to call when mouse is pressed"""
        scroll_position = self.parent.timeline_scroll.horizontalScrollBar().value()
        scroll_width = self.parent.timeline_scroll.width()

        cursor_is_out_of_view = bool(self.parent.player_widget.position * self.width_proportion < self.parent.timeline_scroll.horizontalScrollBar().value() or self.parent.player_widget.position * self.width_proportion > self.parent.timeline_scroll.width() + self.parent.timeline_scroll.horizontalScrollBar().value())

        self.is_cursor_pressing = True
        self.parent.selected_subtitle = False

        for subtitle in self.parent.subtitles_list:
            if (subtitle[0] / self.parent.video_metadata.get('duration', 0.01)) > ((scroll_position + scroll_width) / self.width()):
                break
            elif (subtitle[0] + subtitle[1]) / self.parent.video_metadata.get('duration', 0.01) < (scroll_position / self.width()):
                continue
            else:
                if event.pos().y() > self.subtitle_y and event.pos().y() < (self.subtitle_height + self.subtitle_y) and (((event.pos().x())/self.width_proportion) > subtitle[0] and ((event.pos().x())/self.width_proportion) < (subtitle[0] + subtitle[1])):
                    self.parent.selected_subtitle = subtitle
                    if event.pos().x()/self.width_proportion > (subtitle[0] + subtitle[1]) - (20/self.width_proportion):
                        self.subtitle_end_is_clicked = True
                        self.offset = ((self.parent.selected_subtitle[0] + self.parent.selected_subtitle[1])*self.width_proportion) - event.pos().x()
                        self.tug_of_war_pressed = self.show_tug_of_war
                    else:
                        self.offset = event.pos().x() - self.parent.selected_subtitle[0]*self.width_proportion
                        if event.pos().x()/self.width_proportion < subtitle[0] + (20/self.width_proportion):
                            self.subtitle_start_is_clicked = True
                            self.tug_of_war_pressed = self.show_tug_of_war
                        else:
                            self.subtitle_is_clicked = True
                    break

        if not (self.subtitle_end_is_clicked or self.subtitle_start_is_clicked or self.subtitle_is_clicked) or cursor_is_out_of_view:
            self.parent.player_widget.position = (event.pos().x() / self.width())*self.parent.video_metadata['duration']
            self.parent.player_widget.seek(self.parent.player_widget.position)
            if self.parent.repeat_activated:
                self.parent.repeat_duration_tmp = []
            update_timecode_label(self.parent)

        self.parent.properties.update_properties_widget(self.parent)

        if (self.subtitle_is_clicked or self.subtitle_start_is_clicked or self.subtitle_end_is_clicked):
            history.history_append(self.parent.subtitles_list)
            self.parent.unsaved = True

        self.update()

    def mouseReleaseEvent(self, event):
        """Function to call when mouse press is released"""
        self.subtitle_is_clicked = False
        self.subtitle_start_is_clicked = False
        self.subtitle_end_is_clicked = False
        self.is_cursor_pressing = False
        self.tug_of_war_pressed = False
        self.update()
        event.accept()

    def mouseMoveEvent(self, event):
        scroll_position = self.parent.timeline_scroll.horizontalScrollBar().value()
        scroll_width = self.parent.timeline_scroll.width()
        """Function to call when mouse moves"""

        self.show_limiters = bool(event.pos().y() > self.subtitle_y and event.pos().y() < (self.subtitle_height + self.subtitle_y))

        for subtitle in self.parent.subtitles_list:
            last = self.parent.subtitles_list[self.parent.subtitles_list.index(subtitle)-1] if self.parent.subtitles_list.index(subtitle) > 0 else [0, 0, '']
            nextsub = self.parent.subtitles_list[self.parent.subtitles_list.index(subtitle)+1] if self.parent.subtitles_list.index(subtitle) < len(self.parent.subtitles_list) - 1 else [self.parent.video_metadata['duration'], 0, '']

            if subtitle[0] + subtitle[1] > event.pos().x()/self.width_proportion > (subtitle[0] + subtitle[1]) - (4/self.width_proportion) and nextsub[0] < (subtitle[0] + subtitle[1] + .02):
                self.show_tug_of_war = subtitle[0] + subtitle[1] + .0005
                break
            elif subtitle[0] < event.pos().x()/self.width_proportion < subtitle[0] + (4/self.width_proportion) and last[0] + last[1] > subtitle[0] - .02:
                self.show_tug_of_war = subtitle[0] - .0005
                break
            elif not self.tug_of_war_pressed:
                self.show_tug_of_war = False

        if self.parent.selected_subtitle:
            i = self.parent.subtitles_list.index(self.parent.selected_subtitle)
            last = self.parent.subtitles_list[self.parent.subtitles_list.index(self.parent.selected_subtitle)-1] if self.parent.subtitles_list.index(self.parent.selected_subtitle) > 0 else [0, 0, '']
            nextsub = self.parent.subtitles_list[self.parent.subtitles_list.index(self.parent.selected_subtitle)+1] if self.parent.subtitles_list.index(self.parent.selected_subtitle) < len(self.parent.subtitles_list) - 1 else [self.parent.video_metadata['duration'], 0, '']
            scenes_list = self.parent.video_metadata['scenes'] if len(self.parent.video_metadata['scenes']) > 1 else [0.0]
            scenes_list.append(self.parent.video_metadata['duration'])
            start_position = (event.pos().x() - self.offset) / self.width_proportion
            last_scene = scenes_list[bisect(scenes_list, start_position)-1]
            next_scene = scenes_list[bisect(scenes_list, start_position)]


            if self.subtitle_start_is_clicked:
                end = self.parent.subtitles_list[i][0] + self.parent.subtitles_list[i][1]
                if not start_position > (end - self.parent.minimum_subtitle_width):
                    if not (bool(self.parent.timeline_snap_move_nereast or self.tug_of_war_pressed) and round(last[0] + last[1] + .001, 3) == round(self.parent.selected_subtitle[0], 3)) and self.parent.timeline_snap and self.parent.timeline_snap_limits and (last[0] + last[1] + self.parent.timeline_snap_value) > start_position:
                        subtitles.move_start_subtitle(subtitles=self.parent.subtitles_list, selected_subtitle=self.parent.selected_subtitle, absolute_time=last[0] + last[1] + 0.001, move_nereast=bool(self.parent.timeline_snap_move_nereast or self.tug_of_war_pressed))
                    elif self.parent.timeline_snap and self.parent.timeline_snap_grid:
                        if self.parent.timeline_grid_type == 'frames':
                            difference = start_position % (1.0/self.parent.video_metadata['framerate'])
                            subtitles.move_start_subtitle(subtitles=self.parent.subtitles_list, selected_subtitle=self.parent.selected_subtitle, amount=difference, move_nereast=bool(self.parent.timeline_snap_move_nereast or self.tug_of_war_pressed))
                        elif self.parent.timeline_grid_type == 'seconds' and float(start_position) > float(float(int(start_position)+1) - float(self.parent.timeline_snap_value)):
                            subtitles.move_start_subtitle(subtitles=self.parent.subtitles_list, selected_subtitle=self.parent.selected_subtitle, absolute_time=float(int(start_position)+1), move_nereast=bool(self.parent.timeline_snap_move_nereast or self.tug_of_war_pressed))
                        elif self.parent.timeline_grid_type == 'seconds' and float(start_position) < float(float(int(start_position)) + float(self.parent.timeline_snap_value)):
                            subtitles.move_start_subtitle(subtitles=self.parent.subtitles_list, selected_subtitle=self.parent.selected_subtitle, absolute_time=float(int(start_position)), move_nereast=bool(self.parent.timeline_snap_move_nereast or self.tug_of_war_pressed))
                        elif self.parent.timeline_grid_type == 'scenes' and start_position > next_scene - self.parent.timeline_snap_value:
                            subtitles.move_start_subtitle(subtitles=self.parent.subtitles_list, selected_subtitle=self.parent.selected_subtitle, absolute_time=next_scene, move_nereast=bool(self.parent.timeline_snap_move_nereast or self.tug_of_war_pressed))
                        elif self.parent.timeline_grid_type == 'scenes' and start_position < last_scene + self.parent.timeline_snap_value:
                            subtitles.move_start_subtitle(subtitles=self.parent.subtitles_list, selected_subtitle=self.parent.selected_subtitle, absolute_time=last_scene, move_nereast=bool(self.parent.timeline_snap_move_nereast or self.tug_of_war_pressed))
                        else:
                            subtitles.move_start_subtitle(subtitles=self.parent.subtitles_list, selected_subtitle=self.parent.selected_subtitle, absolute_time=start_position, move_nereast=bool(self.parent.timeline_snap_move_nereast or self.tug_of_war_pressed))
                    else:
                        subtitles.move_start_subtitle(subtitles=self.parent.subtitles_list, selected_subtitle=self.parent.selected_subtitle, absolute_time=start_position, move_nereast=bool(self.parent.timeline_snap_move_nereast or self.tug_of_war_pressed))
                if self.tug_of_war_pressed:
                    self.show_tug_of_war = self.parent.selected_subtitle[0]
            elif self.subtitle_end_is_clicked:
                end_position = (event.pos().x() + self.offset) / self.width_proportion
                if not end_position < (self.parent.subtitles_list[i][0] + self.parent.minimum_subtitle_width):
                    if not (bool(self.parent.timeline_snap_move_nereast or self.tug_of_war_pressed) and round(end_position, 3) >= round(nextsub[0] - 0.001, 3)) and self.parent.timeline_snap and self.parent.timeline_snap_limits and (nextsub[0] - self.parent.timeline_snap_value) < end_position:
                        # self.parent.subtitles_list[i][1] = (nextsub[0] - 0.001) - self.parent.subtitles_list[i][0]
                        subtitles.move_end_subtitle(subtitles=self.parent.subtitles_list, selected_subtitle=self.parent.selected_subtitle, absolute_time=(nextsub[0] - 0.001), move_nereast=bool(self.parent.timeline_snap_move_nereast or self.tug_of_war_pressed))
                    elif self.parent.timeline_snap and self.parent.timeline_snap_grid:
                        if self.parent.timeline_grid_type == 'frames':
                            difference = end_position % (1.0/self.parent.video_metadata['framerate'])
                            subtitles.move_end_subtitle(subtitles=self.parent.subtitles_list, selected_subtitle=self.parent.selected_subtitle, amount=difference, move_nereast=bool(self.parent.timeline_snap_move_nereast or self.tug_of_war_pressed))
                        elif self.parent.timeline_grid_type == 'seconds' and float(end_position) > float(float(int(end_position)+1) - float(self.parent.timeline_snap_value)):
                            subtitles.move_end_subtitle(subtitles=self.parent.subtitles_list, selected_subtitle=self.parent.selected_subtitle, absolute_time=float(int(end_position)+1), move_nereast=bool(self.parent.timeline_snap_move_nereast or self.tug_of_war_pressed))
                        elif self.parent.timeline_grid_type == 'seconds' and float(end_position) < float(float(int(end_position)) + float(self.parent.timeline_snap_value)):
                            subtitles.move_end_subtitle(subtitles=self.parent.subtitles_list, selected_subtitle=self.parent.selected_subtitle, absolute_time=float(int(end_position)), move_nereast=bool(self.parent.timeline_snap_move_nereast or self.tug_of_war_pressed))
                        elif self.parent.timeline_grid_type == 'scenes' and end_position > next_scene - self.parent.timeline_snap_value:
                            subtitles.move_end_subtitle(subtitles=self.parent.subtitles_list, selected_subtitle=self.parent.selected_subtitle, absolute_time=next_scene, move_nereast=bool(self.parent.timeline_snap_move_nereast or self.tug_of_war_pressed))
                        elif self.parent.timeline_grid_type == 'scenes' and end_position < last_scene + self.parent.timeline_snap_value:
                            subtitles.move_end_subtitle(subtitles=self.parent.subtitles_list, selected_subtitle=self.parent.selected_subtitle, absolute_time=last_scene, move_nereast=bool(self.parent.timeline_snap_move_nereast or self.tug_of_war_pressed))
                        else:
                            subtitles.move_end_subtitle(subtitles=self.parent.subtitles_list, selected_subtitle=self.parent.selected_subtitle, absolute_time=end_position, move_nereast=bool(self.parent.timeline_snap_move_nereast or self.tug_of_war_pressed))
                    else:
                        subtitles.move_end_subtitle(subtitles=self.parent.subtitles_list, selected_subtitle=self.parent.selected_subtitle, absolute_time=end_position, move_nereast=bool(self.parent.timeline_snap_move_nereast or self.tug_of_war_pressed))
                if self.tug_of_war_pressed:
                    self.show_tug_of_war = self.parent.selected_subtitle[0] + self.parent.selected_subtitle[1]
            elif self.subtitle_is_clicked:
                if self.parent.timeline_snap and self.parent.timeline_snap_moving and ((nextsub[0] - self.parent.timeline_snap_value) < (start_position + self.parent.subtitles_list[i][1]) or (last[0] + last[1] + self.parent.timeline_snap_value) > start_position):
                    if (nextsub[0] - self.parent.timeline_snap_value) < (start_position + self.parent.subtitles_list[i][1]):
                        self.parent.subtitles_list[i][0] = nextsub[0] - self.parent.subtitles_list[i][1] - 0.001
                    else:
                        self.parent.subtitles_list[i][0] = last[0] + last[1] + 0.001
                elif self.parent.timeline_snap and self.parent.timeline_snap_grid:
                    if self.parent.timeline_grid_type == 'frames':
                        difference = start_position % (1.0/self.parent.video_metadata['framerate'])
                        self.parent.subtitles_list[i][0] = start_position - difference
                    elif self.parent.timeline_grid_type == 'seconds' and float(start_position) > float(float(int(start_position)+1) - float(self.parent.timeline_snap_value)):
                        self.parent.subtitles_list[i][0] = float(int(start_position)+1)
                    elif self.parent.timeline_grid_type == 'seconds' and float(start_position) < float(float(int(start_position)) + float(self.parent.timeline_snap_value)):
                        self.parent.subtitles_list[i][0] = float(int(start_position))
                    elif self.parent.timeline_grid_type == 'scenes' and start_position > next_scene - self.parent.timeline_snap_value:
                        self.parent.subtitles_list[i][0] = next_scene
                    elif self.parent.timeline_grid_type == 'scenes' and start_position < last_scene + self.parent.timeline_snap_value:
                        self.parent.subtitles_list[i][0] = last_scene
                    else:
                        self.parent.subtitles_list[i][0] = start_position
                else:
                    self.parent.subtitles_list[i][0] = start_position


        if self.is_cursor_pressing and not (self.subtitle_start_is_clicked or self.subtitle_end_is_clicked or self.subtitle_is_clicked):
            self.parent.player_widget.seek((event.pos().x() / self.width())*self.parent.video_metadata['duration'])
            # if self.parent.repeat_activated:
            #     self.parent.repeat_duration_tmp = []
            update_timecode_label(self.parent)
        self.update()

    def mouseDoubleClickEvent(self, event):
        """Function to call when mouse double clicks"""
        self.update()
        event.accept()

    def resizeEvent(self, event):
        """Function to call when timeline is resized"""
        self.width_proportion = self.width()/self.parent.video_metadata.get('duration', 0.01)
        self.subtitle_height = self.height()-65
        event.accept()


def get_timeline_time_str(seconds):
    """Function to return timecode from seconds"""
    secs = int(seconds % 60)
    mins = int((seconds / 60) % 60)
    hrs = int((seconds / 60) / 60)

    if hrs:
        return "{hh:02d}:{mm:02d}:{ss:02d}".format(hh=hrs, mm=mins, ss=secs)
    elif mins:
        return "{mm:02d}:{ss:02d}".format(mm=mins, ss=secs)
    else:
        return "{ss:02d}".format(ss=secs)


def load(self):
    """Function to load timeline widgets"""
    self.timeline_widget = Timeline(parent=self)
    self.timeline_widget.setObjectName('timeline_widget')
    self.timeline_widget.setMouseTracking(True)

    class TimelineScroll(QScrollArea):
        """Class for timeline scroll area"""
        def enterEvent(self, event):
            """Function to call when mouse cursor enters the area"""
            event.accept()

        def leaveEvent(self, event):
            """Function to call when mouse cursor leaves the area"""
            event.accept()

        def wheelEvent(self, event):
            """Function to call when mouse wheel is activated"""
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() + event.angleDelta().y())
            event.accept()

        # def keyPressEvent(self, event):
        #     """Function to call when keyboard press on timeline"""
        #     self.keyPressEvent(event)

    self.timeline_scroll = TimelineScroll(parent=self.playercontrols_widget)
    self.timeline_scroll.setObjectName('timeline_scroll')
    self.timeline_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    self.timeline_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
    self.timeline_scroll.setWidget(self.timeline_widget)

    def thread_get_waveform_ended(command):
        self.video_metadata['waveform'][command[0]] = {'points': command[1], 'qimages': []}
        self.videoinfo_label.setText(self.tr('Waveform updated'))
        self.timeline_widget.update()
        self.thread_get_qimages.values_list = command[1]
        self.thread_get_qimages.zoom = command[0]
        self.thread_get_qimages.width = self.timeline_scroll.width()
        self.thread_get_qimages.border_color = self.settings['timeline'].get('waveform_border_color', '#ff153450')
        self.thread_get_qimages.fill_color = self.settings['timeline'].get('waveform_fill_color', '#cc153450')
        self.thread_get_qimages.start(QThread.IdlePriority)

    self.thread_get_waveform = ThreadGetWaveform(self)
    self.thread_get_waveform.command.connect(thread_get_waveform_ended)

    def thread_get_qimages_ended(command):
        self.video_metadata['waveform'][command[0]]['qimages'] = command[1]
        self.videoinfo_label.setText(self.tr('Waveform optimized'))
        self.timeline_widget.update()

    self.thread_get_qimages = ThreadGetQImages(self)
    self.thread_get_qimages.command.connect(thread_get_qimages_ended)


def resized(self):
    """Function to call when timeline is resized"""
    self.timeline_scroll.setGeometry(0, self.playercontrols_widget_central_bottom_background.y(), self.playercontrols_widget.width(), self.playercontrols_widget.height()-self.playercontrols_widget_central_bottom_background.y())
    update_timeline(self)


def update_timeline(self):
    """Function to update timeline"""
    self.timeline_widget.setGeometry(0, -40, self.video_metadata.get('duration', 0.01)*self.mediaplayer_zoom, self.timeline_scroll.height()-15)


def update_scrollbar(self, position=0):
    """Function to update scrollbar of timeline"""
    if position == 'middle':
        offset = self.timeline_scroll.width()*.5
    elif isinstance(position, float):
        offset = self.timeline_scroll.width()*position
    elif isinstance(position, int):
        offset = position
    # self.timeline_scroll.horizontalScrollBar().setValue(self.player_widget.mpv.time_pos * (self.timeline_widget.width()/self.video_metadata.get('duration', 0.01)) - offset)
    self.timeline_scroll.horizontalScrollBar().setValue(self.player_widget.position * (self.timeline_widget.width()/self.video_metadata.get('duration', 0.01)) - offset)


def update_timecode_label(self):
    """Function to update timecode label"""
    self.playercontrols_timecode_label.setText(str(timecode.Timecode('1000', start_seconds=self.player_widget.position, fractional=True)))


def update(self):
    """Function to update timeline"""
    self.player.update_subtitle_layer(self)
    if self.repeat_activated:
        # self.player_widget.position = self.repeat_duration_tmp[0][0]
        if not self.repeat_duration_tmp:
            self.repeat_duration_tmp = [[self.player_widget.position, self.player_widget.position + self.repeat_duration] for i in range(self.repeat_times)]
        else:
            if self.player_widget.position > self.repeat_duration_tmp[0][1]:
                self.player_widget.position = self.repeat_duration_tmp[0][0]
                # self.player_widget.mpv.wait_for_property('seekable')
                self.player_widget.seek(self.player_widget.position)
                # self.player_widget.mpv.seek(self.player_widget.position, reference='absolute')
                pos = self.repeat_duration_tmp.pop(0)
                self.repeat_duration_tmp.append([pos[1], pos[1] + self.repeat_duration])
    if self.settings['timeline'].get('scrolling', 'page') == 'follow':
        if (self.player_widget.position * (self.timeline_widget.width()/self.video_metadata.get('duration', 0.01))) > self.timeline_scroll.width()*.5 and (self.player_widget.position * (self.timeline_widget.width()/self.video_metadata.get('duration', 0.01))) < (self.timeline_widget.width() - (self.timeline_scroll.width()*.5)):
            update_scrollbar(self, position='middle')
    elif self.settings['timeline'].get('scrolling', 'page') == 'page' and (self.player_widget.position * (self.timeline_widget.width()/self.video_metadata.get('duration', 0.01))) > self.timeline_scroll.width() + self.timeline_scroll.horizontalScrollBar().value():
        update_scrollbar(self)

    current_sub, index = subtitles.subtitle_under_current_position(subtitles=self.subtitles_list, position=self.player_widget.position)
    if current_sub and not (self.subtitles_list_qlistwidget.verticalScrollBar().value() + self.subtitles_list_qlistwidget.verticalScrollBar().pageStep() > index > self.subtitles_list_qlistwidget.verticalScrollBar().value()):
        self.subtitles_list_qlistwidget.verticalScrollBar().setValue(index - 1)

    update_timecode_label(self)
    self.timeline_widget.update()


def zoom_update_waveform(self):
    """Function to update timeline zoom"""
    if not isinstance(self.video_metadata['audio'], bool) and self.mediaplayer_zoom not in self.video_metadata['waveform'].keys():
        self.videoinfo_label.setText(self.tr('Generating waveform...'))
        self.thread_get_waveform.audio = self.video_metadata['audio']
        self.thread_get_waveform.zoom = self.mediaplayer_zoom
        self.thread_get_waveform.duration = self.video_metadata.get('duration', 0.01)
        self.thread_get_waveform.start(QThread.IdlePriority)
