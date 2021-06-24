import sys
import socket
from moduls import load_settings, send_message, get_message
from service_code import actions, status_code
from socket import *
import json

config = load_settings('DEVELOP')

def create_presence_responce(message):
    if config['ACTION'] in message \
        and message[config['ACTION']] == actions.PRESENCE \
        and config['TIME'] in message \
        and config['USER'] in message:
            return {config['RESPONSE']: status_code.OK}
    return {
        config['RESPONSE']: status_code.BAD_REQUEST,
        config['ERROR']: 'Bad Request'
    }

def start_server():
    try:
        listen_ip = sys.argv[1]
        listen_port = int(sys.argv[2])
        if not 65535 >= listen_port >= 1024:
            raise ValueError

    except IndexError:
        listen_ip = config['DEFAULT_IP_ADDRESS']
        listen_port = int(config['DEFAULT_PORT'])

    except ValueError:
        print('Порт должен быть указан в пределах от 1024 до 65535')
        sys.exit(1)

    transport = socket(AF_INET, SOCK_STREAM)
    transport.bind((listen_ip, listen_port))
    transport.listen(int(config['MAX_CONNECTIONS']))

    while True:
        client, client_address = transport.accept()
        try:
            message = get_message(client, int(config['MAX_PACKAGE_LENGTH']), config['ENCODING'])
            print(message)
            response = create_presence_responce(message)
            send_message(client, response, config['ENCODING'])
            client.close()
        except (ValueError, json.JSONDecodeError):
            print('Принято некорретное сообщение от клиента')
            client.close()

if __name__ == "__main__":
    start_server()