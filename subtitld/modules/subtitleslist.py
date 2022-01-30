"""Module for subtitle list panel

"""

import os

from PyQt5.QtGui import QColor, QFont, QFontMetrics, QIcon
from PyQt5.QtWidgets import QHBoxLayout, QLayout, QPushButton, QLabel, QFileDialog, QListView, QMessageBox, QSizePolicy, QStackedWidget, QStyle, QStyledItemDelegate, QTextEdit, QVBoxLayout, QWidget, QLineEdit
from PyQt5.QtCore import QAbstractListModel, QMargins, QPropertyAnimation, QEasingCurve, QRect, Qt, QSize

from subtitld.modules import file_io, quality_check, subtitles
from subtitld.modules.paths import LIST_OF_SUPPORTED_SUBTITLE_EXTENSIONS, PATH_SUBTITLD_GRAPHICS


class subtitles_list_qlistwidget_model(QAbstractListModel):
    def __init__(self, *args, subtitles=None, **kwargs):
        super(subtitles_list_qlistwidget_model, self).__init__(*args, **kwargs)
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


class subtitles_list_qlistwidget_delegate(QStyledItemDelegate):
    def __init__(self, parent=None, settings=None):
        super(subtitles_list_qlistwidget_delegate, self).__init__(parent)
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


def load(self):
    """Function to load subtitles list widgets"""
    self.subtitles_list_widget = QLabel(parent=self)
    self.subtitles_list_widget.setObjectName('subtitles_list_widget')
    self.subtitles_list_widget_animation = QPropertyAnimation(self.subtitles_list_widget, b'geometry')
    self.subtitles_list_widget_animation.setEasingCurve(QEasingCurve.OutCirc)
    self.subtitles_list_widget.setAttribute(Qt.WA_LayoutOnEntireRect)
    self.subtitles_list_widget.setLayout(QVBoxLayout(self.subtitles_list_widget))
    self.subtitles_list_widget.layout().setContentsMargins(0, 20, 35, 210)
    self.subtitles_list_widget.layout().setSpacing(20)

    self.subtitles_list_widget_top_bar = QHBoxLayout()
    self.subtitles_list_widget_top_bar.setSpacing(8)
    self.subtitles_list_widget_top_bar.setContentsMargins(0, 0, 0, 0)

    self.toppanel_format_label = QLabel()
    self.toppanel_format_label.setObjectName('toppanel_format_label')
    self.toppanel_format_label.setProperty('class', 'unsaved')
    self.toppanel_format_label.setLayout(QHBoxLayout(self.toppanel_format_label))
    self.toppanel_format_label.setMinimumHeight(40)
    self.toppanel_format_label.layout().setSpacing(8)
    self.toppanel_format_label.layout().setContentsMargins(0, 0, 0, 0)
    self.toppanel_format_label.layout().setSizeConstraint(QLayout.SetMaximumSize)

    self.toppanel_format_label_text = QLabel()
    self.toppanel_format_label_text.setObjectName('toppanel_format_label_text')
    self.toppanel_format_label_text.setSizePolicy(QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum))
    self.toppanel_format_label.layout().addWidget(self.toppanel_format_label_text)

    self.toppanel_save_button = QPushButton()
    self.toppanel_save_button.setObjectName('toppanel_save_button')
    self.toppanel_save_button.clicked.connect(lambda: toppanel_save_button_clicked(self))
    self.toppanel_save_button.setIcon(QIcon(os.path.join(PATH_SUBTITLD_GRAPHICS, 'save_icon.png')))
    self.toppanel_save_button.setProperty('class', 'subbutton2_dark')
    self.toppanel_save_button.setSizePolicy(QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum))
    self.toppanel_format_label.layout().addWidget(self.toppanel_save_button)

    self.subtitles_list_widget_top_bar.addWidget(self.toppanel_format_label)

    class toppanel_subtitle_file_info_label(QLabel):
        def enterEvent(widget, event):
            self.toppanel_open_button.setVisible(True)
            event.accept()

        def leaveEvent(widget, event):
            self.toppanel_open_button.setVisible(False)
            event.accept()

    self.toppanel_subtitle_file_info_label = toppanel_subtitle_file_info_label()
    self.toppanel_subtitle_file_info_label.setLayout(QHBoxLayout(self.toppanel_subtitle_file_info_label))
    # self.toppanel_subtitle_file_info_label.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum))
    self.toppanel_subtitle_file_info_label.layout().setContentsMargins(0, 5, 5, 5)
    self.toppanel_subtitle_file_info_label.setObjectName('toppanel_subtitle_file_info_label')
    self.subtitles_list_widget_top_bar.addWidget(self.toppanel_subtitle_file_info_label)

    self.toppanel_open_button = QPushButton('Open different file'.upper())
    self.toppanel_open_button.setProperty('class', 'subbutton2_dark')
    self.toppanel_open_button.clicked.connect(lambda: toppanel_open_button_clicked(self))
    self.toppanel_open_button.setIcon(QIcon(os.path.join(PATH_SUBTITLD_GRAPHICS, 'open_icon.png')))
    self.toppanel_open_button.setSizePolicy(QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum))
    # self.toppanel_open_button.setProperty('class', 'button')
    self.toppanel_open_button.setVisible(False)
    self.toppanel_subtitle_file_info_label.layout().addWidget(self.toppanel_open_button, 0, Qt.AlignRight)

    self.subtitles_list_widget.layout().addLayout(self.subtitles_list_widget_top_bar)

    self.subtitles_list_stackedwidgets = QStackedWidget()

    self.subtitles_list_simplelist_widget = QWidget()
    self.subtitles_list_simplelist_widget_vbox = QVBoxLayout(self.subtitles_list_simplelist_widget)
    self.subtitles_list_simplelist_widget_vbox.setContentsMargins(0, 0, 0, 0)
    self.subtitles_list_simplelist_widget_vbox.setSpacing(10)

    self.subtitles_list_qlistwidget_model = subtitles_list_qlistwidget_model()

    self.subtitles_list_qlistwidget_delegate = subtitles_list_qlistwidget_delegate(settings=self.settings)

    self.subtitles_list_qlistwidget = QListView()
    self.subtitles_list_qlistwidget.setViewMode(QListView.ListMode)
    self.subtitles_list_qlistwidget.setObjectName('subtitles_list_qlistwidget')
    self.subtitles_list_qlistwidget.setContentsMargins(QMargins(0, 0, 0, 0))
    self.subtitles_list_qlistwidget.setSpacing(0)
    self.subtitles_list_qlistwidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    self.subtitles_list_qlistwidget.setFocusPolicy(Qt.NoFocus)
    self.subtitles_list_qlistwidget.setIconSize(QSize(42, 42))
    self.subtitles_list_qlistwidget.setModel(self.subtitles_list_qlistwidget_model)
    self.subtitles_list_qlistwidget.setItemDelegate(self.subtitles_list_qlistwidget_delegate)
    self.subtitles_list_qlistwidget.clicked.connect(lambda: subtitles_list_qlistwidget_item_clicked(self))
    self.subtitles_list_simplelist_widget_vbox.addWidget(self.subtitles_list_qlistwidget)

    self.subtitles_list_findandreplace_list = []
    self.subtitles_list_findandreplace_index = None

    self.subtitles_list_findandreplace_toggle_button = QPushButton('Find'.upper(), )  # It will be 'Find and replace'
    self.subtitles_list_findandreplace_toggle_button.setProperty('class', 'button')
    self.subtitles_list_findandreplace_toggle_button.setVisible(False)
    self.subtitles_list_findandreplace_toggle_button.clicked.connect(lambda: subtitles_list_findandreplace_toggle_button_clicked(self))
    self.subtitles_list_simplelist_widget_vbox.addWidget(self.subtitles_list_findandreplace_toggle_button)

    self.subtitles_list_findandreplace_panel = QWidget()
    self.subtitles_list_findandreplace_panel.setWindowFlags(Qt.Tool)
    # self.subtitles_list_findandreplace_panel.setObjectName('QLabel')
    # self.subtitles_list_findandreplace_panel.setStyleSheet('QLabel { border-radius: 4px; background: rgba(106, 116, 131,100); }')
    self.subtitles_list_findandreplace_panel.setVisible(False)
    self.subtitles_list_simplelist_widget_vbox.addWidget(self.subtitles_list_findandreplace_panel)

    self.subtitles_list_findandreplace_find_field = QLineEdit(parent=self.subtitles_list_findandreplace_panel)
    self.subtitles_list_findandreplace_find_field.setObjectName('qlineedit')
    self.subtitles_list_findandreplace_find_field.textChanged.connect(lambda: subtitles_list_findandreplace_find_field_textchanged(self))

    self.subtitles_list_findandreplace_findnext_button = QPushButton('FIND', parent=self.subtitles_list_findandreplace_panel)
    self.subtitles_list_findandreplace_findnext_button.setProperty('class', 'button')
    self.subtitles_list_findandreplace_findnext_button.clicked.connect(lambda: subtitles_list_findandreplace_find_field_clicked(self))

    self.subtitles_list_findandreplace_replace_field = QLineEdit(parent=self.subtitles_list_findandreplace_panel)
    self.subtitles_list_findandreplace_replace_field.setObjectName('qlineedit')
    self.subtitles_list_findandreplace_replace_field.setVisible(False)

    self.subtitles_list_findandreplace_replace_button = QPushButton(parent=self.subtitles_list_findandreplace_panel)
    self.subtitles_list_findandreplace_replace_button.setProperty('class', 'button')
    self.subtitles_list_findandreplace_replace_button.setVisible(False)

    self.subtitles_list_findandreplace_replaceandfindnext_button = QPushButton(parent=self.subtitles_list_findandreplace_panel)
    self.subtitles_list_findandreplace_replaceandfindnext_button.setProperty('class', 'button')
    self.subtitles_list_findandreplace_replaceandfindnext_button.setVisible(False)

    self.subtitles_list_findandreplace_replaceall_button = QPushButton(parent=self.subtitles_list_findandreplace_panel)
    self.subtitles_list_findandreplace_replaceall_button.setProperty('class', 'button')
    self.subtitles_list_findandreplace_replaceall_button.setVisible(False)

    self.subtitles_list_simplelist_properties = QVBoxLayout()
    self.subtitles_list_simplelist_properties.setContentsMargins(20, 0, 0, 0)
    self.subtitles_list_simplelist_properties.setSpacing(0)
    self.subtitles_list_simplelist_properties_buttons_line = QHBoxLayout()
    self.subtitles_list_simplelist_properties_buttons_line.setContentsMargins(0, 0, 0, 0)
    self.subtitles_list_simplelist_properties_buttons_line.setSpacing(0)

    self.properties_textedit = QTextEdit()
    self.properties_textedit.setObjectName('properties_textedit')
    self.properties_textedit.setFixedHeight(120)
    self.properties_textedit.textChanged.connect(lambda: properties_textedit_changed(self))
    self.subtitles_list_simplelist_properties.addWidget(self.properties_textedit)

    self.send_text_to_last_subtitle_button = QPushButton(self.tr('Send to last').upper())
    self.send_text_to_last_subtitle_button.setObjectName('send_text_to_last_subtitle_button')
    self.send_text_to_last_subtitle_button.setLayout(QHBoxLayout(self.send_text_to_last_subtitle_button))
    self.send_text_to_last_subtitle_button.layout().setContentsMargins(3, 0, 3, 3)
    self.send_text_to_last_subtitle_button.setIcon(QIcon(os.path.join(PATH_SUBTITLD_GRAPHICS, 'send_text_to_last_subtitle_icon.png')))
    self.send_text_to_last_subtitle_button.setProperty('class', 'subbutton2_dark')
    self.send_text_to_last_subtitle_button.setStyleSheet('#send_text_to_last_subtitle_button {padding-left: 40px; border-top:0; border-right:0; padding-top:8px; padding-top:5px;}')
    self.send_text_to_last_subtitle_button.clicked.connect(lambda: send_text_to_last_subtitle_button_clicked(self))
    self.subtitles_list_simplelist_properties_buttons_line.addWidget(self.send_text_to_last_subtitle_button)

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
    self.send_text_to_next_subtitle_button.setIcon(QIcon(os.path.join(PATH_SUBTITLD_GRAPHICS, 'send_text_to_next_subtitle_icon.png')))
    self.send_text_to_next_subtitle_button.setProperty('class', 'subbutton2_dark')
    self.send_text_to_next_subtitle_button.setStyleSheet('#send_text_to_next_subtitle_button {padding-top: 8px; padding-right: 40px; border-top:0; border-left:0; padding-top:5px;}')
    self.send_text_to_next_subtitle_button.clicked.connect(lambda: send_text_to_next_subtitle_button_clicked(self))
    self.subtitles_list_simplelist_properties_buttons_line.addWidget(self.send_text_to_next_subtitle_button)

    self.send_text_to_next_subtitle_and_slice_button = QPushButton()
    self.send_text_to_next_subtitle_and_slice_button.setObjectName('send_text_to_next_subtitle_and_slice_button')
    self.send_text_to_next_subtitle_and_slice_button.setIcon(QIcon(os.path.join(PATH_SUBTITLD_GRAPHICS, 'slice_selected_subtitle_icon.png')))
    self.send_text_to_next_subtitle_and_slice_button.setProperty('class', 'subbutton2_dark')
    self.send_text_to_next_subtitle_and_slice_button.setStyleSheet('#send_text_to_next_subtitle_and_slice_button {border-top:0; padding-top: 6px;}')
    self.send_text_to_next_subtitle_and_slice_button.clicked.connect(lambda: send_text_to_next_subtitle_and_slice_button_clicked(self))
    self.send_text_to_next_subtitle_and_slice_button.setSizePolicy(QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum))
    self.send_text_to_next_subtitle_button.layout().addWidget(self.send_text_to_next_subtitle_and_slice_button, 0, Qt.AlignRight)

    self.subtitles_list_simplelist_properties.addLayout(self.subtitles_list_simplelist_properties_buttons_line)

    self.subtitles_list_simplelist_widget_vbox.addLayout(self.subtitles_list_simplelist_properties)

    self.subtitles_list_stackedwidgets.addWidget(self.subtitles_list_simplelist_widget)

    self.subtitles_list_widget.layout().addWidget(self.subtitles_list_stackedwidgets)

    self.properties_information = QLabel()
    self.properties_information.setWordWrap(True)
    self.properties_information.setObjectName('properties_information')
    self.subtitles_list_simplelist_widget_vbox.addWidget(self.properties_information)

    # self.properties_toggle_button = QPushButton(parent=self)
    # self.properties_toggle_button.clicked.connect(lambda: properties_toggle_button_clicked(self))
    # self.properties_toggle_button.setCheckable(True)
    # self.properties_toggle_button.setObjectName('properties_toggle_button')
    # self.properties_toggle_button_animation = QPropertyAnimation(self.properties_toggle_button, b'geometry')
    # self.properties_toggle_button_animation.setEasingCurve(QEasingCurve.OutCirc)

    self.subtitles_list_toggle_button = QPushButton(parent=self)
    self.subtitles_list_toggle_button.setFixedSize(QSize(22, 70))
    self.subtitles_list_toggle_button.clicked.connect(lambda: subtitles_list_toggle_button_clicked(self))
    self.subtitles_list_toggle_button.setCheckable(True)
    self.subtitles_list_toggle_button.setObjectName('subtitles_list_toggle_button')
    self.subtitles_list_toggle_button_animation = QPropertyAnimation(self.subtitles_list_toggle_button, b'geometry')
    self.subtitles_list_toggle_button_animation.setEasingCurve(QEasingCurve.OutCirc)


def resized(self):
    """Function to call when resizing subtitles list"""
    if self.subtitles_list or self.video_metadata:
        self.subtitles_list_widget.setGeometry(0, 0, (self.width() * self.subtitleslist_width_proportion) - 15, self.height())
    else:
        self.subtitles_list_widget.setGeometry(-((self.width() * self.subtitleslist_width_proportion) - 15), 0, (self.width() * self.subtitleslist_width_proportion) - 15, self.height())

    x = self.subtitles_list_widget.x() + self.subtitles_list_widget.width()
    if (self.subtitles_list or self.video_metadata) and self.subtitles_list_toggle_button.isChecked():
        x = self.global_subtitlesvideo_panel_widget.x() + self.global_subtitlesvideo_panel_widget.width()
    x -= self.subtitles_list_toggle_button.width()

    self.subtitles_list_toggle_button.move(x, self.subtitles_list_widget.y())


def subtitles_list_toggle_button_clicked(self):
    """Function to call when clicking toggle button"""
    if self.subtitles_list_toggle_button.isChecked():
        subtitleslist_toggle_button_to_end(self)
        self.global_subtitlesvideo_panel.show_global_subtitlesvideo_panel(self)
        hide(self)
    else:
        self.global_subtitlesvideo_panel.hide_global_subtitlesvideo_panel(self)
        show(self)


def update_topbar_status(self):
    self.toppanel_format_label.setObjectName('toppanel_format_label')
    self.toppanel_format_label.setProperty('class', 'unsaved' if self.unsaved else 'saved')
    self.toppanel_format_label.setStyleSheet(self.toppanel_format_label.styleSheet())


def subtitleslist_toggle_button_to_end(self):
    """Function to show subtitles list panel"""
    self.generate_effect(self.subtitles_list_toggle_button_animation, 'geometry', 700, [self.subtitles_list_toggle_button.x(), self.subtitles_list_toggle_button.y(), self.subtitles_list_toggle_button.width(), self.subtitles_list_toggle_button.height()], [self.global_subtitlesvideo_panel_widget.width() - 22, self.global_subtitlesvideo_panel_widget.y(), self.subtitles_list_toggle_button.width(), self.subtitles_list_toggle_button.height()])


def update_subtitle_list_qlistwidget(self):
    None
    # if self.selected_subtitle:
    #     item, item_widget = generate_qlistwidget_item_widget(self, self.subtitles_list_qlistwidget.currentRow() + 1, self.selected_subtitle)
    #     self.subtitles_list_qlistwidget.setItemWidget(self.subtitles_list_qlistwidget.currentRow(), item_widget)


def update_subtitles_list_qlistwidget(self):
    """Function to update subtitles list widgets"""
    # self.subtitles_list_qlistwidget.clear()
    if self.subtitles_list:
        self.subtitles_list_qlistwidget_model.subtitles = self.subtitles_list
        self.subtitles_list_qlistwidget_model.layoutChanged.emit()

        # counter = 1
        # for sub in sorted(self.subtitles_list):
        #     print(sub)
        #     item, item_widget = generate_qlistwidget_item_widget(self, counter, sub)

        #     self.subtitles_list_qlistwidget.addItem(item)
        #     self.subtitles_list_qlistwidget.setItemWidget(item, item_widget)

        #     counter += 1
    if self.selected_subtitle:
        self.subtitles_list_qlistwidget.setCurrentIndex(self.subtitles_list_qlistwidget_model.get_index(self.selected_subtitle))


def update_subtitleslist_format_label(self):
    self.toppanel_format_label_text.setText(self.format_to_save)


def subtitles_list_qlistwidget_item_clicked(self):
    """Function to call when a subtitle item on the list is clicked"""
    if self.subtitles_list_qlistwidget.currentIndex():
        sub_index = self.subtitles_list_qlistwidget.currentIndex().row()
        self.selected_subtitle = self.subtitles_list[sub_index]

    if self.selected_subtitle:
        if not (self.player_widget.position > self.selected_subtitle[0] and self.player_widget.position < self.selected_subtitle[0] + self.selected_subtitle[1]):
            self.player_widget.seek(self.selected_subtitle[0] + (self.selected_subtitle[1] * .5))

    self.properties_textedit.blockSignals(True)
    update_properties_widget(self)
    self.properties_textedit.blockSignals(False)

    self.timeline.update(self)
    self.timeline.update_scrollbar(self, position='middle')


def show(self):
    """Function to show subtitle list panel"""
    self.generate_effect(self.subtitles_list_widget_animation, 'geometry', 700, [self.subtitles_list_widget.x(), self.subtitles_list_widget.y(), self.subtitles_list_widget.width(), self.subtitles_list_widget.height()], [0, self.subtitles_list_widget.y(), self.subtitles_list_widget.width(), self.subtitles_list_widget.height()])
    self.generate_effect(self.subtitles_list_toggle_button_animation, 'geometry', 700, [self.subtitles_list_toggle_button.x(), self.subtitles_list_toggle_button.y(), self.subtitles_list_toggle_button.width(), self.subtitles_list_toggle_button.height()], [self.subtitles_list_widget.width() - 22, self.subtitles_list_widget.y(), self.subtitles_list_toggle_button.width(), self.subtitles_list_toggle_button.height()])
    self.global_subtitlesvideo_panel.hide_global_subtitlesvideo_panel(self)
    update_toppanel_subtitle_file_info_label(self)
    update_properties_widget(self)


def hide(self):
    """Function to hide subtitle list panel"""
    self.generate_effect(self.subtitles_list_widget_animation, 'geometry', 700, [self.subtitles_list_widget.x(), self.subtitles_list_widget.y(), self.subtitles_list_widget.width(), self.subtitles_list_widget.height()], [-self.subtitles_list_widget.width(), self.subtitles_list_widget.y(), self.subtitles_list_widget.width(), self.subtitles_list_widget.height()])


def toppanel_save_button_clicked(self):
    """Function to call when save button on subtitles list panel is clicked"""
    actual_subtitle_file = False
    if self.actual_subtitle_file:
        for ext in LIST_OF_SUPPORTED_SUBTITLE_EXTENSIONS[self.format_to_save]['extensions']:
            if self.actual_subtitle_file.endswith(ext):
                actual_subtitle_file = self.actual_subtitle_file
                break

    if not actual_subtitle_file:
        suggested_path = os.path.dirname(self.video_metadata['filepath'])
        save_formats = self.format_to_save + ' ' + LIST_OF_SUPPORTED_SUBTITLE_EXTENSIONS[self.format_to_save]['description'] + ' ({})'.format(" ".join(["*.{}".format(fo) for fo in LIST_OF_SUPPORTED_SUBTITLE_EXTENSIONS[self.format_to_save]['extensions']]))

        for extformat in LIST_OF_SUPPORTED_SUBTITLE_EXTENSIONS:
            if not extformat == self.format_to_save:
                save_formats += ';;' + extformat + ' ' + LIST_OF_SUPPORTED_SUBTITLE_EXTENSIONS[extformat]['description'] + ' ({})'.format(" ".join(["*.{}".format(fo) for fo in LIST_OF_SUPPORTED_SUBTITLE_EXTENSIONS[extformat]['extensions']]))
        suggested_name = os.path.basename(self.video_metadata['filepath']).rsplit('.', 1)[0]

        # tem que reportar o bug que não retorna o selectedFilter se o dialogo for nativo
        filedialog = QFileDialog.getSaveFileName(parent=self, caption=self.tr('Select the subtitle file'), directory=os.path.join(suggested_path, suggested_name), filter=save_formats, options=QFileDialog.DontUseNativeDialog)

        if filedialog[0] and filedialog[1]:
            filename = filedialog[0]
            exts = []
            for ext in filedialog[1].split('(', 1)[1].split(')', 1)[0].split('*'):
                if ext:
                    exts.append(ext.strip())
            if not filename.endswith(tuple(exts)):
                filename += exts[0]
            if not self.format_to_save == filedialog[1].split(' ', 1)[0]:
                self.format_to_save = filedialog[1].split(' ', 1)[0]

            self.global_subtitlesvideo_panel.update_global_subtitlesvideo_save_as_combobox(self)

            self.actual_subtitle_file = filename

    if self.actual_subtitle_file:
        file_io.save_file(self.actual_subtitle_file, self.subtitles_list, self.format_to_save, self.selected_language)
        file_io.save_file(self.actual_subtitle_file.rsplit('.', 1)[0] + '.usf', self.subtitles_list, 'USF', self.selected_language)
        self.format_usf_present = True
        update_subtitleslist_format_label(self)
        update_toppanel_subtitle_file_info_label(self)
        self.unsaved = False

    update_topbar_status(self)


def toppanel_open_button_clicked(self, update_interface=True):
    """Function to call when open button on subtitles list panel is clicked"""
    if self.unsaved:
        save_message_box = QMessageBox(self)

        save_message_box.setWindowTitle(self.tr('Unsaved changes'))
        save_message_box.setText(
            self.tr('Do you want to save the changes you made on the subtitles?')
        )
        save_message_box.addButton(self.tr('Save'), QMessageBox.AcceptRole)
        save_message_box.addButton(self.tr("Don't save"), QMessageBox.RejectRole)
        ret = save_message_box.exec_()

        if ret == QMessageBox.AcceptRole:
            self.subttileslist.toppanel_save_button_clicked(self)

    file_io.open_filepath(self)
    update_topbar_status(self)


def subtitles_list_findandreplace_toggle_button_clicked(self):
    self.subtitles_list_findandreplace_panel.setVisible(True)


def subtitles_list_findandreplace_find_field_textchanged(self):
    self.subtitles_list_findandreplace_list = []
    self.subtitles_list_findandreplace_index = None


def subtitles_list_findandreplace_find_field_clicked(self):
    if self.subtitles_list_findandreplace_find_field.text():
        if self.subtitles_list_findandreplace_index is None:
            self.subtitles_list_findandreplace_list = []
            for subtitle in self.subtitles_list:
                if self.subtitles_list_findandreplace_find_field.text() in subtitle[2]:
                    self.subtitles_list_findandreplace_list.append([self.subtitles_list.index(subtitle)])
            self.subtitles_list_findandreplace_index = 0
        subtitles_list_findandreplace_update(self)


def subtitles_list_findandreplace_update(self):
    if self.subtitles_list_findandreplace_index is not None and self.subtitles_list_findandreplace_list:
        self.selected_subtitle = self.subtitles_list[self.subtitles_list_findandreplace_list[self.subtitles_list_findandreplace_index][0]]
        if self.selected_subtitle:
            self.subtitles_list_qlistwidget.setCurrentRow(self.subtitles_list.index(self.selected_subtitle))
            subtitles_list_qlistwidget_item_clicked(self)
            if self.subtitles_list_findandreplace_index < len(self.subtitles_list_findandreplace_list) - 1:
                self.subtitles_list_findandreplace_index += 1
            else:
                self.subtitles_list_findandreplace_index = 0


def update_toppanel_subtitle_file_info_label(self):
    """Function to update top information on subtitles list panel"""
    text = self.tr('Actual video does not have saved subtitle file.')
    if self.actual_subtitle_file:
        text = '<b><small>' + self.tr('Actual project:').upper() + '</small></b><br><big>' + os.path.basename(self.actual_subtitle_file) + '</big>'
    self.toppanel_subtitle_file_info_label.setText(text)


# def properties_toggle_button_clicked(self):
#     """Function to call when panel's toggle button is clicked"""
#     if self.properties_toggle_button.isChecked():
#         hide(self)
#         self.global_properties_panel.show_global_properties_panel(self)
#         properties_toggle_button_to_end(self)
#     else:
#         show(self)
#         self.global_properties_panel.hide_global_properties_panel(self)


# def properties_toggle_button_to_end(self):
#     """Function to show properties panel"""
#     self.generate_effect(self.properties_toggle_button_animation, 'geometry', 700, [self.properties_toggle_button.x(), self.properties_toggle_button.y(), self.properties_toggle_button.width(), self.properties_toggle_button.height()], [int(self.width() * .8), self.properties_toggle_button.y(), self.properties_toggle_button.width(), self.properties_toggle_button.height()])


def update_properties_widget(self):
    """Function to update properties panel widgets"""
    update_properties_information(self)
    self.properties_textedit.setVisible(bool(self.selected_subtitle))
    self.send_text_to_next_subtitle_button.setVisible(bool(self.selected_subtitle))
    self.send_text_to_next_subtitle_and_slice_button.setVisible(bool(self.selected_subtitle))
    self.send_text_to_last_subtitle_button.setVisible(bool(self.selected_subtitle))
    self.send_text_to_last_subtitle_and_slice_button.setVisible(bool(self.selected_subtitle))

    text = ''
    if self.selected_subtitle:
        text = self.selected_subtitle[2]
    self.properties_textedit.setText(text)
    self.properties_information.setVisible(bool(self.selected_subtitle) and self.settings['quality_check']['show_statistics'])


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


def properties_textedit_changed(self):
    """Function to call when properties textedit is changed"""
    old_selected_subtitle = self.selected_subtitle
    if old_selected_subtitle:
        counter = self.subtitles_list.index(old_selected_subtitle)
        self.subtitles_list[counter][2] = self.properties_textedit.toPlainText()
        update_subtitle_list_qlistwidget(self)
        self.timeline.update(self)
        self.player.update_subtitle_layer(self)
        update_properties_information(self)


def send_text_to_next_subtitle_button_clicked(self):
    """Function to call when send text to next subtitle is clicked"""
    pos = self.properties_textedit.textCursor().position()
    last_text = self.properties_textedit.toPlainText()[:pos].strip()
    next_text = self.properties_textedit.toPlainText()[pos:].strip()
    subtitles.send_text_to_next_subtitle(subtitles=self.subtitles_list, selected_subtitle=self.selected_subtitle, last_text=last_text, next_text=next_text)
    update_subtitles_list_qlistwidget(self)
    self.timeline.update(self)
    update_properties_widget(self)
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
    update_subtitles_list_qlistwidget(self)
    self.timeline.update(self)
    update_properties_widget(self)
    self.timeline_widget.setFocus(Qt.TabFocusReason)
