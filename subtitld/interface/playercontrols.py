"""Player control widgets.

"""

import os
from bisect import bisect
from PySide6.QtWidgets import QPushButton, QLabel, QDoubleSpinBox, QSlider, QSpinBox, QComboBox, QTabWidget, QWidget, QStylePainter, QStyleOptionTab, QStyle, QTabBar, QColorDialog, QFrame, QHBoxLayout, QSizePolicy, QVBoxLayout, QLayout
from PySide6.QtCore import QPropertyAnimation, QEasingCurve, Qt, QRect, QPoint, QThread, QSize
from PySide6.QtGui import QIcon, QPainter, QLinearGradient, QBrush, QColor
from subtitld.interface import subtitles_panel
from subtitld.interface.translation import _

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
        event.accept()

def load(self):
    """Function to load player control widgets"""
    class playercontrols_widget(QLabel):
        """Class for timeline scroll area"""
        def __init__(self, parent=None):
            super().__init__(parent)
            self.parent = parent

        def paintEvent(self, event):
            painter = QPainter(self)

            painter.setRenderHint(QPainter.Antialiasing)

            visible_rect = QRect(0, 20, self.width(), self.height() - 20)
            background_gradient = QLinearGradient(0, 0, 0, self.height())
            background_gradient.setColorAt(0.0, QColor('#ff0e1418'))
            background_gradient.setColorAt(1.0, QColor('#ff0f1519'))
            painter.setBrush(QBrush(background_gradient))
            painter.drawRect(visible_rect)

            painter.end()
            event.accept()

    self.playercontrols_widget = playercontrols_widget(parent=self)
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
    self.playercontrols_properties_panel_tabwidget.setObjectName('playercontrols_properties_panel_tabwidget')
    self.playercontrols_properties_panel_tabwidget.setTabBar(QLeftTabBar(self.playercontrols_properties_panel_tabwidget))
    self.playercontrols_properties_panel_tabwidget.setTabPosition(QTabWidget.West)
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
    self.playercontrols_properties_panel_tabwidget_background.setObjectName('playercontrols_properties_panel_tabwidget_background')

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

    self.playercontrols_widget_frame = QFrame(parent=self.playercontrols_widget)
    self.playercontrols_widget_frame.setLayout(QVBoxLayout())
    self.playercontrols_widget_frame.layout().setContentsMargins(0, 0, 0, 0)

    self.playercontrols_widget_frame_top_hbox = QHBoxLayout()
    self.playercontrols_widget_frame_top_hbox.setSpacing(0)

    self.playercontrols_widget_frame_top_left = QFrame()
    self.playercontrols_widget_frame_top_left.setAttribute(Qt.WA_LayoutOnEntireRect)
    self.playercontrols_widget_frame_top_left.setObjectName('playercontrols_widget_frame_top_left')
    self.playercontrols_widget_frame_top_left.setFixedHeight(60)
    self.playercontrols_widget_frame_top_left.setLayout(QHBoxLayout())
    self.playercontrols_widget_frame_top_left.layout().setContentsMargins(0, 7, 7, 13)
    self.playercontrols_widget_frame_top_left.layout().setSpacing(6)
    self.playercontrols_widget_frame_top_left.layout().addStretch()

    self.gap_hbox = QFrame()
    self.gap_hbox.setLayout(QHBoxLayout())
    self.gap_hbox.setSizePolicy(QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum))
    self.gap_hbox.layout().setSizeConstraint(QLayout.SetMinimumSize)
    self.gap_hbox.layout().setContentsMargins(0, 0, 0, 0)
    self.gap_hbox.layout().setSpacing(0)

    self.gap_add_subtitle_button = QPushButton()
    self.gap_add_subtitle_button.setObjectName('gap_add_subtitle_button')
    self.gap_add_subtitle_button.setProperty('class', 'button_dark')
    self.gap_add_subtitle_button.setProperty('borderless_top', 'true')
    self.gap_add_subtitle_button.setProperty('borderless_right', 'true')
    self.gap_add_subtitle_button.setSizePolicy(QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum))
    self.gap_add_subtitle_button.clicked.connect(lambda: gap_add_subtitle_button_clicked(self))
    self.gap_hbox.layout().addWidget(self.gap_add_subtitle_button)

    self.gap_hbox.layout().addSpacing(-21)

    self.gap_subtitle_duration = QDoubleSpinBox()
    self.gap_subtitle_duration.setProperty('class', 'spin_playercontrols')
    self.gap_subtitle_duration.setMinimum(.1)
    self.gap_subtitle_duration.setMaximum(60.)
    self.gap_subtitle_duration.setFixedSize(QSize(40, 20))
    self.gap_hbox.layout().addWidget(self.gap_subtitle_duration)

    self.gap_hbox.layout().addSpacing(-21)

    self.gap_remove_subtitle_button = QPushButton()
    self.gap_remove_subtitle_button.setObjectName('gap_remove_subtitle_button')
    self.gap_remove_subtitle_button.setProperty('class', 'button_dark')
    self.gap_remove_subtitle_button.setProperty('borderless_left', 'true')
    self.gap_remove_subtitle_button.setProperty('borderless_top', 'true')
    self.gap_remove_subtitle_button.setSizePolicy(QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum))
    self.gap_remove_subtitle_button.clicked.connect(lambda: gap_remove_subtitle_button_clicked(self))
    self.gap_hbox.layout().addWidget(self.gap_remove_subtitle_button)

    self.gap_subtitle_duration.raise_()

    self.playercontrols_widget_frame_top_left.layout().addWidget(self.gap_hbox, 0)

    self.add_remove_subtitle_frame = QFrame()
    self.add_remove_subtitle_frame.setLayout(QHBoxLayout())
    self.add_remove_subtitle_frame.setSizePolicy(QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum))
    self.add_remove_subtitle_frame.layout().setSizeConstraint(QLayout.SetMinimumSize)
    self.add_remove_subtitle_frame.layout().setContentsMargins(0, 0, 0, 0)
    self.add_remove_subtitle_frame.layout().setSpacing(0)

    self.add_subtitle_button = QPushButton()
    self.add_subtitle_button.setObjectName('add_subtitle_button')
    self.add_subtitle_button.setProperty('class', 'button_dark')
    self.add_subtitle_button.setProperty('borderless_right', 'true')
    self.add_subtitle_button.setProperty('borderless_top', 'true')
    self.add_subtitle_button.setSizePolicy(QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum))
    self.add_subtitle_button.clicked.connect(lambda: add_subtitle_button_clicked(self))
    self.add_subtitle_button.setLayout(QHBoxLayout())
    self.add_subtitle_button.layout().setSizeConstraint(QLayout.SetMinimumSize)
    self.add_subtitle_button.layout().setContentsMargins(38, 0, 10, 5)
    self.add_subtitle_button.layout().setSpacing(0)

    self.add_subtitle_button_label = QLabel()
    self.add_subtitle_button_label.setObjectName('add_subtitle_button_label')
    # self.add_subtitle_button_label.setSizePolicy(QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum))
    self.add_subtitle_button.layout().addWidget(self.add_subtitle_button_label)

    self.add_subtitle_button.layout().addSpacing(6)

    self.add_subtitle_duration = QDoubleSpinBox()
    self.add_subtitle_duration.setObjectName('add_subtitle_duration')
    self.add_subtitle_duration.setProperty('class', 'spin_playercontrols')
    self.add_subtitle_duration.setMinimum(.1)
    self.add_subtitle_duration.setMaximum(60.)
    # self.add_subtitle_duration.setFixedSize(QSize(40, 20))
    # self.add_subtitle_duration.setSizePolicy(QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum))
    self.add_subtitle_duration.valueChanged.connect(lambda: add_subtitle_duration_changed(self))
    self.add_subtitle_button.layout().addWidget(self.add_subtitle_duration)  # , 0, Qt.AlignBottom)

    self.add_subtitle_button.layout().addSpacing(6)

    self.add_subtitle_starting_from_last = QPushButton()
    self.add_subtitle_starting_from_last.setObjectName('add_subtitle_starting_from_last')
    self.add_subtitle_starting_from_last.setProperty('class', 'button_dark')
    self.add_subtitle_starting_from_last.setProperty('borderless_right', 'true')
    self.add_subtitle_starting_from_last.setProperty('borderless_top', 'true')
    self.add_subtitle_starting_from_last.setCheckable(True)
    self.add_subtitle_starting_from_last.setSizePolicy(QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum))
    self.add_subtitle_starting_from_last.clicked.connect(lambda: add_subtitle_starting_from_last_clicked(self))
    self.add_subtitle_button.layout().addWidget(self.add_subtitle_starting_from_last)

    self.add_subtitle_and_play = QPushButton()
    self.add_subtitle_and_play.setObjectName('add_subtitle_and_play')
    self.add_subtitle_and_play.setProperty('class', 'button_dark')
    self.add_subtitle_and_play.setProperty('borderless_left', 'true')
    self.add_subtitle_and_play.setProperty('borderless_top', 'true')
    self.add_subtitle_and_play.setCheckable(True)
    self.add_subtitle_and_play.setSizePolicy(QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum))
    self.add_subtitle_and_play.clicked.connect(lambda: add_subtitle_and_play_clicked(self))
    self.add_subtitle_button.layout().addWidget(self.add_subtitle_and_play)

    self.add_remove_subtitle_frame.layout().addWidget(self.add_subtitle_button)

    self.remove_selected_subtitle_button = QPushButton()
    self.remove_selected_subtitle_button.setObjectName('remove_selected_subtitle_button')
    self.remove_selected_subtitle_button.setProperty('class', 'button_dark')
    self.remove_selected_subtitle_button.setProperty('borderless_left', 'true')
    self.remove_selected_subtitle_button.setProperty('borderless_top', 'true')
    self.remove_selected_subtitle_button.setSizePolicy(QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum))
    self.remove_selected_subtitle_button.clicked.connect(lambda: remove_selected_subtitle_button_clicked(self))
    self.add_remove_subtitle_frame.layout().addWidget(self.remove_selected_subtitle_button)

    self.playercontrols_widget_frame_top_left.layout().addWidget(self.add_remove_subtitle_frame, 0)

    self.change_playback_speed = QPushButton()
    self.change_playback_speed.setProperty('class', 'timeline_top_controls_button_left')
    self.change_playback_speed.setCheckable(True)
    self.change_playback_speed.setLayout(QHBoxLayout())
    self.change_playback_speed.setSizePolicy(QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum))
    self.change_playback_speed.layout().setSizeConstraint(QLayout.SetMinimumSize)
    self.change_playback_speed.layout().setContentsMargins(10, 10, 42, 10)
    self.change_playback_speed.layout().setSpacing(0)
    self.change_playback_speed.clicked.connect(lambda: change_playback_speed_clicked(self))

    self.change_playback_speed_decrease = QPushButton('-')
    self.change_playback_speed_decrease.setProperty('class', 'button')
    self.change_playback_speed_decrease.setProperty('borderless_right', 'true')
    self.change_playback_speed_decrease.setFixedWidth(20)
    self.change_playback_speed_decrease.setStyleSheet('QPushButton {padding:0;}')
    self.change_playback_speed_decrease.clicked.connect(lambda: change_playback_speed_decrease_clicked(self))
    self.change_playback_speed_decrease.setSizePolicy(QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum))
    self.change_playback_speed.layout().addWidget(self.change_playback_speed_decrease)

    self.change_playback_speed_slider = QSlider(Qt.Horizontal)
    self.change_playback_speed_slider.setMinimum(5)
    self.change_playback_speed_slider.setMaximum(300)
    self.change_playback_speed_slider.setPageStep(10)
    self.change_playback_speed_slider.setFixedWidth(60)
    self.change_playback_speed_slider.sliderReleased.connect(lambda: change_playback_speed_slider(self))
    self.change_playback_speed_slider.setSizePolicy(QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum))
    self.change_playback_speed.layout().addWidget(self.change_playback_speed_slider)

    self.change_playback_speed_increase = QPushButton('+', )
    self.change_playback_speed_increase.setProperty('class', 'button')
    self.change_playback_speed_increase.setProperty('borderless_left', 'true')
    self.change_playback_speed_increase.setFixedWidth(20)
    self.change_playback_speed_increase.setStyleSheet('QPushButton {padding:0;}')
    self.change_playback_speed_increase.clicked.connect(lambda: change_playback_speed_increase_clicked(self))
    self.change_playback_speed_increase.setSizePolicy(QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum))
    self.change_playback_speed.layout().addWidget(self.change_playback_speed_increase)

    self.change_playback_speed_label = QLabel()
    self.change_playback_speed_label.setSizePolicy(QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum))
    self.change_playback_speed_label.setObjectName('change_playback_speed_label')
    self.change_playback_speed_label.setFixedWidth(40)
    self.change_playback_speed.layout().addWidget(self.change_playback_speed_label)

    self.playercontrols_widget_frame_top_left.layout().addWidget(self.change_playback_speed, 0)

    self.playercontrols_widget_frame_top_hbox.layout().addWidget(self.playercontrols_widget_frame_top_left, 1)

    self.playercontrols_widget_frame_top_middle = QFrame()
    self.playercontrols_widget_frame_top_middle.setFixedHeight(60)
    self.playercontrols_widget_frame_top_middle.setObjectName('playercontrols_widget_frame_top_middle')
    self.playercontrols_widget_frame_top_middle.setSizePolicy(QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum))
    self.playercontrols_widget_frame_top_middle.setLayout(QHBoxLayout())
    self.playercontrols_widget_frame_top_middle.layout().setContentsMargins(0, 10, 0, 6)
    self.playercontrols_widget_frame_top_middle.layout().setSpacing(0)

    self.playercontrols_stop_button = QPushButton()
    self.playercontrols_stop_button.setObjectName('playercontrols_stop_button')
    self.playercontrols_stop_button.setProperty('class', 'playercontrols_button')
    self.playercontrols_stop_button.clicked.connect(lambda: playercontrols_stop_button_clicked(self))
    self.playercontrols_stop_button.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum))
    self.playercontrols_widget_frame_top_middle.layout().addWidget(self.playercontrols_stop_button)

    self.playercontrols_playpause_button = QPushButton()
    self.playercontrols_playpause_button.setObjectName('playercontrols_playpause_button')
    self.playercontrols_playpause_button.setProperty('class', 'playercontrols_button')
    self.playercontrols_playpause_button.setCheckable(True)
    self.playercontrols_playpause_button.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum))
    self.playercontrols_playpause_button.clicked.connect(lambda: playercontrols_playpause_button_clicked(self))
    self.playercontrols_playpause_button.setLayout(QHBoxLayout())
    self.playercontrols_playpause_button.layout().setSizeConstraint(QLayout.SetMinimumSize)
    self.playercontrols_playpause_button.layout().setContentsMargins(52, 6, 12, 6)
    self.playercontrols_playpause_button.layout().setSpacing(0)

    self.playercontrols_play_from_last_start_button = QPushButton()
    self.playercontrols_play_from_last_start_button.setObjectName('playercontrols_play_from_last_start_button')
    self.playercontrols_play_from_last_start_button.setProperty('class', 'subbutton_transparent')
    self.playercontrols_play_from_last_start_button.setProperty('borderless_right', 'true')
    self.playercontrols_play_from_last_start_button.setSizePolicy(QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum))
    self.playercontrols_play_from_last_start_button.clicked.connect(lambda: playercontrols_play_from_last_start_button_clicked(self))
    self.playercontrols_playpause_button.layout().addWidget(self.playercontrols_play_from_last_start_button, 0)

    self.playercontrols_play_from_next_start_button = QPushButton()
    self.playercontrols_play_from_next_start_button.setObjectName('playercontrols_play_from_next_start_button')
    self.playercontrols_play_from_next_start_button.setProperty('class', 'subbutton_transparent')
    self.playercontrols_play_from_next_start_button.setProperty('borderless_left', 'true')

    self.playercontrols_play_from_next_start_button.setSizePolicy(QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum))
    self.playercontrols_play_from_next_start_button.clicked.connect(lambda: playercontrols_play_from_next_start_button_clicked(self))
    self.playercontrols_playpause_button.layout().addWidget(self.playercontrols_play_from_next_start_button, 0)

    self.playercontrols_widget_frame_top_middle.layout().addWidget(self.playercontrols_playpause_button)

    self.playercontrols_widget_frame_top_hbox.layout().addWidget(self.playercontrols_widget_frame_top_middle)

    self.playercontrols_widget_frame_top_right = QFrame()
    self.playercontrols_widget_frame_top_right.setAttribute(Qt.WA_LayoutOnEntireRect)
    self.playercontrols_widget_frame_top_right.setObjectName('playercontrols_widget_frame_top_right')
    self.playercontrols_widget_frame_top_right.setFixedHeight(60)
    self.playercontrols_widget_frame_top_right.setLayout(QHBoxLayout())
    self.playercontrols_widget_frame_top_right.layout().setContentsMargins(7, 7, 0, 13)
    self.playercontrols_widget_frame_top_right.layout().setSpacing(6)

    self.repeat_playback = QPushButton()
    self.repeat_playback.setProperty('class', 'timeline_top_controls_button_right')
    self.repeat_playback.setCheckable(True)
    self.repeat_playback.setLayout(QHBoxLayout())
    self.repeat_playback.setSizePolicy(QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum))
    self.repeat_playback.layout().setSizeConstraint(QLayout.SetMinimumSize)
    self.repeat_playback.layout().setContentsMargins(46, 10, 12, 10)
    self.repeat_playback.layout().setSpacing(2)
    self.repeat_playback.clicked.connect(lambda: repeat_playback_clicked(self))

    self.repeat_playback_duration = QDoubleSpinBox()
    self.repeat_playback_duration.setProperty('class', 'spin_playercontrols')
    self.repeat_playback_duration.setMinimum(.1)
    self.repeat_playback_duration.setMaximum(60.)
    self.repeat_playback_duration.valueChanged.connect(lambda: repeat_playback_duration_changed(self))
    self.repeat_playback_duration.setSizePolicy(QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum))
    self.repeat_playback.layout().addWidget(self.repeat_playback_duration)

    self.repeat_playback_x_label = QLabel('x', )
    self.repeat_playback_x_label.setObjectName('repeat_playback_x_label')
    self.repeat_playback.layout().addWidget(self.repeat_playback_x_label)

    self.repeat_playback_times = QSpinBox()
    self.repeat_playback_times.setProperty('class', 'spin_playercontrols')
    self.repeat_playback_times.setMinimum(1)
    self.repeat_playback_times.setMaximum(20)
    self.repeat_playback_times.valueChanged.connect(lambda: repeat_playback_times_changed(self))
    self.repeat_playback_times.setSizePolicy(QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum))
    self.repeat_playback.layout().addWidget(self.repeat_playback_times)

    self.playercontrols_widget_frame_top_right.layout().addWidget(self.repeat_playback)

    self.merge_slice_frame = QFrame()
    self.merge_slice_frame.setLayout(QHBoxLayout())
    self.merge_slice_frame.setSizePolicy(QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum))
    self.merge_slice_frame.layout().setSizeConstraint(QLayout.SetMinimumSize)
    self.merge_slice_frame.layout().setContentsMargins(0, 0, 0, 0)
    self.merge_slice_frame.layout().setSpacing(0)

    self.merge_back_selected_subtitle_button = QPushButton()
    self.merge_back_selected_subtitle_button.setObjectName('merge_back_selected_subtitle_button')
    self.merge_back_selected_subtitle_button.setProperty('class', 'button_dark')
    self.merge_back_selected_subtitle_button.setProperty('borderless_right', 'true')
    self.merge_back_selected_subtitle_button.setProperty('borderless_top', 'true')
    self.merge_back_selected_subtitle_button.setSizePolicy(QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum))
    self.merge_back_selected_subtitle_button.clicked.connect(lambda: merge_back_selected_subtitle_button_clicked(self))
    self.merge_slice_frame.layout().addWidget(self.merge_back_selected_subtitle_button)

    self.slice_selected_subtitle_button = QPushButton()
    self.slice_selected_subtitle_button.setObjectName('slice_selected_subtitle_button')
    self.slice_selected_subtitle_button.setProperty('class', 'button_dark')
    self.slice_selected_subtitle_button.setProperty('borderless_left', 'true')
    self.slice_selected_subtitle_button.setProperty('borderless_right', 'true')
    self.slice_selected_subtitle_button.setProperty('borderless_top', 'true')
    self.slice_selected_subtitle_button.setSizePolicy(QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum))
    self.slice_selected_subtitle_button.clicked.connect(lambda: slice_selected_subtitle_button_clicked(self))
    self.merge_slice_frame.layout().addWidget(self.slice_selected_subtitle_button)

    self.merge_next_selected_subtitle_button = QPushButton()
    self.merge_next_selected_subtitle_button.setObjectName('merge_next_selected_subtitle_button')
    self.merge_next_selected_subtitle_button.setProperty('class', 'button_dark')
    self.merge_next_selected_subtitle_button.setProperty('borderless_left', 'true')
    self.merge_next_selected_subtitle_button.setProperty('borderless_top', 'true')
    self.merge_next_selected_subtitle_button.setSizePolicy(QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum))
    self.merge_next_selected_subtitle_button.clicked.connect(lambda: merge_next_selected_subtitle_button_clicked(self))
    self.merge_slice_frame.layout().addWidget(self.merge_next_selected_subtitle_button)

    self.playercontrols_widget_frame_top_right.layout().addWidget(self.merge_slice_frame)

    self.start_end_moving_frame = QFrame()
    self.start_end_moving_frame.setLayout(QHBoxLayout())
    self.start_end_moving_frame.setSizePolicy(QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum))
    self.start_end_moving_frame.layout().setSizeConstraint(QLayout.SetMinimumSize)
    self.start_end_moving_frame.layout().setContentsMargins(0, 0, 0, 0)
    self.start_end_moving_frame.layout().setSpacing(0)

    self.next_start_to_current_position_button = QPushButton()
    self.next_start_to_current_position_button.setObjectName('next_start_to_current_position_button')
    self.next_start_to_current_position_button.setProperty('class', 'button_dark')
    self.next_start_to_current_position_button.setProperty('borderless_top', 'true')
    self.next_start_to_current_position_button.setProperty('borderless_right', 'true')
    self.next_start_to_current_position_button.setSizePolicy(QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum))
    self.next_start_to_current_position_button.clicked.connect(lambda: next_start_to_current_position_button_clicked(self))
    self.start_end_moving_frame.layout().addWidget(self.next_start_to_current_position_button)

    self.last_start_to_current_position_button = QPushButton()
    self.last_start_to_current_position_button.setObjectName('last_start_to_current_position_button')
    self.last_start_to_current_position_button.setProperty('class', 'button_dark')
    self.last_start_to_current_position_button.setProperty('borderless_top', 'true')
    self.last_start_to_current_position_button.setProperty('borderless_right', 'true')
    self.last_start_to_current_position_button.setProperty('borderless_left', 'true')
    self.last_start_to_current_position_button.setSizePolicy(QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum))
    self.last_start_to_current_position_button.clicked.connect(lambda: last_start_to_current_position_button_clicked(self))
    self.start_end_moving_frame.layout().addWidget(self.last_start_to_current_position_button)

    self.last_start_last_end_to_current_position_button = QPushButton()
    self.last_start_last_end_to_current_position_button.setObjectName('last_start_last_end_to_current_position_button')
    self.last_start_last_end_to_current_position_button.setProperty('class', 'button_dark')
    self.last_start_last_end_to_current_position_button.setProperty('borderless_top', 'true')
    self.last_start_last_end_to_current_position_button.setProperty('borderless_right', 'true')
    self.last_start_last_end_to_current_position_button.setProperty('borderless_left', 'true')
    self.last_start_last_end_to_current_position_button.setSizePolicy(QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum))
    self.last_start_last_end_to_current_position_button.clicked.connect(lambda: last_start_last_end_to_current_position_button_clicked(self))
    self.start_end_moving_frame.layout().addWidget(self.last_start_last_end_to_current_position_button)

    self.next_end_to_current_position_button = QPushButton()
    self.next_end_to_current_position_button.setObjectName('next_end_to_current_position_button')
    self.next_end_to_current_position_button.setProperty('class', 'button_dark')
    self.next_end_to_current_position_button.setProperty('borderless_top', 'true')
    self.next_end_to_current_position_button.setProperty('borderless_right', 'true')
    self.next_end_to_current_position_button.setProperty('borderless_left', 'true')
    self.next_end_to_current_position_button.setSizePolicy(QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum))
    self.next_end_to_current_position_button.clicked.connect(lambda: next_end_to_current_position_button_clicked(self))
    self.start_end_moving_frame.layout().addWidget(self.next_end_to_current_position_button)

    self.last_end_to_current_position_button = QPushButton()
    self.last_end_to_current_position_button.setObjectName('last_end_to_current_position_button')
    self.last_end_to_current_position_button.setProperty('class', 'button_dark')
    self.last_end_to_current_position_button.setProperty('borderless_top', 'true')
    self.last_end_to_current_position_button.setProperty('borderless_right', 'true')
    self.last_end_to_current_position_button.setProperty('borderless_left', 'true')
    self.last_end_to_current_position_button.setSizePolicy(QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum))
    self.last_end_to_current_position_button.clicked.connect(lambda: last_end_to_current_position_button_clicked(self))
    self.start_end_moving_frame.layout().addWidget(self.last_end_to_current_position_button)

    self.next_start_next_end_to_current_position_button = QPushButton()
    self.next_start_next_end_to_current_position_button.setObjectName('next_start_next_end_to_current_position_button')
    self.next_start_next_end_to_current_position_button.setProperty('class', 'button_dark')
    self.next_start_next_end_to_current_position_button.setProperty('borderless_top', 'true')
    self.next_start_next_end_to_current_position_button.setProperty('borderless_left', 'true')
    self.next_start_next_end_to_current_position_button.setSizePolicy(QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum))
    self.next_start_next_end_to_current_position_button.clicked.connect(lambda: next_start_next_end_to_current_position_button_clicked(self))
    self.start_end_moving_frame.layout().addWidget(self.next_start_next_end_to_current_position_button)

    self.playercontrols_widget_frame_top_right.layout().addWidget(self.start_end_moving_frame)

    self.playercontrols_widget_frame_top_right.layout().addStretch()

    self.playercontrols_widget_frame_top_hbox.layout().addWidget(self.playercontrols_widget_frame_top_right, 1)

    self.playercontrols_widget_frame.layout().addLayout(self.playercontrols_widget_frame_top_hbox)

    self.playercontrols_widget_frame_bottom_hbox = QHBoxLayout()
    self.playercontrols_widget_frame_bottom_hbox.setSpacing(0)

    self.playercontrols_widget_frame_bottom_left = QFrame()
    self.playercontrols_widget_frame_bottom_left.setAttribute(Qt.WA_LayoutOnEntireRect)
    self.playercontrols_widget_frame_bottom_left.setObjectName('playercontrols_widget_frame_bottom_left')
    self.playercontrols_widget_frame_bottom_left.setFixedHeight(26)
    self.playercontrols_widget_frame_bottom_left.setLayout(QHBoxLayout())
    self.playercontrols_widget_frame_bottom_left.layout().setContentsMargins(0, 0, 4, 2)
    self.playercontrols_widget_frame_bottom_left.layout().setSpacing(0)
    self.playercontrols_widget_frame_bottom_left.layout().addStretch()

    self.timelinescrolling_none_button = QPushButton()
    self.timelinescrolling_none_button.setObjectName('timelinescrolling_none_button')
    self.timelinescrolling_none_button.setProperty('class', 'subbutton')
    self.timelinescrolling_none_button.setProperty('borderless_bottom', 'true')
    self.timelinescrolling_none_button.setProperty('borderless_right', 'true')
    self.timelinescrolling_none_button.setCheckable(True)
    self.timelinescrolling_none_button.clicked.connect(lambda: timelinescrolling_type_changed(self, 'none'))
    self.timelinescrolling_none_button.setSizePolicy(QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum))
    self.playercontrols_widget_frame_bottom_left.layout().addWidget(self.timelinescrolling_none_button)

    self.timelinescrolling_page_button = QPushButton()
    self.timelinescrolling_page_button.setObjectName('timelinescrolling_page_button')
    self.timelinescrolling_page_button.setProperty('class', 'subbutton')
    self.timelinescrolling_page_button.setProperty('borderless_bottom', 'true')
    self.timelinescrolling_page_button.setProperty('borderless_right', 'true')
    self.timelinescrolling_page_button.setCheckable(True)
    self.timelinescrolling_page_button.setSizePolicy(QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum))
    self.timelinescrolling_page_button.clicked.connect(lambda: timelinescrolling_type_changed(self, 'page'))
    self.playercontrols_widget_frame_bottom_left.layout().addWidget(self.timelinescrolling_page_button)

    self.timelinescrolling_follow_button = QPushButton()
    self.timelinescrolling_follow_button.setObjectName('timelinescrolling_follow_button')
    self.timelinescrolling_follow_button.setProperty('class', 'subbutton')
    self.timelinescrolling_follow_button.setProperty('borderless_bottom', 'true')
    self.timelinescrolling_follow_button.setCheckable(True)
    self.timelinescrolling_follow_button.setSizePolicy(QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum))
    self.timelinescrolling_follow_button.clicked.connect(lambda: timelinescrolling_type_changed(self, 'follow'))
    self.playercontrols_widget_frame_bottom_left.layout().addWidget(self.timelinescrolling_follow_button)

    self.playercontrols_widget_frame_bottom_left.layout().addSpacing(4)

    self.snap_button = QPushButton()
    self.snap_button.setProperty('class', 'subbutton')
    self.snap_button.setProperty('borderless_right', 'true')
    self.snap_button.setProperty('borderless_bottom', 'true')
    self.snap_button.setCheckable(True)
    self.snap_button.setSizePolicy(QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum))
    self.snap_button.clicked.connect(lambda: snap_button_clicked(self))
    self.snap_button.setLayout(QHBoxLayout())
    self.snap_button.layout().setSizeConstraint(QLayout.SetMinimumSize)
    self.snap_button.layout().setContentsMargins(10, 4, 5, 4)
    self.snap_button.layout().setSpacing(4)
    self.playercontrols_widget_frame_bottom_left.layout().addWidget(self.snap_button)

    self.snap_button_label = QLabel()
    self.snap_button_label.setObjectName('snap_button_label')
    self.snap_button.layout().addWidget(self.snap_button_label)

    self.snap_value = QDoubleSpinBox()
    self.snap_value.setProperty('class', 'spin_playercontrols')
    self.snap_value.setSizePolicy(QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum))
    self.snap_value.valueChanged.connect(lambda: snap_value_changed(self))
    self.snap_button.layout().addWidget(self.snap_value)

    self.snap_limits_button = QPushButton()
    self.snap_limits_button.setObjectName('snap_limits_button')
    self.snap_limits_button.setProperty('class', 'subbutton')
    self.snap_limits_button.setProperty('borderless_right', 'true')
    self.snap_limits_button.setProperty('borderless_bottom', 'true')
    self.snap_limits_button.setCheckable(True)
    self.snap_limits_button.setSizePolicy(QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum))
    self.snap_limits_button.clicked.connect(lambda: snap_limits_button_clicked(self))
    self.playercontrols_widget_frame_bottom_left.layout().addWidget(self.snap_limits_button)

    self.snap_grid_button = QPushButton()
    self.snap_grid_button.setObjectName('snap_grid_button')
    self.snap_grid_button.setProperty('class', 'subbutton')
    self.snap_grid_button.setProperty('borderless_right', 'true')
    self.snap_grid_button.setProperty('borderless_bottom', 'true')
    self.snap_grid_button.setCheckable(True)
    self.snap_grid_button.setSizePolicy(QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum))
    self.snap_grid_button.clicked.connect(lambda: snap_grid_button_clicked(self))
    self.playercontrols_widget_frame_bottom_left.layout().addWidget(self.snap_grid_button)

    self.snap_move_button = QPushButton()
    self.snap_move_button.setObjectName('snap_move_button')
    self.snap_move_button.setProperty('class', 'subbutton')
    self.snap_move_button.setProperty('borderless_right', 'true')
    self.snap_move_button.setProperty('borderless_bottom', 'true')
    self.snap_move_button.setCheckable(True)
    self.snap_move_button.setSizePolicy(QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum))
    self.snap_move_button.clicked.connect(lambda: snap_move_button_clicked(self))
    self.playercontrols_widget_frame_bottom_left.layout().addWidget(self.snap_move_button)

    self.snap_move_nereast_button = QPushButton()
    self.snap_move_nereast_button.setObjectName('snap_move_nereast_button')
    self.snap_move_nereast_button.setProperty('class', 'subbutton')
    self.snap_move_nereast_button.setProperty('borderless_bottom', 'true')
    self.snap_move_nereast_button.setCheckable(True)
    self.snap_move_nereast_button.setSizePolicy(QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum))
    self.snap_move_nereast_button.clicked.connect(lambda: snap_move_nereast_button_clicked(self))
    self.playercontrols_widget_frame_bottom_left.layout().addWidget(self.snap_move_nereast_button)

    self.playercontrols_widget_frame_bottom_left.layout().addSpacing(4)

    self.move_start_back_subtitle = QPushButton()
    self.move_start_back_subtitle.setObjectName('move_start_back_subtitle')
    self.move_start_back_subtitle.setProperty('class', 'subbutton2_dark')
    self.move_start_back_subtitle.setProperty('borderless_bottom', 'true')
    self.move_start_back_subtitle.setProperty('borderless_right', 'true')
    self.move_start_back_subtitle.setSizePolicy(QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum))
    self.move_start_back_subtitle.clicked.connect(lambda: move_start_back_subtitle_clicked(self))
    self.playercontrols_widget_frame_bottom_left.layout().addWidget(self.move_start_back_subtitle)

    self.move_start_forward_subtitle = QPushButton()
    self.move_start_forward_subtitle.setObjectName('move_start_forward_subtitle')
    self.move_start_forward_subtitle.setProperty('class', 'subbutton2_dark')
    self.move_start_forward_subtitle.setProperty('borderless_bottom', 'true')
    self.move_start_forward_subtitle.setProperty('borderless_left', 'true')
    self.move_start_forward_subtitle.setSizePolicy(QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum))
    self.move_start_forward_subtitle.clicked.connect(lambda: move_start_forward_subtitle_clicked(self))
    self.playercontrols_widget_frame_bottom_left.layout().addWidget(self.move_start_forward_subtitle)

    self.playercontrols_widget_frame_bottom_left.layout().addSpacing(2)

    self.move_backward_subtitle = QPushButton()
    self.move_backward_subtitle.setObjectName('move_backward_subtitle')
    self.move_backward_subtitle.setProperty('class', 'subbutton2_dark')
    self.move_backward_subtitle.setProperty('borderless_bottom', 'true')
    self.move_backward_subtitle.setSizePolicy(QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum))
    self.move_backward_subtitle.clicked.connect(lambda: move_backward_subtitle_clicked(self))
    self.playercontrols_widget_frame_bottom_left.layout().addWidget(self.move_backward_subtitle)

    self.playercontrols_widget_frame_bottom_left.layout().addSpacing(2)

    self.timeline_cursor_back_frame = QPushButton()
    self.timeline_cursor_back_frame.setObjectName('timeline_cursor_back_frame')
    self.timeline_cursor_back_frame.setProperty('class', 'subbutton_left_dark')
    self.timeline_cursor_back_frame.setProperty('borderless_bottom', 'true')
    self.timeline_cursor_back_frame.setSizePolicy(QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum))
    self.timeline_cursor_back_frame.clicked.connect(lambda: timeline_cursor_back_frame_clicked(self))
    self.playercontrols_widget_frame_bottom_left.layout().addWidget(self.timeline_cursor_back_frame)

    self.playercontrols_widget_frame_bottom_hbox.layout().addWidget(self.playercontrols_widget_frame_bottom_left, 1)

    self.playercontrols_widget_frame_bottom_middle = QFrame()
    self.playercontrols_widget_frame_bottom_middle.setFixedHeight(26)
    self.playercontrols_widget_frame_bottom_middle.setObjectName('playercontrols_widget_frame_bottom_middle')
    self.playercontrols_widget_frame_bottom_middle.setSizePolicy(QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum))
    self.playercontrols_widget_frame_bottom_middle.setLayout(QHBoxLayout())
    self.playercontrols_widget_frame_bottom_middle.layout().setContentsMargins(0, 0, 0, 0)
    self.playercontrols_widget_frame_bottom_middle.layout().setSpacing(0)

    self.playercontrols_timecode_label = QLabel()
    self.playercontrols_timecode_label.setObjectName('playercontrols_timecode_label')
    self.playercontrols_timecode_label.setFixedWidth(100)
    self.playercontrols_timecode_label.setAlignment(Qt.AlignCenter)
    # self.playercontrols_timecode_label.setSizePolicy(QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum))
    self.playercontrols_widget_frame_bottom_middle.layout().addWidget(self.playercontrols_timecode_label)

    self.playercontrols_widget_frame_bottom_hbox.layout().addWidget(self.playercontrols_widget_frame_bottom_middle, 0)

    self.playercontrols_widget_frame_bottom_right_absolute = QFrame()
    self.playercontrols_widget_frame_bottom_right_absolute.setAttribute(Qt.WA_LayoutOnEntireRect)
    # self.playercontrols_widget_frame_bottom_right_absolute.setObjectName('playercontrols_widget_frame_bottom_right')
    self.playercontrols_widget_frame_bottom_right_absolute.setFixedHeight(26)
    self.playercontrols_widget_frame_bottom_right_absolute.setLayout(QHBoxLayout())
    self.playercontrols_widget_frame_bottom_right_absolute.layout().setContentsMargins(0, 0, 0, 0)
    self.playercontrols_widget_frame_bottom_right_absolute.layout().setSpacing(0)

    self.playercontrols_widget_frame_bottom_right = QFrame()
    # self.playercontrols_widget_frame_bottom_right.setAttribute(Qt.WA_LayoutOnEntireRect)
    self.playercontrols_widget_frame_bottom_right.setObjectName('playercontrols_widget_frame_bottom_right')
    # self.playercontrols_widget_frame_bottom_right.setFixedHeight(26)
    self.playercontrols_widget_frame_bottom_right.setLayout(QHBoxLayout())
    self.playercontrols_widget_frame_bottom_right.layout().setContentsMargins(0, 0, 0, 2)
    self.playercontrols_widget_frame_bottom_right.layout().setSpacing(0)

    self.playercontrols_widget_frame_bottom_right.layout().addSpacing(-8)

    self.timeline_cursor_next_frame = QPushButton()
    self.timeline_cursor_next_frame.setObjectName('timeline_cursor_next_frame')
    self.timeline_cursor_next_frame.setProperty('class', 'subbutton_right_dark')
    self.timeline_cursor_next_frame.setProperty('borderless_bottom', 'true')
    self.timeline_cursor_next_frame.setSizePolicy(QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum))
    self.timeline_cursor_next_frame.clicked.connect(lambda: timeline_cursor_next_frame_clicked(self))
    self.playercontrols_widget_frame_bottom_right.layout().addWidget(self.timeline_cursor_next_frame)

    self.playercontrols_widget_frame_bottom_right.layout().addSpacing(2)

    self.move_forward_subtitle = QPushButton()
    self.move_forward_subtitle.setObjectName('move_forward_subtitle')
    self.move_forward_subtitle.setProperty('class', 'subbutton2_dark')
    self.move_forward_subtitle.setProperty('borderless_bottom', 'true')
    self.move_forward_subtitle.setSizePolicy(QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum))
    self.move_forward_subtitle.clicked.connect(lambda: move_forward_subtitle_clicked(self))
    self.playercontrols_widget_frame_bottom_right.layout().addWidget(self.move_forward_subtitle)

    self.playercontrols_widget_frame_bottom_right.layout().addSpacing(2)

    self.move_end_back_subtitle = QPushButton()
    self.move_end_back_subtitle.setObjectName('move_end_back_subtitle')
    self.move_end_back_subtitle.setProperty('class', 'subbutton2_dark')
    self.move_end_back_subtitle.setProperty('borderless_bottom', 'true')
    self.move_end_back_subtitle.setProperty('borderless_right', 'true')
    self.move_end_back_subtitle.setSizePolicy(QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum))
    self.move_end_back_subtitle.clicked.connect(lambda: move_end_back_subtitle_clicked(self))
    self.playercontrols_widget_frame_bottom_right.layout().addWidget(self.move_end_back_subtitle)

    self.move_end_forward_subtitle = QPushButton()
    self.move_end_forward_subtitle.setObjectName('move_end_forward_subtitle')
    self.move_end_forward_subtitle.setProperty('class', 'subbutton2_dark')
    self.move_end_forward_subtitle.setProperty('borderless_bottom', 'true')
    self.move_end_forward_subtitle.setProperty('borderless_left', 'true')
    self.move_end_forward_subtitle.setSizePolicy(QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum))
    self.move_end_forward_subtitle.clicked.connect(lambda: move_end_forward_subtitle_clicked(self))
    self.playercontrols_widget_frame_bottom_right.layout().addWidget(self.move_end_forward_subtitle)

    self.playercontrols_widget_frame_bottom_right.layout().addSpacing(4)

    self.grid_button = QPushButton()
    self.grid_button.setProperty('class', 'subbutton')
    self.grid_button.setProperty('borderless_bottom', 'true')
    self.grid_button.setProperty('borderless_right', 'true')
    self.grid_button.setCheckable(True)
    self.grid_button.clicked.connect(lambda: grid_button_clicked(self))
    self.grid_button.setSizePolicy(QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum))
    self.playercontrols_widget_frame_bottom_right.layout().addWidget(self.grid_button)

    self.grid_frames_button = QPushButton()
    self.grid_frames_button.setObjectName('grid_frames_button')
    self.grid_frames_button.setProperty('class', 'subbutton')
    self.grid_frames_button.setProperty('borderless_bottom', 'true')
    self.grid_frames_button.setProperty('borderless_right', 'true')
    self.grid_frames_button.setCheckable(True)
    self.grid_frames_button.clicked.connect(lambda: grid_type_changed(self, 'frames'))
    self.grid_frames_button.setSizePolicy(QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum))
    self.playercontrols_widget_frame_bottom_right.layout().addWidget(self.grid_frames_button)

    self.grid_seconds_button = QPushButton()
    self.grid_seconds_button.setObjectName('grid_seconds_button')
    self.grid_seconds_button.setProperty('class', 'subbutton')
    self.grid_seconds_button.setProperty('borderless_bottom', 'true')
    self.grid_seconds_button.setProperty('borderless_right', 'true')
    self.grid_seconds_button.setCheckable(True)
    self.grid_seconds_button.clicked.connect(lambda: grid_type_changed(self, 'seconds'))
    self.grid_seconds_button.setSizePolicy(QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum))
    self.playercontrols_widget_frame_bottom_right.layout().addWidget(self.grid_seconds_button)

    self.grid_scenes_button = QPushButton()
    self.grid_scenes_button.setObjectName('grid_scenes_button')
    self.grid_scenes_button.setProperty('class', 'subbutton')
    self.grid_scenes_button.setProperty('borderless_bottom', 'true')
    # self.grid_scenes_button.setProperty('borderless_right', 'true')
    self.grid_scenes_button.setCheckable(True)
    self.grid_scenes_button.clicked.connect(lambda: grid_type_changed(self, 'scenes'))
    self.grid_scenes_button.setSizePolicy(QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum))
    self.playercontrols_widget_frame_bottom_right.layout().addWidget(self.grid_scenes_button)

    self.playercontrols_widget_frame_bottom_right.layout().addSpacing(4)

    self.step_button = QPushButton()
    self.step_button.setProperty('class', 'subbutton')
    self.step_button.setProperty('borderless_bottom', 'true')
    self.step_button.setCheckable(True)
    self.step_button.clicked.connect(lambda: update_step_buttons(self))
    self.step_button.setLayout(QHBoxLayout())
    self.step_button.setSizePolicy(QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum))
    self.step_button.layout().setSizeConstraint(QLayout.SetMinimumSize)
    self.step_button.layout().setContentsMargins(10, 4, 5, 4)
    self.step_button.layout().setSpacing(2)

    self.step_button_label = QLabel()
    self.step_button_label.setObjectName('step_button_label')
    # self.step_button_label.setSizePolicy(QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum))
    self.step_button.layout().addWidget(self.step_button_label)

    self.step_value_f = QDoubleSpinBox()
    self.step_value_f.setObjectName('step_value_f')
    self.step_value_f.setProperty('class', 'spin_playercontrols')
    self.step_value_f.setMinimum(.001)
    self.step_value_f.setMaximum(999.999)
    self.step_value_f.valueChanged.connect(lambda: step_value_changed(self))
    # self.step_value_f.setSizePolicy(QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum))
    self.step_button.layout().addWidget(self.step_value_f)

    self.step_value_i = QSpinBox()
    self.step_value_i.setObjectName('step_value_i')
    self.step_value_i.setProperty('class', 'spin_playercontrols')
    self.step_value_i.setMinimum(1)
    self.step_value_i.setMaximum(999)
    self.step_value_i.valueChanged.connect(lambda: step_value_changed(self))
    # self.step_value_i.setSizePolicy(QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum))
    self.step_button.layout().addWidget(self.step_value_i)

    self.step_unit = QComboBox()
    self.step_unit.setObjectName('step_unit')
    self.step_unit.setProperty('class', 'combobox_playercontrols')
    self.step_unit.insertItems(0, STEPS_LIST)
    self.step_unit.activated.connect(lambda: step_value_changed(self))
    # self.step_unit.setFixedWidth(50)
    # self.step_unit.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum))
    self.step_button.layout().addWidget(self.step_unit)

    self.playercontrols_widget_frame_bottom_right.layout().addWidget(self.step_button)

    self.playercontrols_widget_frame_bottom_right.layout().addSpacing(4)

    self.zoomin_button = QPushButton(parent=self.playercontrols_widget)
    self.zoomin_button.setObjectName('zoomin_button')
    self.zoomin_button.setProperty('borderless_bottom', 'true')
    self.zoomin_button.setProperty('borderless_right', 'true')
    self.zoomin_button.setProperty('class', 'subbutton2_dark')
    self.zoomin_button.setSizePolicy(QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum))
    self.zoomin_button.clicked.connect(lambda: zoomin_button_clicked(self))
    self.playercontrols_widget_frame_bottom_right.layout().addWidget(self.zoomin_button)

    self.zoomout_button = QPushButton(parent=self.playercontrols_widget)
    self.zoomout_button.setObjectName('zoomout_button')
    self.zoomout_button.setProperty('borderless_bottom', 'true')
    self.zoomout_button.setProperty('borderless_left', 'true')
    self.zoomout_button.setProperty('class', 'subbutton2_dark')
    self.zoomout_button.setSizePolicy(QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum))
    self.zoomout_button.clicked.connect(lambda: zoomout_button_clicked(self))
    self.playercontrols_widget_frame_bottom_right.layout().addWidget(self.zoomout_button)

    self.playercontrols_widget_frame_bottom_right.layout().addStretch()

    self.playercontrols_widget_frame_bottom_right_absolute.layout().addWidget(self.playercontrols_widget_frame_bottom_right)

    self.playercontrols_widget_frame_bottom_right_corner = QFrame()
    self.playercontrols_widget_frame_bottom_right_corner.setObjectName('playercontrols_widget_frame_bottom_right_corner')
    self.playercontrols_widget_frame_bottom_right_corner.setSizePolicy(QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum))
    self.playercontrols_widget_frame_bottom_right_corner.setFixedWidth(35)
    self.playercontrols_widget_frame_bottom_right_corner.setLayout(QHBoxLayout())
    self.playercontrols_widget_frame_bottom_right_corner.layout().setContentsMargins(0, 0, 0, 0)
    self.playercontrols_widget_frame_bottom_right_corner.layout().setSpacing(0)

    self.playercontrols_properties_panel_toggle = QPushButton()
    self.playercontrols_properties_panel_toggle.setObjectName('playercontrols_properties_panel_toggle')
    self.playercontrols_properties_panel_toggle.setCheckable(True)
    self.playercontrols_widget_frame_bottom_right_corner.layout().addWidget(self.playercontrols_properties_panel_toggle)
    self.playercontrols_properties_panel_toggle.clicked.connect(lambda: playercontrols_properties_panel_toggle_pressed(self))
    self.playercontrols_properties_panel_toggle_animation = QPropertyAnimation(self.playercontrols_properties_panel_toggle, b'geometry')
    self.playercontrols_properties_panel_toggle_animation.setEasingCurve(QEasingCurve.OutCirc)

    self.playercontrols_widget_frame_bottom_right_absolute.layout().addWidget(self.playercontrols_widget_frame_bottom_right_corner, 0)

    self.playercontrols_widget_frame_bottom_hbox.layout().addWidget(self.playercontrols_widget_frame_bottom_right_absolute, 1)

    self.playercontrols_widget_frame.layout().addLayout(self.playercontrols_widget_frame_bottom_hbox)


def resized(self):
    """Function to call when resizing widgets"""
    if (self.subtitles_list or self.video_metadata) and not self.subtitles_panel_toggle_button.isChecked():
        self.playercontrols_widget.setGeometry(0, self.height() - 200, self.width(), 200)
    else:
        self.playercontrols_widget.setGeometry(0, self.height(), self.width(), 200)

    self.playercontrols_widget_frame.setGeometry(0, 10, self.playercontrols_widget.width(), 86)

    show_or_hide_playercontrols_properties_panel(self)
    self.playercontrols_properties_panel_tabwidget.setGeometry(10, 34, self.playercontrols_properties_panel.width() - 40, self.playercontrols_properties_panel.height() - 60)
    self.playercontrols_properties_panel_tabwidget_subtitles_subtitle_title_normal.setGeometry(10, 10, 100, 15)
    self.playercontrols_properties_panel_tabwidget_subtitles_subtitle_border_color_title_normal.setGeometry(10, 25, 30, 15)
    self.playercontrols_properties_panel_tabwidget_subtitles_subtitle_border_color_button.setGeometry(10, 40, 30, 30)
    self.playercontrols_properties_panel_tabwidget_subtitles_subtitle_fill_color_title_normal.setGeometry(45, 25, 30, 15)
    self.playercontrols_properties_panel_tabwidget_subtitles_subtitle_fill_color_button.setGeometry(45, 40, 30, 30)
    self.playercontrols_properties_panel_tabwidget_subtitles_subtitle_text_color_title_normal.setGeometry(80, 25, 30, 15)
    self.playercontrols_properties_panel_tabwidget_subtitles_subtitle_text_color_button.setGeometry(80, 40, 30, 30)
    self.playercontrols_properties_panel_tabwidget_subtitles_subtitle_title_selected.setGeometry(120, 10, 100, 15)
    self.playercontrols_properties_panel_tabwidget_subtitles_subtitle_border_color_title_selected.setGeometry(120, 25, 30, 15)
    self.playercontrols_properties_panel_tabwidget_subtitles_selected_subtitle_border_color_button.setGeometry(120, 40, 30, 30)
    self.playercontrols_properties_panel_tabwidget_subtitles_subtitle_fill_color_title_selected.setGeometry(155, 25, 30, 15)
    self.playercontrols_properties_panel_tabwidget_subtitles_selected_subtitle_fill_color_button.setGeometry(155, 40, 30, 30)
    self.playercontrols_properties_panel_tabwidget_subtitles_subtitle_text_color_title_selected.setGeometry(190, 25, 30, 15)
    self.playercontrols_properties_panel_tabwidget_subtitles_selected_subtitle_text_color_button.setGeometry(190, 40, 30, 30)
    self.playercontrols_properties_panel_tabwidget_subtitles_subtitle_title_arrows.setGeometry(225, 10, 70, 15)
    self.playercontrols_properties_panel_tabwidget_subtitles_subtitle_title_normal_arrows.setGeometry(225, 25, 30, 15)
    self.playercontrols_properties_panel_tabwidget_subtitles_subtitle_arrow_normal_button.setGeometry(225, 40, 30, 30)
    self.playercontrols_properties_panel_tabwidget_subtitles_selected_subtitle_title_normal_arrows.setGeometry(260, 25, 30, 15)
    self.playercontrols_properties_panel_tabwidget_subtitles_selected_subtitle_arrow_normal_button.setGeometry(260, 40, 30, 30)
    self.playercontrols_properties_panel_tabwidget_waveform_title_normal.setGeometry(10, 10, 100, 15)
    self.playercontrols_properties_panel_tabwidget_waveform_border_color_title_normal.setGeometry(10, 25, 30, 15)
    self.playercontrols_properties_panel_tabwidget_waveform_border_color_button.setGeometry(10, 40, 30, 30)
    self.playercontrols_properties_panel_tabwidget_waveform_fill_color_title_normal.setGeometry(45, 25, 30, 15)
    self.playercontrols_properties_panel_tabwidget_waveform_fill_color_button.setGeometry(45, 40, 30, 30)
    self.playercontrols_properties_panel_tabwidget_background_title_normal.setGeometry(10, 10, 100, 15)
    self.playercontrols_properties_panel_tabwidget_background_time_text_color_title_normal.setGeometry(10, 25, 30, 15)
    self.playercontrols_properties_panel_tabwidget_background_time_text_color_button.setGeometry(10, 40, 30, 30)
    self.playercontrols_properties_panel_tabwidget_background_cursor_color_title_normal.setGeometry(45, 25, 30, 15)
    self.playercontrols_properties_panel_tabwidget_background_cursor_color_button.setGeometry(45, 40, 30, 30)
    self.playercontrols_properties_panel_tabwidget_background_grid_color_title_normal.setGeometry(80, 25, 30, 15)
    self.playercontrols_properties_panel_tabwidget_background_grid_color_button.setGeometry(80, 40, 30, 30)

    # self.gap_subtitle_duration.setGeometry(self.gap_hbox.width() / 2 - 20, 10, 40, 20)


def playercontrols_stop_button_clicked(self):
    """Function to call when stop button is clicked"""
    # self.player_widget.position = 0.0
    # self.update_timeline.stop()
    playercontrols_playpause_button_clicked(self)
    self.player_widget.stop()
    self.playercontrols_playpause_button.setChecked(False)
    # playercontrols_playpause_button_update(self)
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
    # playercontrols_playpause_button_update(self)


# def playercontrols_playpause_button_update(self):
#     """Function to update things when stop button is clicked"""
#     None
#     self.playercontrols_playpause_button.setStylesheet(self.playercontrols_playpause_button.stylesheet())
#     self.playercontrols_playpause_button.setIcon(QIcon(os.path.join(PATH_SUBTITLD_GRAPHICS, 'pause_icon.svg')) if self.playercontrols_playpause_button.isChecked() else QIcon(os.path.join(PATH_SUBTITLD_GRAPHICS, 'play_icon.svg')))


def show(self):
    """Function that shows the entire panel"""
    show_playercontrols(self)
    update_snap_buttons(self)
    update_grid_buttons(self)
    update_step_buttons(self)
    update_playback_speed_buttons(self)
    timelinescrolling_type_changed(self, self.settings['timeline'].get('scrolling', 'page'))
    self.add_subtitle_duration.setValue(self.default_new_subtitle_duration)
    self.gap_subtitle_duration.setValue(2.0)
    self.repeat_playback_duration.setValue(self.repeat_duration)
    self.repeat_playback_times.setValue(self.repeat_times)


def show_playercontrols(self):
    self.generate_effect(self.playercontrols_widget_animation, 'geometry', 800, [self.playercontrols_widget.x(), self.playercontrols_widget.y(), self.playercontrols_widget.width(), self.playercontrols_widget.height()], [self.playercontrols_widget.x(), self.height() - 200, self.playercontrols_widget.width(), self.playercontrols_widget.height()])


def hide_playercontrols(self):
    self.generate_effect(self.playercontrols_widget_animation, 'geometry', 800, [self.playercontrols_widget.x(), self.playercontrols_widget.y(), self.playercontrols_widget.width(), self.playercontrols_widget.height()], [self.playercontrols_widget.x(), self.height(), self.playercontrols_widget.width(), self.playercontrols_widget.height()])


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
    proportion = ((self.player_widget.position * self.timeline_widget.width_proportion) - self.timeline_scroll.horizontalScrollBar().value()) / self.timeline_scroll.width()
    self.timeline_widget.setGeometry(0, 0, int(round(self.video_metadata.get('duration', 0.01) * self.mediaplayer_zoom)), self.timeline_scroll.height() - 20)
    # self.timeline.zoom_update_waveform(self)
    self.timeline.update_scrollbar(self, position=proportion)


def snap_button_clicked(self):
    """Function to call when snap button is clicked"""
    self.settings['timeline']['snap'] = self.snap_button.isChecked()
    update_snap_buttons(self)


def snap_move_button_clicked(self):
    """Function to call when snap move button is clicked"""
    self.settings['timeline']['snap_moving'] = self.snap_move_button.isChecked()


def snap_move_nereast_button_clicked(self):
    """Function to call when snap move next button is clicked"""
    self.settings['timeline']['snap_move_nereast'] = self.snap_move_nereast_button.isChecked()


def snap_limits_button_clicked(self):
    """Function to call when snap limits button is clicked"""
    self.settings['timeline']['snap_limits'] = self.snap_limits_button.isChecked()


def snap_grid_button_clicked(self):
    """Function to call when snap to grid button is clicked"""
    self.settings['timeline']['snap_grid'] = self.snap_grid_button.isChecked()


def snap_value_changed(self):
    """Function to call when snap value is changed"""
    self.settings['timeline']['snap_value'] = self.snap_value.value() if self.snap_value.value() else .1


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
    subtitles_panel.update_topbar_status(self)
    self.selected_subtitle = False
    self.timeline.update(self)
    self.timeline_widget.setFocus(Qt.TabFocusReason)


def gap_remove_subtitle_button_clicked(self):
    """Function to call when remove gap button is clicked"""
    subtitles.set_gap(subtitles=self.subtitles_list, position=self.player_widget.position, gap=-(self.gap_subtitle_duration.value()))
    self.unsaved = True
    subtitles_panel.update_topbar_status(self)
    self.selected_subtitle = False
    self.timeline.update(self)
    self.timeline_widget.setFocus(Qt.TabFocusReason)


def update_snap_buttons(self):
    """Function to update snap buttons"""
    self.snap_button.setChecked(bool(self.settings['timeline'].get('snap', True)))
    self.snap_limits_button.setEnabled(self.snap_button.isChecked())
    self.snap_limits_button.setChecked(bool(self.settings['timeline'].get('snap_limits', True)))
    self.snap_move_button.setEnabled(self.snap_button.isChecked())
    self.snap_move_button.setChecked(bool(self.settings['timeline'].get('snap_moving', True)))
    self.snap_grid_button.setEnabled(self.snap_button.isChecked())
    self.snap_grid_button.setChecked(bool(self.settings['timeline'].get('snap_grid', False)))
    self.snap_move_nereast_button.setEnabled(self.snap_button.isChecked())
    self.snap_move_nereast_button.setChecked(bool(self.settings['timeline'].get('snap_move_nereast', False)))
    self.snap_value.setEnabled(self.snap_button.isChecked())
    self.snap_value.setValue(float(self.settings['timeline'].get('snap_value', .1)))
    self.timeline_widget.update()


def update_playback_speed_buttons(self):
    """Function to update playback speed buttons"""
    # self.change_playback_speed_icon_label.setEnabled(self.change_playback_speed.isChecked())
    self.change_playback_speed_decrease.setEnabled(self.change_playback_speed.isChecked())
    self.change_playback_speed_slider.setEnabled(self.change_playback_speed.isChecked())
    self.change_playback_speed_increase.setEnabled(self.change_playback_speed.isChecked())
    self.change_playback_speed_label.setText('x' + str(self.playback_speed))
    self.change_playback_speed_slider.setValue(int(self.playback_speed * 100))


def grid_button_clicked(self):
    """Function to call when grid button is clicked"""
    self.settings['timeline']['show_grid'] = self.grid_button.isChecked()
    if not self.settings['timeline'].get('grid_type', False):
        self.settings['timeline']['grid_type'] = 'seconds'
    update_grid_buttons(self)


def grid_type_changed(self, gridtype):
    """Function to call when grid type button is clicked"""
    self.settings['timeline']['grid_type'] = gridtype
    update_grid_buttons(self)


def update_grid_buttons(self):
    """Function to update grid buttons"""
    self.grid_button.setChecked(self.settings['timeline'].get('show_grid', False))
    self.grid_frames_button.setEnabled(self.settings['timeline'].get('show_grid', False))
    self.grid_frames_button.setChecked(True if self.settings['timeline'].get('grid_type', False) == 'frames' else False)
    self.grid_seconds_button.setEnabled(self.settings['timeline'].get('show_grid', False))
    self.grid_seconds_button.setChecked(True if self.settings['timeline'].get('grid_type', False) == 'seconds' else False)
    self.grid_scenes_button.setEnabled(self.settings['timeline'].get('show_grid', False))
    self.grid_scenes_button.setChecked(True if self.settings['timeline'].get('grid_type', False) == 'scenes' else False)
    self.timeline_widget.update()


def playercontrols_play_from_last_start_button_clicked(self):
    """Function to call when stop button is clicked"""
    subt = [item[0] for item in self.subtitles_list]
    last_subtitle = self.subtitles_list[bisect(subt, self.player_widget.position) - 1]
    self.player_widget.seek(last_subtitle[0])
    self.player_widget.play()
    # self.timeline.update_scrollbar(self)
    # self.timeline.update(self)
    self.timeline_widget.setFocus(Qt.TabFocusReason)
    self.playercontrols_playpause_button.setChecked(True)
    # playercontrols_playpause_button_update(self)


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
    self.playercontrols_playpause_button.setChecked(True)
    # playercontrols_playpause_button_update(self)


def add_subtitle_button_clicked(self):
    """Function to call when add subtitle button is clicked"""
    # start_position = False
    self.selected_subtitle = subtitles.add_subtitle(subtitles=self.subtitles_list, position=self.player_widget.position, duration=self.default_new_subtitle_duration, from_last_subtitle=self.add_subtitle_starting_from_last.isChecked())
    self.unsaved = True
    subtitles_panel.update_topbar_status(self)
    self.subtitles_panel.update_subtitles_panel_widget_vision_content(self)
    self.timeline.update(self)
    # self.subtitles_panel.update_properties_widget(self)
    self.properties_textedit.setFocus(Qt.TabFocusReason)
    if self.add_subtitle_and_play.isChecked():
        self.player_widget.play()


def remove_selected_subtitle_button_clicked(self):
    """Function to call when remove selected subtitle button is clicked"""
    subtitles.remove_subtitle(subtitles=self.subtitles_list, selected_subtitle=self.selected_subtitle)
    self.unsaved = True
    subtitles_panel.update_topbar_status(self)
    self.selected_subtitle = False
    subtitles_panel.update_subtitles_panel_widget_vision_content(self)
    self.timeline.update(self)
    # self.subtitles_panel.update_properties_widget(self)
    self.timeline_widget.setFocus(Qt.TabFocusReason)


def slice_selected_subtitle_button_clicked(self):
    """Function to call when slice selected subtitle button is clicked"""
    if self.selected_subtitle:
        pos = self.properties_textedit.textCursor().position()
        last_text = self.properties_textedit.toPlainText()[:pos]
        next_text = self.properties_textedit.toPlainText()[pos:]
        self.selected_subtitle = subtitles.slice_subtitle(subtitles=self.subtitles_list, selected_subtitle=self.selected_subtitle, position=self.player_widget.position, next_text=next_text, last_text=last_text)
        self.unsaved = True
        subtitles_panel.update_topbar_status(self)
        self.subtitles_panel.update_subtitles_panel_widget_vision_content(self)
        self.timeline.update(self)
        # self.subtitles_panel.update_properties_widget(self)
        self.timeline_widget.setFocus(Qt.TabFocusReason)


def select_subtitle_in_current_position(self):
    """Function to call when actual subtitle under cursor need to be selected"""
    subtitle, _ = subtitles.subtitle_under_current_position(subtitles=self.subtitles_list, position=self.player_widget.position)
    if subtitle:
        self.selected_subtitle = subtitle
        self.subtitles_panel.update_subtitles_panel_widget_vision_content(self)
        self.timeline.update(self)
        # self.subtitles_panel.update_properties_widget(self)


def select_next_subtitle_over_current_position(self):
    """Function to call when next subtitle under cursor need to be selected"""
    subtitle = subtitles.next_subtitle_current_position(subtitles=self.subtitles_list, position=self.player_widget.position)
    if subtitle:
        self.selected_subtitle = subtitle
        self.subtitles_panel.update_subtitles_panel_widget_vision_content(self)
        self.timeline.update(self)
        # self.subtitles_panel.update_properties_widget(self)


def select_last_subtitle_over_current_position(self):
    """Function to call when last subtitle under cursor need to be selected"""
    subtitle = subtitles.last_subtitle_current_position(subtitles=self.subtitles_list, position=self.player_widget.position)
    if subtitle:
        self.selected_subtitle = subtitle
        self.subtitles_panel.update_subtitles_panel_widget_vision_content(self)
        self.timeline.update(self)
        # self.subtitles_panel.update_properties_widget(self)


def merge_back_selected_subtitle_button_clicked(self):
    """Function to merge selected subtitle with the last subtitle"""
    if self.selected_subtitle:
        self.selected_subtitle = subtitles.merge_back_subtitle(subtitles=self.subtitles_list, selected_subtitle=self.selected_subtitle)
        self.unsaved = True
        subtitles_panel.update_topbar_status(self)
        self.subtitles_panel.update_subtitles_panel_widget_vision_content(self)
        self.timeline.update(self)
        # self.subtitles_panel.update_properties_widget(self)
        self.timeline_widget.setFocus(Qt.TabFocusReason)


def merge_next_selected_subtitle_button_clicked(self):
    """Function to merge selected subtitle with the next subtitle"""
    if self.selected_subtitle:
        self.selected_subtitle = subtitles.merge_next_subtitle(subtitles=self.subtitles_list, selected_subtitle=self.selected_subtitle)
        self.unsaved = True
        subtitles_panel.update_topbar_status(self)
        self.subtitles_panel.update_subtitles_panel_widget_vision_content(self)
        self.timeline.update(self)
        # self.subtitles_panel.update_properties_widget(self)
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
        subtitles_panel.update_topbar_status(self)
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
        subtitles_panel.update_topbar_status(self)
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
        subtitles.move_start_subtitle(subtitles=self.subtitles_list, selected_subtitle=self.selected_subtitle, amount=-amount, move_nereast=bool(self.settings['timeline'].get('snap_move_nereast', False)))
        self.unsaved = True
        subtitles_panel.update_topbar_status(self)
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
        subtitles.move_start_subtitle(subtitles=self.subtitles_list, selected_subtitle=self.selected_subtitle, amount=amount, move_nereast=bool(self.settings['timeline'].get('snap_move_nereast', False)))
        self.unsaved = True
        subtitles_panel.update_topbar_status(self)
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
        subtitles_panel.update_topbar_status(self)
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
        subtitles_panel.update_topbar_status(self)
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
    subtitles_panel.update_topbar_status(self)
    self.subtitles_panel.update_subtitles_panel_widget_vision_content(self)
    self.timeline.update(self)
    # self.subtitles_panel.update_properties_widget(self)
    self.timeline_widget.setFocus(Qt.TabFocusReason)


def last_end_to_current_position_button_clicked(self):
    """Function to move last ending position of selected subtitle to current cursor position"""
    subtitles.last_end_to_current_position(subtitles=self.subtitles_list, position=self.player_widget.position)
    self.unsaved = True
    subtitles_panel.update_topbar_status(self)
    self.subtitles_panel.update_subtitles_panel_widget_vision_content(self)
    self.timeline.update(self)
    # self.subtitles_panel.update_properties_widget(self)
    self.timeline_widget.setFocus(Qt.TabFocusReason)


def last_start_to_current_position_button_clicked(self):
    """Function to move last starting position subtitle to current cursor position"""
    subtitles.last_start_to_current_position(subtitles=self.subtitles_list, position=self.player_widget.position)
    self.unsaved = True
    subtitles_panel.update_topbar_status(self)
    self.subtitles_panel.update_subtitles_panel_widget_vision_content(self)
    self.timeline.update(self)
    # self.subtitles_panel.update_properties_widget(self)
    self.timeline_widget.setFocus(Qt.TabFocusReason)


def last_start_last_end_to_current_position_button_clicked(self):
    """Function to move starting position subtitle to current cursor position"""
    subtitles.subtitle_start_to_current_position(subtitles=self.subtitles_list, position=self.player_widget.position)
    self.unsaved = True
    subtitles_panel.update_topbar_status(self)
    self.subtitles_panel.update_subtitles_panel_widget_vision_content(self)
    self.timeline.update(self)
    # self.subtitles_panel.update_properties_widget(self)
    self.timeline_widget.setFocus(Qt.TabFocusReason)


def next_start_next_end_to_current_position_button_clicked(self):
    """Function to move ending position subtitle to current cursor position"""
    subtitles.subtitle_end_to_current_position(subtitles=self.subtitles_list, position=self.player_widget.position)
    self.unsaved = True
    subtitles_panel.update_topbar_status(self)
    self.subtitles_panel.update_subtitles_panel_widget_vision_content(self)
    self.timeline.update(self)
    # self.subtitles_panel.update_properties_widget(self)
    self.timeline_widget.setFocus(Qt.TabFocusReason)


def next_end_to_current_position_button_clicked(self):
    """Function to move next ending position to current cursor position"""
    subtitles.next_end_to_current_position(subtitles=self.subtitles_list, position=self.player_widget.position)
    self.unsaved = True
    subtitles_panel.update_topbar_status(self)
    self.subtitles_panel.update_subtitles_panel_widget_vision_content(self)
    self.timeline.update(self)
    # self.subtitles_panel.update_properties_widget(self)
    self.timeline_widget.setFocus(Qt.TabFocusReason)


def change_playback_speed_clicked(self):
    """Function to call when playback speed button is clicked"""
    # if not self.change_playback_speed.isChecked():
    # self.playback_speed = 1.0
    self.player.update_speed(self)
    update_playback_speed_buttons(self)
    self.timeline_widget.setFocus(Qt.TabFocusReason)


def change_playback_speed_decrease_clicked(self):
    """Function to call when playback speed decrease button is clicked"""
    self.change_playback_speed_slider.setValue(self.change_playback_speed_slider.value() - 10)
    self.playback_speed = self.change_playback_speed_slider.value() / 100.0
    self.player.update_speed(self)
    update_playback_speed_buttons(self)
    self.timeline_widget.setFocus(Qt.TabFocusReason)


def change_playback_speed_slider(self):
    """Function to call when playback speed slider button is changed"""
    self.playback_speed = self.change_playback_speed_slider.value() / 100.0
    self.player.update_speed(self)
    update_playback_speed_buttons(self)
    self.timeline_widget.setFocus(Qt.TabFocusReason)


def change_playback_speed_increase_clicked(self):
    """Function to call when playback speed increase button is clicked"""
    self.change_playback_speed_slider.setValue(self.change_playback_speed_slider.value() + 10)
    self.playback_speed = self.change_playback_speed_slider.value() / 100.0
    self.player.update_speed(self)
    update_playback_speed_buttons(self)
    self.timeline_widget.setFocus(Qt.TabFocusReason)


def repeat_playback_clicked(self):
    """Function to call when playback repeat button is clicked"""
    self.repeat_activated = self.repeat_playback.isChecked()
    self.repeat_duration_tmp = []
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
        self.playercontrols_properties_panel_placeholder.setGeometry(self.playercontrols_widget.width() - panel_width, 5, panel_width, 180)
        self.playercontrols_properties_panel.setGeometry(0, 56, self.playercontrols_properties_panel_placeholder.width(), 140)
        # self.playercontrols_properties_panel_toggle.setGeometry(self.playercontrols_widget_bottom_right_corner.x(), self.playercontrols_widget_bottom_right_corner.y() + 100, self.playercontrols_widget_bottom_right_corner.width(), self.playercontrols_widget_bottom_right_corner.height())
    else:
        self.playercontrols_properties_panel_placeholder.setGeometry(self.playercontrols_widget.width() - panel_width, 5, panel_width, 80)
        self.playercontrols_properties_panel.setGeometry(0, 56, self.playercontrols_properties_panel_placeholder.width(), 140)
        # self.playercontrols_properties_panel_toggle.setGeometry(self.playercontrols_widget_bottom_right_corner.x(), self.playercontrols_widget_bottom_right_corner.y(), self.playercontrols_widget_bottom_right_corner.width(), self.playercontrols_widget_bottom_right_corner.height())


def playercontrols_properties_panel_toggle_pressed(self):
    playercontrols_properties_panel_tabwidget_subtitles_update_widgets(self)
    show_or_hide_playercontrols_properties_panel(self)


def playercontrols_properties_panel_tabwidget_subtitles_subtitle_border_color_button_clicked(self):
    """Function to show qcolordialog to choose subtitle border color"""
    color = QColorDialog.getColor(options=QColorDialog.ShowAlphaChannel)
    if color.isValid():
        self.settings['timeline']['subtitle_border_color'] = color.name(1)
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


def translate_widgets(self):
    self.add_subtitle_button_label.setText(_('playercontrols.add'))
    self.snap_button_label.setText(_('playercontrols.snap'))
    self.step_button_label.setText(_('playercontrols.step'))
    self.remove_selected_subtitle_button.setText(_('playercontrols.remove'))
    self.grid_button.setText(_('playercontrols.grid'))
