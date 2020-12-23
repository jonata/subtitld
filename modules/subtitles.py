"""Module to handle subtitles

"""

from bisect import bisect
from modules import history


def add_subtitle(subtitles=False, position=0.0, duration=5.0, text=''):
    """Function to add a subtitle to the main subtitle list"""
    if not subtitles:
        subtitles = []

    history.history_append(subtitles)

    subt = [item[0] for item in subtitles]
    index = bisect(subt, position)

    if index and subtitles[index-1][0] + subtitles[index-1][1] > position:
        subtitles[index-1][1] -= (subtitles[index-1][0] + subtitles[index-1][1]) - position

    if len(subtitles) - 1 > index and subtitles[index][0] - position < duration:
        duration = subtitles[index][0] - position

    subtitles.insert(index, [position, duration, text])

    return subtitles[subtitles.index([position, duration, text])]


def remove_subtitle(subtitles=False, selected_subtitle=False):
    """Function to add a subtitle to the main subtitle list"""
    if not subtitles:
        subtitles = []

    if selected_subtitle:
        history.history_append(subtitles)

        subtitles.remove(selected_subtitle)
    return subtitles


def slice_subtitle(subtitles=False, selected_subtitle=False, position=0.0, last_text='', next_text=''):
    """Function to slice a subtitle in the main subtitle list"""
    if not subtitles:
        subtitles = []

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


def merge_back_subtitle(subtitles=False, selected_subtitle=False):
    """Function to merge a subtitle to the last in the main subtitle list"""
    if not subtitles:
        subtitles = []

    if selected_subtitle and subtitles.index(selected_subtitle):
        history.history_append(subtitles)

        index = subtitles.index(selected_subtitle)
        subtitles[index-1][1] = selected_subtitle[0] + selected_subtitle[1] - subtitles[index-1][0]
        subtitles[index-1][2] += ' ' + subtitles[index][2]

        remove_subtitle(subtitles=subtitles, selected_subtitle=subtitles[index])

        return subtitles[index-1]


def merge_next_subtitle(subtitles=False, selected_subtitle=False):
    """Function to merge a subtitle to the next in the main subtitle list"""
    if not subtitles:
        subtitles = []

    result = False
    if selected_subtitle and subtitles.index(selected_subtitle) < len(subtitles) - 1:
        history.history_append(subtitles)

        index = subtitles.index(selected_subtitle)
        subtitles[index][1] = subtitles[index+1][0] + subtitles[index+1][1] - selected_subtitle[0]
        subtitles[index][2] += ' ' + subtitles[index+1][2]

        remove_subtitle(subtitles=subtitles, selected_subtitle=subtitles[index+1])

        result = subtitles[index]
    return result


def move_subtitle(subtitles=False, selected_subtitle=False, amount=0.0):
    """Function to move a subtitle in the main subtitle list"""
    if not subtitles:
        subtitles = []

    if selected_subtitle:
        history.history_append(subtitles)
        selected_subtitle[0] += amount


def move_start_subtitle(subtitles=False, selected_subtitle=False, amount=0.0):
    """Function to move the start a subtitle in the main subtitle list"""
    if not subtitles:
        subtitles = []

    if selected_subtitle:
        history.history_append(subtitles)
        selected_subtitle[0] += amount
        selected_subtitle[1] -= amount


def move_end_subtitle(subtitles=False, selected_subtitle=False, amount=0.0):
    """Function to move the end of a subtitle in the main subtitle list"""
    if not subtitles:
        subtitles = []

    if selected_subtitle:
        history.history_append(subtitles)
        selected_subtitle[1] += amount


def next_start_to_current_position(subtitles=False, position=0.0):
    """Function to set next start to position of a subtitle in the main subtitle list"""
    if not subtitles:
        subtitles = []

    history.history_append(subtitles)
    subt = [item[0] for item in subtitles]
    index = bisect(subt, position)
    if index < len(subt):
        end = subtitles[index][0] + subtitles[index][1]
        subtitles[index][0] = position
        subtitles[index][1] = end - position
    if index and subtitles[index-1][0] + subtitles[index-1][1] > position:
        last_end_to_current_position(subtitles=subtitles, position=position - 0.001)


def subtitle_start_to_current_position(subtitles=False, position=0.0):
    """Function to set start to position of a subtitle in the main subtitle list"""
    if not subtitles:
        subtitles = []

    history.history_append(subtitles)
    subt = [item[0] for item in subtitles]
    index = bisect(subt, position)
    if index and position < (subtitles[index-1][0] + subtitles[index-1][1]):
        end = subtitles[index-1][0] + subtitles[index-1][1]
        subtitles[index-1][0] = position
        subtitles[index-1][1] = end - position
    else:
        end = subtitles[index][0] + subtitles[index][1]
        subtitles[index][0] = position
        subtitles[index][1] = end - position


def subtitle_end_to_current_position(subtitles=False, position=0.0):
    """Function to set end to position of a subtitle in the main subtitle list"""
    if not subtitles:
        subtitles = []

    history.history_append(subtitles)
    subt = [item[0] for item in subtitles]
    index = bisect(subt, position)
    if index:
        if position < (subtitles[index-1][0] + subtitles[index-1][1]):
            subtitles[index-1][1] = position - subtitles[index-1][0]
        else:
            subtitles[index-1][1] = position - subtitles[index-1][0]


def subtitle_under_current_position(subtitles=False, position=0.0):
    """Function to return subtitle under position"""
    if not subtitles:
        subtitles = []

    current_subtitle = False
    subt = [item[0] for item in subtitles]
    index = bisect(subt, position)
    if position > subtitles[index-1][0] and position < (subtitles[index-1][0] + subtitles[index-1][1]):
        current_subtitle = subtitles[index-1]
    return current_subtitle


def last_subtitle_current_position(subtitles=False, position=0.0):
    """Function to return the last subtitle of position"""
    if not subtitles:
        subtitles = []

    last_subtitle = False
    subt = [item[0] for item in subtitles]
    index = bisect(subt, position)
    if index:
        if position > (subtitles[index-1][0] + subtitles[index-1][1]):
            last_subtitle = subtitles[index-1]
    return last_subtitle


def next_subtitle_current_position(subtitles=False, position=0.0):
    """Function to return the next subtitle of position"""
    if not subtitles:
        subtitles = []

    next_subtitle = False
    subt = [item[0] for item in subtitles]
    index = bisect(subt, position)
    if index < len(subt):
        next_subtitle = subtitles[index]
    return next_subtitle


def next_end_to_current_position(subtitles=False, position=0.0):
    """Function set next end to position"""
    if not subtitles:
        subtitles = []

    history.history_append(subtitles)
    subt = [item[0] for item in subtitles]
    index = bisect(subt, position)
    if index:
        end = subtitles[index-1][0] + subtitles[index-1][1]
        if end > position:
            subtitles[index-1][1] = position - subtitles[index-1][0]


def last_end_to_current_position(subtitles=False, position=0.0):
    """Function set last end to position"""
    if not subtitles:
        subtitles = []

    history.history_append(subtitles)
    subt = [item[0] for item in subtitles]
    index = bisect(subt, position)

    if index - 1 < len(subt) - 1:
        subtitles[index-1][1] = position - subtitles[index-1][0]


def last_start_to_current_position(subtitles=False, position=0.0):
    """Function set last start to position"""
    if not subtitles:
        subtitles = []

    history.history_append(subtitles)
    subt = [item[0] for item in subtitles]
    index = bisect(subt, position)
    if index and subtitles[index-1][0] < position and not (subtitles[index-1][0] + subtitles[index-1][1]) < position:
        end = subtitles[index-1][0] + subtitles[index-1][1]
        subtitles[index-1][0] = position
        subtitles[index-1][1] = end - position


def send_text_to_next_subtitle(subtitles=False, selected_subtitle=False, last_text='', next_text=''):
    """Function send text to the next subtitle"""
    if not subtitles:
        subtitles = []

    if selected_subtitle and subtitles.index(selected_subtitle) + 1 < len(subtitles):
        history.history_append(subtitles)
        index = subtitles.index(selected_subtitle)
        subtitles[index][2] = last_text
        subtitles[index+1][2] = next_text + ' ' + subtitles[index+1][2]


def send_text_to_last_subtitle(subtitles=False, selected_subtitle=False, last_text='', next_text=''):
    """Function send text to the last subtitle"""
    if not subtitles:
        subtitles = []

    if selected_subtitle and subtitles.index(selected_subtitle):
        history.history_append(subtitles)
        index = subtitles.index(selected_subtitle)
        subtitles[index][2] = next_text
        subtitles[index-1][2] += ' ' + last_text


def set_gap(subtitles=False, position=0.0, gap=0.0):
    """Function to set gap in subtitles"""
    if not subtitles:
        subtitles = []

    for subtitle in subtitles:
        if subtitle[0] > position:
            subtitle[0] += gap
