"""Subtitles Video panel

"""

from translate import Translator

from PySide6.QtWidgets import QComboBox, QPushButton, QWidget, QMessageBox, QGridLayout
from PySide6.QtCore import Qt

from subtitld.modules.paths import LANGUAGE_DICT_LIST
from subtitld.interface import global_panel

LANGUAGE_DESCRIPTIONS = LANGUAGE_DICT_LIST.keys()


def load_menu(self):
    """Function to load subtitles panel widgets"""
    self.global_panel_translation_menu_button = QPushButton('Translation')
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

    self.global_subtitlesvideo_translate_button = QPushButton(self.tr('Translate').upper())
    self.global_subtitlesvideo_translate_button.setProperty('class', 'button')
    self.global_subtitlesvideo_translate_button.clicked.connect(lambda: global_subtitlesvideo_translate_button_clicked(self))
    self.global_panel_translation_content.layout().addWidget(self.global_subtitlesvideo_translate_button, 0, 2, Qt.AlignTop)

    self.global_panel_content_stacked_widgets.addWidget(self.global_panel_translation_content)


def global_subtitlesvideo_translate_button_clicked(self):
    """Function to translate subtitles"""
    run_command = False

    if bool(self.subtitles_list):
        are_you_sure_message = QMessageBox(self)
        are_you_sure_message.setWindowTitle(self.tr('Are you sure?'))
        are_you_sure_message.setText(self.tr('This will overwrite your actual subtitle set. New text will be applied. Are you sure you want to replace your actual subtitles?'))
        are_you_sure_message.addButton(self.tr('Yes'), QMessageBox.AcceptRole)
        are_you_sure_message.addButton(self.tr('No'), QMessageBox.RejectRole)
        ret = are_you_sure_message.exec_()

        if ret == QMessageBox.AcceptRole:
            run_command = True
    else:
        run_command = True

    if run_command:
        language_from = LANGUAGE_DICT_LIST[self.global_subtitlesvideo_autosync_lang_from_combobox.currentText()].split('-')[0]
        language_to = LANGUAGE_DICT_LIST[self.global_subtitlesvideo_autosync_lang_to_combobox.currentText()].split('-')[0]
        translator = Translator(from_lang=language_from, to_lang=language_to)

        for subtitle in self.subtitles_list:
            subtitle[2] = translator.translate(subtitle[2].replace('\n', ' ').replace('  ', ' '))

