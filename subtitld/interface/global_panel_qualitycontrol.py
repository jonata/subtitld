"""Subtitles Video panel

"""

from PyQt5.QtWidgets import QDoubleSpinBox, QLabel, QPushButton, QSpinBox, QWidget, QVBoxLayout, QCheckBox, QGridLayout, QSlider
from PyQt5.QtCore import Qt

from subtitld.interface import global_panel


def load_menu(self):
    """Function to load subtitles panel widgets"""
    self.global_panel_qualitycontrol_menu_button = QPushButton('Quality control')
    self.global_panel_qualitycontrol_menu_button.setCheckable(True)
    self.global_panel_qualitycontrol_menu_button.setProperty('class', 'global_panel_menu')
    self.global_panel_qualitycontrol_menu_button.clicked.connect(lambda: global_panel_menu_changed(self))
    self.global_panel_menu.layout().addWidget(self.global_panel_qualitycontrol_menu_button)


def global_panel_menu_changed(self):
    global_panel.global_panel_menu_changed(self, self.global_panel_qualitycontrol_menu_button, self.global_panel_qualitycontrol_content)


def load_widgets(self):
    """Function to load subtitles panel widgets"""

    self.global_panel_qualitycontrol_content = QWidget()
    self.global_panel_qualitycontrol_content.setLayout(QVBoxLayout())

    self.global_panel_tabwidget_show_statistics_checkbox = QCheckBox('Enable quality statistics')
    self.global_panel_tabwidget_show_statistics_checkbox.setChecked(False)
    self.global_panel_tabwidget_show_statistics_checkbox.stateChanged.connect(lambda: update_quality_settings(self))
    self.global_panel_qualitycontrol_content.layout().addWidget(self.global_panel_tabwidget_show_statistics_checkbox)

    self.global_panel_tabwidget_quality_enable_checkbox = QCheckBox('Enable quality check')
    self.global_panel_tabwidget_quality_enable_checkbox.setChecked(False)
    self.global_panel_tabwidget_quality_enable_checkbox.stateChanged.connect(lambda: update_quality_settings(self))
    self.global_panel_qualitycontrol_content.layout().addWidget(self.global_panel_tabwidget_quality_enable_checkbox)

    self.global_panel_tabwidget_quality_forms_grid = QGridLayout()

    self.global_panel_tabwidget_quality_readingspeed_vbox = QVBoxLayout()
    self.global_panel_tabwidget_quality_readingspeed_label = QLabel(self.tr('Reading Speed (characters per second)').upper(), parent=self.global_panel_qualitycontrol_content)
    self.global_panel_tabwidget_quality_readingspeed_vbox.addWidget(self.global_panel_tabwidget_quality_readingspeed_label)
    self.global_panel_tabwidget_quality_readingspeed = QSpinBox(parent=self.global_panel_qualitycontrol_content)
    self.global_panel_tabwidget_quality_readingspeed.setMinimum(0)
    self.global_panel_tabwidget_quality_readingspeed.setMaximum(999)
    self.global_panel_tabwidget_quality_readingspeed.setValue(21)
    self.global_panel_tabwidget_quality_readingspeed.valueChanged.connect(lambda: update_quality_settings(self))
    self.global_panel_tabwidget_quality_readingspeed_vbox.addWidget(self.global_panel_tabwidget_quality_readingspeed)
    self.global_panel_tabwidget_quality_forms_grid.addLayout(self.global_panel_tabwidget_quality_readingspeed_vbox, 0, 0)

    self.global_panel_tabwidget_quality_minimumduration_vbox = QVBoxLayout()
    self.global_panel_tabwidget_quality_minimumduration_label = QLabel(self.tr('Minimum subtitle duration (in seconds)').upper(), parent=self.global_panel_qualitycontrol_content)
    self.global_panel_tabwidget_quality_minimumduration_vbox.addWidget(self.global_panel_tabwidget_quality_minimumduration_label)
    self.global_panel_tabwidget_quality_minimumduration = QDoubleSpinBox(parent=self.global_panel_qualitycontrol_content)
    self.global_panel_tabwidget_quality_minimumduration.setMinimum(0.1)
    self.global_panel_tabwidget_quality_minimumduration.setMaximum(999.999)
    self.global_panel_tabwidget_quality_minimumduration.setValue(.7)
    self.global_panel_tabwidget_quality_minimumduration.valueChanged.connect(lambda: update_quality_settings(self))
    self.global_panel_tabwidget_quality_minimumduration_vbox.addWidget(self.global_panel_tabwidget_quality_minimumduration)
    self.global_panel_tabwidget_quality_forms_grid.addLayout(self.global_panel_tabwidget_quality_minimumduration_vbox, 0, 1)

    self.global_panel_tabwidget_quality_maximumduration_vbox = QVBoxLayout()
    self.global_panel_tabwidget_quality_maximumduration_label = QLabel(self.tr('Maximum subtitle duration (in seconds)').upper(), parent=self.global_panel_qualitycontrol_content)
    self.global_panel_tabwidget_quality_maximumduration_vbox.addWidget(self.global_panel_tabwidget_quality_maximumduration_label)
    self.global_panel_tabwidget_quality_maximumduration = QDoubleSpinBox(parent=self.global_panel_qualitycontrol_content)
    self.global_panel_tabwidget_quality_maximumduration.setMinimum(0.2)
    self.global_panel_tabwidget_quality_maximumduration.setMaximum(999.999)
    self.global_panel_tabwidget_quality_maximumduration.setValue(7)
    self.global_panel_tabwidget_quality_maximumduration.valueChanged.connect(lambda: update_quality_settings(self))
    self.global_panel_tabwidget_quality_maximumduration_vbox.addWidget(self.global_panel_tabwidget_quality_maximumduration)
    self.global_panel_tabwidget_quality_forms_grid.addLayout(self.global_panel_tabwidget_quality_maximumduration_vbox, 0, 2)

    self.global_panel_tabwidget_quality_maximumlines_vbox = QVBoxLayout()
    self.global_panel_tabwidget_quality_maximumlines_label = QLabel(self.tr('Maximum number of lines').upper(), parent=self.global_panel_qualitycontrol_content)
    self.global_panel_tabwidget_quality_maximumlines_vbox.addWidget(self.global_panel_tabwidget_quality_maximumlines_label)
    self.global_panel_tabwidget_quality_maximumlines = QSpinBox(parent=self.global_panel_qualitycontrol_content)
    self.global_panel_tabwidget_quality_maximumlines.setMinimum(1)
    self.global_panel_tabwidget_quality_maximumlines.setMaximum(10)
    self.global_panel_tabwidget_quality_maximumlines.setValue(2)
    self.global_panel_tabwidget_quality_maximumlines.valueChanged.connect(lambda: update_quality_settings(self))
    self.global_panel_tabwidget_quality_maximumlines_vbox.addWidget(self.global_panel_tabwidget_quality_maximumlines)
    self.global_panel_tabwidget_quality_forms_grid.addLayout(self.global_panel_tabwidget_quality_maximumlines_vbox, 1, 0)

    self.global_panel_tabwidget_quality_maximumcharactersperline_vbox = QVBoxLayout()
    self.global_panel_tabwidget_quality_maximumcharactersperline_label = QLabel(self.tr('Maximum number characters per line').upper(), parent=self.global_panel_qualitycontrol_content)
    self.global_panel_tabwidget_quality_maximumcharactersperline_vbox.addWidget(self.global_panel_tabwidget_quality_maximumcharactersperline_label)
    self.global_panel_tabwidget_quality_maximumcharactersperline = QSpinBox(parent=self.global_panel_qualitycontrol_content)
    self.global_panel_tabwidget_quality_maximumcharactersperline.setMinimum(1)
    self.global_panel_tabwidget_quality_maximumcharactersperline.setMaximum(999)
    self.global_panel_tabwidget_quality_maximumcharactersperline.setValue(42)
    self.global_panel_tabwidget_quality_maximumcharactersperline.valueChanged.connect(lambda: update_quality_settings(self))
    self.global_panel_tabwidget_quality_maximumcharactersperline_vbox.addWidget(self.global_panel_tabwidget_quality_maximumcharactersperline)
    self.global_panel_tabwidget_quality_forms_grid.addLayout(self.global_panel_tabwidget_quality_maximumcharactersperline_vbox, 1, 1)

    self.global_panel_qualitycontrol_content.layout().addLayout(self.global_panel_tabwidget_quality_forms_grid)

    self.global_panel_tabwidget_quality_prefercompact_checkbox = QCheckBox('Prefer compact subtitles')
    self.global_panel_tabwidget_quality_prefercompact_checkbox.setChecked(False)
    self.global_panel_tabwidget_quality_prefercompact_checkbox.stateChanged.connect(lambda: update_quality_settings(self))
    self.global_panel_qualitycontrol_content.layout().addWidget(self.global_panel_tabwidget_quality_prefercompact_checkbox)

    self.global_panel_tabwidget_quality_balanceratio_vbox = QVBoxLayout()
    self.global_panel_tabwidget_quality_balanceratio_checkbox = QCheckBox('Balance line length ratio (percentage the shortest should be of the largest)')
    self.global_panel_tabwidget_quality_balanceratio_checkbox.setChecked(False)
    self.global_panel_tabwidget_quality_balanceratio_checkbox.stateChanged.connect(lambda: update_quality_settings(self))
    self.global_panel_tabwidget_quality_balanceratio_vbox.addWidget(self.global_panel_tabwidget_quality_balanceratio_checkbox)
    self.global_panel_tabwidget_quality_balanceratio_slider = QSlider(orientation=Qt.Horizontal)
    self.global_panel_tabwidget_quality_balanceratio_slider.setMinimum(0)
    self.global_panel_tabwidget_quality_balanceratio_slider.setMaximum(100)
    self.global_panel_tabwidget_quality_balanceratio_slider.setValue(50)
    self.global_panel_tabwidget_quality_balanceratio_slider.valueChanged.connect(lambda: update_quality_settings(self))
    self.global_panel_tabwidget_quality_balanceratio_vbox.addWidget(self.global_panel_tabwidget_quality_balanceratio_slider)
    self.global_panel_qualitycontrol_content.layout().addLayout(self.global_panel_tabwidget_quality_balanceratio_vbox)

    self.global_panel_qualitycontrol_content.layout().addStretch()
    self.global_panel_qualitycontrol_content.setLayout(self.global_panel_qualitycontrol_content.layout())

    self.global_panel_content_stacked_widgets.addWidget(self.global_panel_qualitycontrol_content)

    update_global_panel_qualitycontrol_content_widgets(self)


def update_global_panel_qualitycontrol_content_widgets(self):
    self.global_panel_tabwidget_quality_enable_checkbox.setChecked(self.settings['quality_check'].get('enabled', False))
    self.global_panel_tabwidget_quality_readingspeed.setValue(self.settings['quality_check'].get('reading_speed', 21))
    self.global_panel_tabwidget_quality_minimumduration.setValue(self.settings['quality_check'].get('minimum_duration', .7))
    self.global_panel_tabwidget_quality_maximumduration.setValue(self.settings['quality_check'].get('maximum_duration', 7))
    self.global_panel_tabwidget_quality_maximumlines.setValue(self.settings['quality_check'].get('maximum_lines', 2))
    self.global_panel_tabwidget_quality_maximumcharactersperline.setValue(self.settings['quality_check'].get('maximum_characters_per_line', 42))
    self.global_panel_tabwidget_quality_prefercompact_checkbox.setChecked(self.settings['quality_check'].get('prefer_compact', False))
    self.global_panel_tabwidget_quality_balanceratio_checkbox.setText('Balance line length ratio ({p}% the shortest should be of the largest)'.format(p=self.settings['quality_check'].get('balance_ratio', 50)))
    self.global_panel_tabwidget_quality_balanceratio_checkbox.setChecked(self.settings['quality_check'].get('balance_ratio_enabled', False))
    self.global_panel_tabwidget_quality_balanceratio_slider.setValue(self.settings['quality_check'].get('balance_ratio', 50))


def update_quality_settings(self):
    self.settings['quality_check']['show_statistics'] = self.global_panel_tabwidget_show_statistics_checkbox.isChecked()
    self.settings['quality_check']['enabled'] = self.global_panel_tabwidget_quality_enable_checkbox.isChecked()
    self.settings['quality_check']['reading_speed'] = self.global_panel_tabwidget_quality_readingspeed.value()
    self.settings['quality_check']['minimum_duration'] = self.global_panel_tabwidget_quality_minimumduration.value()
    self.settings['quality_check']['maximum_duration'] = self.global_panel_tabwidget_quality_maximumduration.value()
    self.settings['quality_check']['maximum_lines'] = self.global_panel_tabwidget_quality_maximumlines.value()
    self.settings['quality_check']['maximum_characters_per_line'] = self.global_panel_tabwidget_quality_maximumcharactersperline.value()
    self.settings['quality_check']['prefer_compact'] = self.global_panel_tabwidget_quality_prefercompact_checkbox.isChecked()
    self.settings['quality_check']['balance_ratio_enabled'] = self.global_panel_tabwidget_quality_balanceratio_checkbox.isChecked()
    self.settings['quality_check']['balance_ratio'] = self.global_panel_tabwidget_quality_balanceratio_slider.value()
    update_global_panel_qualitycontrol_content_widgets(self)
