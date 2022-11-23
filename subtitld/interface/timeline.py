"""Timeline module

"""

import time
from bisect import bisect

from PySide6.QtGui import QPainter, QPen, QColor, QPolygonF, QFont, QPixmap, QPainterPath, QLinearGradient, QFontMetrics
from PySide6.QtWidgets import QWidget, QScrollArea
from PySide6.QtCore import Qt, QRectF, QPointF, QThread, Signal, QMarginsF

from subtitld import timecode

from subtitld.modules import waveform
from subtitld.modules import history
from subtitld.modules import subtitles
from subtitld.modules import quality_check
from subtitld.modules import utils
from subtitld.interface import subtitles_panel


class ThreadGetWaveform(QThread):
    """Class of qtread to get waveform data"""
    command = Signal(list)
    zoom = False
    audio = False
    duration = False
    width = False
    height = False
    filepath = ''

    def run(self):
        # positive_values, negative_values, _ = waveform.generate_waveform_zoom(zoom=self.zoom, duration=self.duration, waveform=self.audio)
        positive_values, negative_values, _ = waveform.generate_waveform_zoom2(zoom=self.zoom, duration=self.duration, filepath=self.filepath)
        self.command.emit([self.zoom, [positive_values, negative_values]])


class ThreadGetQImages(QThread):
    """Class to generate QThread for QImages"""
    command = Signal(list)
    endcommand = Signal(str)
    values_list = []
    zoom = 100.0
    width = 32767
    border_color = '#ff153450'
    fill_color = '#cc153450'

    def run(self):
        """Function to run QThread"""

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
                    polygon.append(QPointF(x_position, (self.height() * .5) + (point * (self.waveformsize * 100))))
                    x_position += 1
                for point in reversed(self.waveform_down):
                    polygon.append(QPointF(x_position, (self.height() * .5) + (point * (self.waveformsize * 100))))
                    x_position -= 1
                painter.drawPolygon(polygon)

                painter.end()

        parser = 0
        while True:
            qpixmap = DrawPixmap(self.width, 124)
            qpixmap.fill(QColor(0, 0, 0, 0))
            qpixmap.waveform_up = self.values_list[0][parser:parser + self.width]
            qpixmap.waveform_down = self.values_list[1][parser:parser + self.width]
            qpixmap.border_color = self.border_color
            qpixmap.fill_color = self.fill_color
            qpixmap.paintEvent()
            self.command.emit([self.zoom, qpixmap.toImage()])                # qpixmap.save('/tmp/teste.png')
            time.sleep(.2)

            parser += self.width
            if parser > len(self.values_list[0]):
                break
        self.endcommand.emit('qthread finished')


class Timeline(QWidget):
    """Class for timeline QWidget"""
    seek = Signal(float)

    def __init__(widget, self):
        super().__init__()
        widget.subtitle_is_clicked = False
        widget.subtitle_start_is_clicked = False
        widget.subtitle_end_is_clicked = False
        widget.subtitle_height = 50
        widget.subtitle_y = 55
        widget.offset = 0.0
        widget.y_waveform = 22
        widget.h_waveform = 124
        widget.show_limiters = False
        widget.show_tug_of_war = False
        widget.tug_of_war_pressed = False
        widget.is_cursor_pressing = False
        widget.waveformsize = .7
        widget.main_self = self
        widget.width_proportion = widget.width() / widget.main_self.video_metadata.get('duration', 0.01)

    def paintEvent(widget, event):
        """Function for paintEvent of Timeline"""
        painter = QPainter(widget)
        scroll_position = widget.main_self.timeline_scroll.horizontalScrollBar().value()
        scroll_width = widget.main_self.timeline_scroll.width()

        painter.setRenderHint(QPainter.Antialiasing)

        # painter.setOpacity(widget.main_self.mediaplayer_opacity)

        if widget.main_self.repeat_duration_tmp:
            rep_rect = QRectF(
                widget.main_self.repeat_duration_tmp[0][0] * widget.width_proportion,
                0,
                (widget.main_self.repeat_duration_tmp[0][1] - widget.main_self.repeat_duration_tmp[0][0]) * widget.width_proportion,
                widget.height()
            )

            grad = QLinearGradient(0, 0, 0, 100)
            c1 = QColor(widget.main_self.settings['timeline'].get('cursor_color', '#ccff0000'))
            c1.setAlpha(80)
            grad.setColorAt(0, c1)
            c2 = QColor(widget.main_self.settings['timeline'].get('cursor_color', '#ccff0000'))
            c2.setAlpha(0)
            grad.setColorAt(1, c2)

            painter.fillRect(rep_rect, grad)

        if widget.main_self.settings['timeline'].get('view_mode', 'verticalform') and widget.main_self.video_metadata.get('waveform', {}):
            if widget.main_self.settings['timeline'].get('view_mode', 'verticalform') in ['waveform', 'verticalform']:
                if widget.main_self.video_metadata.get('waveform', {}):
                    x_factor = 1
                    available_zoom = widget.main_self.mediaplayer_zoom
                    if available_zoom not in widget.main_self.video_metadata['waveform'].keys():
                        available_zoom = sorted(widget.main_self.video_metadata['waveform'].keys())[0]
                        x_factor = widget.main_self.mediaplayer_zoom / available_zoom

                    w_factor = (widget.main_self.video_metadata.get('duration', 0.01) * available_zoom) / len(widget.main_self.video_metadata['waveform'][available_zoom]['points'][0])

                    if widget.main_self.video_metadata['waveform'][available_zoom].get('qimages', []):
                        xpos = 0
                        for qimage in widget.main_self.video_metadata['waveform'][available_zoom]['qimages']:
                            wid = qimage.width() * w_factor * x_factor
                            if not xpos > scroll_position + scroll_width and not xpos + wid < scroll_position:
                                painter.drawImage(QRectF(xpos, widget.y_waveform, wid, widget.h_waveform), qimage)
                            xpos += wid

                    elif widget.main_self.video_metadata['waveform'][available_zoom].get('points', []):
                        painter.setPen(QPen(QColor(widget.main_self.settings['timeline'].get('waveform_border_color', '#ff153450')), 1, Qt.SolidLine))
                        painter.setBrush(QColor(widget.main_self.settings['timeline'].get('waveform_fill_color', '#cc153450')))

                        x_position = 0
                        polygon = QPolygonF()

                        for point in widget.main_self.video_metadata['waveform'][available_zoom]['points'][0][int(scroll_position / (x_factor * w_factor)):int((scroll_position + scroll_width) / (x_factor * w_factor))]:
                            polygon.append(QPointF((x_position + scroll_position), widget.y_waveform + (widget.h_waveform * .5) + (point * (widget.waveformsize * 100))))
                            x_position += (x_factor * w_factor)

                        for point in reversed(widget.main_self.video_metadata['waveform'][available_zoom]['points'][1][int(scroll_position / (x_factor * w_factor)):int((scroll_position + scroll_width) / (x_factor * w_factor))]):
                            polygon.append(QPointF((x_position + scroll_position), widget.y_waveform + (widget.h_waveform * .5) + (point * (widget.waveformsize * 100))))
                            x_position -= (x_factor * w_factor)

                        painter.drawPolygon(polygon)

        if widget.main_self.subtitles_list:
            painter.setOpacity(1)
            # painter.setPen(QPen(QColor.fromRgb(240, 240, 240, 200), 1, Qt.SolidLine))

            for subtitle in sorted(widget.main_self.subtitles_list):
                if (subtitle[0] / widget.main_self.video_metadata.get('duration', 0.01)) > ((scroll_position + scroll_width) / widget.width()):
                    break
                elif (subtitle[0] + subtitle[1]) / widget.main_self.video_metadata.get('duration', 0.01) < (scroll_position / widget.width()):
                    continue
                else:
                    if widget.main_self.selected_subtitle == subtitle:
                        painter.setPen(QColor(widget.main_self.settings['timeline'].get('selected_subtitle_border_color', '#ff304251')))
                        painter.setBrush(QColor(widget.main_self.settings['timeline'].get('selected_subtitle_fill_color', '#cc3e5363')))
                    else:
                        painter.setPen(QColor(widget.main_self.settings['timeline'].get('subtitle_border_color', '#ff6a7483')))
                        painter.setBrush(QColor(widget.main_self.settings['timeline'].get('subtitle_fill_color', '#ccb8cee0')))

                    subtitle_rect = QRectF(
                        subtitle[0] * widget.width_proportion,
                        widget.subtitle_y,
                        subtitle[1] * widget.width_proportion,
                        widget.subtitle_height
                    )

                    painter.drawRoundedRect(subtitle_rect, 2.0, 2.0, Qt.AbsoluteSize)

                    approved, _, _ = quality_check.check_subtitle(subtitle, widget.main_self.settings['quality_check'])
                    if widget.main_self.settings['quality_check'].get('enabled', False) and not approved:
                        painter.setPen(QColor('#9e1a1a'))
                    elif widget.main_self.selected_subtitle == subtitle:
                        painter.setPen(QColor(widget.main_self.settings['timeline'].get('selected_subtitle_text_color', '#ffffffff')))
                    else:
                        painter.setPen(QColor(widget.main_self.settings['timeline'].get('subtitle_text_color', '#ff304251')))

                    subtitle_rect -= QMarginsF(22, 2, 22, 2)
                    painter.drawText(subtitle_rect, Qt.AlignCenter | Qt.TextWordWrap, subtitle[2])

                    if widget.show_limiters and (subtitle[1] * widget.width_proportion) > 40:
                        if widget.main_self.selected_subtitle == subtitle:
                            painter.setBrush(QColor(widget.main_self.settings['timeline'].get('selected_subtitle_fill_color', '#cc3e5363')))
                        else:
                            painter.setBrush(QColor(widget.main_self.settings['timeline'].get('subtitle_fill_color', '#ccb8cee0')))

                        painter.setPen(Qt.NoPen)
                        lim_rect = QRectF(
                            (subtitle[0] * widget.width_proportion) + 2,
                            widget.subtitle_y + 2,
                            18,
                            widget.subtitle_height - 4
                        )

                        painter.drawRoundedRect(lim_rect, 1.0, 1.0, Qt.AbsoluteSize)

                        lx = 1
                        for _ in range(2):
                            if widget.main_self.selected_subtitle == subtitle:
                                lpen = QPen(QColor('#07000000') if lx % 2 else QColor(widget.main_self.settings['timeline'].get('selected_subtitle_arrow_color', '#ff969696')), 2)
                            else:
                                lpen = QPen(QColor('#07000000') if lx % 2 else QColor(widget.main_self.settings['timeline'].get('subtitle_arrow_color', '#ff969696')), 2)

                            painter.setPen(lpen)
                            painter.setBrush(Qt.NoBrush)
                            path = QPainterPath()
                            path.moveTo(lim_rect.center().x() + 2 + lx, lim_rect.center().y() - 10)
                            path.lineTo(lim_rect.center().x() - 1 + lx, lim_rect.center().y())
                            path.lineTo(lim_rect.center().x() + 2 + lx, lim_rect.center().y() + 10)
                            painter.drawPath(path)
                            lx -= 1

                        if widget.main_self.selected_subtitle == subtitle:
                            painter.setBrush(QColor(widget.main_self.settings['timeline'].get('selected_subtitle_fill_color', '#cc3e5363')))
                        else:
                            painter.setBrush(QColor(widget.main_self.settings['timeline'].get('subtitle_fill_color', '#ccb8cee0')))

                        painter.setPen(Qt.NoPen)
                        lim_rect = QRectF(
                            (subtitle[0] * widget.width_proportion) + (subtitle[1] * widget.width_proportion) - 20,
                            widget.subtitle_y + 2,
                            18,
                            widget.subtitle_height - 4
                        )

                        painter.drawRoundedRect(lim_rect, 1.0, 1.0, Qt.AbsoluteSize)

                        lx = 1
                        for _ in range(2):
                            if widget.main_self.selected_subtitle == subtitle:
                                lpen = QPen(QColor('#07000000') if lx % 2 else QColor(widget.main_self.settings['timeline'].get('selected_subtitle_arrow_color', '#ff969696')), 2)
                            else:
                                lpen = QPen(QColor('#07000000') if lx % 2 else QColor(widget.main_self.settings['timeline'].get('subtitle_arrow_color', '#ff969696')), 2)

                            painter.setPen(lpen)
                            painter.setBrush(Qt.NoBrush)
                            path = QPainterPath()
                            path.moveTo(lim_rect.center().x() + lx, lim_rect.center().y() - 10)
                            path.lineTo(lim_rect.center().x() + 3 + lx, lim_rect.center().y())
                            path.lineTo(lim_rect.center().x() + lx, lim_rect.center().y() + 10)
                            painter.drawPath(path)
                            lx -= 1

            painter.setOpacity(1)

        grid_pen = QPen(QColor(widget.main_self.settings['timeline'].get('grid_color', '#336a7483')), 1, Qt.SolidLine)
        painter.setFont(QFont('Ubuntu Mono', 8))
        xpos = 0
        for sec in range(int(widget.main_self.video_metadata['duration'])):
            if xpos >= scroll_position and xpos <= (scroll_position + widget.main_self.timeline_scroll.width()):
                if (widget.main_self.mediaplayer_zoom > 75) or (widget.main_self.mediaplayer_zoom > 50 and widget.main_self.mediaplayer_zoom <= 75 and not int((sec % 2))) or (widget.main_self.mediaplayer_zoom > 25 and widget.main_self.mediaplayer_zoom <= 50 and not int((sec % 4))) or (widget.main_self.mediaplayer_zoom <= 25 and not int((sec % 8))):
                    lim_rect = QRectF(
                        xpos + 3,
                        27,
                        50,
                        20
                    )
                    painter.setPen(QColor(widget.main_self.settings['timeline'].get('time_text_color', '#806a7483')))
                    painter.drawText(lim_rect, Qt.AlignLeft, utils.get_timeline_time_str(sec))
                if widget.main_self.settings['timeline'].get('show_grid', False) and widget.main_self.settings['timeline'].get('grid_type', False) == 'seconds':
                    painter.setPen(grid_pen)
                    painter.drawLine(xpos, 0, xpos, widget.height())
            xpos += widget.width_proportion
        if widget.main_self.settings['timeline'].get('show_grid', False) and widget.main_self.settings['timeline'].get('grid_type', False) == 'frames':
            painter.setPen(grid_pen)
            xpos = 0.0
            for _ in range(int(widget.main_self.video_metadata['duration'] * widget.main_self.video_metadata['framerate'])):
                if xpos >= scroll_position and xpos <= (scroll_position + widget.main_self.timeline_scroll.width()):
                    painter.drawLine(xpos, 0, xpos, widget.height())
                xpos += widget.width_proportion / widget.main_self.video_metadata['framerate']
        elif widget.main_self.settings['timeline'].get('show_grid', False) and widget.main_self.settings['timeline'].get('grid_type', False) == 'scenes' and widget.main_self.video_metadata['scenes']:
            painter.setPen(grid_pen)
            for scene in widget.main_self.video_metadata['scenes']:
                xpos = (scene * widget.width_proportion)
                if xpos >= scroll_position and xpos <= (scroll_position + widget.main_self.timeline_scroll.width()):
                    painter.drawLine(xpos, 0, xpos, widget.height())

        if bool(widget.show_tug_of_war):
            tug_of_war_pen = QPen(QColor(widget.main_self.settings['timeline'].get('selected_subtitle_arrow_color', '#ff969696')), 4, Qt.SolidLine, Qt.RoundCap)
            painter.setPen(tug_of_war_pen)
            xpos = int(widget.show_tug_of_war * widget.width_proportion) - 4
            y_tug_pos = 0
            for _ in range(6):
                # print(xpos)
                # print(widget.subtitle_y)
                # print(y_tug_pos)
                # print(int(widget.subtitle_y + 8 + y_tug_pos, xpos + 8))
                # print(int(widget.subtitle_y + 8 + y_tug_pos))
                painter.drawLine(xpos, int(widget.subtitle_y + 8 + y_tug_pos), int(xpos + 8), int(widget.subtitle_y + 8 + y_tug_pos))
                # painter.drawLine(xpos, widget.subtitle_y + 8 + y_tug_pos, xpos + 8, widget.subtitle_y + widget.subtitle_height - 8)
                y_tug_pos += (widget.subtitle_height - 8) / 6

        if widget.main_self.player_widget.position is not None:
            painter.setPen(QPen(QColor(widget.main_self.settings['timeline'].get('cursor_color', '#ccff0000')), 2, Qt.SolidLine))
            cursor_pos = int(widget.main_self.player_widget.position * widget.width_proportion)
            painter.drawLine(cursor_pos, 0, cursor_pos, widget.height())

            if (widget.main_self.repeat_duration_tmp and widget.main_self.player_widget.position > widget.main_self.repeat_duration_tmp[0][0]) or (widget.main_self.change_playback_speed.isChecked()):
                cfont = QFont('Ubuntu Mono', 10)
                cfont.setBold(True)

                text = ''
                if widget.main_self.repeat_activated:
                    text += '⤺{}'.format(len(widget.main_self.repeat_duration_tmp))

                if widget.main_self.change_playback_speed.isChecked() and not widget.main_self.playback_speed == 1.0:
                    text += (' ' if text else '') + 'x{}'.format(widget.main_self.playback_speed)

                cfont_metr = QFontMetrics(cfont).horizontalAdvance(text)

                c_ind_color = QColor(widget.main_self.settings['timeline'].get('cursor_color', '#ccff0000'))
                c_ind_color.setAlpha(150)
                painter.setBrush(c_ind_color)
                painter.setPen(Qt.NoPen)

                path = QPainterPath()
                path.moveTo(cursor_pos, 25)
                path.lineTo(cursor_pos - cfont_metr - 12, 25)
                path.lineTo(cursor_pos - cfont_metr - 7, 47)
                path.lineTo(cursor_pos, 47)
                path.lineTo(cursor_pos, 25)
                painter.drawPath(path)

                painter.setFont(cfont)
                painter.setPen(QPen(QColor(widget.main_self.settings['timeline'].get('cursor_text_indicator', '#ffffffff'))))
                text_rect = path.boundingRect() + QMarginsF(5, 0, 5, 0)
                painter.drawText(text_rect, Qt.AlignCenter | Qt.TextWordWrap, text)

        painter.end()
        event.accept()

    def mousePressEvent(widget, event):
        """Function to call when mouse is pressed"""
        scroll_position = widget.main_self.timeline_scroll.horizontalScrollBar().value()
        scroll_width = widget.main_self.timeline_scroll.width()

        cursor_is_out_of_view = bool(widget.main_self.player_widget.position * widget.width_proportion < widget.main_self.timeline_scroll.horizontalScrollBar().value() or widget.main_self.player_widget.position * widget.width_proportion > widget.main_self.timeline_scroll.width() + widget.main_self.timeline_scroll.horizontalScrollBar().value())

        widget.is_cursor_pressing = True
        widget.main_self.selected_subtitle = False

        for subtitle in sorted(widget.main_self.subtitles_list):
            if (subtitle[0] / widget.main_self.video_metadata.get('duration', 0.01)) > ((scroll_position + scroll_width) / widget.width()):
                break
            elif (subtitle[0] + subtitle[1]) / widget.main_self.video_metadata.get('duration', 0.01) < (scroll_position / widget.width()):
                continue
            else:
                if event.pos().y() > widget.subtitle_y and event.pos().y() < (widget.subtitle_height + widget.subtitle_y) and (((event.pos().x()) / widget.width_proportion) > subtitle[0] and ((event.pos().x()) / widget.width_proportion) < (subtitle[0] + subtitle[1])):
                    widget.main_self.selected_subtitle = subtitle
                    if event.pos().x() / widget.width_proportion > (subtitle[0] + subtitle[1]) - (20 / widget.width_proportion):
                        widget.subtitle_end_is_clicked = True
                        widget.offset = ((widget.main_self.selected_subtitle[0] + widget.main_self.selected_subtitle[1]) * widget.width_proportion) - event.pos().x()
                        widget.tug_of_war_pressed = widget.show_tug_of_war
                    else:
                        widget.offset = event.pos().x() - widget.main_self.selected_subtitle[0] * widget.width_proportion
                        if event.pos().x() / widget.width_proportion < subtitle[0] + (20 / widget.width_proportion):
                            widget.subtitle_start_is_clicked = True
                            widget.tug_of_war_pressed = widget.show_tug_of_war
                        else:
                            widget.subtitle_is_clicked = True
                    break

        if not (widget.subtitle_end_is_clicked or widget.subtitle_start_is_clicked or widget.subtitle_is_clicked) or cursor_is_out_of_view:
            # widget.main_self.player_widget.position = (event.pos().x() / widget.width()) * widget.main_self.video_metadata['duration']
            widget.main_self.player_widget.seek((event.pos().x() / widget.width()) * widget.main_self.video_metadata['duration'])
            if widget.main_self.repeat_activated:
                widget.main_self.repeat_duration_tmp = []
            widget.seek.emit(widget.main_self.player_widget.position)
            # update_timecode_label(widget.parent)

        if (widget.subtitle_is_clicked or widget.subtitle_start_is_clicked or widget.subtitle_end_is_clicked):
            history.history_append(widget.main_self.subtitles_list)
            widget.main_self.unsaved = True

        widget.update()

    def mouseReleaseEvent(widget, event):
        """Function to call when mouse press is released"""
        widget.subtitle_is_clicked = False
        widget.subtitle_start_is_clicked = False
        widget.subtitle_end_is_clicked = False
        widget.is_cursor_pressing = False
        widget.tug_of_war_pressed = False
        widget.update()
        subtitles_panel.update_subtitles_panel_widget_vision_content(widget.main_self)
        event.accept()

    def mouseMoveEvent(widget, event):
        """Function to call when mouse moves"""
        # scroll_position = widget.main_self.timeline_scroll.horizontalScrollBar().value()
        # scroll_width = widget.main_self.timeline_scroll.width()

        widget.show_limiters = bool(event.pos().y() > widget.subtitle_y and event.pos().y() < (widget.subtitle_height + widget.subtitle_y))

        for subtitle in sorted(widget.main_self.subtitles_list):
            last = widget.main_self.subtitles_list[widget.main_self.subtitles_list.index(subtitle) - 1] if widget.main_self.subtitles_list.index(subtitle) > 0 else [0, 0, '']
            nextsub = widget.main_self.subtitles_list[widget.main_self.subtitles_list.index(subtitle) + 1] if widget.main_self.subtitles_list.index(subtitle) < len(widget.main_self.subtitles_list) - 1 else [widget.main_self.video_metadata['duration'], 0, '']

            if subtitle[0] + subtitle[1] > event.pos().x() / widget.width_proportion > (subtitle[0] + subtitle[1]) - (4 / widget.width_proportion) and nextsub[0] < (subtitle[0] + subtitle[1] + .02):
                widget.show_tug_of_war = subtitle[0] + subtitle[1] + .0005
                break
            elif subtitle[0] < event.pos().x() / widget.width_proportion < subtitle[0] + (4 / widget.width_proportion) and last[0] + last[1] > subtitle[0] - .02:
                widget.show_tug_of_war = subtitle[0] - .0005
                break
            elif not widget.tug_of_war_pressed:
                widget.show_tug_of_war = False

        if widget.main_self.selected_subtitle:
            i = widget.main_self.subtitles_list.index(widget.main_self.selected_subtitle)
            last = widget.main_self.subtitles_list[widget.main_self.subtitles_list.index(widget.main_self.selected_subtitle) - 1] if widget.main_self.subtitles_list.index(widget.main_self.selected_subtitle) > 0 else [0, 0, '']
            nextsub = widget.main_self.subtitles_list[widget.main_self.subtitles_list.index(widget.main_self.selected_subtitle) + 1] if widget.main_self.subtitles_list.index(widget.main_self.selected_subtitle) < len(widget.main_self.subtitles_list) - 1 else [widget.main_self.video_metadata['duration'], 0, '']
            scenes_list = widget.main_self.video_metadata['scenes'] if len(widget.main_self.video_metadata['scenes']) > 1 else [0.0]
            scenes_list.append(widget.main_self.video_metadata['duration'])
            start_position = (event.pos().x() - widget.offset) / widget.width_proportion
            last_scene = scenes_list[bisect(scenes_list, start_position) - 1]
            next_scene = scenes_list[bisect(scenes_list, start_position)]

            if widget.subtitle_start_is_clicked:
                end = widget.main_self.subtitles_list[i][0] + widget.main_self.subtitles_list[i][1]
                if not start_position > (end - widget.main_self.settings['default_values'].get('minimum_subtitle_width', 1)):
                    if not (bool(widget.main_self.settings['timeline'].get('snap_move_nereast', False) or widget.tug_of_war_pressed) and round(last[0] + last[1] + .001, 3) == round(widget.main_self.selected_subtitle[0], 3)) and widget.main_self.settings['timeline'].get('snap', True) and widget.main_self.settings['timeline'].get('snap_limits', True) and (last[0] + last[1] + widget.main_self.settings['timeline'].get('snap_value', .1)) > start_position:
                        subtitles.move_start_subtitle(subtitles=widget.main_self.subtitles_list, selected_subtitle=widget.main_self.selected_subtitle, absolute_time=last[0] + last[1] + 0.001, move_nereast=bool(widget.main_self.settings['timeline'].get('snap_move_nereast', False) or widget.tug_of_war_pressed))
                    elif widget.main_self.settings['timeline'].get('snap', True) and widget.main_self.settings['timeline'].get('snap_grid', False):
                        if widget.main_self.settings['timeline'].get('grid_type', False) == 'frames':
                            difference = start_position % (1.0 / widget.main_self.video_metadata['framerate'])
                            subtitles.move_start_subtitle(subtitles=widget.main_self.subtitles_list, selected_subtitle=widget.main_self.selected_subtitle, amount=difference, move_nereast=bool(widget.main_self.settings['timeline'].get('snap_move_nereast', False) or widget.tug_of_war_pressed))
                        elif widget.main_self.settings['timeline'].get('grid_type', False) == 'seconds' and float(start_position) > float(float(int(start_position) + 1) - float(widget.main_self.settings['timeline'].get('snap_value', .1))):
                            subtitles.move_start_subtitle(subtitles=widget.main_self.subtitles_list, selected_subtitle=widget.main_self.selected_subtitle, absolute_time=float(int(start_position) + 1), move_nereast=bool(widget.main_self.settings['timeline'].get('snap_move_nereast', False) or widget.tug_of_war_pressed))
                        elif widget.main_self.settings['timeline'].get('grid_type', False) == 'seconds' and float(start_position) < float(float(int(start_position)) + float(widget.main_self.settings['timeline'].get('snap_value', .1))):
                            subtitles.move_start_subtitle(subtitles=widget.main_self.subtitles_list, selected_subtitle=widget.main_self.selected_subtitle, absolute_time=float(int(start_position)), move_nereast=bool(widget.main_self.settings['timeline'].get('snap_move_nereast', False) or widget.tug_of_war_pressed))
                        elif widget.main_self.settings['timeline'].get('grid_type', False) == 'scenes' and start_position > next_scene - widget.main_self.settings['timeline'].get('snap_value', .1):
                            subtitles.move_start_subtitle(subtitles=widget.main_self.subtitles_list, selected_subtitle=widget.main_self.selected_subtitle, absolute_time=next_scene, move_nereast=bool(widget.main_self.settings['timeline'].get('snap_move_nereast', False) or widget.tug_of_war_pressed))
                        elif widget.main_self.settings['timeline'].get('grid_type', False) == 'scenes' and start_position < last_scene + widget.main_self.settings['timeline'].get('snap_value', .1):
                            subtitles.move_start_subtitle(subtitles=widget.main_self.subtitles_list, selected_subtitle=widget.main_self.selected_subtitle, absolute_time=last_scene, move_nereast=bool(widget.main_self.settings['timeline'].get('snap_move_nereast', False) or widget.tug_of_war_pressed))
                        else:
                            subtitles.move_start_subtitle(subtitles=widget.main_self.subtitles_list, selected_subtitle=widget.main_self.selected_subtitle, absolute_time=start_position, move_nereast=bool(widget.main_self.settings['timeline'].get('snap_move_nereast', False) or widget.tug_of_war_pressed))
                    else:
                        subtitles.move_start_subtitle(subtitles=widget.main_self.subtitles_list, selected_subtitle=widget.main_self.selected_subtitle, absolute_time=start_position, move_nereast=bool(widget.main_self.settings['timeline'].get('snap_move_nereast', False) or widget.tug_of_war_pressed))
                if widget.tug_of_war_pressed:
                    widget.show_tug_of_war = widget.main_self.selected_subtitle[0]
            elif widget.subtitle_end_is_clicked:
                end_position = (event.pos().x() + widget.offset) / widget.width_proportion
                if not end_position < (widget.main_self.subtitles_list[i][0] + widget.main_self.settings['default_values'].get('minimum_subtitle_width', 1)):
                    if not (bool(widget.main_self.settings['timeline'].get('snap_move_nereast', False) or widget.tug_of_war_pressed) and round(end_position, 3) >= round(nextsub[0] - 0.001, 3)) and widget.main_self.settings['timeline'].get('snap', True) and widget.main_self.settings['timeline'].get('snap_limits', True) and (nextsub[0] - widget.main_self.settings['timeline'].get('snap_value', .1)) < end_position:
                        # widget.main_self.subtitles_list[i][1] = (nextsub[0] - 0.001) - widget.main_self.subtitles_list[i][0]
                        subtitles.move_end_subtitle(subtitles=widget.main_self.subtitles_list, selected_subtitle=widget.main_self.selected_subtitle, absolute_time=(nextsub[0] - 0.001), move_nereast=bool(widget.main_self.settings['timeline'].get('snap_move_nereast', False) or widget.tug_of_war_pressed))
                    elif widget.main_self.settings['timeline'].get('snap', True) and widget.main_self.settings['timeline'].get('snap_grid', False):
                        if widget.main_self.settings['timeline'].get('grid_type', False) == 'frames':
                            difference = end_position % (1.0 / widget.main_self.video_metadata['framerate'])
                            subtitles.move_end_subtitle(subtitles=widget.main_self.subtitles_list, selected_subtitle=widget.main_self.selected_subtitle, amount=difference, move_nereast=bool(widget.main_self.settings['timeline'].get('snap_move_nereast', False) or widget.tug_of_war_pressed))
                        elif widget.main_self.settings['timeline'].get('grid_type', False) == 'seconds' and float(end_position) > float(float(int(end_position) + 1) - float(widget.main_self.settings['timeline'].get('snap_value', .1))):
                            subtitles.move_end_subtitle(subtitles=widget.main_self.subtitles_list, selected_subtitle=widget.main_self.selected_subtitle, absolute_time=float(int(end_position) + 1), move_nereast=bool(widget.main_self.settings['timeline'].get('snap_move_nereast', False) or widget.tug_of_war_pressed))
                        elif widget.main_self.settings['timeline'].get('grid_type', False) == 'seconds' and float(end_position) < float(float(int(end_position)) + float(widget.main_self.settings['timeline'].get('snap_value', .1))):
                            subtitles.move_end_subtitle(subtitles=widget.main_self.subtitles_list, selected_subtitle=widget.main_self.selected_subtitle, absolute_time=float(int(end_position)), move_nereast=bool(widget.main_self.settings['timeline'].get('snap_move_nereast', False) or widget.tug_of_war_pressed))
                        elif widget.main_self.settings['timeline'].get('grid_type', False) == 'scenes' and end_position > next_scene - widget.main_self.settings['timeline'].get('snap_value', .1):
                            subtitles.move_end_subtitle(subtitles=widget.main_self.subtitles_list, selected_subtitle=widget.main_self.selected_subtitle, absolute_time=next_scene, move_nereast=bool(widget.main_self.settings['timeline'].get('snap_move_nereast', False) or widget.tug_of_war_pressed))
                        elif widget.main_self.settings['timeline'].get('grid_type', False) == 'scenes' and end_position < last_scene + widget.main_self.settings['timeline'].get('snap_value', .1):
                            subtitles.move_end_subtitle(subtitles=widget.main_self.subtitles_list, selected_subtitle=widget.main_self.selected_subtitle, absolute_time=last_scene, move_nereast=bool(widget.main_self.settings['timeline'].get('snap_move_nereast', False) or widget.tug_of_war_pressed))
                        else:
                            subtitles.move_end_subtitle(subtitles=widget.main_self.subtitles_list, selected_subtitle=widget.main_self.selected_subtitle, absolute_time=end_position, move_nereast=bool(widget.main_self.settings['timeline'].get('snap_move_nereast', False) or widget.tug_of_war_pressed))
                    else:
                        subtitles.move_end_subtitle(subtitles=widget.main_self.subtitles_list, selected_subtitle=widget.main_self.selected_subtitle, absolute_time=end_position, move_nereast=bool(widget.main_self.settings['timeline'].get('snap_move_nereast', False) or widget.tug_of_war_pressed))
                if widget.tug_of_war_pressed:
                    widget.show_tug_of_war = widget.main_self.selected_subtitle[0] + widget.main_self.selected_subtitle[1]
            elif widget.subtitle_is_clicked:
                if widget.main_self.settings['timeline'].get('snap', True) and widget.main_self.settings.get('timeline', {}).get('snap_moving', True) and ((nextsub[0] - widget.main_self.settings['timeline'].get('snap_value', .1)) < (start_position + widget.main_self.subtitles_list[i][1]) or (last[0] + last[1] + widget.main_self.settings['timeline'].get('snap_value', .1)) > start_position):
                    if (nextsub[0] - widget.main_self.settings['timeline'].get('snap_value', .1)) < (start_position + widget.main_self.subtitles_list[i][1]):
                        widget.main_self.subtitles_list[i][0] = nextsub[0] - widget.main_self.subtitles_list[i][1] - 0.001
                    else:
                        widget.main_self.subtitles_list[i][0] = last[0] + last[1] + 0.001
                elif widget.main_self.settings['timeline'].get('snap', True) and widget.main_self.settings['timeline'].get('snap_grid', False):
                    if widget.main_self.settings['timeline'].get('grid_type', False) == 'frames':
                        difference = start_position % (1.0 / widget.main_self.video_metadata['framerate'])
                        widget.main_self.subtitles_list[i][0] = start_position - difference
                    elif widget.main_self.settings['timeline'].get('grid_type', False) == 'seconds' and float(start_position) > float(float(int(start_position) + 1) - float(widget.main_self.settings['timeline'].get('snap_value', .1))):
                        widget.main_self.subtitles_list[i][0] = float(int(start_position) + 1)
                    elif widget.main_self.settings['timeline'].get('grid_type', False) == 'seconds' and float(start_position) < float(float(int(start_position)) + float(widget.main_self.settings['timeline'].get('snap_value', .1))):
                        widget.main_self.subtitles_list[i][0] = float(int(start_position))
                    elif widget.main_self.settings['timeline'].get('grid_type', False) == 'scenes' and start_position > next_scene - widget.main_self.settings['timeline'].get('snap_value', .1):
                        widget.main_self.subtitles_list[i][0] = next_scene
                    elif widget.main_self.settings['timeline'].get('grid_type', False) == 'scenes' and start_position < last_scene + widget.main_self.settings['timeline'].get('snap_value', .1):
                        widget.main_self.subtitles_list[i][0] = last_scene
                    else:
                        widget.main_self.subtitles_list[i][0] = start_position
                else:
                    widget.main_self.subtitles_list[i][0] = start_position

        if widget.is_cursor_pressing and not (widget.subtitle_start_is_clicked or widget.subtitle_end_is_clicked or widget.subtitle_is_clicked):
            # widget.seek.emit((event.pos().x() / widget.width()) * widget.main_self.video_metadata['duration'])
            widget.main_self.player_widget.seek((event.pos().x() / widget.width()) * widget.main_self.video_metadata['duration'])
            # if widget.main_self.repeat_activated:
            #     widget.main_self.repeat_duration_tmp = []
            widget.seek.emit(widget.main_self.player_widget.position)
            # update_timecode_label(widget.parent)
        widget.update()

    def mouseDoubleClickEvent(widget, event):
        """Function to call when mouse double clicks"""
        widget.update()
        event.accept()

    def resizeEvent(widget, event):
        """Function to call when timeline is resized"""
        widget.width_proportion = widget.width() / widget.main_self.video_metadata.get('duration', 0.01)
        widget.subtitle_height = widget.height() - 65
        event.accept()


def load(self):
    """Function to load timeline widgets"""
    self.timeline_widget = Timeline(self)
    self.timeline_widget.setObjectName('timeline_widget')
    self.timeline_widget.setMouseTracking(True)
    # self.timeline_widget.seek.connect(lambda position: update_timecode_label(self, position))

    class TimelineScroll(QScrollArea):
        """Class for timeline scroll area"""
        def __init__(self, parent=None):
            super().__init__(parent)
            self.parent = parent

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
        # self.videoinfo_label.setText('Waveform updated')
        self.timeline_widget.update()
        self.thread_get_qimages.values_list = command[1]
        self.thread_get_qimages.zoom = command[0]
        self.thread_get_qimages.width = self.timeline_scroll.width()
        self.thread_get_qimages.border_color = self.settings['timeline'].get('waveform_border_color', '#ff153450')
        self.thread_get_qimages.fill_color = self.settings['timeline'].get('waveform_fill_color', '#cc153450')
        self.thread_get_qimages.start()
        # self.thread_get_qimages.start(QThread.IdlePriority)

    self.thread_get_waveform = ThreadGetWaveform(self)
    self.thread_get_waveform.command.connect(thread_get_waveform_ended)

    def thread_get_qimages_ended(command):
        self.video_metadata['waveform'][command[0]]['qimages'].append(command[1])
        self.timeline_widget.update()

    # def thread_qimages_endcommand(command):
    #     self.videoinfo_label.setText('Waveform optimized')

    self.thread_get_qimages = ThreadGetQImages(self)
    self.thread_get_qimages.command.connect(thread_get_qimages_ended)
    # self.thread_get_qimages.endcommand.connect(thread_qimages_endcommand)


def resized(self):
    """Function to call when timeline is resized"""
    self.timeline_scroll.setGeometry(0, self.playercontrols_widget_frame.y() + self.playercontrols_widget_frame.height() - 26, self.playercontrols_widget.width(), self.playercontrols_widget.height() - self.playercontrols_widget_frame.y() - self.playercontrols_widget_frame.height() + 26)
    update_timeline(self)


def update_timeline(self):
    """Function to update timeline"""
    self.timeline_widget.setGeometry(0, -40, int(self.video_metadata.get('duration', 0.01) * self.mediaplayer_zoom), self.timeline_scroll.height() - 15)


def update_scrollbar(self, position=0):
    """Function to update scrollbar of timeline"""
    current_position_in_timeline_widget = (self.player_widget.position / self.video_metadata.get('duration', 0.01)) * self.timeline_widget.width()
    offset = 0

    if position == 'middle':
        if (self.timeline_widget.width() - (self.timeline_scroll.width() * .5)) > current_position_in_timeline_widget > self.timeline_scroll.width() * .5:
            offset = self.timeline_scroll.width() * .5
    elif isinstance(position, float):
        offset = self.timeline_scroll.width() * position
    elif isinstance(position, int):
        offset = position

    self.timeline_scroll.horizontalScrollBar().setValue(int(current_position_in_timeline_widget - offset))


def update_timecode_label(self, position):
    """Function to update timecode label"""
    self.playercontrols_timecode_label.setText(str(timecode.Timecode('1000', start_seconds=position, fractional=True)))


def update(self):
    """Function to update timeline"""
    self.player.update_subtitle_layer(self)
    if self.repeat_activated:
        if not self.repeat_duration_tmp:
            self.repeat_duration_tmp = [[self.player_widget.position, self.player_widget.position + self.repeat_duration] for i in range(self.repeat_times)]
        else:
            last_pos = self.repeat_duration_tmp[0][1]
            if self.player_widget.position > last_pos:
                self.player_widget.position = self.repeat_duration_tmp[0][0]
                self.player_widget.seek(self.player_widget.position)
                del self.repeat_duration_tmp[0]
                if not len(self.repeat_duration_tmp):
                    for i in range(self.repeat_times):
                        self.repeat_duration_tmp.append([last_pos, last_pos + self.repeat_duration])
    if not self.player_widget.mpv.pause:
        current_position_in_timeline_widget = (self.player_widget.position * (self.timeline_widget.width() / self.video_metadata.get('duration', 0.01)))
        if self.settings['timeline'].get('scrolling', 'page') == 'follow':
            update_scrollbar(self, position='middle')
        elif self.settings['timeline'].get('scrolling', 'page') == 'page' and current_position_in_timeline_widget > self.timeline_scroll.width() + self.timeline_scroll.horizontalScrollBar().value():
            update_scrollbar(self)
    self.timeline_widget.update()
    update_timecode_label(self, self.player_widget.position)


def zoom_update_waveform(self):
    """Function to update timeline zoom"""
    if not isinstance(self.video_metadata['audio'], bool) and self.mediaplayer_zoom not in self.video_metadata['waveform'].keys():
        # self.videoinfo_label.setText('Generating waveform...')
        # self.thread_get_waveform.audio = self.video_metadata['audio']
        self.thread_get_waveform.filepath = self.video_metadata['filepath']
        self.thread_get_waveform.zoom = self.mediaplayer_zoom
        self.thread_get_waveform.duration = self.video_metadata.get('duration', 0.01)
        self.thread_get_waveform.start(QThread.IdlePriority)
