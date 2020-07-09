#!/usr/bin/env python3

from bisect import bisect
from modules import history


def add_subtitle(subtitles=[], position=0.0, duration=5.0, text=''):
    history.history_append(subtitles)

    subt = [item[0] for item in subtitles]
    index = bisect(subt, position)

    if index and subtitles[index-1][0] + subtitles[index-1][1] > position:
        subtitles[index-1][1] -= (subtitles[index-1][0] + subtitles[index-1][1]) - position

    if len(subtitles) - 1 > index and subtitles[index][0] - position < duration:
        duration = subtitles[index][0] - position

    subtitles.insert(index, [position, duration, text])

    return subtitles[subtitles.index([position, duration, text])]


def remove_subtitle(subtitles=[], selected_subtitle=False):
    if selected_subtitle:
        history.history_append(subtitles)

        subtitles.remove(selected_subtitle)
    return subtitles


def slice_subtitle(subtitles=[], selected_subtitle=False, position=0.0, last_text='', next_text=''):
    if selected_subtitle and position > selected_subtitle[0] and position < (selected_subtitle[0] + selected_subtitle[1]):
        history.history_append(subtitles)

        index = subtitles.index(selected_subtitle)

        if position > subtitles[index][0] and position < (subtitles[index][0] + subtitles[index][1]):
            position_to_cut = position
        else:
            position_to_cut = (subtitles[index][0] + subtitles[index][1])/2

        new_duration = (subtitles[index][0] + subtitles[index][1]) - position_to_cut

        subtitles[index][1] = position_to_cut - subtitles[index][0] - 0.001
        subtitles[index][2] = last_text

        return add_subtitle(subtitles=subtitles, position=position_to_cut, duration=new_duration, text=next_text)


def merge_back_subtitle(subtitles=[], selected_subtitle=False):
    if selected_subtitle and subtitles.index(selected_subtitle):
        history.history_append(subtitles)

        index = subtitles.index(selected_subtitle)
        subtitles[index-1][1] = selected_subtitle[0] + selected_subtitle[1] - subtitles[index-1][0]
        subtitles[index-1][2] += ' ' + subtitles[index][2]

        remove_subtitle(subtitles=subtitles, selected_subtitle=subtitles[index])

        return subtitles[index-1]


def merge_next_subtitle(subtitles=[], selected_subtitle=False):
    if selected_subtitle and subtitles.index(selected_subtitle) < len(subtitles) - 1:
        history.history_append(subtitles)

        index = subtitles.index(selected_subtitle)
        subtitles[index][1] = subtitles[index+1][0] + subtitles[index+1][1] - selected_subtitle[0]
        subtitles[index][2] += ' ' + subtitles[index+1][2]

        remove_subtitle(subtitles=subtitles, selected_subtitle=subtitles[index+1])

        return subtitles[index]


def next_start_to_current_position(subtitles=[], position=0.0):
    history.history_append(subtitles)
    subt = [item[0] for item in subtitles]
    index = bisect(subt, position)
    if index < len(subt):
        end = subtitles[index][0] + subtitles[index][1]
        subtitles[index][0] = position
        subtitles[index][1] = end - position
    if index and subtitles[index-1][0] + subtitles[index-1][1] > position:
        last_end_to_current_position(subtitles=subtitles, position=position - 0.001)


def next_end_to_current_position(subtitles=[], position=0.0):
    history.history_append(subtitles)
    subt = [item[0] for item in subtitles]
    index = bisect(subt, position)
    if index:
        end = subtitles[index-1][0] + subtitles[index-1][1]
        if end > position:
            subtitles[index-1][1] = position - subtitles[index-1][0]


def last_end_to_current_position(subtitles=[], position=0.0):
    history.history_append(subtitles)
    subt = [item[0] for item in subtitles]
    index = bisect(subt, position)

    if index - 1 < len(subt) - 1:
        subtitles[index-1][1] = position - subtitles[index-1][0]


def last_start_to_current_position(subtitles=[], position=0.0):
    history.history_append(subtitles)
    subt = [item[0] for item in subtitles]
    index = bisect(subt, position)
    if index and subtitles[index-1][0] < position and not (subtitles[index-1][0] + subtitles[index-1][1]) < position:
        end = subtitles[index-1][0] + subtitles[index-1][1]
        subtitles[index-1][0] = position
        subtitles[index-1][1] = end - position


def send_text_to_next_subtitle(subtitles=[], selected_subtitle=False, last_text='', next_text=''):
    if selected_subtitle and subtitles.index(selected_subtitle) + 1 < len(subtitles):
        history.history_append(subtitles)
        index = subtitles.index(selected_subtitle)
        subtitles[index][2] = last_text
        subtitles[index+1][2] = next_text + ' ' + subtitles[index+1][2]


def send_text_to_last_subtitle(subtitles=[], selected_subtitle=False, last_text='', next_text=''):
    if selected_subtitle and subtitles.index(selected_subtitle):
        history.history_append(subtitles)
        index = subtitles.index(selected_subtitle)
        subtitles[index][2] = next_text
        subtitles[index-1][2] += ' ' + last_text


def set_gap(subtitles=[], position=0.0, gap=0.0):
    for subtitle in subtitles:
        if subtitle[0] > position:
            subtitle[0] += gap
