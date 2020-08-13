
#!/usr/bin/env python3

from PySide2.QtGui import QKeySequence

shortcuts_dict = {
                    'playpause': 'Play/Pause'
}


def load(self, shortcut_commands):
    for command in shortcut_commands.keys():
        if command == 'playpause':
            self.playercontrols.playercontrols_playpause_button.setShortcut(QKeySequence.fromString(shortcut_commands[command]))
