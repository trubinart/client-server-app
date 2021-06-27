import os
import sys
import configparser
import json


def load_settings(enviroment):
    if not os.path.exists('settings.ini'):
        print('Нет файла settings.ini')
        sys.exit(1)

    config_keys = [
        'DEFAULT_PORT',
        'MAX_CONNECTIONS',
        'MAX_PACKAGE_LENGTH',
        'ENCODING',
        'ACTION',
        'TIME',
        'USER',
        'ACCOUNT_NAME',
        'RESPONSE',
        'ERROR',
    ]
    config = configparser.ConfigParser()
    config.read("settings.ini")

    for key in config_keys:
        if key not in config[enviroment]:
            print(f'В файле settings.ini нет {key}')
            sys.exit(1)

    return config[enviroment]


def send_message(open_socket, message, encoding):
    request = json.dumps(message)
    open_socket.send(request.encode(encoding))


def get_message(open_socket, max_package_lenght, encoding):
    response = open_socket.recv(max_package_lenght)
    if isinstance(response, bytes):
        json_response = response.decode(encoding)
        response_dict = json.loads(json_response)
        if isinstance(response_dict, dict):
            return response_dict
        raise ValueError
    raise ValueError