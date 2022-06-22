"""Subtitles Video panel

"""
from PyQt5.QtWidgets import QPushButton, QWidget, QTableWidget, QAbstractItemView, QLineEdit, QTableWidgetItem, QHeaderView, QVBoxLayout
from PyQt5.QtCore import QEvent, Qt
from PyQt5.QtGui import QKeySequence

from subtitld.modules.shortcuts import shortcuts_dict
from subtitld.interface import global_panel


class GlobalSubtitlesvideoPanelTabwidgetShortkeysEditbox(QLineEdit):
    """Class to reimplement QLineEdit in order to get shorkeys selection"""
    def __init__(self, *args, parent=None):
        super(GlobalSubtitlesvideoPanelTabwidgetShortkeysEditbox, self).__init__(*args)
        # self.set_key_sequence(key_sequence)

    def set_key_sequence(self, key_sequence):
        """Set text with the shortkey"""
        self.setText(key_sequence.toString(QKeySequence.NativeText))

    def keyPressEvent(self, event):
        """Function on keyPressEvent"""
        if event.type() == QEvent.KeyPress:
            key = event.key()

            if key == Qt.Key_unknown:
                return

            if key in [Qt.Key_Control, Qt.Key_Shift, Qt.Key_Alt, Qt.Key_Meta]:
                return

            modifiers = event.modifiers()
            # keyText = event.text()

            if modifiers & Qt.ShiftModifier:
                key += Qt.SHIFT
            if modifiers & Qt.ControlModifier:
                key += Qt.CTRL
            if modifiers & Qt.AltModifier:
                key += Qt.ALT
            if modifiers & Qt.MetaModifier:
                key += Qt.META

            self.set_key_sequence(QKeySequence(key))


def load_menu(self):
    """Function to load subtitles panel widgets"""
    self.global_panel_keyboardshortcuts_menu_button = QPushButton('Keyboard shortcuts')
    self.global_panel_keyboardshortcuts_menu_button.setCheckable(True)
    self.global_panel_keyboardshortcuts_menu_button.setProperty('class', 'global_panel_menu')
    self.global_panel_keyboardshortcuts_menu_button.clicked.connect(lambda: global_panel_menu_changed(self))
    self.global_panel_menu.layout().addWidget(self.global_panel_keyboardshortcuts_menu_button)


def global_panel_menu_changed(self):
    global_panel.global_panel_menu_changed(self, self.global_panel_keyboardshortcuts_menu_button, self.global_panel_keyboardshortcuts_content)


def load_widgets(self):
    """Function to load subtitles panel widgets"""

    self.global_panel_keyboardshortcuts_content = QWidget()
    self.global_panel_keyboardshortcuts_content.setLayout(QVBoxLayout())
    self.global_panel_keyboardshortcuts_content.layout().setContentsMargins(0, 0, 0, 0)

    self.global_panel_tabwidget_shortkeys_editbox = GlobalSubtitlesvideoPanelTabwidgetShortkeysEditbox()
    self.global_panel_tabwidget_shortkeys_editbox.setStyleSheet('QLineEdit { background-color:rgb(255, 255, 255); border: 1px solid silver; border-radius: 5px; padding: 5px 5px 5px 5px; font-size:16px; color:black; qproperty-alignment: "AlignCenter";}')
    self.global_panel_keyboardshortcuts_content.layout().addWidget(self.global_panel_tabwidget_shortkeys_editbox)

    self.global_panel_tabwidget_shortkeys_editbox_confirm = QPushButton(self.tr('Confirm').upper())
    self.global_panel_tabwidget_shortkeys_editbox_confirm.setProperty('class', 'button_dark')
    self.global_panel_tabwidget_shortkeys_editbox_confirm.clicked.connect(lambda: global_panel_tabwidget_shortkeys_editbox_confirm_clicked(self))
    self.global_panel_keyboardshortcuts_content.layout().addWidget(self.global_panel_tabwidget_shortkeys_editbox_confirm)

    self.global_panel_tabwidget_shortkeys_editbox_cancel = QPushButton(self.tr('Cancel').upper())
    self.global_panel_tabwidget_shortkeys_editbox_cancel.setProperty('class', 'button_dark')
    self.global_panel_tabwidget_shortkeys_editbox_cancel.clicked.connect(lambda: global_panel_tabwidget_shortkeys_editbox_cancel_clicked(self))
    self.global_panel_keyboardshortcuts_content.layout().addWidget(self.global_panel_tabwidget_shortkeys_editbox_cancel)

    self.global_panel_tabwidget_shortkeys_table = QTableWidget()
    self.global_panel_tabwidget_shortkeys_table.setColumnCount(2)
    self.global_panel_tabwidget_shortkeys_table.verticalHeader().setVisible(False)
    self.global_panel_tabwidget_shortkeys_table.horizontalHeader().setVisible(False)
    self.global_panel_tabwidget_shortkeys_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    # self.global_panel_tabwidget_shortkeys_table.setShowGrid(False)
    self.global_panel_tabwidget_shortkeys_table.setSelectionBehavior(QAbstractItemView.SelectRows)
    # self.global_panel_tabwidget_shortkeys_table.clicked.connect(lambda:project_new_panel_info_panel_options_pmaterials_panel_files_clicked(self))
    self.global_panel_keyboardshortcuts_content.layout().addWidget(self.global_panel_tabwidget_shortkeys_table)

    self.global_panel_tabwidget_shortkeys_set_button = QPushButton(self.tr('Set shortcut').upper())
    # self.global_panel_tabwidget_shortkeys_set_button.setCheckable(True)
    self.global_panel_tabwidget_shortkeys_set_button.setProperty('class', 'button_dark')
    self.global_panel_tabwidget_shortkeys_set_button.clicked.connect(lambda: global_panel_tabwidget_shortkeys_set_button_clicked(self))
    self.global_panel_keyboardshortcuts_content.layout().addWidget(self.global_panel_tabwidget_shortkeys_set_button)

    self.global_panel_content_stacked_widgets.addWidget(self.global_panel_keyboardshortcuts_content)

    global_panel_tabwidget_shortkeys_table_update(self)


def global_panel_tabwidget_shortkeys_table_update(self):
    """Function to update subtitlesvideo panel shorkeys table"""
    self.global_panel_tabwidget_shortkeys_table.clear()
    self.global_panel_tabwidget_shortkeys_table.setRowCount(len(shortcuts_dict))
    inverted_shortcuts_dict = {value: key for key, value in shortcuts_dict.items()}
    i = 0
    for item in shortcuts_dict:
        item_name = QTableWidgetItem(shortcuts_dict[item])
        self.global_panel_tabwidget_shortkeys_table.setItem(i, 0, item_name)
        item_name = QTableWidgetItem(self.settings['shortcuts'].get(inverted_shortcuts_dict[shortcuts_dict[item]], [''])[0])
        self.global_panel_tabwidget_shortkeys_table.setItem(i, 1, item_name)
        i += 1


def global_panel_tabwidget_shortkeys_set_button_clicked(self):
    """Function to change button states"""
    self.global_panel_tabwidget_shortkeys_set_button.setVisible(not self.global_panel_tabwidget_shortkeys_set_button.isVisible())
    self.global_panel_tabwidget_shortkeys_editbox.setVisible(not self.global_panel_tabwidget_shortkeys_set_button.isVisible())
    self.global_panel_tabwidget_shortkeys_editbox_confirm.setVisible(not self.global_panel_tabwidget_shortkeys_set_button.isVisible())
    self.global_panel_tabwidget_shortkeys_editbox_cancel.setVisible(not self.global_panel_tabwidget_shortkeys_set_button.isVisible())
    self.global_panel_tabwidget_shortkeys_table.setVisible(self.global_panel_tabwidget_shortkeys_set_button.isVisible())


def global_panel_tabwidget_shortkeys_editbox_cancel_clicked(self):
    """Function to cancel shortkeys editing"""
    # self.global_panel_tabwidget_shortkeys_set_button.setVisible(True)
    global_panel_tabwidget_shortkeys_set_button_clicked(self)


def global_panel_tabwidget_shortkeys_editbox_confirm_clicked(self):
    """Function to confirm shortkey editing"""
    inverted_shortcuts_dict = {value: key for key, value in shortcuts_dict.items()}
    self.settings['shortcuts'][inverted_shortcuts_dict[self.global_panel_tabwidget_shortkeys_table.item(self.global_panel_tabwidget_shortkeys_table.currentRow(), 0).text()]] = [self.global_panel_tabwidget_shortkeys_editbox.text()]
    self.shortcuts.load(self, self.settings['shortcuts'])
    global_panel_tabwidget_shortkeys_table_update(self)
    global_panel_tabwidget_shortkeys_editbox_cancel_clicked(self)
