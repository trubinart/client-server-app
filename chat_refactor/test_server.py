import unittest
from server import create_presence_responce
from moduls import load_settings
from service_code import actions, status_code
import time
import subprocess

config = load_settings('DEVELOP')

class TestServer(unittest.TestCase):
    def test_create_presence_responce_200(self):
        account_name = 'test account'
        message = {
            config['ACTION']: actions.PRESENCE,
            config['TIME']: time.ctime(time.time()),
            config['USER']: {
                config['ACCOUNT_NAME']: account_name
            }
        }

        self.assertEqual(create_presence_responce(message),
                         {config['RESPONSE']: status_code.OK},
                         'test_create_presence_responce_200')

    def test_create_presence_responce_400(self):
        message = {
            config['ACTION']: actions.PRESENCE,
            config['TIME']: time.ctime(time.time()),
        }

        self.assertEqual(create_presence_responce(message),
                         {config['RESPONSE']: status_code.BAD_REQUEST,
                             config['ERROR']: 'Bad Request'},
                         'test_create_presence_responce_400')

if __name__ == '__main__':
    unittest.main()
