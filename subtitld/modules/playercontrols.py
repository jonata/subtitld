"""Player control widgets.

"""

import os
from bisect import bisect
from PyQt5.QtWidgets import QPushButton, QLabel, QDoubleSpinBox, QSlider, QSpinBox, QComboBox, QTabWidget, QWidget, QStylePainter, QStyleOptionTab, QStyle, QTabBar, QColorDialog
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, Qt, QSize, QRect, QPoint, QThread
from PyQt5.QtGui import QIcon

from subtitld.modules import subtitles
from subtitld.modules.paths import PATH_SUBTITLD_GRAPHICS

STEPS_LIST = ['Frames', 'Seconds']

class QLeftTabBar(QTabBar):
    def tabSizeHint(self, index):
        s = QTabBar.tabSizeHint(self, index)
        s.transpose()
        return s

    def paintEvent(self, event):
        painter = QStylePainter(self)
        opt = QStyleOptionTab()

        for i in range(self.count()):
            self.initStyleOption(opt, i)
            painter.drawControl(QStyle.CE_TabBarTabShape, opt)
            painter.save()

            s = opt.rect.size()
            s.transpose()
            r = QRect(QPoint(), s)
            r.moveCenter(opt.rect.center())
            opt.rect = r

            c = self.tabRect(i).center()
            painter.translate(c)
            painter.rotate(90)
            painter.translate(-c)
            painter.drawControl(QStyle.CE_TabBarTabLabel, opt)
            painter.restore()

def load(self):
    """Function to load player control widgets"""
    self.playercontrols_widget = QLabel(parent=self)
    self.playercontrols_widget.setObjectName('playercontrols_widget')
    self.playercontrols_widget_animation = QPropertyAnimation(self.playercontrols_widget, b'geometry')
    self.playercontrols_widget_animation.setEasingCurve(QEasingCurve.OutCirc)

    self.timeline.load(self)

    self.playercontrols_properties_panel_placeholder = QWidget(parent=self.playercontrols_widget)

    self.playercontrols_properties_panel = QLabel(parent=self.playercontrols_properties_panel_placeholder)
    self.playercontrols_properties_panel.setObjectName('player_controls_sub_panel')
    self.playercontrols_properties_panel.setStyleSheet('QLabel {border-top:0; border-right:0;}')
    self.playercontrols_properties_panel_animation = QPropertyAnimation(self.playercontrols_properties_panel, b'geometry')
    self.playercontrols_properties_panel_animation.setEasingCurve(QEasingCurve.OutCirc)

    self.playercontrols_properties_panel_tabwidget = QTabWidget(parent=self.playercontrols_properties_panel)
    self.playercontrols_properties_panel_tabwidget.setTabBar(QLeftTabBar(self.playercontrols_properties_panel_tabwidget))
    self.playercontrols_properties_panel_tabwidget.setTabPosition(2)
    self.playercontrols_properties_panel_tabwidget.setStyleSheet('''
                            QTabBar:tab                                    { background: rgba(184,206,224,150); color: rgba(46,62,76,150); border: 1px solid rgba(106, 116, 131, 100); padding: 10px; border-top-left-radius: 2px; border-top-right-radius: 0; border-bottom-left-radius: 2px; border-left:0; padding-top: -16px; padding-left: 4px; padding-bottom:6px; padding-right:2px; }
                            QTabBar:tab:selected                           { background: rgb(184,206,224); color: rgb(46,62,76); border: 1px solid rgb(106, 116, 131); border-right:0; }
                            QTabWidget:pane                                { background: rgb(184,206,224); border: 1px solid rgb(106, 116, 131); border-bottom-right-radius: 2px;  border-top-left-radius: 0; border-top-right-radius: 2px; border-left: 0;}
                            ''')

    self.playercontrols_properties_panel_tabwidget_subtitles = QWidget()

    self.playercontrols_properties_panel_tabwidget_subtitles_subtitle_title_normal = QLabel('Normal subtitle colors'.upper(), parent=self.playercontrols_properties_panel_tabwidget_subtitles)
    self.playercontrols_properties_panel_tabwidget_subtitles_subtitle_title_normal.setObjectName('small_label')
    self.playercontrols_properties_panel_tabwidget_subtitles_subtitle_title_normal.setStyleSheet(' QLabel {font-weight:bold;} ')

    self.playercontrols_properties_panel_tabwidget_subtitles_subtitle_border_color_title_normal = QLabel('Border'.upper(), parent=self.playercontrols_properties_panel_tabwidget_subtitles)
    self.playercontrols_properties_panel_tabwidget_subtitles_subtitle_border_color_title_normal.setObjectName('small_label')

    self.playercontrols_properties_panel_tabwidget_subtitles_subtitle_border_color_button = QPushButton(parent=self.playercontrols_properties_panel_tabwidget_subtitles)
    self.playercontrols_properties_panel_tabwidget_subtitles_subtitle_border_color_button.clicked.connect(lambda: playercontrols_properties_panel_tabwidget_subtitles_subtitle_border_color_button_clicked(self))

    self.playercontrols_properties_panel_tabwidget_subtitles_subtitle_fill_color_title_normal = QLabel('Fill'.upper(), parent=self.playercontrols_properties_panel_tabwidget_subtitles)
    self.playercontrols_properties_panel_tabwidget_subtitles_subtitle_fill_color_title_normal.setObjectName('small_label')

    self.playercontrols_properties_panel_tabwidget_subtitles_subtitle_fill_color_button = QPushButton(parent=self.playercontrols_properties_panel_tabwidget_subtitles)
    self.playercontrols_properties_panel_tabwidget_subtitles_subtitle_fill_color_button.clicked.connect(lambda: playercontrols_properties_panel_tabwidget_subtitles_subtitle_fill_color_button_clicked(self))

    self.playercontrols_properties_panel_tabwidget_subtitles_subtitle_text_color_title_normal = QLabel('Text'.upper(), parent=self.playercontrols_properties_panel_tabwidget_subtitles)
    self.playercontrols_properties_panel_tabwidget_subtitles_subtitle_text_color_title_normal.setObjectName('small_label')

    self.playercontrols_properties_panel_tabwidget_subtitles_subtitle_text_color_button = QPushButton(parent=self.playercontrols_properties_panel_tabwidget_subtitles)
    self.playercontrols_properties_panel_tabwidget_subtitles_subtitle_text_color_button.clicked.connect(lambda: playercontrols_properties_panel_tabwidget_subtitles_subtitle_text_color_button_clicked(self))

    self.playercontrols_properties_panel_tabwidget_subtitles_subtitle_title_selected = QLabel('Selected subtitle colors'.upper(), parent=self.playercontrols_properties_panel_tabwidget_subtitles)
    self.playercontrols_properties_panel_tabwidget_subtitles_subtitle_title_selected.setObjectName('small_label')
    self.playercontrols_properties_panel_tabwidget_subtitles_subtitle_title_selected.setStyleSheet(' QLabel {font-weight:bold;} ')

    self.playercontrols_properties_panel_tabwidget_subtitles_subtitle_border_color_title_selected = QLabel('Border'.upper(), parent=self.playercontrols_properties_panel_tabwidget_subtitles)
    self.playercontrols_properties_panel_tabwidget_subtitles_subtitle_border_color_title_selected.setObjectName('small_label')

    self.playercontrols_properties_panel_tabwidget_subtitles_selected_subtitle_border_color_button = QPushButton(parent=self.playercontrols_properties_panel_tabwidget_subtitles)
    self.playercontrols_properties_panel_tabwidget_subtitles_selected_subtitle_border_color_button.clicked.connect(lambda: playercontrols_properties_panel_tabwidget_subtitles_selected_subtitle_border_color_button_clicked(self))

    self.playercontrols_properties_panel_tabwidget_subtitles_subtitle_fill_color_title_selected = QLabel('Fill'.upper(), parent=self.playercontrols_properties_panel_tabwidget_subtitles)
    self.playercontrols_properties_panel_tabwidget_subtitles_subtitle_fill_color_title_selected.setObjectName('small_label')

    self.playercontrols_properties_panel_tabwidget_subtitles_selected_subtitle_fill_color_button = QPushButton(parent=self.playercontrols_properties_panel_tabwidget_subtitles)
    self.playercontrols_properties_panel_tabwidget_subtitles_selected_subtitle_fill_color_button.clicked.connect(lambda: playercontrols_properties_panel_tabwidget_subtitles_selected_subtitle_fill_color_button_clicked(self))

    self.playercontrols_properties_panel_tabwidget_subtitles_subtitle_text_color_title_selected = QLabel('Text'.upper(), parent=self.playercontrols_properties_panel_tabwidget_subtitles)
    self.playercontrols_properties_panel_tabwidget_subtitles_subtitle_text_color_title_selected.setObjectName('small_label')

    self.playercontrols_properties_panel_tabwidget_subtitles_selected_subtitle_text_color_button = QPushButton(parent=self.playercontrols_properties_panel_tabwidget_subtitles)
    self.playercontrols_properties_panel_tabwidget_subtitles_selected_subtitle_text_color_button.clicked.connect(lambda: playercontrols_properties_panel_tabwidget_subtitles_selected_subtitle_text_color_button_clicked(self))

    self.playercontrols_properties_panel_tabwidget_subtitles_subtitle_title_arrows = QLabel('Arrows colors'.upper(), parent=self.playercontrols_properties_panel_tabwidget_subtitles)
    self.playercontrols_properties_panel_tabwidget_subtitles_subtitle_title_arrows.setObjectName('small_label')
    self.playercontrols_properties_panel_tabwidget_subtitles_subtitle_title_arrows.setStyleSheet(' QLabel {font-weight:bold;} ')

    self.playercontrols_properties_panel_tabwidget_subtitles_subtitle_title_normal_arrows = QLabel('Normal'.upper(), parent=self.playercontrols_properties_panel_tabwidget_subtitles)
    self.playercontrols_properties_panel_tabwidget_subtitles_subtitle_title_normal_arrows.setObjectName('small_label')

    self.playercontrols_properties_panel_tabwidget_subtitles_subtitle_arrow_normal_button = QPushButton(parent=self.playercontrols_properties_panel_tabwidget_subtitles)
    self.playercontrols_properties_panel_tabwidget_subtitles_subtitle_arrow_normal_button.clicked.connect(lambda: playercontrols_properties_panel_tabwidget_subtitles_subtitle_arrow_normal_button_clicked(self))

    self.playercontrols_properties_panel_tabwidget_subtitles_selected_subtitle_title_normal_arrows = QLabel('Selected'.upper(), parent=self.playercontrols_properties_panel_tabwidget_subtitles)
    self.playercontrols_properties_panel_tabwidget_subtitles_selected_subtitle_title_normal_arrows.setObjectName('small_label')

    self.playercontrols_properties_panel_tabwidget_subtitles_selected_subtitle_arrow_normal_button = QPushButton(parent=self.playercontrols_properties_panel_tabwidget_subtitles)
    self.playercontrols_properties_panel_tabwidget_subtitles_selected_subtitle_arrow_normal_button.clicked.connect(lambda: playercontrols_properties_panel_tabwidget_subtitles_selected_subtitle_arrow_normal_button_clicked(self))

    self.playercontrols_properties_panel_tabwidget.addTab(self.playercontrols_properties_panel_tabwidget_subtitles, '')
    self.playercontrols_properties_panel_tabwidget.setTabIcon(0, QIcon(os.path.join(PATH_SUBTITLD_GRAPHICS, 'playercontrols_properties_panel_subtitle_icon.svg')))

    self.playercontrols_properties_panel_tabwidget_waveform = QWidget()

    self.playercontrols_properties_panel_tabwidget_waveform_title_normal = QLabel('Waveform colors'.upper(), parent=self.playercontrols_properties_panel_tabwidget_waveform)
    self.playercontrols_properties_panel_tabwidget_waveform_title_normal.setObjectName('small_label')
    self.playercontrols_properties_panel_tabwidget_waveform_title_normal.setStyleSheet(' QLabel {font-weight:bold;} ')

    self.playercontrols_properties_panel_tabwidget_waveform_border_color_title_normal = QLabel('Border'.upper(), parent=self.playercontrols_properties_panel_tabwidget_waveform)
    self.playercontrols_properties_panel_tabwidget_waveform_border_color_title_normal.setObjectName('small_label')

    self.playercontrols_properties_panel_tabwidget_waveform_border_color_button = QPushButton(parent=self.playercontrols_properties_panel_tabwidget_waveform)
    self.playercontrols_properties_panel_tabwidget_waveform_border_color_button.clicked.connect(lambda: playercontrols_properties_panel_tabwidget_waveform_border_color_button_clicked(self))

    self.playercontrols_properties_panel_tabwidget_waveform_fill_color_title_normal = QLabel('Fill'.upper(), parent=self.playercontrols_properties_panel_tabwidget_waveform)
    self.playercontrols_properties_panel_tabwidget_waveform_fill_color_title_normal.setObjectName('small_label')

    self.playercontrols_properties_panel_tabwidget_waveform_fill_color_button = QPushButton(parent=self.playercontrols_properties_panel_tabwidget_waveform)
    self.playercontrols_properties_panel_tabwidget_waveform_fill_color_button.clicked.connect(lambda: playercontrols_properties_panel_tabwidget_waveform_fill_color_button_clicked(self))

    self.playercontrols_properties_panel_tabwidget.addTab(self.playercontrols_properties_panel_tabwidget_waveform, '')
    self.playercontrols_properties_panel_tabwidget.setTabIcon(1, QIcon(os.path.join(PATH_SUBTITLD_GRAPHICS, 'playercontrols_properties_panel_waveform_icon.svg')))

    self.playercontrols_properties_panel_tabwidget_background = QWidget()

    self.playercontrols_properties_panel_tabwidget_background_title_normal = QLabel('Background colors'.upper(), parent=self.playercontrols_properties_panel_tabwidget_background)
    self.playercontrols_properties_panel_tabwidget_background_title_normal.setObjectName('small_label')
    self.playercontrols_properties_panel_tabwidget_background_title_normal.setStyleSheet(' QLabel {font-weight:bold;} ')

    self.playercontrols_properties_panel_tabwidget_background_time_text_color_title_normal = QLabel('Time'.upper(), parent=self.playercontrols_properties_panel_tabwidget_background)
    self.playercontrols_properties_panel_tabwidget_background_time_text_color_title_normal.setObjectName('small_label')

    self.playercontrols_properties_panel_tabwidget_background_time_text_color_button = QPushButton(parent=self.playercontrols_properties_panel_tabwidget_background)
    self.playercontrols_properties_panel_tabwidget_background_time_text_color_button.clicked.connect(lambda: playercontrols_properties_panel_tabwidget_background_time_text_color_button_clicked(self))

    self.playercontrols_properties_panel_tabwidget_background_cursor_color_title_normal = QLabel('Cursor'.upper(), parent=self.playercontrols_properties_panel_tabwidget_background)
    self.playercontrols_properties_panel_tabwidget_background_cursor_color_title_normal.setObjectName('small_label')

    self.playercontrols_properties_panel_tabwidget_background_cursor_color_button = QPushButton(parent=self.playercontrols_properties_panel_tabwidget_background)
    self.playercontrols_properties_panel_tabwidget_background_cursor_color_button.clicked.connect(lambda: playercontrols_properties_panel_tabwidget_background_cursor_color_button_clicked(self))

    self.playercontrols_properties_panel_tabwidget_background_grid_color_title_normal = QLabel('Grid'.upper(), parent=self.playercontrols_properties_panel_tabwidget_background)
    self.playercontrols_properties_panel_tabwidget_background_grid_color_title_normal.setObjectName('small_label')

    self.playercontrols_properties_panel_tabwidget_background_grid_color_button = QPushButton(parent=self.playercontrols_properties_panel_tabwidget_background)
    self.playercontrols_properties_panel_tabwidget_background_grid_color_button.clicked.connect(lambda: playercontrols_properties_panel_tabwidget_background_grid_color_button_clicked(self))

    self.playercontrols_properties_panel_tabwidget.addTab(self.playercontrols_properties_panel_tabwidget_background, '')
    self.playercontrols_properties_panel_tabwidget.setTabIcon(2, QIcon(os.path.join(PATH_SUBTITLD_GRAPHICS, 'playercontrols_properties_panel_background_icon.svg')))

    self.playercontrols_widget_central_top_background = QLabel(parent=self.playercontrols_widget)
    self.playercontrols_widget_central_top_background.setObjectName('playercontrols_widget_central_top_background')

    self.playercontrols_widget_central_bottom_background = QLabel(parent=self.playercontrols_widget)
    self.playercontrols_widget_central_bottom_background.setObjectName('playercontrols_widget_central_bottom_background')

    self.playercontrols_widget_central_top = QLabel(parent=self.playercontrols_widget)
    self.playercontrols_widget_central_top.setObjectName('playercontrols_widget_central_top')

    self.playercontrols_widget_central_bottom = QLabel(parent=self.playercontrols_widget)
    self.playercontrols_widget_central_bottom.setObjectName('playercontrols_widget_central_bottom')

    self.playercontrols_widget_top_right = QLabel(parent=self.playercontrols_widget)
    self.playercontrols_widget_top_right.setObjectName('playercontrols_widget_top_right')

    self.playercontrols_widget_top_left = QLabel(parent=self.playercontrols_widget)
    self.playercontrols_widget_top_left.setObjectName('playercontrols_widget_top_left')

    self.playercontrols_widget_bottom_right = QLabel(parent=self.playercontrols_widget)
    self.playercontrols_widget_bottom_right.setObjectName('playercontrols_widget_bottom_right')

    self.playercontrols_widget_bottom_right_corner = QLabel(parent=self.playercontrols_widget)
    self.playercontrols_widget_bottom_right_corner.setObjectName('playercontrols_widget_central_bottom')
    self.playercontrols_widget_bottom_right_corner.setStyleSheet('QLabel {border-right:0;}')

    self.playercontrols_widget_bottom_left = QLabel(parent=self.playercontrols_widget)
    self.playercontrols_widget_bottom_left.setObjectName('playercontrols_widget_bottom_left')

    self.playercontrols_play_from_last_start_button = QPushButton(parent=self.playercontrols_widget_central_top)
    self.playercontrols_play_from_last_start_button.setObjectName('player_controls_button')
    self.playercontrols_play_from_last_start_button.setIcon(QIcon(os.path.join(PATH_SUBTITLD_GRAPHICS, 'play_from_last_start_icon.png')))
    self.playercontrols_play_from_last_start_button.setIconSize(QSize(24, 24))
    self.playercontrols_play_from_last_start_button.clicked.connect(lambda: playercontrols_play_from_last_start_button_clicked(self))

    self.playercontrols_stop_button = QPushButton(parent=self.playercontrols_widget_central_top)
    self.playercontrols_stop_button.setObjectName('player_controls_button')
    self.playercontrols_stop_button.setIcon(QIcon(os.path.join(PATH_SUBTITLD_GRAPHICS, 'stop_icon.png')))
    self.playercontrols_stop_button.setIconSize(QSize(15, 15))
    self.playercontrols_stop_button.clicked.connect(lambda: playercontrols_stop_button_clicked(self))

    self.playercontrols_playpause_button = QPushButton(parent=self.playercontrols_widget_central_top)
    self.playercontrols_playpause_button.setObjectName('player_controls_button')
    self.playercontrols_playpause_button.setCheckable(True)
    self.playercontrols_playpause_button.setIcon(QIcon(os.path.join(PATH_SUBTITLD_GRAPHICS, 'play_icon.png')))
    self.playercontrols_playpause_button.setIconSize(QSize(20, 20))
    self.playercontrols_playpause_button.clicked.connect(lambda: playercontrols_playpause_button_clicked(self))

    self.playercontrols_play_from_next_start_button = QPushButton(parent=self.playercontrols_widget_central_top)
    self.playercontrols_play_from_next_start_button.setObjectName('player_controls_button')
    self.playercontrols_play_from_next_start_button.setIcon(QIcon(os.path.join(PATH_SUBTITLD_GRAPHICS, 'play_from_next_start_icon.png')))
    self.playercontrols_play_from_next_start_button.setIconSize(QSize(24, 24))
    self.playercontrols_play_from_next_start_button.clicked.connect(lambda: playercontrols_play_from_next_start_button_clicked(self))

    self.gap_add_subtitle_button = QPushButton(parent=self.playercontrols_widget)
    self.gap_add_subtitle_button.setIcon(QIcon(os.path.join(PATH_SUBTITLD_GRAPHICS, 'gap_add_icon.png')))
    self.gap_add_subtitle_button.setIconSize(QSize(20, 20))
    self.gap_add_subtitle_button.setObjectName('button_dark')
    self.gap_add_subtitle_button.setStyleSheet('QPushButton { border-right:0; border-bottom:0; padding-right:26px; }')
    self.gap_add_subtitle_button.clicked.connect(lambda: gap_add_subtitle_button_clicked(self))

    self.gap_remove_subtitle_button = QPushButton(parent=self.playercontrols_widget)
    self.gap_remove_subtitle_button.setIcon(QIcon(os.path.join(PATH_SUBTITLD_GRAPHICS, 'gap_remove_icon.png')))
    self.gap_remove_subtitle_button.setIconSize(QSize(20, 20))
    self.gap_remove_subtitle_button.setObjectName('button_dark')
    self.gap_remove_subtitle_button.setStyleSheet('QPushButton { border-left:0; border-bottom:0; padding-left:26px; }')
    self.gap_remove_subtitle_button.clicked.connect(lambda: gap_remove_subtitle_button_clicked(self))

    self.gap_subtitle_duration = QDoubleSpinBox(parent=self.playercontrols_widget)
    self.gap_subtitle_duration.setObjectName('controls_qdoublespinbox')
    self.gap_subtitle_duration.setMinimum(.1)
    self.gap_subtitle_duration.setMaximum(60.)

    self.add_subtitle_button = QPushButton('ADD', parent=self.playercontrols_widget)
    self.add_subtitle_button.setIcon(QIcon(os.path.join(PATH_SUBTITLD_GRAPHICS, 'add_subtitle_icon.png')))
    self.add_subtitle_button.setIconSize(QSize(20, 20))
    self.add_subtitle_button.setObjectName('button_dark')
    self.add_subtitle_button.setStyleSheet('QPushButton {padding-right:105px; border-right:0; border-bottom:0;}')
    self.add_subtitle_button.clicked.connect(lambda: add_subtitle_button_clicked(self))

    self.add_subtitle_duration = QDoubleSpinBox(parent=self.add_subtitle_button)
    self.add_subtitle_duration.setObjectName('controls_qdoublespinbox')
    self.add_subtitle_duration.setMinimum(.1)
    self.add_subtitle_duration.setMaximum(60.)
    self.add_subtitle_duration.valueChanged.connect(lambda: add_subtitle_duration_changed(self))

    self.add_subtitle_starting_from_last = QPushButton(parent=self.add_subtitle_button)
    self.add_subtitle_starting_from_last.setObjectName('button_dark')
    self.add_subtitle_starting_from_last.setCheckable(True)
    self.add_subtitle_starting_from_last.setIcon(QIcon(os.path.join(PATH_SUBTITLD_GRAPHICS, 'add_from_last.svg')))
    self.add_subtitle_starting_from_last.setIconSize(QSize(15, 15))
    self.add_subtitle_starting_from_last.setStyleSheet('QPushButton {padding-right:0; padding-bottom:6 px;}')
    self.add_subtitle_starting_from_last.clicked.connect(lambda: add_subtitle_starting_from_last_clicked(self))

    self.add_subtitle_and_play = QPushButton(parent=self.add_subtitle_button)
    self.add_subtitle_and_play.setObjectName('button_dark')
    self.add_subtitle_and_play.setCheckable(True)
    self.add_subtitle_and_play.setIcon(QIcon(os.path.join(PATH_SUBTITLD_GRAPHICS, 'add_and_play.svg')))
    self.add_subtitle_and_play.setIconSize(QSize(15, 15))
    self.add_subtitle_and_play.setStyleSheet('QPushButton {padding-right:0; border-right:5px; border-left:0; padding-bottom:6px;}')
    self.add_subtitle_and_play.clicked.connect(lambda: add_subtitle_and_play_clicked(self))

    self.remove_selected_subtitle_button = QPushButton('REMOVE', parent=self.playercontrols_widget)
    self.remove_selected_subtitle_button.setIcon(QIcon(os.path.join(PATH_SUBTITLD_GRAPHICS, 'remove_selected_subtitle_icon.png')))
    self.remove_selected_subtitle_button.setIconSize(QSize(20, 20))
    self.remove_selected_subtitle_button.setObjectName('button_dark')
    self.remove_selected_subtitle_button.setStyleSheet('QPushButton { border-left:0; border-bottom:0;}')
    self.remove_selected_subtitle_button.clicked.connect(lambda: remove_selected_subtitle_button_clicked(self))

    self.merge_back_selected_subtitle_button = QPushButton(parent=self.playercontrols_widget)
    self.merge_back_selected_subtitle_button.setIcon(QIcon(os.path.join(PATH_SUBTITLD_GRAPHICS, 'merge_back_selected_subtitle_icon.png')))
    self.merge_back_selected_subtitle_button.setIconSize(QSize(20, 20))
    self.merge_back_selected_subtitle_button.setObjectName('button_dark')
    self.merge_back_selected_subtitle_button.setStyleSheet('QPushButton {border-bottom:0; border-right:0;}')
    self.merge_back_selected_subtitle_button.clicked.connect(lambda: merge_back_selected_subtitle_button_clicked(self))

    self.slice_selected_subtitle_button = QPushButton(parent=self.playercontrols_widget)
    self.slice_selected_subtitle_button.setIcon(QIcon(os.path.join(PATH_SUBTITLD_GRAPHICS, 'slice_selected_subtitle_icon.png')))
    self.slice_selected_subtitle_button.setIconSize(QSize(20, 20))
    self.slice_selected_subtitle_button.setObjectName('button_dark')
    self.slice_selected_subtitle_button.setStyleSheet('QPushButton {border-bottom:0; border-left:0; border-right:0;}')
    self.slice_selected_subtitle_button.clicked.connect(lambda: slice_selected_subtitle_button_clicked(self))

    self.merge_next_selected_subtitle_button = QPushButton(parent=self.playercontrols_widget)
    self.merge_next_selected_subtitle_button.setIcon(QIcon(os.path.join(PATH_SUBTITLD_GRAPHICS, 'merge_next_selected_subtitle_icon.png')))
    self.merge_next_selected_subtitle_button.setIconSize(QSize(20, 20))
    self.merge_next_selected_subtitle_button.setObjectName('button_dark')
    self.merge_next_selected_subtitle_button.setStyleSheet('QPushButton {border-bottom:0; border-left:0;}')
    self.merge_next_selected_subtitle_button.clicked.connect(lambda: merge_next_selected_subtitle_button_clicked(self))

    self.move_start_back_subtitle = QPushButton(parent=self.playercontrols_widget)
    self.move_start_back_subtitle.setIcon(QIcon(os.path.join(PATH_SUBTITLD_GRAPHICS, 'move_start_back_subtitle.png')))
    self.move_start_back_subtitle.setObjectName('subbutton2_dark')
    self.move_start_back_subtitle.setStyleSheet('QPushButton {border-bottom:0; border-right:0;}')
    self.move_start_back_subtitle.clicked.connect(lambda: move_start_back_subtitle_clicked(self))

    self.move_start_forward_subtitle = QPushButton(parent=self.playercontrols_widget)
    self.move_start_forward_subtitle.setIcon(QIcon(os.path.join(PATH_SUBTITLD_GRAPHICS, 'move_start_forward_subtitle.png')))
    self.move_start_forward_subtitle.setObjectName('subbutton2_dark')
    self.move_start_forward_subtitle.setStyleSheet('QPushButton {border-bottom:0; border-left:0; padding-left:2px;}')
    self.move_start_forward_subtitle.clicked.connect(lambda: move_start_forward_subtitle_clicked(self))

    self.move_backward_subtitle = QPushButton(parent=self.playercontrols_widget)
    self.move_backward_subtitle.setIcon(QIcon(os.path.join(PATH_SUBTITLD_GRAPHICS, 'move_backward_subtitle.png')))
    self.move_backward_subtitle.setObjectName('subbutton2_dark')
    self.move_backward_subtitle.setStyleSheet('QPushButton {border-bottom:0;}')
    self.move_backward_subtitle.clicked.connect(lambda: move_backward_subtitle_clicked(self))

    self.timeline_cursor_back_frame = QPushButton(parent=self.playercontrols_widget)
    self.timeline_cursor_back_frame.setIcon(QIcon(os.path.join(PATH_SUBTITLD_GRAPHICS, 'timeline_cursor_back_frame.png')))
    self.timeline_cursor_back_frame.setObjectName('subbutton_left_dark')
    self.timeline_cursor_back_frame.setStyleSheet('QPushButton {border-bottom:0;}')
    self.timeline_cursor_back_frame.clicked.connect(lambda: timeline_cursor_back_frame_clicked(self))

    self.playercontrols_timecode_label = QLabel(parent=self.playercontrols_widget_central_bottom)
    self.playercontrols_timecode_label.setObjectName('playercontrols_timecode_label')

    self.timeline_cursor_next_frame = QPushButton(parent=self.playercontrols_widget)
    self.timeline_cursor_next_frame.setIcon(QIcon(os.path.join(PATH_SUBTITLD_GRAPHICS, 'timeline_cursor_next_frame.png')))
    self.timeline_cursor_next_frame.setObjectName('subbutton_right_dark')
    self.timeline_cursor_next_frame.setStyleSheet('QPushButton {border-bottom:0;}')
    self.timeline_cursor_next_frame.clicked.connect(lambda: timeline_cursor_next_frame_clicked(self))

    self.move_forward_subtitle = QPushButton(parent=self.playercontrols_widget)
    self.move_forward_subtitle.setIcon(QIcon(os.path.join(PATH_SUBTITLD_GRAPHICS, 'move_forward_subtitle.png')))
    self.move_forward_subtitle.setObjectName('subbutton2_dark')
    self.move_forward_subtitle.setStyleSheet('QPushButton {border-bottom:0;}')
    self.move_forward_subtitle.clicked.connect(lambda: move_forward_subtitle_clicked(self))

    self.move_end_back_subtitle = QPushButton(parent=self.playercontrols_widget)
    self.move_end_back_subtitle.setIcon(QIcon(os.path.join(PATH_SUBTITLD_GRAPHICS, 'move_end_back_subtitle.png')))
    self.move_end_back_subtitle.setObjectName('subbutton2_dark')
    self.move_end_back_subtitle.setStyleSheet('QPushButton {border-bottom:0; border-right:0;}')
    self.move_end_back_subtitle.clicked.connect(lambda: move_end_back_subtitle_clicked(self))

    self.move_end_forward_subtitle = QPushButton(parent=self.playercontrols_widget)
    self.move_end_forward_subtitle.setIcon(QIcon(os.path.join(PATH_SUBTITLD_GRAPHICS, 'move_end_forward_subtitle.png')))
    self.move_end_forward_subtitle.setObjectName('subbutton2_dark')
    self.move_end_forward_subtitle.setStyleSheet('QPushButton {border-bottom:0; border-left:0; padding-left:2px;}')
    self.move_end_forward_subtitle.clicked.connect(lambda: move_end_forward_subtitle_clicked(self))

    self.zoomin_button = QPushButton(parent=self.playercontrols_widget)
    self.zoomin_button.setIcon(QIcon(os.path.join(PATH_SUBTITLD_GRAPHICS, 'zoom_in_icon.png')))
    self.zoomin_button.setIconSize(QSize(20, 20))
    self.zoomin_button.setObjectName('button_dark')
    self.zoomin_button.setStyleSheet('QPushButton {border-bottom:0; border-left:0;}')
    self.zoomin_button.clicked.connect(lambda: zoomin_button_clicked(self))

    self.zoomout_button = QPushButton(parent=self.playercontrols_widget)
    self.zoomout_button.setIcon(QIcon(os.path.join(PATH_SUBTITLD_GRAPHICS, 'zoom_out_icon.png')))
    self.zoomout_button.setIconSize(QSize(20, 20))
    self.zoomout_button.setObjectName('button_dark')
    self.zoomout_button.setStyleSheet('QPushButton {border-bottom:0; border-right:0;}')
    self.zoomout_button.clicked.connect(lambda: zoomout_button_clicked(self))

    self.next_start_to_current_position_button = QPushButton(parent=self.playercontrols_widget)
    self.next_start_to_current_position_button.setIcon(QIcon(os.path.join(PATH_SUBTITLD_GRAPHICS, 'next_start_to_current_position_icon.png')))
    self.next_start_to_current_position_button.setIconSize(QSize(20, 20))
    self.next_start_to_current_position_button.setObjectName('button_dark')
    self.next_start_to_current_position_button.setStyleSheet('QPushButton {border-bottom:0; border-right:0; padding-right:10px;}')
    self.next_start_to_current_position_button.clicked.connect(lambda: next_start_to_current_position_button_clicked(self))

    self.last_start_to_current_position_button = QPushButton(parent=self.playercontrols_widget)
    self.last_start_to_current_position_button.setIcon(QIcon(os.path.join(PATH_SUBTITLD_GRAPHICS, 'last_start_to_current_position_icon.png')))
    self.last_start_to_current_position_button.setIconSize(QSize(20, 20))
    self.last_start_to_current_position_button.setObjectName('button_dark')
    self.last_start_to_current_position_button.setStyleSheet('QPushButton {border-bottom:0; border-right:0; border-left:0; padding-left:10px;}')
    self.last_start_to_current_position_button.clicked.connect(lambda: last_start_to_current_position_button_clicked(self))

    self.subtitle_start_to_current_position_button = QPushButton(parent=self.playercontrols_widget)
    self.subtitle_start_to_current_position_button.setObjectName('button_dark')
    self.subtitle_start_to_current_position_button.setStyleSheet('QPushButton {border-bottom:0;}')
    self.subtitle_start_to_current_position_button.clicked.connect(lambda: subtitle_start_to_current_position_button_clicked(self))

    self.next_end_to_current_position_button = QPushButton(parent=self.playercontrols_widget)
    self.next_end_to_current_position_button.setIcon(QIcon(os.path.join(PATH_SUBTITLD_GRAPHICS, 'next_end_to_current_position_icon.png')))
    self.next_end_to_current_position_button.setIconSize(QSize(20, 20))
    self.next_end_to_current_position_button.setObjectName('button_dark')
    self.next_end_to_current_position_button.setStyleSheet('QPushButton {border-bottom:0; border-left:0; border-right:0; padding-right:10px;}')
    self.next_end_to_current_position_button.clicked.connect(lambda: next_end_to_current_position_button_clicked(self))

    self.last_end_to_current_position_button = QPushButton(parent=self.playercontrols_widget)
    self.last_end_to_current_position_button.setIcon(QIcon(os.path.join(PATH_SUBTITLD_GRAPHICS, 'last_end_to_current_position_icon.png')))
    self.last_end_to_current_position_button.setIconSize(QSize(20, 20))
    self.last_end_to_current_position_button.setObjectName('button_dark')
    self.last_end_to_current_position_button.setStyleSheet('QPushButton {border-bottom:0; border-left:0; padding-left:10px;}')
    self.last_end_to_current_position_button.clicked.connect(lambda: last_end_to_current_position_button_clicked(self))

    self.subtitle_end_to_current_position_button = QPushButton(parent=self.playercontrols_widget)
    self.subtitle_end_to_current_position_button.setObjectName('button_dark')
    self.subtitle_end_to_current_position_button.setStyleSheet('QPushButton {border-bottom:0;}')
    self.subtitle_end_to_current_position_button.clicked.connect(lambda: subtitle_end_to_current_position_button_clicked(self))

    self.change_playback_speed = QPushButton(parent=self.playercontrols_widget)
    self.change_playback_speed.setObjectName('button')
    self.change_playback_speed.setCheckable(True)
    self.change_playback_speed.setStyleSheet('QPushButton {border-top:0; padding-left:36px; text-align:left;}')
    self.change_playback_speed.clicked.connect(lambda: change_playback_speed_clicked(self))

    self.change_playback_speed_icon_label = QLabel(parent=self.change_playback_speed)
    self.change_playback_speed_icon_label.setStyleSheet('QLabel { image: url(' + os.path.join(PATH_SUBTITLD_GRAPHICS, 'playback_speed_icon.png') + ')}')

    self.change_playback_speed_decrease = QPushButton('-', parent=self.change_playback_speed)
    self.change_playback_speed_decrease.setObjectName('button')
    self.change_playback_speed_decrease.setStyleSheet('QPushButton {border-top:5px; padding-left:5px; border-right:0;}')
    self.change_playback_speed_decrease.clicked.connect(lambda: change_playback_speed_decrease_clicked(self))

    self.change_playback_speed_slider = QSlider(Qt.Horizontal, parent=self.change_playback_speed)
    self.change_playback_speed_slider.setMinimum(5)
    self.change_playback_speed_slider.setMaximum(300)
    self.change_playback_speed_slider.setPageStep(10)
    self.change_playback_speed_slider.sliderReleased.connect(lambda: change_playback_speed_slider(self))

    self.change_playback_speed_increase = QPushButton('+', parent=self.change_playback_speed)
    self.change_playback_speed_increase.setObjectName('button')
    self.change_playback_speed_increase.setStyleSheet('QPushButton {border-top:5px; padding-left:5px; border-left:0;}')
    self.change_playback_speed_increase.clicked.connect(lambda: change_playback_speed_increase_clicked(self))

    self.repeat_playback = QPushButton(parent=self.playercontrols_widget)
    self.repeat_playback.setObjectName('button')
    self.repeat_playback.setCheckable(True)
    self.repeat_playback.setStyleSheet('QPushButton {border-top:0; }')
    self.repeat_playback.clicked.connect(lambda: repeat_playback_clicked(self))

    self.repeat_playback_icon_label = QLabel(parent=self.repeat_playback)
    self.repeat_playback_icon_label.setStyleSheet('QLabel { image: url(' + os.path.join(PATH_SUBTITLD_GRAPHICS, 'playback_repeat_icon.png') + ')}')

    self.repeat_playback_duration = QDoubleSpinBox(parent=self.repeat_playback)
    self.repeat_playback_duration.setObjectName('controls_qdoublespinbox')
    self.repeat_playback_duration.setMinimum(.1)
    self.repeat_playback_duration.setMaximum(60.)
    self.repeat_playback_duration.valueChanged.connect(lambda: repeat_playback_duration_changed(self))

    self.repeat_playback_x_label = QLabel('x', parent=self.repeat_playback)
    self.repeat_playback_x_label.setStyleSheet('QLabel {qproperty-alignment:AlignCenter; font-weight:bold; color:rgb(184,206,224); }')

    self.repeat_playback_times = QSpinBox(parent=self.repeat_playback)
    self.repeat_playback_times.setObjectName('controls_qspinbox')
    self.repeat_playback_times.setMinimum(1)
    self.repeat_playback_times.setMaximum(20)
    self.repeat_playback_times.valueChanged.connect(lambda: repeat_playback_times_changed(self))

    self.timelinescrolling_none_button = QPushButton(parent=self.playercontrols_widget)
    self.timelinescrolling_none_button.setObjectName('subbutton')
    self.timelinescrolling_none_button.setStyleSheet('QPushButton {border-right:0; border-top:0;}')
    self.timelinescrolling_none_button.setIcon(QIcon(os.path.join(PATH_SUBTITLD_GRAPHICS, 'timelinescrolling_none_icon.svg')))
    self.timelinescrolling_none_button.setCheckable(True)
    self.timelinescrolling_none_button.clicked.connect(lambda: timelinescrolling_type_changed(self, 'none'))

    self.timelinescrolling_page_button = QPushButton(parent=self.playercontrols_widget)
    self.timelinescrolling_page_button.setObjectName('subbutton')
    self.timelinescrolling_page_button.setStyleSheet('QPushButton {border-right:0; border-top:0;}')
    self.timelinescrolling_page_button.setCheckable(True)
    self.timelinescrolling_page_button.setIcon(QIcon(os.path.join(PATH_SUBTITLD_GRAPHICS, 'timelinescrolling_page_icon.svg')))
    self.timelinescrolling_page_button.clicked.connect(lambda: timelinescrolling_type_changed(self, 'page'))

    self.timelinescrolling_follow_button = QPushButton(parent=self.playercontrols_widget)
    self.timelinescrolling_follow_button.setObjectName('subbutton')
    self.timelinescrolling_follow_button.setStyleSheet('QPushButton {border-top:0;}')
    self.timelinescrolling_follow_button.setCheckable(True)
    self.timelinescrolling_follow_button.setIcon(QIcon(os.path.join(PATH_SUBTITLD_GRAPHICS, 'timelinescrolling_follow_icon.svg')))
    self.timelinescrolling_follow_button.clicked.connect(lambda: timelinescrolling_type_changed(self, 'follow'))

    self.grid_button = QPushButton('GRID', parent=self.playercontrols_widget)
    self.grid_button.setObjectName('subbutton')
    self.grid_button.setStyleSheet('QPushButton {border-right:0; border-top:0;}')
    self.grid_button.setCheckable(True)
    self.grid_button.clicked.connect(lambda: grid_button_clicked(self))

    self.grid_frames_button = QPushButton(parent=self.playercontrols_widget)
    self.grid_frames_button.setObjectName('subbutton')
    self.grid_frames_button.setStyleSheet('QPushButton {border-right:0; border-top:0;}')
    self.grid_frames_button.setIcon(QIcon(os.path.join(PATH_SUBTITLD_GRAPHICS, 'grid_frames_icon.png')))
    self.grid_frames_button.setCheckable(True)
    self.grid_frames_button.clicked.connect(lambda: grid_type_changed(self, 'frames'))

    self.grid_seconds_button = QPushButton(parent=self.playercontrols_widget)
    self.grid_seconds_button.setObjectName('subbutton')
    self.grid_seconds_button.setStyleSheet('QPushButton {border-right:0; border-top:0;}')
    self.grid_seconds_button.setCheckable(True)
    self.grid_seconds_button.setIcon(QIcon(os.path.join(PATH_SUBTITLD_GRAPHICS, 'grid_seconds_icon.png')))
    self.grid_seconds_button.clicked.connect(lambda: grid_type_changed(self, 'seconds'))

    self.grid_scenes_button = QPushButton(parent=self.playercontrols_widget)
    self.grid_scenes_button.setObjectName('subbutton')
    self.grid_scenes_button.setStyleSheet('QPushButton {border-top:0;}')
    self.grid_scenes_button.setCheckable(True)
    self.grid_scenes_button.setIcon(QIcon(os.path.join(PATH_SUBTITLD_GRAPHICS, 'grid_scenes_icon.png')))
    self.grid_scenes_button.clicked.connect(lambda: grid_type_changed(self, 'scenes'))

    self.snap_button = QPushButton('SNAP', parent=self.playercontrols_widget)
    self.snap_button.setObjectName('subbutton')
    self.snap_button.setStyleSheet('QPushButton {border-right:0; border-top:0;}')
    self.snap_button.setCheckable(True)
    self.snap_button.clicked.connect(lambda: snap_button_clicked(self))

    self.snap_value = QDoubleSpinBox(parent=self.snap_button)
    self.snap_value.setObjectName('controls_qdoublespinbox')
    self.snap_value.valueChanged.connect(lambda: snap_value_changed(self))

    self.snap_limits_button = QPushButton(parent=self.playercontrols_widget)
    self.snap_limits_button.setObjectName('subbutton')
    self.snap_limits_button.setStyleSheet('QPushButton {border-right:0; border-top:0;}')
    self.snap_limits_button.setIcon(QIcon(os.path.join(PATH_SUBTITLD_GRAPHICS, 'snap_limits_icon.png')))
    self.snap_limits_button.setCheckable(True)
    self.snap_limits_button.clicked.connect(lambda: snap_limits_button_clicked(self))

    self.snap_grid_button = QPushButton(parent=self.playercontrols_widget)
    self.snap_grid_button.setObjectName('subbutton')
    self.snap_grid_button.setStyleSheet('QPushButton {border-right:0; border-top:0;}')
    self.snap_grid_button.setCheckable(True)
    self.snap_grid_button.setIcon(QIcon(os.path.join(PATH_SUBTITLD_GRAPHICS, 'snap_grid_icon.png')))
    self.snap_grid_button.clicked.connect(lambda: snap_grid_button_clicked(self))

    self.snap_move_button = QPushButton(parent=self.playercontrols_widget)
    self.snap_move_button.setObjectName('subbutton')
    self.snap_move_button.setStyleSheet('QPushButton {border-right:0; border-top:0;}')
    self.snap_move_button.setCheckable(True)
    self.snap_move_button.setIcon(QIcon(os.path.join(PATH_SUBTITLD_GRAPHICS, 'snap_moving_icon.png')))
    self.snap_move_button.clicked.connect(lambda: snap_move_button_clicked(self))

    self.snap_move_nereast_button = QPushButton(parent=self.playercontrols_widget)
    self.snap_move_nereast_button.setObjectName('subbutton')
    self.snap_move_nereast_button.setStyleSheet('QPushButton {border-top:0;}')
    self.snap_move_nereast_button.setCheckable(True)
    self.snap_move_nereast_button.setIcon(QIcon(os.path.join(PATH_SUBTITLD_GRAPHICS, 'snap_move_next.svg')))
    self.snap_move_nereast_button.clicked.connect(lambda: snap_move_nereast_button_clicked(self))

    self.step_button = QPushButton('STEP', parent=self.playercontrols_widget)
    self.step_button.setObjectName('subbutton')
    self.step_button.setStyleSheet('QPushButton {border-top:0;}')
    self.step_button.setCheckable(True)
    self.step_button.clicked.connect(lambda: update_step_buttons(self))

    self.step_value_f = QDoubleSpinBox(parent=self.step_button)
    self.step_value_f.setObjectName('controls_qdoublespinbox')
    self.step_value_f.setMinimum(.001)
    self.step_value_f.setMaximum(999.999)
    self.step_value_f.valueChanged.connect(lambda: step_value_changed(self))

    self.step_value_i = QSpinBox(parent=self.step_button)
    self.step_value_i.setObjectName('controls_qspinbox')
    self.step_value_i.setMinimum(1)
    self.step_value_i.setMaximum(999)
    self.step_value_i.valueChanged.connect(lambda: step_value_changed(self))

    self.step_unit = QComboBox(parent=self.step_button)
    self.step_unit.setObjectName('controls_combobox')
    self.step_unit.insertItems(0, STEPS_LIST)
    self.step_unit.activated.connect(lambda: step_value_changed(self))

    self.playercontrols_properties_panel_toggle = QPushButton(parent=self.playercontrols_widget)
    self.playercontrols_properties_panel_toggle.setObjectName('playercontrols_properties_panel_toggle')
    self.playercontrols_properties_panel_toggle.setCheckable(True)
    self.playercontrols_properties_panel_toggle.clicked.connect(lambda: playercontrols_properties_panel_toggle_pressed(self))
    self.playercontrols_properties_panel_toggle_animation = QPropertyAnimation(self.playercontrols_properties_panel_toggle, b'geometry')
    self.playercontrols_properties_panel_toggle_animation.setEasingCurve(QEasingCurve.OutCirc)


def resized(self):
    """Function to call when resizing widgets"""
    if self.subtitles_list or self.video_metadata:
        self.playercontrols_widget.setGeometry(0, self.height()-200, self.width(), 200)
    else:
        self.playercontrols_widget.setGeometry(0, self.height(), self.width(), 200)
    top_width = 300
    bottom_width = 120
    self.playercontrols_widget_central_top_background.setGeometry((self.playercontrols_widget.width()*.5)-(top_width*.5), 10, top_width, 45)
    self.playercontrols_widget_central_bottom_background.setGeometry((self.playercontrols_widget.width()*.5)-(bottom_width*.5), 62, bottom_width, 22)
    self.playercontrols_widget_central_top.setGeometry((self.playercontrols_widget.width()*.5)-(top_width*.5), 0, top_width, 60)
    self.playercontrols_widget_central_bottom.setGeometry((self.playercontrols_widget.width()*.5)-(bottom_width*.5), 60, bottom_width, 26)
    self.playercontrols_timecode_label.setGeometry(0, 0, self.playercontrols_widget_central_bottom.width(), self.playercontrols_widget_central_bottom.height())

    self.playercontrols_widget_top_right.setGeometry(self.playercontrols_widget_central_top.x() + self.playercontrols_widget_central_top.width(), self.playercontrols_widget_central_top.y(), self.playercontrols_widget.width()-(self.playercontrols_widget_central_top.x() + self.playercontrols_widget_central_top.width()), self.playercontrols_widget_central_top.height())
    self.playercontrols_widget_top_left.setGeometry(0, self.playercontrols_widget_central_top.y(), self.playercontrols_widget.width()-(self.playercontrols_widget_central_top.x() + self.playercontrols_widget_central_top.width()), self.playercontrols_widget_central_top.height())
    self.playercontrols_widget_bottom_right.setGeometry(self.playercontrols_widget_central_bottom.x() + self.playercontrols_widget_central_bottom.width(), self.playercontrols_widget_central_bottom.y(), self.playercontrols_widget.width()-(self.playercontrols_widget_central_bottom.x() + self.playercontrols_widget_central_bottom.width())-30, self.playercontrols_widget_central_bottom.height())
    self.playercontrols_widget_bottom_right_corner.setGeometry(self.playercontrols_widget_bottom_right.x() + self.playercontrols_widget_bottom_right.width(), self.playercontrols_widget_bottom_right.y(), 30, self.playercontrols_widget_bottom_right.height())
    self.playercontrols_widget_bottom_left.setGeometry(0, self.playercontrols_widget_central_bottom.y(), self.playercontrols_widget_central_bottom.x(), self.playercontrols_widget_central_bottom.height())

    show_or_hide_playercontrols_properties_panel(self)
    self.playercontrols_properties_panel_tabwidget.setGeometry(10, 34, self.playercontrols_properties_panel.width()-40, self.playercontrols_properties_panel.height()-60)
    self.playercontrols_properties_panel_tabwidget_subtitles_subtitle_title_normal.setGeometry(10,10,100,15)
    self.playercontrols_properties_panel_tabwidget_subtitles_subtitle_border_color_title_normal.setGeometry(10,25,30,15)
    self.playercontrols_properties_panel_tabwidget_subtitles_subtitle_border_color_button.setGeometry(10,40,30,30)
    self.playercontrols_properties_panel_tabwidget_subtitles_subtitle_fill_color_title_normal.setGeometry(45,25,30,15)
    self.playercontrols_properties_panel_tabwidget_subtitles_subtitle_fill_color_button.setGeometry(45,40,30,30)
    self.playercontrols_properties_panel_tabwidget_subtitles_subtitle_text_color_title_normal.setGeometry(80,25,30,15)
    self.playercontrols_properties_panel_tabwidget_subtitles_subtitle_text_color_button.setGeometry(80,40,30,30)
    self.playercontrols_properties_panel_tabwidget_subtitles_subtitle_title_selected.setGeometry(120,10,100,15)
    self.playercontrols_properties_panel_tabwidget_subtitles_subtitle_border_color_title_selected.setGeometry(120,25,30,15)
    self.playercontrols_properties_panel_tabwidget_subtitles_selected_subtitle_border_color_button.setGeometry(120,40,30,30)
    self.playercontrols_properties_panel_tabwidget_subtitles_subtitle_fill_color_title_selected.setGeometry(155,25,30,15)
    self.playercontrols_properties_panel_tabwidget_subtitles_selected_subtitle_fill_color_button.setGeometry(155,40,30,30)
    self.playercontrols_properties_panel_tabwidget_subtitles_subtitle_text_color_title_selected.setGeometry(190,25,30,15)
    self.playercontrols_properties_panel_tabwidget_subtitles_selected_subtitle_text_color_button.setGeometry(190,40,30,30)
    self.playercontrols_properties_panel_tabwidget_subtitles_subtitle_title_arrows.setGeometry(225,10,70,15)
    self.playercontrols_properties_panel_tabwidget_subtitles_subtitle_title_normal_arrows.setGeometry(225,25,30,15)
    self.playercontrols_properties_panel_tabwidget_subtitles_subtitle_arrow_normal_button.setGeometry(225,40,30,30)
    self.playercontrols_properties_panel_tabwidget_subtitles_selected_subtitle_title_normal_arrows.setGeometry(260,25,30,15)
    self.playercontrols_properties_panel_tabwidget_subtitles_selected_subtitle_arrow_normal_button.setGeometry(260,40,30,30)
    self.playercontrols_properties_panel_tabwidget_waveform_title_normal.setGeometry(10,10,100,15)
    self.playercontrols_properties_panel_tabwidget_waveform_border_color_title_normal.setGeometry(10,25,30,15)
    self.playercontrols_properties_panel_tabwidget_waveform_border_color_button.setGeometry(10,40,30,30)
    self.playercontrols_properties_panel_tabwidget_waveform_fill_color_title_normal.setGeometry(45,25,30,15)
    self.playercontrols_properties_panel_tabwidget_waveform_fill_color_button.setGeometry(45,40,30,30)
    self.playercontrols_properties_panel_tabwidget_background_title_normal.setGeometry(10,10,100,15)
    self.playercontrols_properties_panel_tabwidget_background_time_text_color_title_normal.setGeometry(10,25,30,15)
    self.playercontrols_properties_panel_tabwidget_background_time_text_color_button.setGeometry(10,40,30,30)
    self.playercontrols_properties_panel_tabwidget_background_cursor_color_title_normal.setGeometry(45,25,30,15)
    self.playercontrols_properties_panel_tabwidget_background_cursor_color_button.setGeometry(45,40,30,30)
    self.playercontrols_properties_panel_tabwidget_background_grid_color_title_normal.setGeometry(80,25,30,15)
    self.playercontrols_properties_panel_tabwidget_background_grid_color_button.setGeometry(80,40,30,30)

    self.playercontrols_stop_button.setGeometry((self.playercontrols_widget_central_top.width()*.5)-55, 11, 50, 43)
    self.playercontrols_playpause_button.setGeometry((self.playercontrols_widget_central_top.width()*.5)-5, 11, 60, 43)
    self.playercontrols_play_from_last_start_button.setGeometry(self.playercontrols_stop_button.x()-50, 11, 50, 43)
    self.playercontrols_play_from_next_start_button.setGeometry(self.playercontrols_playpause_button.x()+self.playercontrols_playpause_button.width(), 11, 50, 43)

    self.move_backward_subtitle.setGeometry((self.playercontrols_widget.width()*.5)-107, 61, 25, 23)
    self.move_start_back_subtitle.setGeometry((self.playercontrols_widget.width()*.5)-159, 61, 25, 23)
    self.move_start_forward_subtitle.setGeometry((self.playercontrols_widget.width()*.5)-134, 61, 25, 23)

    self.timeline_cursor_back_frame.setGeometry((self.playercontrols_widget.width()*.5)-80, 61, 25, 23)

    self.remove_selected_subtitle_button.setGeometry(self.move_start_back_subtitle.x() - 5 - 100, self.add_subtitle_button.y(), 100, 40)

    self.add_subtitle_button.setGeometry(self.remove_selected_subtitle_button.x() - 178, 44, 178, 40)
    self.add_subtitle_duration.setGeometry(66, 8, 46, self.add_subtitle_button.height()-14)
    self.add_subtitle_starting_from_last.setGeometry(self.add_subtitle_duration.x() + self.add_subtitle_duration.width() + 2, 8, self.add_subtitle_button.height()-14, self.add_subtitle_button.height()-8)
    self.add_subtitle_and_play.setGeometry(self.add_subtitle_starting_from_last.x() + self.add_subtitle_starting_from_last.width(), 8, self.add_subtitle_button.height()-14, self.add_subtitle_button.height()-8)

    self.gap_add_subtitle_button.setGeometry(self.add_subtitle_button.x()-131, 44, 63, 40)
    self.gap_remove_subtitle_button.setGeometry(self.gap_add_subtitle_button.x()+self.gap_add_subtitle_button.width(), 44, 63, self.gap_add_subtitle_button.height())
    self.gap_subtitle_duration.setGeometry(self.gap_add_subtitle_button.x()+40, 51, 46, self.gap_add_subtitle_button.height()-14)

    self.timeline_cursor_next_frame.setGeometry((self.playercontrols_widget.width()*.5)+55, 61, 25, 23)

    self.move_forward_subtitle.setGeometry((self.playercontrols_widget.width()*.5)+82, 61, 25, 23)
    self.move_end_back_subtitle.setGeometry((self.playercontrols_widget.width()*.5)+109, 61, 25, 23)
    self.move_end_forward_subtitle.setGeometry((self.playercontrols_widget.width()*.5)+134, 61, 25, 23)

    self.merge_back_selected_subtitle_button.setGeometry((self.playercontrols_widget.width()*.5)+164, 44, 40, 40)
    self.slice_selected_subtitle_button.setGeometry(self.merge_back_selected_subtitle_button.x() + self.merge_back_selected_subtitle_button.width(), self.merge_back_selected_subtitle_button.y(), 40, 40)
    self.merge_next_selected_subtitle_button.setGeometry(self.slice_selected_subtitle_button.x() + self.slice_selected_subtitle_button.width(), self.merge_back_selected_subtitle_button.y(), 40, 40)

    self.next_start_to_current_position_button.setGeometry(self.merge_next_selected_subtitle_button.x()+self.merge_next_selected_subtitle_button.width()+5, 44, 50, 40)
    self.subtitle_start_to_current_position_button.setGeometry(self.next_start_to_current_position_button.x()+40, 50, 20, 34)
    self.last_start_to_current_position_button.setGeometry(self.next_start_to_current_position_button.x()+self.next_start_to_current_position_button.width(), self.next_start_to_current_position_button.y(), 50, 40)
    self.next_end_to_current_position_button.setGeometry(self.last_start_to_current_position_button.x()+self.last_start_to_current_position_button.width(), self.next_start_to_current_position_button.y(), 50, 40)
    self.subtitle_end_to_current_position_button.setGeometry(self.next_end_to_current_position_button.x()+40, 50, 20, 34)
    self.last_end_to_current_position_button.setGeometry(self.next_end_to_current_position_button.x()+self.next_end_to_current_position_button.width(), self.next_start_to_current_position_button.y(), 50, 40)

    self.change_playback_speed.setGeometry(self.playercontrols_widget_central_top.x()-182, 7, 180, 36)
    self.change_playback_speed_icon_label.setGeometry(0, 0, self.change_playback_speed.height(), self.change_playback_speed.height())
    self.change_playback_speed_decrease.setGeometry(70, 10, 20, 20)
    self.change_playback_speed_slider.setGeometry(90, 10, 60, 20)
    self.change_playback_speed_increase.setGeometry(150, 10, 20, 20)

    self.repeat_playback.setGeometry(self.playercontrols_widget_central_top.x()+self.playercontrols_widget_central_top.width()+2, 7, 150, 36)
    self.repeat_playback_icon_label.setGeometry(0, 0, self.repeat_playback.height(), self.repeat_playback.height())
    self.repeat_playback_duration.setGeometry(self.repeat_playback_icon_label.x()+self.repeat_playback_icon_label.width(), 6, 46, self.repeat_playback.height()-14)
    self.repeat_playback_x_label.setGeometry(self.repeat_playback_duration.x()+self.repeat_playback_duration.width(), 0, 15, self.repeat_playback.height())
    self.repeat_playback_times.setGeometry(self.repeat_playback_x_label.x()+self.repeat_playback_x_label.width(), 6, 40, self.repeat_playback.height()-14)

    self.zoomout_button.setGeometry(self.last_end_to_current_position_button.x() + self.last_end_to_current_position_button.width() + 5, 44, 40, 40)
    self.zoomin_button.setGeometry(self.zoomout_button.x() + self.zoomout_button.width(), 44, 40, 40)

    self.grid_button.setGeometry(self.change_playback_speed.x()-145, 7, 50, 24)
    self.grid_frames_button.setGeometry(self.grid_button.x()+self.grid_button.width(), self.grid_button.y(), 30, self.grid_button.height())
    self.grid_seconds_button.setGeometry(self.grid_frames_button.x()+self.grid_frames_button.width(), self.grid_button.y(), 30, self.grid_button.height())
    self.grid_scenes_button.setGeometry(self.grid_seconds_button.x()+self.grid_seconds_button.width(), self.grid_button.y(), 30, self.grid_button.height())

    self.snap_button.setGeometry(self.repeat_playback.x()+self.repeat_playback.width()+5, 7, 100, 24)
    self.snap_value.setGeometry(self.snap_button.width()-50, 4, 46, self.snap_button.height()-8)
    self.snap_limits_button.setGeometry(self.snap_button.x()+self.snap_button.width(), self.snap_button.y(), 30, self.snap_button.height())
    self.snap_move_button.setGeometry(self.snap_limits_button.x()+self.snap_limits_button.width(), self.snap_button.y(), 30, self.snap_button.height())
    self.snap_grid_button.setGeometry(self.snap_move_button.x()+self.snap_move_button.width(), self.snap_button.y(), 30, self.snap_button.height())
    self.snap_move_nereast_button.setGeometry(self.snap_grid_button.x()+self.snap_grid_button.width(), self.snap_button.y(), 30, self.snap_button.height())

    self.step_button.setGeometry(self.snap_move_nereast_button.x()+self.snap_move_nereast_button.width()+5, 7, 160, 24)
    self.step_value_f.setGeometry(self.step_button.width()-112, 4, 46, self.step_button.height()-8)
    self.step_value_i.setGeometry(self.step_button.width()-112, 4, 46, self.step_button.height()-8)
    self.step_unit.setGeometry(self.step_button.width()-65, 4, 58, self.step_button.height()-8)

    self.timelinescrolling_none_button.setGeometry(self.grid_button.x() - 95, 7, 30, self.grid_button.height())
    self.timelinescrolling_page_button.setGeometry(self.grid_button.x() - 65, 7, 30, self.grid_button.height())
    self.timelinescrolling_follow_button.setGeometry(self.grid_button.x() - 35, 7, 30, self.grid_button.height())


def playercontrols_stop_button_clicked(self):
    """Function to call when stop button is clicked"""
    # self.player_widget.position = 0.0
    # self.update_timeline.stop()
    playercontrols_playpause_button_clicked(self)
    self.player_widget.stop()
    self.playercontrols_playpause_button.setChecked(False)
    playercontrols_playpause_button_update(self)
    # self.timeline.update_scrollbar(self)
    self.timeline.update(self)


def playercontrols_playpause_button_clicked(self):
    """Function to call when play/pause button is clicked"""
    self.player_widget.pause()
    if self.repeat_activated:
        self.repeat_duration_tmp = []
    if not self.player_widget.mpv.pause and not self.playercontrols_playpause_button.isChecked():
        self.playercontrols_playpause_button.setChecked(True)
    elif self.player_widget.mpv.pause and self.playercontrols_playpause_button.isChecked():
        self.playercontrols_playpause_button.setChecked(False)
    playercontrols_playpause_button_update(self)


def playercontrols_playpause_button_update(self):
    """Function to update things when stop button is clicked"""
    self.playercontrols_playpause_button.setIcon(QIcon(os.path.join(PATH_SUBTITLD_GRAPHICS, 'pause_icon.png')) if self.playercontrols_playpause_button.isChecked() else QIcon(os.path.join(PATH_SUBTITLD_GRAPHICS, 'play_icon.png')))


def show(self):
    """Function that shows the entire panel"""
    self.generate_effect(self.playercontrols_widget_animation, 'geometry', 1000, [self.playercontrols_widget.x(), self.playercontrols_widget.y(), self.playercontrols_widget.width(), self.playercontrols_widget.height()], [self.playercontrols_widget.x(), self.height()-200, self.playercontrols_widget.width(), self.playercontrols_widget.height()])
    update_snap_buttons(self)
    update_grid_buttons(self)
    update_step_buttons(self)
    update_playback_speed_buttons(self)
    timelinescrolling_type_changed(self, self.settings['timeline'].get('scrolling', 'page'))
    self.add_subtitle_duration.setValue(self.default_new_subtitle_duration)
    self.gap_subtitle_duration.setValue(2.0)
    self.repeat_playback_duration.setValue(self.repeat_duration)
    self.repeat_playback_times.setValue(self.repeat_times)


def zoomin_button_clicked(self):
    """Function to call when zoonin button is clicked"""
    self.mediaplayer_zoom += 10.0
    zoom_buttons_update(self)


def zoomout_button_clicked(self):
    """Function to call when zoonout button is clicked"""
    self.mediaplayer_zoom -= 10.0
    zoom_buttons_update(self)


def zoom_buttons_update(self):
    """Function to update zoom buttons"""
    self.zoomout_button.setEnabled(True if self.mediaplayer_zoom - 5.0 > 0.0 else False)
    self.zoomin_button.setEnabled(True if self.mediaplayer_zoom + 5.0 < 500.0 else False)
    proportion = ((self.player_widget.position*self.timeline_widget.width_proportion)-self.timeline_scroll.horizontalScrollBar().value())/self.timeline_scroll.width()
    self.timeline_widget.setGeometry(0, 0, int(round(self.video_metadata.get('duration', 0.01)*self.mediaplayer_zoom)), self.timeline_scroll.height()-20)
    # self.timeline.zoom_update_waveform(self)
    self.timeline.update_scrollbar(self, position=proportion)


def snap_button_clicked(self):
    """Function to call when snap button is clicked"""
    self.timeline_snap = self.snap_button.isChecked()
    update_snap_buttons(self)


def snap_move_button_clicked(self):
    """Function to call when snap move button is clicked"""
    self.timeline_snap_moving = self.snap_move_button.isChecked()


def snap_move_nereast_button_clicked(self):
    """Function to call when snap move next button is clicked"""
    self.timeline_snap_move_nereast = self.snap_move_nereast_button.isChecked()


def snap_limits_button_clicked(self):
    """Function to call when snap limits button is clicked"""
    self.timeline_snap_limits = self.snap_limits_button.isChecked()


def snap_grid_button_clicked(self):
    """Function to call when snap to grid button is clicked"""
    self.timeline_snap_grid = self.snap_grid_button.isChecked()


def snap_value_changed(self):
    """Function to call when snap value is changed"""
    self.timeline_snap_value = self.snap_value.value() if self.snap_value.value() else .1


def step_value_changed(self):
    """Function to set variables to settings"""
    self.settings['timeline']['step_unit'] = self.step_unit.currentText()
    if self.settings['timeline'].get('step_unit', 'Frames') == 'Seconds':
        self.settings['timeline']['step_value'] = self.step_value_f.value()
    else:
        self.settings['timeline']['step_value'] = self.step_value_i.value()
    update_step_information(self)


def update_step_buttons(self):
    """Function to update step widgets"""
    self.step_value_f.setEnabled(self.step_button.isChecked())
    self.step_value_i.setEnabled(self.step_button.isChecked())
    self.step_unit.setEnabled(self.step_button.isChecked())
    update_step_information(self)


def update_step_information(self):
    """Updates the widgets information"""
    self.step_unit.setCurrentIndex(STEPS_LIST.index(self.settings['timeline'].get('step_unit', 'Frames')))
    self.step_value_f.setValue(float(self.settings['timeline'].get('step_value', 1.0)))
    self.step_value_i.setValue(int(self.settings['timeline'].get('step_value', 1)))
    self.step_value_f.setVisible(self.settings['timeline'].get('step_unit', 'Frames') == 'Seconds')
    self.step_value_i.setVisible(self.settings['timeline'].get('step_unit', 'Frames') == 'Frames')


def timelinescrolling_type_changed(self, scrollingtype='page'):
    """Function to call when timeline scrolling method is changed"""
    self.timelinescrolling_none_button.setChecked((scrollingtype == 'none'))
    self.timelinescrolling_page_button.setChecked((scrollingtype == 'page'))
    self.timelinescrolling_follow_button.setChecked((scrollingtype == 'follow'))
    self.settings['timeline']['scrolling'] = scrollingtype


def add_subtitle_duration_changed(self):
    """Function to call when subtitle default duration is changed"""
    self.default_new_subtitle_duration = self.add_subtitle_duration.value()


def add_subtitle_starting_from_last_clicked(self):
    self.timeline_widget.setFocus(Qt.TabFocusReason)

def add_subtitle_and_play_clicked(self):
    self.timeline_widget.setFocus(Qt.TabFocusReason)

def gap_add_subtitle_button_clicked(self):
    """Function to call when add gap button is clicked"""
    subtitles.set_gap(subtitles=self.subtitles_list, position=self.player_widget.position, gap=self.gap_subtitle_duration.value())
    self.unsaved = True
    self.selected_subtitle = False
    self.timeline.update(self)
    self.timeline_widget.setFocus(Qt.TabFocusReason)


def gap_remove_subtitle_button_clicked(self):
    """Function to call when remove gap button is clicked"""
    subtitles.set_gap(subtitles=self.subtitles_list, position=self.player_widget.position, gap=-(self.gap_subtitle_duration.value()))
    self.unsaved = True
    self.selected_subtitle = False
    self.timeline.update(self)
    self.timeline_widget.setFocus(Qt.TabFocusReason)


def update_snap_buttons(self):
    """Function to update snap buttons"""
    self.snap_button.setChecked(bool(self.timeline_snap))
    self.snap_limits_button.setEnabled(self.snap_button.isChecked())
    self.snap_limits_button.setChecked(bool(self.timeline_snap_limits))
    self.snap_move_button.setEnabled(self.snap_button.isChecked())
    self.snap_move_button.setChecked(bool(self.timeline_snap_moving))
    self.snap_grid_button.setEnabled(self.snap_button.isChecked())
    self.snap_grid_button.setChecked(bool(self.timeline_snap_grid))
    self.snap_move_nereast_button.setEnabled(self.snap_button.isChecked())
    self.snap_move_nereast_button.setChecked(bool(self.timeline_snap_move_nereast))
    self.snap_value.setEnabled(self.snap_button.isChecked())
    self.snap_value.setValue(self.timeline_snap_value if self.timeline_snap_value else .1)
    self.timeline_widget.update()


def update_playback_speed_buttons(self):
    """Function to update playback speed buttons"""
    self.change_playback_speed_icon_label.setEnabled(self.change_playback_speed.isChecked())
    self.change_playback_speed_decrease.setEnabled(self.change_playback_speed.isChecked())
    self.change_playback_speed_slider.setEnabled(self.change_playback_speed.isChecked())
    self.change_playback_speed_increase.setEnabled(self.change_playback_speed.isChecked())
    self.change_playback_speed.setText('x' + str(self.playback_speed))
    self.change_playback_speed_slider.setValue(self.playback_speed*100)


def grid_button_clicked(self):
    """Function to call when grid button is clicked"""
    self.timeline_show_grid = self.grid_button.isChecked()
    if not self.timeline_grid_type:
        self.timeline_grid_type = 'seconds'
    update_grid_buttons(self)


def grid_type_changed(self, gridtype):
    """Function to call when grid type button is clicked"""
    self.timeline_grid_type = gridtype
    update_grid_buttons(self)


def update_grid_buttons(self):
    """Function to update grid buttons"""
    self.grid_button.setChecked(self.timeline_show_grid)
    self.grid_frames_button.setEnabled(self.timeline_show_grid)
    self.grid_frames_button.setChecked(True if self.timeline_grid_type == 'frames' else False)
    self.grid_seconds_button.setEnabled(self.timeline_show_grid)
    self.grid_seconds_button.setChecked(True if self.timeline_grid_type == 'seconds' else False)
    self.grid_scenes_button.setEnabled(self.timeline_show_grid)
    self.grid_scenes_button.setChecked(True if self.timeline_grid_type == 'scenes' else False)
    self.timeline_widget.update()


def playercontrols_play_from_last_start_button_clicked(self):
    """Function to call when stop button is clicked"""
    subt = [item[0] for item in self.subtitles_list]
    last_subtitle = self.subtitles_list[bisect(subt, self.player_widget.position)-1]
    self.player_widget.seek(last_subtitle[0])
    self.player_widget.play()
    self.timeline.update_scrollbar(self)
    self.timeline.update(self)
    self.timeline_widget.setFocus(Qt.TabFocusReason)


def playercontrols_play_from_next_start_button_clicked(self):
    """Function to call when play from next subtitle button is clicked"""
    subt = [item[0] for item in self.subtitles_list]
    i = bisect(subt, self.player_widget.position)
    if i < len(self.subtitles_list):
        last_subtitle = self.subtitles_list[i]
        self.player_widget.seek(last_subtitle[0])
        self.player_widget.play()
        self.timeline.update_scrollbar(self)
        self.timeline.update(self)
        self.timeline_widget.setFocus(Qt.TabFocusReason)


def add_subtitle_button_clicked(self):
    """Function to call when add subtitle button is clicked"""
    start_position = False
    self.selected_subtitle = subtitles.add_subtitle(subtitles=self.subtitles_list, position=self.player_widget.position, duration=self.default_new_subtitle_duration, from_last_subtitle=self.add_subtitle_starting_from_last.isChecked())
    self.unsaved = True
    self.subtitleslist.update_subtitles_list_qlistwidget(self)
    self.timeline.update(self)
    self.properties.update_properties_widget(self)
    self.properties_textedit.setFocus(Qt.TabFocusReason)
    if self.add_subtitle_and_play.isChecked():
        self.player_widget.play()


def remove_selected_subtitle_button_clicked(self):
    """Function to call when remove selected subtitle button is clicked"""
    subtitles.remove_subtitle(subtitles=self.subtitles_list, selected_subtitle=self.selected_subtitle)
    self.unsaved = True
    self.selected_subtitle = False
    self.subtitleslist.update_subtitles_list_qlistwidget(self)
    self.timeline.update(self)
    self.properties.update_properties_widget(self)
    self.timeline_widget.setFocus(Qt.TabFocusReason)


def slice_selected_subtitle_button_clicked(self):
    """Function to call when slice selected subtitle button is clicked"""
    if self.selected_subtitle:
        pos = self.properties_textedit.textCursor().position()
        last_text = self.properties_textedit.toPlainText()[:pos]
        next_text = self.properties_textedit.toPlainText()[pos:]
        self.selected_subtitle = subtitles.slice_subtitle(subtitles=self.subtitles_list, selected_subtitle=self.selected_subtitle, position=self.player_widget.position, next_text=next_text, last_text=last_text)
        self.unsaved = True
        self.subtitleslist.update_subtitles_list_qlistwidget(self)
        self.timeline.update(self)
        self.properties.update_properties_widget(self)
        self.timeline_widget.setFocus(Qt.TabFocusReason)


def select_subtitle_in_current_position(self):
    """Function to call when actual subtitle under cursor need to be selected"""
    subtitle, _ = subtitles.subtitle_under_current_position(subtitles=self.subtitles_list, position=self.player_widget.position)
    if subtitle:
        self.selected_subtitle = subtitle
        self.subtitleslist.update_subtitles_list_qlistwidget(self)
        self.timeline.update(self)
        self.properties.update_properties_widget(self)


def select_next_subtitle_over_current_position(self):
    """Function to call when next subtitle under cursor need to be selected"""
    subtitle = subtitles.next_subtitle_current_position(subtitles=self.subtitles_list, position=self.player_widget.position)
    if subtitle:
        self.selected_subtitle = subtitle
        self.subtitleslist.update_subtitles_list_qlistwidget(self)
        self.timeline.update(self)
        self.properties.update_properties_widget(self)


def select_last_subtitle_over_current_position(self):
    """Function to call when last subtitle under cursor need to be selected"""
    subtitle = subtitles.last_subtitle_current_position(subtitles=self.subtitles_list, position=self.player_widget.position)
    if subtitle:
        self.selected_subtitle = subtitle
        self.subtitleslist.update_subtitles_list_qlistwidget(self)
        self.timeline.update(self)
        self.properties.update_properties_widget(self)


def merge_back_selected_subtitle_button_clicked(self):
    """Function to merge selected subtitle with the last subtitle"""
    if self.selected_subtitle:
        self.selected_subtitle = subtitles.merge_back_subtitle(subtitles=self.subtitles_list, selected_subtitle=self.selected_subtitle)
        self.unsaved = True
        self.subtitleslist.update_subtitles_list_qlistwidget(self)
        self.timeline.update(self)
        self.properties.update_properties_widget(self)
        self.timeline_widget.setFocus(Qt.TabFocusReason)


def merge_next_selected_subtitle_button_clicked(self):
    """Function to merge selected subtitle with the next subtitle"""
    if self.selected_subtitle:
        self.selected_subtitle = subtitles.merge_next_subtitle(subtitles=self.subtitles_list, selected_subtitle=self.selected_subtitle)
        self.unsaved = True
        self.subtitleslist.update_subtitles_list_qlistwidget(self)
        self.timeline.update(self)
        self.properties.update_properties_widget(self)
        self.timeline_widget.setFocus(Qt.TabFocusReason)


def move_backward_subtitle_clicked(self):
    """Function to move subtitle backward"""
    if self.selected_subtitle:
        amount = (1.0 / self.video_metadata['framerate'])
        if self.step_button.isChecked():
            if self.settings['timeline'].get('step_unit', 'Frames') == 'Frames':
                amount = (int(self.settings['timeline'].get('step_value', 1)) / self.video_metadata['framerate'])
            else:
                amount = float(self.settings['timeline'].get('step_value', 1.0))
        subtitles.move_subtitle(subtitles=self.subtitles_list, selected_subtitle=self.selected_subtitle, amount=-amount)
        self.unsaved = True
        self.timeline.update(self)
        self.timeline_widget.setFocus(Qt.TabFocusReason)


def move_forward_subtitle_clicked(self):
    """Function to move subtitle forward"""
    if self.selected_subtitle:
        amount = (1.0 / self.video_metadata['framerate'])
        if self.step_button.isChecked():
            if self.settings['timeline'].get('step_unit', 'Frames') == 'Frames':
                amount = (int(self.settings['timeline'].get('step_value', 1)) / self.video_metadata['framerate'])
            else:
                amount = float(self.settings['timeline'].get('step_value', 1.0))
        subtitles.move_subtitle(subtitles=self.subtitles_list, selected_subtitle=self.selected_subtitle, amount=amount)
        self.unsaved = True
        self.timeline.update(self)
        self.timeline_widget.setFocus(Qt.TabFocusReason)


def move_start_back_subtitle_clicked(self):
    """Function to move starting position of selected subtitle backward"""
    if self.selected_subtitle:
        amount = (1.0 / self.video_metadata['framerate'])
        if self.step_button.isChecked():
            if self.settings['timeline'].get('step_unit', 'Frames') == 'Frames':
                amount = (int(self.settings['timeline'].get('step_value', 1)) / self.video_metadata['framerate'])
            else:
                amount = float(self.settings['timeline'].get('step_value', 1.0))
        subtitles.move_start_subtitle(subtitles=self.subtitles_list, selected_subtitle=self.selected_subtitle, amount=-amount, move_nereast=bool(self.timeline_snap_move_nereast))
        self.unsaved = True
        self.timeline.update(self)
        self.timeline_widget.setFocus(Qt.TabFocusReason)


def move_start_forward_subtitle_clicked(self):
    """Function to move starting position of selected subtitle forward"""
    if self.selected_subtitle:
        amount = (1.0 / self.video_metadata['framerate'])
        if self.step_button.isChecked():
            if self.settings['timeline'].get('step_unit', 'Frames') == 'Frames':
                amount = (int(self.settings['timeline'].get('step_value', 1)) / self.video_metadata['framerate'])
            else:
                amount = float(self.settings['timeline'].get('step_value', 1.0))
        subtitles.move_start_subtitle(subtitles=self.subtitles_list, selected_subtitle=self.selected_subtitle, amount=amount, move_nereast=bool(self.timeline_snap_move_nereast))
        self.unsaved = True
        self.timeline.update(self)
        self.timeline_widget.setFocus(Qt.TabFocusReason)


def move_end_back_subtitle_clicked(self):
    """Function to move ending position of selected subtitle backwards"""
    if self.selected_subtitle:
        amount = (1.0 / self.video_metadata['framerate'])
        if self.step_button.isChecked():
            if self.settings['timeline'].get('step_unit', 'Frames') == 'Frames':
                amount = (int(self.settings['timeline'].get('step_value', 1)) / self.video_metadata['framerate'])
            else:
                amount = float(self.settings['timeline'].get('step_value', 1.0))
        subtitles.move_end_subtitle(subtitles=self.subtitles_list, selected_subtitle=self.selected_subtitle, amount=-amount)
        self.unsaved = True
        self.timeline.update(self)
        self.timeline_widget.setFocus(Qt.TabFocusReason)


def move_end_forward_subtitle_clicked(self):
    """Function to move ending position of selected subtitle forward"""
    if self.selected_subtitle:
        amount = (1.0 / self.video_metadata['framerate'])
        if self.step_button.isChecked():
            if self.settings['timeline'].get('step_unit', 'Frames') == 'Frames':
                amount = (int(self.settings['timeline'].get('step_value', 1)) / self.video_metadata['framerate'])
            else:
                amount = float(self.settings['timeline'].get('step_value', 1.0))
        subtitles.move_end_subtitle(subtitles=self.subtitles_list, selected_subtitle=self.selected_subtitle, amount=amount)
        self.unsaved = True
        self.timeline.update(self)
        self.timeline_widget.setFocus(Qt.TabFocusReason)


def timeline_cursor_back_frame_clicked(self):
    """Function to move cursor one frame backward"""
    self.player_widget.frameBackStep()
    self.timeline_widget.setFocus(Qt.TabFocusReason)


def timeline_cursor_next_frame_clicked(self):
    """Function to move cursor one frame forward"""
    self.player_widget.frameStep()
    self.timeline_widget.setFocus(Qt.TabFocusReason)


def next_start_to_current_position_button_clicked(self):
    """Function to move cursor one frame backward"""
    subtitles.next_start_to_current_position(subtitles=self.subtitles_list, position=self.player_widget.position)
    self.unsaved = True
    self.subtitleslist.update_subtitles_list_qlistwidget(self)
    self.timeline.update(self)
    self.properties.update_properties_widget(self)
    self.timeline_widget.setFocus(Qt.TabFocusReason)


def last_end_to_current_position_button_clicked(self):
    """Function to move last ending position of selected subtitle to current cursor position"""
    subtitles.last_end_to_current_position(subtitles=self.subtitles_list, position=self.player_widget.position)
    self.unsaved = True
    self.subtitleslist.update_subtitles_list_qlistwidget(self)
    self.timeline.update(self)
    self.properties.update_properties_widget(self)
    self.timeline_widget.setFocus(Qt.TabFocusReason)


def last_start_to_current_position_button_clicked(self):
    """Function to move last starting position subtitle to current cursor position"""
    subtitles.last_start_to_current_position(subtitles=self.subtitles_list, position=self.player_widget.position)
    self.unsaved = True
    self.subtitleslist.update_subtitles_list_qlistwidget(self)
    self.timeline.update(self)
    self.properties.update_properties_widget(self)
    self.timeline_widget.setFocus(Qt.TabFocusReason)


def subtitle_start_to_current_position_button_clicked(self):
    """Function to move starting position subtitle to current cursor position"""
    subtitles.subtitle_start_to_current_position(subtitles=self.subtitles_list, position=self.player_widget.position)
    self.unsaved = True
    self.subtitleslist.update_subtitles_list_qlistwidget(self)
    self.timeline.update(self)
    self.properties.update_properties_widget(self)
    self.timeline_widget.setFocus(Qt.TabFocusReason)


def subtitle_end_to_current_position_button_clicked(self):
    """Function to move ending position subtitle to current cursor position"""
    subtitles.subtitle_end_to_current_position(subtitles=self.subtitles_list, position=self.player_widget.position)
    self.unsaved = True
    self.subtitleslist.update_subtitles_list_qlistwidget(self)
    self.timeline.update(self)
    self.properties.update_properties_widget(self)
    self.timeline_widget.setFocus(Qt.TabFocusReason)


def next_end_to_current_position_button_clicked(self):
    """Function to move next ending position to current cursor position"""
    subtitles.next_end_to_current_position(subtitles=self.subtitles_list, position=self.player_widget.position)
    self.unsaved = True
    self.subtitleslist.update_subtitles_list_qlistwidget(self)
    self.timeline.update(self)
    self.properties.update_properties_widget(self)
    self.timeline_widget.setFocus(Qt.TabFocusReason)


def change_playback_speed_clicked(self):
    """Function to call when playback speed button is clicked"""
    if not self.change_playback_speed.isChecked():
        self.playback_speed = 1.0
        self.player.update_speed(self)
    update_playback_speed_buttons(self)
    self.timeline_widget.setFocus(Qt.TabFocusReason)


def change_playback_speed_decrease_clicked(self):
    """Function to call when playback speed decrease button is clicked"""
    self.change_playback_speed_slider.setValue(self.change_playback_speed_slider.value()-10)
    self.playback_speed = self.change_playback_speed_slider.value()/100.0
    self.player.update_speed(self)
    update_playback_speed_buttons(self)
    self.timeline_widget.setFocus(Qt.TabFocusReason)


def change_playback_speed_slider(self):
    """Function to call when playback speed slider button is changed"""
    self.playback_speed = self.change_playback_speed_slider.value()/100.0
    self.player.update_speed(self)
    update_playback_speed_buttons(self)
    self.timeline_widget.setFocus(Qt.TabFocusReason)


def change_playback_speed_increase_clicked(self):
    """Function to call when playback speed increase button is clicked"""
    self.change_playback_speed_slider.setValue(self.change_playback_speed_slider.value()+10)
    self.playback_speed = self.change_playback_speed_slider.value()/100.0
    self.player.update_speed(self)
    update_playback_speed_buttons(self)
    self.timeline_widget.setFocus(Qt.TabFocusReason)


def repeat_playback_clicked(self):
    """Function to call when playback repeat button is clicked"""
    self.repeat_activated = self.repeat_playback.isChecked()
    self.timeline_widget.setFocus(Qt.TabFocusReason)


def repeat_playback_duration_changed(self):
    """Function to call when playback repeat duration is changed"""
    self.repeat_duration = self.repeat_playback_duration.value()
    self.timeline_widget.setFocus(Qt.TabFocusReason)


def repeat_playback_times_changed(self):
    """Function to call when playback repeat number of times is changed"""
    self.repeat_times = self.repeat_playback_times.value()
    self.timeline_widget.setFocus(Qt.TabFocusReason)


def playercontrols_properties_panel_tabwidget_subtitles_update_widgets(self):
    self.playercontrols_properties_panel_tabwidget_subtitles_selected_subtitle_border_color_button.setStyleSheet('background-color: {color};'.format(color=self.settings['timeline'].get('selected_subtitle_border_color', '#cc3e5363')))
    self.playercontrols_properties_panel_tabwidget_subtitles_selected_subtitle_fill_color_button.setStyleSheet('background-color: {color};'.format(color=self.settings['timeline'].get('selected_subtitle_fill_color', '#cc3e5363')))
    self.playercontrols_properties_panel_tabwidget_subtitles_selected_subtitle_text_color_button.setStyleSheet('background-color: {color};'.format(color=self.settings['timeline'].get('selected_subtitle_text_color', '#ffffffff')))
    self.playercontrols_properties_panel_tabwidget_subtitles_subtitle_border_color_button.setStyleSheet('background-color: {color};'.format(color=self.settings['timeline'].get('subtitle_border_color', '#ff6a7483')))
    self.playercontrols_properties_panel_tabwidget_subtitles_subtitle_fill_color_button.setStyleSheet('background-color: {color};'.format(color=self.settings['timeline'].get('subtitle_fill_color', '#ccb8cee0')))
    self.playercontrols_properties_panel_tabwidget_subtitles_subtitle_text_color_button.setStyleSheet('background-color: {color};'.format(color=self.settings['timeline'].get('subtitle_text_color', '#ff304251')))
    self.playercontrols_properties_panel_tabwidget_subtitles_subtitle_arrow_normal_button.setStyleSheet('background-color: {color};'.format(color=self.settings['timeline'].get('subtitle_arrow_color', '#ff969696')))
    self.playercontrols_properties_panel_tabwidget_subtitles_selected_subtitle_arrow_normal_button.setStyleSheet('background-color: {color};'.format(color=self.settings['timeline'].get('selected_subtitle_arrow_color', '#ff969696')))
    self.playercontrols_properties_panel_tabwidget_waveform_border_color_button.setStyleSheet('background-color: {color};'.format(color=self.settings['timeline'].get('waveform_border_color', '#ff153450')))
    self.playercontrols_properties_panel_tabwidget_waveform_fill_color_button.setStyleSheet('background-color: {color};'.format(color=self.settings['timeline'].get('waveform_fill_color', '#cc153450')))
    self.playercontrols_properties_panel_tabwidget_background_grid_color_button.setStyleSheet('background-color: {color};'.format(color=self.settings['timeline'].get('grid_color', '#336a7483')))
    self.playercontrols_properties_panel_tabwidget_background_time_text_color_button.setStyleSheet('background-color: {color};'.format(color=self.settings['timeline'].get('time_text_color', '#806a7483')))
    self.playercontrols_properties_panel_tabwidget_background_cursor_color_button.setStyleSheet('background-color: {color};'.format(color=self.settings['timeline'].get('cursor_color', '#ccff0000')))




def show_or_hide_playercontrols_properties_panel(self):
    """Function to show playercontrol properties panel"""
    panel_width = 365
    if self.playercontrols_properties_panel_toggle.isChecked():
        self.playercontrols_properties_panel_placeholder.setGeometry(self.playercontrols_widget.width()-panel_width, 5, panel_width, 180)
        self.playercontrols_properties_panel.setGeometry(0, 56, self.playercontrols_properties_panel_placeholder.width(), 140)
        self.playercontrols_properties_panel_toggle.setGeometry(self.playercontrols_widget_bottom_right_corner.x(), self.playercontrols_widget_bottom_right_corner.y()+100, self.playercontrols_widget_bottom_right_corner.width(), self.playercontrols_widget_bottom_right_corner.height())
    else:
        self.playercontrols_properties_panel_placeholder.setGeometry(self.playercontrols_widget.width()-panel_width, 5, panel_width, 80)
        self.playercontrols_properties_panel.setGeometry(0, 56, self.playercontrols_properties_panel_placeholder.width(), 140)
        self.playercontrols_properties_panel_toggle.setGeometry(self.playercontrols_widget_bottom_right_corner.x(), self.playercontrols_widget_bottom_right_corner.y(), self.playercontrols_widget_bottom_right_corner.width(), self.playercontrols_widget_bottom_right_corner.height())

def playercontrols_properties_panel_toggle_pressed(self):
    playercontrols_properties_panel_tabwidget_subtitles_update_widgets(self)
    show_or_hide_playercontrols_properties_panel(self)


def playercontrols_properties_panel_tabwidget_subtitles_subtitle_border_color_button_clicked(self):
    """Function to show qcolordialog to choose subtitle border color"""
    color = QColorDialog.getColor(options=QColorDialog.ShowAlphaChannel)
    if color.isValid():
        self.settings['timeline']['subtitle_border_color'] =  color.name(1)
    playercontrols_properties_panel_tabwidget_subtitles_update_widgets(self)
    self.timeline_widget.update()


def playercontrols_properties_panel_tabwidget_subtitles_subtitle_fill_color_button_clicked(self):
    """Function to show qcolordialog to choose subtitle fill color"""
    color = QColorDialog.getColor(options=QColorDialog.ShowAlphaChannel)
    if color.isValid():
        self.settings['timeline']['subtitle_fill_color'] = color.name(1)
    playercontrols_properties_panel_tabwidget_subtitles_update_widgets(self)
    self.timeline_widget.update()


def playercontrols_properties_panel_tabwidget_subtitles_subtitle_text_color_button_clicked(self):
    """Function to show qcolordialog to choose subtitle text color"""
    color = QColorDialog.getColor(options=QColorDialog.ShowAlphaChannel)
    if color.isValid():
        self.settings['timeline']['subtitle_text_color'] = color.name(1)
    playercontrols_properties_panel_tabwidget_subtitles_update_widgets(self)
    self.timeline_widget.update()


def playercontrols_properties_panel_tabwidget_subtitles_selected_subtitle_border_color_button_clicked(self):
    """Function to show qcolordialog to choose selected subtitle border color"""
    color = QColorDialog.getColor(options=QColorDialog.ShowAlphaChannel)
    if color.isValid():
        self.settings['timeline']['selected_subtitle_border_color'] = color.name(1)
    playercontrols_properties_panel_tabwidget_subtitles_update_widgets(self)
    self.timeline_widget.update()


def playercontrols_properties_panel_tabwidget_subtitles_selected_subtitle_fill_color_button_clicked(self):
    """Function to show qcolordialog to choose selected subtitle fill color"""
    color = QColorDialog.getColor(options=QColorDialog.ShowAlphaChannel)
    if color.isValid():
        self.settings['timeline']['selected_subtitle_fill_color'] = color.name(1)
    playercontrols_properties_panel_tabwidget_subtitles_update_widgets(self)
    self.timeline_widget.update()


def playercontrols_properties_panel_tabwidget_subtitles_selected_subtitle_text_color_button_clicked(self):
    """Function to show qcolordialog to choose selected subtitle text color"""
    color = QColorDialog.getColor(options=QColorDialog.ShowAlphaChannel)
    if color.isValid():
        self.settings['timeline']['selected_subtitle_text_color'] = color.name(1)
    playercontrols_properties_panel_tabwidget_subtitles_update_widgets(self)
    self.timeline_widget.update()


def playercontrols_properties_panel_tabwidget_subtitles_subtitle_arrow_normal_button_clicked(self):
    """Function to show qcolordialog to choose selected subtitle arrow color"""
    color = QColorDialog.getColor(options=QColorDialog.ShowAlphaChannel)
    if color.isValid():
        self.settings['timeline']['subtitle_arrow_color'] = color.name(1)
    playercontrols_properties_panel_tabwidget_subtitles_update_widgets(self)
    self.timeline_widget.update()


def playercontrols_properties_panel_tabwidget_subtitles_selected_subtitle_arrow_normal_button_clicked(self):
    """Function to show qcolordialog to choose selected selected subtitle arrow color"""
    color = QColorDialog.getColor(options=QColorDialog.ShowAlphaChannel)
    if color.isValid():
        self.settings['timeline']['selected_subtitle_arrow_color'] = color.name(1)
    playercontrols_properties_panel_tabwidget_subtitles_update_widgets(self)
    self.timeline_widget.update()


def playercontrols_properties_panel_tabwidget_waveform_border_color_button_clicked(self):
    """Function to show qcolordialog to choose waveform border color"""
    color = QColorDialog.getColor(options=QColorDialog.ShowAlphaChannel)
    if color.isValid():
        for available_zoom in self.video_metadata['waveform']:
            if self.video_metadata['waveform'][available_zoom].get('qimages', []):
                self.video_metadata['waveform'][available_zoom]['qimages'] = []
        self.settings['timeline']['waveform_border_color'] = color.name(1)
        self.thread_get_qimages.border_color = self.settings['timeline'].get('waveform_border_color', '#ff153450')
        self.thread_get_qimages.fill_color = self.settings['timeline'].get('waveform_fill_color', '#cc153450')
        self.thread_get_qimages.start(QThread.IdlePriority)
    playercontrols_properties_panel_tabwidget_subtitles_update_widgets(self)
    self.timeline_widget.update()


def playercontrols_properties_panel_tabwidget_waveform_fill_color_button_clicked(self):
    """Function to show qcolordialog to choose waveform fill color"""
    color = QColorDialog.getColor(options=QColorDialog.ShowAlphaChannel)
    if color.isValid():
        for available_zoom in self.video_metadata['waveform']:
            if self.video_metadata['waveform'][available_zoom].get('qimages', []):
                self.video_metadata['waveform'][available_zoom]['qimages'] = []
        self.settings['timeline']['waveform_fill_color'] = color.name(1)
        self.thread_get_qimages.border_color = self.settings['timeline'].get('waveform_border_color', '#ff153450')
        self.thread_get_qimages.fill_color = self.settings['timeline'].get('waveform_fill_color', '#cc153450')
        self.thread_get_qimages.start(QThread.IdlePriority)
    playercontrols_properties_panel_tabwidget_subtitles_update_widgets(self)
    self.timeline_widget.update()


def playercontrols_properties_panel_tabwidget_background_grid_color_button_clicked(self):
    """Function to show qcolordialog to choose background start color"""
    color = QColorDialog.getColor(options=QColorDialog.ShowAlphaChannel)
    if color.isValid():
        self.settings['timeline']['grid_color'] = color.name(1)
    playercontrols_properties_panel_tabwidget_subtitles_update_widgets(self)
    self.timeline_widget.update()


def playercontrols_properties_panel_tabwidget_background_time_text_color_button_clicked(self):
    """Function to show qcolordialog to choose background end color"""
    color = QColorDialog.getColor(options=QColorDialog.ShowAlphaChannel)
    if color.isValid():
        self.settings['timeline']['time_text_color'] = color.name(1)
    playercontrols_properties_panel_tabwidget_subtitles_update_widgets(self)
    self.timeline_widget.update()

def playercontrols_properties_panel_tabwidget_background_cursor_color_button_clicked(self):
    """Function to show qcolordialog to choose background end color"""
    color = QColorDialog.getColor(options=QColorDialog.ShowAlphaChannel)
    if color.isValid():
        self.settings['timeline']['cursor_color'] = color.name(1)
    playercontrols_properties_panel_tabwidget_subtitles_update_widgets(self)
    self.timeline_widget.update()