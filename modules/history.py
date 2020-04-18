#!/usr/bin/env python3

import copy

ALL_HISTORY = []
REDO_HISTORY = []

def history_append(subtitles=[]):
    ALL_HISTORY.append(copy.deepcopy(subtitles))
    REDO_HISTORY = []

def history_undo(actual_subtitles):
    REDO_HISTORY.append(copy.deepcopy(actual_subtitles))
    return ALL_HISTORY.pop() if ALL_HISTORY else []


def history_redo(actual_subtitles):
    return REDO_HISTORY.pop() if REDO_HISTORY else []
