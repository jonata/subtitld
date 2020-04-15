#!/usr/bin/env python3

from bisect import bisect

def add_subtitle(subtitles=[], position=0.0, duration=5.0, text=''):
    current_index = 0

    subt = [item[0] for item in subtitles]
    index = bisect(subt, position)


    if index and subtitles[index-1][0] + subtitles[index-1][1] > position:
        subtitles[index-1][1] -= (subtitles[index-1][0] + subtitles[index-1][1]) - position

    if len(subtitles) - 1 > index and subtitles[index][0] - position < duration:
        duration = subtitles[index][0] - position

    subtitles.insert(index, [position, duration, text])

    return subtitles[current_index]

def remove_subtitle(subtitles=[], selected_subtitle=False):
    if selected_subtitle:
        subtitles.remove(selected_subtitle)
    return subtitles

def slice_subtitle(subtitles=[], selected_subtitle=False, position=0.0, last_text='', next_text=''):
    if selected_subtitle and position > selected_subtitle[0] and position < (selected_subtitle[0] + selected_subtitle[1]):
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
        index = subtitles.index(selected_subtitle)
        subtitles[index-1][1] = selected_subtitle[0] + selected_subtitle[1] - subtitles[index-1][0]
        subtitles[index-1][2] += ' ' + subtitles[index][2]

        remove_subtitle(subtitles=subtitles, selected_subtitle=subtitles[index])

        return subtitles[index-1]

def merge_next_subtitle(subtitles=[], selected_subtitle=False):
    if selected_subtitle and subtitles.index(selected_subtitle) < len(subtitles) - 1:
        index = subtitles.index(selected_subtitle)
        subtitles[index][1] = subtitles[index+1][0] + subtitles[index+1][1] - selected_subtitle[0]
        subtitles[index][2] += ' ' + subtitles[index+1][2]

        remove_subtitle(subtitles=subtitles, selected_subtitle=subtitles[index+1])

        return subtitles[index]

def next_start_to_current_position(subtitles=[], position=0.0):
    subt = [item[0] for item in subtitles]
    index = bisect(subt, position)
    if index < len(subt) - 1:
        end = subtitles[index][0] + subtitles[index][1]
        subtitles[index][0] = position
        subtitles[index][1] = end - position
    if index -1 < len(subt) - 1 and (subtitles[index-1][0] + subtitles[index-1][1]) > position:
        last_end_to_current_position(subtitles=subtitles, position=position - 0.001)

def last_end_to_current_position(subtitles=[], position=0.0):
    subt = [item[0] for item in subtitles]
    index = bisect(subt, position)
    print(subtitles[index])
    if index -1 < len(subt) - 1:
        subtitles[index-1][1] = position - subtitles[index-1][0]

def send_text_to_next_subtitle(subtitles=[], selected_subtitle=False, last_text='', next_text=''):
    if selected_subtitle and subtitles.index(selected_subtitle) + 1 < len(subtitles):
        index = subtitles.index(selected_subtitle)
        subtitles[index][2] = last_text
        subtitles[index+1][2] = next_text + ' ' + subtitles[index+1][2]

def send_text_to_last_subtitle(subtitles=[], selected_subtitle=False, last_text='', next_text=''):
    if selected_subtitle and subtitles.index(selected_subtitle):
        index = subtitles.index(selected_subtitle)
        subtitles[index][2] = next_text
        subtitles[index-1][2] += ' ' + last_text
