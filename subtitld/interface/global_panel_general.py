from PySide6.QtWidgets import QLabel, QComboBox, QPushButton, QWidget, QVBoxLayout, QCheckBox, QDoubleSpinBox, QHBoxLayout
from PySide6.QtCore import Qt

from subtitld.modules.paths import LIST_OF_SUPPORTED_SUBTITLE_EXTENSIONS
from subtitld.interface import global_panel
from subtitld.interface.translation import _



def load_menu(self):
    """Function to load subtitles panel widgets"""
    self.global_panel_general_menu_button = QPushButton()
    self.global_panel_general_menu_button.setCheckable(True)
    self.global_panel_general_menu_button.setProperty('class', 'global_panel_menu')
    self.global_panel_general_menu_button.clicked.connect(lambda: global_panel_menu_changed(self))
    self.global_panel_menu.layout().addWidget(self.global_panel_general_menu_button)


def global_panel_menu_changed(self):
    self.global_panel_general_menu_button.setEnabled(False)
    global_panel.global_panel_menu_changed(self, self.global_panel_general_menu_button, self.global_panel_general_content)


def load_widgets(self):
    """Function to load subtitles panel widgets"""

    self.global_panel_general_content = QWidget()
    self.global_panel_general_content.setLayout(QVBoxLayout())
    self.global_panel_general_content.layout().setContentsMargins(0, 0, 0, 0)
    self.global_panel_general_content.layout().setSpacing(20)

    self.global_panel_general_save_as_line = QVBoxLayout()
    self.global_panel_general_save_as_line.setContentsMargins(0, 0, 0, 0)
    self.global_panel_general_save_as_line.setSpacing(5)

    self.global_subtitlesvideo_save_as_label = QLabel(parent=self.global_panel_general_content)
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

    self.global_panel_general_save_copy = QCheckBox()
    self.global_panel_general_save_copy.stateChanged.connect(lambda: global_panel_general_save_copy_changed(self))
    self.global_panel_general_save_as_line.addWidget(self.global_panel_general_save_copy, 0, Qt.AlignLeft)

    self.global_panel_general_content.layout().addLayout(self.global_panel_general_save_as_line)

    self.global_panel_general_minimum_duration_line = QVBoxLayout()
    self.global_panel_general_minimum_duration_line.setContentsMargins(0, 0, 0, 0)
    self.global_panel_general_minimum_duration_line.setSpacing(2)

    self.global_panel_general_minimum_duration_label = QLabel()
    self.global_panel_general_minimum_duration_label.setProperty('class', 'widget_label')
    self.global_panel_general_minimum_duration_line.addWidget(self.global_panel_general_minimum_duration_label, 0, Qt.AlignLeft)

    self.global_panel_general_minimum_duration_line_2 = QHBoxLayout()
    self.global_panel_general_minimum_duration_line_2.setContentsMargins(0, 0, 0, 0)
    self.global_panel_general_minimum_duration_line_2.setSpacing(5)

    self.global_panel_general_minimum_duration_spinbox = QDoubleSpinBox()
    self.global_panel_general_minimum_duration_spinbox.setMinimum(.1)
    self.global_panel_general_minimum_duration_spinbox.setMaximum(999.999)
    self.global_panel_general_minimum_duration_spinbox.valueChanged.connect(lambda: global_panel_general_minimum_duration_spinbox_changed(self))
    self.global_panel_general_minimum_duration_line_2.addWidget(self.global_panel_general_minimum_duration_spinbox, 0, Qt.AlignLeft)

    self.global_panel_general_minimum_duration_seconds_label = QLabel()
    self.global_panel_general_minimum_duration_seconds_label.setProperty('class', 'units_label')
    self.global_panel_general_minimum_duration_line_2.addWidget(self.global_panel_general_minimum_duration_seconds_label, 0, Qt.AlignLeft)

    self.global_panel_general_minimum_duration_line_2.addStretch()

    self.global_panel_general_minimum_duration_line.addLayout(self.global_panel_general_minimum_duration_line_2)

    self.global_panel_general_content.layout().addLayout(self.global_panel_general_minimum_duration_line)

    self.global_panel_general_content.layout().addStretch()

    self.global_panel_content_stacked_widgets.addWidget(self.global_panel_general_content)

    update_widgets(self)


def global_subtitlesvideo_save_as_combobox_activated(self):
    """Function to change format as combobox selection"""
    self.settings['default_values']['subtitle_format'] = self.global_subtitlesvideo_save_as_combobox.currentText().split(' ', 1)[0]


def global_panel_general_save_copy_changed(self):
    self.settings['default_values']['save_automatic_copy'] = self.global_panel_general_save_copy.isChecked()


def global_panel_general_minimum_duration_spinbox_changed(self):
    self.settings['default_values']['minimum_subtitle_width'] = self.global_panel_general_minimum_duration_spinbox.value()


def update_widgets(self):
    for item in [self.global_subtitlesvideo_save_as_combobox.itemText(i) for i in range(self.global_subtitlesvideo_save_as_combobox.count())]:
        if item.startswith(self.settings['default_values'].get('subtitle_format', 'USF')):
            self.global_subtitlesvideo_save_as_combobox.setCurrentText(item)
            break

    self.global_panel_general_save_copy.setChecked(self.settings['default_values'].get('save_automatic_copy', False))

    self.global_panel_general_minimum_duration_spinbox.setValue(self.settings['default_values'].get('minimum_subtitle_width', 1.0))


def translate_widgets(self):
    self.global_panel_general_menu_button.setText(_('global_panel_general.title'))
    self.global_subtitlesvideo_save_as_label.setText(_('global_panel_general.default_format_save'))
    self.global_panel_general_save_copy.setText(_('global_panel_general.save_copy'))
    self.global_panel_general_minimum_duration_label.setText(_('global_panel_general.minimum_duration'))
    self.global_panel_general_minimum_duration_seconds_label.setText(_('units.seconds'))
