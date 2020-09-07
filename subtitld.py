#!/usr/bin/python3

import os
import sys
import time
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QLabel, QGraphicsOpacityEffect, QMessageBox
from PyQt5.QtGui import QIcon, QFont, QFontDatabase
from PyQt5.QtCore import Qt, QRect, QPropertyAnimation, QTranslator

from modules.paths import PATH_LOCALE, PATH_SUBTITLD_GRAPHICS, PATH_SUBTITLD_USER_CONFIG_FILE, ACTUAL_OS, LIST_OF_SUPPORTED_SUBTITLE_EXTENSIONS, LIST_OF_SUPPORTED_VIDEO_EXTENSIONS
from modules.history import history_redo, history_undo
from modules import config
from modules import authentication

if ACTUAL_OS == 'darwin':
    from modules.paths import NSURL

list_of_supported_subtitle_extensions = []
for type in LIST_OF_SUPPORTED_SUBTITLE_EXTENSIONS.keys():
    for ext in LIST_OF_SUPPORTED_SUBTITLE_EXTENSIONS[type]['extensions']:
        list_of_supported_subtitle_extensions.append(ext)
list_of_supported_subtitle_extensions = tuple(list_of_supported_subtitle_extensions)

class subtitld(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Subtitld')
        self.setWindowIcon(QIcon(os.path.join(PATH_SUBTITLD_GRAPHICS, 'subtitld.png')))
        self.setAcceptDrops(True)

        # Setting some default values
        self.update_accuracy = 200
        self.subtitles_list = []
        self.video_metadata = {}

        self.actual_subtitle_file = ''
        self.actual_video_file = ''

        self.selected_subtitle = False
        self.mediaplayer_zoom = 100.0
        self.video_waveformsize = .7
        self.mediaplayer_opacity = .5
        self.video_length = 0.01
        self.mediaplayer_current_position = 0.0
        self.mediaplayer_view_mode = 'verticalform'
        self.timeline_snap = True
        self.timeline_snap_value = .1
        self.timeline_snap_limits = True
        self.timeline_snap_moving = True
        self.timeline_snap_grid = False
        self.minimum_subtitle_width = 1
        self.timeline_show_grid = False
        self.timeline_grid_type = False
        self.playback_speed = 1.0
        self.default_new_subtitle_duration = 5.0
        self.repeat_duration = 5.0
        self.repeat_duration_tmp = []
        self.repeat_times = 3
        self.repeat_activated = False
        self.unsaved = False
        self.format_to_save = 'SRT'
        self.selected_language = 'en'

        self.settings = config.load(PATH_SUBTITLD_USER_CONFIG_FILE)

        self.machine_id = authentication.get_machine_id()

        self.advanced_mode = authentication.check_authentication(auth_dict=self.settings['authentication'].get('codes', {}).get(ACTUAL_OS, {}), email=self.settings['authentication'].get('email', ''), machineid=self.machine_id)

        self.background_label = QLabel(self)
        self.background_label.setObjectName('background_label')

        self.background_label2 = QLabel(self)
        self.background_label2.setObjectName('background_label2')
        self.background_label2_transparency = QGraphicsOpacityEffect()
        self.background_label2.setGraphicsEffect(self.background_label2_transparency)
        self.background_label2_transparency_animation = QPropertyAnimation(self.background_label2_transparency, b'opacity')

        # Setting the gorgeous watermarked background logo
        self.background_watermark_label = QLabel(self)
        self.background_watermark_label.setObjectName('background_watermark_label')

        # I have placed all the stylesheet properties into a separate file, so importing it here
        from modules import stylesheet
        stylesheet.set_stylesheet(self)

        # The file io system
        from modules import file_io
        self.file_io = file_io
        self.file_io.load(self)

        # The start screen
        from modules import startscreen
        self.startscreen = startscreen
        self.startscreen.load(self)
        self.startscreen.show(self)

        # The mpv video player
        from modules import player
        self.player = player
        self.player.load(self)

        from modules import global_subtitlesvideo_panel
        self.global_subtitlesvideo_panel = global_subtitlesvideo_panel
        self.global_subtitlesvideo_panel.load(self, PATH_SUBTITLD_GRAPHICS)

        from modules import subtitleslist
        self.subtitleslist = subtitleslist
        self.subtitleslist.load(self, PATH_SUBTITLD_GRAPHICS)

        from modules import global_properties_panel
        self.global_properties_panel = global_properties_panel
        self.global_properties_panel.load(self, PATH_SUBTITLD_GRAPHICS)

        from modules import properties
        self.properties = properties
        self.properties.load(self, PATH_SUBTITLD_GRAPHICS)

        from modules import timeline
        self.timeline = timeline

        from modules import playercontrols
        self.playercontrols = playercontrols
        self.playercontrols.load(self, PATH_SUBTITLD_GRAPHICS)

        self.setGeometry(0, 0, QDesktopWidget().screenGeometry().width(), QDesktopWidget().screenGeometry().height())

        self.subtitleslist.update_subtitles_list_widget(self)
        self.properties.update_properties_widget(self)
        self.player.update(self)

        from modules import shortcuts
        self.shortcuts = shortcuts
        self.shortcuts.load(self, self.settings['shortcuts'])

    def dragEnterEvent(widget, event):
        if event.mimeData().hasUrls and len(event.mimeData().urls()) > 0:
            if sys.platform == 'darwin':
                filename = str(NSURL.alloc().initWithString_(event.mimeData().urls()[0].toString()).fileSystemRepresentation())
            else:
                filename = event.mimeData().urls()[0].toLocalFile()

            if filename.lower().endswith(('.subtitld')) or filename.lower().endswith(list_of_supported_subtitle_extensions) or filename.lower().endswith(LIST_OF_SUPPORTED_VIDEO_EXTENSIONS):
                event.accept()

    def dropEvent(widget, event):
        if sys.platform == 'darwin':
            filename = str(NSURL.alloc().initWithString_(event.mimeData().urls()[0].toString()).fileSystemRepresentation())
        else:
            filename = event.mimeData().urls()[0].toLocalFile()

        if filename.lower().endswith(('.subtitld')) or filename.lower().endswith(list_of_supported_subtitle_extensions) or filename.lower().endswith(LIST_OF_SUPPORTED_VIDEO_EXTENSIONS):
            if filename.lower().endswith(('.subtitld')):
                authentication.append_authentication_keys(config=widget.settings, dict=authentication.load_subtitld_codes_file(path=filename))
            else:
                widget.file_io.open_filepath(widget, file_to_open=filename)
            event.accept()

    def resizeEvent(self, event):
        self.background_label.setGeometry(0, 0, self.width(), self.height())
        self.background_label2.setGeometry(0, 0, self.width(), self.height())

        self.startscreen.resized(self)
        self.subtitleslist.resized(self)
        self.properties.resized(self)

        self.global_subtitlesvideo_panel.resized(self)
        self.global_properties_panel.resized(self)

        self.playercontrols.resized(self)

        self.background_watermark_label.setGeometry(int((self.width()*.5)-129), int(((self.height()-self.playercontrols_widget.height())*.5)-129), 258, 258)

        self.player.resized(self)
        self.timeline.resized(self)

    def closeEvent(self, event):
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
                self.subtitleslist.toppanel_save_button_clicked(self)

        config.save(self.settings, PATH_SUBTITLD_USER_CONFIG_FILE)
        self.thread_get_waveform.quit()
        self.thread_extract_waveform.quit()
        self.player_widget.close()
        time.sleep(.1)
        event.accept()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space:
            self.player_widget.pause()
            self.playercontrols_playpause_button.setChecked(not self.playercontrols_playpause_button.isChecked())
            self.playercontrols.playercontrols_playpause_button_update(self)

        if event.key() == Qt.Key_F1:
            self.playercontrols.add_subtitle_button_clicked(self)

        if event.key() == Qt.Key_F12:
            self.playercontrols.add_subtitle_button_clicked(self)

        if event.key() == Qt.Key_Z:
            if event.modifiers() == Qt.ControlModifier | Qt.ShiftModifier:
                history_redo(actual_subtitles=self.subtitles_list)
            elif event.modifiers() == Qt.ControlModifier:
                history_undo(actual_subtitles=self.subtitles_list)
            self.selected_subtitle = False
            self.subtitleslist.update_subtitles_list_qlistwidget(self)
            self.properties.update_properties_widget(self)
            self.timeline.update(self)

        if event.key() == Qt.Key_Left:
            self.player_widget.frameBackStep()

        if event.key() == Qt.Key_Right:
            self.player_widget.frameStep()

    def live_recording_note_thread_updated(self, result):
        self.recording_note = result

    def generate_effect(self, widget, effect_type, duration, startValue, endValue):
        widget.setDuration(duration)
        if effect_type == 'geometry':
            widget.setStartValue(QRect(startValue[0], startValue[1], startValue[2], startValue[3]))
            widget.setEndValue(QRect(endValue[0], endValue[1], endValue[2], endValue[3]))
        elif effect_type == 'opacity':
            widget.setStartValue(startValue)
            widget.setEndValue(endValue)
        widget.start()


def edit_syllable_returnpressed(self):
    self.lyrics_notes[self.lyrics_notes.index(self.selected_note)][3] = self.player_controls.edit_sylable.text()
    self.timeline_widget.update()


def viewnotesin_button_clicked(self):
    if self.mediaplayer_viewnotes[0] + 1 < 29 and self.mediaplayer_viewnotes[-1] - 1 > -29:
        self.mediaplayer_viewnotes.insert(0, self.mediaplayer_viewnotes[0] + 1)
        self.mediaplayer_viewnotes.append(self.mediaplayer_viewnotes[-1] - 1)
    self.timeline_widget.update()


def viewnotesout_button_clicked(self):
    if len(self.mediaplayer_viewnotes) > 2:
        del self.mediaplayer_viewnotes[0]
        del self.mediaplayer_viewnotes[-1]
    self.timeline_widget.update()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    if os.path.isfile(os.path.join(PATH_LOCALE, 'en_US.qm')):
        translator = QTranslator()
        translator.load(os.path.join(PATH_LOCALE, 'en_US.qm'))
        app.installTranslator(translator)
    # app.setDesktopSettingsAware(False)
    app.setStyle("plastique")
    app.setApplicationName("Subtitld")

    font_database = QFontDatabase()
    font_database.addApplicationFont(os.path.join(PATH_SUBTITLD_GRAPHICS, 'Ubuntu-B.ttf'))
    font_database.addApplicationFont(os.path.join(PATH_SUBTITLD_GRAPHICS, 'Ubuntu-BI.ttf'))
    font_database.addApplicationFont(os.path.join(PATH_SUBTITLD_GRAPHICS, 'Ubuntu-C.ttf'))
    font_database.addApplicationFont(os.path.join(PATH_SUBTITLD_GRAPHICS, 'Ubuntu-L.ttf'))
    font_database.addApplicationFont(os.path.join(PATH_SUBTITLD_GRAPHICS, 'Ubuntu-LI.ttf'))
    font_database.addApplicationFont(os.path.join(PATH_SUBTITLD_GRAPHICS, 'Ubuntu-M.ttf'))
    font_database.addApplicationFont(os.path.join(PATH_SUBTITLD_GRAPHICS, 'Ubuntu-MI.ttf'))
    font_database.addApplicationFont(os.path.join(PATH_SUBTITLD_GRAPHICS, 'UbuntuMono-B.ttf'))
    font_database.addApplicationFont(os.path.join(PATH_SUBTITLD_GRAPHICS, 'UbuntuMono-BI.ttf'))
    font_database.addApplicationFont(os.path.join(PATH_SUBTITLD_GRAPHICS, 'UbuntuMono-R.ttf'))
    font_database.addApplicationFont(os.path.join(PATH_SUBTITLD_GRAPHICS, 'UbuntuMono-RI.ttf'))
    font_database.addApplicationFont(os.path.join(PATH_SUBTITLD_GRAPHICS, 'Ubuntu-R.ttf'))
    font_database.addApplicationFont(os.path.join(PATH_SUBTITLD_GRAPHICS, 'Ubuntu-RI.ttf'))
    font_database.addApplicationFont(os.path.join(PATH_SUBTITLD_GRAPHICS, 'Ubuntu-Th.ttf'))

    app.setFont(QFont('Ubuntu', 10))
    app.main = subtitld()
    app.main.show()

    sys.exit(app.exec_())
