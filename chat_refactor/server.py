import sys
import socket
from moduls import load_settings, send_message, get_message
from services import actions, status_code
from socket import *
import json
import logging.config
from log.log_module import log

# НАСТРОЙКИ ЛОГИРОВАНИЯ
logging.config.fileConfig('log/logging.ini',
                          disable_existing_loggers=False,
                          defaults={'logfilename': 'log/server.log'})
logger = logging.getLogger('server')

# ЗАГРУЖАЮ НАСТРОЙКИ
config = load_settings('DEVELOP')


# СОЗДАЮ ОТВЕТ НА PRESENCE СООБЩЕНИЕ ОТ КЛИЕНТА
@log(logger)
def create_presence_responce(message):
    if config['ACTION'] in message \
            and message[config['ACTION']] == actions.PRESENCE \
            and config['TIME'] in message \
            and config['USER'] in message:
        logger.info(f'Ответ от сервера сформирован успешно - КОД 200')
        return {config['RESPONSE']: status_code.OK}

    logger.error(f'Некорректное сообщение от клиента. Ответ от сервера - КОД 400 \n'
                 f'{message}')
    return {
        config['RESPONSE']: status_code.BAD_REQUEST,
        config['ERROR']: 'Bad Request'
    }


# ЗАПУСК И НАСТРОЙКА СЕРВЕРА
@log(logger)
def start_server():
    try:
        listen_ip = sys.argv[1]
        listen_port = int(sys.argv[2])
        if not 65535 >= listen_port >= 1024:
            raise ValueError

        logger.info(f'Все аргументы скрипта переданы верно')

    except IndexError:
        listen_ip = config['DEFAULT_IP_ADDRESS']
        listen_port = int(config['DEFAULT_PORT'])
        logger.error(f'Один из аргументов сервера передан не верно. '
                     f'Были использованы аргументы из файла settings.ini', exc_info=True)

    except ValueError:
        print('Порт должен быть указан в пределах от 1024 до 65535')
        logger.error(f'Порт в аргументах сервера не верный: {listen_port}', exc_info=True)
        sys.exit(1)

    transport = socket(AF_INET, SOCK_STREAM)
    transport.bind((listen_ip, listen_port))
    transport.listen(int(config['MAX_CONNECTIONS']))

    logger.info(f'Успешное подключение на сервере: host {listen_ip}, port {listen_port}')

    while True:
        client, client_address = transport.accept()
        try:
            message = get_message(client, int(config['MAX_PACKAGE_LENGTH']), config['ENCODING'])
            logger.info(f'Сообщение от клиента декодировано успешно')
            response = create_presence_responce(message)
            send_message(client, response, config['ENCODING'])
            logger.info(f'Ответ отправлен клиенту')
        except (ValueError, json.JSONDecodeError):
            logger.error(f'Ошибка декодирования сообщения', exc_info=True)

        client.close()

if __name__ == "__main__":
    start_server()
