"""Module for subtitle list panel

"""
import os

from PyQt5.QtWidgets import QHBoxLayout, QPushButton, QLabel, QSizePolicy, QTextEdit, QVBoxLayout, QWidget, QStyledItemDelegate, QStyle, QListView, QLineEdit, QFrame
from PyQt5.QtGui import QIcon, QFontMetrics, QFont, QColor
from PyQt5.QtCore import Qt, QSize, QAbstractListModel, QRect, QMargins

from subtitld.interface import subtitles_panel
from subtitld.modules import utils
from subtitld.modules import quality_check
from subtitld.modules import subtitles
from subtitld.modules.paths import PATH_SUBTITLD_GRAPHICS


class subtitles_panel_qlistwidget_model(QAbstractListModel):
    def __init__(self, *args, subtitles=None, **kwargs):
        super(subtitles_panel_qlistwidget_model, self).__init__(*args, **kwargs)
        self.subtitles = subtitles or []

    def data(self, index, role):
        if role == Qt.DisplayRole:
            return self.subtitles[index.row()][-1]

        # if role == Qt.DecorationRole:
        #     status, _ = self.subtitles[index.row()]
        #     if status:
        #         return tick

    def get_index(self, subtitle):
        index = self.subtitles.index(subtitle)
        return self.index(index)

    def rowCount(self, index):
        return len(self.subtitles)


class subtitles_panel_qlistwidget_delegate(QStyledItemDelegate):
    def __init__(self, parent=None, settings=None):
        super(subtitles_panel_qlistwidget_delegate, self).__init__(parent)
        self.settings = settings or {}

    def get_number_width(self, index):
        number_width = QFontMetrics(QFont('Ubuntu', 8)).horizontalAdvance((len(str(index.model().rowCount(index)))) * '8')
        return number_width

    def get_text_height(self, option, index):
        row_text = index.data(Qt.DisplayRole)
        width = option.rect.width()
        height = QFontMetrics(QFont('Ubuntu', 11)).boundingRect(QRect(0, 0, width - (20 + 10 + self.get_number_width(index) + 10 + 10), 100), Qt.TextWordWrap, row_text).height()
        return height

    def paint(self, painter, option, index):
        row_text = index.data(Qt.DisplayRole)
        number_width = self.get_number_width(index)

        if option.state & QStyle.State_Selected:
            painter.setPen(Qt.NoPen)
            painter.setBrush(QColor(self.settings.get('subtitle_list', {}).get('background_color', '#102e3e4c')))
            painter.drawRect(option.rect)
            # painter.setBrush(QColor('#55d43f'))
            # painter.drawRect(QRect(0, option.rect.y(), 20, option.rect.height()))

        sub_is_ok = True
        if self.settings['quality_check'].get('enabled', False):
            sub_is_ok, reasons = quality_check.check_subtitle(index.model().subtitles[index.row()], self.settings['quality_check'])

        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(self.settings.get('subtitle_list', {}).get('number_background_color', '#aa2e3e4c') if sub_is_ok else self.settings.get('subtitle_list', {}).get('number_background_warning_color', '#aa9e1a1a')))

        number_rect = QRect(20, option.rect.y(), 10 + number_width + 10, option.rect.height())
        text_rect = QRect(number_rect.right(), option.rect.y(), option.rect.width() - number_rect.right(), option.rect.height())

        painter.drawRect(number_rect)

        painter.setPen(QColor(self.settings.get('subtitle_list', {}).get('number_color', '#ffffff') if sub_is_ok else self.settings.get('subtitle_list', {}).get('number_warning_color', '#ffffff')))

        number_rect = number_rect.marginsRemoved(QMargins(10, 10, 10, 10))

        painter.setFont(QFont('Ubuntu', 8))
        painter.drawText(number_rect, 0, str(index.row() + 1))

        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(self.settings.get('subtitle_list', {}).get('text_background_color', '#102e3e4c') if sub_is_ok else self.settings.get('subtitle_list', {}).get('text_background_warning_color', '#109e1a1a')))

        painter.drawRect(text_rect)

        text_rect = text_rect.marginsRemoved(QMargins(10, 10, 10, 10))

        painter.setPen(QColor(self.settings.get('subtitle_list', {}).get('text_color', '#2e3e4c') if sub_is_ok else self.settings.get('subtitle_list', {}).get('text_warning_color', '#9e1a1a')))
        painter.setFont(QFont('Ubuntu', 11))
        painter.drawText(text_rect, Qt.TextWordWrap, row_text)

    def sizeHint(self, option, index):
        width = option.rect.width()
        height = self.get_text_height(option, index) + 20
        return QSize(width, height)


def add_widgets(self):
    self.subtitles_panel_simplelist_widget = QWidget()
    self.subtitles_panel_simplelist_widget_vbox = QVBoxLayout(self.subtitles_panel_simplelist_widget)
    self.subtitles_panel_simplelist_widget_vbox.setContentsMargins(0, 0, 0, 0)
    self.subtitles_panel_simplelist_widget_vbox.setSpacing(10)

    self.subtitles_panel_qlistwidget_model = subtitles_panel_qlistwidget_model()

    self.subtitles_panel_qlistwidget_delegate = subtitles_panel_qlistwidget_delegate(settings=self.settings)

    self.subtitles_panel_qlistwidget = QListView()
    self.subtitles_panel_qlistwidget.setViewMode(QListView.ListMode)
    self.subtitles_panel_qlistwidget.setObjectName('subtitles_panel_qlistwidget')
    self.subtitles_panel_qlistwidget.setContentsMargins(QMargins(0, 0, 0, 0))
    self.subtitles_panel_qlistwidget.setSpacing(0)
    self.subtitles_panel_qlistwidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    self.subtitles_panel_qlistwidget.setFocusPolicy(Qt.NoFocus)
    self.subtitles_panel_qlistwidget.setModel(self.subtitles_panel_qlistwidget_model)
    self.subtitles_panel_qlistwidget.setItemDelegate(self.subtitles_panel_qlistwidget_delegate)
    # self.subtitles_panel_qlistwidget.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum))
    self.subtitles_panel_qlistwidget.clicked.connect(lambda: subtitles_panel_qlistwidget_item_clicked(self))
    self.subtitles_panel_simplelist_widget_vbox.addWidget(self.subtitles_panel_qlistwidget, 1)

    self.subtitles_panel_simplelist_properties = QFrame()
    self.subtitles_panel_simplelist_properties.setLayout(QVBoxLayout())
    self.subtitles_panel_simplelist_properties.layout().setContentsMargins(20, 0, 0, 0)
    self.subtitles_panel_simplelist_properties.layout().setSpacing(0)

    self.subtitles_panel_simplelist_properties_textedit_line = QHBoxLayout()
    self.subtitles_panel_simplelist_properties_textedit_line.setContentsMargins(0, 0, 0, 0)
    self.subtitles_panel_simplelist_properties_textedit_line.setSpacing(0)

    self.properties_textedit = QTextEdit()
    self.properties_textedit.setObjectName('properties_textedit')
    self.properties_textedit.setFixedHeight(120)
    self.properties_textedit.textChanged.connect(lambda: properties_textedit_changed(self))
    self.subtitles_panel_simplelist_properties_textedit_line.addWidget(self.properties_textedit)

    self.subtitles_panel_simplelist_properties_textedit_timings_column = QVBoxLayout()
    self.subtitles_panel_simplelist_properties_textedit_timings_column.setContentsMargins(0, 0, 0, 0)
    self.subtitles_panel_simplelist_properties_textedit_timings_column.setSpacing(0)

    self.subtitles_panel_simplelist_properties_start_timing_frame = QFrame()
    self.subtitles_panel_simplelist_properties_start_timing_frame.setObjectName('subtitles_panel_simplelist_properties_start_timing_frame')
    self.subtitles_panel_simplelist_properties_start_timing_frame.setProperty('class', 'qframe_timings')
    self.subtitles_panel_simplelist_properties_start_timing_frame.setLayout(QVBoxLayout())
    self.subtitles_panel_simplelist_properties_start_timing_frame.layout().setContentsMargins(2, 2, 2, 2)
    self.subtitles_panel_simplelist_properties_start_timing_frame.layout().setSpacing(0)

    self.subtitles_panel_simplelist_properties_start_timing_label = QLabel('Start')
    self.subtitles_panel_simplelist_properties_start_timing_label.setObjectName('subtitles_panel_simplelist_properties_start_timing_label')
    self.subtitles_panel_simplelist_properties_start_timing_label.setProperty('class', 'properties_timing_labels')
    self.subtitles_panel_simplelist_properties_start_timing_label.setSizePolicy(QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum))
    self.subtitles_panel_simplelist_properties_start_timing_frame.layout().addWidget(self.subtitles_panel_simplelist_properties_start_timing_label)

    self.subtitles_panel_simplelist_properties_start_timing_qlineedit = QLineEdit()
    self.subtitles_panel_simplelist_properties_start_timing_qlineedit.setProperty('class', 'qlineedit_timings')
    self.subtitles_panel_simplelist_properties_start_timing_qlineedit.setObjectName('subtitles_panel_simplelist_properties_start_timing_qlineedit')
    self.subtitles_panel_simplelist_properties_start_timing_qlineedit.setSizePolicy(QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum))
    self.subtitles_panel_simplelist_properties_start_timing_qlineedit.textEdited.connect(lambda: subtitles_panel_simplelist_properties_start_timing_qlineedit_text_edited(self))
    self.subtitles_panel_simplelist_properties_start_timing_frame.layout().addWidget(self.subtitles_panel_simplelist_properties_start_timing_qlineedit)

    self.subtitles_panel_simplelist_properties_textedit_timings_column.addWidget(self.subtitles_panel_simplelist_properties_start_timing_frame)

    self.subtitles_panel_simplelist_properties_textedit_timings_column.addSpacing(-10)
    self.subtitles_panel_simplelist_properties_duration_timing_lock_button = QPushButton()
    self.subtitles_panel_simplelist_properties_duration_timing_lock_button.setObjectName('subtitles_panel_simplelist_properties_duration_timing_lock_button')
    self.subtitles_panel_simplelist_properties_duration_timing_lock_button.setProperty('class', 'subbutton_transparent')
    self.subtitles_panel_simplelist_properties_duration_timing_lock_button.setProperty('borderless_right', 'true')
    self.subtitles_panel_simplelist_properties_duration_timing_lock_button.setCheckable(True)
    self.subtitles_panel_simplelist_properties_duration_timing_lock_button.setFixedSize(QSize(20, 20))
    self.subtitles_panel_simplelist_properties_textedit_timings_column.addWidget(self.subtitles_panel_simplelist_properties_duration_timing_lock_button, 0, Qt.AlignRight)
    self.subtitles_panel_simplelist_properties_textedit_timings_column.addSpacing(-10)

    self.subtitles_panel_simplelist_properties_duration_timing_frame = QFrame()
    self.subtitles_panel_simplelist_properties_duration_timing_frame.setObjectName('subtitles_panel_simplelist_properties_duration_timing_frame')
    self.subtitles_panel_simplelist_properties_duration_timing_frame.setProperty('class', 'qframe_timings')
    self.subtitles_panel_simplelist_properties_duration_timing_frame.setLayout(QVBoxLayout())
    self.subtitles_panel_simplelist_properties_duration_timing_frame.layout().setContentsMargins(2, 2, 2, 2)
    self.subtitles_panel_simplelist_properties_duration_timing_frame.layout().setSpacing(0)

    self.subtitles_panel_simplelist_properties_duration_timing_label = QLabel('Duration')
    self.subtitles_panel_simplelist_properties_duration_timing_label.setObjectName('subtitles_panel_simplelist_properties_duration_timing_label')
    self.subtitles_panel_simplelist_properties_duration_timing_label.setProperty('class', 'properties_timing_labels')
    self.subtitles_panel_simplelist_properties_duration_timing_label.setSizePolicy(QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum))
    self.subtitles_panel_simplelist_properties_duration_timing_frame.layout().addWidget(self.subtitles_panel_simplelist_properties_duration_timing_label)

    self.subtitles_panel_simplelist_properties_duration_timing_qlineedit = QLineEdit()
    self.subtitles_panel_simplelist_properties_duration_timing_qlineedit.setProperty('class', 'qlineedit_timings')
    self.subtitles_panel_simplelist_properties_duration_timing_qlineedit.setObjectName('subtitles_panel_simplelist_properties_duration_timing_qlineedit')
    self.subtitles_panel_simplelist_properties_duration_timing_qlineedit.setSizePolicy(QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum))
    self.subtitles_panel_simplelist_properties_duration_timing_qlineedit.textEdited.connect(lambda: subtitles_panel_simplelist_properties_duration_timing_qlineedit_text_edited(self))
    self.subtitles_panel_simplelist_properties_duration_timing_frame.layout().addWidget(self.subtitles_panel_simplelist_properties_duration_timing_qlineedit)

    self.subtitles_panel_simplelist_properties_textedit_timings_column.addWidget(self.subtitles_panel_simplelist_properties_duration_timing_frame)

    self.subtitles_panel_simplelist_properties_ending_timing_frame = QFrame()
    self.subtitles_panel_simplelist_properties_ending_timing_frame.setObjectName('subtitles_panel_simplelist_properties_ending_timing_frame')
    self.subtitles_panel_simplelist_properties_ending_timing_frame.setProperty('class', 'qframe_timings')
    self.subtitles_panel_simplelist_properties_ending_timing_frame.setLayout(QVBoxLayout())
    self.subtitles_panel_simplelist_properties_ending_timing_frame.layout().setContentsMargins(2, 2, 2, 2)
    self.subtitles_panel_simplelist_properties_ending_timing_frame.layout().setSpacing(0)

    self.subtitles_panel_simplelist_properties_ending_timing_label = QLabel('End')
    self.subtitles_panel_simplelist_properties_ending_timing_label.setObjectName('subtitles_panel_simplelist_properties_ending_timing_label')
    self.subtitles_panel_simplelist_properties_ending_timing_label.setProperty('class', 'properties_timing_labels')
    self.subtitles_panel_simplelist_properties_ending_timing_label.setSizePolicy(QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum))
    self.subtitles_panel_simplelist_properties_ending_timing_frame.layout().addWidget(self.subtitles_panel_simplelist_properties_ending_timing_label)

    self.subtitles_panel_simplelist_properties_ending_timing_qlineedit = QLineEdit()
    self.subtitles_panel_simplelist_properties_ending_timing_qlineedit.setProperty('class', 'qlineedit_timings')
    self.subtitles_panel_simplelist_properties_ending_timing_qlineedit.setObjectName('subtitles_panel_simplelist_properties_ending_timing_qlineedit')
    self.subtitles_panel_simplelist_properties_ending_timing_qlineedit.setSizePolicy(QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum))
    self.subtitles_panel_simplelist_properties_ending_timing_qlineedit.textEdited.connect(lambda: subtitles_panel_simplelist_properties_ending_timing_qlineedit_text_edited(self))
    self.subtitles_panel_simplelist_properties_ending_timing_frame.layout().addWidget(self.subtitles_panel_simplelist_properties_ending_timing_qlineedit)

    self.subtitles_panel_simplelist_properties_textedit_timings_column.addWidget(self.subtitles_panel_simplelist_properties_ending_timing_frame)

    self.subtitles_panel_simplelist_properties_textedit_line.addLayout(self.subtitles_panel_simplelist_properties_textedit_timings_column)

    self.subtitles_panel_simplelist_properties.layout().addLayout(self.subtitles_panel_simplelist_properties_textedit_line)

    self.subtitles_panel_simplelist_properties_buttons_line = QHBoxLayout()
    self.subtitles_panel_simplelist_properties_buttons_line.setContentsMargins(0, 0, 0, 0)
    self.subtitles_panel_simplelist_properties_buttons_line.setSpacing(0)

    self.send_text_to_last_subtitle_button = QPushButton(self.tr('Send to last').upper())
    self.send_text_to_last_subtitle_button.setObjectName('send_text_to_last_subtitle_button')
    self.send_text_to_last_subtitle_button.setLayout(QHBoxLayout(self.send_text_to_last_subtitle_button))
    self.send_text_to_last_subtitle_button.layout().setContentsMargins(3, 0, 3, 3)
    self.send_text_to_last_subtitle_button.setProperty('class', 'subbutton2_dark')
    self.send_text_to_last_subtitle_button.setStyleSheet('#send_text_to_last_subtitle_button {padding-left: 40px; border-top:0; border-right:0; padding-top:8px; padding-top:5px;}')
    self.send_text_to_last_subtitle_button.clicked.connect(lambda: send_text_to_last_subtitle_button_clicked(self))
    self.subtitles_panel_simplelist_properties_buttons_line.addWidget(self.send_text_to_last_subtitle_button)

    self.send_text_to_last_subtitle_and_slice_button = QPushButton()
    self.send_text_to_last_subtitle_and_slice_button.setObjectName('send_text_to_last_subtitle_and_slice_button')
    self.send_text_to_last_subtitle_and_slice_button.setIcon(QIcon(os.path.join(PATH_SUBTITLD_GRAPHICS, 'slice_selected_subtitle_icon.png')))
    self.send_text_to_last_subtitle_and_slice_button.setProperty('class', 'subbutton2_dark')
    self.send_text_to_last_subtitle_and_slice_button.setStyleSheet('#send_text_to_last_subtitle_and_slice_button {border-top:0; padding-top: 6px;}')
    self.send_text_to_last_subtitle_and_slice_button.clicked.connect(lambda: send_text_to_last_subtitle_and_slice_button_clicked(self))
    self.send_text_to_last_subtitle_and_slice_button.setSizePolicy(QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum))
    self.send_text_to_last_subtitle_button.layout().addWidget(self.send_text_to_last_subtitle_and_slice_button, 0, Qt.AlignLeft)

    self.send_text_to_next_subtitle_button = QPushButton(self.tr('Send to next').upper())
    self.send_text_to_next_subtitle_button.setObjectName('send_text_to_next_subtitle_button')
    self.send_text_to_next_subtitle_button.setLayout(QHBoxLayout(self.send_text_to_next_subtitle_button))
    self.send_text_to_next_subtitle_button.layout().setContentsMargins(3, 0, 3, 3)
    self.send_text_to_next_subtitle_button.setProperty('class', 'subbutton2_dark')
    self.send_text_to_next_subtitle_button.setStyleSheet('#send_text_to_next_subtitle_button {padding-top: 8px; padding-right: 40px; border-top:0; border-left:0; padding-top:5px;}')
    self.send_text_to_next_subtitle_button.clicked.connect(lambda: send_text_to_next_subtitle_button_clicked(self))
    self.subtitles_panel_simplelist_properties_buttons_line.addWidget(self.send_text_to_next_subtitle_button)

    self.send_text_to_next_subtitle_and_slice_button = QPushButton()
    self.send_text_to_next_subtitle_and_slice_button.setObjectName('send_text_to_next_subtitle_and_slice_button')
    self.send_text_to_next_subtitle_and_slice_button.setIcon(QIcon(os.path.join(PATH_SUBTITLD_GRAPHICS, 'slice_selected_subtitle_icon.png')))
    self.send_text_to_next_subtitle_and_slice_button.setProperty('class', 'subbutton2_dark')
    self.send_text_to_next_subtitle_and_slice_button.setStyleSheet('#send_text_to_next_subtitle_and_slice_button {border-top:0; padding-top: 6px;}')
    self.send_text_to_next_subtitle_and_slice_button.clicked.connect(lambda: send_text_to_next_subtitle_and_slice_button_clicked(self))
    self.send_text_to_next_subtitle_and_slice_button.setSizePolicy(QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum))
    self.send_text_to_next_subtitle_button.layout().addWidget(self.send_text_to_next_subtitle_and_slice_button, 0, Qt.AlignRight)

    self.subtitles_panel_simplelist_properties.layout().addLayout(self.subtitles_panel_simplelist_properties_buttons_line)

    self.subtitles_panel_simplelist_widget_vbox.addWidget(self.subtitles_panel_simplelist_properties, 0)

    self.properties_information = QLabel()
    self.properties_information.setWordWrap(True)
    self.properties_information.setObjectName('properties_information')
    self.subtitles_panel_simplelist_widget_vbox.addWidget(self.properties_information)

    self.subtitles_panel_stackedwidgets.addWidget(self.subtitles_panel_simplelist_widget)


def add_button(self):
    self.subtitles_panel_widget_button_list = QPushButton()
    self.subtitles_panel_widget_button_list.setObjectName('subtitles_panel_widget_button_list')
    self.subtitles_panel_widget_button_list.setProperty('class', 'subtitles_panel_left_button')
    self.subtitles_panel_widget_button_list.setCheckable(True)
    self.subtitles_panel_widget_button_list.setChecked(True)
    self.subtitles_panel_widget_button_list.setFixedWidth(23)
    self.subtitles_panel_widget_button_list.clicked.connect(lambda vision: subtitles_panel.update_subtitles_panel_widget_vision(self, 'list'))
    self.subtitles_panel_widget_buttons_vbox.addWidget(self.subtitles_panel_widget_button_list)


def subtitles_panel_markdown_qtextedit_cursorpositionchanged(self):
    position = self.subtitles_panel_markdown_qtextedit.textCursor().position()

    cursor = 0
    # markdown_text = ''
    for subtitle in sorted(self.subtitles_list):
        cursor += len(str("{:.3f}".format(subtitle[0])))
        next_index = self.subtitles_list.index(subtitle) + 1
        if not next_index >= len(self.subtitles_list) and not self.subtitles_list[next_index][0] - 0.001 == subtitle[0] + subtitle[1]:
            cursor += len(' - ' + str("{:.3f}".format(subtitle[0] + subtitle[1])))
        cursor += len('\n')

        cursor += len(str(subtitle[2]) + '\n\n')
        if cursor > position:
            self.selected_subtitle = subtitle
            break

    if self.selected_subtitle:
        if not (self.player_widget.position > self.selected_subtitle[0] and self.player_widget.position < self.selected_subtitle[0] + self.selected_subtitle[1]):
            self.player_widget.seek(self.selected_subtitle[0] + (self.selected_subtitle[1] * .5))

    self.timeline.update(self)
    self.timeline.update_scrollbar(self, position='middle')

    # print(self.selected_subtitle)


def subtitles_panel_markdown_qtextedit_textchanged(self):
    subtitles_panel_markdown_qtextedit_update_subtitles_list(self)


def subtitles_panel_markdown_qtextedit_update_subtitles_list(self):
    sub_list = []

    last_time = []
    last_text = ''
    s = 0
    for line in self.subtitles_panel_markdown_qtextedit.toPlainText().split('\n'):
        if all(utils.is_float(t) for t in line.strip().replace(' - ', ' ').split(' ')):
            this_time = [
                float(line.strip().split(' - ')[0])
            ]

            if ' - ' in line.strip():
                this_time.append(float(line.strip().split(' - ')[-1]))
            else:
                this_time.append(0)

            if last_time:
                sub_list.append(
                    [
                        float(last_time[0]),
                        (float(last_time[1]) - float(last_time[0])) if last_time[1] else (float(this_time[0]) - .001 - float(last_time[0])),
                        last_text.strip()
                    ]
                )
                last_text = ''
                s += 1

            last_time = this_time

        else:
            last_text += line + '\n'

    if last_time:
        sub_list.append(
            [
                float(last_time[0]),
                (float(last_time[1]) - float(last_time[0])) if last_time[1] else (float(this_time[0]) - .001 - float(last_time[0])),
                last_text.strip()
            ]
        )
        last_text = ''

    self.selected_subtitle = False

    # Sanitize subtitles so there is no overlaping subtitles?

    self.subtitles_list = sorted(sub_list)

    self.timeline.update(self)


def update_subtitles_panel_qlistwidget(self):
    """Function to update subtitles list widgets"""

    current_sub, index = subtitles.subtitle_under_current_position(subtitles=self.subtitles_list, position=self.player_widget.position)
    if current_sub and not (self.subtitles_panel_qlistwidget.verticalScrollBar().value() + self.subtitles_panel_qlistwidget.verticalScrollBar().pageStep() > index > self.subtitles_panel_qlistwidget.verticalScrollBar().value()):
        self.subtitles_panel_qlistwidget.verticalScrollBar().setValue(index - 1)

    if self.subtitles_list:
        self.subtitles_panel_qlistwidget_model.subtitles = sorted(self.subtitles_list)
        self.subtitles_panel_qlistwidget_model.layoutChanged.emit()

        # counter = 1
        # for sub in sorted(self.subtitles_list):
        #     print(sub)
        #     item, item_widget = generate_qlistwidget_item_widget(self, counter, sub)

        #     self.subtitles_panel_qlistwidget.addItem(item)
        #     self.subtitles_panel_qlistwidget.setItemWidget(item, item_widget)

        #     counter += 1
    if self.selected_subtitle:
        self.subtitles_panel_qlistwidget.setCurrentIndex(self.subtitles_panel_qlistwidget_model.get_index(self.selected_subtitle))

    update_properties_widget(self)


def subtitles_panel_qlistwidget_item_clicked(self):
    """Function to call when a subtitle item on the list is clicked"""
    if self.subtitles_panel_qlistwidget.currentIndex():
        sub_index = self.subtitles_panel_qlistwidget.currentIndex().row()
        self.selected_subtitle = self.subtitles_list[sub_index]

    if self.selected_subtitle:
        self.properties_textedit.blockSignals(True)
        update_properties_widget(self)
        self.properties_textedit.blockSignals(False)

        if not self.selected_subtitle[0] < self.player_widget.position < self.selected_subtitle[0] + self.selected_subtitle[1]:
            self.player_widget.seek(self.selected_subtitle[0] + (self.selected_subtitle[1] * .5))

        self.timeline.update_scrollbar(self, position='middle')


def send_text_to_next_subtitle_button_clicked(self):
    """Function to call when send text to next subtitle is clicked"""
    pos = self.properties_textedit.textCursor().position()
    last_text = self.properties_textedit.toPlainText()[:pos].strip()
    next_text = self.properties_textedit.toPlainText()[pos:].strip()
    subtitles.send_text_to_next_subtitle(subtitles=self.subtitles_list, selected_subtitle=self.selected_subtitle, last_text=last_text, next_text=next_text)
    subtitles_panel.update_subtitles_panel_widget_vision_content(self)
    self.timeline.update(self)

    self.timeline_widget.setFocus(Qt.TabFocusReason)


def send_text_to_last_subtitle_and_slice_button_clicked(self):
    """Function to send text to the last subtitle and slice at the same time"""
    position = self.player_widget.position
    if not self.selected_subtitle[0] + self.selected_subtitle[1] > self.player_widget.position > self.selected_subtitle[0]:
        position = self.selected_subtitle[0] + (self.selected_subtitle[1] * .5)
    subtitles.subtitle_start_to_current_position(subtitles=self.subtitles_list, position=position)
    subtitles.last_end_to_current_position(subtitles=self.subtitles_list, position=position - .001)
    send_text_to_last_subtitle_button_clicked(self)


def send_text_to_next_subtitle_and_slice_button_clicked(self):
    """Function to send text to the next subtitle and slice at the same time"""
    position = self.player_widget.position
    if not self.selected_subtitle[0] + self.selected_subtitle[1] > self.player_widget.position > self.selected_subtitle[0]:
        position = self.selected_subtitle[0] + (self.selected_subtitle[1] * .5)
    subtitles.subtitle_end_to_current_position(subtitles=self.subtitles_list, position=position)
    subtitles.next_start_to_current_position(subtitles=self.subtitles_list, position=position + .001)
    send_text_to_next_subtitle_button_clicked(self)


def send_text_to_last_subtitle_button_clicked(self):
    """Function to call when send text to last subtitle is clicked"""
    pos = self.properties_textedit.textCursor().position()
    last_text = self.properties_textedit.toPlainText()[:pos].strip()
    next_text = self.properties_textedit.toPlainText()[pos:].strip()
    subtitles.send_text_to_last_subtitle(subtitles=self.subtitles_list, selected_subtitle=self.selected_subtitle, last_text=last_text, next_text=next_text)
    subtitles_panel.update_subtitles_panel_widget_vision_content(self)
    self.timeline.update(self)
    self.timeline_widget.setFocus(Qt.TabFocusReason)


def properties_textedit_changed(self):
    """Function to call when properties textedit is changed"""
    old_selected_subtitle = self.selected_subtitle
    if old_selected_subtitle and old_selected_subtitle[2] != self.properties_textedit.toPlainText():
        counter = self.subtitles_list.index(old_selected_subtitle)
        subtitles.change_subtitle_text(subtitles=self.subtitles_list, selected_subtitle=self.subtitles_list[counter], text=self.properties_textedit.toPlainText())
        self.unsaved = True
        subtitles_panel.update_topbar_status(self)
        self.timeline.update(self)
        self.player.update_subtitle_layer(self)
        update_properties_information(self)


def update_properties_information(self):
    if self.selected_subtitle:
        info_text = '<small>' + self.tr('Words').upper() + ':</small><br><big><b>' + str(len(self.selected_subtitle[2].replace('\n', ' ').split(' '))) + '</b></big><br><br><small>' + self.tr('Characters').upper() + ':</small><br><big><b>' + str(len(self.selected_subtitle[2].replace('\n', '').replace(' ', ''))) + '</b></big>'
        if self.settings['quality_check'].get('enabled', False):
            approved, reasons = quality_check.check_subtitle(self.selected_subtitle, self.settings['quality_check'])
            if not approved:
                info_text += '<br><br><font color="#9e1a1a"><small>' + self.tr('Quality check').upper() + ':</small><br><big><b>'
                for reason in reasons:
                    info_text += str(reason) + '<br><br>'
                info_text += '</b></big></font>'
        self.properties_information.setText(info_text)


def update_properties_widget(self):
    """Function to update properties panel widgets"""
    if self.subtitles_panel_stackedwidgets.currentWidget() == self.subtitles_panel_simplelist_widget:
        update_properties_information(self)
        self.subtitles_panel_simplelist_properties.setVisible(bool(self.selected_subtitle))
        self.subtitles_panel_simplelist_properties_duration_timing_lock_button.raise_()

        text = ''
        if self.selected_subtitle:
            text = self.selected_subtitle[2]

            self.subtitles_panel_simplelist_properties_start_timing_qlineedit.setText(utils.get_timeline_time_str(self.selected_subtitle[0], ms=True))
            self.subtitles_panel_simplelist_properties_duration_timing_qlineedit.setText(utils.get_timeline_time_str(self.selected_subtitle[1], ms=True))
            self.subtitles_panel_simplelist_properties_ending_timing_qlineedit.setText(utils.get_timeline_time_str(self.selected_subtitle[0] + self.selected_subtitle[1], ms=True))

        self.properties_textedit.setText(text)
        self.properties_information.setVisible(bool(self.selected_subtitle) and self.settings['quality_check']['show_statistics'])


def subtitles_panel_simplelist_properties_start_timing_qlineedit_text_edited(self):
    if self.selected_subtitle:
        if not (self.subtitles_panel_simplelist_properties_start_timing_qlineedit.text() == '' or utils.convert_ffmpeg_timecode_to_seconds(self.subtitles_panel_simplelist_properties_start_timing_qlineedit.text()) > self.selected_subtitle[0] + self.selected_subtitle[1]):
            new_start = utils.convert_ffmpeg_timecode_to_seconds(self.subtitles_panel_simplelist_properties_start_timing_qlineedit.text())
            duration = self.selected_subtitle[1] if self.subtitles_panel_simplelist_properties_duration_timing_lock_button.isChecked() else (self.selected_subtitle[0] + self.selected_subtitle[1] - new_start)
            self.selected_subtitle[0] = new_start
            self.selected_subtitle[1] = duration
    self.timeline.update(self)


def subtitles_panel_simplelist_properties_duration_timing_qlineedit_text_edited(self):
    if self.selected_subtitle:
        if self.subtitles_panel_simplelist_properties_duration_timing_qlineedit.text() == '':
            self.subtitles_panel_simplelist_properties_duration_timing_qlineedit.setText(utils.get_timeline_time_str(self.selected_subtitle[1] - self.selected_subtitle[0], ms=True))
        else:
            self.selected_subtitle[1] = utils.convert_ffmpeg_timecode_to_seconds(self.subtitles_panel_simplelist_properties_duration_timing_qlineedit.text())
    self.timeline.update(self)


def subtitles_panel_simplelist_properties_ending_timing_qlineedit_text_edited(self):
    if self.selected_subtitle:
        if self.subtitles_panel_simplelist_properties_ending_timing_qlineedit.text() == '':
            self.subtitles_panel_simplelist_properties_ending_timing_qlineedit.setText(utils.get_timeline_time_str(self.selected_subtitle[0] + self.selected_subtitle[1], ms=True))
        else:
            self.selected_subtitle[1] = utils.convert_ffmpeg_timecode_to_seconds(self.subtitles_panel_simplelist_properties_ending_timing_qlineedit.text()) - utils.convert_ffmpeg_timecode_to_seconds(self.subtitles_panel_simplelist_properties_starting_timing_qlineedit.text())
    self.timeline.update(self)
