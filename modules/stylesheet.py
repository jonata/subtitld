#!/usr/bin/python3
# -*- coding: utf-8 -*-

from modules.paths import *

def set_stylesheet(self):
    self.setStyleSheet('''
                            #background_label                           { background: qlineargradient( x1:0 y1:0, x2:0 y2:1, stop:0 rgb(7,9,11), stop:1 rgb(26,35,43)); }
                            #background_label2                          { background: qlineargradient( x1:0 y1:0, x2:0 y2:1, stop:0 rgb(26,35,43), stop:1 rgb(46,62,76)); }
                            #background_watermark_label                 { image: url("''' + get_graphics_path('background_watermark.png') + '''"); }
                            #subtitles_list_widget                      { border-top: 0; border-right: 2px; border-bottom: 0; border-left: 0; border-image: url("''' + get_graphics_path('subtitle_list_widget_background.png') + '''") 0 2 0 0 stretch stretch; }
                            #properties_widget                          { border-top: 0; border-right: 0; border-bottom: 0; border-left: 2px; border-image: url("''' + get_graphics_path('properties_widget_background.png') + '''") 0 0 0 2 stretch stretch; }
                            #playercontrols_widget_central              { border-top: 90px; border-right: 28px; border-bottom: 0; border-left: 28px; border-image: url("''' + get_graphics_path('timeline_top_controls_background.png') + '''") 90 28 0 28 stretch stretch; }
                            #playercontrols_widget_right                { border-top: 90px; border-right: 0; border-bottom: 0; border-left: 0; border-image: url("''' + get_graphics_path('timeline_top_controls_background.png') + '''") 90 0 0 58 stretch stretch; }
                            #playercontrols_widget_left                 { border-top: 90px; border-right: 0; border-bottom: 0; border-left: 0; border-image: url("''' + get_graphics_path('timeline_top_controls_background.png') + '''") 90 58 0 0 stretch stretch; }
                            #player_border                              { border-top: 5px; border-right: 5px; border-bottom: 5px; border-left: 5px; border-image: url("''' + get_graphics_path('video_border.png') + '''") 5 5 5 5 stretch stretch; }

                            #timeline_scroll                            { padding-top:-30px; border-top: 30px; border-right: 0; border-bottom: 0; border-left: 0; border-image: url("''' + get_graphics_path('timeline_background.png') + '''") 30 5 5 5 stretch stretch; background-color:transparent; }
                            #timeline_widget                            { background-color:transparent; }

                            QPushButton                                 { font-size:10px; color:white; }
                            #start_screen_recent_alert                  { font-size:14px; color: rgb(106, 116, 131); qproperty-alignment: "AlignCenter"; padding: 40px; }

                            #player_subtitle_layer                      { font-size:40px; color: rgb(255, 255, 255); qproperty-alignment: "AlignCenter | AlignBottom"; padding: 10px; }
                            #player_subtitle_textedit                   { padding:10px; font-size:32px; color: rgb(0, 0, 0); }

                            #button_dark                                { border-left: 5px; border-top: 5px; border-right: 5px; border-bottom: 5px; border-image: url("''' + get_graphics_path('button_dark_normal.png') + '''") 5 5 5 5 stretch stretch; outline: none; }
                            #button_dark:hover:pressed                  { border-left: 5px; border-top: 5px; border-right: 5px; border-bottom: 5px; border-image: url("''' + get_graphics_path('button_dark_pressed.png') + '''") 5 5 5 5 stretch stretch; outline: none;  }
                            #button_dark:hover                          { border-left: 5px; border-top: 5px; border-right: 5px; border-bottom: 5px; border-image: url("''' + get_graphics_path('button_dark_hover.png') + '''") 5 5 5 5 stretch stretch; outline: none; }
                            #button_dark:disabled                       { border-left: 5px; border-top: 5px; border-right: 5px; border-bottom: 5px; border-image: url("''' + get_graphics_path('button_dark_disabled.png') + '''") 5 5 5 5 stretch stretch; outline: none; }

                            #button_dark_no_right                       { border-left: 5px; border-top: 5px; border-right: 0; border-bottom: 5px; border-image: url("''' + get_graphics_path('button_dark_normal.png') + '''") 5 5 5 5 stretch stretch; outline: none; }
                            #button_dark_no_right:hover:pressed         { border-left: 5px; border-top: 5px; border-right: 0; border-bottom: 5px; border-image: url("''' + get_graphics_path('button_dark_pressed.png') + '''") 5 5 5 5 stretch stretch; outline: none;  }
                            #button_dark_no_right:hover                 { border-left: 5px; border-top: 5px; border-right: 0; border-bottom: 5px; border-image: url("''' + get_graphics_path('button_dark_hover.png') + '''") 5 5 5 5 stretch stretch; outline: none; }
                            #button_dark_no_right:disabled              { border-left: 5px; border-top: 5px; border-right: 0; border-bottom: 5px; border-image: url("''' + get_graphics_path('button_dark_disabled.png') + '''") 5 5 5 5 stretch stretch; outline: none; }

                            #button_dark_no_left                        { border-left: 0; border-top: 5px; border-right: 5px; border-bottom: 5px; border-image: url("''' + get_graphics_path('button_dark_normal.png') + '''") 5 5 5 5 stretch stretch; outline: none; }
                            #button_dark_no_left:hover:pressed          { border-left: 0; border-top: 5px; border-right: 5px; border-bottom: 5px; border-image: url("''' + get_graphics_path('button_dark_pressed.png') + '''") 5 5 5 5 stretch stretch; outline: none;  }
                            #button_dark_no_left:hover                  { border-left: 0; border-top: 5px; border-right: 5px; border-bottom: 5px; border-image: url("''' + get_graphics_path('button_dark_hover.png') + '''") 5 5 5 5 stretch stretch; outline: none; }
                            #button_dark_no_left:disabled               { border-left: 0; border-top: 5px; border-right: 5px; border-bottom: 5px; border-image: url("''' + get_graphics_path('button_dark_disabled.png') + '''") 5 5 5 5 stretch stretch; outline: none; }

                            #button_no_right_top                        { border-left: 5px; border-top: 0; border-right: 0; border-bottom: 5px; border-image: url("''' + get_graphics_path('button_normal.png') + '''") 5 5 5 5 stretch stretch; outline: none; }
                            #button_no_right_top:hover:pressed          { border-left: 5px; border-top: 0; border-right: 0; border-bottom: 5px; border-image: url("''' + get_graphics_path('button_pressed.png') + '''") 5 5 5 5 stretch stretch; outline: none;  }
                            #button_no_right_top:hover                  { border-left: 5px; border-top: 0; border-right: 0; border-bottom: 5px; border-image: url("''' + get_graphics_path('button_hover.png') + '''") 5 5 5 5 stretch stretch; outline: none; }
                            #button_no_right_top:disabled               { border-left: 5px; border-top: 0; border-right: 0; border-bottom: 5px; border-image: url("''' + get_graphics_path('button_disabled.png') + '''") 5 5 5 5 stretch stretch; outline: none; }

                            #button_no_left_top                        { border-left: 0; border-top: 0; border-right: 5px; border-bottom: 5px; border-image: url("''' + get_graphics_path('button_normal.png') + '''") 5 5 5 5 stretch stretch; outline: none; }
                            #button_no_left_top:hover:pressed          { border-left: 0; border-top: 0; border-right: 5px; border-bottom: 5px; border-image: url("''' + get_graphics_path('button_pressed.png') + '''") 5 5 5 5 stretch stretch; outline: none;  }
                            #button_no_left_top:hover                  { border-left: 0; border-top: 0; border-right: 5px; border-bottom: 5px; border-image: url("''' + get_graphics_path('button_hover.png') + '''") 5 5 5 5 stretch stretch; outline: none; }
                            #button_no_left_top:disabled               { border-left: 0; border-top: 0; border-right: 5px; border-bottom: 5px; border-image: url("''' + get_graphics_path('button_disabled.png') + '''") 5 5 5 5 stretch stretch; outline: none; }

                            #button_no_right                            { border-left: 5px; border-top: 5px; border-right: 0; border-bottom: 5px; border-image: url("''' + get_graphics_path('button_normal.png') + '''") 5 5 5 5 stretch stretch; outline: none; }
                            #button_no_right:hover:pressed              { border-left: 5px; border-top: 5px; border-right: 0; border-bottom: 5px; border-image: url("''' + get_graphics_path('button_pressed.png') + '''") 5 5 5 5 stretch stretch; outline: none;  }
                            #button_no_right:hover                      { border-left: 5px; border-top: 5px; border-right: 0; border-bottom: 5px; border-image: url("''' + get_graphics_path('button_hover.png') + '''") 5 5 5 5 stretch stretch; outline: none; }
                            #button_no_right:disabled                   { border-left: 5px; border-top: 5px; border-right: 0; border-bottom: 5px; border-image: url("''' + get_graphics_path('button_disabled.png') + '''") 5 5 5 5 stretch stretch; outline: none; }

                            #button_no_left                             { border-left: 0; border-top: 5px; border-right: 5px; border-bottom: 5px; border-image: url("''' + get_graphics_path('button_normal.png') + '''") 5 5 5 5 stretch stretch; outline: none; }
                            #button_no_left:hover:pressed               { border-left: 0; border-top: 5px; border-right: 5px; border-bottom: 5px; border-image: url("''' + get_graphics_path('button_pressed.png') + '''") 5 5 5 5 stretch stretch; outline: none;  }
                            #button_no_left:hover                       { border-left: 0; border-top: 5px; border-right: 5px; border-bottom: 5px; border-image: url("''' + get_graphics_path('button_hover.png') + '''") 5 5 5 5 stretch stretch; outline: none; }
                            #button_no_left:disabled                    { border-left: 0; border-top: 5px; border-right: 5px; border-bottom: 5px; border-image: url("''' + get_graphics_path('button_disabled.png') + '''") 5 5 5 5 stretch stretch; outline: none; }

                            #subtitles_list_qlistwidget                 { outline: none; font-size:14px; color:rgb(106, 116, 131); border-top-right-radius: 4px; background-color: rgba(255, 255, 255, 200); padding:5px;} QListWidget::item { padding:5px; border-radius: 2px;} QListWidget::item:selected { background:rgb(184, 206, 224); color:rgb(106, 116, 131); }
                            #start_screen_recent_listwidget             { outline: none; font-size:14px; color:rgb(106, 116, 131); border-radius: 4px; background-color: rgba(106, 116, 131, 20); padding:5px;} QListWidget::item { padding:5px; border-radius: 2px;} QListWidget::item:selected { background:rgb(184, 206, 224); color:rgb(106, 116, 131); }

                            QScrollBar:horizontal                       { height: 15px; margin: 2px 2px 2px 2px; border: 1px transparent rgba(0,0,0,50); border-radius: 2px; background-color: rgba(0,0,0,50); }
                            QScrollBar::handle:horizontal               { background-color: rgba(0,0,0,50); min-width: 5px; border-radius: 2px; }
                            QScrollBar::add-line:horizontal             { border: none; background: none; }
                            QScrollBar::sub-line:horizontal             { border: none; background: none; }
                            QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal { background: none; }
                            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal { background: none; }

                            #start_screen_recentfiles_background        { background-color: rgba(106, 116, 131, 50); }
                            #start_screen_top_shadow                    { border-left: 0; border-top: 1px; border-right: 0; border-bottom: 0; border-image: url("''' + get_graphics_path('start_screen_top_shadow.png') + '''") 1 0 0 0 stretch stretch; outline: none; }
                            #start_screen_open_label                    { font-size:10px; color:rgb(106, 116, 131); qproperty-alignment: "AlignVCenter | AlignRight"; qproperty-wordWrap: true}
                            #start_screen_recent_label                  { font-size:10px; color:rgb(106, 116, 131); qproperty-alignment: "AlignCenter"; qproperty-wordWrap: true}
                            #start_screen_adver_label                   { font-size:10px; color:rgb(106, 116, 131); qproperty-alignment: "AlignVCenter | AlignLeft"; qproperty-wordWrap: true}
                            #start_screen_adver_label_details           { font-size:14px; color:rgb(106, 116, 131); qproperty-alignment: "AlignTop | AlignLeft"; qproperty-wordWrap: true}
    ''')


# QScrollBar::add-line:horizontal             { margin: 0px 3px 0px 3px; border-image: url(:/qss_icons/rc/right_arrow_disabled.png); width: 10px; height: 10px; subcontrol-position: right; subcontrol-origin: margin; }
# QScrollBar::sub-line:horizontal             { margin: 0px 3px 0px 3px; border-image: url(:/qss_icons/rc/left_arrow_disabled.png); height: 10px; width: 10px; subcontrol-position: left; subcontrol-origin: margin; }
# QScrollBar::add-line:horizontal:hover,QScrollBar::add-line:horizontal:on { border-image: url(:/qss_icons/rc/right_arrow.png); height: 10px; width: 10px; subcontrol-position: right; subcontrol-origin: margin; }
# QScrollBar::sub-line:horizontal:hover, QScrollBar::sub-line:horizontal:on {  border-image: url(:/qss_icons/rc/left_arrow.png); height: 10px; width: 10px; subcontrol-position: left; subcontrol-origin: margin; }
#QScrollBar:vertical { background-color: #2A2929; width: 15px; margin: 15px 3px 15px 3px; border: 1px transparent #2A2929; border-radius: 4px; }
# QScrollBar::handle:vertical { background-color: red; min-height: 5px; border-radius: 4px; }
# QScrollBar::sub-line:vertical { margin: 3px 0px 3px 0px; border-image: url(:/qss_icons/rc/up_arrow_disabled.png); height: 10px; width: 10px; subcontrol-position: top; subcontrol-origin: margin; }
# QScrollBar::add-line:vertical { margin: 3px 0px 3px 0px; border-image: url(:/qss_icons/rc/down_arrow_disabled.png); height: 10px; width: 10px; subcontrol-position: bottom; subcontrol-origin: margin; }
# QScrollBar::sub-line:vertical:hover,QScrollBar::sub-line:vertical:on { border-image: url(:/qss_icons/rc/up_arrow.png); height: 10px; width: 10px; subcontrol-position: top; subcontrol-origin: margin; }
# QScrollBar::add-line:vertical:hover, QScrollBar::add-line:vertical:on { border-image: url(:/qss_icons/rc/down_arrow.png); height: 10px; width: 10px; subcontrol-position: bottom; subcontrol-origin: margin; }
# QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical { background: none; }
# QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: none; }
