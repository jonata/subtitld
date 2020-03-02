#!/usr/bin/python3

import os, sys, threading
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QLabel
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, QTimer

from modules.paths import *
#from modules import file_io
from modules import waveform

import numpy

class subtitld(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Subtitld')
        self.setWindowIcon(QIcon(os.path.join(PATH_SUBTITLD_GRAPHICS, 'subtitld.png')))

        self.update_accuracy = 200
        self.subtitles_list = []
        self.video_metadata = {}
        self.actual_subtitle_file = False
        self.selected_subtitle = False
        self.mediaplayer_zoom = 100.0
        self.video_waveformsize = .7
        self.mediaplayer_opacity = .5
        self.video_length = 0.01
        self.mediaplayer_current_position = 0.0
        self.mediaplayer_is_playing = False
        self.mediaplayer_view_mode = 'verticalform'

        self.background_label = QLabel(self)
        self.background_label.setObjectName('background_label')

        self.setStyleSheet('''
                                #background_label                           { border-left:0; border-top:0; border-right:0; border-bottom:0; border-image: url("''' + get_graphics_path('background.png') + '''") 0 0 0 0 stretch stretch; }
                                #subtitles_list_widget                      { border-top: 0; border-right: 2px; border-bottom: 0; border-left: 0; border-image: url("''' + get_graphics_path('subtitle_list_widget_background.png') + '''") 0 2 0 0 stretch stretch; }
                                #properties_widget                          { border-top: 0; border-right: 0; border-bottom: 0; border-left: 2px; border-image: url("''' + get_graphics_path('properties_widget_background.png') + '''") 0 0 0 2 stretch stretch; }
                                #playercontrols_widget_central              { border-top: 90px; border-right: 28px; border-bottom: 0; border-left: 28px; border-image: url("''' + get_graphics_path('timeline_top_controls_background.png') + '''") 90 28 0 28 stretch stretch; }
                                #playercontrols_widget_right                { border-top: 90px; border-right: 0; border-bottom: 0; border-left: 0; border-image: url("''' + get_graphics_path('timeline_top_controls_background.png') + '''") 90 0 0 58 stretch stretch; }
                                #playercontrols_widget_left                 { border-top: 90px; border-right: 0; border-bottom: 0; border-left: 0; border-image: url("''' + get_graphics_path('timeline_top_controls_background.png') + '''") 90 58 0 0 stretch stretch; }
                                #player_border                              { border-top: 5px; border-right: 5px; border-bottom: 5px; border-left: 5px; border-image: url("''' + get_graphics_path('video_border.png') + '''") 5 5 5 5 stretch stretch; }

                                #timeline_scroll                            { padding-top:-30px; border-top: 30px; border-right: 0; border-bottom: 0; border-left: 0; border-image: url("''' + get_graphics_path('timeline_background.png') + '''") 30 5 5 5 stretch stretch; background-color:transparent; }
                                #timeline_widget                            { background-color:transparent; }

                                QPushButton                                 { font-size:10px; color:white; }
                                #subtitles_list_widget_alert                { font-size:20px; color: rgba(200, 200, 200, 100); qproperty-alignment: "AlignCenter"; padding: 40px; }

                                #player_subtitle_layer                      { font-size:40px; color: rgb(255, 255, 255); qproperty-alignment: "AlignCenter | AlignBottom"; padding: 40px; }

                                #button_dark_no_right                       { border-left: 5px; border-top: 5px; border-right: 0; border-bottom: 5px; border-image: url("''' + get_graphics_path('button_dark_normal.png') + '''") 5 5 5 5 stretch stretch; outline: none; }
                                #button_dark_no_right:hover:pressed         { border-left: 5px; border-top: 5px; border-right: 0; border-bottom: 5px; border-image: url("''' + get_graphics_path('button_dark_pressed.png') + '''") 5 5 5 5 stretch stretch; outline: none;  }
                                #button_dark_no_right:hover                 { border-left: 5px; border-top: 5px; border-right: 0; border-bottom: 5px; border-image: url("''' + get_graphics_path('button_dark_hover.png') + '''") 5 5 5 5 stretch stretch; outline: none; }
                                #button_dark_no_right:disabled              { border-left: 5px; border-top: 5px; border-right: 0; border-bottom: 5px; border-image: url("''' + get_graphics_path('button_dark_disabled.png') + '''") 5 5 5 5 stretch stretch; outline: none; }

                                #button_dark_no_left                        { border-left: 0; border-top: 5px; border-right: 5px; border-bottom: 5px; border-image: url("''' + get_graphics_path('button_dark_normal.png') + '''") 5 5 5 5 stretch stretch; outline: none; }
                                #button_dark_no_left:hover:pressed          { border-left: 0; border-top: 5px; border-right: 5px; border-bottom: 5px; border-image: url("''' + get_graphics_path('button_dark_pressed.png') + '''") 5 5 5 5 stretch stretch; outline: none;  }
                                #button_dark_no_left:hover                  { border-left: 0; border-top: 5px; border-right: 5px; border-bottom: 5px; border-image: url("''' + get_graphics_path('button_dark_hover.png') + '''") 5 5 5 5 stretch stretch; outline: none; }
                                #button_dark_no_left:disabled               { border-left: 0; border-top: 5px; border-right: 5px; border-bottom: 5px; border-image: url("''' + get_graphics_path('button_dark_disabled.png') + '''") 5 5 5 5 stretch stretch; outline: none; }

                                #button_no_right                            { border-left: 5px; border-top: 5px; border-right: 0; border-bottom: 5px; border-image: url("''' + get_graphics_path('button_normal.png') + '''") 5 5 5 5 stretch stretch; outline: none; }
                                #button_no_right:hover:pressed              { border-left: 5px; border-top: 5px; border-right: 0; border-bottom: 5px; border-image: url("''' + get_graphics_path('button_pressed.png') + '''") 5 5 5 5 stretch stretch; outline: none;  }
                                #button_no_right:hover                      { border-left: 5px; border-top: 5px; border-right: 0; border-bottom: 5px; border-image: url("''' + get_graphics_path('button_hover.png') + '''") 5 5 5 5 stretch stretch; outline: none; }
                                #button_no_right:disabled                   { border-left: 5px; border-top: 5px; border-right: 0; border-bottom: 5px; border-image: url("''' + get_graphics_path('button_disabled.png') + '''") 5 5 5 5 stretch stretch; outline: none; }

                                #button_no_left                             { border-left: 0; border-top: 5px; border-right: 5px; border-bottom: 5px; border-image: url("''' + get_graphics_path('button_normal.png') + '''") 5 5 5 5 stretch stretch; outline: none; }
                                #button_no_left:hover:pressed               { border-left: 0; border-top: 5px; border-right: 5px; border-bottom: 5px; border-image: url("''' + get_graphics_path('button_pressed.png') + '''") 5 5 5 5 stretch stretch; outline: none;  }
                                #button_no_left:hover                       { border-left: 0; border-top: 5px; border-right: 5px; border-bottom: 5px; border-image: url("''' + get_graphics_path('button_hover.png') + '''") 5 5 5 5 stretch stretch; outline: none; }
                                #button_no_left:disabled                    { border-left: 0; border-top: 5px; border-right: 5px; border-bottom: 5px; border-image: url("''' + get_graphics_path('button_disabled.png') + '''") 5 5 5 5 stretch stretch; outline: none; }

                                QListWidget                                 { outline: none; font-size:20px; color:black; } QListWidget::item:selected { background:#EEEEEE; color:gray; }
        ''')

        from modules import player
        self.player = player
        self.player.load(self)

        from modules import subtitleslist
        self.subtitleslist = subtitleslist
        self.subtitleslist.load(self, PATH_SUBTITLD_GRAPHICS)

        from modules import properties
        self.properties = properties
        self.properties.load(self, PATH_SUBTITLD_GRAPHICS)

        from modules import playercontrols
        self.playercontrols = playercontrols
        self.playercontrols.load(self, PATH_SUBTITLD_GRAPHICS)

        from modules import timeline
        self.timeline = timeline
        self.timeline.load(self, PATH_SUBTITLD_GRAPHICS)


        #from modules import document_edit
        #self.document_edit = document_edit
        #self.document_edit.load(self, PATH_SUBTITLD_GRAPHICS)


        #from modules import top_bar
        #self.top_bar = top_bar
        #self.top_bar.load(self, PATH_SUBTITLD_GRAPHICS)

        #from modules import importer
        #self.importer = importer
        #self.importer.load(self, PATH_SUBTITLD_GRAPHICS)


        self.setGeometry(0, 0, QDesktopWidget().screenGeometry().width(), QDesktopWidget().screenGeometry().height())

        self.subtitleslist.update_subtitles_list_widget(self)
        self.properties.update_properties_widget(self)
        self.playercontrols.update_playercontrols_widget(self)
        self.player.update(self)

        self.timer = QTimer(self)
        self.timer.setInterval(self.update_accuracy)
        self.timer.timeout.connect(lambda:update_things(self))
        self.timer.start()

    def resizeEvent(self, event):
        self.background_label.setGeometry(0,0,self.width(),self.height())

        self.subtitleslist.resized(self)
        self.playercontrols.resized(self)
        self.properties.resized(self)
        self.player.resized(self)
        self.timeline.resized(self)

    def closeEvent(self, _):
        self.player_widget.close()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space:
            self.player_widget.mpv.pause = not self.player_widget.mpv.pause

        if event.key() == Qt.Key_Slash:
            self.player_controls.play_button_selection.setChecked(not self.player_controls.play_button_selection.isChecked())

        if event.key() == Qt.Key_9:
            self.player_controls.new_back(self)

        if event.key() == Qt.Key_8:
            self.player_controls.note_above(self)

        if event.key() == Qt.Key_2:
            self.player_controls.note_below(self)

        if event.key() == Qt.Key_6:
            self.player_controls.note_ends_forward(self)

        if event.key() == Qt.Key_4:
            self.player_controls.note_starts_back(self)

        if event.key() == Qt.Key_1:
            self.player_controls.note_starts_forward(self)

        if event.key() == Qt.Key_3:
            self.player_controls.note_ends_back(self)

        if event.key() in [Qt.Key_Asterisk]:
            self.player_controls.golden_note(self)

        if event.key() in [Qt.Key_5]:
            self.player_controls.freestyle_note(self)

        if event.key() in [Qt.Key_Comma, Qt.Key_Period]:
            self.player_controls.line_break(self)

        if event.key() in [Qt.Key_Delete, Qt.Key_Backspace]:
            self.player_controls.note_remove(self)

        if event.key() == Qt.Key_Plus:
            zoomin_button_clicked(self)

        if event.key() == Qt.Key_Minus:
            zoomout_button_clicked(self)

        if event.key() == Qt.Key_Q:
            if self.player_controls.listen_note_preview.isChecked():
                self.now_previewing_note = 'F3'
                frequency = 174.6141 #F3
                time = 0.5#self.lyrics_metadata['bpm'] / 60000.0
                sounddevice.play(numpy.array((10000 * numpy.sin(2 * numpy.pi * frequency * (numpy.arange(44100 * time) / 44100.0))), dtype=numpy.int16))


        #if event.key() == Qt.Key_2:
        #    frequency = 184.9972 #F#3
        #    time = 0.5#self.lyrics_metadata['bpm'] / 60000.0
        #    sounddevice.play(numpy.array((10000 * numpy.sin(2 * numpy.pi * frequency * (numpy.arange(44100 * time) / 44100.0))), dtype=numpy.int16))

        if event.key() == Qt.Key_W:
            if self.player_controls.listen_note_preview.isChecked():
                self.now_previewing_note = 'G3'
                frequency = 195.9977 #G3
                time = 0.5#self.lyrics_metadata['bpm'] / 60000.0
                sounddevice.play(numpy.array((10000 * numpy.sin(2 * numpy.pi * frequency * (numpy.arange(44100 * time) / 44100.0))), dtype=numpy.int16))

        #if event.key() == Qt.Key_3:
        #    frequency = 207.6523 #G#3
        #    time = 0.5#self.lyrics_metadata['bpm'] / 60000.0
        #    sounddevice.play(numpy.array((10000 * numpy.sin(2 * numpy.pi * frequency * (numpy.arange(44100 * time) / 44100.0))), dtype=numpy.int16))

        if event.key() == Qt.Key_E:
            if self.player_controls.listen_note_preview.isChecked():
                self.now_previewing_note = 'A4'
                frequency = 220.0000 #A3
                time = 0.5#self.lyrics_metadata['bpm'] / 60000.0
                sounddevice.play(numpy.array((10000 * numpy.sin(2 * numpy.pi * frequency * (numpy.arange(44100 * time) / 44100.0))), dtype=numpy.int16))

        #if event.key() == Qt.Key_4:
        #    frequency = 233.0819 #A#3
        #    time = 0.5#self.lyrics_metadata['bpm'] / 60000.0
        #    sounddevice.play(numpy.array((10000 * numpy.sin(2 * numpy.pi * frequency * (numpy.arange(44100 * time) / 44100.0))), dtype=numpy.int16))

        if event.key() == Qt.Key_R:
            if self.player_controls.listen_note_preview.isChecked():
                self.now_previewing_note = 'B4'
                frequency = 246.9417 #B3
                time = 0.5#self.lyrics_metadata['bpm'] / 60000.0
                sounddevice.play(numpy.array((10000 * numpy.sin(2 * numpy.pi * frequency * (numpy.arange(44100 * time) / 44100.0))), dtype=numpy.int16))

        if event.key() == Qt.Key_T:
            if self.player_controls.listen_note_preview.isChecked():
                self.now_previewing_note = 'C4'
                frequency = 261.6256 #C4
                time = 0.5#self.lyrics_metadata['bpm'] / 60000.0
                sounddevice.play(numpy.array((10000 * numpy.sin(2 * numpy.pi * frequency * (numpy.arange(44100 * time) / 44100.0))), dtype=numpy.int16))

        #if event.key() == Qt.Key_6:
        #    frequency = 277.1826 #C#4
        #    time = 0.5#self.lyrics_metadata['bpm'] / 60000.0
        #    sounddevice.play(numpy.array((10000 * numpy.sin(2 * numpy.pi * frequency * (numpy.arange(44100 * time) / 44100.0))), dtype=numpy.int16))

        if event.key() == Qt.Key_Y:
            if self.player_controls.listen_note_preview.isChecked():
                self.now_previewing_note = 'D4'
                frequency = 293.6648 #D4
                time = 0.5#self.lyrics_metadata['bpm'] / 60000.0
                sounddevice.play(numpy.array((10000 * numpy.sin(2 * numpy.pi * frequency * (numpy.arange(44100 * time) / 44100.0))), dtype=numpy.int16))

        #if event.key() == Qt.Key_7:
        #    frequency = 311.1270 #D#4
        #    time = 0.5#self.lyrics_metadata['bpm'] / 60000.0
        #    sounddevice.play(numpy.array((10000 * numpy.sin(2 * numpy.pi * frequency * (numpy.arange(44100 * time) / 44100.0))), dtype=numpy.int16))

        if event.key() == Qt.Key_U:
            if self.player_controls.listen_note_preview.isChecked():
                self.now_previewing_note = 'E4'
                frequency = 329.6276 #E4
                time = 0.5#self.lyrics_metadata['bpm'] / 60000.0
                sounddevice.play(numpy.array((10000 * numpy.sin(2 * numpy.pi * frequency * (numpy.arange(44100 * time) / 44100.0))), dtype=numpy.int16))

        if event.key() == Qt.Key_I:
            if self.player_controls.listen_note_preview.isChecked():
                self.now_previewing_note = 'F4'
                frequency = 349.2282 #F4
                time = 0.5#self.lyrics_metadata['bpm'] / 60000.0
                sounddevice.play(numpy.array((10000 * numpy.sin(2 * numpy.pi * frequency * (numpy.arange(44100 * time) / 44100.0))), dtype=numpy.int16))

        #if event.key() == Qt.Key_9:
        #    frequency = 369.9944 #F#4
        #    time = 0.5#self.lyrics_metadata['bpm'] / 60000.0
        #    sounddevice.play(numpy.array((10000 * numpy.sin(2 * numpy.pi * frequency * (numpy.arange(44100 * time) / 44100.0))), dtype=numpy.int16))

        if event.key() == Qt.Key_O:
            if self.player_controls.listen_note_preview.isChecked():
                self.now_previewing_note = 'G4'
                frequency = 391.9954 #G4
                time = 0.5#self.lyrics_metadata['bpm'] / 60000.0
                sounddevice.play(numpy.array((10000 * numpy.sin(2 * numpy.pi * frequency * (numpy.arange(44100 * time) / 44100.0))), dtype=numpy.int16))

        #if event.key() == Qt.Key_0:
        #    frequency = 415.3047 #G#4
        #    time = 0.5#self.lyrics_metadata['bpm'] / 60000.0
        #    sounddevice.play(numpy.array((10000 * numpy.sin(2 * numpy.pi * frequency * (numpy.arange(44100 * time) / 44100.0))), dtype=numpy.int16))

        if event.key() == Qt.Key_P:
            if self.player_controls.listen_note_preview.isChecked():
                self.now_previewing_note = 'A5'
                frequency = 440.0000 #A4
                time = 0.5#self.lyrics_metadata['bpm'] / 60000.0
                sounddevice.play(numpy.array((10000 * numpy.sin(2 * numpy.pi * frequency * (numpy.arange(44100 * time) / 44100.0))), dtype=numpy.int16))


    def live_recording_note_thread_updated(self, result):
        self.recording_note = result

def update_things(self):
    # if self.mediaplayer_is_playing:
    #     self.mediaplayer_current_position += ((self.update_accuracy*.001)/self.music_length)#(event.pos().x() / widget.width()) * len(self.music_waveform['full'])
    #     if self.player_controls.play_button_selection.isChecked() and self.selected_note:
    #         if self.mediaplayer_current_position*len(self.music_waveform['full']) > (int(self.lyrics_metadata['gap'] * ( len(self.music_waveform['full']) / (self.music_length * 1000))) + int(    ((len(self.music_waveform['full']) / (self.music_length/60.0))    /     self.lyrics_metadata['bpm'])*.25         * int(self.selected_note[0])) + int(    ((len(self.music_waveform['full']) / (self.music_length/60.0))    /     self.lyrics_metadata['bpm'])*.25         * int(self.selected_note[1]))):
    #             self.player_controls.stop_button.setVisible(False)
    #             self.player_controls.play_button.setVisible(True)
    #             self.player_controls.play_button_selection.setVisible(True)
    #             self.mediaplayer_is_playing = False
    #             self.mediaplayer_current_position = float((int(self.lyrics_metadata['gap'] * ( len(self.music_waveform['full']) / (self.music_length * 1000))) + int(((len(self.music_waveform['full']) / (self.music_length/60.0))    /     self.lyrics_metadata['bpm'])*.25         * int(self.selected_note[0]))) / len(self.music_waveform['full']))
    self.timeline_widget.update()
    self.player.update_subtitle_layer(self)

def edit_syllable_returnpressed(self):
    self.lyrics_notes[self.lyrics_notes.index(self.selected_note)][3] = self.player_controls.edit_sylable.text()
    self.timeline_widget.update()

def zoomin_button_clicked(self):
    self.mediaplayer_zoom += 5.0
    if not self.mediaplayer_zoom in self.video_metadata.get('waveform', {}).keys():
        threading.Thread(target=waveform.get_waveform_zoom(self, self.mediaplayer_zoom, self.video_metadata['duration'], self.video_metadata['waveform'][0], self.video_metadata.get('duration', 0.01)*self.mediaplayer_zoom, self.timeline_widget.height()-30)).start()
    self.timeline_widget.setGeometry(0,0,int(round(self.video_metadata.get('duration', 0.01)*self.mediaplayer_zoom)),self.timeline_scroll.height()-20)
    #self.timeline_widget.update()

def zoomout_button_clicked(self):
    self.mediaplayer_zoom -= 5.0
    if not self.mediaplayer_zoom in self.video_metadata.get('waveform', {}).keys():
        threading.Thread(target=waveform.get_waveform_zoom(self, self.mediaplayer_zoom, self.video_metadata['duration'], self.video_metadata['waveform'][0], self.video_metadata.get('duration', 0.01)*self.mediaplayer_zoom, self.timeline_widget.height()-30)).start()
    self.timeline_widget.setGeometry(0,0,int(round(self.video_metadata.get('duration', 0.01)*self.mediaplayer_zoom)),self.timeline_scroll.height()-20)
    #self.timeline_widget.update()

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

def show_importer_pannel_button_clicked(self):
    if self.show_importer_panel_button.isChecked():
        generate_effect(self.importer.widget_animation, 'geometry', 500, [self.importer.widget.x(),self.importer.widget.y(),self.importer.widget.width(),self.importer.widget.height()], [self.width()-300,self.importer.widget.y(),self.importer.widget.width(),self.importer.widget.height()])
        generate_effect(self.show_importer_panel_button_animation, 'geometry', 500, [self.show_importer_panel_button.x(),self.show_importer_panel_button.y(),self.show_importer_panel_button.width(),self.show_importer_panel_button.height()], [self.width()-290,self.show_importer_panel_button.y(),self.show_importer_panel_button.width(),self.show_importer_panel_button.height()])
    else:
        generate_effect(self.importer.widget_animation, 'geometry', 500, [self.importer.widget.x(),self.importer.widget.y(),self.importer.widget.width(),self.importer.widget.height()], [self.width(),self.importer.widget.y(),self.importer.widget.width(),self.importer.widget.height()])
        generate_effect(self.show_importer_panel_button_animation, 'geometry', 500, [self.show_importer_panel_button.x(),self.show_importer_panel_button.y(),self.show_importer_panel_button.width(),self.show_importer_panel_button.height()], [self.width()-25,self.show_importer_panel_button.y(),self.show_importer_panel_button.width(),self.show_importer_panel_button.height()])

def generate_effect(widget, effect_type, duration, startValue, endValue):
    widget.setDuration(duration)
    if effect_type == 'geometry':
        widget.setStartValue(QRect(startValue[0],startValue[1],startValue[2],startValue[3]))
        widget.setEndValue(QRect(endValue[0],endValue[1],endValue[2],endValue[3]))
    elif effect_type == 'opacity':
        widget.setStartValue(startValue)
        widget.setEndValue(endValue)
    widget.start()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    #app.setDesktopSettingsAware(False)
    app.setStyle("plastique")
    app.setApplicationName("Subtitld")

    if sys.platform == 'darwin':
        from PyQt5.QtGui import QFontDatabase
        font_database = QFontDatabase()
        font_database.addApplicationFont(os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), 'Ubuntu-RI.ttf'))
        font_database.addApplicationFont(os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), 'Ubuntu-R.ttf'))
        font_database.addApplicationFont(os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), 'Ubuntu-B.ttf'))
        font_database.addApplicationFont(os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), 'Ubuntu-BI.ttf'))

    app.setFont(QFont('Ubuntu', 10))
    app.main = subtitld()
    app.main.show()

    sys.exit(app.exec_())
