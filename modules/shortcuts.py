
#!/usr/bin/env python3

from PyQt5.QtWidgets import QShortcut, QAction
from PyQt5.QtGui import QKeySequence

shortcuts_dict = {
                    'playpause': 'Play/Pause'
}


def load(self, shortcut_commands):
    for command in shortcut_commands.keys():
        if command == 'playpause':
            playpause_action = QAction(shortcuts_dict['playpause'], self)
            playpause_action.setShortcuts(shortcut_commands[command])
            playpause_action.triggered.connect(lambda: self.playercontrols.playercontrols_playpause_button_clicked(self))
            self.addAction(playpause_action)

            #menu.addAction(history_action)
            #self.shcut = QShortcut(QKeySequence(shortcut_commands[command]), self)
            #self.shcut.activated.connect(self.playercontrols.playercontrols_playpause_button_clicked)
            #self.shcut = QShortcut(QKeySequence('Ctrl+O'), self)
            #self.shcut.activated.connect(lambda: self.playercontrols.playercontrols_playpause_button_clicked(self))
            #self.playercontrols_playpause_button.setShortcut(QKeySequence.fromString(shortcut_commands[command]))
            #self.playercontrols_playpause_button.setShortcut(QKeySequence.fromString('Shift+0'))
            #self.playercontrols_playpause_button.setShortcut(QKeySequence(shortcut_commands[command][0]))
            #self.playercontrols_playpause_button.setShortcut(shortcut_commands[command])
            #print(shortcut_commands[command])
