from captionstransformer import core
from bs4 import BeautifulSoup
import bleach
from datetime import datetime, timedelta


class Reader(core.Reader):
    def text_to_captions(self):
        soup = BeautifulSoup(self.rawcontent, 'html.parser')

        # Check if there's a <SAMI> tag:
        if not soup.sami:
            return False
        else:
            samiparam = str(soup.sami.head.samiparam)
            if 'Metrics {' in samiparam and 'duration: ' in samiparam.split('Metrics {',1)[-1]:
                self.max_duration = int(samiparam.split('Metrics {',1)[-1].split('duration: ',1)[-1].split(';',1)[0])
            else:
                self.max_duration = 5000
            empty_last_time = soup.new_tag("sync", start=str(self.max_duration))
            soup.sami.body.append(empty_last_time)
            prev_line_time = core.get_date(second=0)
            prev_line_text = ''
            for sync in soup.sami.body.find_all('sync'):
                this_line_time = self.get_start(sync)
                linerepr = repr(str(sync.p)[1:].split('<',1)[0].split('>',1)[-1])[1:-1]
                this_line_text = linerepr.replace('<br>', '\n').strip()
                if this_line_text.endswith('\\t'):
                    this_line_text = this_line_text[:-2]
                if this_line_text.endswith('\\n'):
                    this_line_text = this_line_text[:-2]
                if prev_line_text != '':
                    caption = core.Caption()
                    caption.start = prev_line_time
                    caption.end = this_line_time
                    caption.text = prev_line_text
                    self.add_caption(caption)
                prev_line_time = this_line_time
                prev_line_text = this_line_text

        return self.captions

    def get_start(self, text):
        return self.get_raw_time(str(float(text.get('start'))/1000), format="date")

    def get_raw_time(self, utime, format="date"):
        if '.' in utime:
            second_f = float(utime)
            second = int(second_f)
            millisecond = int(1000 * (second_f - second))
        else:
            second = int(utime)
            millisecond = 0
        if format == "date":
            return core.get_date(second=second, millisecond=millisecond)
        else:
            return timedelta(seconds=second, milliseconds=millisecond)


class Writer(core.Writer):
    DOCUMENT_TPL = u"""<SAMI>\n<Head>\n\t<Title></Title>\n\t<SAMIParam>\n\t\tCopyright {}\n\t\tMedia {}\n\t\tMetrics {time:ms; duration: 7200000;}\n\t\tSpec {MSFT:1.0;}\n\t</SAMIParam>\n</Head>\n\n<Body>\n%s</Body>\n</SAMI>"""
    CAPTION_TPL = u"""\t<SYNC Start=%(start)s>\n\t\t<P Class=ENUSCC>%(text)s"""

    def format_time(self, caption):
        """Return start time for the given format"""
        return {'start': self.get_utime(caption.start)}

    def get_utime(self, dt):
        start_milliseconds = ((3600 * dt.hour + 60 * dt.minute + dt.second) * 1000) + (dt.microsecond / 1000)
        return u"%i" % start_milliseconds
