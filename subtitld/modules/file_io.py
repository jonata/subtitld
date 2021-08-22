"""File input and output functions.

"""

import os
import datetime
import html

from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import QThread, pyqtSignal

from scenedetect.video_manager import VideoManager
from scenedetect.scene_manager import SceneManager
from scenedetect.stats_manager import StatsManager
from scenedetect.detectors import ContentDetector

import numpy
import pycaption
from pycaption.exceptions import CaptionReadSyntaxError, CaptionReadNoCaptions
import chardet
import pysubs2
from cleantext import clean
import captionstransformer
from subtitld import scc2srt, timecode

from subtitld.modules import waveform
from subtitld.modules import usf
from subtitld.modules.paths import LIST_OF_SUPPORTED_SUBTITLE_EXTENSIONS, LIST_OF_SUPPORTED_VIDEO_EXTENSIONS, REAL_PATH_HOME

list_of_supported_subtitle_extensions = []
for exttype in LIST_OF_SUPPORTED_SUBTITLE_EXTENSIONS:
    for ext in LIST_OF_SUPPORTED_SUBTITLE_EXTENSIONS[exttype]['extensions']:
        list_of_supported_subtitle_extensions.append(ext)


class ThreadExtractSceneTimePositions(QThread):
    """Thread to extract time positions of scenes"""
    command = pyqtSignal(list)
    filepath = ''

    def run(self):
        """Run function of extract time positions thread"""
        if self.filepath:
            result = []
            try:
                video_manager = VideoManager([self.filepath])
                stats_manager = StatsManager()
                scene_manager = SceneManager(stats_manager)
                scene_manager.add_detector(ContentDetector())
                base_timecode = video_manager.get_base_timecode()
                try:
                    video_manager.set_downscale_factor()
                    video_manager.start()
                    scene_manager.detect_scenes(frame_source=video_manager, show_progress=False)
                    scene_list = scene_manager.get_scene_list(base_timecode)
                    for _, scene in enumerate(scene_list):
                        result.append(scene[0].get_seconds())
                finally:
                    video_manager.release()
            except Exception:
                pass
            self.command.emit(result)


class ThreadExtractWaveform(QThread):
    """Thread to extract waveform"""
    command = pyqtSignal(numpy.ndarray)
    filepath = ''
    audio = ''
    duration = ''
    width = ''
    height = ''

    def run(self):
        """Run function of thread to extract waveform"""
        if self.filepath:
            result = waveform.ffmpeg_load_audio(filepath=self.filepath)
            self.command.emit(result)


def load(self):
    """Load thread objects"""
    def thread_extract_waveform_ended(command):
        self.video_metadata['audio'] = command
        self.timeline.zoom_update_waveform(self)
        self.videoinfo_label.setText(self.tr('Audio ffmpeg_extract_subtitleed'))

    self.thread_extract_waveform = ThreadExtractWaveform(self)
    self.thread_extract_waveform.command.connect(thread_extract_waveform_ended)

    def thread_extract_scene_time_positions_ended(command):
        self.video_metadata['scenes'] = command

    self.thread_extract_scene_time_positions = ThreadExtractSceneTimePositions(self)
    self.thread_extract_scene_time_positions.command.connect(thread_extract_scene_time_positions_ended)


def open_filepath(self, files_to_open=False, update_interface=False):
    """Open subtitle or video and performs some checks"""
    supported_subtitle_files = self.tr('Subtitle files') + ' ({})'.format(" ".join(["*.{}".format(fo) for fo in list_of_supported_subtitle_extensions]))
    supported_video_files = self.tr('Video files') + ' ({})'.format(" ".join(["*{}".format(fo) for fo in LIST_OF_SUPPORTED_VIDEO_EXTENSIONS]))

    if not files_to_open:
        files_to_open = [QFileDialog.getOpenFileName(parent=self.parent(), caption=self.tr('Select the video or subtitle file'), directory=REAL_PATH_HOME, filter=supported_subtitle_files + ';;' + supported_video_files)[0]]

    for filepath in files_to_open:
        if os.path.isfile(filepath):
            if not self.subtitles_list and filepath.lower().endswith(tuple(list_of_supported_subtitle_extensions)):
                self.subtitles_list, self.format_to_save = process_subtitles_file(filepath)
                self.actual_subtitle_file = filepath

            elif not self.video_metadata and filepath.lower().endswith(LIST_OF_SUPPORTED_VIDEO_EXTENSIONS):
                self.video_metadata = process_video_file(filepath)

            if not self.video_metadata and self.subtitles_list:
                for filename in os.listdir(os.path.dirname(filepath)):
                    if filename.rsplit('.', 1)[0] == os.path.basename(filepath).rsplit('.', 1)[0] and filename.endswith(LIST_OF_SUPPORTED_VIDEO_EXTENSIONS):
                        self.video_metadata = process_video_file(os.path.join(os.path.dirname(filepath), filename))
                        break

            elif self.video_metadata and not self.subtitles_list:
                for filename in os.listdir(os.path.dirname(filepath)):
                    if filename.rsplit('.', 1)[0] == os.path.basename(filepath).rsplit('.', 1)[0] and filename.endswith(tuple(list_of_supported_subtitle_extensions)):
                        self.subtitles_list, self.format_to_save = process_subtitles_file(os.path.join(os.path.dirname(filepath), filename))
                        self.actual_subtitle_file = os.path.join(os.path.dirname(filepath), filename)
                        break

            if not self.video_metadata:
                filepath = QFileDialog.getOpenFileName(parent=self.parent(), caption=self.tr('Select the video file'), directory=REAL_PATH_HOME, filter=supported_video_files)[0]
                if filepath and os.path.isfile(filepath) and filepath.lower().endswith(LIST_OF_SUPPORTED_VIDEO_EXTENSIONS):
                    self.video_metadata = process_video_file(filepath)

    if self.video_metadata:
        self.actual_video_file = self.video_metadata['filepath']
        if self.video_metadata['audio_is_present']:
            self.thread_extract_waveform.filepath = self.video_metadata['filepath']
            self.thread_extract_waveform.start()
            self.videoinfo_label.setText(self.tr('Extracting audio...'))
        #self.thread_extract_scene_time_positions.filepath = self.video_metadata['filepath']
        #self.thread_extract_scene_time_positions.start()
        self.player.update(self)
        self.player_widget.loadfile(self.video_metadata['filepath'])
        self.player.resize_player_widget(self)
        if not self.actual_subtitle_file:
            if self.video_metadata.get('subttiles', ''):
                self.subtitles_list, self.format_to_save = process_subtitles_file(self.video_metadata['subttiles'])
        self.subtitleslist.update_subtitles_list_widget(self)
        self.settings['recent_files'][self.actual_subtitle_file] = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        self.autosave_timer.start()

        if update_interface:
            self.timeline.update_timeline(self)
            self.startscreen.hide(self)
            self.playercontrols.show(self)
            self.properties.show(self)
            self.subtitleslist.show(self)
            self.global_subtitlesvideo_panel.hide_global_subtitlesvideo_panel(self)
            self.global_properties_panel.hide_global_properties_panel(self)

    self.global_subtitlesvideo_panel.update_global_subtitlesvideo_save_as_combobox(self)

    if os.path.isfile(os.path.join(os.path.dirname(self.actual_subtitle_file), os.path.basename(self.actual_subtitle_file).rsplit('.', 1)[0] + '.usf')):
        self.format_usf_present = True
    else:
        self.format_usf_present = False

    self.subtitleslist.update_subtitleslist_format_label(self)


def process_subtitles_file(subtitle_file=False, subtitle_format='SRT'):
    """Definition to process subtitle file. It returns a dict with the subtitles."""
    final_subtitles = []

    if subtitle_file and os.path.isfile(subtitle_file):
        if subtitle_file.lower().endswith(('.srt')):
            enc = chardet.detect(open(subtitle_file, 'rb').read())['encoding']
            with open(subtitle_file, mode='rb') as srt_file:
                srt_content = srt_file.read().decode(enc, 'ignore')

                if ' -> ' in srt_content:
                    srt_content = srt_content.replace(' -> ', ' --> ')

                srt_reader = pycaption.SRTReader().read(srt_content)
                languages = srt_reader.get_languages()
                language = languages[0]
                captions = srt_reader.get_captions(language)
                for caption in captions:
                    final_subtitles.append([caption.start/1000000, (caption.end/1000000) - caption.start/1000000, caption.get_text()])

        elif subtitle_file.lower().endswith(('.vtt', '.webvtt')):
            subtitle_format = 'VTT'
            with open(subtitle_file, encoding='utf-8') as vtt_file:
                try:
                    vtt_reader = pycaption.WebVTTReader().read(vtt_file.read())
                    languages = vtt_reader.get_languages()
                    language = languages[0]
                    captions = vtt_reader.get_captions(language)
                    for caption in captions:
                        final_subtitles.append([caption.start/1000000, (caption.end/1000000) - caption.start/1000000, caption.get_text()])
                except CaptionReadSyntaxError:
                    with open(subtitle_file, encoding='utf-8') as fileobj:
                        subfile = pysubs2.SSAFile.from_string(fileobj.read())

                    for event in subfile.events:
                        start = event.start / 1000.0
                        duration = event.duration / 1000.0
                        text = event.plaintext
                        final_subtitles.append([start, duration, text])
                except CaptionReadNoCaptions:
                    pass

                    # error_message = QMessageBox()
                    # error_message.setWindowTitle(self.tr('There is a problem with this file and can not be opened.'))

        elif subtitle_file.lower().endswith(('.ttml', '.dfxp')):
            subtitle_format = 'DFXP'
            with open(subtitle_file, encoding='utf-8') as dfxp_file:
                dfxp_reader = pycaption.DFXPReader().read(dfxp_file.read())
                languages = dfxp_reader.get_languages()
                language = languages[0]
                captions = dfxp_reader.get_captions(language)
                for caption in captions:
                    final_subtitles.append([caption.start/1000000, (caption.end/1000000) - caption.start/1000000, caption.get_text()])

        elif subtitle_file.lower().endswith(('.smi', '.sami')):
            subtitle_format = 'SAMI'
            with open(subtitle_file, encoding='utf-8') as sami_file:
                sami_reader = pycaption.SAMIReader().read(sami_file.read())
                languages = sami_reader.get_languages()
                language = languages[0]
                captions = sami_reader.get_captions(language)
                for caption in captions:
                    final_subtitles.append([caption.start/1000000, (caption.end/1000000) - caption.start/1000000, caption.get_text()])

        elif subtitle_file.lower().endswith(('.sbv')):
            subtitle_format = 'SBV'
            with open(subtitle_file, encoding='utf-8') as sbv_file:
                from captionstransformer.sbv import Reader
                captions = Reader(sbv_file).read()
                for caption in captions:
                    final_subtitles.append([(caption.start-datetime.datetime(1900, 1, 1)).total_seconds(), caption.duration.total_seconds(), caption.text.strip()])

        elif subtitle_file.lower().endswith(('.xml')):
            subtitle_format = 'XML'
            if '<transcript>' in open(subtitle_file).read():
                with open(subtitle_file, encoding='utf-8') as xml_file:
                    captions = captionstransformer.transcript.Reader(xml_file).read()
                    for caption in captions:
                        final_subtitles.append([(caption.start-datetime.datetime(1900, 1, 1)).total_seconds(), caption.duration.total_seconds(), html.unescape(caption.text)])

        elif subtitle_file.lower().endswith(('.ass', '.ssa', '.sub')):
            if subtitle_file.lower().endswith(('.ass', '.ssa')):
                subtitle_format = 'ASS'
                with open(subtitle_file, encoding='utf-8') as fileobj:
                    subfile = pysubs2.SSAFile.from_string(fileobj.read())
            elif subtitle_file.lower().endswith(('.sub')):
                subtitle_format = 'SUB'
                enc = chardet.detect(open(subtitle_file, 'rb').read())['encoding']
                subfile = pysubs2.SSAFile.from_string(open(subtitle_file, mode='rb').read().decode(enc, 'ignore'))

            for event in subfile.events:
                start = event.start / 1000.0
                duration = event.duration / 1000.0
                text = event.plaintext
                final_subtitles.append([start, duration, text])

        elif subtitle_file.lower().endswith(('.scc')):
            subtitle_format = 'SCC'
            final_subtitles = scc2srt.get_list_of_captions(subtitle_file)

        elif subtitle_file.lower().endswith(('.usf')):
            subtitle_format = 'USF'
            final_subtitles = usf.USFReader().read(open(subtitle_file).read())

    return final_subtitles, subtitle_format


def process_video_file(video_file=False):
    """Function to process video file. It returns a dict with video properties."""
    video_metadata = {}
    json_result = waveform.ffmpeg_load_metadata(video_file)
    video_metadata['audio'] = False
    video_metadata['audio_is_present'] = False
    video_metadata['waveform'] = {}
    video_metadata['duration'] = float(json_result.get('format', {}).get('duration', '0.01'))
    for stream in json_result.get('streams', []):
        if stream.get('codec_type', '') == 'video' and not stream.get('codec_name', 'png') in ['png', 'mjpeg']:
            video_metadata['width'] = int(stream.get('width', 640))
            video_metadata['height'] = int(stream.get('height', 480))
            video_metadata['framerate'] = int(stream.get('r_frame_rate', '1/30').split('/', 1)[0])/int(stream.get('r_frame_rate', '1/30').split('/', 1)[-1])
        elif stream.get('codec_type', '') in ['subtitle'] and not video_metadata.get('subttiles', False):
            video_metadata['subttiles'] = waveform.ffmpeg_extract_subtitle(video_file, stream.get('index', 2))
            # TODO: select what language if multiple embedded subtitles
        elif stream.get('codec_type', '') in ['audio']:
            video_metadata['audio_is_present'] = True
    video_metadata['filepath'] = video_file
    video_metadata['scenes'] = []

    return video_metadata


def import_file(filename=False, subtitle_format=False): #, fit_to_length=False, length=.01, distribute_fixed_duration=False):
    """Function to import file into the subtitle project."""
    final_subtitles = []
    if filename:
        if filename.lower().endswith(('.txt')):
            subtitle_format = 'TXT'
            with open(filename) as txt_file:
                # clean("some input",
                #     fix_unicode=True,               # fix various unicode errors
                #     to_ascii=True,                  # transliterate to closest ASCII representation
                #     lower=True,                     # lowercase text
                #     no_line_breaks=False,           # fully strip line breaks as opposed to only normalizing them
                #     no_urls=False,                  # replace all URLs with a special token
                #     no_emails=False,                # replace all email addresses with a special token
                #     no_phone_numbers=False,         # replace all phone numbers with a special token
                #     no_numbers=False,               # replace all numbers with a special token
                #     no_digits=False,                # replace all digits with a special token
                #     no_currency_symbols=False,      # replace all currency symbols with a special token
                #     no_punct=False,                 # fully remove punctuation
                #     replace_with_url="<URL>",
                #     replace_with_email="<EMAIL>",
                #     replace_with_phone_number="<PHONE>",
                #     replace_with_number="<NUMBER>",
                # replace_with_digit="0",
                # replace_with_currency_symbol="<CUR>",
                # lang="en"                       # set to 'de' for German special handling
                # )

                #txt_content = clean(txt_file.read())
                txt_content = txt_file.read()
                pos = 0.0
                for phrase in txt_content.split('. '):
                    final_subtitles.append([pos, 5.0, phrase + '.'])
                    pos += 5.0
        elif filename.lower().endswith(('.srt')):
            subtitle_format = 'SRT'
            final_subtitles += process_subtitles_file(subtitle_file=filename, subtitle_format=subtitle_format)[0]

    return final_subtitles, subtitle_format


def export_file(filename=False, subtitles_list=False, export_format='TXT', options=False):
    """Function to export file. A filepath and a subtitle dict is given."""
    if subtitles_list and filename:
        if export_format in ['.txt']:
            final_txt = ''
            for sub in subtitles_list:
                final_txt += sub[2].replace('\n', ' ') + ' '
            if options:
                if options.get('new_line', False):
                    final_txt = final_txt.replace('. ', '.\n')
                    final_txt = final_txt.replace('! ', '!\n')
                    final_txt = final_txt.replace('? ', '?\n')
            with open(filename, mode='w', encoding='utf-8') as txt_file:
                txt_file.write(final_txt)
        elif export_format in ['.kdenlive']:
            final_xml = '''<?xml version='1.0' encoding='utf-8'?><mlt LC_NUMERIC="C" producer="main_bin" version="6.26.1" root="/home/jonata"><profile frame_rate_num="25" sample_aspect_num="1" display_aspect_den="9" colorspace="709" progressive="1" description="HD 1080p 25 fps" display_aspect_num="16" frame_rate_den="1" width="1920" height="1080" sample_aspect_den="1"/>'''

            i = 0
            for sub in subtitles_list:
                final_xml += '''<producer id="producer{i}" in="{zerotime}" out="{out}">
                                <property name="length">{length}</property>
                                <property name="eof">pause</property>
                                <property name="resource"/>
                                <property name="progressive">1</property>
                                <property name="aspect_ratio">1</property>
                                <property name="seekable">1</property>
                                <property name="mlt_service">kdenlivetitle</property>
                                <property name="kdenlive:duration">125</property>
                                <property name="kdenlive:clipname">{clipname}</property>
                                <property name="xmldata">&lt;kdenlivetitle duration="125" LC_NUMERIC="C" width="1920" height="1080" out="124"> &lt;item type="QGraphicsTextItem" z-index="0"> &lt;position x="784" y="910"> &lt;transform>1,0,0,0,1,0,0,0,1&lt;/transform> &lt;/position>
                                &lt;content shadow="0;#64000000;3;3;3" font-underline="0" box-height="62" font-outline-color="0,0,0,255" font="Ubuntu" letter-spacing="0" font-pixel-size="54" font-italic="0" typewriter="0;2;1;0;0" alignment="1" font-weight="50" font-outline="0"
                                box-width="351.719" font-color="255,255,255,255">{content}&lt;/content> &lt;/item> &lt;startviewport rect="0,0,1920,1080"/> &lt;endviewport rect="0,0,1920,1080"/> &lt;background color="0,0,0,0"/> &lt;/kdenlivetitle>
                                </property>
                                <property name="kdenlive:folderid">-1</property>
                                <property name="kdenlive:id">{id}</property>
                                <property name="force_reload">0</property>
                                <property name="meta.media.width">1920</property>
                                <property name="meta.media.height">1080</property>
                            </producer>'''.format(i=i, id=i+2, length=int(sub[1]*25), clipname='Subtitle {i}'.format(i=i), content=sub[2], zerotime=str(timecode.Timecode('1000', start_seconds=0.001, fractional=True)), out=str(timecode.Timecode('1000', start_seconds=sub[1], fractional=True)))
                i += 1

            final_xml += '''<playlist id="main_bin">
                            <property name="kdenlive:docproperties.activeTrack">2</property>
                            <property name="kdenlive:docproperties.audioChannels">2</property>
                            <property name="kdenlive:docproperties.audioTarget">-1</property>
                            <property name="kdenlive:docproperties.disablepreview">0</property>
                            <property name="kdenlive:docproperties.documentid">1621801540856</property>
                            <property name="kdenlive:docproperties.enableTimelineZone">0</property>
                            <property name="kdenlive:docproperties.enableexternalproxy">0</property>
                            <property name="kdenlive:docproperties.enableproxy">0</property>
                            <property name="kdenlive:docproperties.externalproxyparams">../Sub;;S03.MP4;../Clip;;.MXF</property>
                            <property name="kdenlive:docproperties.generateimageproxy">0</property>
                            <property name="kdenlive:docproperties.generateproxy">0</property>
                            <property name="kdenlive:docproperties.groups">[ ]
                            </property>
                            <property name="kdenlive:docproperties.kdenliveversion">21.04.0</property>
                            <property name="kdenlive:docproperties.position">372</property>
                            <property name="kdenlive:docproperties.previewextension"/>
                            <property name="kdenlive:docproperties.previewparameters"/>
                            <property name="kdenlive:docproperties.profile">atsc_1080p_25</property>
                            <property name="kdenlive:docproperties.proxyextension"/>
                            <property name="kdenlive:docproperties.proxyimageminsize">2000</property>
                            <property name="kdenlive:docproperties.proxyimagesize">800</property>
                            <property name="kdenlive:docproperties.proxyminsize">1000</property>
                            <property name="kdenlive:docproperties.proxyparams"/>
                            <property name="kdenlive:docproperties.scrollPos">0</property>
                            <property name="kdenlive:docproperties.seekOffset">30000</property>
                            <property name="kdenlive:docproperties.version">1</property>
                            <property name="kdenlive:docproperties.verticalzoom">1</property>
                            <property name="kdenlive:docproperties.videoTarget">-1</property>
                            <property name="kdenlive:docproperties.zonein">0</property>
                            <property name="kdenlive:docproperties.zoneout">75</property>
                            <property name="kdenlive:docproperties.zoom">8</property>
                            <property name="kdenlive:expandedFolders"/>
                            <property name="kdenlive:documentnotes"/>
                            <property name="xml_retain">1</property>\n'''

            i = 0
            for sub in subtitles_list:
                final_xml += '''<entry producer="producer{i}" in="{zerotime}" out="{out}"/>\n'''.format(i=i, zerotime=str(timecode.Timecode('1000', start_seconds=0.001, fractional=True)), out=str(timecode.Timecode('1000', start_seconds=sub[1], fractional=True)))
                i += 1

            final_xml += '''</playlist>
                            <producer id="black_track" in="00:00:00.000" out="00:20:12.120">
                                <property name="length">2147483647</property>
                                <property name="eof">continue</property>
                                <property name="resource">black</property>
                                <property name="aspect_ratio">1</property>
                                <property name="mlt_service">color</property>
                                <property name="mlt_image_format">rgb24a</property>
                                <property name="set.test_audio">0</property>
                            </producer>
                            <playlist id="playlist0">
                                <property name="kdenlive:audio_track">1</property>
                            </playlist>
                            <playlist id="playlist1"/>
                            <tractor id="tractor0" in="00:00:00.000">
                                <property name="kdenlive:audio_track">1</property>
                                <property name="kdenlive:trackheight">69</property>
                                <property name="kdenlive:timeline_active">1</property>
                                <property name="kdenlive:collapsed">0</property>
                                <property name="kdenlive:thumbs_format"/>
                                <property name="kdenlive:audio_rec"/>
                                <track hide="video" producer="playlist0"/>
                                <track hide="video" producer="playlist1"/>
                            </tractor>
                            <playlist id="playlist2">
                                <property name="kdenlive:audio_track">1</property>
                            </playlist>
                            <playlist id="playlist3"/>
                            <tractor id="tractor1" in="00:00:00.000">
                                <property name="kdenlive:audio_track">1</property>
                                <property name="kdenlive:trackheight">69</property>
                                <property name="kdenlive:timeline_active">1</property>
                                <property name="kdenlive:collapsed">0</property>
                                <property name="kdenlive:thumbs_format"/>
                                <property name="kdenlive:audio_rec"/>
                                <track hide="video" producer="playlist2"/>
                                <track hide="video" producer="playlist3"/>
                            </tractor>
                            <playlist id="playlist4"/>
                            <playlist id="playlist5"/>
                            <tractor id="tractor2" in="00:00:00.000" out="00:00:12.080">
                                <property name="kdenlive:trackheight">69</property>
                                <property name="kdenlive:timeline_active">1</property>
                                <property name="kdenlive:collapsed">0</property>
                                <property name="kdenlive:thumbs_format"/>
                                <property name="kdenlive:audio_rec"/>
                                <track hide="audio" producer="playlist4"/>
                                <track producer="playlist5"/>
                            </tractor>
                            <playlist id="playlist6">'''
            i = 0
            last_intime = 0
            for sub in subtitles_list:
                last_intime = sub[0] - last_intime
                if last_intime:
                    final_xml += '''
                                    <blank length="{intime}"/>'''.format(intime=str(timecode.Timecode('1000', start_seconds=last_intime, fractional=True)))
                final_xml += '''
                                <entry producer="producer{i}" in="{zerotime}" out="{out}">
                                    <property name="kdenlive:id">{id}</property>
                                </entry>'''.format(i=i, id=i+2, zerotime=str(timecode.Timecode('1000', start_seconds=0.001, fractional=True)), out=str(timecode.Timecode('1000', start_seconds=sub[1], fractional=True)))
                last_intime = sub[0] + sub[1]
                i += 1

            final_xml += '''
                            </playlist>
                            <playlist id="playlist7"/>
                            <tractor id="tractor3" in="00:00:00.000">
                                <property name="kdenlive:trackheight">69</property>
                                <property name="kdenlive:timeline_active">1</property>
                                <property name="kdenlive:collapsed">0</property>
                                <property name="kdenlive:thumbs_format"/>
                                <property name="kdenlive:audio_rec"/>
                                <track hide="audio" producer="playlist6"/>
                                <track producer="playlist7"/>
                            </tractor>
                            <tractor id="tractor4" global_feed="1" in="00:00:00.000" out="00:20:12.120">
                                <track producer="black_track"/>
                                <track producer="tractor0"/>
                                <track producer="tractor1"/>
                                <track producer="tractor2"/>
                                <track producer="tractor3"/>
                            </tractor>
                            </mlt>'''

            with open(filename, mode='w', encoding='utf-8') as txt_file:
                txt_file.write(final_xml)


def save_file(final_file, subtitles_list, subtitle_format='SRT', language='en'):
    """Function to save the subtitle project. A subtitles dict and the format is given."""
    if subtitles_list:
        # if not final_file.lower().endswith('.' + format.lower()):
        #     final_file += '.' + format.lower()

        if subtitle_format in ['SRT', 'DFXP', 'SAMI', 'SCC', 'VTT']:
            captions = pycaption.CaptionList()
            for sub in subtitles_list:
                # skip extra blank lines
                nodes = [pycaption.CaptionNode.create_text(sub[2])]
                caption = pycaption.Caption(start=sub[0]*1000000, end=(sub[0] + sub[1])*1000000, nodes=nodes)
                captions.append(caption)
            caption_set = pycaption.CaptionSet({language: captions})

            if subtitle_format == 'SRT':
                open(final_file, mode='w', encoding='utf-8').write(pycaption.SRTWriter().write(caption_set))
            elif subtitle_format == 'DFXP':
                open(final_file, mode='w', encoding='utf-8').write(pycaption.DFXPWriter().write(caption_set))
            elif subtitle_format == 'SAMI':
                open(final_file, mode='w', encoding='utf-8').write(pycaption.SAMIWriter().write(caption_set))
            elif subtitle_format == 'SCC':
                open(final_file, mode='w', encoding='utf-8').write(pycaption.SCCWriter().write(caption_set))
            elif subtitle_format == 'VTT':
                open(final_file, mode='w', encoding='utf-8').write(pycaption.WebVTTWriter().write(caption_set))

        elif subtitle_format in ['ASS', 'SBV', 'XML', 'SUB']:
            if subtitle_format in ['ASS', 'SUB']:
                assfile = pysubs2.SSAFile()
                index = 0
                for sub in reversed(sorted(subtitles_list)):
                    assfile.insert(index, pysubs2.SSAEvent(start=int(sub[0]*1000), end=int((sub[0]*1000)+(sub[1]*1000)), text=sub[2].replace('\n', ' ')))
                if subtitle_format == 'SUB':
                    assfile.save(final_file, subtitle_format='microdvd')
                else:
                    assfile.save(final_file)
            else:
                if subtitle_format == 'SBV':
                    from captionstransformer.sbv import Writer
                elif subtitle_format == 'XML':
                    from captionstransformer.transcript import Writer
                writer = Writer(open(final_file, mode='w', encoding='utf-8'))
                captions = []
                for cap in subtitles_list:
                    caption = captionstransformer.core.Caption()
                    caption.start = captionstransformer.core.get_date(second=int(cap[0]//1), millisecond=int((cap[0]%1)*1000))
                    caption.duration = captionstransformer.core.get_date(second=int(cap[1]//1), millisecond=int((cap[1]%1)*1000)) -  captionstransformer.core.get_date()
                    caption.text = cap[2]
                    captions.append(caption)
                writer.set_captions(captions)
                writer.write()

        elif subtitle_format in ['USF']:
            open(final_file, mode='w', encoding='utf-8').write(usf.USFWriter().write(subtitles_list))
