"""Stylesheet module

"""

from subtitld.modules.paths import get_graphics_path


def set_stylesheet(self):
    """Function to set stylesheet on self"""
    stylesheet_text = '''
                            #background_label                                    { background: qlineargradient( x1:0 y1:0, x2:0 y2:1, stop:0 rgb(7,9,11), stop:1 rgb(26,35,43)); }
                            #background_label2                                   { background: qlineargradient( x1:0 y1:0, x2:0 y2:1, stop:0 rgb(26,35,43), stop:1 rgb(46,62,76)); }
                            #background_watermark_label                          { image: url("''' + get_graphics_path('background_watermark.png') + '''"); }
                            #subtitles_list_widget                               { border-top: 81px; border-right: 25px;  border-bottom: 0;    border-left: 0;    border-image: url("''' + get_graphics_path('subtitle_list_widget_background.png') + '''")     81  25  0  0 stretch stretch; }
                            #global_subtitlesvideo_panel_left                    { border-top: 0;    border-right: 0;     border-bottom: 0;    border-left: 0;    border-image: url("''' + get_graphics_path('global_config_subtitles_background.png') + '''")  0  0  0  0 stretch stretch; }
                            #global_subtitlesvideo_panel_right                   { border-top: 0;    border-right: 2px;   border-bottom: 0;    border-left: 0;    border-image: url("''' + get_graphics_path('global_config_video_background.png') + '''")      0  2  0  5 stretch stretch; }
                            #global_properties_panel                             { border-top: 0;    border-right: 0;     border-bottom: 0;    border-left: 2px;  border-image: url("''' + get_graphics_path('global_config_properties_background.png') + '''") 0  0  0  2 stretch stretch; }
                            #subtitles_list_top_widget                           { border-top: 0;    border-right: 0;     border-bottom: 2px;  border-left: 0;    border-image: url("''' + get_graphics_path('subtitle_list_top_background.png') + '''")        0  0  2  0 stretch stretch; }
                            #properties_widget                                   { border-top: 81px; border-right: 0;     border-bottom: 0;    border-left: 25px; border-image: url("''' + get_graphics_path('properties_widget_background.png') + '''")        81  0  0  25 stretch stretch; }
                            #playercontrols_widget_central_top_background        { border-top: 0;    border-right: 0;     border-bottom: 0;    border-left: 0;    border-image: url("''' + get_graphics_path('timeline_top_controls_background.png') + '''")    0  0  0  0 stretch stretch; }
                            #playercontrols_widget_central_top                   { border-top: 0;    border-right: 18px;  border-bottom: 0;    border-left: 18px; border-image: url("''' + get_graphics_path('timeline_top_controls.png') + '''")               0 18 0 18 stretch stretch; }
                            #playercontrols_widget_central_bottom_background     { border-top: 0;    border-right: 0;     border-bottom: 0;    border-left: 0;    border-image: url("''' + get_graphics_path('timeline_bottom_controls_background.png') + '''") 0 0 0 0 stretch stretch; }
                            #playercontrols_widget_central_bottom                { border-top: 0;    border-right: 12px;  border-bottom: 0;    border-left: 12px; border-image: url("''' + get_graphics_path('timeline_bottom_controls.png') + '''")            0 12 0 12 stretch stretch; }
                            #playercontrols_widget_top_left                      { border-top: 0;    border-right: 0;     border-bottom: 0;    border-left: 39px; border-image: url("''' + get_graphics_path('timeline_top_controls.png') + '''")               0 38 0 1 stretch stretch; }
                            #playercontrols_widget_bottom_left                   { border-top: 0;    border-right: 0;     border-bottom: 0;    border-left: 25px; border-image: url("''' + get_graphics_path('timeline_bottom_controls.png') + '''")            0 24 0 1 stretch stretch; }
                            #playercontrols_widget_top_right                     { border-top: 0;    border-right: 25px;  border-bottom: 0;    border-left: 0;    border-image: url("''' + get_graphics_path('timeline_top_controls.png') + '''")               0 1 0 38 stretch stretch; }
                            #playercontrols_widget_bottom_right                  { border-top: 0;    border-right: 25px;  border-bottom: 0;    border-left: 0;    border-image: url("''' + get_graphics_path('timeline_bottom_controls.png') + '''")            0 1 0 24 stretch stretch; }
                            #player_border                                       { border-top: 5px;  border-right: 5px;   border-bottom: 5px;  border-left: 5px;  border-image: url("''' + get_graphics_path('video_border.png') + '''")                        5 5 5 5 stretch stretch; }
                            #playercontrols_timecode_label                       { font-size:14px; color: rgba(106, 116, 131,100); qproperty-alignment: "AlignCenter"; font-family:"Ubuntu Mono"; }

                            #player_controls_button                              { border-top: 0;    border-right: 15px;  border-bottom: 0;    border-left: 15px; border-image: url("''' + get_graphics_path('player_controls_button_normal.png') + '''")          0 15 0 15 stretch stretch; }
                            #player_controls_button:hover:pressed                { border-top: 0;    border-right: 15px;  border-bottom: 0;    border-left: 15px; border-image: url("''' + get_graphics_path('player_controls_button_pressed.png') + '''")          0 15 0 15 stretch stretch; }
                            #player_controls_button:checked                      { border-top: 0;    border-right: 15px;  border-bottom: 0;    border-left: 15px; border-image: url("''' + get_graphics_path('player_controls_button_pressed.png') + '''")          0 15 0 15 stretch stretch; }
                            #player_controls_button:hover:checked                { border-top: 0;    border-right: 15px;  border-bottom: 0;    border-left: 15px; border-image: url("''' + get_graphics_path('player_controls_button_pressed.png') + '''")          0 15 0 15 stretch stretch; }
                            #player_controls_button:hover                        { border-top: 0;    border-right: 15px;  border-bottom: 0;    border-left: 15px; border-image: url("''' + get_graphics_path('player_controls_button_hover.png') + '''")          0 15 0 15 stretch stretch; }
                            #player_controls_button:disabled                     { border-top: 0;    border-right: 15px;  border-bottom: 0;    border-left: 15px; border-image: url("''' + get_graphics_path('player_controls_button_normal.png') + '''")          0 15 0 15 stretch stretch; color:rgba(255,255,255,100);}

                            #subtitles_list_toggle_button                        { border-top: 0;    border-right: 0;     border-bottom: 0;    border-left: 0;    border-image: url("''' + get_graphics_path('subtitles_list_toggle_button_normal.png') + '''")            0 0 0 0 stretch stretch; }
                            #subtitles_list_toggle_button:hover:pressed          { border-top: 0;    border-right: 0;     border-bottom: 0;    border-left: 0;    border-image: url("''' + get_graphics_path('subtitles_list_toggle_button_hover_pressed.png') + '''")            0 0 0 0 stretch stretch; }
                            #subtitles_list_toggle_button:checked                { border-top: 0;    border-right: 0;     border-bottom: 0;    border-left: 0;    border-image: url("''' + get_graphics_path('subtitles_list_toggle_button_pressed.png') + '''")            0 0 0 0 stretch stretch; }
                            #subtitles_list_toggle_button:hover:checked          { border-top: 0;    border-right: 0;     border-bottom: 0;    border-left: 0;    border-image: url("''' + get_graphics_path('subtitles_list_toggle_button_hover_pressed.png') + '''")            0 0 0 0 stretch stretch; }
                            #subtitles_list_toggle_button:hover                  { border-top: 0;    border-right: 0;     border-bottom: 0;    border-left: 0;    border-image: url("''' + get_graphics_path('subtitles_list_toggle_button_hover.png') + '''")            0 0 0 0 stretch stretch; }
                            #subtitles_list_toggle_button:disabled               { border-top: 0;    border-right: 0;     border-bottom: 0;    border-left: 0;    border-image: url("''' + get_graphics_path('subtitles_list_toggle_button_normal.png') + '''")            0 0 0 0 stretch stretch; }

                            #properties_toggle_button                            { border-top: 0;    border-right: 0;     border-bottom: 0;    border-left: 0;    border-image: url("''' + get_graphics_path('properties_toggle_button_normal.png') + '''")            0 0 0 0 stretch stretch; }
                            #properties_toggle_button:hover:pressed              { border-top: 0;    border-right: 0;     border-bottom: 0;    border-left: 0;    border-image: url("''' + get_graphics_path('properties_toggle_button_hover_pressed.png') + '''")            0 0 0 0 stretch stretch; }
                            #properties_toggle_button:checked                    { border-top: 0;    border-right: 0;     border-bottom: 0;    border-left: 0;    border-image: url("''' + get_graphics_path('properties_toggle_button_pressed.png') + '''")            0 0 0 0 stretch stretch; }
                            #properties_toggle_button:hover:checked              { border-top: 0;    border-right: 0;     border-bottom: 0;    border-left: 0;    border-image: url("''' + get_graphics_path('properties_toggle_button_hover_pressed.png') + '''")            0 0 0 0 stretch stretch; }
                            #properties_toggle_button:hover                      { border-top: 0;    border-right: 0;     border-bottom: 0;    border-left: 0;    border-image: url("''' + get_graphics_path('properties_toggle_button_hover.png') + '''")            0 0 0 0 stretch stretch; }
                            #properties_toggle_button:disabled                   { border-top: 0;    border-right: 0;     border-bottom: 0;    border-left: 0;    border-image: url("''' + get_graphics_path('properties_toggle_button_normal.png') + '''")            0 0 0 0 stretch stretch; }

                            #playercontrols_properties_panel_toggle                            { border: 0; background-image: url("''' + get_graphics_path('playercontrols_properties_panel_toggle_normal.svg') + '''"); background-repeat: no-repeat; background-position: center right; }
                            #playercontrols_properties_panel_toggle:hover:pressed              { border: 0; background-image: url("''' + get_graphics_path('playercontrols_properties_panel_toggle_pressed_hover.svg') + '''"); background-repeat: no-repeat; background-position: center right; }
                            #playercontrols_properties_panel_toggle:checked                    { border: 0; background-image: url("''' + get_graphics_path('playercontrols_properties_panel_toggle_pressed.svg') + '''"); background-repeat: no-repeat; background-position: center right; }
                            #playercontrols_properties_panel_toggle:hover:checked              { border: 0; background-image: url("''' + get_graphics_path('playercontrols_properties_panel_toggle_pressed_hover.svg') + '''"); background-repeat: no-repeat; background-position: center right; }
                            #playercontrols_properties_panel_toggle:hover                      { border: 0; background-image: url("''' + get_graphics_path('playercontrols_properties_panel_toggle_hover.svg') + '''"); background-repeat: no-repeat; background-position: center right; }
                            #playercontrols_properties_panel_toggle:disabled                   { border: 0; background-image: url("''' + get_graphics_path('playercontrols_properties_panel_toggle_normal.svg') + '''"); background-repeat: no-repeat; background-position: center right; }

                            #player_controls_sub_panel                           { border-top: 5px; border-right: 5px; border-bottom: 5px; border-left: 5px; border-image: url("''' + get_graphics_path('player_controls_sub_panel.svg') + '''") 5 5 5 5 stretch stretch; }

                            #playercontrols_widget                               { border-top: 108px; border-right: 0; border-bottom: 0; border-left: 0; border-image: url("''' + get_graphics_path('timeline_background.png') + '''") 108 0 0 0 stretch stretch; }
                            #timeline_scroll                                     { background-color:transparent; }
                            #timeline_widget                                     { background-color:transparent; }

                            #toppanel_widget_left                                { border-top: 0;    border-right: 16px;  border-bottom: 55px;    border-left: 0;    border-image: url("''' + get_graphics_path('toppanel_background_left.png') + '''")          0 16 55 0 stretch stretch; }
                            #toppanel_widget_right                               { border-top: 0;    border-right: 18px;  border-bottom: 55px;    border-left: 5px;  border-image: url("''' + get_graphics_path('toppanel_background_right.png') + '''")          0 18 55 5 stretch stretch; }
                            #videoinfo_label                                     { font-size:12px; color: rgba(106, 116, 131,100); qproperty-alignment: "AlignCenter"; font-family:"Ubuntu Mono"; }
                            #toppanel_subtitle_file_info_label                   { font-size:10px; color: rgba(48, 66, 81,255); qproperty-alignment: "AlignVCenter | AlignLeft"; qproperty-wordWrap: true }

                            QPushButton                                          { font-size:10px; color:white; }
                            #start_screen_recent_alert                           { font-size:14px; color: rgb(106, 116, 131); qproperty-alignment: "AlignCenter"; padding: 40px; }

                            #properties_information                              { font-size:12px; color:white; qproperty-alignment: "AlignTop";  }

                            #player_subtitle_layer                               { font-size:40px; color: rgb(255, 255, 255); qproperty-alignment: "AlignCenter | AlignBottom"; padding: 10px; }
                            #properties_textedit                                 { margin-left:2px; margin-right:2px; font-size:26px; color: black; border-bottom-right-radius: 4px; border-bottom-left-radius: 4px; }
                            #subtitles_list_qlistwidget                          { outline: none; font-size:14px; color:rgb(106, 116, 131); border-top-right-radius: 4px; background-color: rgba(255, 255, 255, 200); padding:5px;} QListWidget::item { padding:5px; border-radius: 2px;} QListWidget::item:selected { background:rgb(184, 206, 224); color:rgb(106, 116, 131); }
                            #start_screen_recent_listwidget                      { outline: none; font-size:14px; color:rgb(106, 116, 131); border-radius: 4px; background-color: rgba(106, 116, 131, 20); padding:5px;} QListWidget::item { padding:5px; border-radius: 2px;} QListWidget::item:selected { background:rgb(184, 206, 224); color:rgb(106, 116, 131); }

                            QScrollBar:horizontal                                { height: 15px; margin: 2px 2px 2px 2px; border: 1px transparent rgba(0,0,0,50); border-radius: 2px; background-color: rgba(0,0,0,50); }
                            QScrollBar::handle:horizontal                        { background-color: rgba(106,116,131,150); min-width: 5px; border-radius: 2px; }
                            QScrollBar::add-line:horizontal                      { border: none; background: none; }
                            QScrollBar::sub-line:horizontal                      { border: none; background: none; }
                            QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal { background: none; }
                            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal { background: none; }

                            QScrollBar:vertical                                { width: 15px; margin: 2px 2px 2px 2px; border: 1px transparent rgba(0,0,0,50); border-radius: 2px; background-color: rgba(0,0,0,50); }
                            QScrollBar::handle:vertical                        { background-color: rgba(0,0,0,50); min-width: 5px; border-radius: 2px; }
                            QScrollBar::add-line:vertical                      { border: none; background: none; }
                            QScrollBar::sub-line:vertical                      { border: none; background: none; }
                            QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical { background: none; }
                            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: none; }

                            #start_screen_recentfiles_background                 { background-color: rgba(106, 116, 131, 50); }
                            #start_screen_adver_panel                            { background-color: rgba(0, 0, 0, 50); border-radius: 5px;}
                            #start_screen_top_shadow                             { border-left: 0; border-top: 1px; border-right: 0; border-bottom: 0; border-image: url("''' + get_graphics_path('start_screen_top_shadow.png') + '''") 1 0 0 0 stretch stretch; outline: none; }
                            #start_screen_open_label                             { font-size:10px; color:rgb(106, 116, 131); qproperty-alignment: "AlignVCenter | AlignRight"; qproperty-wordWrap: true}
                            #start_screen_recent_label                           { font-size:10px; color:rgb(106, 116, 131); qproperty-alignment: "AlignCenter"; qproperty-wordWrap: true}
                            #start_screen_adver_label                            { font-size:10px; color:rgb(106, 116, 131); qproperty-alignment: "AlignVCenter | AlignLeft"; qproperty-wordWrap: true}
                            #start_screen_adver_panel_label                      { font-size:10px; color:rgb(106, 116, 131); qproperty-alignment: "AlignCenter"; qproperty-wordWrap: true; font-weight: bold;}
                            #start_screen_adver_label_details                    { font-size:14px; color:rgb(106, 116, 131); qproperty-alignment: "AlignTop | AlignLeft"; qproperty-wordWrap: true}
                            #start_screen_adver_label_machineid                  { font-size:24px; color:rgb(106, 116, 131); qproperty-alignment: "AlignCenter"; font-weight: bold; }
                            #start_screen_adver_label_status                     { font-size:14px; color:rgb(106, 116, 131); qproperty-alignment: "AlignCenter"; padding-left:20px; padding-right:20px;  qproperty-wordWrap: true; }
                            #start_screen_adver_label_email                      { padding:10px; border: 1px transparent rgba(255,255,255,20); border-radius: 2px; background-color: rgba(255,255,255,200); color:rgb(48,66,81); font-size:14px;  qproperty-alignment: "AlignCenter"; }

                            #small_label                                         { font-size:7px; color:rgb(26,35,43); qproperty-wordWrap: true}

                            #controls_qspinbox                                   { padding-left:1px; border-width: 1; border-color: rgba(0,0,0,100); background-color: rgba(255,255,255,50); min-width: 5px; border-radius: 2px; font-size:10px; color:rgba(48,66,81,255) }
                            #controls_qdoublespinbox                             { padding-left:1px; border-width: 1; border-color: rgba(0,0,0,100); background-color: rgba(255,255,255,50); min-width: 5px; border-radius: 2px; font-size:10px; color:rgba(48,66,81,255) }
                            #controls_combobox                                   { padding-left:1px; border-width: 1; border-color: rgba(0,0,0,100); background-color: rgba(255,255,255,50); min-width: 5px; border-radius: 2px; font-size:10px; color:rgba(48,66,81,255) }

                            QMessageBox                                          { background-color:rgb(26,35,43); }
                            QMessageBox QLabel                                   { color: rgb(106, 116, 131); }
                            QMessageBox QPushButton                              { background-color: rgb(106, 116, 131); }

                            QTabBar:tab                                          { background: rgba(184,206,224,150); color: rgba(46,62,76,150); border: 1px solid rgba(106, 116, 131, 100); padding: 10px; border-top-left-radius: 2px; border-top-right-radius: 2px; border-bottom:0; }
                            QTabBar:tab:selected                                 { background: rgb(184,206,224); color: rgb(46,62,76); border: 1px solid rgb(106, 116, 131); border-bottom:0; }
                            QTabWidget:pane                                      { background: rgb(184,206,224); border: 1px solid rgb(106, 116, 131); border-bottom-left-radius: 2px; border-bottom-right-radius: 2px; border-top: 0;}
                            '''

    for button_color in ['button', 'button_dark', 'button_red', 'button_green']:
        stylesheet_text += '#' + button_color + '                                { font-size:11px; border-left:5px; border-top:5px; border-right:5px; border-bottom:5px; border-image: url("' + get_graphics_path(button_color + '_normal.png') + '") 5 5 5 5 stretch stretch; outline: none; } '
        stylesheet_text += '#' + button_color + ':hover:pressed                  { font-size:11px; border-left:5px; border-top:5px; border-right:5px; border-bottom:5px; border-image: url("' + get_graphics_path(button_color + '_pressed.png') + '") 5 5 5 5 stretch stretch; outline: none;  } '
        stylesheet_text += '#' + button_color + ':checked                        { font-size:11px; border-left:5px; border-top:5px; border-right:5px; border-bottom:5px; border-image: url("' + get_graphics_path(button_color + '_pressed.png') + '") 5 5 5 5 stretch stretch; outline: none;  } '
        stylesheet_text += '#' + button_color + ':hover:checked                  { font-size:11px; border-left:5px; border-top:5px; border-right:5px; border-bottom:5px; border-image: url("' + get_graphics_path(button_color + '_pressed.png') + '") 5 5 5 5 stretch stretch; outline: none;  } '
        stylesheet_text += '#' + button_color + ':hover                          { font-size:11px; border-left:5px; border-top:5px; border-right:5px; border-bottom:5px; border-image: url("' + get_graphics_path(button_color + '_hover.png') + '") 5 5 5 5 stretch stretch; outline: none; } '
        stylesheet_text += '#' + button_color + ':disabled                       { font-size:11px; border-left:5px; border-top:5px; border-right:5px; border-bottom:5px; border-image: url("' + get_graphics_path(button_color + '_disabled.png') + '") 5 5 5 5 stretch stretch; outline: none; color:rgba(255,255,255,100); }'

    for button_color in ['subbutton', 'subbutton_dark']:
        stylesheet_text += '#' + button_color + '                                { padding-left:4px; font-size:10px; border-left:5px; border-top:2px; border-right:2px; border-bottom:2px; border-image: url("' + get_graphics_path(button_color + '_normal.png') + '") 2 2 2 5 stretch stretch; outline: none; color:rgba(48,66,81,255); text-align:left; font-weight:bold;} '
        stylesheet_text += '#' + button_color + ':hover:pressed                  { padding-left:4px; font-size:10px; border-left:5px; border-top:2px; border-right:2px; border-bottom:2px; border-image: url("' + get_graphics_path(button_color + '_pressed.png') + '") 2 2 2 5 stretch stretch; outline: none;  } '
        stylesheet_text += '#' + button_color + ':checked                        { padding-left:4px; font-size:10px; border-left:5px; border-top:2px; border-right:2px; border-bottom:2px; border-image: url("' + get_graphics_path(button_color + '_pressed.png') + '") 2 2 2 5 stretch stretch; outline: none;  } '
        stylesheet_text += '#' + button_color + ':hover:checked                  { padding-left:4px; font-size:10px; border-left:5px; border-top:2px; border-right:2px; border-bottom:2px; border-image: url("' + get_graphics_path(button_color + '_pressed.png') + '") 2 2 2 5 stretch stretch; outline: none;  } '
        stylesheet_text += '#' + button_color + ':hover                          { padding-left:4px; font-size:10px; border-left:5px; border-top:2px; border-right:2px; border-bottom:2px; border-image: url("' + get_graphics_path(button_color + '_hover.png') + '") 2 2 2 5 stretch stretch; outline: none; } '
        stylesheet_text += '#' + button_color + ':disabled                       { padding-left:4px; font-size:10px; border-left:5px; border-top:2px; border-right:2px; border-bottom:2px; border-image: url("' + get_graphics_path(button_color + '_disabled.png') + '") 2 2 2 5 stretch stretch; outline: none; color:rgba(0,0,0,100); }'

    for button_color in ['subbutton2_dark', 'subbutton_left_dark', 'subbutton_right_dark']:
        stylesheet_text += '#' + button_color + '                                { font-size:10px; border-left:5px; border-top:2px; border-right:2px; border-bottom:2px; border-image: url("' + get_graphics_path(button_color + '_normal.png') + '") 2 2 2 5 stretch stretch; outline: none; color:rgba(48,66,81,255); text-align:left; font-weight:bold;} '
        stylesheet_text += '#' + button_color + ':hover:pressed                  { font-size:10px; border-left:5px; border-top:2px; border-right:2px; border-bottom:2px; border-image: url("' + get_graphics_path(button_color + '_pressed.png') + '") 2 2 2 5 stretch stretch; outline: none;  } '
        stylesheet_text += '#' + button_color + ':checked                        { font-size:10px; border-left:5px; border-top:2px; border-right:2px; border-bottom:2px; border-image: url("' + get_graphics_path(button_color + '_pressed.png') + '") 2 2 2 5 stretch stretch; outline: none;  } '
        stylesheet_text += '#' + button_color + ':hover:checked                  { font-size:10px; border-left:5px; border-top:2px; border-right:2px; border-bottom:2px; border-image: url("' + get_graphics_path(button_color + '_pressed.png') + '") 2 2 2 5 stretch stretch; outline: none;  } '
        stylesheet_text += '#' + button_color + ':hover                          { font-size:10px; border-left:5px; border-top:2px; border-right:2px; border-bottom:2px; border-image: url("' + get_graphics_path(button_color + '_hover.png') + '") 2 2 2 5 stretch stretch; outline: none; } '
        stylesheet_text += '#' + button_color + ':disabled                       { font-size:10px; border-left:5px; border-top:2px; border-right:2px; border-bottom:2px; border-image: url("' + get_graphics_path(button_color + '_disabled.png') + '") 2 2 2 5 stretch stretch; outline: none; color:rgba(0,0,0,100); }'

    for button_color in ['keyboard_key']:
        stylesheet_text += '#' + button_color + '                                { font-size:10px; border-left:8px; border-top:5px; border-right:8px; border-bottom:11px; border-image: url("' + get_graphics_path(button_color + '_normal.png') + '") 5 8 11 5 stretch stretch; outline: none; color:rgba(48,66,81,255); text-align:left; font-weight:bold;} '
        stylesheet_text += '#' + button_color + ':hover:pressed                  { font-size:10px; border-left:8px; border-top:5px; border-right:8px; border-bottom:11px; border-image: url("' + get_graphics_path(button_color + '_pressed.png') + '") 5 8 11 5 stretch stretch; outline: none;  } '
        stylesheet_text += '#' + button_color + ':checked                        { font-size:10px; border-left:8px; border-top:5px; border-right:8px; border-bottom:11px; border-image: url("' + get_graphics_path(button_color + '_pressed.png') + '") 5 8 11 5 stretch stretch; outline: none;  } '
        stylesheet_text += '#' + button_color + ':hover:checked                  { font-size:10px; border-left:8px; border-top:5px; border-right:8px; border-bottom:11px; border-image: url("' + get_graphics_path(button_color + '_pressed.png') + '") 5 8 11 5 stretch stretch; outline: none;  } '
        stylesheet_text += '#' + button_color + ':hover                          { font-size:10px; border-left:8px; border-top:5px; border-right:8px; border-bottom:11px; border-image: url("' + get_graphics_path(button_color + '_hover.png') + '") 5 8 11 5 stretch stretch; outline: none; } '
        stylesheet_text += '#' + button_color + ':disabled                       { font-size:10px; border-left:8px; border-top:5px; border-right:8px; border-bottom:11px; border-image: url("' + get_graphics_path(button_color + '_disabled.png') + '") 5 8 11 5 stretch stretch; outline: none; color:rgba(0,0,0,100); }'

    self.setStyleSheet(stylesheet_text)
