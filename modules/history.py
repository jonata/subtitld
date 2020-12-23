"""History module (Ctrl+Z)

"""

import copy

ALL_HISTORY = []
REDO_HISTORY = []


def history_append(subtitles):
    """Append subtitles list to history"""
    ALL_HISTORY.append(copy.deepcopy(subtitles))
    REDO_HISTORY.clear()


def history_undo(actual_subtitles):
    """Revert to last subtitle on the history list"""
    if ALL_HISTORY:
        REDO_HISTORY.append(copy.deepcopy(actual_subtitles))
        actual_subtitles.clear()
        actual_subtitles.extend(copy.deepcopy(ALL_HISTORY.pop()))


def history_redo(actual_subtitles):
    """Redo subtitle on the history list"""
    if REDO_HISTORY:
        actual_subtitles.clear()
        actual_subtitles.extend(copy.deepcopy(REDO_HISTORY.pop()))
