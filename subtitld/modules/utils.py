"""All path definitions for Subtitld"""


def is_float(element: str) -> bool:
    try:
        float(element)
        return True
    except ValueError:
        return False


def get_timeline_time_str(seconds, ms=False):
    """Function to return timecode from seconds"""
    secs = int(seconds % 60)
    mins = int((seconds / 60) % 60)
    hrs = int((seconds / 60) / 60)
    mss = int(round(float('0.' + str(seconds).split('.', 1)[-1]), 3) * 1000)

    if ms:
        if hrs:
            return "{hh:02d}:{mm:02d}:{ss:02d}.{mss:03d}".format(hh=hrs, mm=mins, ss=secs, mss=mss)
        elif mins:
            return "{mm:02d}:{ss:02d}.{mss:03d}".format(mm=mins, ss=secs, mss=mss)
        else:
            return "{ss:02d}.{mss:03d}".format(ss=secs, mss=mss)
    else:
        if hrs:
            return "{hh:02d}:{mm:02d}:{ss:02d}".format(hh=hrs, mm=mins, ss=secs)
        elif mins:
            return "{mm:02d}:{ss:02d}".format(mm=mins, ss=secs)
        else:
            return "{ss:02d}".format(ss=secs)


def convert_ffmpeg_timecode_to_seconds(timecode):
    """Function to convert ffmpeg timecode to seconds"""
    if timecode:
        final_value = float(timecode.split(':')[-1])
        if timecode.count(':') > 2:
            final_value += int(timecode.split(':')[-2]) * 60.0
        if timecode.count(':') > 3:
            final_value += int(timecode.split(':')[-3]) * 3600.0
        if timecode.count(':') > 4:
            final_value += int(timecode.split(':')[-4]) * 3600.0
        return final_value
    else:
        return False
