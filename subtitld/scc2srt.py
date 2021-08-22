import re
import logging
import sys
import os

_ccTxMatrix = dict()

_ccRowTable = {
    0x11, 0x40, 0x5F,
    0x11, 0x60, 0x7F,
    0x12, 0x40, 0x5F,
    0x12, 0x60, 0x7F,
    0x15, 0x40, 0x5F,
    0x15, 0x60, 0x7F,
    0x16, 0x40, 0x5F,
    0x16, 0x60, 0x7F,
    0x17, 0x40, 0x5F,
    0x17, 0x60, 0x7F,
    0x10, 0x40, 0x5F,
    0x13, 0x40, 0x5F,
    0x13, 0x60, 0x7F,
    0x14, 0x40, 0x5F,
    0x14, 0x60, 0x7F
}

tmpMatrix = [0x80, 0x01, 0x02, 0x83, 0x04, 0x85, 0x86, 0x07, 0x08, 0x89, 0x8a, 0x0b, 0x8c, 0x0d, 0x0e, 0x8f,
             0x10, 0x91, 0x92, 0x13, 0x94, 0x15, 0x16, 0x97, 0x98, 0x19, 0x1a, 0x9b, 0x1c, 0x9d, 0x9e, 0x1f,
             0x20, 0xa1, 0xa2, 0x23, 0xa4, 0x25, 0x26, 0xa7, 0xa8, 0x29, 0x2a, 0xab, 0x2c, 0xad, 0xae, 0x2f,
             0xb0, 0x31, 0x32, 0xb3, 0x34, 0xb5, 0xb6, 0x37, 0x38, 0xb9, 0xba, 0x3b, 0xbc, 0x3d, 0x3e, 0xbf,
             0x40, 0xc1, 0xc2, 0x43, 0xc4, 0x45, 0x46, 0xc7, 0xc8, 0x49, 0x4a, 0xcb, 0x4c, 0xcd, 0xce, 0x4f,
             0xd0, 0x51, 0x52, 0xd3, 0x54, 0xd5, 0xd6, 0x57, 0x58, 0xd9, 0xda, 0x5b, 0xdc, 0x5d, 0x5e, 0xdf,
             0xe0, 0x61, 0x62, 0xe3, 0x64, 0xe5, 0xe6, 0x67, 0x68, 0xe9, 0xea, 0x6b, 0xec, 0x6d, 0x6e, 0xef,
             0x70, 0xf1, 0xf2, 0x73, 0xf4, 0x75, 0x76, 0xf7, 0xf8, 0x79, 0x7a, 0xfb, 0x7c, 0xfd, 0xfe, 0x7f]

_specialChars = {
    0xb0: '®',
    0x31: '°',
    0x32: '½',
    0xb3: '¿',
    0xb4: '™',
    0xb5: '¢',
    0xb6: '£',
    0x37: '♪',
    0x38: 'à',
    0xb9: ' ',
    0xba: 'è',
    0x3b: 'â',
    0xbc: 'ê',
    0x3d: 'î',
    0x3e: 'ô',
    0xbf: 'û',
}

_extendedChars = {
    '9220': 'Á',
    '92a1': 'É',
    '92a2': 'Ó',
    '9223': 'Ú',
    '92a4': 'Ü',
    '9225': 'ü',
    '9226': '‘',
    '92a7': '¡',
    '92a8': '*',
    '9229': '’',
    '922a': '—',
    '92ab': '©',
    '922c': '℠',
    '92ad': '•',
    '92ae': '“',
    '922f': '”',
    '92b0': 'À',
    '9231': 'Â',
    '9232': 'Ç',
    '92b3': 'È',
    '9234': 'Ê',
    '92b5': 'Ë',
    '92b6': 'ë',
    '9237': 'Î',
    '9238': 'Ï',
    '92b9': 'ï',
    '92ba': 'Ô',
    '923b': 'Ù',
    '92bc': 'ù',
    '923d': 'Û',
    '923e': '«',
    '92bf': '»',
    '1320': 'Ã',
    '13a1': 'ã',
    '13a2': 'Í',
    '1323': 'Ì',
    '13a4': 'ì',
    '1325': 'Ò',
    '1326': 'ò',
    '13a7': 'Õ',
    '13a8': 'õ',
    '1329': '{',
    '132a': '}',
    '13ab': '\\',
    '132c': '^',
    '13ad': '_',
    '13ae': '¦',
    '132f': '~',
    '13b0': 'Ä',
    '1331': 'ä',
    '1332': 'Ö',
    '13b3': 'ö',
    '1334': 'ß',
    '13b5': '¥',
    '13b6': '¤',
    '1337': '|',
    '1338': 'Å',
    '13b9': 'å',
    '13ba': 'Ø',
    '133b': 'ø',
    '13bc': '┌',
    '133d': '┐',
    '133e': '└',
    '13bf': '┘',
}


class SCCItem(object):
    start_time = None
    end_time = None
    text = None


def _milliseconds_to_smtpe(time: int):
    hoursMs = int(time / 3600000) * 3600000
    minutesMs = int((time - hoursMs) / 60000) * 60000
    secondsMs = int((time - (hoursMs + minutesMs)) / 1000) * 1000
    millseconds = int(time - (hoursMs + minutesMs + secondsMs))

    return '{0:02d}:{1:02d}:{2:02d}.{3:03d}'.format(int(hoursMs / 3600000), int(minutesMs / 60000), int(secondsMs / 1000), int(millseconds))


def _milliseconds_to_smtpe2(time: int, fps=29.976):
    hoursMs = int(time / 3600000) * 3600000
    minutesMs = int((time - hoursMs) / 60000) * 60000
    secondsMs = int((time - (hoursMs + minutesMs)) / 1000) * 1000
    millseconds = int(time - (hoursMs + minutesMs + secondsMs))

    return '{0:02d}:{1:02d}:{2:02d}:{3:02d}'.format(int(hoursMs / 3600000), int(minutesMs / 60000), int(secondsMs / 1000), int((millseconds / 1008 * fps)))


def _debug_render_command(control_codes):
    command = None
    row = 0

    row_sequence = [0x11, 0x11, 0x12, 0x12, 0x15, 0x15, 0x16, 0x16, 0x17, 0x17, 0x10, 0x13, 0x13, 0x14, 0x14, 0x00]

    if (control_codes[0] < 0x13 and control_codes[0] > 0x14):
        if (control_codes[1] >= 0x40 and control_codes[1] <= 0x5F):
            idx = (row_sequence[0::2].index(control_codes[0]))
            row = (idx * 2) + 1
        if (control_codes[1] >= 0x60 and control_codes[1] <= 0x7F):
            idx = (row_sequence[1::2].index(control_codes[0]))
            row = (idx + 1) * 2
    if (control_codes[0] == 0x13 or control_codes[0] == 0x14):
        if (control_codes[1] >= 0x40 and control_codes[1] <= 0x5F):
            idx = (row_sequence[1::2].index(control_codes[0]))
            row = (idx + 1) * 2
        if (control_codes[1] >= 0x60 and control_codes[1] <= 0x7F):
            idx = (row_sequence[0::2].index(control_codes[0]))
            row = (idx * 2) + 1

    if control_codes[0] == 0x11 and (0x20 >= control_codes[1] <= 0x2F):

        if control_codes[1] == 0x20 or control_codes[1] == 0x21:
            command = "MRC - White"
        elif control_codes[1] == 0x22 or control_codes[1] == 0x23:
            command = "MRC - Green"
        elif control_codes[1] == 0x24 or control_codes[1] == 0x25:
            command = "MRC - Blue"
        elif control_codes[1] == 0x26 or control_codes[1] == 0x27:
            command = "MRC - Cyan"
        elif control_codes[1] == 0x28 or control_codes[1] == 0x29:
            command = "MRC - Red"
        elif control_codes[1] == 0x2A or control_codes[1] == 0x2B:
            command = "MRC - Yellow"
        elif control_codes[1] == 0x2C or control_codes[1] == 0x2D:
            command = "MRC - Magenta"
        elif control_codes[1] == 0x2E:
            command = "MRC - Italic"

        if (control_codes[1] & 1) == 1:
            command += ' Underline'

    if control_codes[0] == 0x11 and control_codes[1] in _extendedChars:
        command = "EXT - (Extended Character)"
    if control_codes[0] >= 0x11 and ((control_codes[1] >= 0xB0 and control_codes[1] <= 0xBF) or (control_codes[1] >= 0x30 and control_codes[1] <= 0x3F)):
        command = "SPC - (Special Character)"
    elif (control_codes[0] >= 0x11 and control_codes[0] <= 0x17) and ((control_codes[1] >= 0x60 and control_codes[1] <= 0x6F) or (control_codes[1] >= 0x40 and control_codes[1] <= 0x4F)):
        command = "PAC - (Underline) Row [{}]".format(row)
    elif (control_codes[0] >= 0x11 and control_codes[0] <= 0x17) and ((control_codes[1] >= 0x50 and control_codes[1] <= 0x5F) or (control_codes[1] >= 0x70 and control_codes[1] <= 0x7F)):
        command = "PAC - (Indent) Row [{}]".format(row)
    elif control_codes[0] == 0x14:
        if control_codes[1] == 0x20:
            command = "RCL - Resume caption loading"
        elif control_codes[1] == 0x21:
            command = "RB - Backspace"
        elif control_codes[1] == 0x22:
            command = "AOF - Alarm Off"
        elif control_codes[1] == 0x23:
            command = "AON - Alarm On"
        elif control_codes[1] == 0x24:
            command = "DER - Delete to end of row"
        elif control_codes[1] == 0x25:
            command = "RU2 - Roll-up captions-2"
        elif control_codes[1] == 0x26:
            command = "RU3 - Roll-up captions-3"
        elif control_codes[1] == 0x27:
            command = "RU4 - Roll-up captions-4"
        elif control_codes[1] == 0x28:
            command = "FON - Flash On"
        elif control_codes[1] == 0x29:
            command = "RDC - Resume direct captioning"
        elif control_codes[1] == 0x2A:
            command = "TR  - Text restart"
        elif control_codes[1] == 0x2B:
            command = "RTD - Resume Text restart"
        elif control_codes[1] == 0x2C:
            command = "EDM - Erase Display Memory"
        elif control_codes[1] == 0x2D:
            command = "CR - Carriage Return"
        elif control_codes[1] == 0x2E:
            command = "ENM - Erase Non-Display Memory"
        elif control_codes[1] == 0x2F:
            command = "EOC - End Of Caption (flip-memory)"
        elif control_codes[1] == 0x21:
            command = "TO1 - Tab Offset 1 Column"
        elif control_codes[1] == 0x22:
            command = "TO1 - Tab Offset 2 Column"
        elif control_codes[1] == 0x23:
            command = "TO2 - Tab Offset 3 Column"

    if command:
        return command

    return command


def parse(file: str, logger: logging.Logger = None, start_offset=0):

    if logger:
        logger.debug("[{}]".format(file))

    for i in range(128):
        _ccTxMatrix[tmpMatrix[i]] = i

    channelOne = False
    current_buffer = ""
    italics = False
    underline = False
    items = []
    end_of_caption = False
    last_caption_item = None
    max_popup_time = 5000
    roll_up_mode = False
    roll_up_start = None
    roll_up_end = None

    with open(file, 'r') as file:
        for line in file:
            if len(line.strip()) > 0:

                line = line.replace("\n", "")
                result = re.match("(.*)\t(.*)", line)

                if result:
                    critera = result.groups(1)[0]

                    smpteTokens = re.match("([0-9*]{2}):([0-9*]{2}):([0-9*]{2})[:;]*([0-9*]{2})", critera)

                    is_drop_frame = ';' in critera

                    if smpteTokens:

                        # parse the line time
                        time_stamp = smpteTokens.groups(1)

                        # assume base time of 01:00:00,000
                        line_control_time = (int(time_stamp[0]) * 3600 + int(time_stamp[1]) * 60 + int(time_stamp[2]) + (float(time_stamp[3]) / 29.97))
                        #line_control_time = 0

                        # create token list of control codes
                        tokens = result.groups(2)[1].split(' ')

                        # create list of control coders
                        codes = [f for f in tokens if len(f) > 0]

                        frame_number = 0

                        for idx, sample in enumerate(codes):


                            frame_number+=1

                            if is_drop_frame:
                                seconds_per_timestamp_second = 1.0
                            else: # non drop frame
                                seconds_per_timestamp_second = 30.0 / 29.97

                            sampleTime = (((line_control_time + (frame_number * ((1/29.97)))) - start_offset) * seconds_per_timestamp_second)

                            # skip duplicate commands
                            if (idx < len(codes)-1 and codes[idx+1] == sample):
                                continue

                            # convert hex control codes to a number
                            cc_raw_code1 = int(sample[0:2], 16)
                            cc_raw_code2 = int(sample[-2:], 16)

                            # convert raw control codes
                            cc_code1 = _ccTxMatrix[cc_raw_code1]
                            cc_code2 = _ccTxMatrix[cc_raw_code2]

                            # detect if rollup mode (first code is rollup command)
                            if frame_number == 1 and not roll_up_mode and cc_code1 == 0x14 and (cc_code2 == 0x25 or cc_code2 == 0x26 or cc_code2 == 0x27):
                                roll_up_mode = True

                            # skip time stamps before the 01:00:00,000 mark
                            #if (sampleTime < 0):
                            #    continue

                            if logger:
                                _log_caption_details(logger, sampleTime, cc_code1, cc_code2, sample)

                            # EDM - Erase Display Memory or ENM - Erase Non-Display Memory
                            if not(roll_up_mode) and len(current_buffer) > 0 and cc_code1 == 0x14 and (cc_code2 == 0x2c or cc_code2 == 0x2f) and last_caption_item:
                                last_caption_item.end_time = sampleTime * 1000

                                if (last_caption_item.end_time - last_caption_item.start_time > max_popup_time):
                                    end_time = (min(len(last_caption_item.text) * 150, max_popup_time))
                                    last_caption_item.end_time = last_caption_item.start_time + end_time

                                if logger: _log_caption_item(logger, sampleTime, last_caption_item)
                                last_caption_item = None

                            # erase display memory - EOC - End Of Caption (flip-memory) / CR - Carriage Return
                            if not roll_up_mode and cc_code1 == 0x14 and cc_code2 == 0x2f:
                                end_of_caption = True

                            # Rollup command
                            if roll_up_mode and cc_code1 == 0x14 and (cc_code2 == 0x25 or cc_code2 == 0x26 or cc_code2 == 0x27):
                                end_of_caption = True

                            # [CR - Carriage Return]
                            if roll_up_mode and cc_code1 == 0x14 and cc_code2 == 0x2d:
                                roll_up_start = sampleTime

                            if 0x10 <= cc_code1 <= 0x14:

                                channelOne = True

                                if (cc_code1 >= 0x11 and cc_code1 <= 0x17) and ((cc_code2 >= 0x60 and cc_code2 <= 0x6F) or (cc_code2 >= 0x40 and cc_code2 <= 0x4F)):
                                    # If the least significant bit of a Preamble Address Code or of a color or italics Mid-Row Code is a 1 (high), un-derlining is turned on
                                    if not underline and (cc_code2 & 1) == 1:
                                        current_buffer += "<u>"
                                        underline = True
                                    continue
                                elif (cc_code1 >= 0x11 and cc_code1 <= 0x17) and ((cc_code2 >= 0x50 and cc_code2 <= 0x5F) or (cc_code2 >= 0x70 and cc_code2 <= 0x7F)):
                                    # indent
                                    if current_buffer and current_buffer[-1:] != '\n':
                                        current_buffer += '\n'
                                    continue

                                if cc_code1 == 0x11 and (cc_code2 >= 0x20 and cc_code2 <= 0x2F):
                                    # Any color Mid-Row Code will turn off italics.
                                    if italics:
                                        current_buffer += "</i> "
                                        italics = False

                                    # un-derlining is turned on if color or italics Mid-Row Code is a 1 (high)
                                    if not underline and (cc_code2 & 1) == 1:
                                        current_buffer += "<u>"
                                        underline = True

                                    if cc_code1 == 0x11 and cc_code2 == 0x2E and not italics:
                                        current_buffer += "<i>"
                                        italics = True

                                if cc_code1 == 0x14 and (cc_code2 == 0x28 or cc_code2 == 0x2D):
                                    # Flash On
                                    if current_buffer and current_buffer[-1:] != '\n':
                                        current_buffer += '\n'
                                elif cc_code1 == 0x11 and cc_raw_code2 in _specialChars:
                                    current_buffer += _specialChars[cc_raw_code2]
                                elif cc_code1 == 0x12 and cc_raw_code2 in _extendedChars:
                                    current_buffer += _extendedChars[cc_raw_code2]
                                elif end_of_caption:

                                    if italics:
                                        current_buffer += "</i> "

                                    if underline:
                                        current_buffer += "</u> "

                                    if current_buffer:

                                        item = SCCItem()
                                        item.end_time = -1
                                        item.text = current_buffer

                                        if roll_up_mode:
                                            item.start_time = roll_up_start * 1000
                                            item.end_time = sampleTime * 1000

                                            if (item.end_time - item.start_time) > max_popup_time:
                                                end_time = (min(len(item.text) * 150, max_popup_time))
                                                item.end_time = item.start_time + end_time

                                            if logger: _log_caption_item(logger, sampleTime, item)
                                        else:
                                            item.start_time = sampleTime * 1000

                                        items.append(item)
                                        last_caption_item = item

                                    current_buffer = ""
                                    italics = False
                                    underline = False
                                    end_of_caption = False

                            elif 0x20 <= cc_code1 <= 0x7F and channelOne:

                                current_buffer += chr(cc_code1)

                                if 0x20 <= cc_code2 <= 0x7F:
                                    current_buffer += chr(cc_code2)

                            elif 0x18 <= cc_code1 <= 0x1F:
                                channelOne = False

    if last_caption_item and last_caption_item.end_time == -1:
        last_caption_item.end_time = sampleTime * 1000
        if logger: _log_caption_item(logger, sampleTime, last_caption_item)

    return items


def _log_caption_details(logger, sampleTime, cc_code1, cc_code2, sample, fps=29.976):

    smpte = _milliseconds_to_smtpe(sampleTime * 1000)
    cmd = _debug_render_command([cc_code1, cc_code2])

    frameTime = _milliseconds_to_smtpe2(sampleTime * 1000, fps)

    if cmd:
        logger.debug("[{5}] [{0}] [{4}] [{1:02x}] [{2:02x}] [{3}]".format(smpte, cc_code1, cc_code2, cmd, sample, frameTime))
    else:
        try:
            logger.debug("[{6}] [{0}] [{1}] [{2:002x}] [{3:002x}] [{4}] [{5}]".format(smpte, sample, cc_code1, cc_code2, chr(cc_code1), chr(cc_code2), frameTime))
        except:
            logger.debug("[{5}] {0},{4},{1},{2},{3}".format(smpte, cc_code1, cc_code2, cmd, sample, frameTime))


def _log_caption_item(logger: object, sampleTime: float, captionItem: object, fps=29.976):

    frameTime = _milliseconds_to_smtpe2(sampleTime * 1000, fps)

    logger.debug("[{0}] [{1}] [{2}] => [{3}]".format(_milliseconds_to_smtpe2(captionItem.start_time),
                                                                   _milliseconds_to_smtpe2(captionItem.end_time),
                                                                   captionItem.text.replace('\n', '<br/>'),
                                                                   frameTime))


def write_srt(items: SCCItem, alignment_padding: int, output_file: str):
    with open(output_file, "w+") as f:
        for idx, val in enumerate(items):
            val.start_time += alignment_padding
            val.end_time += alignment_padding

            f.write('{}\n'.format(str(idx + 1)))
            f.write('{} --> {}\n'.format(_milliseconds_to_smtpe(val.start_time), _milliseconds_to_smtpe(val.end_time)))
            f.write('{}\n'.format(val.text))
            f.write('\n')

def get_list_of_captions(input_file):
    items = parse(input_file)
    #alignment_padding = 0
    final_lines = []
    for idx, val in enumerate(items):
        #val.start_time += alignment_padding
        #val.end_time += alignment_padding
        final_lines.append([(val.start_time/1000.0), ((val.end_time/1000.0) - (val.start_time/1000.0)), val.text])
    return final_lines

def convert(input_file: str, output_file: str, alignment_padding=0, logger: logging.Logger = None):

    items = parse(input_file, logger,  )

    write_srt(items, alignment_padding, output_file)
