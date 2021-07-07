from socket import *
import json

s = socket(AF_INET, SOCK_STREAM)
s.connect(('', 7978))

# message = 'hi, there'

# request = json.dumps(message)
# s.send(request.encode('utf-8'))
while True:
    response = s.recv(1024)
    if response:
        data = response.decode('utf-8')
        print(data)
    else:
        continue
