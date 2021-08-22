"""Module for subtitle list panel

"""

import os

from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtWidgets import QPushButton, QLabel, QFileDialog, QListWidget, QListView, QMessageBox, QWidget, QLineEdit
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, Qt, QSize

from subtitld.modules import file_io, quality_check
from subtitld.modules.paths import LIST_OF_SUPPORTED_SUBTITLE_EXTENSIONS, PATH_SUBTITLD_GRAPHICS


def load(self):
    """Function to load subtitles list widgets"""
    self.subtitles_list_widget = QLabel(parent=self)
    self.subtitles_list_widget.setObjectName('subtitles_list_widget')
    self.subtitles_list_widget_animation = QPropertyAnimation(self.subtitles_list_widget, b'geometry')
    self.subtitles_list_widget_animation.setEasingCurve(QEasingCurve.OutCirc)

    self.toppanel_usf_label = QLabel(parent=self.subtitles_list_widget)

    self.toppanel_format_label = QLabel(parent=self.subtitles_list_widget)
    self.toppanel_format_label.setStyleSheet('QLabel { qproperty-alignment: "AlignRight | AlignVCenter"; padding: 0 4 0 0; font-weight: bold; font-size:10px; color: white; border-bottom-right-radius: 3px; background-color: rgb(62,83,99); }')

    self.toppanel_save_button = QPushButton(parent=self.subtitles_list_widget)
    self.toppanel_save_button.clicked.connect(lambda: toppanel_save_button_clicked(self))
    self.toppanel_save_button.setIcon(QIcon(os.path.join(PATH_SUBTITLD_GRAPHICS, 'save_icon.png')))
    self.toppanel_save_button.setIconSize(QSize(20, 20))
    self.toppanel_save_button.setObjectName('button_dark')
    self.toppanel_save_button.setStyleSheet('QPushButton { border-right:0; }')

    self.toppanel_open_button = QPushButton(parent=self.subtitles_list_widget)
    self.toppanel_open_button.clicked.connect(lambda: toppanel_open_button_clicked(self))
    self.toppanel_open_button.setIcon(QIcon(os.path.join(PATH_SUBTITLD_GRAPHICS, 'open_icon.png')))
    self.toppanel_open_button.setIconSize(QSize(20, 20))
    self.toppanel_open_button.setObjectName('button')
    self.toppanel_open_button.setStyleSheet('QPushButton { border-left:0; }')

    self.toppanel_subtitle_file_info_label = QLabel(parent=self.subtitles_list_widget)
    self.toppanel_subtitle_file_info_label.setObjectName('toppanel_subtitle_file_info_label')

    self.subtitles_list_qlistwidget = QListWidget(parent=self.subtitles_list_widget)
    self.subtitles_list_qlistwidget.setViewMode(QListView.ListMode)
    self.subtitles_list_qlistwidget.setObjectName('subtitles_list_qlistwidget')
    self.subtitles_list_qlistwidget.setSpacing(5)
    self.subtitles_list_qlistwidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    self.subtitles_list_qlistwidget.setFocusPolicy(Qt.NoFocus)
    self.subtitles_list_qlistwidget.setIconSize(QSize(42, 42))
    self.subtitles_list_qlistwidget.clicked.connect(lambda: subtitles_list_qlistwidget_item_clicked(self))

    self.subtitles_list_findandreplace_list = []
    self.subtitles_list_findandreplace_index = None

    self.subtitles_list_findandreplace_toggle_button = QPushButton('Find'.upper(), parent=self.subtitles_list_widget) # It will be 'Find and replace'
    self.subtitles_list_findandreplace_toggle_button.setObjectName('button')
    self.subtitles_list_findandreplace_toggle_button.clicked.connect(lambda: subtitles_list_findandreplace_toggle_button_clicked(self))

    self.subtitles_list_findandreplace_panel = QWidget()
    self.subtitles_list_findandreplace_panel.setWindowFlags(Qt.Tool)
    #self.subtitles_list_findandreplace_panel.setObjectName('QLabel')
    #self.subtitles_list_findandreplace_panel.setStyleSheet('QLabel { border-radius: 4px; background: rgba(106, 116, 131,100); }')
    self.subtitles_list_findandreplace_panel.setVisible(False)

    self.subtitles_list_findandreplace_find_field = QLineEdit(parent=self.subtitles_list_findandreplace_panel)
    self.subtitles_list_findandreplace_find_field.setObjectName('qlineedit')
    self.subtitles_list_findandreplace_find_field.textChanged.connect(lambda: subtitles_list_findandreplace_find_field_textchanged(self))

    self.subtitles_list_findandreplace_findnext_button = QPushButton('FIND', parent=self.subtitles_list_findandreplace_panel)
    self.subtitles_list_findandreplace_findnext_button.setObjectName('button')
    self.subtitles_list_findandreplace_findnext_button.clicked.connect(lambda: subtitles_list_findandreplace_find_field_clicked(self))

    self.subtitles_list_findandreplace_replace_field = QLineEdit(parent=self.subtitles_list_findandreplace_panel)
    self.subtitles_list_findandreplace_replace_field.setObjectName('qlineedit')
    self.subtitles_list_findandreplace_replace_field.setVisible(False)

    self.subtitles_list_findandreplace_replace_button = QPushButton(parent=self.subtitles_list_findandreplace_panel)
    self.subtitles_list_findandreplace_replace_button.setObjectName('button')
    self.subtitles_list_findandreplace_replace_button.setVisible(False)

    self.subtitles_list_findandreplace_replaceandfindnext_button = QPushButton(parent=self.subtitles_list_findandreplace_panel)
    self.subtitles_list_findandreplace_replaceandfindnext_button.setObjectName('button')
    self.subtitles_list_findandreplace_replaceandfindnext_button.setVisible(False)

    self.subtitles_list_findandreplace_replaceall_button = QPushButton(parent=self.subtitles_list_findandreplace_panel)
    self.subtitles_list_findandreplace_replaceall_button.setObjectName('button')
    self.subtitles_list_findandreplace_replaceall_button.setVisible(False)

    self.subtitles_list_toggle_button = QPushButton(parent=self)
    self.subtitles_list_toggle_button.clicked.connect(lambda: subtitles_list_toggle_button_clicked(self))
    self.subtitles_list_toggle_button.setCheckable(True)
    self.subtitles_list_toggle_button.setObjectName('subtitles_list_toggle_button')
    self.subtitles_list_toggle_button_animation = QPropertyAnimation(self.subtitles_list_toggle_button, b'geometry')
    self.subtitles_list_toggle_button_animation.setEasingCurve(QEasingCurve.OutCirc)


def resized(self):
    """Function to call when resizing subtitles list"""
    if self.subtitles_list or self.video_metadata:
        self.subtitles_list_widget.setGeometry(0, 0, (self.width()*.2)-15, self.height())
    else:
        self.subtitles_list_widget.setGeometry(-((self.width()*.2)-15), 0, (self.width()*.2)-15, self.height())

    self.toppanel_usf_label.setGeometry(0, 20, 55, 20)
    self.toppanel_format_label.setGeometry(0, 40, 55, 20)

    self.toppanel_save_button.setGeometry(60, 20, 40, 40)
    self.toppanel_open_button.setGeometry(self.toppanel_save_button.x()+self.toppanel_save_button.width(), self.toppanel_save_button.y(), self.toppanel_save_button.height(), self.toppanel_save_button.height())
    self.toppanel_subtitle_file_info_label.setGeometry(self.toppanel_open_button.x()+self.toppanel_open_button.width()+10, self.toppanel_save_button.y(), self.subtitles_list_widget.width()-self.toppanel_open_button.x()-self.toppanel_open_button.width()-40, self.toppanel_save_button.height())

    #self.subtitles_list_qlistwidget.setGeometry(20, 100, self.subtitles_list_widget.width()-40, self.subtitles_list_widget.height()-80-self.playercontrols_widget.height()-60)

    if (self.subtitles_list or self.video_metadata):
        if self.subtitles_list_toggle_button.isChecked():
            self.subtitles_list_toggle_button.setGeometry(self.global_subtitlesvideo_panel_widget.width()-25, 0, 25, 80)
        else:
            self.subtitles_list_toggle_button.setGeometry(self.subtitles_list_widget.width()-25, 0, 25, 80)
    else:
        self.subtitles_list_toggle_button.setGeometry(-25, 0, 25, 80)

    # subtitles_list_findandreplace_toggle_button_clicked(self)

    self.subtitles_list_qlistwidget.setGeometry(20, 100, self.subtitles_list_widget.width()-40, self.subtitles_list_widget.height()-80-self.playercontrols_widget.height()-60)
    self.subtitles_list_findandreplace_toggle_button.setGeometry(self.subtitles_list_qlistwidget.x(), self.subtitles_list_widget.height()-self.playercontrols_widget.height()-35, ( self.subtitles_list_widget.width()-40)*.5, 20)
    self.subtitles_list_findandreplace_panel.setGeometry(self.subtitles_list_qlistwidget.x(), self.subtitles_list_widget.height()-self.playercontrols_widget.height()-105, self.subtitles_list_qlistwidget.width(), 65)
    self.subtitles_list_findandreplace_find_field.setGeometry(5, 5, self.subtitles_list_findandreplace_panel.width()-90, 25)
    self.subtitles_list_findandreplace_findnext_button.setGeometry(5+self.subtitles_list_findandreplace_find_field.width()+5, 5, 50, 25)
    self.subtitles_list_findandreplace_replace_field.setGeometry(5, 35, self.subtitles_list_findandreplace_panel.width()-90, 25)
    self.subtitles_list_findandreplace_replace_button.setGeometry(5+self.subtitles_list_findandreplace_replace_field.width()+5, 35, 25, 25)
    self.subtitles_list_findandreplace_replaceandfindnext_button.setGeometry(5+self.subtitles_list_findandreplace_replace_field.width()+30, 35, 25, 25)
    self.subtitles_list_findandreplace_replaceall_button.setGeometry(5+self.subtitles_list_findandreplace_replace_field.width()+55, 35, 25, 25)

def subtitles_list_toggle_button_clicked(self):
    """Function to call when clicking toggle button"""
    if self.subtitles_list_toggle_button.isChecked():
        subtitleslist_toggle_button_to_end(self)
        self.global_subtitlesvideo_panel.show_global_subtitlesvideo_panel(self)
        hide(self)
    else:
        self.global_subtitlesvideo_panel.hide_global_subtitlesvideo_panel(self)
        show(self)


def subtitleslist_toggle_button_to_end(self):
    """Function to show subtitles list panel"""
    self.generate_effect(self.subtitles_list_toggle_button_animation, 'geometry', 700, [self.subtitles_list_toggle_button.x(), self.subtitles_list_toggle_button.y(), self.subtitles_list_toggle_button.width(), self.subtitles_list_toggle_button.height()], [self.global_subtitlesvideo_panel_widget.width()-25, self.subtitles_list_toggle_button.y(), self.subtitles_list_toggle_button.width(), self.subtitles_list_toggle_button.height()])


def update_subtitles_list_widget(self):
    """Function to update subtitles list widgets"""
    # self.subtitles_list_qlistwidget.setVisible(bool(self.subtitles_list))
    update_subtitles_list_qlistwidget(self)


def update_subtitles_list_qlistwidget(self):
    """Function to update subtitles list widgets"""
    self.subtitles_list_qlistwidget.clear()
    if self.subtitles_list:
        counter = 1
        for sub in sorted(self.subtitles_list):
            self.subtitles_list_qlistwidget.addItem(str(counter) + ' - ' + sub[2])

            if self.settings['quality_check'].get('enabled', False):
                approved, reasons = quality_check.check_subtitle(sub, self.settings['quality_check'])
                if not approved:
                    self.subtitles_list_qlistwidget.item(counter-1).setForeground(QColor('#9e1a1a'))
                    # set item tipbox with reasons?
            counter += 1
    if self.selected_subtitle:
        self.subtitles_list_qlistwidget.setCurrentRow(self.subtitles_list.index(self.selected_subtitle))


def update_subtitleslist_format_label(self):
    if self.format_usf_present:
        self.toppanel_usf_label.setText('USF')
        self.toppanel_usf_label.setStyleSheet('QLabel { qproperty-alignment: "AlignRight | AlignVCenter"; padding: 0 4 0 0; font-weight: bold; font-size:10px; color: rgb(62,83,99); border-top-right-radius: 3px; background-color: rgb(85,212,63); }')
    else:
        self.toppanel_usf_label.setText('NO USF')
        self.toppanel_usf_label.setStyleSheet('QLabel { qproperty-alignment: "AlignRight | AlignVCenter"; padding: 0 4 0 0; font-weight: bold; font-size:10px; color: silver; border-top-right-radius: 3px; background-color: rgb(106,116,131); }')
    self.toppanel_format_label.setText(self.format_to_save)

def subtitles_list_qlistwidget_item_clicked(self):
    """Function to call when a subtitle item on the list is clicked"""
    if self.subtitles_list_qlistwidget.currentItem():
        sub_index = int(self.subtitles_list_qlistwidget.currentItem().text().split(' - ')[0]) - 1
        self.selected_subtitle = self.subtitles_list[sub_index]

    if self.selected_subtitle:
        if not (self.player_widget.position > self.selected_subtitle[0] and self.player_widget.position < self.selected_subtitle[0] + self.selected_subtitle[1]):
            self.player_widget.seek(self.selected_subtitle[0] + (self.selected_subtitle[1]*.5))

    self.properties.update_properties_widget(self)
    self.timeline.update(self)
    self.timeline.update_scrollbar(self, position='middle')


def show(self):
    """Function to show subtitle list panel"""
    self.generate_effect(self.subtitles_list_widget_animation, 'geometry', 700, [self.subtitles_list_widget.x(), self.subtitles_list_widget.y(), self.subtitles_list_widget.width(), self.subtitles_list_widget.height()], [0, self.subtitles_list_widget.y(), self.subtitles_list_widget.width(), self.subtitles_list_widget.height()])
    self.generate_effect(self.subtitles_list_toggle_button_animation, 'geometry', 700, [self.subtitles_list_toggle_button.x(), self.subtitles_list_toggle_button.y(), self.subtitles_list_toggle_button.width(), self.subtitles_list_toggle_button.height()], [self.subtitles_list_widget.width()-25, self.subtitles_list_toggle_button.y(), self.subtitles_list_toggle_button.width(), self.subtitles_list_toggle_button.height()])
    self.global_subtitlesvideo_panel.hide_global_subtitlesvideo_panel(self)
    update_toppanel_subtitle_file_info_label(self)


def hide(self):
    """Function to hide subtitle list panel"""
    self.generate_effect(self.subtitles_list_widget_animation, 'geometry', 700, [self.subtitles_list_widget.x(), self.subtitles_list_widget.y(), self.subtitles_list_widget.width(), self.subtitles_list_widget.height()], [-int(self.width()*.2), self.subtitles_list_widget.y(), self.subtitles_list_widget.width(), self.subtitles_list_widget.height()])


def toppanel_save_button_clicked(self):
    """Function to call when save button on subtitles list panel is clicked"""
    actual_subtitle_file = False
    if self.actual_subtitle_file:
        for ext in LIST_OF_SUPPORTED_SUBTITLE_EXTENSIONS[self.format_to_save]['extensions']:
            if self.actual_subtitle_file.endswith(ext):
                actual_subtitle_file = self.actual_subtitle_file
                break

    if not actual_subtitle_file:
        suggested_path = os.path.dirname(self.video_metadata['filepath'])
        save_formats = self.format_to_save + ' ' + LIST_OF_SUPPORTED_SUBTITLE_EXTENSIONS[self.format_to_save]['description'] + ' ({})'.format(" ".join(["*.{}".format(fo) for fo in LIST_OF_SUPPORTED_SUBTITLE_EXTENSIONS[self.format_to_save]['extensions']]))

        for extformat in LIST_OF_SUPPORTED_SUBTITLE_EXTENSIONS:
            if not extformat == self.format_to_save:
                save_formats += ';;' + extformat + ' ' + LIST_OF_SUPPORTED_SUBTITLE_EXTENSIONS[extformat]['description'] + ' ({})'.format(" ".join(["*.{}".format(fo) for fo in LIST_OF_SUPPORTED_SUBTITLE_EXTENSIONS[extformat]['extensions']]))
        suggested_name = os.path.basename(self.video_metadata['filepath']).rsplit('.', 1)[0]

        # tem que reportar o bug que não retorna o selectedFilter se o dialogo for nativo
        filedialog = QFileDialog.getSaveFileName(self, self.tr('Select the subtitle file'), os.path.join(suggested_path, suggested_name), save_formats)

        if filedialog[0] and filedialog[1]:
            filename = filedialog[0]
            exts = []
            for ext in filedialog[1].split('(', 1)[1].split(')', 1)[0].split('*'):
                if ext:
                    exts.append(ext.strip())
            if not filename.endswith(tuple(exts)):
                filename += exts[0]
            if not self.format_to_save == filedialog[1].split(' ', 1)[0]:
                self.format_to_save = filedialog[1].split(' ', 1)[0]

            self.global_subtitlesvideo_panel.update_global_subtitlesvideo_save_as_combobox(self)

            self.actual_subtitle_file = filename

    if self.actual_subtitle_file:
        file_io.save_file(self.actual_subtitle_file, self.subtitles_list, self.format_to_save, self.selected_language)
        file_io.save_file(self.actual_subtitle_file.rsplit('.', 1)[0] + '.usf', self.subtitles_list, 'USF', self.selected_language)
        self.format_usf_present = True
        update_subtitleslist_format_label(self)
        update_toppanel_subtitle_file_info_label(self)
        self.unsaved = False


def toppanel_open_button_clicked(self, update_interface=True):
    """Function to call when open button on subtitles list panel is clicked"""
    if self.unsaved:
        save_message_box = QMessageBox(self)

        save_message_box.setWindowTitle(self.tr('Unsaved changes'))
        save_message_box.setText(
            self.tr('Do you want to save the changes you made on the subtitles?')
        )
        save_message_box.addButton(self.tr('Save'), QMessageBox.AcceptRole)
        save_message_box.addButton(self.tr("Don't save"), QMessageBox.RejectRole)
        ret = save_message_box.exec_()

        if ret == QMessageBox.AcceptRole:
            self.subttileslist.toppanel_save_button_clicked(self)

    file_io.open_filepath(self)


def subtitles_list_findandreplace_toggle_button_clicked(self):
    self.subtitles_list_findandreplace_panel.setVisible(True)

def subtitles_list_findandreplace_find_field_textchanged(self):
    self.subtitles_list_findandreplace_list = []
    self.subtitles_list_findandreplace_index = None


def subtitles_list_findandreplace_find_field_clicked(self):
    if self.subtitles_list_findandreplace_find_field.text():
        if self.subtitles_list_findandreplace_index is None:
            self.subtitles_list_findandreplace_list = []
            for subtitle in self.subtitles_list:
                if self.subtitles_list_findandreplace_find_field.text() in subtitle[2]:
                    self.subtitles_list_findandreplace_list.append([self.subtitles_list.index(subtitle)])
            self.subtitles_list_findandreplace_index = 0
        subtitles_list_findandreplace_update(self)


def subtitles_list_findandreplace_update(self):
    if self.subtitles_list_findandreplace_index is not None and self.subtitles_list_findandreplace_list:
        self.selected_subtitle = self.subtitles_list[self.subtitles_list_findandreplace_list[self.subtitles_list_findandreplace_index][0]]
        if self.selected_subtitle:
            self.subtitles_list_qlistwidget.setCurrentRow(self.subtitles_list.index(self.selected_subtitle))
            subtitles_list_qlistwidget_item_clicked(self)
            if self.subtitles_list_findandreplace_index < len(self.subtitles_list_findandreplace_list) - 1:
                self.subtitles_list_findandreplace_index += 1
            else:
                self.subtitles_list_findandreplace_index = 0

def update_toppanel_subtitle_file_info_label(self):
    """Function to update top information on subtitles list panel"""
    text = self.tr('Actual video does not have saved subtitle file.')
    if self.actual_subtitle_file:
        text = '<b><snall>' + self.tr('Actual project').upper() + '</small></b><br><big>' + os.path.basename(self.actual_subtitle_file) + '</big>'
    self.toppanel_subtitle_file_info_label.setText(text)
