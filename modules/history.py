#!/usr/bin/env python3

import copy

ALL_HISTORY = []
REDO_HISTORY = []


def history_append(subtitles=[]):
    ALL_HISTORY.append(copy.deepcopy(subtitles))
    REDO_HISTORY.clear()


def history_undo(actual_subtitles):
    if ALL_HISTORY:
        REDO_HISTORY.append(copy.deepcopy(actual_subtitles))
        actual_subtitles.clear()
        actual_subtitles.extend(copy.deepcopy(ALL_HISTORY.pop()))


def history_redo(actual_subtitles):
    if REDO_HISTORY:
        actual_subtitles.clear()
        actual_subtitles.extend(copy.deepcopy(REDO_HISTORY.pop()))
