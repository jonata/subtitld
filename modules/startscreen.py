#!/usr/bin/python3
# -*- coding: utf-8 -*-

import webbrowser
from datetime import datetime
from PyQt5.QtWidgets import QPushButton, QLabel, QWidget, QGraphicsOpacityEffect, QListWidget, QApplication, QLineEdit
from PyQt5.QtCore import QPropertyAnimation, Qt, QThread, pyqtSignal

from modules import file_io
from modules import authentication
from modules.paths import ACTUAL_OS


class thread_verify_user_and_machineid(QThread):
    command = pyqtSignal(dict)
    email = ''
    machine_id = ''

    def run(self):
        if self.email and self.machine_id:
            result = authentication.verify_user_and_machineid(email=self.email, machine_id=self.machine_id)
            self.command.emit(result)


def load(self):
    self.start_screen = QLabel(parent=self)
    self.start_screen_transparency = QGraphicsOpacityEffect()
    self.start_screen.setGraphicsEffect(self.start_screen_transparency)
    self.start_screen_transparency_animation = QPropertyAnimation(self.start_screen_transparency, b'opacity')
    self.start_screen_transparency.setOpacity(0)

    self.start_screen_recentfiles_background = QLabel(parent=self.start_screen)
    self.start_screen_recentfiles_background.setObjectName('start_screen_recentfiles_background')
    self.start_screen_recentfiles_background.setAutoFillBackground(True)

    self.start_screen_top_shadow = QLabel(parent=self.start_screen)
    self.start_screen_top_shadow.setObjectName('start_screen_top_shadow')

    self.start_screen_open_label = QLabel('OPEN A SUBTITLE OR A VIDEO', parent=self.start_screen)
    self.start_screen_open_label.setObjectName('start_screen_open_label')

    self.start_screen_open_button = QPushButton('OPEN', parent=self.start_screen)
    self.start_screen_open_button.clicked.connect(lambda: start_screen_open_button_clicked(self))
    self.start_screen_open_button.setObjectName('button_dark')

    self.start_screen_recent_label = QLabel('RECENT SUBTITLES', parent=self.start_screen)
    self.start_screen_recent_label.setObjectName('start_screen_recent_label')

    self.start_screen_recent_listwidget = QListWidget(parent=self.start_screen)
    self.start_screen_recent_listwidget.setObjectName('start_screen_recent_listwidget')
    self.start_screen_recent_listwidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    self.start_screen_recent_listwidget.setFocusPolicy(Qt.NoFocus)
    self.start_screen_recent_listwidget.itemDoubleClicked.connect(lambda: start_screen_recent_listwidget_item_clicked(self))

    self.start_screen_recent_alert = QLabel('There is no recent file history.', parent=self.start_screen)
    self.start_screen_recent_alert.setWordWrap(True)
    self.start_screen_recent_alert.setObjectName('start_screen_recent_alert')

    self.start_screen_adver_label = QLabel(parent=self.start_screen)
    self.start_screen_adver_label.setObjectName('start_screen_adver_label')
    self.start_screen_adver_label.setText('ADVANCED VERSION' if self.advanced_mode else 'BASIC VERSION')

    class start_screen_adver_holder(QWidget):
        def enterEvent(widget, event):
            self.start_screen_adver_label_show_machineid_button.setVisible(True)
            self.start_screen_adver_label_details.setVisible(False)

        def leaveEvent(widget, event):
            if not self.start_screen_adver_label_show_machineid_button.isChecked():
                self.start_screen_adver_label_show_machineid_button.setVisible(False)
                self.start_screen_adver_label_details.setVisible(True)

    self.start_screen_adver_holder = start_screen_adver_holder(parent=self.start_screen)

    self.start_screen_adver_label_details = QLabel(parent=self.start_screen_adver_holder)
    self.start_screen_adver_label_details.setObjectName('start_screen_adver_label_details')

    days = authentication.get_days_to_expiry_date(auth_dict=self.settings['authentication'].get('codes', {}).get(ACTUAL_OS, {}))

    self.start_screen_adver_label_details.setText(str('You have more %s days to use<br>the Advanced version. If you<br>need some more information,<br>visit <b>subtitld.jonata.org</b>.' % days) if self.advanced_mode else 'If you need more features,<br>enable the advanced version.<br>Visit <b>subtitld.jonata.org</b> for<br>more information.')

    self.start_screen_adver_label_show_machineid_button = QPushButton('SHOW ADVANCED INFO', parent=self.start_screen_adver_holder)
    self.start_screen_adver_label_show_machineid_button.clicked.connect(lambda: start_screen_adver_label_show_machineid_button_clicked(self))
    self.start_screen_adver_label_show_machineid_button.setCheckable(True)
    self.start_screen_adver_label_show_machineid_button.setVisible(False)
    self.start_screen_adver_label_show_machineid_button.setObjectName('button_dark')

    self.start_screen_adver_panel = QLabel(parent=self)
    self.start_screen_adver_panel.setObjectName('start_screen_adver_panel')
    self.start_screen_adver_panel.setVisible(False)

    self.start_screen_adver_panel_label = QLabel('ADVANCED VERSION', parent=self.start_screen_adver_panel)
    self.start_screen_adver_panel_label.setObjectName('start_screen_adver_panel_label')

    self.start_screen_adver_label_machineid_label = QLabel('YOUR MACHINE ID IS:', parent=self.start_screen_adver_panel)
    self.start_screen_adver_label_machineid_label.setObjectName('start_screen_recent_label')

    class start_screen_adver_label_machineid(QLabel):
        def enterEvent(widget, event):
            self.generate_effect(self.start_screen_adver_label_machineid_copy_transparency_animation, 'opacity', 200, self.start_screen_adver_label_machineid_copy_transparency.opacity(), 1.0)

        def leaveEvent(widget, event):
            self.generate_effect(self.start_screen_adver_label_machineid_copy_transparency_animation, 'opacity', 50, self.start_screen_adver_label_machineid_copy_transparency.opacity(), 0.0)

    self.start_screen_adver_label_machineid = start_screen_adver_label_machineid(self.machine_id, parent=self.start_screen_adver_panel)
    self.start_screen_adver_label_machineid.setObjectName('start_screen_adver_label_machineid')

    self.start_screen_adver_label_machineid_copy = QPushButton('COPY', parent=self.start_screen_adver_label_machineid)
    self.start_screen_adver_label_machineid_copy.clicked.connect(lambda: start_screen_adver_label_machineid_copy_clicked(self))
    self.start_screen_adver_label_machineid_copy.setObjectName('button')
    self.start_screen_adver_label_machineid_copy_transparency = QGraphicsOpacityEffect()
    self.start_screen_adver_label_machineid_copy.setGraphicsEffect(self.start_screen_adver_label_machineid_copy_transparency)
    self.start_screen_adver_label_machineid_copy_transparency_animation = QPropertyAnimation(self.start_screen_adver_label_machineid_copy_transparency, b'opacity')
    self.start_screen_adver_label_machineid_copy_transparency.setOpacity(0)

    self.start_screen_adver_label_email_label = QLabel('YOUR EMAIL IS:', parent=self.start_screen_adver_panel)
    self.start_screen_adver_label_email_label.setObjectName('start_screen_recent_label')

    self.start_screen_adver_label_email = QLineEdit(parent=self.start_screen_adver_panel)
    self.start_screen_adver_label_email.setObjectName('start_screen_adver_label_email')
    self.start_screen_adver_label_email.editingFinished.connect(lambda: start_screen_adver_label_email_editing_finished(self))
    self.start_screen_adver_label_email.textEdited.connect(lambda: update_start_screen_adver_label_machineid_verify(self))
    self.start_screen_adver_label_email.setText(self.settings['authentication'].get('email', ''))

    self.start_screen_adver_label_status = QLabel(parent=self.start_screen_adver_panel)
    self.start_screen_adver_label_status.setObjectName('start_screen_adver_label_status')
    if self.advanced_mode:
        text = 'You are using the advanced version.'
    else:
        text = 'You are usign the basic version.'
    text += str(str('<br><small style="color:#3e5363;" >LAST CHECKED: ' + datetime.strptime(self.settings['authentication']['last_checked'], '%Y%m%d%H%M%S').strftime("%d/%m/%Y - %H:%M:%S")) if self.settings['authentication'].get('last_checked', '') else str(''))
    self.start_screen_adver_label_status.setText(text)

    self.start_screen_adver_label_machineid_verify = QPushButton('VERIFY', parent=self.start_screen_adver_panel)
    self.start_screen_adver_label_machineid_verify.clicked.connect(lambda: start_screen_adver_label_machineid_verify_clicked(self))
    self.start_screen_adver_label_machineid_verify.setObjectName('button')
    self.start_screen_adver_label_machineid_verify.setStyleSheet('QPushButton {border-right:0}')

    self.start_screen_adver_label_machineid_register = QPushButton('REGISTER', parent=self.start_screen_adver_panel)
    self.start_screen_adver_label_machineid_register.clicked.connect(lambda: start_screen_adver_label_machineid_register_clicked(self))
    self.start_screen_adver_label_machineid_register.setObjectName('button_dark')
    self.start_screen_adver_label_machineid_register.setStyleSheet('QPushButton {border-left:0}')

    def thread_verify_user_and_machineid_ended(command):
        text = ''

        self.settings['authentication']['last_checked'] = datetime.now().strftime("%Y%m%d%H%M%S")
        if command.get('is_valid', False):
            text = 'You can use Subtitld Advanced features until ' + command['expiry_date'] + str('.')
            if command.get('authentication_keys', '') and command['authentication_keys'].get(ACTUAL_OS, ''):
                authentication.append_authentication_keys(config=self.settings, dict=command['authentication_keys'][ACTUAL_OS])
            self.advanced_mode = True
        else:
            text = 'You cannot use Subtitld Advanced features. Click on Register for more information.'
        text = text + str(str('<br><small style="color:#3e5363;" >LAST CHECKED: ' + datetime.strptime(self.settings['authentication']['last_checked'], '%Y%m%d%H%M%S').strftime("%d/%m/%Y - %H:%M:%S")) if self.settings['authentication'].get('last_checked', '') else str(''))
        self.start_screen_adver_label_status.setText(text)

        if command.get('register_url', ''):
            self.settings['authentication']['register_url'] = command['register_url']

    self.thread_verify_user_and_machineid = thread_verify_user_and_machineid(self)
    self.thread_verify_user_and_machineid.command.connect(thread_verify_user_and_machineid_ended)

    update_start_screen_adver_panel(self)


def resized(self):
    self.start_screen.setGeometry(0, self.height()-200, self.width(), 200)
    self.start_screen_recentfiles_background.setGeometry((self.start_screen.width()*.5)-175, 0, 350, self.start_screen.height())
    self.start_screen_top_shadow.setGeometry(0, 0, self.start_screen.width(), 150)
    self.start_screen_open_label.setGeometry(0, 20, (self.start_screen.width()*.5)-195, 20)
    self.start_screen_recent_label.setGeometry((self.start_screen.width()*.5)-175, 20, 350, 20)

    self.start_screen_open_button.setGeometry((self.start_screen.width()*.5)-195-200, 50, 200, 40)
    self.start_screen_recent_listwidget.setGeometry((self.start_screen.width()*.5)-155, 50, 310, self.start_screen.height()-50-20)
    self.start_screen_recent_alert.setGeometry((self.start_screen.width()*.5)-155, 50, 310, self.start_screen.height()-50-20)
    self.start_screen_adver_label.setGeometry((self.start_screen.width()*.5)+195, 20, self.start_screen_adver_panel.width(), 20)

    self.start_screen_adver_holder.setGeometry((self.start_screen.width()*.5)+195, 30, self.start_screen.width() - ((self.start_screen.width()*.5)+195), self.start_screen.height()-20)
    self.start_screen_adver_label_details.setGeometry(0, 20, self.start_screen_adver_holder.width(),  self.start_screen_adver_holder.height())
    self.start_screen_adver_label_show_machineid_button.setGeometry(self.start_screen_adver_label_details.x(),  self.start_screen_adver_label_details.y(),  200,  40)
    s = [600, 300]
    self.start_screen_adver_panel.setGeometry((self.start_screen.width()*.5)-(s[0]*.5), ((self.height()-200)*.5)-(s[1]*.5), s[0], s[1])
    self.start_screen_adver_panel_label.setGeometry(0, 0, self.start_screen_adver_panel.width(), 50)
    self.start_screen_adver_label_machineid_label.setGeometry(0, 50, self.start_screen_adver_panel.width(),  20)
    self.start_screen_adver_label_machineid.setGeometry(0, 70, self.start_screen_adver_panel.width(),  40)
    self.start_screen_adver_label_email_label.setGeometry(40, 110, self.start_screen_adver_panel.width()-80,  30)
    self.start_screen_adver_label_email.setGeometry(40, 140, self.start_screen_adver_panel.width()-80,  40)
    self.start_screen_adver_label_machineid_copy.setGeometry((self.start_screen_adver_label_machineid.width()*.5)-50, 5, 100,  30)
    self.start_screen_adver_label_status.setGeometry(0, 180, self.start_screen_adver_panel.width(), 60)
    self.start_screen_adver_label_machineid_verify.setGeometry((self.start_screen_adver_panel.width()*.5)-140, 240, 100, 40)
    self.start_screen_adver_label_machineid_register.setGeometry((self.start_screen_adver_panel.width()*.5)-40, 240, 180, 40)


def show(self):
    if self.settings['recent_files']:
        self.start_screen_recent_alert.setVisible(False)
        hist_list = []
        for filename in self.settings['recent_files'].keys():
            hist_list.append([self.settings['recent_files'][filename], filename])

        for date in reversed(sorted(hist_list)):
            self.start_screen_recent_listwidget.addItem(date[1])
    else:
        self.start_screen_recent_listwidget.setVisible(False)
    self.generate_effect(self.start_screen_transparency_animation, 'opacity', 2000, 0.0, 1.0)


def hide(self):
    self.generate_effect(self.start_screen_transparency_animation, 'opacity', 200, 1.0, 0.0)
    self.generate_effect(self.background_label2_transparency_animation, 'opacity', 500, 1.0, 0.0)


def start_screen_adver_label_email_editing_finished(self):
    if self.start_screen_adver_label_email.text():
        self.settings['authentication']['email'] = self.start_screen_adver_label_email.text()
    update_start_screen_adver_panel(self)


def start_screen_open_button_clicked(self):
    file_io.open_filepath(self)


def start_screen_recent_listwidget_item_clicked(self):
    file_to_open = self.start_screen_recent_listwidget.currentItem().text()
    file_io.open_filepath(self, file_to_open)


def start_screen_adver_label_show_machineid_button_clicked(self):
    update_start_screen_adver_panel(self)


def update_start_screen_adver_panel(self):
    self.start_screen_adver_panel.setVisible(self.start_screen_adver_label_show_machineid_button.isChecked())
    update_start_screen_adver_label_machineid_verify(self)


def update_start_screen_adver_label_machineid_verify(self):
    self.start_screen_adver_label_machineid_verify.setEnabled(bool('@' in self.start_screen_adver_label_email.text() and len(self.start_screen_adver_label_email.text().split('@', 1)[0]) > 0 and len(self.start_screen_adver_label_email.text().split('@', 1)[1].split('.')) > 1 and len(self.start_screen_adver_label_email.text().split('@', 1)[1].split('.', 1)[0]) > 1 and len(self.start_screen_adver_label_email.text().split('@', 1)[1].split('.', 1)[1]) > 1))


def start_screen_adver_label_machineid_copy_clicked(self):
    QApplication.clipboard().setText(self.start_screen_adver_label_machineid.text())


def start_screen_adver_label_machineid_verify_clicked(self):
    self.thread_verify_user_and_machineid.email = self.start_screen_adver_label_email.text()
    self.thread_verify_user_and_machineid.machine_id = self.start_screen_adver_label_machineid.text()
    self.thread_verify_user_and_machineid.start()
    self.start_screen_adver_label_status.setText('<small style="color:#3e5363;" >Verifying...</small>')


def start_screen_adver_label_machineid_register_clicked(self):
    webbrowser.open(self.settings['authentication'].get('register_url', 'https://subtitld.jonata.org/'))
