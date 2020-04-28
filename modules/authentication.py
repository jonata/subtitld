#!/usr/bin/env python3

import os
import sys
import subprocess
import requests
import hashlib
from datetime import datetime

def get_machine_id():
    machine_id = ''
    if sys.platform == 'darwin':
        ioreg_cmd = subprocess.run(['ioreg','-rd1','-c','IOPlatformExpertDevice'], stdout=subprocess.PIPE, text=True)
        machine_id = ioreg.stdout.split('IOPlatformUUID',1)[1].split('\n')[0].strip()
    elif sys.platform in ['win32', 'msys']:
        reg_cmd = subprocess.run(['reg', 'query', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Cryptography', '/v', 'MachineGuid'], stdout=subprocess.PIPE, text=True, startupinfo=STARTUPINFO)
        machine_id = reg_cmd.stdout.split('REG_SZ',1)[1].strip()
    elif 'bsd' in sys.platform:
        machine_id = open('/etc/hostid', 'r').read().strip()
    else:
        machine_id = open('/etc/machine-id', 'r').read().strip()

    return machine_id

def verify_user_and_machineid(email=False, machine_id=False):
    if email and machine_id:
        information = {
                            'email': email,
                            'machineid': machine_id,
                            'os': str(sys.platform)
        }
        response = requests.post('https://api.jonata.org/subtitld/verify_email_and_machineid', json=information)

        return response.json()

def check_authentication(auth_dict=False, email=False, machineid=False):
    result = False
    if auth_dict and email and machineid:
        date_today = datetime.now().strftime("%Y%m%d")
        auth_hash = auth_dict.get(date_today, '')
        if auth_hash == hashlib.md5(str(email + '|' + machineid + '|' + date_today).encode()).hexdigest():
            result = True
    return result

def append_authentication_keys(config=False, dict=False):
    if config and dict:
        for date in dict.keys():
            if datetime.strptime(date, '%Y%m%d') >= datetime.now():
                config['authentication']['codes'][date] = dict[date]

def load_subtitld_codes_file(path=''):
    final_dict = {}
    if path and os.path.isfile(path):
        with open(path) as f:
            json_dict = json.load(f)
            if ACTUAL_OS in json_dict.get('authentication_keys', {}).keys():
                final_dict = json_dict['authentication_keys'][ACTUAL_OS]
    return final_dict

def get_days_to_expiry_date(auth_dict=False):
    days = 0
    if auth_dict:
        last_day = auth_dict.keys()[-1]
        days = (datetime.strptime(last_day, '%Y%m%d') - datetime.now()).days
    return days

#
# def load_authentications(authentications_path=False):
#     auth_dict = {}
#     if authentications_path and os.path.isfile(os.path.join(authentications_path, 'subtitld.auth')):
#         with open(os.path.join(authentications_path, 'subtitld.auth')) as f:
#             auth_dict['subtitld'] = json.load(f)
#
#     return auth_dict

#
# def save_authentications(authentications_path=False, module=False, auth_dict=False):
#     if authentications_path and module and auth_dict:
#         with open(os.path.join(authentications_path, module + '.auth'), 'w') as f:
#             json.dump(auth_dict, f)
