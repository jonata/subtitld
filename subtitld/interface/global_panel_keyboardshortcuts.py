"""Subtitles Video panel

"""
from PySide6.QtWidgets import QPushButton, QWidget, QTableWidget, QAbstractItemView, QLineEdit, QTableWidgetItem, QHeaderView, QVBoxLayout, QHBoxLayout, QLabel, QGridLayout, QSizePolicy
from PySide6.QtCore import QEvent, Qt
from PySide6.QtGui import QKeySequence
from subtitld.modules import shortcuts

from subtitld.modules.shortcuts import shortcuts_dict, default_shortcuts_dict
from subtitld.interface import global_panel
from subtitld.interface.translation import _


class global_panel_keyboardshortcut_qlineedit(QLineEdit):
    """Class to reimplement QLineEdit in order to get shorkeys selection"""
    def __init__(widget, *args):
        super(global_panel_keyboardshortcut_qlineedit, widget).__init__(*args)
        widget.setLayout(QHBoxLayout())
        widget.setAlignment(Qt.AlignCenter)
        widget.setReadOnly(True)
        widget.setSizePolicy(QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Preferred))
        widget.layout().setContentsMargins(0, 0, 0, 0)
        widget.layout().setSpacing(5)
        widget.command = ''

    def update_shortcuts(widget):
        while widget.layout().count():
            child = widget.layout().takeAt(0).widget()
            if child:
                child.setParent(None)
                child.deleteLater()

        command_string = widget.command

        widget.layout().addStretch()

        if not command_string:
            qlabel = QLabel(_('global_panel_keyboardshortcuts.press_shorkey_combination') if widget.isEnabled() else _('global_panel_keyboardshortcuts.no_shortkey'))
            qlabel.setProperty('class', 'units_label')
            qlabel.setAlignment(Qt.AlignCenter)
            widget.layout().addWidget(qlabel, 0, Qt.AlignCenter | Qt.AlignBottom)
        else:
            if command_string == '+':
                command_string = '＋'
            for key in command_string.replace('++', '+＋').split('+'):
                if key:
                    button = QPushButton(key)
                    button.setProperty('class', 'keyboard_key')
                    widget.layout().addWidget(button, 0, Qt.AlignCenter | Qt.AlignBottom)

        widget.layout().addStretch()

    def keyPressEvent(widget, event):
        widget.setReadOnly(False)
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
            widget.command = QKeySequence(key).toString()
            widget.update_shortcuts()

        widget.setReadOnly(True)


def load_menu(self):
    """Function to load subtitles panel widgets"""
    self.global_panel_keyboardshortcuts_menu_button = QPushButton()
    self.global_panel_keyboardshortcuts_menu_button.setCheckable(True)
    self.global_panel_keyboardshortcuts_menu_button.setProperty('class', 'global_panel_menu')
    self.global_panel_keyboardshortcuts_menu_button.clicked.connect(lambda: global_panel_menu_changed(self))
    self.global_panel_menu.layout().addWidget(self.global_panel_keyboardshortcuts_menu_button)


def global_panel_menu_changed(self):
    self.global_panel_keyboardshortcuts_menu_button.setEnabled(False)
    global_panel.global_panel_menu_changed(self, self.global_panel_keyboardshortcuts_menu_button, self.global_panel_keyboardshortcuts_content)


def load_widgets(self):
    """Function to load subtitles panel widgets"""

    self.global_panel_keyboardshortcuts_content = QWidget()
    self.global_panel_keyboardshortcuts_content.setLayout(QGridLayout())
    self.global_panel_keyboardshortcuts_content.layout().setContentsMargins(0, 0, 0, 0)

    self.global_panel_tabwidget_shortkeys_table = QTableWidget()
    self.global_panel_tabwidget_shortkeys_table.setObjectName('global_panel_tabwidget_shortkeys_table')
    self.global_panel_tabwidget_shortkeys_table.setColumnCount(3)
    self.global_panel_tabwidget_shortkeys_table.verticalHeader().setVisible(False)
    self.global_panel_tabwidget_shortkeys_table.setColumnHidden(1, True)
    self.global_panel_tabwidget_shortkeys_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
    self.global_panel_tabwidget_shortkeys_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    self.global_panel_tabwidget_shortkeys_table.horizontalHeader().setHighlightSections(False)
    self.global_panel_tabwidget_shortkeys_table.horizontalHeader().setDefaultAlignment(Qt.AlignLeft | Qt.AlignVCenter)
    self.global_panel_tabwidget_shortkeys_table.setShowGrid(False)
    self.global_panel_tabwidget_shortkeys_table.setSelectionBehavior(QAbstractItemView.SelectRows)
    self.global_panel_tabwidget_shortkeys_table.clicked.connect(lambda: global_panel_tabwidget_shortkeys_table_clicked(self))
    self.global_panel_keyboardshortcuts_content.layout().addWidget(self.global_panel_tabwidget_shortkeys_table, 0, 0, 3, 1)

    self.global_panel_tabwidget_shortkeys_details = QVBoxLayout()

    self.global_panel_tabwidget_shortkeys_details_warning = QLabel()
    self.global_panel_tabwidget_shortkeys_details_warning.setProperty('class', 'units_label')
    self.global_panel_tabwidget_shortkeys_details.addWidget(self.global_panel_tabwidget_shortkeys_details_warning, 0, Qt.AlignCenter)

    self.global_panel_keyboardshortcut_qlineedit = global_panel_keyboardshortcut_qlineedit()
    self.global_panel_keyboardshortcut_qlineedit.setObjectName('global_panel_keyboardshortcut_qlineedit')
    self.global_panel_tabwidget_shortkeys_details.addWidget(self.global_panel_keyboardshortcut_qlineedit)

    self.global_panel_keyboardshortcut_buttons = QWidget()
    self.global_panel_keyboardshortcut_buttons.setLayout(QHBoxLayout())
    self.global_panel_keyboardshortcut_buttons.layout().setContentsMargins(0, 10, 0, 0)
    self.global_panel_keyboardshortcut_buttons.layout().setSpacing(5)

    self.global_panel_keyboardshortcut_change_button = QPushButton()
    self.global_panel_keyboardshortcut_change_button.setProperty('class', 'subbutton2_dark')
    self.global_panel_keyboardshortcut_change_button.clicked.connect(lambda: global_panel_keyboardshortcut_change_button_clicked(self))
    self.global_panel_keyboardshortcut_buttons.layout().addWidget(self.global_panel_keyboardshortcut_change_button)

    self.global_panel_keyboardshortcut_confirm_button = QPushButton()
    self.global_panel_keyboardshortcut_confirm_button.setProperty('class', 'subbutton2_dark')
    self.global_panel_keyboardshortcut_confirm_button.clicked.connect(lambda: global_panel_keyboardshortcut_confirm_button_clicked(self))
    self.global_panel_keyboardshortcut_buttons.layout().addWidget(self.global_panel_keyboardshortcut_confirm_button)

    self.global_panel_keyboardshortcut_cancel_button = QPushButton()
    self.global_panel_keyboardshortcut_cancel_button.setProperty('class', 'subbutton2_dark')
    self.global_panel_keyboardshortcut_cancel_button.clicked.connect(lambda: global_panel_keyboardshortcut_cancel_button_clicked(self))
    self.global_panel_keyboardshortcut_buttons.layout().addWidget(self.global_panel_keyboardshortcut_cancel_button)

    self.global_panel_keyboardshortcut_clear_button = QPushButton()
    self.global_panel_keyboardshortcut_clear_button.setProperty('class', 'subbutton2_dark')
    self.global_panel_keyboardshortcut_clear_button.clicked.connect(lambda: global_panel_keyboardshortcut_clear_button_clicked(self))
    self.global_panel_keyboardshortcut_buttons.layout().addWidget(self.global_panel_keyboardshortcut_clear_button)

    self.global_panel_tabwidget_shortkeys_details.addWidget(self.global_panel_keyboardshortcut_buttons, 0, Qt.AlignCenter | Qt.AlignTop)

    self.global_panel_keyboardshortcuts_content.layout().addLayout(self.global_panel_tabwidget_shortkeys_details, 3, 0, 1, 1)

    self.global_panel_content_stacked_widgets.addWidget(self.global_panel_keyboardshortcuts_content)


def global_panel_tabwidget_shortkeys_table_update(self):
    """Function to update subtitlesvideo panel shorkeys table"""
    self.global_panel_tabwidget_shortkeys_table.clear()
    self.global_panel_tabwidget_shortkeys_table.setRowCount(len(shortcuts_dict))
    self.global_panel_tabwidget_shortkeys_table.setHorizontalHeaderLabels([_('global_panel_keyboardshortcuts.command'), 'internal_command', _('global_panel_keyboardshortcuts.shortkeys')])

    i = 0
    for item in shortcuts_dict:
        item_name = QTableWidgetItem(shortcuts_dict[item])
        self.global_panel_tabwidget_shortkeys_table.setItem(i, 0, item_name)
        item_name = QTableWidgetItem(item)
        self.global_panel_tabwidget_shortkeys_table.setItem(i, 1, item_name)
        item_name = QTableWidgetItem(self.settings['shortcuts'].get(item, default_shortcuts_dict.get(item, ['']))[0])
        self.global_panel_tabwidget_shortkeys_table.setItem(i, 2, item_name)
        i += 1
    update_global_panel_tabwidget_shortkeys_details(self)


def global_panel_tabwidget_shortkeys_table_clicked(self):
    update_global_panel_tabwidget_shortkeys_details(self)
    global_panel_keyboardshortcut_cancel_button_clicked(self)


def update_global_panel_tabwidget_shortkeys_details(self):
    self.global_panel_tabwidget_shortkeys_details_warning.setVisible(not bool(self.global_panel_tabwidget_shortkeys_table.currentItem()))
    self.global_panel_keyboardshortcut_qlineedit.setVisible(bool(self.global_panel_tabwidget_shortkeys_table.currentItem()))
    self.global_panel_keyboardshortcut_buttons.setVisible(bool(self.global_panel_tabwidget_shortkeys_table.currentItem()))

    if self.global_panel_tabwidget_shortkeys_table.currentItem():
        self.global_panel_keyboardshortcut_qlineedit.command = self.global_panel_tabwidget_shortkeys_table.item(self.global_panel_tabwidget_shortkeys_table.currentRow(), 2).text()
        self.global_panel_keyboardshortcut_qlineedit.update_shortcuts()


def global_panel_keyboardshortcut_change_button_clicked(self):
    self.global_panel_keyboardshortcut_confirm_button.setVisible(True)
    self.global_panel_keyboardshortcut_cancel_button.setVisible(True)
    self.global_panel_keyboardshortcut_change_button.setVisible(False)
    self.global_panel_keyboardshortcut_clear_button.setVisible(False)

    self.global_panel_keyboardshortcut_qlineedit.setEnabled(True)
    self.global_panel_keyboardshortcut_qlineedit.command = ''
    self.global_panel_keyboardshortcut_qlineedit.update_shortcuts()
    shortcuts.disable_actions(self)
    self.global_panel_keyboardshortcut_qlineedit.setFocus()


def global_panel_keyboardshortcut_confirm_button_clicked(self):
    command = self.global_panel_tabwidget_shortkeys_table.item(self.global_panel_tabwidget_shortkeys_table.currentRow(), 1).text()
    self.settings['shortcuts'][command] = [self.global_panel_keyboardshortcut_qlineedit.command]

    global_panel_keyboardshortcut_cancel_button_clicked(self)

    selected_row = self.global_panel_tabwidget_shortkeys_table.currentRow()
    global_panel_tabwidget_shortkeys_table_update(self)
    self.global_panel_tabwidget_shortkeys_table.setCurrentCell(selected_row, 0)
    global_panel_tabwidget_shortkeys_table_clicked(self)

    shortcuts.enable_actions(self)


def global_panel_keyboardshortcut_clear_button_clicked(self):
    command = self.global_panel_tabwidget_shortkeys_table.item(self.global_panel_tabwidget_shortkeys_table.currentRow(), 1).text()
    self.settings['shortcuts'][command] = ['']

    global_panel_keyboardshortcut_cancel_button_clicked(self)

    selected_row = self.global_panel_tabwidget_shortkeys_table.currentRow()
    global_panel_tabwidget_shortkeys_table_update(self)
    self.global_panel_tabwidget_shortkeys_table.setCurrentCell(selected_row, 0)
    global_panel_tabwidget_shortkeys_table_clicked(self)


def global_panel_keyboardshortcut_cancel_button_clicked(self):
    self.global_panel_keyboardshortcut_confirm_button.setVisible(False)
    self.global_panel_keyboardshortcut_cancel_button.setVisible(False)
    self.global_panel_keyboardshortcut_change_button.setVisible(True)
    self.global_panel_keyboardshortcut_clear_button.setVisible(True)
    self.global_panel_keyboardshortcut_qlineedit.setEnabled(False)

    update_global_panel_tabwidget_shortkeys_details(self)


def translate_widgets(self):
    self.global_panel_keyboardshortcuts_menu_button.setText(_('global_panel_keyboardshortcuts.title'))
    self.global_panel_keyboardshortcut_change_button.setText(_('global_panel_keyboardshortcuts.change'))
    self.global_panel_keyboardshortcut_confirm_button.setText(_('global_panel_keyboardshortcuts.confirm'))
    self.global_panel_keyboardshortcut_cancel_button.setText(_('global_panel_keyboardshortcuts.cancel'))
    self.global_panel_keyboardshortcut_clear_button.setText(_('global_panel_keyboardshortcuts.clear'))
    self.global_panel_tabwidget_shortkeys_details_warning.setText(_('global_panel_keyboardshortcuts.select_a_command'))
    global_panel_tabwidget_shortkeys_table_update(self)