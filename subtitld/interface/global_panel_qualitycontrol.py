from PySide6.QtWidgets import QDoubleSpinBox, QLabel, QPushButton, QSpinBox, QWidget, QVBoxLayout, QCheckBox, QSlider, QGroupBox, QHBoxLayout
from PySide6.QtCore import Qt

from subtitld.interface import global_panel
from subtitld.interface.translation import _


def load_menu(self):
    """Function to load subtitles panel widgets"""
    self.global_panel_qualitycontrol_menu_button = QPushButton()
    self.global_panel_qualitycontrol_menu_button.setCheckable(True)
    self.global_panel_qualitycontrol_menu_button.setProperty('class', 'global_panel_menu')
    self.global_panel_qualitycontrol_menu_button.clicked.connect(lambda: global_panel_menu_changed(self))
    self.global_panel_menu.layout().addWidget(self.global_panel_qualitycontrol_menu_button)


def global_panel_menu_changed(self):
    self.global_panel_qualitycontrol_menu_button.setEnabled(False)
    global_panel.global_panel_menu_changed(self, self.global_panel_qualitycontrol_menu_button, self.global_panel_qualitycontrol_content)


def load_widgets(self):
    """Function to load subtitles panel widgets"""

    self.global_panel_qualitycontrol_content = QWidget()
    self.global_panel_qualitycontrol_content.setLayout(QVBoxLayout())

    self.global_panel_tabwidget_show_statistics_checkbox = QCheckBox()
    self.global_panel_tabwidget_show_statistics_checkbox.setChecked(False)
    self.global_panel_tabwidget_show_statistics_checkbox.stateChanged.connect(lambda: update_quality_settings(self))
    self.global_panel_qualitycontrol_content.layout().addWidget(self.global_panel_tabwidget_show_statistics_checkbox)

    self.global_panel_tabwidget_quality_enable_groupbox = QGroupBox()
    self.global_panel_tabwidget_quality_enable_groupbox.setCheckable(True)
    self.global_panel_tabwidget_quality_enable_groupbox.setLayout(QVBoxLayout())
    self.global_panel_tabwidget_quality_enable_groupbox.toggled.connect(lambda: update_quality_settings(self))
    self.global_panel_tabwidget_quality_enable_groupbox.layout().setContentsMargins(10, 10, 10, 10)
    self.global_panel_tabwidget_quality_enable_groupbox.layout().setSpacing(20)

    self.global_panel_tabwidget_quality_readingspeed_vbox = QVBoxLayout()
    self.global_panel_tabwidget_quality_readingspeed_vbox.setContentsMargins(0, 0, 0, 0)
    self.global_panel_tabwidget_quality_readingspeed_vbox.setSpacing(2)

    self.global_panel_tabwidget_quality_readingspeed_label = QLabel()
    self.global_panel_tabwidget_quality_readingspeed_label.setProperty('class', 'widget_label')
    self.global_panel_tabwidget_quality_readingspeed_vbox.addWidget(self.global_panel_tabwidget_quality_readingspeed_label, 0, Qt.AlignLeft)

    self.global_panel_tabwidget_quality_readingspeed_line = QHBoxLayout()
    self.global_panel_tabwidget_quality_readingspeed_line.setContentsMargins(0, 0, 0, 0)
    self.global_panel_tabwidget_quality_readingspeed_line.setSpacing(5)

    self.global_panel_tabwidget_quality_readingspeed_cps = QSpinBox()
    self.global_panel_tabwidget_quality_readingspeed_cps.setMinimum(0)
    self.global_panel_tabwidget_quality_readingspeed_cps.setMaximum(999)
    self.global_panel_tabwidget_quality_readingspeed_cps.setValue(21)
    self.global_panel_tabwidget_quality_readingspeed_cps.valueChanged.connect(lambda: update_quality_settings(self))
    self.global_panel_tabwidget_quality_readingspeed_line.addWidget(self.global_panel_tabwidget_quality_readingspeed_cps)

    self.global_panel_tabwidget_quality_readingspeed_cps_label = QLabel()
    self.global_panel_tabwidget_quality_readingspeed_cps_label.setProperty('class', 'units_label')
    self.global_panel_tabwidget_quality_readingspeed_line.addWidget(self.global_panel_tabwidget_quality_readingspeed_cps_label, 0, Qt.AlignLeft)

    self.global_panel_tabwidget_quality_readingspeed_wpm = QSpinBox()
    self.global_panel_tabwidget_quality_readingspeed_wpm.setMinimum(0)
    self.global_panel_tabwidget_quality_readingspeed_wpm.setMaximum(999)
    self.global_panel_tabwidget_quality_readingspeed_wpm.setValue(140)
    self.global_panel_tabwidget_quality_readingspeed_wpm.valueChanged.connect(lambda: update_quality_settings(self))
    self.global_panel_tabwidget_quality_readingspeed_line.addWidget(self.global_panel_tabwidget_quality_readingspeed_wpm)

    self.global_panel_tabwidget_quality_readingspeed_wpm_label = QLabel()
    self.global_panel_tabwidget_quality_readingspeed_wpm_label.setProperty('class', 'units_label')
    self.global_panel_tabwidget_quality_readingspeed_line.addWidget(self.global_panel_tabwidget_quality_readingspeed_wpm_label, 0, Qt.AlignLeft)

    self.global_panel_tabwidget_quality_readingspeed_line.addStretch()

    self.global_panel_tabwidget_quality_readingspeed_vbox.addLayout(self.global_panel_tabwidget_quality_readingspeed_line)

    self.global_panel_tabwidget_quality_enable_groupbox.layout().addLayout(self.global_panel_tabwidget_quality_readingspeed_vbox)

    self.global_panel_tabwidget_quality_duration_vbox = QVBoxLayout()
    self.global_panel_tabwidget_quality_duration_vbox.setContentsMargins(0, 0, 0, 0)
    self.global_panel_tabwidget_quality_duration_vbox.setSpacing(2)

    self.global_panel_tabwidget_quality_duration_label = QLabel()
    self.global_panel_tabwidget_quality_duration_label.setProperty('class', 'widget_label')
    self.global_panel_tabwidget_quality_duration_vbox.addWidget(self.global_panel_tabwidget_quality_duration_label, 0, Qt.AlignLeft)

    self.global_panel_tabwidget_quality_duration_line = QHBoxLayout()
    self.global_panel_tabwidget_quality_duration_line.setContentsMargins(0, 0, 0, 0)
    self.global_panel_tabwidget_quality_duration_line.setSpacing(5)

    self.global_panel_tabwidget_quality_duration_minimum = QDoubleSpinBox()
    self.global_panel_tabwidget_quality_duration_minimum.setMinimum(0.1)
    self.global_panel_tabwidget_quality_duration_minimum.setMaximum(999.999)
    self.global_panel_tabwidget_quality_duration_minimum.setValue(.7)
    self.global_panel_tabwidget_quality_duration_minimum.valueChanged.connect(lambda: update_quality_settings(self))
    self.global_panel_tabwidget_quality_duration_line.addWidget(self.global_panel_tabwidget_quality_duration_minimum)

    self.global_panel_tabwidget_quality_duration_minimum_label = QLabel()
    self.global_panel_tabwidget_quality_duration_minimum_label.setProperty('class', 'units_label')
    self.global_panel_tabwidget_quality_duration_line.addWidget(self.global_panel_tabwidget_quality_duration_minimum_label)

    self.global_panel_tabwidget_quality_duration_maximum = QDoubleSpinBox()
    self.global_panel_tabwidget_quality_duration_maximum.setMinimum(0.2)
    self.global_panel_tabwidget_quality_duration_maximum.setMaximum(999.999)
    self.global_panel_tabwidget_quality_duration_maximum.setValue(7)
    self.global_panel_tabwidget_quality_duration_maximum.valueChanged.connect(lambda: update_quality_settings(self))
    self.global_panel_tabwidget_quality_duration_line.addWidget(self.global_panel_tabwidget_quality_duration_maximum)

    self.global_panel_tabwidget_quality_duration_maximum_label = QLabel()
    self.global_panel_tabwidget_quality_duration_maximum_label.setProperty('class', 'units_label')
    self.global_panel_tabwidget_quality_duration_line.addWidget(self.global_panel_tabwidget_quality_duration_maximum_label)

    self.global_panel_tabwidget_quality_duration_line.addStretch()

    self.global_panel_tabwidget_quality_duration_vbox.addLayout(self.global_panel_tabwidget_quality_duration_line)

    self.global_panel_tabwidget_quality_enable_groupbox.layout().addLayout(self.global_panel_tabwidget_quality_duration_vbox)

    self.global_panel_tabwidget_quality_lines_vbox = QVBoxLayout()
    self.global_panel_tabwidget_quality_lines_vbox.setContentsMargins(0, 0, 0, 0)
    self.global_panel_tabwidget_quality_lines_vbox.setSpacing(2)

    self.global_panel_tabwidget_quality_lines_label = QLabel()
    self.global_panel_tabwidget_quality_lines_label.setProperty('class', 'widget_label')
    self.global_panel_tabwidget_quality_lines_vbox.addWidget(self.global_panel_tabwidget_quality_lines_label, 0, Qt.AlignLeft)

    self.global_panel_tabwidget_quality_lines_line = QHBoxLayout()
    self.global_panel_tabwidget_quality_lines_line.setContentsMargins(0, 0, 0, 0)
    self.global_panel_tabwidget_quality_lines_line.setSpacing(5)

    self.global_panel_tabwidget_quality_lines_maximum = QSpinBox()
    self.global_panel_tabwidget_quality_lines_maximum.setMinimum(1)
    self.global_panel_tabwidget_quality_lines_maximum.setMaximum(10)
    self.global_panel_tabwidget_quality_lines_maximum.setValue(2)
    self.global_panel_tabwidget_quality_lines_maximum.valueChanged.connect(lambda: update_quality_settings(self))
    self.global_panel_tabwidget_quality_lines_line.addWidget(self.global_panel_tabwidget_quality_lines_maximum)

    self.global_panel_tabwidget_quality_lines_maximum_label = QLabel()
    self.global_panel_tabwidget_quality_lines_maximum_label.setProperty('class', 'units_label')
    self.global_panel_tabwidget_quality_lines_line.addWidget(self.global_panel_tabwidget_quality_lines_maximum_label)

    self.global_panel_tabwidget_quality_lines_maximumcharacters = QSpinBox()
    self.global_panel_tabwidget_quality_lines_maximumcharacters.setMinimum(1)
    self.global_panel_tabwidget_quality_lines_maximumcharacters.setMaximum(999)
    self.global_panel_tabwidget_quality_lines_maximumcharacters.setValue(42)
    self.global_panel_tabwidget_quality_lines_maximumcharacters.valueChanged.connect(lambda: update_quality_settings(self))
    self.global_panel_tabwidget_quality_lines_line.addWidget(self.global_panel_tabwidget_quality_lines_maximumcharacters)

    self.global_panel_tabwidget_quality_lines_maximumcharacters_label = QLabel()
    self.global_panel_tabwidget_quality_lines_maximumcharacters_label.setProperty('class', 'units_label')
    self.global_panel_tabwidget_quality_lines_line.addWidget(self.global_panel_tabwidget_quality_lines_maximumcharacters_label)

    self.global_panel_tabwidget_quality_lines_line.addStretch()

    self.global_panel_tabwidget_quality_lines_vbox.addLayout(self.global_panel_tabwidget_quality_lines_line)

    self.global_panel_tabwidget_quality_lines_vbox.addSpacing(5)

    self.global_panel_tabwidget_quality_prefer_compact_checkbox = QCheckBox()
    self.global_panel_tabwidget_quality_prefer_compact_checkbox.stateChanged.connect(lambda: update_quality_settings(self))
    self.global_panel_tabwidget_quality_lines_vbox.addWidget(self.global_panel_tabwidget_quality_prefer_compact_checkbox)

    self.global_panel_tabwidget_quality_lines_vbox.addSpacing(5)

    self.global_panel_tabwidget_quality_balanceratio_checkbox = QCheckBox()
    self.global_panel_tabwidget_quality_balanceratio_checkbox.stateChanged.connect(lambda: update_quality_settings(self))
    self.global_panel_tabwidget_quality_lines_vbox.addWidget(self.global_panel_tabwidget_quality_balanceratio_checkbox)

    self.global_panel_tabwidget_quality_lines_vbox.addSpacing(5)

    self.global_panel_tabwidget_quality_balanceratio_hbox = QHBoxLayout()
    self.global_panel_tabwidget_quality_balanceratio_hbox.setContentsMargins(0, 0, 0, 0)
    self.global_panel_tabwidget_quality_balanceratio_hbox.setSpacing(5)

    self.global_panel_tabwidget_quality_balanceratio_slider = QSlider(orientation=Qt.Horizontal)
    self.global_panel_tabwidget_quality_balanceratio_slider.setObjectName('global_panel_tabwidget_quality_balanceratio_slider')
    self.global_panel_tabwidget_quality_balanceratio_slider.setMinimum(0)
    self.global_panel_tabwidget_quality_balanceratio_slider.setMaximum(100)
    self.global_panel_tabwidget_quality_balanceratio_slider.setValue(50)
    self.global_panel_tabwidget_quality_balanceratio_slider.setMaximumWidth(200)
    self.global_panel_tabwidget_quality_balanceratio_slider.valueChanged.connect(lambda: update_quality_settings(self))
    self.global_panel_tabwidget_quality_balanceratio_hbox.addWidget(self.global_panel_tabwidget_quality_balanceratio_slider)

    self.global_panel_tabwidget_quality_balanceratio_slider_label = QLabel()
    self.global_panel_tabwidget_quality_balanceratio_slider_label.setProperty('class', 'units_label')
    self.global_panel_tabwidget_quality_balanceratio_hbox.addWidget(self.global_panel_tabwidget_quality_balanceratio_slider_label)

    self.global_panel_tabwidget_quality_balanceratio_hbox.addStretch()

    self.global_panel_tabwidget_quality_lines_vbox.addLayout(self.global_panel_tabwidget_quality_balanceratio_hbox)

    self.global_panel_tabwidget_quality_enable_groupbox.layout().addLayout(self.global_panel_tabwidget_quality_lines_vbox)

    self.global_panel_qualitycontrol_content.layout().addWidget(self.global_panel_tabwidget_quality_enable_groupbox)

    self.global_panel_qualitycontrol_content.layout().addStretch()

    self.global_panel_content_stacked_widgets.addWidget(self.global_panel_qualitycontrol_content)

    update_global_panel_qualitycontrol_content_widgets(self)


def update_global_panel_qualitycontrol_content_widgets(self):
    self.global_panel_tabwidget_show_statistics_checkbox.setChecked(self.settings['quality_check'].get('show_statistics', False))
    self.global_panel_tabwidget_quality_enable_groupbox.setChecked(self.settings['quality_check'].get('enabled', False))
    self.global_panel_tabwidget_quality_readingspeed_cps.setValue(self.settings['quality_check'].get('reading_speed_cps', 21))
    self.global_panel_tabwidget_quality_readingspeed_wpm.setValue(self.settings['quality_check'].get('reading_speed_wpm', 140))
    self.global_panel_tabwidget_quality_duration_minimum.setValue(self.settings['quality_check'].get('minimum_duration', .7))
    self.global_panel_tabwidget_quality_duration_maximum.setValue(self.settings['quality_check'].get('maximum_duration', 7))
    self.global_panel_tabwidget_quality_lines_maximum.setValue(self.settings['quality_check'].get('maximum_lines', 2))
    self.global_panel_tabwidget_quality_lines_maximumcharacters.setValue(self.settings['quality_check'].get('maximum_characters_per_line', 42))
    self.global_panel_tabwidget_quality_prefer_compact_checkbox.setChecked(self.settings['quality_check'].get('prefer_compact', False))
    self.global_panel_tabwidget_quality_balanceratio_checkbox.setChecked(self.settings['quality_check'].get('balance_ratio_enabled', False))
    self.global_panel_tabwidget_quality_balanceratio_slider.setValue(self.settings['quality_check'].get('balance_ratio', 50))
    self.global_panel_tabwidget_quality_balanceratio_slider_label.setText('Ratio ({p}% the shortest should be of the largest)'.format(p=self.settings['quality_check'].get('balance_ratio', 50)))


def update_quality_settings(self):
    self.settings['quality_check']['show_statistics'] = self.global_panel_tabwidget_show_statistics_checkbox.isChecked()
    self.settings['quality_check']['enabled'] = self.global_panel_tabwidget_quality_enable_groupbox.isChecked()
    self.settings['quality_check']['reading_speed_cps'] = self.global_panel_tabwidget_quality_readingspeed_cps.value()
    self.settings['quality_check']['reading_speed_wpm'] = self.global_panel_tabwidget_quality_readingspeed_wpm.value()
    self.settings['quality_check']['minimum_duration'] = self.global_panel_tabwidget_quality_duration_minimum.value()
    self.settings['quality_check']['maximum_duration'] = self.global_panel_tabwidget_quality_duration_maximum.value()
    self.settings['quality_check']['maximum_lines'] = self.global_panel_tabwidget_quality_lines_maximum.value()
    self.settings['quality_check']['maximum_characters_per_line'] = self.global_panel_tabwidget_quality_lines_maximumcharacters.value()
    self.settings['quality_check']['prefer_compact'] = self.global_panel_tabwidget_quality_prefer_compact_checkbox.isChecked()
    self.settings['quality_check']['balance_ratio_enabled'] = self.global_panel_tabwidget_quality_balanceratio_checkbox.isChecked()
    self.settings['quality_check']['balance_ratio'] = self.global_panel_tabwidget_quality_balanceratio_slider.value()
    update_global_panel_qualitycontrol_content_widgets(self)

def translate_widgets(self):
    self.global_panel_qualitycontrol_menu_button.setText(_('global_panel_qualitycontrol.title'))
    self.global_panel_tabwidget_show_statistics_checkbox.setText(_('global_panel_qualitycontrol.show_statistics'))
    self.global_panel_tabwidget_quality_enable_groupbox.setTitle(_('global_panel_qualitycontrol.quality_check'))
    self.global_panel_tabwidget_quality_readingspeed_label.setText(_('global_panel_qualitycontrol.reading_speed'))
    self.global_panel_tabwidget_quality_readingspeed_cps_label.setText(_('global_panel_qualitycontrol.characters_per_second'))
    self.global_panel_tabwidget_quality_readingspeed_wpm_label.setText(_('global_panel_qualitycontrol.words_per_minute'))
    self.global_panel_tabwidget_quality_duration_label.setText(_('global_panel_qualitycontrol.subtitle_duration'))
    self.global_panel_tabwidget_quality_duration_minimum_label.setText(_('global_panel_qualitycontrol.minimum_in_seconds'))
    self.global_panel_tabwidget_quality_duration_maximum_label.setText(_('global_panel_qualitycontrol.maximum_in_seconds'))
    self.global_panel_tabwidget_quality_lines_label.setText(_('units.lines'))
    self.global_panel_tabwidget_quality_lines_maximum_label.setText(_('units.maximum'))
    self.global_panel_tabwidget_quality_lines_maximumcharacters_label.setText(_('global_panel_qualitycontrol.maximum_characters_per_line'))
    self.global_panel_tabwidget_quality_prefer_compact_checkbox.setText(_('global_panel_qualitycontrol.prefer_compact_subtitles'))
    self.global_panel_tabwidget_quality_balanceratio_checkbox.setText(_('global_panel_qualitycontrol.balance_line_length'))
