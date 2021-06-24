import sys
import socket
import time
from moduls import load_settings, send_message, get_message
from service_code import actions
from socket import *
import json

config = load_settings('DEVELOP')


def create_presence_message(account_name):
    message = {
        config['ACTION']: actions.PRESENCE,
        config['TIME']: time.ctime(time.time()),
        config['USER']: {
            config['ACCOUNT_NAME']: account_name
        }
    }
    return message


def check_responce(responce):
    if config['RESPONSE'] in responce:
        if responce[config['RESPONSE']] == 200:
            return '200'
        if responce[config['RESPONSE']] == 400:
            return '400'
    raise ValueError


def start_client():
    try:
        server_ip = sys.argv[1]
        server_port = int(sys.argv[2])
        if not 65535 >= server_port >= 1024:
            raise ValueError

    except IndexError:
        server_ip = config['DEFAULT_IP_ADDRESS']
        server_port = int(config['DEFAULT_PORT'])

    except ValueError:
        print('Порт должен быть указан в пределах от 1024 до 65535')
        sys.exit(1)

    transport = socket(AF_INET, SOCK_STREAM)
    transport.connect((server_ip, server_port))

    presence_message = create_presence_message('artem trubin')
    send_message(transport, presence_message, config['ENCODING'])

    try:
        response = get_message(transport, int(config['MAX_PACKAGE_LENGTH']), config['ENCODING'])
        check = check_responce(response)
        print(f'Ответ от сервера {check}')
        print(response)
    except (ValueError, json.JSONDecodeError):
        print('Ошибка декодирования сообщения')

    transport.close()

if __name__ == "__main__":
    start_client()