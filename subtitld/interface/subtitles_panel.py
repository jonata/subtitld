"""Module for subtitle list panel

"""

# from multiprocessing.spawn import old_main_modules
import os
import datetime

from PySide6.QtWidgets import QHBoxLayout, QLayout, QPushButton, QLabel, QMessageBox, QSizePolicy, QStackedWidget, QVBoxLayout, QWidget, QLineEdit, QProgressBar, QFileDialog
from PySide6.QtCore import QPropertyAnimation, QEasingCurve, Qt, QSize
from PySide6.QtGui import QTextCursor

from subtitld.interface import subtitles_panel_widget_markdown, subtitles_panel_widget_qlistwidget, subtitles_panel_widget_timeline, timeline
from subtitld.interface.translation import _
from subtitld.modules import file_io
from subtitld.modules import subtitles
from subtitld.modules.paths import LIST_OF_SUPPORTED_SUBTITLE_EXTENSIONS
from subtitld.modules.utils import get_subtitle_format, get_format_from_extension


def load(self):
    """Function to load subtitles list widgets"""
    self.subtitles_panel_widget = QLabel(parent=self)
    self.subtitles_panel_widget.setObjectName('subtitles_panel_widget')
    self.subtitles_panel_widget_animation = QPropertyAnimation(self.subtitles_panel_widget, b'geometry')
    self.subtitles_panel_widget_animation.setEasingCurve(QEasingCurve.OutCirc)
    self.subtitles_panel_widget.setAttribute(Qt.WA_LayoutOnEntireRect)
    self.subtitles_panel_widget.setLayout(QHBoxLayout())
    self.subtitles_panel_widget.layout().setContentsMargins(0, 20, 2, 210)
    self.subtitles_panel_widget.layout().setSpacing(0)

    self.subtitles_panel_widget_vbox = QVBoxLayout()
    self.subtitles_panel_widget_vbox.setContentsMargins(0, 0, 0, 0)
    self.subtitles_panel_widget_vbox.setSpacing(20)

    self.subtitles_panel_widget_top_bar = QHBoxLayout()
    self.subtitles_panel_widget_top_bar.setSpacing(8)
    self.subtitles_panel_widget_top_bar.setContentsMargins(0, 0, 0, 0)

    self.toppanel_format_label = QLabel()
    self.toppanel_format_label.setObjectName('toppanel_format_label')
    self.toppanel_format_label.setProperty('class', 'unsaved')
    self.toppanel_format_label.setLayout(QHBoxLayout())
    # self.toppanel_format_label.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum))
    # self.toppanel_format_label.setMinimumHeight(40)
    self.toppanel_format_label.layout().setSpacing(8)
    self.toppanel_format_label.layout().setContentsMargins(20, 5, 5, 5)
    self.toppanel_format_label.layout().setSizeConstraint(QLayout.SetMinAndMaxSize)

    self.toppanel_format_label_text = QLabel()
    self.toppanel_format_label_text.setObjectName('toppanel_format_label_text')
    self.toppanel_format_label_text.setSizePolicy(QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum))
    self.toppanel_format_label.layout().addWidget(self.toppanel_format_label_text, 0)

    class toppanel_save_button(QPushButton):
        def __init__(widget, parent=None):
            super().__init__(parent)
            widget.key_modifiers = []

        def keyPressEvent(widget, event):
            widget.key_modifiers = event.modifiers()
            event.accept()

        def keyReleaseEvent(widget, event):
            widget.key_modifiers = []
            event.accept()

        # def mouseReleaseEvent(widget, event):
        #     toppanel_save_button_clicked(self)
        #     event.accept()

    self.toppanel_save_button = toppanel_save_button()
    self.toppanel_save_button.setObjectName('toppanel_save_button')
    self.toppanel_save_button.clicked.connect(lambda: toppanel_save_button_clicked(self))
    self.toppanel_save_button.setProperty('class', 'subbutton2_dark')
    # self.toppanel_save_button.setFixedSize(QSize(48, 48))
    self.toppanel_save_button.setSizePolicy(QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum))
    self.toppanel_format_label.layout().addWidget(self.toppanel_save_button, 0)

    self.subtitles_panel_widget_top_bar.addWidget(self.toppanel_format_label, 0)

    class toppanel_subtitle_file_info_label(QLabel):
        def enterEvent(widget, event):
            self.toppanel_open_button.setVisible(True)
            event.accept()

        def leaveEvent(widget, event):
            self.toppanel_open_button.setVisible(False)
            event.accept()

    self.toppanel_subtitle_file_info_label = toppanel_subtitle_file_info_label()
    self.toppanel_subtitle_file_info_label.setLayout(QHBoxLayout(self.toppanel_subtitle_file_info_label))
    self.toppanel_subtitle_file_info_label.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum))
    self.toppanel_subtitle_file_info_label.layout().setContentsMargins(0, 0, 0, 0)
    self.toppanel_subtitle_file_info_label.setObjectName('toppanel_subtitle_file_info_label')

    self.toppanel_open_button = QPushButton()
    self.toppanel_open_button.setObjectName('toppanel_open_button')
    self.toppanel_open_button.setProperty('class', 'subbutton2_dark')
    self.toppanel_open_button.clicked.connect(lambda: toppanel_open_button_clicked(self))
    # self.toppanel_open_button.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum))
    # self.toppanel_open_button.setProperty('class', 'button')
    self.toppanel_open_button.setVisible(False)
    self.toppanel_subtitle_file_info_label.layout().addWidget(self.toppanel_open_button, 0, Qt.AlignRight)

    self.subtitles_panel_widget_top_bar.addWidget(self.toppanel_subtitle_file_info_label, 1)

    self.toppanel_subtitle_file_progress_bar = QProgressBar()
    self.toppanel_subtitle_file_progress_bar.setObjectName('toppanel_subtitle_file_progress_bar')
    self.toppanel_subtitle_file_progress_bar.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum))
    self.toppanel_subtitle_file_progress_bar.setValue(40)
    self.toppanel_subtitle_file_progress_bar.setAlignment(Qt.AlignCenter)
    self.toppanel_subtitle_file_progress_bar.setVisible(False)
    self.subtitles_panel_widget_top_bar.addWidget(self.toppanel_subtitle_file_progress_bar, 1)

    self.subtitles_panel_widget_vbox.layout().addLayout(self.subtitles_panel_widget_top_bar)

    self.subtitles_panel_stackedwidgets = QStackedWidget()

    subtitles_panel_widget_qlistwidget.add_widgets(self)

    subtitles_panel_widget_markdown.add_widgets(self)

    subtitles_panel_widget_timeline.add_widgets(self)

    self.subtitles_panel_widget_vbox.layout().addWidget(self.subtitles_panel_stackedwidgets)
    self.subtitles_panel_widget.layout().addLayout(self.subtitles_panel_widget_vbox)

    self.subtitles_panel_widget_buttons_vbox = QVBoxLayout()
    self.subtitles_panel_widget_buttons_vbox.setContentsMargins(10, 51, 0, 0)
    self.subtitles_panel_widget_buttons_vbox.setSpacing(0)

    subtitles_panel_widget_qlistwidget.add_button(self)

    self.subtitles_panel_widget_buttons_vbox.addSpacing(-10)

    subtitles_panel_widget_markdown.add_button(self)

    self.subtitles_panel_widget_buttons_vbox.addSpacing(-10)

    subtitles_panel_widget_timeline.add_button(self)

    self.subtitles_panel_widget_buttons_vbox.addStretch()

    self.subtitles_panel_findandreplace_list = []
    self.subtitles_panel_findandreplace_index = None

    self.subtitles_panel_findandreplace_toggle_button = QPushButton()  # It will be 'Find and replace'
    self.subtitles_panel_findandreplace_toggle_button.setObjectName('subtitles_panel_findandreplace_toggle_button')
    self.subtitles_panel_findandreplace_toggle_button.setProperty('class', 'button_dark')
    self.subtitles_panel_findandreplace_toggle_button.setProperty('borderless_right', 'true')
    self.subtitles_panel_findandreplace_toggle_button.setFixedWidth(23)
    self.subtitles_panel_findandreplace_toggle_button.clicked.connect(lambda: subtitles_panel_findandreplace_toggle_button_clicked(self))
    self.subtitles_panel_widget_buttons_vbox.addWidget(self.subtitles_panel_findandreplace_toggle_button)

    self.subtitles_panel_findandreplace_panel = QWidget(self)
    self.subtitles_panel_findandreplace_panel.setWindowFlags(Qt.Tool)
    self.subtitles_panel_findandreplace_panel.setObjectName('subtitles_panel_findandreplace_panel')
    self.subtitles_panel_findandreplace_panel.setLayout(QVBoxLayout())
    self.subtitles_panel_findandreplace_panel.layout().setSpacing(5)
    self.subtitles_panel_findandreplace_panel.layout().setContentsMargins(10, 10, 10, 10)
    self.subtitles_panel_findandreplace_panel.setVisible(False)

    self.subtitles_panel_findandreplace_find_line = QWidget(self)
    self.subtitles_panel_findandreplace_find_line.setLayout(QHBoxLayout())
    # self.subtitles_panel_findandreplace_find_line.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum))
    self.subtitles_panel_findandreplace_find_line.layout().setSpacing(0)
    self.subtitles_panel_findandreplace_find_line.layout().setContentsMargins(0, 0, 0, 0)
    self.subtitles_panel_findandreplace_find_line.layout().setSizeConstraint(QLayout.SetMaximumSize)

    self.subtitles_panel_findandreplace_findback_button = QPushButton()
    self.subtitles_panel_findandreplace_findback_button.setObjectName('subtitles_panel_findandreplace_findback_button')
    self.subtitles_panel_findandreplace_findback_button.setProperty('class', 'button_dark')
    self.subtitles_panel_findandreplace_findback_button.setProperty('borderless_right', True)
    self.subtitles_panel_findandreplace_findback_button.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum))
    self.subtitles_panel_findandreplace_findback_button.clicked.connect(lambda: subtitles_panel_findandreplace_findback_field_clicked(self))
    self.subtitles_panel_findandreplace_find_line.layout().addWidget(self.subtitles_panel_findandreplace_findback_button, 0)

    self.subtitles_panel_findandreplace_find_field = QLineEdit()
    self.subtitles_panel_findandreplace_find_field.setObjectName('subtitles_panel_findandreplace_find_field')
    self.subtitles_panel_findandreplace_find_field.setProperty('borderless_right', True)
    self.subtitles_panel_findandreplace_find_field.setProperty('borderless_left', True)
    self.subtitles_panel_findandreplace_find_field.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum))
    self.subtitles_panel_findandreplace_find_field.setFixedWidth(150)
    self.subtitles_panel_findandreplace_find_field.textChanged.connect(lambda: subtitles_panel_findandreplace_find_field_textchanged(self))
    self.subtitles_panel_findandreplace_find_line.layout().addWidget(self.subtitles_panel_findandreplace_find_field, 1)

    self.subtitles_panel_findandreplace_findnext_button = QPushButton()
    self.subtitles_panel_findandreplace_findnext_button.setObjectName('subtitles_panel_findandreplace_findnext_button')
    self.subtitles_panel_findandreplace_findnext_button.setProperty('class', 'button_dark')
    self.subtitles_panel_findandreplace_findnext_button.setProperty('borderless_left', True)
    self.subtitles_panel_findandreplace_findnext_button.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum))
    self.subtitles_panel_findandreplace_findnext_button.clicked.connect(lambda: subtitles_panel_findandreplace_findnext_field_clicked(self))
    self.subtitles_panel_findandreplace_find_line.layout().addWidget(self.subtitles_panel_findandreplace_findnext_button, 0)

    self.subtitles_panel_findandreplace_find_line.layout().addStretch()

    self.subtitles_panel_findandreplace_casesensitive = QPushButton()
    self.subtitles_panel_findandreplace_casesensitive.setObjectName('subtitles_panel_findandreplace_casesensitive')
    self.subtitles_panel_findandreplace_casesensitive.setProperty('class', 'button')
    self.subtitles_panel_findandreplace_casesensitive.setCheckable(True)
    self.subtitles_panel_findandreplace_casesensitive.clicked.connect(lambda: subtitles_panel_findandreplace_casesensitive_clicked(self))
    self.subtitles_panel_findandreplace_find_line.layout().addWidget(self.subtitles_panel_findandreplace_casesensitive, 0)

    self.subtitles_panel_findandreplace_panel.layout().addWidget(self.subtitles_panel_findandreplace_find_line)

    self.subtitles_panel_findandreplace_information_label = QLabel()
    self.subtitles_panel_findandreplace_information_label.setProperty('class', 'qlabel_for_buttons')
    self.subtitles_panel_findandreplace_panel.layout().addWidget(self.subtitles_panel_findandreplace_information_label)

    self.subtitles_panel_findandreplace_replace_line = QWidget(self)
    self.subtitles_panel_findandreplace_replace_line.setLayout(QHBoxLayout())
    self.subtitles_panel_findandreplace_replace_line.layout().setSpacing(0)
    self.subtitles_panel_findandreplace_replace_line.layout().setContentsMargins(0, 0, 0, 0)
    self.subtitles_panel_findandreplace_replace_line.layout().setSizeConstraint(QLayout.SetMaximumSize)

    self.subtitles_panel_findandreplace_replace_field = QLineEdit()
    self.subtitles_panel_findandreplace_replace_field.setObjectName('subtitles_panel_findandreplace_replace_field')
    self.subtitles_panel_findandreplace_replace_field.setProperty('borderless_right', True)
    self.subtitles_panel_findandreplace_replace_field.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum))
    self.subtitles_panel_findandreplace_replace_field.setFixedWidth(150)
    # self.subtitles_panel_findandreplace_replace_field.setFixedHeight(25)
    # self.subtitles_panel_findandreplace_replace_field.setVisible(False)
    self.subtitles_panel_findandreplace_replace_line.layout().addWidget(self.subtitles_panel_findandreplace_replace_field, 1)

    self.subtitles_panel_findandreplace_replaceandfindnext_button = QPushButton()
    self.subtitles_panel_findandreplace_replaceandfindnext_button.setProperty('class', 'button_dark')
    self.subtitles_panel_findandreplace_replaceandfindnext_button.setProperty('borderless_left', True)
    self.subtitles_panel_findandreplace_replaceandfindnext_button.setProperty('borderless_right', True)
    self.subtitles_panel_findandreplace_replaceandfindnext_button.setLayout(QHBoxLayout())
    self.subtitles_panel_findandreplace_replaceandfindnext_button.layout().setContentsMargins(0, 2, 4, 2)
    self.subtitles_panel_findandreplace_replaceandfindnext_button.layout().setSizeConstraint(QLayout.SetMinimumSize)
    self.subtitles_panel_findandreplace_replaceandfindnext_button.clicked.connect(lambda: subtitles_panel_findandreplace_replaceandfindnext_button_clicked(self))

    self.subtitles_panel_findandreplace_replace_button = QPushButton()
    self.subtitles_panel_findandreplace_replace_button.setProperty('class', 'button_dark')
    self.subtitles_panel_findandreplace_replace_button.setProperty('borderless_left', True)
    self.subtitles_panel_findandreplace_replace_button.setObjectName('subtitles_panel_findandreplace_replace_button')
    self.subtitles_panel_findandreplace_replace_button.clicked.connect(lambda: subtitles_panel_findandreplace_replace_button_clicked(self))
    self.subtitles_panel_findandreplace_replaceandfindnext_button.layout().addWidget(self.subtitles_panel_findandreplace_replace_button, 0)

    self.subtitles_panel_findandreplace_replaceandfindnext_button_label = QLabel()
    self.subtitles_panel_findandreplace_replaceandfindnext_button_label.setProperty('class', 'qlabel_for_buttons')
    self.subtitles_panel_findandreplace_replaceandfindnext_button.layout().addWidget(self.subtitles_panel_findandreplace_replaceandfindnext_button_label, 0)

    self.subtitles_panel_findandreplace_replace_line.layout().addWidget(self.subtitles_panel_findandreplace_replaceandfindnext_button, 0)

    self.subtitles_panel_findandreplace_replace_line.layout().addSpacing(1)

    self.subtitles_panel_findandreplace_replaceall_button = QPushButton()
    self.subtitles_panel_findandreplace_replaceall_button.setProperty('class', 'button_dark')
    self.subtitles_panel_findandreplace_replaceall_button.setProperty('borderless_left', True)
    self.subtitles_panel_findandreplace_replaceall_button.clicked.connect(lambda: subtitles_panel_findandreplace_replaceall_button_clicked(self))
    self.subtitles_panel_findandreplace_replace_line.layout().addWidget(self.subtitles_panel_findandreplace_replaceall_button, 0)

    # self.subtitles_panel_findandreplace_replace_line.layout().addStretch()

    self.subtitles_panel_findandreplace_panel.layout().addWidget(self.subtitles_panel_findandreplace_replace_line)

    self.subtitles_panel_findandreplace_panel.setFixedHeight(self.subtitles_panel_findandreplace_panel.minimumSizeHint().height())

    self.subtitles_panel_toggle_button = QPushButton(parent=self)
    self.subtitles_panel_toggle_button.setFixedSize(QSize(22, 70))
    self.subtitles_panel_toggle_button.clicked.connect(lambda: subtitles_panel_toggle_button_clicked(self))
    self.subtitles_panel_toggle_button.setCheckable(True)
    self.subtitles_panel_toggle_button.setObjectName('subtitles_panel_toggle_button')
    self.subtitles_panel_toggle_button_animation = QPropertyAnimation(self.subtitles_panel_toggle_button, b'geometry')
    self.subtitles_panel_toggle_button_animation.setEasingCurve(QEasingCurve.OutCirc)

    self.subtitles_panel_widget.layout().addLayout(self.subtitles_panel_widget_buttons_vbox)

    update_subtitles_panel_widget_vision(self)


def resized(self):
    """Function to call when resizing subtitles list"""
    x = int(-((self.width() * self.subtitles_panel_width_proportion) - 15))
    if (self.subtitles_list or self.video_metadata) and not self.subtitles_panel_toggle_button.isChecked():
        x = 0
    self.subtitles_panel_widget.setGeometry(x, 0, int((self.width() * self.subtitles_panel_width_proportion) - 15), int(self.height()))

    # x = self.subtitles_panel_widget.x() + self.subtitles_panel_widget.width()
    # if (self.subtitles_list or self.video_metadata) and self.subtitles_panel_toggle_button.isChecked():
    #     x = self.global_panel_widget.x() + self.global_panel_widget.width() - self.subtitles_panel_toggle_button.width()
    # x -= self.subtitles_panel_toggle_button.width()

    self.subtitles_panel_toggle_button.move(self.global_panel_widget.x() + self.global_panel_widget.width() - self.subtitles_panel_toggle_button.width(), self.subtitles_panel_widget.y())
    subtitles_panel_widget_timeline.timeline_resized(self)


def subtitles_panel_toggle_button_clicked(self):
    """Function to call when clicking toggle button"""
    if self.subtitles_panel_toggle_button.isChecked():
        subtitles_panel_toggle_button_to_end(self)
        self.global_panel.show_global_panel(self)
        self.playercontrols.hide_playercontrols(self)
        hide(self)
    else:
        self.global_panel.hide_global_panel(self)
        self.playercontrols.show_playercontrols(self)
        show(self)


def update_topbar_status(self):
    # self.toppanel_format_label.setObjectName('toppanel_format_label')
    self.toppanel_format_label.setProperty('class', 'unsaved' if self.unsaved else 'saved')
    self.toppanel_format_label.setStyleSheet(self.toppanel_format_label.styleSheet())


def subtitles_panel_toggle_button_to_end(self):
    """Function to show subtitles list panel"""
    self.generate_effect(self.subtitles_panel_toggle_button_animation, 'geometry', 700, [self.subtitles_panel_toggle_button.x(), self.subtitles_panel_toggle_button.y(), self.subtitles_panel_toggle_button.width(), self.subtitles_panel_toggle_button.height()], [self.global_panel_widget.width() - 22, self.global_panel_widget.y(), self.subtitles_panel_toggle_button.width(), self.subtitles_panel_toggle_button.height()])


def update_subtitles_panel_widget_vision_content(self):
    if self.subtitles_panel_stackedwidgets.currentWidget() == self.subtitles_panel_simplelist_widget:
        subtitles_panel_widget_qlistwidget.update_subtitles_panel_qlistwidget(self)

    elif self.subtitles_panel_stackedwidgets.currentWidget() == self.subtitles_panel_markdown_widget:
        if not self.subtitles_panel_markdown_qtextedit.hasFocus():
            subtitles_panel_widget_markdown.update_subtitles_panel_markdown(self)

    elif self.subtitles_panel_stackedwidgets.currentWidget() == self.subtitles_panel_timeline_widget:
        subtitles_panel_widget_timeline.update_subtitles_panel_timeline(self)


def update_subtitles_panel_format_label(self):
    self.toppanel_format_label_text.setText(get_subtitle_format(self.actual_subtitle_file) or self.settings['default_values'].get('subtitle_format', 'USF'))


def show(self):
    """Function to show subtitle list panel"""
    self.generate_effect(
        self.subtitles_panel_widget_animation,
        'geometry',
        700,
        [int(self.subtitles_panel_widget.x()), int(self.subtitles_panel_widget.y()), int(self.subtitles_panel_widget.width()), int(self.subtitles_panel_widget.height())],
        [0, int(self.subtitles_panel_widget.y()), int(self.subtitles_panel_widget.width()), int(self.subtitles_panel_widget.height())]
    )
    self.generate_effect(self.subtitles_panel_toggle_button_animation, 'geometry', 700, [self.subtitles_panel_toggle_button.x(), self.subtitles_panel_toggle_button.y(), self.subtitles_panel_toggle_button.width(), self.subtitles_panel_toggle_button.height()], [self.subtitles_panel_widget.width() - 22, self.subtitles_panel_widget.y(), self.subtitles_panel_toggle_button.width(), self.subtitles_panel_toggle_button.height()])
    self.global_panel.hide_global_panel(self)
    update_toppanel_subtitle_file_info_label(self)
    update_subtitles_panel_widget_vision_content(self)


def hide(self):
    """Function to hide subtitle list panel"""
    self.generate_effect(self.subtitles_panel_widget_animation, 'geometry', 700, [self.subtitles_panel_widget.x(), self.subtitles_panel_widget.y(), self.subtitles_panel_widget.width(), self.subtitles_panel_widget.height()], [-self.subtitles_panel_widget.width(), self.subtitles_panel_widget.y(), self.subtitles_panel_widget.width(), self.subtitles_panel_widget.height()])


def toppanel_save_button_clicked(self):
    """Function to call when save button on subtitles list panel is clicked"""

    actual_subtitle_file = False
    subtitle_format = get_subtitle_format(self.actual_subtitle_file)
    if subtitle_format:
        actual_subtitle_file = self.actual_subtitle_file
    else:
        subtitle_format = self.settings['default_values'].get('subtitle_format', 'USF')

    if not actual_subtitle_file:
        suggested_path = os.path.dirname(self.video_metadata['filepath'])
        suggested_filename = os.path.basename(self.video_metadata['filepath']).rsplit('.', 1)[0] + '.' + LIST_OF_SUPPORTED_SUBTITLE_EXTENSIONS[subtitle_format]['extensions'][0]

        self.actual_subtitle_file = os.path.join(suggested_path, suggested_filename)

    if self.toppanel_save_button.key_modifiers:
        if Qt.ShiftModifier in self.toppanel_save_button.key_modifiers:
            filedialog_title = 'Save subtitle as'
        if Qt.AltModifier in self.toppanel_save_button.key_modifiers:
            filedialog_title = 'Save a copy of the subtitle as'
        if Qt.ControlModifier in self.toppanel_save_button.key_modifiers:
            filedialog_title = 'Export as'

        supported_subtitle_files = ''
        for exttype in LIST_OF_SUPPORTED_SUBTITLE_EXTENSIONS:
            supported_subtitle_files += LIST_OF_SUPPORTED_SUBTITLE_EXTENSIONS[exttype]['description'] + ' ({})'.format(" ".join(["*.{}".format(fo) for fo in LIST_OF_SUPPORTED_SUBTITLE_EXTENSIONS[exttype]['extensions']])) + ';;'

        filedialog = QFileDialog.getSaveFileName(parent=self, caption=filedialog_title, dir=os.path.dirname(self.actual_subtitle_file), filter=supported_subtitle_files)

        if filedialog[0] and filedialog[1]:
            filepath = filedialog[0]
            selected_extensions = filedialog[1].split('(', 1)[-1].split(')', 1)[0].replace('*.', '').split(' ')
            if not filepath.rsplit('.', 1)[-1].lower() in selected_extensions:
                selected_extension = selected_extensions[0]
                filepath += f'.{selected_extension}'
            else:
                selected_extension = filepath.rsplit('.', 1)[-1].lower()
            selected_format = get_format_from_extension(selected_extension)

            if Qt.ShiftModifier in self.toppanel_save_button.key_modifiers:
                self.actual_subtitle_file = filepath
                self.settings['recent_files'][self.actual_subtitle_file] = {
                    'last_opened': datetime.datetime.now().strftime("%Y%m%d%H%M%S"),
                    'video_filepath': self.video_metadata['filepath']
                }
                file_io.save_file(self.actual_subtitle_file, self.subtitles_list, selected_format, self.selected_language)
                if self.settings['default_values'].get('save_automatic_copy', False) and not subtitle_format == self.settings['default_values'].get('subtitle_format', 'USF'):
                    file_io.save_file(self.actual_subtitle_file.rsplit('.', 1)[0] + '.{}'.format(LIST_OF_SUPPORTED_SUBTITLE_EXTENSIONS[self.settings['default_values'].get('subtitle_format', 'USF')]['extensions'][0]), self.subtitles_list, self.settings['default_values'].get('subtitle_format', 'USF'), self.selected_language)
                update_subtitles_panel_format_label(self)
                update_toppanel_subtitle_file_info_label(self)
                self.unsaved = False

            if Qt.AltModifier in self.toppanel_save_button.key_modifiers:
                file_io.save_file(filepath, self.subtitles_list, selected_format, self.selected_language)

            if Qt.ControlModifier in self.toppanel_save_button.key_modifiers:
                file_io.save_file(filepath, self.subtitles_list, selected_format, self.selected_language)

    elif self.actual_subtitle_file:
        file_io.save_file(self.actual_subtitle_file, self.subtitles_list, subtitle_format, self.selected_language)
        if self.settings['default_values'].get('save_automatic_copy', False) and not subtitle_format == self.settings['default_values'].get('subtitle_format', 'USF'):
            file_io.save_file(self.actual_subtitle_file.rsplit('.', 1)[0] + '.{}'.format(LIST_OF_SUPPORTED_SUBTITLE_EXTENSIONS[self.settings['default_values'].get('subtitle_format', 'USF')]['extensions'][0]), self.subtitles_list, self.settings['default_values'].get('subtitle_format', 'USF'), self.selected_language)
        update_subtitles_panel_format_label(self)
        update_toppanel_subtitle_file_info_label(self)
        self.unsaved = False

    update_topbar_status(self)


def toppanel_open_button_clicked(self):
    """Function to call when open button on subtitles list panel is clicked"""
    if self.unsaved:
        save_message_box = QMessageBox(self)

        save_message_box.setWindowTitle('Unsaved changes')
        save_message_box.setText('Do you want to save the changes you made on the subtitles?')

        save_message_box.addButton('Save', QMessageBox.AcceptRole)
        save_message_box.addButton("Don't save", QMessageBox.RejectRole)
        ret = save_message_box.exec_()

        if ret == QMessageBox.AcceptRole:
            toppanel_save_button_clicked(self)

    file_io.open_filepath(self)
    update_topbar_status(self)


def subtitles_panel_findandreplace_toggle_button_clicked(self):
    self.subtitles_panel_findandreplace_panel.setVisible(True)
    subtitles_panel_findandreplace_find_field_textchanged(self)


def subtitles_panel_findandreplace_find_field_textchanged(self):
    self.subtitles_panel_findandreplace_findback_button.setEnabled(bool(self.subtitles_panel_findandreplace_find_field.text()))
    self.subtitles_panel_findandreplace_findnext_button.setEnabled(bool(self.subtitles_panel_findandreplace_find_field.text()))
    self.subtitles_panel_findandreplace_replaceandfindnext_button.setEnabled(bool(self.subtitles_panel_findandreplace_find_field.text()))
    self.subtitles_panel_findandreplace_replace_button.setEnabled(bool(self.subtitles_panel_findandreplace_find_field.text()))
    self.subtitles_panel_findandreplace_replaceall_button.setEnabled(bool(self.subtitles_panel_findandreplace_find_field.text()))

    subtitles_panel_findandreplace_perform_search(self)

    text = 'Type the text to find'
    if bool(self.subtitles_panel_findandreplace_find_field.text()):
        if self.subtitles_panel_findandreplace_list:
            text = 'Found {} matches'.format(len(self.subtitles_panel_findandreplace_list))
        else:
            text = 'No matches found for "{}"'.format(self.subtitles_panel_findandreplace_find_field.text())

    self.subtitles_panel_findandreplace_information_label.setText(text)


def subtitles_panel_findandreplace_replaceandfindnext_button_clicked(self):
    subtitles_panel_findandreplace_replace_button_clicked(self)
    subtitles_panel_findandreplace_findnext_field_clicked(self)


def subtitles_panel_findandreplace_replace_button_clicked(self):
    if self.selected_subtitle:
        subtitles.change_subtitle_text(subtitles=self.subtitles_list, selected_subtitle=self.selected_subtitle, text=self.selected_subtitle[2][:self.subtitles_panel_findandreplace_list[self.subtitles_panel_findandreplace_index][1]] + self.subtitles_panel_findandreplace_replace_field.text() + self.selected_subtitle[2][self.subtitles_panel_findandreplace_list[self.subtitles_panel_findandreplace_index][1] + self.subtitles_panel_findandreplace_list[self.subtitles_panel_findandreplace_index][2]:])
        self.unsaved = True
        update_topbar_status(self)

    ind = self.subtitles_panel_findandreplace_index
    subtitles_panel_findandreplace_find_field_textchanged(self)
    self.subtitles_panel_findandreplace_index = ind

    if self.subtitles_panel_stackedwidgets.currentWidget() == self.subtitles_panel_simplelist_widget:
        subtitles_panel_widget_qlistwidget.update_properties_widget(self)
    elif self.subtitles_panel_stackedwidgets.currentWidget() == self.subtitles_panel_markdown_widget:
        subtitles_panel_widget_markdown.update_subtitles_panel_markdown(self)
    elif self.subtitles_panel_stackedwidgets.currentWidget() == self.subtitles_panel_timeline_widget:
        subtitles_panel_widget_timeline.update_subtitles_panel_timeline(self)


def subtitles_panel_findandreplace_replaceall_button_clicked(self):
    while self.subtitles_panel_findandreplace_list:
        subtitles_panel_findandreplace_replaceandfindnext_button_clicked(self)
    subtitles_panel_findandreplace_update(self)


def subtitles_panel_findandreplace_casesensitive_clicked(self):
    subtitles_panel_findandreplace_find_field_textchanged(self)


def subtitles_panel_findandreplace_perform_search(self):
    self.subtitles_panel_findandreplace_list = []
    self.subtitles_panel_findandreplace_index = 0

    text_to_search = self.subtitles_panel_findandreplace_find_field.text() if self.subtitles_panel_findandreplace_casesensitive.isChecked() else self.subtitles_panel_findandreplace_find_field.text().lower()
    for subtitle in self.subtitles_list:
        if text_to_search in (subtitle[2] if self.subtitles_panel_findandreplace_casesensitive.isChecked() else subtitle[2].lower()):
            s = 0
            for _ in range((subtitle[2] if self.subtitles_panel_findandreplace_casesensitive.isChecked() else subtitle[2].lower()).count(text_to_search)):
                self.subtitles_panel_findandreplace_list.append([self.subtitles_list.index(subtitle), subtitle[2].find(text_to_search, s), len(text_to_search)])
                s += subtitle[2].find(text_to_search, s) + len(text_to_search)


def subtitles_panel_findandreplace_findback_field_clicked(self):
    self.subtitles_panel_findandreplace_index -= 1
    if self.subtitles_panel_findandreplace_index < 0:
        self.subtitles_panel_findandreplace_index = len(self.subtitles_panel_findandreplace_list) - 1
    subtitles_panel_findandreplace_update(self)


def subtitles_panel_findandreplace_findnext_field_clicked(self):
    self.subtitles_panel_findandreplace_index += 1
    if self.subtitles_panel_findandreplace_index >= len(self.subtitles_panel_findandreplace_list):
        self.subtitles_panel_findandreplace_index = 0
    subtitles_panel_findandreplace_update(self)


def subtitles_panel_findandreplace_update(self):
    if self.subtitles_panel_findandreplace_list:
        self.selected_subtitle = self.subtitles_list[self.subtitles_panel_findandreplace_list[self.subtitles_panel_findandreplace_index][0]]

        if not self.selected_subtitle[0] < self.player_widget.position < self.selected_subtitle[0] + self.selected_subtitle[1]:
            self.player_widget.seek(self.selected_subtitle[0] + (self.selected_subtitle[1] * .5))
            timeline.update_scrollbar(self, position='middle')

        update_subtitles_panel_widget_vision_content(self)
        if self.subtitles_panel_stackedwidgets.currentWidget() == self.subtitles_panel_simplelist_widget:
            c = self.properties_textedit.textCursor()
            c.setPosition(self.subtitles_panel_findandreplace_list[self.subtitles_panel_findandreplace_index][1])
            c.setPosition(self.subtitles_panel_findandreplace_list[self.subtitles_panel_findandreplace_index][1] + self.subtitles_panel_findandreplace_list[self.subtitles_panel_findandreplace_index][2], QTextCursor.KeepAnchor)
            self.properties_textedit.setTextCursor(c)
        elif self.subtitles_panel_stackedwidgets.currentWidget() == self.subtitles_panel_markdown_widget:
            subtitles_panel_widget_markdown.update_subtitles_panel_markdown(self, selection=[self.subtitles_panel_findandreplace_list[self.subtitles_panel_findandreplace_index][1], self.subtitles_panel_findandreplace_list[self.subtitles_panel_findandreplace_index][2]])
        elif self.subtitles_panel_stackedwidgets.currentWidget() == self.subtitles_panel_timeline_widget:
            self.subtitles_panel_timeline_widget_timeline.show_editing_widgets = True
            self.subtitles_panel_timeline_widget_timeline.update_editing_widgets()
            c = self.subtitles_panel_timeline_widget_timeline.text_qtextedit.textCursor()
            c.setPosition(self.subtitles_panel_findandreplace_list[self.subtitles_panel_findandreplace_index][1])
            c.setPosition(self.subtitles_panel_findandreplace_list[self.subtitles_panel_findandreplace_index][1] + self.subtitles_panel_findandreplace_list[self.subtitles_panel_findandreplace_index][2], QTextCursor.KeepAnchor)
            self.subtitles_panel_timeline_widget_timeline.text_qtextedit.setTextCursor(c)
            subtitles_panel_widget_timeline.update_scrollbar(self, position='middle')


def update_toppanel_subtitle_file_info_label(self):
    """Function to update top information on subtitles list panel"""
    text = 'Actual video does not have saved subtitle file.'
    if self.actual_subtitle_file:
        text = '<b><small>' + 'Actual project:'.upper() + '</small></b><br><big>' + os.path.basename(self.actual_subtitle_file) + '</big>'
    self.toppanel_subtitle_file_info_label.setText(text)


def update_subtitles_panel_widget_vision(self, vision='list'):
    if vision == 'list':
        self.subtitles_panel_stackedwidgets.setCurrentWidget(self.subtitles_panel_simplelist_widget)
        self.subtitles_panel_widget_button_list.setEnabled(False)
    else:
        self.subtitles_panel_widget_button_list.setEnabled(True)
        self.subtitles_panel_widget_button_list.setChecked(False)

    if vision == 'markdown':
        self.subtitles_panel_stackedwidgets.setCurrentWidget(self.subtitles_panel_markdown_widget)
        self.subtitles_panel_widget_button_markdown.setEnabled(False)
    else:
        self.subtitles_panel_widget_button_markdown.setEnabled(True)
        self.subtitles_panel_widget_button_markdown.setChecked(False)

    if vision == 'timeline':
        self.subtitles_panel_stackedwidgets.setCurrentWidget(self.subtitles_panel_timeline_widget)
        self.subtitles_panel_widget_button_timeline.setEnabled(False)
        subtitles_panel_widget_timeline.timeline_resized(self)
    else:
        self.subtitles_panel_widget_button_timeline.setEnabled(True)
        self.subtitles_panel_widget_button_timeline.setChecked(False)

    update_subtitles_panel_widget_vision_content(self)


def update_processing_status(self, show_widgets=False, value=0):
    self.toppanel_subtitle_file_progress_bar.setVisible(show_widgets)
    self.toppanel_subtitle_file_progress_bar.setValue(value)
    self.toppanel_subtitle_file_info_label.setVisible(not show_widgets)


def translate_widgets(self):
    self.subtitles_panel_findandreplace_replaceandfindnext_button_label.setText(_('subtitles_panel.and_find_next'))
    self.toppanel_open_button.setText(_('subtitles_panel.open_different_file'))
    self.subtitles_panel_findandreplace_findnext_button.setText(_('subtitles_panel.find'))
    self.subtitles_panel_findandreplace_replace_button.setText(_('subtitles_panel.replace'))
    self.subtitles_panel_findandreplace_replaceall_button.setText(_('subtitles_panel.replace_all'))
    subtitles_panel_widget_qlistwidget.translate_widgets(self)
