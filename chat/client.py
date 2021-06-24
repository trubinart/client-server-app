from socket import *
import time
import json
from sys import argv

script, ip, port = argv

timestr = time.ctime(time.time())
message = {
	"action": "presence",
	"time": timestr,
	"type": "status"
}

s = socket(AF_INET, SOCK_STREAM)
s.connect((ip, int(port)))

request = json.dumps(message)
s.send(request.encode('utf-8'))

response = s.recv(1024)
data = json.loads(response)
print(data)

s.close()