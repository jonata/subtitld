"""Subtitles Video panel

"""
from PySide6.QtWidgets import QLabel, QComboBox, QPushButton, QWidget, QVBoxLayout, QHBoxLayout
from PySide6.QtCore import Qt

from subtitld.modules.paths import LIST_OF_SUPPORTED_SUBTITLE_EXTENSIONS
from subtitld.interface import global_panel


def load_menu(self):
    """Function to load subtitles panel widgets"""
    self.global_panel_general_menu_button = QPushButton('General')
    self.global_panel_general_menu_button.setCheckable(True)
    self.global_panel_general_menu_button.setProperty('class', 'global_panel_menu')
    self.global_panel_general_menu_button.clicked.connect(lambda: global_panel_menu_changed(self))
    self.global_panel_menu.layout().addWidget(self.global_panel_general_menu_button)


def global_panel_menu_changed(self):
    global_panel.global_panel_menu_changed(self, self.global_panel_general_menu_button, self.global_panel_general_content)


def load_widgets(self):
    """Function to load subtitles panel widgets"""

    self.global_panel_general_content = QWidget()
    self.global_panel_general_content.setLayout(QVBoxLayout())
    self.global_panel_general_content.layout().setContentsMargins(0, 0, 0, 0)
    self.global_panel_general_content.layout().setSpacing(10)

    self.global_panel_general_save_as_line = QVBoxLayout()
    self.global_panel_general_save_as_line.setContentsMargins(0, 0, 0, 0)
    self.global_panel_general_save_as_line.setSpacing(2)

    self.global_subtitlesvideo_save_as_label = QLabel(self.tr('Default format to save:').upper(), parent=self.global_panel_general_content)
    self.global_subtitlesvideo_save_as_label.setProperty('class', 'widget_label')
    self.global_panel_general_save_as_line.addWidget(self.global_subtitlesvideo_save_as_label, 0, Qt.AlignLeft)

    list_of_subtitle_extensions = []
    for extformat in LIST_OF_SUPPORTED_SUBTITLE_EXTENSIONS:
        list_of_subtitle_extensions.append(extformat + ' - ' + LIST_OF_SUPPORTED_SUBTITLE_EXTENSIONS[extformat]['description'])
    self.global_subtitlesvideo_save_as_combobox = QComboBox(parent=self.global_panel_general_content)
    self.global_subtitlesvideo_save_as_combobox.setProperty('class', 'button')
    self.global_subtitlesvideo_save_as_combobox.addItems(list_of_subtitle_extensions)
    # self.global_subtitlesvideo_save_as_combobox.view().window().setWindowFlags(Qt.Popup | Qt.FramelessWindowHint)
    # self.global_subtitlesvideo_save_as_combobox.view().window().setAttribute(Qt.WA_TranslucentBackground)
    self.global_subtitlesvideo_save_as_combobox.activated.connect(lambda: global_subtitlesvideo_save_as_combobox_activated(self))
    self.global_panel_general_save_as_line.addWidget(self.global_subtitlesvideo_save_as_combobox, 0, Qt.AlignLeft)

    self.global_panel_general_content.layout().addLayout(self.global_panel_general_save_as_line)
    self.global_panel_general_content.layout().addStretch()

    self.global_panel_content_stacked_widgets.addWidget(self.global_panel_general_content)

    update_widgets(self)


def global_subtitlesvideo_save_as_combobox_activated(self):
    """Function to change format as combobox selection"""
    self.settings['default_values']['subtitle_format'] = self.global_subtitlesvideo_save_as_combobox.currentText().split(' ', 1)[0]


def update_widgets(self):
    for item in [self.global_subtitlesvideo_save_as_combobox.itemText(i) for i in range(self.global_subtitlesvideo_save_as_combobox.count())]:
        if item.startswith(self.settings['default_values'].get('subtitle_format', 'USF')):
            self.global_subtitlesvideo_save_as_combobox.setCurrentText(item)
            break
