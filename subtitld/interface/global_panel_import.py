import os

from PySide6.QtWidgets import QPushButton, QFileDialog, QWidget

from subtitld.modules.paths import LIST_OF_SUPPORTED_IMPORT_EXTENSIONS
from subtitld.interface import global_panel
from subtitld.interface.translation import _
from subtitld.modules import file_io


list_of_supported_import_extensions = []
for exttype in LIST_OF_SUPPORTED_IMPORT_EXTENSIONS:
    for ext in LIST_OF_SUPPORTED_IMPORT_EXTENSIONS[exttype]['extensions']:
        list_of_supported_import_extensions.append(ext)


def load_menu(self):
    """Function to load subtitles panel widgets"""
    self.global_panel_import_menu_button = QPushButton()
    self.global_panel_import_menu_button.setCheckable(True)
    self.global_panel_import_menu_button.setProperty('class', 'global_panel_menu')
    self.global_panel_import_menu_button.clicked.connect(lambda: global_panel_menu_changed(self))
    self.global_panel_menu.layout().addWidget(self.global_panel_import_menu_button)


def global_panel_menu_changed(self):
    self.global_panel_import_menu_button.setEnabled(False)
    global_panel.global_panel_menu_changed(self, self.global_panel_import_menu_button, self.global_panel_import_content)


def load_widgets(self):
    """Function to load subtitles panel widgets"""

    self.global_panel_import_content = QWidget()

    self.global_subtitlesvideo_import_button = QPushButton(parent=self.global_panel_import_content)
    self.global_subtitlesvideo_import_button.setProperty('class', 'button')
    # self.global_subtitlesvideo_import_button.setCheckable(True)
    self.global_subtitlesvideo_import_button.clicked.connect(lambda: global_subtitlesvideo_import_button_clicked(self))

    # self.global_subtitlesvideo_import_panel = QLabel(parent=self.global_panel_import_content)
    # self.global_subtitlesvideo_import_panel.setVisible(False)

    # self.global_subtitlesvideo_import_panel_radiobox = QRadioBox(parent=self.global_subtitlesvideo_import_panel)
    self.global_panel_content_stacked_widgets.addWidget(self.global_panel_import_content)


def global_subtitlesvideo_import_button_clicked(self):
    """Function to import file"""
    # if self.global_subtitlesvideo_import_button.isChecked():
    #     self.global_subtitlesvideo_export_button.setGeometry(20, 200, self.global_panel_menu.width() - 40, 30)
    # else:
    #     self.global_subtitlesvideo_export_button.setGeometry(20, 120, self.global_panel_menu.width() - 40, 30)
    # self.global_subtitlesvideo_import_panel.setVisible(self.global_subtitlesvideo_import_button.isChecked())

    supported_import_files = 'Text files' + ' ({})'.format(" ".join([" * .{}".format(fo) for fo in list_of_supported_import_extensions]))
    file_to_open = QFileDialog.getOpenFileName(parent=self, caption='Select the file to import', dir=os.path.expanduser("~"), filter=supported_import_files)[0]
    if file_to_open:
        self.subtitles_list += file_io.import_file(filename=file_to_open)[0]
        self.subtitles_list.sort()
        # update_widgets(self)


def translate_widgets(self):
    self.global_panel_import_menu_button.setText(_('global_panel_import.title'))
    self.global_subtitlesvideo_import_button.setText(_('global_panel_import.import'))
