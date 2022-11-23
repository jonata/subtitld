import os
import sys
import datetime
import argparse
import locale

from PySide6.QtWidgets import QApplication, QWidget, QLabel, QGraphicsOpacityEffect, QMessageBox
from PySide6.QtGui import QIcon, QFont, QFontDatabase
from PySide6.QtCore import Qt, QRect, QPropertyAnimation, QTimer

from subtitld.modules import config, file_io
from subtitld.modules.history import history_redo, history_undo
from subtitld.modules.paths import PATH_SUBTITLD_DATA_THUMBNAILS, PATH_SUBTITLD_GRAPHICS, PATH_SUBTITLD_USER_CONFIG_FILE, ACTUAL_OS, LIST_OF_SUPPORTED_SUBTITLE_EXTENSIONS, LIST_OF_SUPPORTED_VIDEO_EXTENSIONS, PATH_SUBTITLD_DATA_BACKUP
from subtitld.interface import translation, startscreen

from subtitld import resources_rc

if ACTUAL_OS == 'darwin':
    from subtitld.modules.paths import NSURL

list_of_supported_subtitle_extensions = []
for t in LIST_OF_SUPPORTED_SUBTITLE_EXTENSIONS:
    for ext in LIST_OF_SUPPORTED_SUBTITLE_EXTENSIONS[t]['extensions']:
        list_of_supported_subtitle_extensions.append(ext)
list_of_supported_subtitle_extensions = tuple(list_of_supported_subtitle_extensions)

parser = argparse.ArgumentParser(description='Subtitld is a software to create, edit and transcribe subtitles')
parser.add_argument('file', type=argparse.FileType('r'), help='The path for video or subtitle file', nargs='*', default=False)
parser.add_argument('--version', help='Prints the actual version of Subtitld.', action='store_true')
args = parser.parse_args()


class Subtitld(QWidget):
    """The main window (QWidget) class"""
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon(":/graphics/subtitld.png"))
        self.setAcceptDrops(True)

        self.setMinimumSize(860, 450)

        # Setting some default values
        self.update_accuracy = 200
        self.subtitles_list = []
        self.video_metadata = {}

        self.actual_subtitle_file = ''
        self.actual_video_file = ''

        self.settings = config.load(PATH_SUBTITLD_USER_CONFIG_FILE)

        translation.load_translation_files()
        translation.set_language(self.settings.get('interface', {}).get('language', locale.getdefaultlocale()[0]))

        self.selected_subtitle = False
        self.mediaplayer_zoom = 100.0
        self.video_waveformsize = .7
        self.mediaplayer_opacity = .5
        self.video_length = 0.01
        self.playback_speed = 1.0
        self.default_new_subtitle_duration = 5.0
        self.repeat_duration = 5.0
        self.repeat_duration_tmp = []
        self.repeat_times = 3
        self.repeat_activated = False
        self.unsaved = False
        self.format_to_save = 'SRT'
        self.selected_language = 'en'
        self.subtitles_panel_width_proportion = .3

        self.background_label = QLabel(self)
        self.background_label.setObjectName('background_label')

        self.start_screen_thumbnail_background = QLabel(parent=self)
        self.start_screen_thumbnail_background.setAlignment(Qt.AlignCenter)
        # self.start_screen_thumbnail_background.setScaledContents(True)
        self.start_screen_thumbnail_background_transparency = QGraphicsOpacityEffect()
        self.start_screen_thumbnail_background.setGraphicsEffect(self.start_screen_thumbnail_background_transparency)
        self.start_screen_thumbnail_background_transparency_animation = QPropertyAnimation(self.start_screen_thumbnail_background_transparency, b'opacity')
        # self.start_screen_thumbnail_background_transparency_animation.setEasingCurve(QEasingCurve.InExpo)
        self.start_screen_thumbnail_background_transparency.setOpacity(1)
        # self.start_screen_thumbnail_background_animation = QPropertyAnimation(self.start_screen_thumbnail_background, b'geometry')
        # self.start_screen_thumbnail_background_animation.setEasingCurve(QEasingCurve.OutCirc)

        self.background_label2 = QLabel(self)
        self.background_label2.setObjectName('background_label2')
        self.background_label2_transparency = QGraphicsOpacityEffect()
        self.background_label2.setGraphicsEffect(self.background_label2_transparency)
        self.background_label2_transparency_animation = QPropertyAnimation(self.background_label2_transparency, b'opacity')
        self.background_label2_transparency.setOpacity(1)

        # Setting the gorgeous watermarked background logo
        self.background_watermark_label = QLabel(self)
        self.background_watermark_label.setObjectName('background_watermark_label')

        # All the stylesheet properties are in a separate file, so importing it here
        self.setStyleSheet(open(os.path.join(PATH_SUBTITLD_GRAPHICS, 'stylesheet.qss')).read())

        # The file io system
        self.file_io = file_io
        self.file_io.load(self)

        # if ACTUAL_OS == 'windows':
        #     # The windows update system
        #     from modules import update
        #     self.update = update
        #     self.update.load(self)

        # The start screen
        self.startscreen = startscreen
        self.startscreen.load(self)
        self.startscreen.show(self)

        # The mpv video player
        from subtitld.interface import player
        self.player = player
        self.player.load(self)

        from subtitld.interface import global_panel
        self.global_panel = global_panel
        self.global_panel.load(self)

        from subtitld.interface import subtitles_panel
        self.subtitles_panel = subtitles_panel
        self.subtitles_panel.load(self)

        from subtitld.interface import timeline
        self.timeline = timeline

        from subtitld.interface import playercontrols
        self.playercontrols = playercontrols
        self.playercontrols.load(self)

        self.player.update(self)

        from subtitld.modules import shortcuts
        self.shortcuts = shortcuts
        self.shortcuts.load(self, self.settings['shortcuts'])

        self.autosave_timer = QTimer(self)
        self.autosave_timer.setInterval(int(self.settings['autosave'].get('interval', 300000)))
        self.autosave_timer.timeout.connect(lambda: autosave_timer_timeout(self))

        self.translate_widgets()

        # Maybe implement saving window position...? Useful?
        # self.setGeometry(0, 0, QDesktopWidget().screenGeometry().width(), QDesktopWidget().screenGeometry().height())
        self.showMaximized()
        # self.setFixedSize(QSize(1280, 720))

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls and len(event.mimeData().urls()) > 0:
            if sys.platform == 'darwin':
                filename = str(NSURL.alloc().initWithString_(event.mimeData().urls()[0].toString()).fileSystemRepresentation())
            else:
                filename = event.mimeData().urls()[0].toLocalFile()

            if filename.lower().endswith(('.subtitld')) or filename.lower().endswith(list_of_supported_subtitle_extensions) or filename.lower().endswith(LIST_OF_SUPPORTED_VIDEO_EXTENSIONS):
                event.accept()

    def dropEvent(self, event):
        event.accept()
        # if sys.platform == 'darwin':
        #     filename = str(NSURL.alloc().initWithString_(event.mimeData().urls()[0].toString()).fileSystemRepresentation())
        # else:
        #     filename = event.mimeData().urls()[0].toLocalFile()

    def resizeEvent(self, event):
        self.background_label.setGeometry(0, 0, self.width(), self.height())
        self.start_screen_thumbnail_background.setGeometry(0, 0, self.width(), self.height())
        self.background_label2.setGeometry(0, 0, self.width(), self.height())

        self.startscreen.resized(self)
        self.subtitles_panel.resized(self)
        # self.properties.resized(self)

        self.global_panel.resized(self)
        # self.global_properties_panel.resized(self)

        self.playercontrols.resized(self)
        # self.playercontrols_properties.resized(self)

        self.background_watermark_label.setGeometry(int((self.width() * .5) - 129), int(((self.height() - self.playercontrols_widget.height()) * .5) - 129), 258, 258)
        # self.background_watermark_label.setVisible(False)

        self.player.resized(self)
        self.timeline.resized(self)
        event.accept()

    def closeEvent(self, event):
        if self.unsaved:
            save_message_box = QMessageBox(self)

            save_message_box.setWindowTitle('Unsaved changes')
            save_message_box.setText('Do you want to save the changes you made on the subtitles?')
            save_message_box.addButton('Save', QMessageBox.AcceptRole)
            save_message_box.addButton("Don't save", QMessageBox.RejectRole)
            ret = save_message_box.exec_()

            if ret == QMessageBox.AcceptRole:
                self.subtitles_panel.toppanel_save_button_clicked(self)

        self.thread_get_waveform.quit()
        self.thread_get_qimages.quit()
        # self.thread_extract_scene_time_positions.quit()
        self.thread_generated_burned_video.quit()
        self.thread_extract_waveform.quit()
        if self.actual_subtitle_file and 'hash' in self.video_metadata:
            self.player_widget.grab().save(os.path.join(PATH_SUBTITLD_DATA_THUMBNAILS, self.video_metadata['hash'] + '.png'))
            self.settings['recent_files'][self.actual_subtitle_file]['last_position'] = self.player_widget.position
        config.save(self.settings, PATH_SUBTITLD_USER_CONFIG_FILE)
        self.player_widget.close()

        event.accept()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space:
            self.player_widget.pause()
            self.playercontrols_playpause_button.setChecked(not self.playercontrols_playpause_button.isChecked())
            # self.playercontrols.playercontrols_playpause_button_update(self)

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
            self.subtitles_panel.update_subtitles_panel_widget_vision_content(self)
            # self.properties.update_properties_widget(self)
            self.timeline.update(self)

        if event.key() == Qt.Key_Left:
            self.player_widget.frameBackStep()

        if event.key() == Qt.Key_Right:
            self.player_widget.frameStep()

    def translate_widgets(self):
        self.setWindowTitle(translation._('window.title'))
        startscreen.translate_widgets(self)
        self.global_panel.translate_widgets(self)
        self.playercontrols.translate_widgets(self)
        self.subtitles_panel.translate_widgets(self)

    def generate_effect(self, widget, effect_type, duration, startValue, endValue):
        widget.setDuration(duration)
        if effect_type == 'geometry':
            widget.setStartValue(QRect(startValue[0], startValue[1], startValue[2], startValue[3]))
            widget.setEndValue(QRect(endValue[0], endValue[1], endValue[2], endValue[3]))
        if effect_type in ['maximumHeight', 'maximumWidth']:
            widget.setStartValue(startValue)
            widget.setEndValue(endValue)
        elif effect_type == 'opacity':
            widget.setStartValue(startValue)
            widget.setEndValue(endValue)
        widget.start()


def autosave_timer_timeout(self):
    filename = os.path.basename(self.actual_subtitle_file).rsplit('.', 1)[0]
    if not filename:
        filename = os.path.basename(self.video_metadata['filepath']).rsplit('.', 1)[0]
    self.file_io.save_file(os.path.join(PATH_SUBTITLD_DATA_BACKUP, filename + '_' + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + '.{}'.format(LIST_OF_SUPPORTED_SUBTITLE_EXTENSIONS[self.settings['default_values'].get('subtitle_format', 'USF')]['extensions'][0])), self.subtitles_list, self.settings['default_values'].get('subtitle_format', 'USF'))


def main():
    app = QApplication(sys.argv)
    # command to update ts files: pylupdate5 subtitld.py modules/*.py -ts locale/en_US.ts
    # if os.path.isfile(os.path.join(PATH_LOCALE, 'en_US.qm')):
    #     translator = QTranslator()
    #     translator.load(os.path.join(PATH_LOCALE, 'en_US.qm'))
    #     app.installTranslator(translator)
    # app.setDesktopSettingsAware(False)
    # app.setStyle("plastique")
    app.setApplicationName("Subtitld")

    QFontDatabase.addApplicationFont(os.path.join(PATH_SUBTITLD_GRAPHICS, 'Ubuntu-B.ttf'))
    QFontDatabase.addApplicationFont(os.path.join(PATH_SUBTITLD_GRAPHICS, 'Ubuntu-BI.ttf'))
    QFontDatabase.addApplicationFont(os.path.join(PATH_SUBTITLD_GRAPHICS, 'Ubuntu-C.ttf'))
    QFontDatabase.addApplicationFont(os.path.join(PATH_SUBTITLD_GRAPHICS, 'Ubuntu-L.ttf'))
    QFontDatabase.addApplicationFont(os.path.join(PATH_SUBTITLD_GRAPHICS, 'Ubuntu-LI.ttf'))
    QFontDatabase.addApplicationFont(os.path.join(PATH_SUBTITLD_GRAPHICS, 'Ubuntu-M.ttf'))
    QFontDatabase.addApplicationFont(os.path.join(PATH_SUBTITLD_GRAPHICS, 'Ubuntu-MI.ttf'))
    QFontDatabase.addApplicationFont(os.path.join(PATH_SUBTITLD_GRAPHICS, 'UbuntuMono-B.ttf'))
    QFontDatabase.addApplicationFont(os.path.join(PATH_SUBTITLD_GRAPHICS, 'UbuntuMono-BI.ttf'))
    QFontDatabase.addApplicationFont(os.path.join(PATH_SUBTITLD_GRAPHICS, 'UbuntuMono-R.ttf'))
    QFontDatabase.addApplicationFont(os.path.join(PATH_SUBTITLD_GRAPHICS, 'UbuntuMono-RI.ttf'))
    QFontDatabase.addApplicationFont(os.path.join(PATH_SUBTITLD_GRAPHICS, 'Ubuntu-R.ttf'))
    QFontDatabase.addApplicationFont(os.path.join(PATH_SUBTITLD_GRAPHICS, 'Ubuntu-RI.ttf'))
    QFontDatabase.addApplicationFont(os.path.join(PATH_SUBTITLD_GRAPHICS, 'Ubuntu-Th.ttf'))

    app.setFont(QFont('Ubuntu', 10))

    app.main = Subtitld()
    app.main.show()

    if args.file:
        files_list = []
        for filepath in args.file:
            files_list.append(filepath.name)
            app.main.file_io.open_filepath(app.main, files_to_open=files_list)

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
