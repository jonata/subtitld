"""Properties panel"""

from PyQt5.QtWidgets import QLabel, QCheckBox
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve


def load(self):
    """Load properties panel widgets"""
    self.global_properties_panel_widget = QLabel(parent=self)
    self.global_properties_panel_widget_animation = QPropertyAnimation(self.global_properties_panel_widget, b'geometry')
    self.global_properties_panel_widget_animation.setEasingCurve(QEasingCurve.OutCirc)

    self.global_properties_panel_background = QLabel(parent=self.global_properties_panel_widget)
    self.global_properties_panel_background.setObjectName('global_properties_panel')

    self.global_properties_panel_show_margins = QCheckBox('Show safety margins', parent=self.global_properties_panel_widget)
    self.global_properties_panel_show_margins.clicked.connect(lambda: global_properties_panel_show_margins_clicked(self))
    self.global_properties_panel_show_margins.setChecked(self.settings['safety_margins'].get('show_action_safe_margins', False))


def resized(self):
    """Resize function of properties panel widgets"""
    if (self.subtitles_list or self.video_metadata):
        if self.properties_toggle_button.isChecked():
            self.global_properties_panel_widget.setGeometry(self.width()*.8, 0, (self.width()*.2), self.height()-self.playercontrols_widget.height()+20)
        else:
            self.global_properties_panel_widget.setGeometry(int(self.width()*.8)+18, 0, (self.width()*.2), self.height()-self.playercontrols_widget.height()+20)
    else:
        self.global_properties_panel_widget.setGeometry(self.width(), 0, (self.width()*.2), self.height()-self.playercontrols_widget.height()+20)
    self.global_properties_panel_background.setGeometry(0, 0, self.global_properties_panel_widget.width(), self.global_properties_panel_widget.height())

    self.global_properties_panel_show_margins.setGeometry(35, 20, self.global_properties_panel_widget.width()-55, 25)


def global_properties_panel_toggle_button_clicked(self):
    """Function when properties panel button is clicked"""
    if self.global_properties_panel_toggle_button.isChecked():
        show_global_properties_panel(self)
    else:
        hide_global_properties_panel(self)


def global_properties_panel_show_margins_clicked(self):
    """Function when checkbox for margins is clicked"""
    if self.global_properties_panel_show_margins.isChecked():
        self.player_widget.show_margins = [.05, .05]
    else:
        self.player_widget.show_margins = False
    self.settings['safety_margins']['show_action_safe_margins'] = self.global_properties_panel_show_margins.isChecked()
    self.settings['safety_margins']['show_title_safe_margins'] = self.global_properties_panel_show_margins.isChecked()
    self.player.update_safety_margins_subtitle_layer(self)


def show_global_properties_panel(self):
    """Function to show global properties panel"""
    self.generate_effect(self.global_properties_panel_widget_animation, 'geometry', 700, [self.global_properties_panel_widget.x(), self.global_properties_panel_widget.y(), self.global_properties_panel_widget.width(), self.global_properties_panel_widget.height()], [int(self.width()*.8), self.global_properties_panel_widget.y(), self.global_properties_panel_widget.width(), self.global_properties_panel_widget.height()])


def hide_global_properties_panel(self):
    """Function to hide global properties panel"""
    self.generate_effect(self.global_properties_panel_widget_animation, 'geometry', 700, [self.global_properties_panel_widget.x(), self.global_properties_panel_widget.y(), self.global_properties_panel_widget.width(), self.global_properties_panel_widget.height()], [int((self.width()*.8)+18), self.global_properties_panel_widget.y(), self.global_properties_panel_widget.width(), self.global_properties_panel_widget.height()])
