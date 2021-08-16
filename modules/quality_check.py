"""Module to check subtitles quality

"""

def check_subtitle(subtitle=[], settings={}):
    """Function to check individual subtitle"""
    approved = True
    reasons = []
    if subtitle and subtitle[1]:
        if len(subtitle[2].replace('\n', '')) / subtitle[1] > settings.get('reading_speed', 21):
            approved = False
            reasons.append('Reading speed: {ars} characters per second. It should be {rs} per second.'.format(rs=settings.get('reading_speed', 21), ars=round(len(subtitle[2].replace('\n', '')) / subtitle[1], 2)))
        if subtitle[1] < settings.get('minimum_duration', .7):
            approved = False
            reasons.append('The duration of this subtitle, {ad}, is less than the minimum of {d}.'.format(d=settings.get('minimum_duration', .7), ad=round(subtitle[1], 2)))
        if subtitle[1] > settings.get('maximum_duration', 7):
            approved = False
            reasons.append('The duration of this subtitle, {ad}, is more than the maximum of {d}.'.format(d=settings.get('maximum_duration', 7), ad=round(subtitle[1], 2)))
        if len(subtitle[2].split('\n')) > settings.get('maximum_lines', 2):
            approved = False
            reasons.append('There are {al} lines, more than the maximum of {l}.'.format(l=settings.get('maximum_lines', 2), al=round(len(subtitle[2].split('\n')), 2)))
        for line in subtitle[2].split('\n'):
            if len(line) > settings.get('maximum_characters_per_line', 42):
                approved = False
                reasons.append('There are more than {c} characters per line ({ac}).'.format(c=settings.get('maximum_characters_per_line', 42), ac=len(line)))
                break
        if len(subtitle[2].split('\n')) > 1:
            if settings.get('prefer_compact', False):
                if len(subtitle[2].replace('\n', '')) < settings.get('maximum_characters_per_line', 42):
                    approved = False
                    reasons.append('The lines should be joined as there are less than {c} characters in total.'.format(c=settings.get('maximum_characters_per_line', 42)))
            if settings.get('balance_ratio_enabled', False):
                if len(min(subtitle[2].split('\n'), key=len)) < len(max(subtitle[2].split('\n'), key=len))*(settings.get('balance_ratio', 50)/100):
                    approved = False
                    reasons.append('The shortest line length is less than {p}% the largest.'.format(p=settings.get('balance_ratio', 50)))

    return [approved, reasons]
