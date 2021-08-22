"""Config functions. Load and save files.

"""

import os
import json

from subtitld.modules.paths import PATH_SUBTITLD_USER_CONFIG_FILE


def load(config_file_path=False):
    """Config load function. Provide a file path with 'config_file_path'.
    It will return a dict with the settings.
    """
    config = {}
    if config_file_path and os.path.isfile(config_file_path):
        with open(config_file_path) as fileobj:
            config = json.load(fileobj)

    if not config.get('recent_files', False):
        config['recent_files'] = {}

    if not config.get('shortcuts', False):
        config['shortcuts'] = {}

    if not config.get('safety_margins', False):
        config['safety_margins'] = {}

    if not config.get('autosave', False):
        config['autosave'] = {}

    if not config.get('timeline', False):
        config['timeline'] = {}

    if not config.get('quality_check', False):
        config['quality_check'] = {}

    return config


def save(config=False, config_file_path=False):
    """Config save function. Provide a dict and
    a file path with 'config_file_path'.
    """
    if config:
        if not config_file_path:
            config_file_path = os.path.join(PATH_SUBTITLD_USER_CONFIG_FILE)
        with open(config_file_path, 'w') as fileobj:
            json.dump(config, fileobj)
