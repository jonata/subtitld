"""Subtitles Video panel

"""

from PySide6.QtWidgets import QPushButton, QWidget, QVBoxLayout, QTabWidget, QLabel, QHBoxLayout, QSpinBox
from PySide6.QtCore import Qt

from subtitld.interface import global_panel


def load_menu(self):
    """Function to load subtitles panel widgets"""
    self.global_panel_interface_menu_button = QPushButton('Interface')
    self.global_panel_interface_menu_button.setCheckable(True)
    self.global_panel_interface_menu_button.setProperty('class', 'global_panel_menu')
    self.global_panel_interface_menu_button.clicked.connect(lambda: global_panel_menu_changed(self))
    self.global_panel_menu.layout().addWidget(self.global_panel_interface_menu_button)


def global_panel_menu_changed(self):
    self.global_panel_interface_menu_button.setEnabled(False)
    global_panel.global_panel_menu_changed(self, self.global_panel_interface_menu_button, self.global_panel_interface_content)


def load_widgets(self):
    """Function to load subtitles panel widgets"""

    self.global_panel_interface_content = QWidget()
    self.global_panel_interface_content.setLayout(QVBoxLayout())
    self.global_panel_interface_content.layout().setContentsMargins(0, 0, 0, 0)
    self.global_panel_interface_content.layout().setSpacing(20)

    self.global_panel_interface_tabwidget = QTabWidget()

    self.global_panel_interface_tabwidget_videoplayer = QWidget()
    self.global_panel_interface_tabwidget_videoplayer.setLayout(QVBoxLayout())
    self.global_panel_interface_tabwidget_videoplayer.layout().setContentsMargins(10, 10, 10, 10)
    self.global_panel_interface_tabwidget_videoplayer.layout().setSpacing(20)

    self.global_panel_interface_videoplayer_fontsize_line = QVBoxLayout()
    self.global_panel_interface_videoplayer_fontsize_line.setContentsMargins(0, 0, 0, 0)
    self.global_panel_interface_videoplayer_fontsize_line.setSpacing(2)

    self.global_panel_interface_videoplayer_fontsize_label = QLabel('Font size')
    self.global_panel_interface_videoplayer_fontsize_label.setProperty('class', 'widget_label')
    self.global_panel_interface_videoplayer_fontsize_line.addWidget(self.global_panel_interface_videoplayer_fontsize_label, 0, Qt.AlignLeft)

    self.global_panel_interface_videoplayer_fontsize_line_2 = QHBoxLayout()
    self.global_panel_interface_videoplayer_fontsize_line_2.setContentsMargins(0, 0, 0, 0)
    self.global_panel_interface_videoplayer_fontsize_line_2.setSpacing(5)

    self.global_panel_interface_videoplayer_fontsize_spinbox = QSpinBox()
    self.global_panel_interface_videoplayer_fontsize_spinbox.setMinimum(1)
    self.global_panel_interface_videoplayer_fontsize_spinbox.setMaximum(999)
    self.global_panel_interface_videoplayer_fontsize_spinbox.valueChanged.connect(lambda: global_panel_interface_videoplayer_fontsize_spinbox_changed(self))
    self.global_panel_interface_videoplayer_fontsize_line_2.addWidget(self.global_panel_interface_videoplayer_fontsize_spinbox, 0, Qt.AlignLeft)

    self.global_panel_interface_videoplayer_fontsize_seconds_label = QLabel('Pixels')
    self.global_panel_interface_videoplayer_fontsize_seconds_label.setProperty('class', 'units_label')
    self.global_panel_interface_videoplayer_fontsize_line_2.addWidget(self.global_panel_interface_videoplayer_fontsize_seconds_label, 0, Qt.AlignLeft)
    self.global_panel_interface_videoplayer_fontsize_line_2.addStretch()

    self.global_panel_interface_videoplayer_fontsize_line.addLayout(self.global_panel_interface_videoplayer_fontsize_line_2)

    self.global_panel_interface_tabwidget_videoplayer.layout().addLayout(self.global_panel_interface_videoplayer_fontsize_line)
    self.global_panel_interface_tabwidget_videoplayer.layout().addStretch()

    self.global_panel_interface_tabwidget.addTab(self.global_panel_interface_tabwidget_videoplayer, 'Video Player')

    self.global_panel_interface_content.layout().addWidget(self.global_panel_interface_tabwidget)

    self.global_panel_content_stacked_widgets.addWidget(self.global_panel_interface_content)

    update_widgets(self)


def global_panel_interface_videoplayer_fontsize_spinbox_changed(self):
    self.settings['videoplayer']['font_size'] = self.global_panel_interface_videoplayer_fontsize_spinbox.value()
    self.player_subtitle_layer.font_size = self.settings['videoplayer']['font_size']


def update_widgets(self):
    self.global_panel_interface_videoplayer_fontsize_spinbox.setValue(self.settings['videoplayer'].get('font_size', 40))
