"""starting screen module

"""

import os
import sys
from datetime import datetime
from PyQt5.QtWidgets import QPushButton, QLabel, QGraphicsOpacityEffect, QListWidget, QListWidgetItem
from PyQt5.QtCore import QPropertyAnimation, Qt, QSize

from subtitld.modules import file_io
from subtitld.modules.paths import VERSION_NUMBER


def load(self):
    """Function to load all starting screen widgets"""
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

    self.start_screen_open_label = QLabel(self.tr('Open a subtitle or a video').upper(), parent=self.start_screen)
    self.start_screen_open_label.setObjectName('start_screen_open_label')

    self.start_screen_open_button = QPushButton(self.tr('Open').upper(), parent=self.start_screen)
    self.start_screen_open_button.clicked.connect(lambda: start_screen_open_button_clicked(self))
    self.start_screen_open_button.setObjectName('button_dark')

    self.start_screen_recent_label = QLabel(self.tr('Recent subtitles').upper(), parent=self.start_screen)
    self.start_screen_recent_label.setObjectName('start_screen_recent_label')

    self.start_screen_recent_listwidget = QListWidget(parent=self.start_screen)
    self.start_screen_recent_listwidget.setObjectName('start_screen_recent_listwidget')
    self.start_screen_recent_listwidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    self.start_screen_recent_listwidget.setFocusPolicy(Qt.NoFocus)
    self.start_screen_recent_listwidget.itemDoubleClicked.connect(lambda: start_screen_recent_listwidget_item_clicked(self))

    self.start_screen_recent_alert = QLabel(self.tr('There is no recent file history.'), parent=self.start_screen)
    self.start_screen_recent_alert.setWordWrap(True)
    self.start_screen_recent_alert.setObjectName('start_screen_recent_alert')

    self.start_screen_adver_label = QLabel(parent=self.start_screen)
    self.start_screen_adver_label.setObjectName('start_screen_adver_label')
    self.start_screen_adver_label.setText(self.tr('Version {}'.format(VERSION_NUMBER)).upper())

    self.start_screen_adver_label_details = QLabel(parent=self.start_screen)
    self.start_screen_adver_label_details.setObjectName('start_screen_adver_label_details')
    self.start_screen_adver_label_details.setText(self.tr('Visit <b>subtitld.jonata.org</b> for<br>more information.'))

    self.start_screen_temp_recent_files_list = []


def resized(self):
    """Function to call when starting screen is resized"""
    self.start_screen.setGeometry(0, self.height()-200, self.width(), 200)
    self.start_screen_recentfiles_background.setGeometry((self.start_screen.width()*.5)-175, 0, 350, self.start_screen.height())
    self.start_screen_top_shadow.setGeometry(0, 0, self.start_screen.width(), 150)
    self.start_screen_open_label.setGeometry(0, 20, (self.start_screen.width()*.5)-195, 20)
    self.start_screen_recent_label.setGeometry((self.start_screen.width()*.5)-175, 20, 350, 20)

    self.start_screen_open_button.setGeometry((self.start_screen.width()*.5)-195-200, 50, 200, 40)
    self.start_screen_recent_listwidget.setGeometry((self.start_screen.width()*.5)-155, 50, 310, self.start_screen.height()-50-20)
    self.start_screen_recent_alert.setGeometry((self.start_screen.width()*.5)-155, 50, 310, self.start_screen.height()-50-20)

    self.start_screen_adver_label.setGeometry((self.start_screen.width()*.5)+195, 20, (self.start_screen.width()-((self.start_screen.width()*.5)+195)), 20)
    self.start_screen_adver_label_details.setGeometry((self.start_screen.width()*.5)+195, 50, (self.start_screen.width()-((self.start_screen.width()*.5)+195)),  self.start_screen.height()-50-20)


def show(self):
    """Function to show starting panel"""
    if self.settings['recent_files']:
        inv_rf = {v: k for k, v in self.settings['recent_files'].items()}
        for item in reversed(sorted(inv_rf)):
            if os.path.isfile(inv_rf[item]):
                for filename in self.start_screen_temp_recent_files_list:
                    if inv_rf[item] == filename[-1]:
                        continue
                iteml = QListWidgetItem()
                iteml.setSizeHint(QSize(iteml.sizeHint().width(), 42))
                if len(item) < 12:
                    lastopened = datetime.strptime(item, '%Y%m%d').strftime('%d/%m/%Y') + ' - '
                else:
                    lastopened = datetime.strptime(item, '%Y%m%d%H%M%S').strftime('%d/%m/%Y - %H:%M:%S') + ' - '
                path = inv_rf[item]
                if (sys.platform == 'win32' or os.name == 'nt'):
                    path = path.replace('/', '\\')
                label = QLabel('<font style="font-size:12px; color:#6a7483;">' + os.path.basename(inv_rf[item]) + '</font><br><font style="font-size:10px; color:#3e5363;">' + lastopened + path.replace('\\\\', '\\') + '</font>')
                label.setStyleSheet('QLabel {padding:1px}')

                self.start_screen_temp_recent_files_list.append([iteml, label, inv_rf[item]])

    if self.start_screen_temp_recent_files_list:
        for item in self.start_screen_temp_recent_files_list:
            self.start_screen_recent_listwidget.addItem(item[0])
            self.start_screen_recent_listwidget.setItemWidget(item[0], item[1])
        self.start_screen_recent_alert.setVisible(False)
    else:
        self.start_screen_recent_listwidget.setVisible(False)
    self.generate_effect(self.start_screen_transparency_animation, 'opacity', 2000, 0.0, 1.0)


def hide(self):
    """Function to hide starting panel"""
    self.generate_effect(self.start_screen_transparency_animation, 'opacity', 200, 1.0, 0.0)
    self.generate_effect(self.background_label2_transparency_animation, 'opacity', 500, 1.0, 0.0)


def start_screen_open_button_clicked(self):
    """Function to call when the open subtitle/video button of starting screen is clicked"""
    file_io.open_filepath(self, update_interface=True)


def start_screen_recent_listwidget_item_clicked(self):
    """Function to call when item on recent files list is clicked"""
    files_to_open = [self.start_screen_temp_recent_files_list[self.start_screen_recent_listwidget.currentRow()][-1]]
    file_io.open_filepath(self, files_to_open=files_to_open, update_interface=True)
