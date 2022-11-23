import os
import sys
from datetime import datetime
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QPushButton, QLabel, QGraphicsOpacityEffect, QListWidget, QListWidgetItem
from PySide6.QtCore import QPropertyAnimation, Qt, QSize

from subtitld.modules import file_io
from subtitld.modules.paths import PATH_SUBTITLD_DATA_THUMBNAILS, VERSION_NUMBER
from subtitld.interface.translation import _


def load(self):
    """Function to load all starting screen widgets"""
    self.start_screen = QLabel(parent=self)
    self.start_screen.setObjectName('start_screen')
    self.start_screen_transparency = QGraphicsOpacityEffect()
    self.start_screen.setGraphicsEffect(self.start_screen_transparency)
    self.start_screen_transparency_animation = QPropertyAnimation(self.start_screen_transparency, b'opacity')
    self.start_screen_transparency.setOpacity(0)

    self.start_screen_recentfiles_background = QLabel(parent=self.start_screen)
    self.start_screen_recentfiles_background.setObjectName('start_screen_recentfiles_background')
    self.start_screen_recentfiles_background.setAutoFillBackground(True)

    self.start_screen_top_shadow = QLabel(parent=self.start_screen)
    self.start_screen_top_shadow.setObjectName('start_screen_top_shadow')

    self.start_screen_open_label = QLabel(parent=self.start_screen)
    self.start_screen_open_label.setAlignment(Qt.AlignRight)
    self.start_screen_open_label.setObjectName('start_screen_open_label')

    self.start_screen_open_button = QPushButton(parent=self.start_screen)
    self.start_screen_open_button.clicked.connect(lambda: start_screen_open_button_clicked(self))
    self.start_screen_open_button.setProperty('class', 'button_dark')

    self.start_screen_recent_label = QLabel(parent=self.start_screen)
    self.start_screen_recent_label.setAlignment(Qt.AlignCenter)
    self.start_screen_recent_label.setObjectName('start_screen_recent_label')

    self.start_screen_recent_listwidget = QListWidget(parent=self.start_screen)
    self.start_screen_recent_listwidget.setObjectName('start_screen_recent_listwidget')
    self.start_screen_recent_listwidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    self.start_screen_recent_listwidget.setFocusPolicy(Qt.NoFocus)
    self.start_screen_recent_listwidget.currentItemChanged.connect(lambda item: start_screen_recent_listwidget_item_changed(self, item))
    self.start_screen_recent_listwidget.itemDoubleClicked.connect(lambda: start_screen_recent_listwidget_item_clicked(self))

    self.start_screen_recent_alert = QLabel(parent=self.start_screen)
    self.start_screen_recent_alert.setWordWrap(True)
    self.start_screen_recent_alert.setObjectName('start_screen_recent_alert')

    self.start_screen_adver_label = QLabel(parent=self.start_screen)
    self.start_screen_adver_label.setObjectName('start_screen_adver_label')

    self.start_screen_adver_label_details = QLabel(parent=self.start_screen)
    self.start_screen_adver_label_details.setObjectName('start_screen_adver_label_details')

    self.start_screen_temp_recent_files_list = []


def resized(self):
    """Function to call when starting screen is resized"""
    self.start_screen.setGeometry(0, self.height() - 200, self.width(), 200)
    self.start_screen_recentfiles_background.setGeometry(int((self.start_screen.width() * .5) - 175), 0, 350, self.start_screen.height())
    self.start_screen_top_shadow.setGeometry(0, 0, self.start_screen.width(), 150)
    self.start_screen_open_label.setGeometry(0, 20, int((self.start_screen.width() * .5) - 195), 20)
    self.start_screen_recent_label.setGeometry(int((self.start_screen.width() * .5) - 175), 20, 350, 20)

    self.start_screen_open_button.setGeometry(int((self.start_screen.width() * .5) - 195 - 200), 50, 200, 40)
    self.start_screen_recent_listwidget.setGeometry(int((self.start_screen.width() * .5) - 155), 50, 310, self.start_screen.height() - 50 - 20)
    self.start_screen_recent_alert.setGeometry(int((self.start_screen.width() * .5) - 155), 50, 310, self.start_screen.height() - 50 - 20)

    self.start_screen_adver_label.setGeometry(int((self.start_screen.width() * .5) + 195), 20, int((self.start_screen.width() - ((self.start_screen.width() * .5) + 195))), 20)
    self.start_screen_adver_label_details.setGeometry(int((self.start_screen.width() * .5) + 195), 50, int((self.start_screen.width() - ((self.start_screen.width() * .5) + 195))), self.start_screen.height() - 50 - 20)


def show(self):
    """Function to show starting panel"""
    if self.settings['recent_files']:
        delete = [item for item in self.settings['recent_files'] if isinstance(self.settings['recent_files'][item], str)]

        for item in delete:
            del self.settings['recent_files'][item]

        inv_rf = {v['last_opened']: k for k, v in self.settings['recent_files'].items()}
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
    # self.start_screen_thumbnail_background.setVisible(False)
    # self.generate_effect(self.player_widget_animation, 'geometry', 1000, [self.start_screen_thumbnail_background.x(), self.start_screen_thumbnail_background.y(), self.start_screen_thumbnail_background.width(), self.start_screen_thumbnail_background.height()], [self.player_widget.x(), self.player_widget.y(), self.player_widget.width(), self.player_widget.height()])
    # self.generate_effect(self.player_widget_transparency_animation, 'opacity', 1000, 0.0, 1.0)
    # self.generate_effect(self.layer_player_vbox_animation, 'contentsMargins', 1000, self.layer_player_vbox.contentsMargins(), [300, 0, 0, 200])


def start_screen_recent_listwidget_item_changed(self, item):
    file_to_open = self.start_screen_temp_recent_files_list[self.start_screen_recent_listwidget.currentRow()][-1]
    # print(self.settings['recent_files'][file_to_open])
    thumbnail_image_path = os.path.join(PATH_SUBTITLD_DATA_THUMBNAILS, self.settings['recent_files'][file_to_open].get('video_hash', '') + '.png')

    if os.path.isfile(thumbnail_image_path) and self.settings['recent_files'][file_to_open].get('video_filepath', False) and os.path.isfile(self.settings['recent_files'][file_to_open]['video_filepath']):
        self.start_screen_thumbnail_background.setPixmap(QPixmap(thumbnail_image_path).scaled(self.start_screen_thumbnail_background.width(), self.start_screen_thumbnail_background.height(), Qt.KeepAspectRatioByExpanding))
        self.generate_effect(self.start_screen_thumbnail_background_transparency_animation, 'opacity', 800, 0.0, 1.0)
    else:
        self.start_screen_thumbnail_background.clear()

    # print(self.settings['recent_files'][file_to_open])


def translate_widgets(self):
    self.start_screen_open_label.setText(_('startscreen.open_subtitle_or_video'))
    self.start_screen_open_button.setText(_('startscreen.open'))
    self.start_screen_recent_label.setText(_('startscreen.recent_subitles'))
    self.start_screen_recent_alert.setText(_('startscreen.no_recent_file_history'))
    self.start_screen_adver_label.setText((_('startscreen.version_number').format(VERSION_NUMBER)))
    self.start_screen_adver_label_details.setText(_('startscreen.visit_website'))