import sys
import socket
from moduls import load_settings, send_message, get_message
from services import actions, status_code
from socket import *
import json
import logging.config
from select import *

# НАСТРОЙКИ ЛОГИРОВАНИЯ
logging.config.fileConfig('log/logging.ini',
                          disable_existing_loggers=False,
                          defaults={'logfilename': 'log/server.log'})
logger = logging.getLogger('server')

# ЗАГРУЖАЮ НАСТРОЙКИ
config = load_settings('DEVELOP')


# СОЗДАЮ ОТВЕТ НА PRESENCE СООБЩЕНИЕ ОТ КЛИЕНТА
def create_presence_responce(message):
    if config['ACTION'] in message \
            and message[config['ACTION']] == actions.PRESENCE \
            and config['TIME'] in message \
            and config['USER'] in message:
        logger.info(f'Ответ от сервера сформирован успешно - КОД 200')
        return {config['RESPONSE']: status_code.OK}

    logger.error(f'Некорректное сообщение от клиента. Ответ от сервера: КОД 400 \n'
                 f'{message}')
    return {
        config['RESPONSE']: status_code.BAD_REQUEST,
        config['ERROR']: 'Bad Request'
    }

# ЗАПУСК И НАСТРОЙКА СЕРВЕРА
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
    transport.settimeout(0.2)

    logger.info(f'Успешное подключение на сервере: host {listen_ip}, port {listen_port}')

    all_clients = []

    while True:
        try:
            client, client_address = transport.accept()
        except OSError:
            pass
        else:
            logger.info(f'Установлено соедение с {client_address}')
            all_clients.append(client)

        recv_data_lst = []
        send_data_lst = []
        err_lst = []
        messages_list = []

        try:
            if all_clients:
                recv_data_lst, send_data_lst, err_lst = select(all_clients, all_clients, [], 0)
        except OSError:
            pass

        if recv_data_lst:
            for client_with_message in recv_data_lst:
                message = get_message(client_with_message, int(config['MAX_PACKAGE_LENGTH']), config['ENCODING'])
                logger.info(f'Сообщение от клиента декодировано успешно')

                if message['action'] == 'presence':
                    response = create_presence_responce(message)
                    try:
                        send_message(client_with_message, response, config['ENCODING'])
                        logger.info(f'Установлено соединение с клиентом {message["user"]}')
                    except:
                        logger.error(f'Клиент {client_with_message.getpeername()} отключился от сервера.')

                if message['action'] == 'msg':
                    messages_list.append(message)
                    logger.info(f'Сообщение от {message["from"]} добавлен в лист рассылки')

        if messages_list and send_data_lst:
            for msg in messages_list:
                for waiting_client in send_data_lst:
                    send_message(waiting_client, msg, config['ENCODING'])
                    logger.info(f'Сообщение к {waiting_client} отправлено')
                messages_list.remove(msg)
                logger.info(f'Сообщение {msg} всем отправлено')

if __name__ == "__main__":
    start_server()

