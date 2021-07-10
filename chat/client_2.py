import sys
import socket
import time
from moduls import load_settings, send_message, get_message
from services import actions
from socket import *
import json
import logging.config
from threading import Thread

# НАСТРОЙКИ ЛОГИРОВАНИЯ
logging.config.fileConfig('log/logging.ini',
                          disable_existing_loggers=False,
                          defaults={'logfilename': 'log/client.log'})
logger = logging.getLogger('client')

# ЗАГРУЖАЮ НАСТРОЙКИ
config = load_settings('DEVELOP')


def create_presence_message(account_name):
    message = {
        config['ACTION']: actions.PRESENCE,
        config['TIME']: time.ctime(time.time()),
        config['USER']: {
            config['ACCOUNT_NAME']: account_name
        }
    }
    logger.info(f'Сформировано presence сообщение')
    return message


def create_msg(message, account_name):
    message = {
        config['ACTION']: actions.MSQ,
        config['TIME']: time.ctime(time.time()),
        config['TO']: "#room_name",
        config['FROM']: account_name,
        config['MESSAGE']: message
    }
    logger.info(f'Сформировано msg от клиента')
    return message


def check_responce(responce):
    if config['RESPONSE'] in responce:
        if responce[config['RESPONSE']] == 200:
            logger.info(f'От сервера пришел ответ - 200')
            return '200'
        if responce[config['RESPONSE']] == 400:
            logger.error(f'От сервера пришел ответ - 400 \n'
                         f'{responce}')
            return '400'
    raise ValueError

def thread_for_send(transport,account_name):
    while True:
        message = input('Введите сообщение: ')
        msg = create_msg(message, account_name)
        send_message(transport, msg, config['ENCODING'])
        logger.info(f'Отправлено сообщение серверу {msg["message"]}')

def thread_for_write(transport):
    while True:
        msg = get_message(transport, int(config['MAX_PACKAGE_LENGTH']), config['ENCODING'])
        logger.info(f'Получено сообщение от {msg["from"]} - {msg["message"]}')
        print(msg['message'])

def start_client():
    try:
        server_ip = sys.argv[1]
        server_port = int(sys.argv[2])
        logger.info(f'Все аргументы скрипта переданы верно')
        if not 65535 >= server_port >= 1024:
            raise ValueError

        logger.info(f'Все аргументы скрипта переданы верно')

    except IndexError:
        server_ip = config['DEFAULT_IP_ADDRESS']
        server_port = int(config['DEFAULT_PORT'])

        logger.error(f'Один из аргументов сервера передан не верно. '
                     f'Были использованы аргументы из файла settings.ini', exc_info=True)

    except ValueError:
        print('Порт должен быть указан в пределах от 1024 до 65535')
        logger.error(f'Порт в аргументах сервера не верный: {server_port}', exc_info=True)
        sys.exit(1)

    transport = socket(AF_INET, SOCK_STREAM)
    transport.connect((server_ip, server_port))
    account_name = 'ivan ivanov'

    logger.info(f'Успешное подключение на клиенте: host {server_ip}, port {server_port}')

    presence_message = create_presence_message(account_name)
    send_message(transport, presence_message, config['ENCODING'])
    logger.info(f'Сообщение от клиента отправлено успешно')

    try:
        response = get_message(transport, int(config['MAX_PACKAGE_LENGTH']), config['ENCODING'])
        check = check_responce(response)
        logger.info(f'Соединение с сервером успешно установлено: ответ {check}')
    except (ValueError, json.JSONDecodeError):
        logger.error(f'Ошибка декодирования сообщения', exc_info=True)

    send = Thread(target=thread_for_send, kwargs={'transport': transport, 'account_name': account_name})
    send.start()

    write = Thread(target=thread_for_write, kwargs={'transport': transport})
    write.start()

if __name__ == "__main__":
    start_client()
