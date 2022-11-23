from bisect import bisect
# from multiprocessing.spawn import old_main_modules
from PySide6.QtWidgets import QWidget, QPushButton, QScrollArea, QLineEdit, QTextEdit
from PySide6.QtGui import QColor, QPen, QPainter, QPolygonF, QTransform, QPainterPath, QFont, QFontMetrics
from PySide6.QtCore import QMarginsF, QRectF, Qt, QPointF, Signal

from subtitld.modules import quality_check
from subtitld.modules import history
from subtitld.modules import subtitles
from subtitld.modules import utils
from subtitld.interface import subtitles_panel


class subtitles_panel_timeline_widget_timeline(QWidget):
    """Class for timeline QWidget"""
    seek = Signal(float)

    def __init__(widget, self):
        super().__init__()
        widget.w_waveform = 125
        widget.x_waveform = widget.width() - widget.w_waveform
        widget.subtitle_width = widget.width()
        widget.subtitle_x = 0
        widget.height_proportion = 1
        widget.show_limiters = False
        widget.subtitle_is_clicked = False
        widget.subtitle_start_is_clicked = False
        widget.subtitle_end_is_clicked = False
        widget.show_tug_of_war = False
        widget.tug_of_war_pressed = False
        widget.is_cursor_pressing = False
        widget.waveformsize = .7
        widget.offset = 0.0
        widget.mediaplayer_zoom = 100.0
        widget.main_self = self

        widget.show_editing_widgets = False

        widget.starting_time_qlineedit = QLineEdit(widget)
        widget.starting_time_qlineedit.editingFinished.connect(lambda: widget.qlineedit_editing_finished())
        widget.starting_time_qlineedit.setProperty('class', 'subtitles_panel_timeline_widget_qlineedit')

        widget.text_qtextedit = QTextEdit(widget)
        widget.text_qtextedit.setProperty('class', 'subtitles_panel_timeline_widget_qlineedit')
        widget.text_qtextedit.textChanged.connect(lambda: widget.qlineedit_editing_finished())
        widget.text_qtextedit.setAlignment(Qt.AlignCenter)

        widget.ending_time_qlineedit = QLineEdit(widget)
        widget.ending_time_qlineedit.editingFinished.connect(lambda: widget.qlineedit_editing_finished())
        widget.ending_time_qlineedit.setProperty('class', 'subtitles_panel_timeline_widget_qlineedit')

        widget.update_editing_widgets()

    def paintEvent(widget, event):
        """Function for paintEvent of Timeline"""
        painter = QPainter(widget)
        scroll_position = widget.main_self.subtitles_panel_timeline_widget.verticalScrollBar().value()
        scroll_height = widget.main_self.subtitles_panel_timeline_widget.height()

        painter.setRenderHint(QPainter.Antialiasing)

        waveform_background_qrectF = QRectF(
            widget.width() - widget.w_waveform,
            0,
            widget.w_waveform,
            widget.height()
        )

        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(widget.main_self.settings['timeline'].get('waveform_background_color', '#55153450')))

        painter.drawRect(waveform_background_qrectF)

        transform_rotate_90 = QTransform()
        transform_rotate_90.rotate(90)

        if widget.main_self.settings['timeline'].get('view_mode', 'verticalform') and widget.main_self.video_metadata.get('waveform', {}):
            if widget.main_self.settings['timeline'].get('view_mode', 'verticalform') in ['waveform', 'verticalform']:
                if widget.main_self.video_metadata.get('waveform', {}):
                    zoom_factor = 1
                    available_zoom = widget.mediaplayer_zoom
                    if available_zoom not in widget.main_self.video_metadata['waveform'].keys():
                        available_zoom = sorted(widget.main_self.video_metadata['waveform'].keys())[0]
                        zoom_factor = widget.mediaplayer_zoom / available_zoom

                    h_factor = (widget.main_self.video_metadata.get('duration', 0.01) * available_zoom) / len(widget.main_self.video_metadata['waveform'][available_zoom]['points'][0])

                    if widget.main_self.video_metadata['waveform'][available_zoom].get('qimages', []):
                        ypos = 0
                        for qimage in widget.main_self.video_metadata['waveform'][available_zoom]['qimages']:
                            wid = qimage.width() * h_factor * zoom_factor
                            if not ypos > scroll_position + scroll_height and not ypos + wid < scroll_position:
                                painter.drawImage(QRectF(widget.x_waveform, ypos, widget.w_waveform, wid), qimage.transformed(transform_rotate_90))
                            ypos += wid

                    elif widget.main_self.video_metadata['waveform'][available_zoom].get('points', []):
                        painter.setPen(QPen(QColor(widget.main_self.settings['timeline'].get('waveform_border_color', '#ff153450')), 1, Qt.SolidLine))
                        painter.setBrush(QColor(widget.main_self.settings['timeline'].get('waveform_fill_color', '#cc153450')))

                        x_position = 0
                        polygon = QPolygonF()

                        for point in widget.main_self.video_metadata['waveform'][available_zoom]['points'][0][int(scroll_position / (zoom_factor * h_factor)):int((scroll_position + scroll_height) / (zoom_factor * h_factor))]:
                            polygon.append(QPointF((x_position + scroll_position), widget.x_waveform + (widget.w_waveform * .5) + (point * (widget.waveformsize * 100))))
                            x_position += (zoom_factor * h_factor)

                        for point in reversed(widget.main_self.video_metadata['waveform'][available_zoom]['points'][1][int(scroll_position / (zoom_factor * h_factor)):int((scroll_position + scroll_height) / (zoom_factor * h_factor))]):
                            polygon.append(QPointF((x_position + scroll_position), widget.x_waveform + (widget.w_waveform * .5) + (point * (widget.waveformsize * 100))))
                            x_position -= (zoom_factor * h_factor)

                        painter.drawPolygon(polygon)

        if widget.main_self.subtitles_list:
            painter.setOpacity(1)

            for subtitle in sorted(widget.main_self.subtitles_list):
                if (subtitle[0] / widget.main_self.video_metadata.get('duration', 0.01)) > ((scroll_position + scroll_height) / widget.height()):
                    break
                elif (subtitle[0] + subtitle[1]) / widget.main_self.video_metadata.get('duration', 0.01) < (scroll_position / widget.height()):
                    continue
                else:
                    painter.setPen(Qt.NoPen)
                    if widget.main_self.selected_subtitle == subtitle:
                        # painter.setPen(QColor(widget.main_self.settings['timeline'].get('selected_subtitle_border_color', '#ff304251')))
                        painter.setBrush(QColor(widget.main_self.settings['timeline'].get('selected_subtitle_fill_color', '#cc3e5363')))
                    else:
                        # painter.setPen(QColor(widget.main_self.settings['timeline'].get('subtitle_border_color', '#ff6a7483')))
                        painter.setBrush(QColor(widget.main_self.settings['timeline'].get('subtitle_fill_color', '#ccb8cee0')))

                    subtitle_rect = QRectF(
                        widget.subtitle_x,
                        subtitle[0] * widget.height_proportion,
                        widget.subtitle_width,
                        subtitle[1] * widget.height_proportion,
                    )

                    painter.drawRect(subtitle_rect)

                    if not widget.main_self.selected_subtitle == subtitle or (widget.main_self.selected_subtitle == subtitle and not widget.show_editing_widgets):
                        start_time = utils.get_timeline_time_str(subtitle[0], ms=True)
                        start_time_width = QFontMetrics(QFont('Ubuntu', 8)).horizontalAdvance(start_time)
                        start_time_rect = QRectF(
                            subtitle_rect.left() + 20,
                            subtitle_rect.top(),
                            start_time_width + 20,
                            20
                        )

                        path = QPainterPath()
                        path.moveTo(start_time_rect.right() + 5, subtitle_rect.top())
                        path.lineTo(0, subtitle_rect.top())
                        path.lineTo(0, subtitle_rect.top() + 20)
                        path.lineTo(start_time_rect.right(), subtitle_rect.top() + 20)
                        path.lineTo(start_time_rect.right() + 5, subtitle_rect.top())
                        painter.drawPath(path)

                        painter.setFont(QFont('Ubuntu Mono', 8))
                        painter.setPen(QColor(widget.main_self.settings['timeline'].get('time_text_color', '#806a7483')))
                        painter.drawText(start_time_rect, Qt.AlignLeft | Qt.AlignVCenter, start_time)

                        approved, _, _ = quality_check.check_subtitle(subtitle, widget.main_self.settings['quality_check'])
                        if widget.main_self.settings['quality_check'].get('enabled', False) and not approved:
                            painter.setPen(QColor('#9e1a1a'))
                        elif widget.main_self.selected_subtitle == subtitle:
                            painter.setPen(QColor(widget.main_self.settings['timeline'].get('selected_subtitle_text_color', '#ffffffff')))
                        else:
                            painter.setPen(QColor(widget.main_self.settings['timeline'].get('subtitle_text_color', '#ff304251')))

                        text_rect = subtitle_rect - QMarginsF(22, 2, widget.w_waveform + 2, 2)
                        painter.setFont(QFont('Ubuntu', 10))
                        painter.drawText(text_rect, Qt.AlignVCenter | Qt.AlignLeft | Qt.TextWordWrap, subtitle[2])

                        if widget.show_limiters and (subtitle[1] * widget.height_proportion) > 40:
                            painter.setPen(Qt.NoPen)

                            path = QPainterPath()
                            path.moveTo(start_time_rect.right() + 5, subtitle_rect.top())
                            path.lineTo((widget.width() - widget.w_waveform) + 5, subtitle_rect.top())
                            path.lineTo((widget.width() - widget.w_waveform), subtitle_rect.top() + 20)
                            path.lineTo(start_time_rect.right(), subtitle_rect.top() + 20)
                            path.lineTo(start_time_rect.right() + 5, subtitle_rect.top())
                            painter.drawPath(path)

                            ly = 1
                            for _ in range(2):
                                if widget.main_self.selected_subtitle == subtitle:
                                    lpen = QPen(QColor('#07000000') if ly % 2 else QColor(widget.main_self.settings['timeline'].get('selected_subtitle_arrow_color', '#ff969696')), 2)
                                else:
                                    lpen = QPen(QColor('#07000000') if ly % 2 else QColor(widget.main_self.settings['timeline'].get('subtitle_arrow_color', '#ff969696')), 2)

                                painter.setPen(lpen)
                                painter.setBrush(Qt.NoBrush)
                                path = QPainterPath()
                                path.moveTo(start_time_rect.right() + ((widget.width() - widget.w_waveform - start_time_rect.right()) * .5) - 10, (subtitle_rect.top() + 10) + ly + 1)
                                path.lineTo(start_time_rect.right() + ((widget.width() - widget.w_waveform - start_time_rect.right()) * .5), (subtitle_rect.top() + 10) - (3) + ly + 1)
                                path.lineTo(start_time_rect.right() + ((widget.width() - widget.w_waveform - start_time_rect.right()) * .5) + 10, (subtitle_rect.top() + 10) + ly + 1)
                                painter.drawPath(path)
                                ly -= 1

                        painter.setPen(Qt.NoPen)

                        if widget.main_self.selected_subtitle == subtitle:
                            painter.setBrush(QColor(widget.main_self.settings['timeline'].get('selected_subtitle_fill_color', '#cc3e5363')))
                        else:
                            painter.setBrush(QColor(widget.main_self.settings['timeline'].get('subtitle_fill_color', '#ccb8cee0')))

                        end_time = utils.get_timeline_time_str(subtitle[0] + subtitle[1], ms=True)
                        end_time_width = QFontMetrics(QFont('Ubuntu', 8)).horizontalAdvance(end_time)
                        end_time_rect = QRectF(
                            subtitle_rect.left() + 20,
                            subtitle_rect.bottom() - 20,
                            end_time_width + 20,
                            20
                        )

                        path = QPainterPath()
                        path.moveTo(end_time_rect.right(), subtitle_rect.bottom() - 20)
                        path.lineTo(0, subtitle_rect.bottom() - 20)
                        path.lineTo(0, subtitle_rect.bottom())
                        path.lineTo(end_time_rect.right() + 5, subtitle_rect.bottom())
                        path.lineTo(end_time_rect.right(), subtitle_rect.bottom() - 20)
                        painter.drawPath(path)

                        painter.setFont(QFont('Ubuntu Mono', 8))
                        painter.setPen(QColor(widget.main_self.settings['timeline'].get('time_text_color', '#806a7483')))
                        painter.drawText(end_time_rect, Qt.AlignLeft | Qt.AlignVCenter, end_time)

                        approved, _, _ = quality_check.check_subtitle(subtitle, widget.main_self.settings['quality_check'])
                        if widget.main_self.settings['quality_check'].get('enabled', False) and not approved:
                            painter.setPen(QColor('#9e1a1a'))
                        elif widget.main_self.selected_subtitle == subtitle:
                            painter.setPen(QColor(widget.main_self.settings['timeline'].get('selected_subtitle_text_color', '#ffffffff')))
                        else:
                            painter.setPen(QColor(widget.main_self.settings['timeline'].get('subtitle_text_color', '#ff304251')))

                        text_rect = subtitle_rect - QMarginsF(22, 2, widget.w_waveform + 2, 2)
                        painter.setFont(QFont('Ubuntu', 10))
                        painter.drawText(text_rect, Qt.AlignVCenter | Qt.AlignLeft | Qt.TextWordWrap, subtitle[2])

                        if widget.show_limiters and (subtitle[1] * widget.height_proportion) > 40:
                            painter.setPen(Qt.NoPen)

                            path = QPainterPath()
                            path.moveTo(end_time_rect.right(), subtitle_rect.bottom() - 20)
                            path.lineTo((widget.width() - widget.w_waveform), subtitle_rect.bottom() - 20)
                            path.lineTo((widget.width() - widget.w_waveform) + 5, subtitle_rect.bottom())
                            path.lineTo(end_time_rect.right() + 5, subtitle_rect.bottom())
                            path.lineTo(end_time_rect.right(), subtitle_rect.bottom() - 20)
                            painter.drawPath(path)

                            ly = 0
                            for _ in range(2):
                                if widget.main_self.selected_subtitle == subtitle:
                                    lpen = QPen(QColor('#07000000') if ly % 2 else QColor(widget.main_self.settings['timeline'].get('selected_subtitle_arrow_color', '#ff969696')), 2)
                                else:
                                    lpen = QPen(QColor('#07000000') if ly % 2 else QColor(widget.main_self.settings['timeline'].get('subtitle_arrow_color', '#ff969696')), 2)

                                painter.setPen(lpen)
                                painter.setBrush(Qt.NoBrush)
                                path = QPainterPath()
                                path.moveTo(end_time_rect.right() + ((widget.width() - widget.w_waveform - end_time_rect.right()) * .5) - 10, (subtitle_rect.bottom() - 20 + 10) + ly - 2)
                                path.lineTo(end_time_rect.right() + ((widget.width() - widget.w_waveform - end_time_rect.right()) * .5), (subtitle_rect.bottom() - 20 + 10) + (3) + ly - 2)
                                path.lineTo(end_time_rect.right() + ((widget.width() - widget.w_waveform - end_time_rect.right()) * .5) + 10, (subtitle_rect.bottom() - 20 + 10) + ly - 2)
                                painter.drawPath(path)
                                ly += 1

                    #     if widget.main_self.selected_subtitle == subtitle:
                    #         painter.setPen(QColor(widget.main_self.settings['timeline'].get('selected_subtitle_arrow_color', '#ff969696')))
                    #     else:
                    #         painter.setPen(QColor(widget.main_self.settings['timeline'].get('subtitle_arrow_color', '#ff969696')))

                    #     painter.drawText(lim_rect, Qt.AlignCenter, '︿')

                    #     painter.setPen(Qt.NoPen)
                    #     lim_rect = QRectF(
                    #         widget.subtitle_x + 2,
                    #         (subtitle[0] * widget.height_proportion) + (subtitle[1] * widget.height_proportion) - 20,
                    #         widget.subtitle_width - 4,
                    #         18
                    #     )

                    #     painter.drawRect(lim_rect)

                    #     if widget.main_self.selected_subtitle == subtitle:
                    #         painter.setPen(QColor(widget.main_self.settings['timeline'].get('selected_subtitle_arrow_color', '#ff969696')))
                    #     else:
                    #         painter.setPen(QColor(widget.main_self.settings['timeline'].get('subtitle_arrow_color', '#ff969696')))

                    #     painter.drawText(lim_rect, Qt.AlignCenter, '﹀')

                    if widget.main_self.selected_subtitle == subtitle:
                        painter.setPen(QColor(widget.main_self.settings['timeline'].get('selected_subtitle_border_color', '#ff304251')))
                    else:
                        painter.setPen(QColor(widget.main_self.settings['timeline'].get('subtitle_border_color', '#ff6a7483')))

                    painter.drawLine(
                        int(widget.subtitle_x),
                        int(subtitle_rect.top()),
                        int(widget.width()),
                        int(subtitle_rect.top()),
                    )

                    painter.drawLine(
                        int(widget.subtitle_x),
                        int(subtitle_rect.bottom()),
                        int(widget.width()),
                        int(subtitle_rect.bottom()),
                    )

            painter.setOpacity(1)

        if bool(widget.show_tug_of_war):
            tug_of_war_pen = QPen(QColor(widget.main_self.settings['timeline'].get('selected_subtitle_arrow_color', '#ff969696')), 4, Qt.SolidLine, Qt.RoundCap)
            painter.setPen(tug_of_war_pen)
            ypos = int(widget.show_tug_of_war * widget.height_proportion) - 4
            x_tug_pos = 0
            for _ in range(6):
                painter.drawLine(
                    int(widget.subtitle_x + 8 + x_tug_pos),
                    ypos,
                    int(widget.subtitle_x + 8 + x_tug_pos),
                    ypos + 8
                )
                # painter.drawLine(ypos, widget.subtitle_y + 8 + x_tug_pos, ypos + 8, widget.subtitle_y + widget.subtitle_height - 8)
                x_tug_pos += (widget.subtitle_width - widget.w_waveform - 16) / 5

        if widget.main_self.player_widget.position is not None:
            painter.setPen(QPen(QColor(widget.main_self.settings['timeline'].get('cursor_color', '#ccff0000')), 2, Qt.SolidLine))
            cursor_pos = int(widget.main_self.player_widget.position * widget.height_proportion)
            painter.drawLine(0, cursor_pos, widget.width(), cursor_pos)

        painter.end()
        event.accept()

    def mousePressEvent(widget, event):
        """Function to call when mouse is pressed"""
        scroll_position = widget.main_self.subtitles_panel_timeline_widget.verticalScrollBar().value()
        scroll_height = widget.main_self.subtitles_panel_timeline_widget.height()

        cursor_is_out_of_view = bool(widget.main_self.player_widget.position * widget.height_proportion < widget.main_self.subtitles_panel_timeline_widget.verticalScrollBar().value() or widget.main_self.player_widget.position * widget.height_proportion > widget.main_self.subtitles_panel_timeline_widget.width() + widget.main_self.subtitles_panel_timeline_widget.verticalScrollBar().value())

        widget.is_cursor_pressing = True
        widget.main_self.selected_subtitle = False

        for subtitle in sorted(widget.main_self.subtitles_list):
            if (subtitle[0] / widget.main_self.video_metadata.get('duration', 0.01)) > ((scroll_position + scroll_height) / widget.height()):
                break
            elif (subtitle[0] + subtitle[1]) / widget.main_self.video_metadata.get('duration', 0.01) < (scroll_position / widget.height()):
                continue
            else:
                if (widget.subtitle_x < event.pos().x() < widget.width() - widget.w_waveform) and (((event.pos().y()) / widget.height_proportion) > subtitle[0] and ((event.pos().y()) / widget.height_proportion) < (subtitle[0] + subtitle[1])):
                    widget.main_self.selected_subtitle = subtitle
                    if event.pos().y() / widget.height_proportion > (subtitle[0] + subtitle[1]) - (20 / widget.height_proportion):
                        widget.subtitle_end_is_clicked = True
                        widget.offset = ((widget.main_self.selected_subtitle[0] + widget.main_self.selected_subtitle[1]) * widget.height_proportion) - event.pos().y()
                        widget.tug_of_war_pressed = widget.show_tug_of_war
                    else:
                        widget.offset = event.pos().y() - widget.main_self.selected_subtitle[0] * widget.height_proportion
                        if event.pos().y() / widget.height_proportion < subtitle[0] + (20 / widget.height_proportion):
                            widget.subtitle_start_is_clicked = True
                            widget.tug_of_war_pressed = widget.show_tug_of_war
                        else:
                            widget.subtitle_is_clicked = True
                    break

        if not (widget.subtitle_end_is_clicked or widget.subtitle_start_is_clicked or widget.subtitle_is_clicked) or cursor_is_out_of_view:
            widget.main_self.player_widget.position = (event.pos().y() / widget.height()) * widget.main_self.video_metadata.get('duration', 0.01)
            widget.seek.emit(widget.main_self.player_widget.position)

        if (widget.subtitle_is_clicked or widget.subtitle_start_is_clicked or widget.subtitle_end_is_clicked):
            history.history_append(widget.main_self.subtitles_list)

        widget.update()

    def mouseReleaseEvent(widget, event):
        """Function to call when mouse press is released"""
        widget.subtitle_is_clicked = False
        widget.subtitle_start_is_clicked = False
        widget.subtitle_end_is_clicked = False
        widget.is_cursor_pressing = False
        widget.tug_of_war_pressed = False
        widget.update()
        event.accept()

    def mouseMoveEvent(widget, event):
        widget.show_limiters = bool(event.pos().x() > widget.subtitle_x and event.pos().x() < (widget.subtitle_width - widget.w_waveform))

        for subtitle in sorted(widget.main_self.subtitles_list):
            last = widget.main_self.subtitles_list[widget.main_self.subtitles_list.index(subtitle) - 1] if widget.main_self.subtitles_list.index(subtitle) > 0 else [0, 0, '']
            nextsub = widget.main_self.subtitles_list[widget.main_self.subtitles_list.index(subtitle) + 1] if widget.main_self.subtitles_list.index(subtitle) < len(widget.main_self.subtitles_list) - 1 else [widget.main_self.video_metadata['duration'], 0, '']

            if subtitle[0] + subtitle[1] > event.pos().y() / widget.height_proportion > (subtitle[0] + subtitle[1]) - (4 / widget.height_proportion) and nextsub[0] < (subtitle[0] + subtitle[1] + .02) and widget.show_limiters:
                widget.show_tug_of_war = subtitle[0] + subtitle[1] + .0005
                break
            elif subtitle[0] < event.pos().y() / widget.height_proportion < subtitle[0] + (4 / widget.height_proportion) and last[0] + last[1] > subtitle[0] - .02 and widget.show_limiters:
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
            start_position = (event.pos().y() - widget.offset) / widget.height_proportion
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
                end_position = (event.pos().y() + widget.offset) / widget.height_proportion
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
            widget.seek.emit((event.pos().y() / widget.height()) * widget.main_self.video_metadata.get('duration', 0.01))

        widget.update()

    def mouseDoubleClickEvent(widget, event):
        widget.show_editing_widgets = True
        widget.update_editing_widgets()
        event.accept()

    def resizeEvent(widget, event):
        """Function to call when timeline is resized"""
        # widget.height_proportion = widget.width()/widget.main_self.video_metadata.get('duration', 0.01)
        widget.x_waveform = widget.width() - widget.w_waveform
        widget.subtitle_width = widget.width()
        widget.height_proportion = widget.height() / widget.main_self.video_metadata.get('duration', 0.01)
        event.accept()

    def leaveEvent(widget, event):
        widget.qlineedit_editing_finished()
        widget.show_editing_widgets = False
        widget.update_editing_widgets()
        event.accept()

    def qlineedit_editing_finished(widget):
        if widget.show_editing_widgets and widget.main_self.selected_subtitle and widget.starting_time_qlineedit.text() and widget.ending_time_qlineedit.text():
            widget.main_self.selected_subtitle[0] = float(widget.starting_time_qlineedit.text())
            widget.main_self.selected_subtitle[1] = float(widget.ending_time_qlineedit.text()) - widget.main_self.selected_subtitle[0]
            widget.main_self.selected_subtitle[2] = widget.text_qtextedit.toPlainText()
        widget.update()

    def update_editing_widgets(widget):
        if widget.main_self.selected_subtitle:
            start_time = utils.get_timeline_time_str(widget.main_self.selected_subtitle[0], ms=True)
            start_time_width = QFontMetrics(QFont('Ubuntu', 8)).horizontalAdvance(start_time)

            widget.starting_time_qlineedit.setGeometry(
                int(widget.subtitle_x) + 10,
                int(widget.main_self.selected_subtitle[0] * widget.height_proportion) + 3,
                start_time_width + 20,
                15,
            )
            widget.starting_time_qlineedit.setText(str(widget.main_self.selected_subtitle[0]))
            widget.starting_time_qlineedit.setVisible(True)

            widget.text_qtextedit.setGeometry(
                int(widget.subtitle_x) + 10,
                int((widget.main_self.selected_subtitle[0]) * widget.height_proportion) + 24,
                widget.x_waveform - 20,
                int((widget.main_self.selected_subtitle[1]) * widget.height_proportion) - 46
            )
            widget.text_qtextedit.blockSignals(True)
            widget.text_qtextedit.setText(str(widget.main_self.selected_subtitle[2]))
            widget.text_qtextedit.blockSignals(False)

            widget.text_qtextedit.setVisible(True)

            end_time = utils.get_timeline_time_str(widget.main_self.selected_subtitle[0], ms=True)
            end_time_width = QFontMetrics(QFont('Ubuntu', 8)).horizontalAdvance(end_time)

            widget.ending_time_qlineedit.setGeometry(
                int(widget.subtitle_x) + 10,
                int((widget.main_self.selected_subtitle[0] + widget.main_self.selected_subtitle[1]) * widget.height_proportion) - 17,
                end_time_width + 20,
                15,
            )
            widget.ending_time_qlineedit.setText(str(widget.main_self.selected_subtitle[0] + widget.main_self.selected_subtitle[1]))
            widget.ending_time_qlineedit.setVisible(True)

        widget.starting_time_qlineedit.setVisible(widget.show_editing_widgets)
        widget.text_qtextedit.setVisible(widget.show_editing_widgets)
        widget.ending_time_qlineedit.setVisible(widget.show_editing_widgets)


def add_button(self):
    self.subtitles_panel_widget_button_timeline = QPushButton()
    self.subtitles_panel_widget_button_timeline.setObjectName('subtitles_panel_widget_button_timeline')
    self.subtitles_panel_widget_button_timeline.setProperty('class', 'subtitles_panel_left_button')
    self.subtitles_panel_widget_button_timeline.setCheckable(True)
    self.subtitles_panel_widget_button_timeline.setFixedWidth(23)
    # self.subtitles_panel_widget_button_timeline.icon().addPixmap(self.subtitles_panel_widget_button_timeline.icon(), QIcon.Disable)
    self.subtitles_panel_widget_button_timeline.clicked.connect(lambda vision: subtitles_panel.update_subtitles_panel_widget_vision(self, 'timeline'))
    self.subtitles_panel_widget_buttons_vbox.addWidget(self.subtitles_panel_widget_button_timeline)


def add_widgets(self):
    self.subtitles_panel_timeline_widget = QScrollArea()
    self.subtitles_panel_timeline_widget.setObjectName('subtitles_panel_timeline_widget')
    self.subtitles_panel_timeline_widget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
    self.subtitles_panel_timeline_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    self.subtitles_panel_timeline_widget_timeline = subtitles_panel_timeline_widget_timeline(self)
    self.subtitles_panel_timeline_widget_timeline.setMouseTracking(True)
    self.subtitles_panel_timeline_widget_timeline.seek.connect(lambda position: subtitles_panel_timeline_widget_timeline_seek(self, position))
    # self.subtitles_panel_timeline_widget_timeline.focusout.connect(lambda: subtitles_panel_timeline_widget_timeline_loses_focus(self))
    # self.subtitles_panel_timeline_widget_timeline.doubleclicked.connect(lambda: subtitles_panel_timeline_widget_timeline_doubleclicked(self))
    self.subtitles_panel_timeline_widget.setWidget(self.subtitles_panel_timeline_widget_timeline)

    self.subtitles_panel_stackedwidgets.addWidget(self.subtitles_panel_timeline_widget)


def update_subtitles_panel_timeline(self):
    # print(self.video_metadata.get('duration', 0.01) * self.mediaplayer_zoom)
    self.subtitles_panel_timeline_widget_timeline.update()

    if self.settings['timeline'].get('scrolling', 'page') == 'follow':
        if (self.player_widget.position * (self.subtitles_panel_timeline_widget_timeline.height() / self.video_metadata.get('duration', 0.01))) > self.subtitles_panel_timeline_widget.width() * .5 and (self.player_widget.position * (self.subtitles_panel_timeline_widget_timeline.height() / self.video_metadata.get('duration', 0.01))) < (self.subtitles_panel_timeline_widget_timeline.height() - (self.subtitles_panel_timeline_widget.height() * .5)):
            update_scrollbar(self, position='middle')
    elif self.settings['timeline'].get('scrolling', 'page') == 'page' and (self.player_widget.position * (self.subtitles_panel_timeline_widget_timeline.height() / self.video_metadata.get('duration', 0.01))) > self.subtitles_panel_timeline_widget.height() + self.subtitles_panel_timeline_widget.verticalScrollBar().value():
        update_scrollbar(self)

    # self.subtitles_panel_timeline_widget_timeline.setGeometry(0, 0, self.subtitles_panel_subtitles_panel_timeline_widget_timeline.height(), self.video_metadata.get('duration', 0.01) * self.mediaplayer_zoom)
    # print(self.subtitles_panel_timeline_widget_timeline.height())


def update_scrollbar(self, position=0):
    """Function to update scrollbar of timeline"""
    if position == 'middle':
        offset = self.subtitles_panel_timeline_widget.height() * .5
    elif isinstance(position, float):
        offset = self.subtitles_panel_timeline_widget.height() * position
    elif isinstance(position, int):
        offset = position
    # self.subtitles_panel_timeline_widget.verticalScrollBar().setValue(self.player_widget.mpv.time_pos * (self.timeline_widget.width()/self.video_metadata.get('duration', 0.01)) - offset)
    self.subtitles_panel_timeline_widget.verticalScrollBar().setValue(int(self.player_widget.position * (self.subtitles_panel_timeline_widget_timeline.height() / self.video_metadata.get('duration', 0.01)) - offset))


def timeline_resized(self):
    self.subtitles_panel_timeline_widget_timeline.setGeometry(0, 0, self.subtitles_panel_timeline_widget.width(), int(self.video_metadata.get('duration', 0.01) * self.mediaplayer_zoom))


def subtitles_panel_timeline_widget_timeline_seek(self, position):
    self.player_widget.seek(position)
