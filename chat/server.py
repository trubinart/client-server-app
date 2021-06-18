from socket import *
from statuse_code import status_code
import json
from sys import argv

script, ip, port = argv


s = socket(AF_INET, SOCK_STREAM)
s.bind((ip, int(port)))
s.listen(5)

responce_body = {
    "response": 0,
    "alert": 'Запрос прошел отлично'
}

responce_body_error = {
    "response": 0,
    "error": 'Какая-то ошибка'
}

while True:
    client, addr = s.accept()

    request = client.recv(1024)
    data = json.loads(request)
    print(data)

    if data['action'] == 'presence':
        responce_body['response'] = status_code['OK']
    else:
        responce_body['response'] = status_code['BAD_REQUEST']
        responce_body.pop('alert')
        responce_body['error'] = 'Какая-то ошибка'

    responce = json.dumps(responce_body)

    client.send(responce.encode('utf-8'))
    client.close()
