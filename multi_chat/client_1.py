from socket import *

s = socket(AF_INET, SOCK_STREAM)
s.connect(('', 7978))

while True:
    message = input('Введите сообщение: ').encode('utf-8')
    s.send(message)
