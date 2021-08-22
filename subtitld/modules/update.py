"""Software update module

"""

import os
import requests

try:
    import _winreg as winreg
except ImportError:
    import winreg

from PyQt5.QtCore import QThread, pyqtSignal

from subtitld.modules.paths import VERSION_NUMBER, PATH_SUBTITLD_DATA_UPDATE



class ThreadCheckVersion(QThread):
    """Class for QThread for checking version"""
    command = pyqtSignal(dict)
    url = 'https://api2.jonata.org/subtitld/windows_version'

    def run(self):
        """Function for running QThread"""
        result = {}
        result = requests.get(self.url).json()
        self.command.emit(result)


class ThreadDownloadInstaller(QThread):
    """Class for QThread for download installer"""
    command = pyqtSignal(str)
    url = 'https://api2.jonata.org/subtitld/get_windows_installer'
    downloadfolder = os.path.join(PATH_SUBTITLD_DATA_UPDATE, 'subtitld_update.exe')

    def run(self):
        """Function for running QThread"""
        if self.url and os.path.isdir(os.path.dirname(self.downloadfolder)):
            result = ''
            with requests.get(self.url, stream=True) as req:
                req.raise_for_status()
                with open(self.downloadfolder, 'wb') as fileupd:
                    for chunk in fileupd.iter_content(chunk_size=8192):
                        fileupd.write(chunk)
                if os.path.isfile(self.downloadfolder):
                    result = self.downloadfolder
            self.command.emit(result)


def set_run_key(key, value):
    """Function to call registry and schedule or remove installer on startup"""
    reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Run', 0, winreg.KEY_SET_VALUE)

    with reg_key:
        if value is None:
            winreg.DeleteValue(reg_key, key)
        else:
            if '%' in value:
                try:
                    var_type = winreg.REG_EXPAND_SZ
                except Exception:
                    pass
            else:
                var_type = winreg.REG_SZ
            winreg.SetValueEx(reg_key, key, 0, var_type, value)


def load(self):
    """Function to load update"""
    if os.path.isfile(os.path.join(PATH_SUBTITLD_DATA_UPDATE, 'subtitld_update.exe')):
        os.remove(os.path.join(PATH_SUBTITLD_DATA_UPDATE, 'subtitld_update.exe'))
    set_run_key('subtitld_update', None)

    def thread_download_installer_ended(command):
        set_run_key('subtitld_update', command + ' /S')

    self.thread_download_installer = ThreadDownloadInstaller(self)
    self.thread_download_installer.command.connect(thread_download_installer_ended)
    self.thread_download_installer.start()

    def thread_check_version_ended(command):
        if not command.get('stable', VERSION_NUMBER) == VERSION_NUMBER:
            self.thread_download_installer.start()

    self.thread_check_version = ThreadCheckVersion(self)
    self.thread_check_version.command.connect(thread_check_version_ended)
    self.thread_check_version.start()
