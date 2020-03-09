#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QMetaObject, pyqtSlot
from PyQt5.QtWidgets import QOpenGLWidget, QApplication, QLabel, QTextEdit, QWidget
from PyQt5.QtOpenGL import QGLContext

from OpenGL import GL  # noqa

from mpv import MPV, _mpv_get_sub_api, _mpv_opengl_cb_set_update_callback, \
        _mpv_opengl_cb_init_gl, OpenGlCbGetProcAddrFn, _mpv_opengl_cb_draw, \
        _mpv_opengl_cb_report_flip, MpvSubApi, OpenGlCbUpdateFn, _mpv_opengl_cb_uninit_gl

def get_proc_addr(_, name):
    glctx = QGLContext.currentContext()
    if glctx is None:
        return 0
    addr = int(glctx.getProcAddress(name.decode('utf-8')))
    return addr

def load(self):
    class player_widget_area(QWidget):
        def enterEvent(widget, event):
            if self.selected_subtitle and not self.player_subtitle_textedit.isVisible() and self.player_subtitle_layer.text():
                self.player_subtitle_textedit.setPlainText(self.selected_subtitle[2])
                self.player_subtitle_layer.setVisible(False)
                self.player_subtitle_textedit.setVisible(True)
        def leaveEvent(widget, event):
            if self.selected_subtitle:
                self.player_subtitle_layer.setVisible(True)
                self.player_subtitle_textedit.setVisible(False)

    self.player_widget_area = player_widget_area(self)

    self.player_border = QLabel(self.player_widget_area)
    #self.player_border.setAttribute(Qt.WA_TransparentForMouseEvents)
    self.player_border.setObjectName('player_border')

    class MpvWidget(QOpenGLWidget):
        def __init__(self, parent=None):
            super().__init__(parent=parent)
            self.mpv = MPV(vo='opengl-cb', ytdl=True)
            self.mpv.osd = False
            self.mpv.autosub = False
            self.mpv_gl = _mpv_get_sub_api(self.mpv.handle, MpvSubApi.MPV_SUB_API_OPENGL_CB)
            self.on_update_c = OpenGlCbUpdateFn(self.on_update)
            self.on_update_fake_c = OpenGlCbUpdateFn(self.on_update_fake)
            self.get_proc_addr_c = OpenGlCbGetProcAddrFn(get_proc_addr)
            _mpv_opengl_cb_set_update_callback(self.mpv_gl, self.on_update_c, None)
            self.frameSwapped.connect(self.swapped, Qt.DirectConnection)

        def initializeGL(self):
            _mpv_opengl_cb_init_gl(self.mpv_gl, None, self.get_proc_addr_c, None)

        def paintGL(self):
            # compatible with HiDPI display
            ratio = self.parent().parent().windowHandle().devicePixelRatio()
            w = int(self.width() * ratio)
            h = int(self.height() * ratio)
            _mpv_opengl_cb_draw(self.mpv_gl, self.defaultFramebufferObject(), w, -h)

        @pyqtSlot()
        def maybe_update(self):
            if self.parent().parent().window().isMinimized():
                self.makeCurrent()
                self.paintGL()
                self.context().swapBuffers(self.context().surface())
                self.swapped()
                self.doneCurrent()
            else:
                self.update()

        def on_update(self, ctx=None):
            # maybe_update method should run on the thread that creates the OpenGLContext,
            # which in general is the main thread. QMetaObject.invokeMethod can
            # do this trick.
            QMetaObject.invokeMethod(self, 'maybe_update')

        def on_update_fake(self, ctx=None):
            pass

        def swapped(self):
            _mpv_opengl_cb_report_flip(self.mpv_gl, 0)

        def closeEvent(self, _):
            self.makeCurrent()
            if self.mpv_gl:
                _mpv_opengl_cb_set_update_callback(self.mpv_gl, self.on_update_fake_c, None)
            _mpv_opengl_cb_uninit_gl(self.mpv_gl)
            self.mpv.terminate()

    self.player_widget = MpvWidget(parent=self.player_widget_area)
    #self.player_widget.setAttribute(Qt.WA_TransparentForMouseEvents)

    self.player_subtitle_layer = QLabel(parent=self.player_widget_area)
    self.player_subtitle_layer.setWordWrap(True)
    self.player_subtitle_layer.setObjectName('player_subtitle_layer')

    self.player_subtitle_textedit = QTextEdit(parent=self.player_widget_area)
    #self.player_subtitle_textedit.setAttribute(Qt.WA_AlwaysStackOnTop)
    self.player_subtitle_textedit.setVisible(False)
    #self.player_subtitle_textedit.setWordWrap(True)
    self.player_subtitle_textedit.setObjectName('player_subtitle_textedit')
    self.player_subtitle_textedit.textChanged.connect(lambda:player_subtitle_textedit_changed(self))


def update(self):
    self.player_widget_area.setVisible(bool(self.video_metadata))
    self.player_border.setVisible(bool(self.video_metadata))

def resized(self):
    self.player_widget_area.setGeometry(self.width()*.2,0,self.width()*.6,self.height()-self.playercontrols_widget.height())
    resize_player_widget(self)

def player_subtitle_textedit_changed(self):
    old_selected_subtitle = self.selected_subtitle
    counter = self.subtitles_list.index(old_selected_subtitle)
    self.subtitles_list[counter][2] = self.player_subtitle_textedit.toPlainText()
    update_subtitle_layer(self)

def playpause(self):
    self.player_widget.mpv.pause = not self.player_widget.mpv.pause
    self.mediaplayer_is_playing = not self.player_widget.mpv.pause

def update_subtitle_layer(self):
    text = ''
    for subtitle in self.subtitles_list:
        if self.player_widget.mpv.time_pos and (self.player_widget.mpv.time_pos > subtitle[0] and self.player_widget.mpv.time_pos < subtitle[0] + subtitle[1]):
            text = subtitle[2]
            break

    self.player_subtitle_layer.setText(text)
    #self.player_subtitle_textedit.setPlainText(text)

def resize_player_widget(self):
    heigth_proportion = (self.player_widget_area.width()-6) / self.video_metadata.get('width', 1)
    self.player_widget.setGeometry(3,(self.player_widget_area.height()*.5)-((heigth_proportion*self.video_metadata.get('height', 1))*.5),self.player_widget_area.width()-6,self.video_metadata.get('height', 1)*heigth_proportion)
    self.player_border.setGeometry(self.player_widget.x()-3, self.player_widget.y()-3, self.player_widget.width()+6, self.player_widget.height()+6)
    self.player_subtitle_layer.setGeometry(self.player_widget.x(),self.player_widget.y(), self.player_widget.width(), self.player_widget.height())
    self.player_subtitle_textedit.setGeometry(self.player_widget.x()+(self.player_widget.width()*.1),self.player_widget.y()+(self.player_widget.height()*.5), self.player_widget.width()*.8, self.player_widget.height()*.4)
