from translate import Translator

from PySide6.QtWidgets import QComboBox, QPushButton, QWidget, QMessageBox, QGridLayout
from PySide6.QtCore import Qt, Signal, QThread

from subtitld.modules.paths import LANGUAGE_DICT_LIST
from subtitld.interface import global_panel, subtitles_panel, player
from subtitld.interface.translation import _

LANGUAGE_DESCRIPTIONS = LANGUAGE_DICT_LIST.keys()


class global_panel_translation_thread(QThread):
    """Thread to generate burned video"""
    response = Signal(dict)
    subtitles_list = []
    language_from = 'en'
    language_to = 'en'

    def run(self):
        if self.subtitles_list and self.language_from and self.language_to:
            translator = Translator(from_lang=self.language_from, to_lang=self.language_to)

            i = 0
            for _ in self.subtitles_list:
                self.response.emit({i : translator.translate(self.subtitles_list[i][2].replace('\n', ' ').replace('  ', ' '))})
                i += 1

            self.response.emit({'status' : 'end'})


def load_menu(self):
    """Function to load subtitles panel widgets"""
    self.global_panel_translation_menu_button = QPushButton()
    self.global_panel_translation_menu_button.setCheckable(True)
    self.global_panel_translation_menu_button.setProperty('class', 'global_panel_menu')
    self.global_panel_translation_menu_button.clicked.connect(lambda: global_panel_menu_changed(self))
    self.global_panel_menu.layout().addWidget(self.global_panel_translation_menu_button)


def global_panel_menu_changed(self):
    self.global_panel_translation_menu_button.setEnabled(False)
    global_panel.global_panel_menu_changed(self, self.global_panel_translation_menu_button, self.global_panel_translation_content)


def load_widgets(self):
    """Function to load subtitles panel widgets"""

    self.global_panel_translation_content = QWidget()
    self.global_panel_translation_content.setLayout(QGridLayout())

    self.global_subtitlesvideo_autosync_lang_from_combobox = QComboBox()
    self.global_subtitlesvideo_autosync_lang_from_combobox.setProperty('class', 'button')
    self.global_subtitlesvideo_autosync_lang_from_combobox.addItems(LANGUAGE_DESCRIPTIONS)
    self.global_panel_translation_content.layout().addWidget(self.global_subtitlesvideo_autosync_lang_from_combobox, 0, 0, Qt.AlignTop)

    self.global_subtitlesvideo_autosync_lang_to_combobox = QComboBox()
    self.global_subtitlesvideo_autosync_lang_to_combobox.setProperty('class', 'button')
    self.global_subtitlesvideo_autosync_lang_to_combobox.addItems(LANGUAGE_DESCRIPTIONS)
    self.global_panel_translation_content.layout().addWidget(self.global_subtitlesvideo_autosync_lang_to_combobox, 0, 1, Qt.AlignTop)

    self.global_subtitlesvideo_translate_button = QPushButton()
    self.global_subtitlesvideo_translate_button.setProperty('class', 'button')
    self.global_subtitlesvideo_translate_button.clicked.connect(lambda: global_subtitlesvideo_translate_button_clicked(self))
    self.global_panel_translation_content.layout().addWidget(self.global_subtitlesvideo_translate_button, 0, 2, Qt.AlignTop)

    def global_panel_translation_thread_ended(response):
        if 'status' in response and response['status'] == 'end':
            subtitles_panel.update_processing_status(self, show_widgets=False, value=0)
            self.global_subtitlesvideo_translate_button.setEnabled(True)
        else:
            for sub in response:
                subtitles_panel.update_processing_status(self, show_widgets=True, value=int((sub / len(self.subtitles_list)) * 100))
                self.subtitles_list[sub][2] = response[sub]

        player.update_timelines(self)

    self.global_panel_translation_thread = global_panel_translation_thread(self)
    self.global_panel_translation_thread.response.connect(global_panel_translation_thread_ended)

    self.global_panel_content_stacked_widgets.addWidget(self.global_panel_translation_content)


def global_subtitlesvideo_translate_button_clicked(self):
    """Function to translate subtitles"""
    run_command = False

    if bool(self.subtitles_list):
        are_you_sure_message = QMessageBox(self)
        are_you_sure_message.setWindowTitle(_('alert.are_you_sure'))
        are_you_sure_message.setText(_('alert.overwrite_warning'))
        are_you_sure_message.addButton('Yes', QMessageBox.AcceptRole)
        are_you_sure_message.addButton('No', QMessageBox.RejectRole)
        ret = are_you_sure_message.exec()

        if ret == 0:
            run_command = True
    else:
        run_command = True


    if run_command:
        self.global_panel_translation_thread.subtitles_list = self.subtitles_list
        self.global_panel_translation_thread.language_from = LANGUAGE_DICT_LIST[self.global_subtitlesvideo_autosync_lang_from_combobox.currentText()].split('-')[0]
        self.global_panel_translation_thread.language_to = LANGUAGE_DICT_LIST[self.global_subtitlesvideo_autosync_lang_to_combobox.currentText()].split('-')[0]
        self.global_panel_translation_thread.start()

        subtitles_panel.update_processing_status(self, show_widgets=True, value=33)
        self.global_subtitlesvideo_translate_button.setEnabled(False)


def translate_widgets(self):
    self.global_panel_translation_menu_button.setText(_('global_panel_translation.title'))
    self.global_subtitlesvideo_translate_button.setText(_('global_panel_translation.translate'))
