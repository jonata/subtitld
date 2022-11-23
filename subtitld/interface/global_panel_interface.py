from PySide6.QtWidgets import QPushButton, QWidget, QVBoxLayout, QTabWidget, QLabel, QHBoxLayout, QSpinBox, QComboBox, QGroupBox, QColorDialog
from PySide6.QtCore import Qt
from PySide6.QtGui import QFontDatabase, QColor

from subtitld.interface import global_panel
from subtitld.interface.translation import _


def load_menu(self):
    """Function to load subtitles panel widgets"""
    self.global_panel_interface_menu_button = QPushButton()
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

    self.global_panel_interface_videoplayer_font_group = QGroupBox()
    self.global_panel_interface_videoplayer_font_group.setLayout(QHBoxLayout())
    self.global_panel_interface_videoplayer_font_group.layout().setContentsMargins(10, 10, 10, 10)
    self.global_panel_interface_videoplayer_font_group.layout().setSpacing(20)

    self.global_panel_interface_videoplayer_fontsize_line = QVBoxLayout()
    self.global_panel_interface_videoplayer_fontsize_line.setContentsMargins(0, 0, 0, 0)
    self.global_panel_interface_videoplayer_fontsize_line.setSpacing(2)

    self.global_panel_interface_videoplayer_fontsize_label = QLabel()
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

    self.global_panel_interface_videoplayer_fontsize_seconds_label = QLabel()
    self.global_panel_interface_videoplayer_fontsize_seconds_label.setProperty('class', 'units_label')
    self.global_panel_interface_videoplayer_fontsize_line_2.addWidget(self.global_panel_interface_videoplayer_fontsize_seconds_label, 0, Qt.AlignLeft)
    # self.global_panel_interface_videoplayer_fontsize_line_2.addStretch()

    self.global_panel_interface_videoplayer_fontsize_line.addLayout(self.global_panel_interface_videoplayer_fontsize_line_2)

    self.global_panel_interface_videoplayer_font_group.layout().addLayout(self.global_panel_interface_videoplayer_fontsize_line)

    self.global_panel_interface_videoplayer_fontfamily_line = QVBoxLayout()
    self.global_panel_interface_videoplayer_fontfamily_line.setContentsMargins(0, 0, 0, 0)
    self.global_panel_interface_videoplayer_fontfamily_line.setSpacing(2)

    self.global_panel_interface_videoplayer_fontfamily_label = QLabel()
    self.global_panel_interface_videoplayer_fontfamily_label.setProperty('class', 'widget_label')
    self.global_panel_interface_videoplayer_fontfamily_line.addWidget(self.global_panel_interface_videoplayer_fontfamily_label, 0, Qt.AlignLeft)

    self.global_panel_interface_videoplayer_fontfamily_line_2 = QHBoxLayout()
    self.global_panel_interface_videoplayer_fontfamily_line_2.setContentsMargins(0, 0, 0, 0)
    self.global_panel_interface_videoplayer_fontfamily_line_2.setSpacing(5)

    fonts = QFontDatabase().families()
    self.global_panel_interface_videoplayer_fontfamily_combobox = QComboBox()
    self.global_panel_interface_videoplayer_fontfamily_combobox.addItems(fonts)
    self.global_panel_interface_videoplayer_fontfamily_combobox.activated.connect(lambda: global_panel_interface_videoplayer_fontfamily_combobox_changed(self))
    self.global_panel_interface_videoplayer_fontfamily_line_2.addWidget(self.global_panel_interface_videoplayer_fontfamily_combobox, 0, Qt.AlignLeft)

    self.global_panel_interface_videoplayer_fontfamily_line.addLayout(self.global_panel_interface_videoplayer_fontfamily_line_2)

    self.global_panel_interface_videoplayer_font_group.layout().addLayout(self.global_panel_interface_videoplayer_fontfamily_line)

    self.global_panel_interface_videoplayer_color_vbox = QVBoxLayout()
    self.global_panel_interface_videoplayer_color_vbox.setContentsMargins(0, 0, 0, 0)
    self.global_panel_interface_videoplayer_color_vbox.setSpacing(2)

    self.global_panel_interface_videoplayer_color_label = QLabel()
    self.global_panel_interface_videoplayer_color_label.setProperty('class', 'widget_label')
    self.global_panel_interface_videoplayer_color_vbox.addWidget(self.global_panel_interface_videoplayer_color_label, 0, Qt.AlignLeft)

    self.global_panel_interface_videoplayer_color_button = QPushButton()
    self.global_panel_interface_videoplayer_color_button.setProperty('class', 'color_pick_button')
    self.global_panel_interface_videoplayer_color_button.setFixedWidth(80)
    self.global_panel_interface_videoplayer_color_button.clicked.connect(lambda: global_panel_interface_videoplayer_color_button_clicked(self))

    self.global_panel_interface_videoplayer_color_vbox.addWidget(self.global_panel_interface_videoplayer_color_button, 0, Qt.AlignLeft)

    self.global_panel_interface_videoplayer_font_group.layout().addLayout(self.global_panel_interface_videoplayer_color_vbox)

    self.global_panel_interface_videoplayer_font_group.layout().addStretch()

    self.global_panel_interface_tabwidget_videoplayer.layout().addWidget(self.global_panel_interface_videoplayer_font_group)

    self.global_panel_interface_videoplayer_shadow_group = QGroupBox()
    self.global_panel_interface_videoplayer_shadow_group.setCheckable(True)
    self.global_panel_interface_videoplayer_shadow_group.setLayout(QHBoxLayout())
    self.global_panel_interface_videoplayer_shadow_group.toggled.connect(lambda: global_panel_interface_videoplayer_shadow_group_toggled(self))
    self.global_panel_interface_videoplayer_shadow_group.layout().setContentsMargins(10, 10, 10, 10)
    self.global_panel_interface_videoplayer_shadow_group.layout().setSpacing(20)

    self.global_panel_interface_videoplayer_shadow_x_position_vbox = QVBoxLayout()
    self.global_panel_interface_videoplayer_shadow_x_position_vbox.setContentsMargins(0, 0, 0, 0)
    self.global_panel_interface_videoplayer_shadow_x_position_vbox.setSpacing(2)

    self.global_panel_interface_videoplayer_shadow_x_position_label = QLabel()
    self.global_panel_interface_videoplayer_shadow_x_position_label.setProperty('class', 'widget_label')
    self.global_panel_interface_videoplayer_shadow_x_position_vbox.addWidget(self.global_panel_interface_videoplayer_shadow_x_position_label, 0, Qt.AlignLeft)

    self.global_panel_interface_videoplayer_shadow_x_position_line = QHBoxLayout()
    self.global_panel_interface_videoplayer_shadow_x_position_line.setContentsMargins(0, 0, 0, 0)
    self.global_panel_interface_videoplayer_shadow_x_position_line.setSpacing(5)

    self.global_panel_interface_videoplayer_shadow_x_position = QSpinBox()
    self.global_panel_interface_videoplayer_shadow_x_position.setMinimum(-99999)
    self.global_panel_interface_videoplayer_shadow_x_position.setMaximum(99999)
    self.global_panel_interface_videoplayer_shadow_x_position.valueChanged.connect(lambda: global_panel_interface_videoplayer_shadow_x_position_changed(self))
    self.global_panel_interface_videoplayer_shadow_x_position_line.addWidget(self.global_panel_interface_videoplayer_shadow_x_position, 0, Qt.AlignLeft)

    self.global_panel_interface_videoplayer_shadow_x_position_pixels_label = QLabel()
    self.global_panel_interface_videoplayer_shadow_x_position_pixels_label.setProperty('class', 'units_label')
    self.global_panel_interface_videoplayer_shadow_x_position_line.addWidget(self.global_panel_interface_videoplayer_shadow_x_position_pixels_label, 0, Qt.AlignLeft)

    self.global_panel_interface_videoplayer_shadow_x_position_vbox.addLayout(self.global_panel_interface_videoplayer_shadow_x_position_line)

    self.global_panel_interface_videoplayer_shadow_group.layout().addLayout(self.global_panel_interface_videoplayer_shadow_x_position_vbox)

    self.global_panel_interface_videoplayer_shadow_y_position_vbox = QVBoxLayout()
    self.global_panel_interface_videoplayer_shadow_y_position_vbox.setContentsMargins(0, 0, 0, 0)
    self.global_panel_interface_videoplayer_shadow_y_position_vbox.setSpacing(2)

    self.global_panel_interface_videoplayer_shadow_y_position_label = QLabel()
    self.global_panel_interface_videoplayer_shadow_y_position_label.setProperty('class', 'widget_label')
    self.global_panel_interface_videoplayer_shadow_y_position_vbox.addWidget(self.global_panel_interface_videoplayer_shadow_y_position_label, 0, Qt.AlignLeft)

    self.global_panel_interface_videoplayer_shadow_y_position_line = QHBoxLayout()
    self.global_panel_interface_videoplayer_shadow_y_position_line.setContentsMargins(0, 0, 0, 0)
    self.global_panel_interface_videoplayer_shadow_y_position_line.setSpacing(5)

    self.global_panel_interface_videoplayer_shadow_y_position = QSpinBox()
    self.global_panel_interface_videoplayer_shadow_y_position.setMinimum(-99999)
    self.global_panel_interface_videoplayer_shadow_y_position.setMaximum(99999)
    self.global_panel_interface_videoplayer_shadow_y_position.valueChanged.connect(lambda: global_panel_interface_videoplayer_shadow_y_position_changed(self))
    self.global_panel_interface_videoplayer_shadow_y_position_line.addWidget(self.global_panel_interface_videoplayer_shadow_y_position, 0, Qt.AlignLeft)

    self.global_panel_interface_videoplayer_shadow_y_position_pixels_label = QLabel()
    self.global_panel_interface_videoplayer_shadow_y_position_pixels_label.setProperty('class', 'units_label')
    self.global_panel_interface_videoplayer_shadow_y_position_line.addWidget(self.global_panel_interface_videoplayer_shadow_y_position_pixels_label, 0, Qt.AlignLeft)

    self.global_panel_interface_videoplayer_shadow_y_position_vbox.addLayout(self.global_panel_interface_videoplayer_shadow_y_position_line)

    self.global_panel_interface_videoplayer_shadow_color_vbox = QVBoxLayout()
    self.global_panel_interface_videoplayer_shadow_color_vbox.setContentsMargins(0, 0, 0, 0)
    self.global_panel_interface_videoplayer_shadow_color_vbox.setSpacing(2)

    self.global_panel_interface_videoplayer_shadow_color_label = QLabel()
    self.global_panel_interface_videoplayer_shadow_color_label.setProperty('class', 'widget_label')
    self.global_panel_interface_videoplayer_shadow_color_vbox.addWidget(self.global_panel_interface_videoplayer_shadow_color_label, 0, Qt.AlignLeft)

    self.global_panel_interface_videoplayer_shadow_color_button = QPushButton()
    self.global_panel_interface_videoplayer_shadow_color_button.setProperty('class', 'color_pick_button')
    self.global_panel_interface_videoplayer_shadow_color_button.setFixedWidth(80)
    self.global_panel_interface_videoplayer_shadow_color_button.clicked.connect(lambda: global_panel_interface_videoplayer_shadow_color_button_clicked(self))

    self.global_panel_interface_videoplayer_shadow_color_vbox.addWidget(self.global_panel_interface_videoplayer_shadow_color_button, 0, Qt.AlignLeft)

    self.global_panel_interface_videoplayer_shadow_group.layout().addLayout(self.global_panel_interface_videoplayer_shadow_color_vbox)

    self.global_panel_interface_videoplayer_shadow_group.layout().addStretch()

    self.global_panel_interface_tabwidget_videoplayer.layout().addWidget(self.global_panel_interface_videoplayer_shadow_group)

    self.global_panel_interface_videoplayer_backgroundbox_group = QGroupBox()
    self.global_panel_interface_videoplayer_backgroundbox_group.setCheckable(True)
    self.global_panel_interface_videoplayer_backgroundbox_group.setLayout(QHBoxLayout())
    self.global_panel_interface_videoplayer_backgroundbox_group.toggled.connect(lambda: global_panel_interface_videoplayer_backgroundbox_group_toggled(self))
    self.global_panel_interface_videoplayer_backgroundbox_group.layout().setContentsMargins(10, 10, 10, 10)
    self.global_panel_interface_videoplayer_backgroundbox_group.layout().setSpacing(20)

    self.global_panel_interface_videoplayer_backgroundbox_padding_vbox = QVBoxLayout()
    self.global_panel_interface_videoplayer_backgroundbox_padding_vbox.setContentsMargins(0, 0, 0, 0)
    self.global_panel_interface_videoplayer_backgroundbox_padding_vbox.setSpacing(2)

    self.global_panel_interface_videoplayer_backgroundbox_padding_label = QLabel()
    self.global_panel_interface_videoplayer_backgroundbox_padding_label.setProperty('class', 'widget_label')
    self.global_panel_interface_videoplayer_backgroundbox_padding_vbox.addWidget(self.global_panel_interface_videoplayer_backgroundbox_padding_label, 0, Qt.AlignLeft)

    self.global_panel_interface_videoplayer_backgroundbox_padding_line = QHBoxLayout()
    self.global_panel_interface_videoplayer_backgroundbox_padding_line.setContentsMargins(0, 0, 0, 0)
    self.global_panel_interface_videoplayer_backgroundbox_padding_line.setSpacing(5)

    self.global_panel_interface_videoplayer_backgroundbox_padding = QSpinBox()
    self.global_panel_interface_videoplayer_backgroundbox_padding.setMinimum(-99999)
    self.global_panel_interface_videoplayer_backgroundbox_padding.setMaximum(99999)
    self.global_panel_interface_videoplayer_backgroundbox_padding.valueChanged.connect(lambda: global_panel_interface_videoplayer_backgroundbox_padding_changed(self))
    self.global_panel_interface_videoplayer_backgroundbox_padding_line.addWidget(self.global_panel_interface_videoplayer_backgroundbox_padding, 0, Qt.AlignLeft)

    self.global_panel_interface_videoplayer_backgroundbox_padding_pixels_label = QLabel()
    self.global_panel_interface_videoplayer_backgroundbox_padding_pixels_label.setProperty('class', 'units_label')
    self.global_panel_interface_videoplayer_backgroundbox_padding_line.addWidget(self.global_panel_interface_videoplayer_backgroundbox_padding_pixels_label, 0, Qt.AlignLeft)

    self.global_panel_interface_videoplayer_backgroundbox_padding_vbox.addLayout(self.global_panel_interface_videoplayer_backgroundbox_padding_line)

    self.global_panel_interface_videoplayer_backgroundbox_group.layout().addLayout(self.global_panel_interface_videoplayer_backgroundbox_padding_vbox)

    self.global_panel_interface_videoplayer_backgroundbox_border_radius_vbox = QVBoxLayout()
    self.global_panel_interface_videoplayer_backgroundbox_border_radius_vbox.setContentsMargins(0, 0, 0, 0)
    self.global_panel_interface_videoplayer_backgroundbox_border_radius_vbox.setSpacing(2)

    self.global_panel_interface_videoplayer_backgroundbox_border_radius_label = QLabel()
    self.global_panel_interface_videoplayer_backgroundbox_border_radius_label.setProperty('class', 'widget_label')
    self.global_panel_interface_videoplayer_backgroundbox_border_radius_vbox.addWidget(self.global_panel_interface_videoplayer_backgroundbox_border_radius_label, 0, Qt.AlignLeft)

    self.global_panel_interface_videoplayer_backgroundbox_border_radius_line = QHBoxLayout()
    self.global_panel_interface_videoplayer_backgroundbox_border_radius_line.setContentsMargins(0, 0, 0, 0)
    self.global_panel_interface_videoplayer_backgroundbox_border_radius_line.setSpacing(5)

    self.global_panel_interface_videoplayer_backgroundbox_border_radius = QSpinBox()
    self.global_panel_interface_videoplayer_backgroundbox_border_radius.setMinimum(0)
    self.global_panel_interface_videoplayer_backgroundbox_border_radius.setMaximum(99999)
    self.global_panel_interface_videoplayer_backgroundbox_border_radius.valueChanged.connect(lambda: global_panel_interface_videoplayer_backgroundbox_border_radius_changed(self))
    self.global_panel_interface_videoplayer_backgroundbox_border_radius_line.addWidget(self.global_panel_interface_videoplayer_backgroundbox_border_radius, 0, Qt.AlignLeft)

    self.global_panel_interface_videoplayer_backgroundbox_border_radius_pixels_label = QLabel('%')
    self.global_panel_interface_videoplayer_backgroundbox_border_radius_pixels_label.setProperty('class', 'units_label')
    self.global_panel_interface_videoplayer_backgroundbox_border_radius_line.addWidget(self.global_panel_interface_videoplayer_backgroundbox_border_radius_pixels_label, 0, Qt.AlignLeft)

    self.global_panel_interface_videoplayer_backgroundbox_border_radius_vbox.addLayout(self.global_panel_interface_videoplayer_backgroundbox_border_radius_line)

    self.global_panel_interface_videoplayer_backgroundbox_group.layout().addLayout(self.global_panel_interface_videoplayer_backgroundbox_border_radius_vbox)

    self.global_panel_interface_videoplayer_backgroundbox_color_vbox = QVBoxLayout()
    self.global_panel_interface_videoplayer_backgroundbox_color_vbox.setContentsMargins(0, 0, 0, 0)
    self.global_panel_interface_videoplayer_backgroundbox_color_vbox.setSpacing(2)

    self.global_panel_interface_videoplayer_backgroundbox_color_label = QLabel()
    self.global_panel_interface_videoplayer_backgroundbox_color_label.setProperty('class', 'widget_label')
    self.global_panel_interface_videoplayer_backgroundbox_color_vbox.addWidget(self.global_panel_interface_videoplayer_backgroundbox_color_label, 0, Qt.AlignLeft)

    self.global_panel_interface_videoplayer_backgroundbox_color_button = QPushButton()
    self.global_panel_interface_videoplayer_backgroundbox_color_button.setProperty('class', 'color_pick_button')
    self.global_panel_interface_videoplayer_backgroundbox_color_button.setFixedWidth(80)
    self.global_panel_interface_videoplayer_backgroundbox_color_button.clicked.connect(lambda: global_panel_interface_videoplayer_backgroundbox_color_button_clicked(self))

    self.global_panel_interface_videoplayer_backgroundbox_color_vbox.addWidget(self.global_panel_interface_videoplayer_backgroundbox_color_button, 0, Qt.AlignLeft)

    self.global_panel_interface_videoplayer_backgroundbox_group.layout().addLayout(self.global_panel_interface_videoplayer_backgroundbox_color_vbox)

    self.global_panel_interface_videoplayer_backgroundbox_group.layout().addStretch()

    self.global_panel_interface_tabwidget_videoplayer.layout().addWidget(self.global_panel_interface_videoplayer_backgroundbox_group)

    self.global_panel_interface_videoplayer_safe_margin_action_group = QGroupBox()
    self.global_panel_interface_videoplayer_safe_margin_action_group.setCheckable(True)
    self.global_panel_interface_videoplayer_safe_margin_action_group.setLayout(QHBoxLayout())
    self.global_panel_interface_videoplayer_safe_margin_action_group.toggled.connect(lambda: global_panel_interface_videoplayer_safe_margin_action_group_toggled(self))
    self.global_panel_interface_videoplayer_safe_margin_action_group.layout().setContentsMargins(10, 10, 10, 10)
    self.global_panel_interface_videoplayer_safe_margin_action_group.layout().setSpacing(20)

    self.global_panel_interface_videoplayer_safe_margin_action_x_margin_vbox = QVBoxLayout()
    self.global_panel_interface_videoplayer_safe_margin_action_x_margin_vbox.setContentsMargins(0, 0, 0, 0)
    self.global_panel_interface_videoplayer_safe_margin_action_x_margin_vbox.setSpacing(2)

    self.global_panel_interface_videoplayer_safe_margin_action_x_margin_label = QLabel()
    self.global_panel_interface_videoplayer_safe_margin_action_x_margin_label.setProperty('class', 'widget_label')
    self.global_panel_interface_videoplayer_safe_margin_action_x_margin_vbox.addWidget(self.global_panel_interface_videoplayer_safe_margin_action_x_margin_label, 0, Qt.AlignLeft)

    self.global_panel_interface_videoplayer_safe_margin_action_x_margin_line = QHBoxLayout()
    self.global_panel_interface_videoplayer_safe_margin_action_x_margin_line.setContentsMargins(0, 0, 0, 0)
    self.global_panel_interface_videoplayer_safe_margin_action_x_margin_line.setSpacing(5)

    self.global_panel_interface_videoplayer_safe_margin_action_x_margin = QSpinBox()
    self.global_panel_interface_videoplayer_safe_margin_action_x_margin.setMinimum(0)
    self.global_panel_interface_videoplayer_safe_margin_action_x_margin.setMaximum(50)
    self.global_panel_interface_videoplayer_safe_margin_action_x_margin.valueChanged.connect(lambda: global_panel_interface_videoplayer_safe_margin_action_x_margin_changed(self))
    self.global_panel_interface_videoplayer_safe_margin_action_x_margin_line.addWidget(self.global_panel_interface_videoplayer_safe_margin_action_x_margin, 0, Qt.AlignLeft)

    self.global_panel_interface_videoplayer_safe_margin_action_x_margin_pixels_label = QLabel('%')
    self.global_panel_interface_videoplayer_safe_margin_action_x_margin_pixels_label.setProperty('class', 'units_label')
    self.global_panel_interface_videoplayer_safe_margin_action_x_margin_line.addWidget(self.global_panel_interface_videoplayer_safe_margin_action_x_margin_pixels_label, 0, Qt.AlignLeft)

    self.global_panel_interface_videoplayer_safe_margin_action_x_margin_vbox.addLayout(self.global_panel_interface_videoplayer_safe_margin_action_x_margin_line)

    self.global_panel_interface_videoplayer_safe_margin_action_group.layout().addLayout(self.global_panel_interface_videoplayer_safe_margin_action_x_margin_vbox)

    self.global_panel_interface_videoplayer_safe_margin_action_y_margin_vbox = QVBoxLayout()
    self.global_panel_interface_videoplayer_safe_margin_action_y_margin_vbox.setContentsMargins(0, 0, 0, 0)
    self.global_panel_interface_videoplayer_safe_margin_action_y_margin_vbox.setSpacing(2)

    self.global_panel_interface_videoplayer_safe_margin_action_y_margin_label = QLabel()
    self.global_panel_interface_videoplayer_safe_margin_action_y_margin_label.setProperty('class', 'widget_label')
    self.global_panel_interface_videoplayer_safe_margin_action_y_margin_vbox.addWidget(self.global_panel_interface_videoplayer_safe_margin_action_y_margin_label, 0, Qt.AlignLeft)

    self.global_panel_interface_videoplayer_safe_margin_action_y_margin_line = QHBoxLayout()
    self.global_panel_interface_videoplayer_safe_margin_action_y_margin_line.setContentsMargins(0, 0, 0, 0)
    self.global_panel_interface_videoplayer_safe_margin_action_y_margin_line.setSpacing(5)

    self.global_panel_interface_videoplayer_safe_margin_action_y_margin = QSpinBox()
    self.global_panel_interface_videoplayer_safe_margin_action_y_margin.setMinimum(0)
    self.global_panel_interface_videoplayer_safe_margin_action_y_margin.setMaximum(50)
    self.global_panel_interface_videoplayer_safe_margin_action_y_margin.valueChanged.connect(lambda: global_panel_interface_videoplayer_safe_margin_action_y_margin_changed(self))
    self.global_panel_interface_videoplayer_safe_margin_action_y_margin_line.addWidget(self.global_panel_interface_videoplayer_safe_margin_action_y_margin, 0, Qt.AlignLeft)

    self.global_panel_interface_videoplayer_safe_margin_action_y_margin_pixels_label = QLabel()
    self.global_panel_interface_videoplayer_safe_margin_action_y_margin_pixels_label.setProperty('class', 'units_label')
    self.global_panel_interface_videoplayer_safe_margin_action_y_margin_line.addWidget(self.global_panel_interface_videoplayer_safe_margin_action_y_margin_pixels_label, 0, Qt.AlignLeft)

    self.global_panel_interface_videoplayer_safe_margin_action_y_margin_vbox.addLayout(self.global_panel_interface_videoplayer_safe_margin_action_y_margin_line)

    self.global_panel_interface_videoplayer_safe_margin_action_group.layout().addLayout(self.global_panel_interface_videoplayer_safe_margin_action_y_margin_vbox)

    self.global_panel_interface_videoplayer_safe_margin_action_color_vbox = QVBoxLayout()
    self.global_panel_interface_videoplayer_safe_margin_action_color_vbox.setContentsMargins(0, 0, 0, 0)
    self.global_panel_interface_videoplayer_safe_margin_action_color_vbox.setSpacing(2)

    self.global_panel_interface_videoplayer_safe_margin_action_color_label = QLabel()
    self.global_panel_interface_videoplayer_safe_margin_action_color_label.setProperty('class', 'widget_label')
    self.global_panel_interface_videoplayer_safe_margin_action_color_vbox.addWidget(self.global_panel_interface_videoplayer_safe_margin_action_color_label, 0, Qt.AlignLeft)

    self.global_panel_interface_videoplayer_safe_margin_action_color_button = QPushButton()
    self.global_panel_interface_videoplayer_safe_margin_action_color_button.setProperty('class', 'color_pick_button')
    self.global_panel_interface_videoplayer_safe_margin_action_color_button.setFixedWidth(80)
    self.global_panel_interface_videoplayer_safe_margin_action_color_button.clicked.connect(lambda: global_panel_interface_videoplayer_safe_margin_action_color_button_clicked(self))

    self.global_panel_interface_videoplayer_safe_margin_action_color_vbox.addWidget(self.global_panel_interface_videoplayer_safe_margin_action_color_button, 0, Qt.AlignLeft)

    self.global_panel_interface_videoplayer_safe_margin_action_group.layout().addLayout(self.global_panel_interface_videoplayer_safe_margin_action_color_vbox)

    self.global_panel_interface_videoplayer_safe_margin_action_group.layout().addStretch()

    self.global_panel_interface_tabwidget_videoplayer.layout().addWidget(self.global_panel_interface_videoplayer_safe_margin_action_group)

    self.global_panel_interface_videoplayer_safe_margin_title_group = QGroupBox()
    self.global_panel_interface_videoplayer_safe_margin_title_group.setCheckable(True)
    self.global_panel_interface_videoplayer_safe_margin_title_group.setLayout(QHBoxLayout())
    self.global_panel_interface_videoplayer_safe_margin_title_group.toggled.connect(lambda: global_panel_interface_videoplayer_safe_margin_title_group_toggled(self))
    self.global_panel_interface_videoplayer_safe_margin_title_group.layout().setContentsMargins(10, 10, 10, 10)
    self.global_panel_interface_videoplayer_safe_margin_title_group.layout().setSpacing(20)

    self.global_panel_interface_videoplayer_safe_margin_title_x_margin_vbox = QVBoxLayout()
    self.global_panel_interface_videoplayer_safe_margin_title_x_margin_vbox.setContentsMargins(0, 0, 0, 0)
    self.global_panel_interface_videoplayer_safe_margin_title_x_margin_vbox.setSpacing(2)

    self.global_panel_interface_videoplayer_safe_margin_title_x_margin_label = QLabel()
    self.global_panel_interface_videoplayer_safe_margin_title_x_margin_label.setProperty('class', 'widget_label')
    self.global_panel_interface_videoplayer_safe_margin_title_x_margin_vbox.addWidget(self.global_panel_interface_videoplayer_safe_margin_title_x_margin_label, 0, Qt.AlignLeft)

    self.global_panel_interface_videoplayer_safe_margin_title_x_margin_line = QHBoxLayout()
    self.global_panel_interface_videoplayer_safe_margin_title_x_margin_line.setContentsMargins(0, 0, 0, 0)
    self.global_panel_interface_videoplayer_safe_margin_title_x_margin_line.setSpacing(5)

    self.global_panel_interface_videoplayer_safe_margin_title_x_margin = QSpinBox()
    self.global_panel_interface_videoplayer_safe_margin_title_x_margin.setMinimum(0)
    self.global_panel_interface_videoplayer_safe_margin_title_x_margin.setMaximum(50)
    self.global_panel_interface_videoplayer_safe_margin_title_x_margin.valueChanged.connect(lambda: global_panel_interface_videoplayer_safe_margin_title_x_margin_changed(self))
    self.global_panel_interface_videoplayer_safe_margin_title_x_margin_line.addWidget(self.global_panel_interface_videoplayer_safe_margin_title_x_margin, 0, Qt.AlignLeft)

    self.global_panel_interface_videoplayer_safe_margin_title_x_margin_pixels_label = QLabel()
    self.global_panel_interface_videoplayer_safe_margin_title_x_margin_pixels_label.setProperty('class', 'units_label')
    self.global_panel_interface_videoplayer_safe_margin_title_x_margin_line.addWidget(self.global_panel_interface_videoplayer_safe_margin_title_x_margin_pixels_label, 0, Qt.AlignLeft)

    self.global_panel_interface_videoplayer_safe_margin_title_x_margin_vbox.addLayout(self.global_panel_interface_videoplayer_safe_margin_title_x_margin_line)

    self.global_panel_interface_videoplayer_safe_margin_title_group.layout().addLayout(self.global_panel_interface_videoplayer_safe_margin_title_x_margin_vbox)

    self.global_panel_interface_videoplayer_safe_margin_title_y_margin_vbox = QVBoxLayout()
    self.global_panel_interface_videoplayer_safe_margin_title_y_margin_vbox.setContentsMargins(0, 0, 0, 0)
    self.global_panel_interface_videoplayer_safe_margin_title_y_margin_vbox.setSpacing(2)

    self.global_panel_interface_videoplayer_safe_margin_title_y_margin_label = QLabel()
    self.global_panel_interface_videoplayer_safe_margin_title_y_margin_label.setProperty('class', 'widget_label')
    self.global_panel_interface_videoplayer_safe_margin_title_y_margin_vbox.addWidget(self.global_panel_interface_videoplayer_safe_margin_title_y_margin_label, 0, Qt.AlignLeft)

    self.global_panel_interface_videoplayer_safe_margin_title_y_margin_line = QHBoxLayout()
    self.global_panel_interface_videoplayer_safe_margin_title_y_margin_line.setContentsMargins(0, 0, 0, 0)
    self.global_panel_interface_videoplayer_safe_margin_title_y_margin_line.setSpacing(5)

    self.global_panel_interface_videoplayer_safe_margin_title_y_margin = QSpinBox()
    self.global_panel_interface_videoplayer_safe_margin_title_y_margin.setMinimum(0)
    self.global_panel_interface_videoplayer_safe_margin_title_y_margin.setMaximum(50)
    self.global_panel_interface_videoplayer_safe_margin_title_y_margin.valueChanged.connect(lambda: global_panel_interface_videoplayer_safe_margin_title_y_margin_changed(self))
    self.global_panel_interface_videoplayer_safe_margin_title_y_margin_line.addWidget(self.global_panel_interface_videoplayer_safe_margin_title_y_margin, 0, Qt.AlignLeft)

    self.global_panel_interface_videoplayer_safe_margin_title_y_margin_pixels_label = QLabel()
    self.global_panel_interface_videoplayer_safe_margin_title_y_margin_pixels_label.setProperty('class', 'units_label')
    self.global_panel_interface_videoplayer_safe_margin_title_y_margin_line.addWidget(self.global_panel_interface_videoplayer_safe_margin_title_y_margin_pixels_label, 0, Qt.AlignLeft)

    self.global_panel_interface_videoplayer_safe_margin_title_y_margin_vbox.addLayout(self.global_panel_interface_videoplayer_safe_margin_title_y_margin_line)

    self.global_panel_interface_videoplayer_safe_margin_title_group.layout().addLayout(self.global_panel_interface_videoplayer_safe_margin_title_y_margin_vbox)

    self.global_panel_interface_videoplayer_safe_margin_title_color_vbox = QVBoxLayout()
    self.global_panel_interface_videoplayer_safe_margin_title_color_vbox.setContentsMargins(0, 0, 0, 0)
    self.global_panel_interface_videoplayer_safe_margin_title_color_vbox.setSpacing(2)

    self.global_panel_interface_videoplayer_safe_margin_title_color_label = QLabel()
    self.global_panel_interface_videoplayer_safe_margin_title_color_label.setProperty('class', 'widget_label')
    self.global_panel_interface_videoplayer_safe_margin_title_color_vbox.addWidget(self.global_panel_interface_videoplayer_safe_margin_title_color_label, 0, Qt.AlignLeft)

    self.global_panel_interface_videoplayer_safe_margin_title_color_button = QPushButton()
    self.global_panel_interface_videoplayer_safe_margin_title_color_button.setProperty('class', 'color_pick_button')
    self.global_panel_interface_videoplayer_safe_margin_title_color_button.setFixedWidth(80)
    self.global_panel_interface_videoplayer_safe_margin_title_color_button.clicked.connect(lambda: global_panel_interface_videoplayer_safe_margin_title_color_button_clicked(self))

    self.global_panel_interface_videoplayer_safe_margin_title_color_vbox.addWidget(self.global_panel_interface_videoplayer_safe_margin_title_color_button, 0, Qt.AlignLeft)

    self.global_panel_interface_videoplayer_safe_margin_title_group.layout().addLayout(self.global_panel_interface_videoplayer_safe_margin_title_color_vbox)

    self.global_panel_interface_videoplayer_safe_margin_title_group.layout().addStretch()

    self.global_panel_interface_tabwidget_videoplayer.layout().addWidget(self.global_panel_interface_videoplayer_safe_margin_title_group)

    self.global_panel_interface_tabwidget_videoplayer.layout().addStretch()

    self.global_panel_interface_tabwidget.addTab(self.global_panel_interface_tabwidget_videoplayer, '')

    self.global_panel_interface_content.layout().addWidget(self.global_panel_interface_tabwidget)

    self.global_panel_content_stacked_widgets.addWidget(self.global_panel_interface_content)

    update_widgets(self)


def global_panel_interface_videoplayer_fontfamily_combobox_changed(self):
    self.settings['videoplayer']['font_family'] = self.global_panel_interface_videoplayer_fontfamily_combobox.currentText()
    self.player_subtitle_layer.update_style(self.settings['videoplayer'])


def global_panel_interface_videoplayer_fontsize_spinbox_changed(self):
    self.settings['videoplayer']['font_size'] = self.global_panel_interface_videoplayer_fontsize_spinbox.value()
    self.player_subtitle_layer.update_style(self.settings['videoplayer'])


def global_panel_interface_videoplayer_shadow_group_toggled(self):
    self.settings['videoplayer']['shadow_enabled'] = self.global_panel_interface_videoplayer_shadow_group.isChecked()
    self.player_subtitle_layer.update_style(self.settings['videoplayer'])


def global_panel_interface_videoplayer_shadow_x_position_changed(self):
    self.settings['videoplayer']['shadow_x'] = self.global_panel_interface_videoplayer_shadow_x_position.value()
    self.player_subtitle_layer.update_style(self.settings['videoplayer'])


def global_panel_interface_videoplayer_shadow_y_position_changed(self):
    self.settings['videoplayer']['shadow_y'] = self.global_panel_interface_videoplayer_shadow_y_position.value()
    self.player_subtitle_layer.update_style(self.settings['videoplayer'])


def global_panel_interface_videoplayer_shadow_color_button_clicked(self):
    color = QColorDialog.getColor(options=QColorDialog.ShowAlphaChannel)
    if color.isValid():
        self.settings['videoplayer']['shadow_color'] = color.name(QColor.HexArgb)
    self.player_subtitle_layer.update_style(self.settings['videoplayer'])
    update_widgets(self)


def global_panel_interface_videoplayer_color_button_clicked(self):
    color = QColorDialog.getColor(options=QColorDialog.ShowAlphaChannel)
    if color.isValid():
        self.settings['videoplayer']['color'] = color.name(QColor.HexArgb)
    self.player_subtitle_layer.update_style(self.settings['videoplayer'])
    update_widgets(self)


def global_panel_interface_videoplayer_backgroundbox_group_toggled(self):
    self.settings['videoplayer']['safe_margin_action_enabled'] = self.global_panel_interface_videoplayer_backgroundbox_group.isChecked()
    self.player_subtitle_layer.update_style(self.settings['videoplayer'])


def global_panel_interface_videoplayer_backgroundbox_padding_changed(self):
    self.settings['videoplayer']['backgroundbox_padding'] = self.global_panel_interface_videoplayer_backgroundbox_padding.value()
    self.player_subtitle_layer.update_style(self.settings['videoplayer'])


def global_panel_interface_videoplayer_backgroundbox_border_radius_changed(self):
    self.settings['videoplayer']['backgroundbox_border_radius'] = self.global_panel_interface_videoplayer_backgroundbox_border_radius.value()
    self.player_subtitle_layer.update_style(self.settings['videoplayer'])


def global_panel_interface_videoplayer_backgroundbox_color_button_clicked(self):
    color = QColorDialog.getColor(options=QColorDialog.ShowAlphaChannel)
    if color.isValid():
        self.settings['videoplayer']['backgroundbox_color'] = color.name(QColor.HexArgb)
    self.player_subtitle_layer.update_style(self.settings['videoplayer'])
    update_widgets(self)


def global_panel_interface_videoplayer_safe_margin_action_group_toggled(self):
    self.settings['videoplayer']['safe_margin_action_enabled'] = self.global_panel_interface_videoplayer_safe_margin_action_group.isChecked()
    self.player_subtitle_layer.update_style(self.settings['videoplayer'])


def global_panel_interface_videoplayer_safe_margin_action_x_margin_changed(self):
    self.settings['videoplayer']['safe_margin_action_x'] = self.global_panel_interface_videoplayer_safe_margin_action_x_margin.value()
    self.player_subtitle_layer.update_style(self.settings['videoplayer'])


def global_panel_interface_videoplayer_safe_margin_action_y_margin_changed(self):
    self.settings['videoplayer']['safe_margin_action_y'] = self.global_panel_interface_videoplayer_safe_margin_action_y_margin.value()
    self.player_subtitle_layer.update_style(self.settings['videoplayer'])


def global_panel_interface_videoplayer_safe_margin_action_color_button_clicked(self):
    color = QColorDialog.getColor(options=QColorDialog.ShowAlphaChannel)
    if color.isValid():
        self.settings['videoplayer']['safe_margin_action_color'] = color.name(QColor.HexArgb)
    self.player_subtitle_layer.update_style(self.settings['videoplayer'])
    update_widgets(self)


def global_panel_interface_videoplayer_safe_margin_title_group_toggled(self):
    self.settings['videoplayer']['safe_margin_title_enabled'] = self.global_panel_interface_videoplayer_safe_margin_title_group.isChecked()
    self.player_subtitle_layer.update_style(self.settings['videoplayer'])


def global_panel_interface_videoplayer_safe_margin_title_x_margin_changed(self):
    self.settings['videoplayer']['safe_margin_title_x'] = self.global_panel_interface_videoplayer_safe_margin_title_x_margin.value()
    self.player_subtitle_layer.update_style(self.settings['videoplayer'])


def global_panel_interface_videoplayer_safe_margin_title_y_margin_changed(self):
    self.settings['videoplayer']['safe_margin_title_y'] = self.global_panel_interface_videoplayer_safe_margin_title_y_margin.value()
    self.player_subtitle_layer.update_style(self.settings['videoplayer'])


def global_panel_interface_videoplayer_safe_margin_title_color_button_clicked(self):
    color = QColorDialog.getColor(options=QColorDialog.ShowAlphaChannel)
    if color.isValid():
        self.settings['videoplayer']['safe_margin_title_color'] = color.name(QColor.HexArgb)
    self.player_subtitle_layer.update_style(self.settings['videoplayer'])
    update_widgets(self)


def update_widgets(self):
    self.global_panel_interface_videoplayer_fontsize_spinbox.setValue(self.settings['videoplayer'].get('font_size', 40))
    self.global_panel_interface_videoplayer_fontfamily_combobox.setCurrentText(self.settings['videoplayer'].get('font_family', 'Ubuntu'))
    self.global_panel_interface_videoplayer_color_button.setStyleSheet('QPushButton { background-color: ' + self.settings['videoplayer'].get('color', '#ffffffff') + ' }')
    self.global_panel_interface_videoplayer_shadow_group.setChecked(self.settings['videoplayer'].get('shadow_enabled', True))
    self.global_panel_interface_videoplayer_shadow_x_position.setValue(self.settings['videoplayer'].get('shadow_x', 2))
    self.global_panel_interface_videoplayer_shadow_y_position.setValue(self.settings['videoplayer'].get('shadow_y', 2))
    self.global_panel_interface_videoplayer_shadow_color_button.setStyleSheet('QPushButton { background-color: ' + self.settings['videoplayer'].get('shadow_color', '#ff000000') + ' }')
    self.global_panel_interface_videoplayer_backgroundbox_group.setChecked(self.settings['videoplayer'].get('backgroundbox_enabled', True))
    self.global_panel_interface_videoplayer_backgroundbox_padding.setValue(self.settings['videoplayer'].get('backgroundbox_padding', 10))
    self.global_panel_interface_videoplayer_backgroundbox_border_radius.setValue(self.settings['videoplayer'].get('backgroundbox_border_radius', 5))
    self.global_panel_interface_videoplayer_backgroundbox_color_button.setStyleSheet('QPushButton { background-color: ' + self.settings['videoplayer'].get('backgroundbox_color', '#55000000') + ' }')
    self.global_panel_interface_videoplayer_safe_margin_action_group.setChecked(self.settings['videoplayer'].get('safe_margin_action_enabled', False))
    self.global_panel_interface_videoplayer_safe_margin_action_x_margin.setValue(self.settings['videoplayer'].get('safe_margin_action_x', 5))
    self.global_panel_interface_videoplayer_safe_margin_action_y_margin.setValue(self.settings['videoplayer'].get('safe_margin_action_y', 5))
    self.global_panel_interface_videoplayer_safe_margin_action_color_button.setStyleSheet('QPushButton { background-color: ' + self.settings['videoplayer'].get('safe_margin_action_color', '#dd67FF4D') + ' }')
    self.global_panel_interface_videoplayer_safe_margin_title_group.setChecked(self.settings['videoplayer'].get('safe_margin_title_enabled', False))
    self.global_panel_interface_videoplayer_safe_margin_title_x_margin.setValue(self.settings['videoplayer'].get('safe_margin_title_x', 10))
    self.global_panel_interface_videoplayer_safe_margin_title_y_margin.setValue(self.settings['videoplayer'].get('safe_margin_title_y', 10))
    self.global_panel_interface_videoplayer_safe_margin_title_color_button.setStyleSheet('QPushButton { background-color: ' + self.settings['videoplayer'].get('safe_margin_title_color', '#ddff0000') + ' }')


def translate_widgets(self):
    self.global_panel_interface_menu_button.setText(_('global_panel_interface.title'))
    self.global_panel_interface_videoplayer_font_group.setTitle(_('units.font'))
    self.global_panel_interface_videoplayer_fontsize_label.setText(_('units.size'))
    self.global_panel_interface_videoplayer_fontsize_seconds_label.setText(_('units.pixels'))
    self.global_panel_interface_videoplayer_fontfamily_label.setText(_('units.font_family'))
    self.global_panel_interface_videoplayer_color_label.setText(_('units.color'))
    self.global_panel_interface_videoplayer_shadow_group.setTitle(_('global_panel_interface.shadow'))
    self.global_panel_interface_videoplayer_shadow_x_position_label.setText(_('global_panel_interface.x_position'))
    self.global_panel_interface_videoplayer_shadow_y_position_label.setText(_('global_panel_interface.y_position'))
    self.global_panel_interface_videoplayer_shadow_y_position_pixels_label.setText(_('units.pixels'))
    self.global_panel_interface_videoplayer_shadow_color_label.setText(_('units.color'))
    self.global_panel_interface_videoplayer_backgroundbox_group.setTitle(_('global_panel_interface.background_box'))
    self.global_panel_interface_videoplayer_backgroundbox_padding_label.setText(_('units.padding'))
    self.global_panel_interface_videoplayer_backgroundbox_padding_pixels_label.setText(_('units.pixels'))
    self.global_panel_interface_videoplayer_backgroundbox_border_radius_label.setText(_('global_panel_interface.border_radius'))
    self.global_panel_interface_videoplayer_backgroundbox_color_label.setText(_('units.color'))
    self.global_panel_interface_videoplayer_safe_margin_action_group.setTitle(_('global_panel_interface.action_safe_margin'))
    self.global_panel_interface_videoplayer_safe_margin_action_x_margin_label.setText(_('global_panel_interface.horizontal_margin'))
    self.global_panel_interface_videoplayer_safe_margin_action_y_margin_label.setText(_('global_panel_interface.vertical_margin'))
    self.global_panel_interface_videoplayer_safe_margin_action_y_margin_pixels_label.setText(_('units.pixels'))
    self.global_panel_interface_videoplayer_safe_margin_action_color_label.setText(_('units.color'))
    self.global_panel_interface_videoplayer_safe_margin_title_group.setTitle(_('global_panel_interface.title_safe_margin'))
    self.global_panel_interface_videoplayer_safe_margin_title_x_margin_label.setText(_('global_panel_interface.horizontal_margin'))
    self.global_panel_interface_videoplayer_safe_margin_title_y_margin_label.setText(_('global_panel_interface.vertical_margin'))
    self.global_panel_interface_videoplayer_safe_margin_title_y_margin_pixels_label.setText(_('units.pixels'))
    self.global_panel_interface_videoplayer_safe_margin_title_color_label.setText(_('units.color'))
    self.global_panel_interface_tabwidget.setTabText(0, _('global_panel_interface.video_player'))
    self.global_panel_interface_videoplayer_shadow_x_position_pixels_label.setText(_('units.pixels'))
    self.global_panel_interface_videoplayer_safe_margin_title_x_margin_pixels_label.setText(_('units.pixels'))