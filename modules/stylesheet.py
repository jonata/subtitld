#!/usr/bin/python3
# -*- coding: utf-8 -*-

from modules.paths import *

def set_stylesheet(self):
    stylesheet_text = '''
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

                            #properties_information                     { font-size:12px; color:white; }

                            #player_subtitle_layer                      { font-size:40px; color: rgb(255, 255, 255); qproperty-alignment: "AlignCenter | AlignBottom"; padding: 10px; }
                            #player_subtitle_textedit                   { padding:10px; font-size:32px; color: rgb(0, 0, 0); }
                            #subtitles_list_qlistwidget                 { outline: none; font-size:14px; color:rgb(106, 116, 131); border-top-right-radius: 4px; background-color: rgba(255, 255, 255, 200); padding:5px;} QListWidget::item { padding:5px; border-radius: 2px;} QListWidget::item:selected { background:rgb(184, 206, 224); color:rgb(106, 116, 131); }
                            #start_screen_recent_listwidget             { outline: none; font-size:14px; color:rgb(106, 116, 131); border-radius: 4px; background-color: rgba(106, 116, 131, 20); padding:5px;} QListWidget::item { padding:5px; border-radius: 2px;} QListWidget::item:selected { background:rgb(184, 206, 224); color:rgb(106, 116, 131); }

                            QScrollBar:horizontal                       { height: 15px; margin: 2px 2px 2px 2px; border: 1px transparent rgba(0,0,0,50); border-radius: 2px; background-color: rgba(0,0,0,50); }
                            QScrollBar::handle:horizontal               { background-color: rgba(0,0,0,50); min-width: 5px; border-radius: 2px; }
                            QScrollBar::add-line:horizontal             { border: none; background: none; }
                            QScrollBar::sub-line:horizontal             { border: none; background: none; }
                            QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal { background: none; }
                            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal { background: none; }

                            #start_screen_recentfiles_background        { background-color: rgba(106, 116, 131, 50); }
                            #start_screen_adver_panel                   { background-color: rgba(0, 0, 0, 50); border-radius: 5px;}
                            #start_screen_top_shadow                    { border-left: 0; border-top: 1px; border-right: 0; border-bottom: 0; border-image: url("''' + get_graphics_path('start_screen_top_shadow.png') + '''") 1 0 0 0 stretch stretch; outline: none; }
                            #start_screen_open_label                    { font-size:10px; color:rgb(106, 116, 131); qproperty-alignment: "AlignVCenter | AlignRight"; qproperty-wordWrap: true}
                            #start_screen_recent_label                  { font-size:10px; color:rgb(106, 116, 131); qproperty-alignment: "AlignCenter"; qproperty-wordWrap: true}
                            #start_screen_adver_label                   { font-size:10px; color:rgb(106, 116, 131); qproperty-alignment: "AlignVCenter | AlignLeft"; qproperty-wordWrap: true}
                            #start_screen_adver_panel_label             { font-size:10px; color:rgb(106, 116, 131); qproperty-alignment: "AlignCenter"; qproperty-wordWrap: true; font-weight: bold;}
                            #start_screen_adver_label_details           { font-size:14px; color:rgb(106, 116, 131); qproperty-alignment: "AlignTop | AlignLeft"; qproperty-wordWrap: true}
                            #start_screen_adver_label_machineid         { font-size:24px; color:rgb(106, 116, 131); qproperty-alignment: "AlignCenter"; font-weight: bold; }
                            #start_screen_adver_label_status            { font-size:14px; color:rgb(106, 116, 131); qproperty-alignment: "AlignCenter"; padding-left:20px; padding-right:20px;  qproperty-wordWrap: true; }
                            #start_screen_adver_label_email             { padding:10px; border: 1px transparent rgba(255,255,255,20); border-radius: 2px; background-color: rgba(255,255,255,200); color:rgb(48,66,81); font-size:14px;  qproperty-alignment: "AlignCenter"; }
                            '''

    for button_color in ['button', 'button_dark', 'button_red', 'button_green']:
        sides = ['left','top','right','bottom','']
        for crop1 in sides:
            c = ['5px', '5px', '5px', '5px']
            if crop1:
                c[sides.index(crop1)] = '0'
                crop1 = '_no_' + crop1
            for crop2 in sides:

                if (crop1 and not crop2) or (not crop1 == crop2) or (not crop1 or not crop2):
                    c1 = c.copy()
                    print(sides)
                    print(crop2)
                    print(sides.index(crop2))
                    print(c1)
                    if crop2:
                        c1[sides.index(crop2)] = '0'
                        crop2 = '_no_' + crop2
                    stylesheet_text += '#' + button_color + crop1 + crop2 + '                                { font-size:11px; border-left: ' + c1[0] + '; border-top: ' + c1[1] + '; border-right: ' + c1[2] + '; border-bottom: ' + c1[3] + '; border-image: url("' + get_graphics_path(button_color + '_normal.png') + '") 5 5 5 5 stretch stretch; outline: none; } '
                    stylesheet_text += '#' + button_color + crop1 + crop2 + ':hover:pressed                  { font-size:11px; border-left: ' + c1[0] + '; border-top: ' + c1[1] + '; border-right: ' + c1[2] + '; border-bottom: ' + c1[3] + '; border-image: url("' + get_graphics_path(button_color + '_pressed.png') + '") 5 5 5 5 stretch stretch; outline: none;  } '
                    stylesheet_text += '#' + button_color + crop1 + crop2 + ':checked                        { font-size:11px; border-left: ' + c1[0] + '; border-top: ' + c1[1] + '; border-right: ' + c1[2] + '; border-bottom: ' + c1[3] + '; border-image: url("' + get_graphics_path(button_color + '_pressed.png') + '") 5 5 5 5 stretch stretch; outline: none;  } '
                    stylesheet_text += '#' + button_color + crop1 + crop2 + ':hover:checked                  { font-size:11px; border-left: ' + c1[0] + '; border-top: ' + c1[1] + '; border-right: ' + c1[2] + '; border-bottom: ' + c1[3] + '; border-image: url("' + get_graphics_path(button_color + '_pressed.png') + '") 5 5 5 5 stretch stretch; outline: none;  } '
                    stylesheet_text += '#' + button_color + crop1 + crop2 + ':hover                          { font-size:11px; border-left: ' + c1[0] + '; border-top: ' + c1[1] + '; border-right: ' + c1[2] + '; border-bottom: ' + c1[3] + '; border-image: url("' + get_graphics_path(button_color + '_hover.png') + '") 5 5 5 5 stretch stretch; outline: none; } '
                    stylesheet_text += '#' + button_color + crop1 + crop2 + ':disabled                       { font-size:11px; border-left: ' + c1[0] + '; border-top: ' + c1[1] + '; border-right: ' + c1[2] + '; border-bottom: ' + c1[3] + '; border-image: url("' + get_graphics_path(button_color + '_disabled.png') + '") 5 5 5 5 stretch stretch; outline: none; color:rgba(255,255,255,100); }'

    self.setStyleSheet(stylesheet_text)


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
