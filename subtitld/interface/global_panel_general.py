"""Subtitles Video panel

"""
from PyQt5.QtWidgets import QLabel, QComboBox, QPushButton, QWidget, QGridLayout, QHBoxLayout
from PyQt5.QtCore import Qt

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
    self.global_panel_general_content.setLayout(QHBoxLayout())

    self.global_panel_general_content_grid = QGridLayout()

    self.global_subtitlesvideo_save_as_label = QLabel(self.tr('Default format to save:').upper(), parent=self.global_panel_general_content)
    self.global_panel_general_content_grid.addWidget(self.global_subtitlesvideo_save_as_label, 0, 0, Qt.AlignTop)

    list_of_subtitle_extensions = []
    for extformat in LIST_OF_SUPPORTED_SUBTITLE_EXTENSIONS:
        list_of_subtitle_extensions.append(extformat + ' - ' + LIST_OF_SUPPORTED_SUBTITLE_EXTENSIONS[extformat]['description'])
    self.global_subtitlesvideo_save_as_combobox = QComboBox(parent=self.global_panel_general_content)
    self.global_subtitlesvideo_save_as_combobox.setProperty('class', 'button')
    self.global_subtitlesvideo_save_as_combobox.addItems(list_of_subtitle_extensions)
    self.global_subtitlesvideo_save_as_combobox.activated.connect(lambda: global_subtitlesvideo_save_as_combobox_activated(self))
    self.global_panel_general_content_grid.addWidget(self.global_subtitlesvideo_save_as_combobox, 0, 1, Qt.AlignTop)

    self.global_panel_general_content.layout().addLayout(self.global_panel_general_content_grid)
    self.global_panel_general_content.layout().addStretch()

    self.global_panel_content_stacked_widgets.addWidget(self.global_panel_general_content)


def global_subtitlesvideo_save_as_combobox_activated(self):
    """Function to change format as combobox selection"""
    self.format_to_save = self.global_subtitlesvideo_save_as_combobox.currentText().split(' ', 1)[0]
