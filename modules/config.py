#!/usr/bin/env python3

import os
import json

from modules.paths import PATH_SUBTITLD_USER_CONFIG_FILE


def load(config_file_path=False):
    config = {}
    if config_file_path and os.path.isfile(config_file_path):
        with open(config_file_path) as f:
            config = json.load(f)

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

    return config


def save(config=False, config_file_path=False):
    if config:
        if not config_file_path:
            config_file_path = os.path.join(PATH_SUBTITLD_USER_CONFIG_FILE)
        with open(config_file_path, 'w') as f:
            json.dump(config, f)
