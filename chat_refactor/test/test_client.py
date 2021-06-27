import unittest
from client import create_presence_message, check_responce
from moduls import load_settings
from service_code import actions, status_code
import time
import subprocess

config = load_settings('DEVELOP')


class TestClient(unittest.TestCase):

    def test_create_presence_message(self):
        account_name = 'test account'
        time_to_msg = time.ctime(time.time())
        message = {
            config['ACTION']: actions.PRESENCE,
            config['TIME']: time_to_msg,
            config['USER']: {
                config['ACCOUNT_NAME']: account_name
            }
        }
        self.assertEqual(create_presence_message(account_name), message, 'test_create_presence_message')

    def test_check_responce_200(self):
        responce = {config['RESPONSE']: status_code.OK}
        self.assertEqual(check_responce(responce), '200', 'test_check_responce')

    def test_check_responce_400(self):
        responce = {
            config['RESPONSE']: status_code.BAD_REQUEST,
            config['ERROR']: 'Bad Request'
        }
        self.assertEqual(check_responce(responce), '400', 'test_check_responce')

    def test_start_client_port(self):
        args = ['python3', 'client.py', '127.0.0.1', '1']
        suproc = subprocess.Popen(args, stdout=subprocess.PIPE, encoding='utf-8')
        stdout, stderr = suproc.communicate()
        self.assertEqual(stdout.replace('\n', ''), 'Порт должен быть указан в пределах от 1024 до 65535',
                         'test_start_client')


if __name__ == '__main__':
    unittest.main()
