"""Shortcuts module

"""

from PyQt5.QtWidgets import QAction


shortcuts_dict = {
    'playpause': 'Play/Pause',
    'subtitle_start_to_current_position': 'Subtitle start to current position',
    'subtitle_end_subtitle_to_current_position': 'Subtitle end to current position',
    'add_new_subtitle_to_current_position': 'Add new subtitle to current position',
    'remove_current_subtitle': 'Remove current subtitle',
    'zoom_out': 'Zoom out',
    'zoom_in': 'Zoom in',
    'slice_current_subtitle': 'Slice current subtitle',
    'select_subtitle_in_current_position': 'Select subtitle in current position',
    'add_step_subtitle_start': 'Add a step to subtitle start',
    'subtract_step_subtitle_start': 'Subtract a step to subtitle start',
    'add_step_subtitle_end': 'Add a step to subtitle end',
    'subtract_step_subtitle_end': 'Subtract a step to subtitle end',
    'move_step_backward_subtitle': 'Move subtitle a step backward',
    'move_step_forward_subtitle': 'Move subtitle a step forward',
    'select_next_subtitle_over_current_position': 'Select next subtitle over current position',
    'select_last_subtitle_over_current_position': 'Select last subtitle over current position',
}


default_shortcuts_dict = {
    'playpause': ['Space'],
    'subtitle_start_to_current_position': ['0'],
    'subtitle_end_subtitle_to_current_position': [','],
    'add_new_subtitle_to_current_position': ['Enter'],
    'remove_current_subtitle': ['*'],
    'zoom_out': ['-'],
    'zoom_in': ['+'],
    'slice_current_subtitle': ['/'],
    'select_subtitle_in_current_position': ['5'],
    'add_step_subtitle_start': ['7'],
    'subtract_step_subtitle_start': ['1'],
    'add_step_subtitle_end': ['9'],
    'subtract_step_subtitle_end': ['3'],
    'move_step_backward_subtitle': ['4'],
    'move_step_forward_subtitle': ['6'],
    'select_next_subtitle_over_current_position': ['8'],
    'select_last_subtitle_over_current_position': ['2'],
}


def load(self, shortcut_commands):
    """Function to load shortcuts commands on widgets"""
    for item in default_shortcuts_dict:
        if not item in shortcut_commands:
            shortcut_commands[item] = default_shortcuts_dict[item]

    for command in shortcut_commands.keys():
        if command == 'playpause':
            playpause_action = QAction(shortcuts_dict['playpause'], self)
            playpause_action.setShortcuts(shortcut_commands[command])
            playpause_action.triggered.connect(lambda: self.playercontrols.playercontrols_playpause_button_clicked(self))
            self.addAction(playpause_action)

    for command in shortcut_commands.keys():
        if command == 'subtitle_start_to_current_position':
            subtitle_start_to_current_position_action = QAction(shortcuts_dict['subtitle_start_to_current_position'], self)
            subtitle_start_to_current_position_action.setShortcuts(shortcut_commands[command])
            subtitle_start_to_current_position_action.triggered.connect(lambda: self.playercontrols.subtitle_start_to_current_position_button_clicked(self))
            self.addAction(subtitle_start_to_current_position_action)

    for command in shortcut_commands.keys():
        if command == 'subtitle_end_subtitle_to_current_position':
            subtitle_end_subtitle_to_current_position_action = QAction(shortcuts_dict['subtitle_end_subtitle_to_current_position'], self)
            subtitle_end_subtitle_to_current_position_action.setShortcuts(shortcut_commands[command])
            subtitle_end_subtitle_to_current_position_action.triggered.connect(lambda: self.playercontrols.subtitle_end_to_current_position_button_clicked(self))
            self.addAction(subtitle_end_subtitle_to_current_position_action)

    for command in shortcut_commands.keys():
        if command == 'add_new_subtitle_to_current_position':
            add_new_subtitle_to_current_position_action = QAction(shortcuts_dict['add_new_subtitle_to_current_position'], self)
            add_new_subtitle_to_current_position_action.setShortcuts(shortcut_commands[command])
            add_new_subtitle_to_current_position_action.triggered.connect(lambda: self.playercontrols.add_subtitle_button_clicked(self))
            self.addAction(add_new_subtitle_to_current_position_action)

    for command in shortcut_commands.keys():
        if command == 'remove_current_subtitle':
            remove_current_subtitle_action = QAction(shortcuts_dict['remove_current_subtitle'], self)
            remove_current_subtitle_action.setShortcuts(shortcut_commands[command])
            remove_current_subtitle_action.triggered.connect(lambda: self.playercontrols.remove_selected_subtitle_button_clicked(self))
            self.addAction(remove_current_subtitle_action)

    for command in shortcut_commands.keys():
        if command == 'zoom_in':
            zoom_in_action = QAction(shortcuts_dict['zoom_in'], self)
            zoom_in_action.setShortcuts(shortcut_commands[command])
            zoom_in_action.triggered.connect(lambda: self.playercontrols.zoomin_button_clicked(self))
            self.addAction(zoom_in_action)

    for command in shortcut_commands.keys():
        if command == 'zoom_out':
            zoom_out_action = QAction(shortcuts_dict['zoom_out'], self)
            zoom_out_action.setShortcuts(shortcut_commands[command])
            zoom_out_action.triggered.connect(lambda: self.playercontrols.zoomout_button_clicked(self))
            self.addAction(zoom_out_action)

    for command in shortcut_commands.keys():
        if command == 'slice_current_subtitle':
            slice_current_subtitle_action = QAction(shortcuts_dict['slice_current_subtitle'], self)
            slice_current_subtitle_action.setShortcuts(shortcut_commands[command])
            slice_current_subtitle_action.triggered.connect(lambda: self.playercontrols.slice_selected_subtitle_button_clicked(self))
            self.addAction(slice_current_subtitle_action)

    for command in shortcut_commands.keys():
        if command == 'select_subtitle_in_current_position':
            select_subtitle_in_current_position_action = QAction(shortcuts_dict['select_subtitle_in_current_position'], self)
            select_subtitle_in_current_position_action.setShortcuts(shortcut_commands[command])
            select_subtitle_in_current_position_action.triggered.connect(lambda: self.playercontrols.select_subtitle_in_current_position(self))
            self.addAction(select_subtitle_in_current_position_action)

    for command in shortcut_commands.keys():
        if command == 'add_step_subtitle_start':
            add_step_subtitle_start_action = QAction(shortcuts_dict['add_step_subtitle_start'], self)
            add_step_subtitle_start_action.setShortcuts(shortcut_commands[command])
            add_step_subtitle_start_action.triggered.connect(lambda: self.playercontrols.move_start_forward_subtitle_clicked(self))
            self.addAction(add_step_subtitle_start_action)

    for command in shortcut_commands.keys():
        if command == 'subtract_step_subtitle_start':
            subtract_step_subtitle_start_action = QAction(shortcuts_dict['subtract_step_subtitle_start'], self)
            subtract_step_subtitle_start_action.setShortcuts(shortcut_commands[command])
            subtract_step_subtitle_start_action.triggered.connect(lambda: self.playercontrols.move_start_back_subtitle_clicked(self))
            self.addAction(subtract_step_subtitle_start_action)

    for command in shortcut_commands.keys():
        if command == 'add_step_subtitle_end':
            add_step_subtitle_end_action = QAction(shortcuts_dict['add_step_subtitle_end'], self)
            add_step_subtitle_end_action.setShortcuts(shortcut_commands[command])
            add_step_subtitle_end_action.triggered.connect(lambda: self.playercontrols.move_end_forward_subtitle_clicked(self))
            self.addAction(add_step_subtitle_end_action)

    for command in shortcut_commands.keys():
        if command == 'subtract_step_subtitle_end':
            subtract_step_subtitle_end_action = QAction(shortcuts_dict['subtract_step_subtitle_end'], self)
            subtract_step_subtitle_end_action.setShortcuts(shortcut_commands[command])
            subtract_step_subtitle_end_action.triggered.connect(lambda: self.playercontrols.move_end_back_subtitle_clicked(self))
            self.addAction(subtract_step_subtitle_end_action)

    for command in shortcut_commands.keys():
        if command == 'move_step_backward_subtitle':
            move_step_backward_subtitle_action = QAction(shortcuts_dict['move_step_backward_subtitle'], self)
            move_step_backward_subtitle_action.setShortcuts(shortcut_commands[command])
            move_step_backward_subtitle_action.triggered.connect(lambda: self.playercontrols.move_backward_subtitle_clicked(self))
            self.addAction(move_step_backward_subtitle_action)

    for command in shortcut_commands.keys():
        if command == 'move_step_forward_subtitle':
            move_step_forward_subtitle_action = QAction(shortcuts_dict['move_step_forward_subtitle'], self)
            move_step_forward_subtitle_action.setShortcuts(shortcut_commands[command])
            move_step_forward_subtitle_action.triggered.connect(lambda: self.playercontrols.move_forward_subtitle_clicked(self))
            self.addAction(move_step_forward_subtitle_action)

    for command in shortcut_commands.keys():
        if command == 'select_next_subtitle_over_current_position':
            select_next_subtitle_over_current_position_action = QAction(shortcuts_dict['select_next_subtitle_over_current_position'], self)
            select_next_subtitle_over_current_position_action.setShortcuts(shortcut_commands[command])
            select_next_subtitle_over_current_position_action.triggered.connect(lambda: self.playercontrols.select_next_subtitle_over_current_position(self))
            self.addAction(select_next_subtitle_over_current_position_action)

    for command in shortcut_commands.keys():
        if command == 'select_last_subtitle_over_current_position':
            select_last_subtitle_over_current_position_action = QAction(shortcuts_dict['select_last_subtitle_over_current_position'], self)
            select_last_subtitle_over_current_position_action.setShortcuts(shortcut_commands[command])
            select_last_subtitle_over_current_position_action.triggered.connect(lambda: self.playercontrols.select_last_subtitle_over_current_position(self))
            self.addAction(select_last_subtitle_over_current_position_action)
