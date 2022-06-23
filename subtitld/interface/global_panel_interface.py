"""Subtitles Video panel

"""

from PySide6.QtWidgets import QPushButton, QWidget

from subtitld.interface import global_panel


def load_menu(self):
    """Function to load subtitles panel widgets"""
    self.global_panel_interface_menu_button = QPushButton('Interface')
    self.global_panel_interface_menu_button.setCheckable(True)
    self.global_panel_interface_menu_button.setProperty('class', 'global_panel_menu')
    self.global_panel_interface_menu_button.clicked.connect(lambda: global_panel_menu_changed(self))
    self.global_panel_menu.layout().addWidget(self.global_panel_interface_menu_button)


def global_panel_menu_changed(self):
    global_panel.global_panel_menu_changed(self, self.global_panel_interface_menu_button, self.global_panel_interface_content)


def load_widgets(self):
    """Function to load subtitles panel widgets"""

    self.global_panel_interface_content = QWidget()
    self.global_panel_content_stacked_widgets.addWidget(self.global_panel_interface_content)
