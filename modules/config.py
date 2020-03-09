#!/usr/bin/env python3

import os
import json
import bcrypt
import datetime

from modules.paths import *

def load(config_file_path=False):
    config = {}
    if config_file_path and os.path.isfile(config_file_path):
        with open(config_file_path) as f:
            config = json.load(f)

    if not config.get('recent_files', False):
        config['recent_files'] = {}

    return config

def save(config=False, config_file_path=False):
    if config:
        if not config_file_path:
            config_file_path = os.path.join(PATH_SUBTITLD_USER_CONFIG_FILE)
        with open(config_file_path, 'w') as f:
            json.dump(config, f)

def load_authentications(authentications_path=False):
    auth_dict = {}
    if authentications_path and os.path.isfile(os.path.join(authentications_path, 'subtitld.auth')):
        with open(os.path.join(authentications_path, 'subtitld.auth')) as f:
            auth_dict['subtitld'] = json.load(f)

    return auth_dict

def save_authentications(authentications_path=False, module=False, auth_dict=False):
    if authentications_path and module and auth_dict:
        with open(os.path.join(authentications_path, module + '.auth'), 'w') as f:
            json.dump(auth_dict, f)

def check_authentication(module=False, auth_dict=False, username=False):
    result = False
    if module and auth_dict and username:
        if module in auth_dict.keys():
            date_today = datetime.datetime.now().strftime("%Y%m%d")
            auth_hash = auth_dict[module].get(date_today, '')
            if bcrypt.checkpw(str(username + '|' + module + '|' + date_today).encode('utf-8'), auth_hash.encode('utf-8')):
                result = True
    return result
