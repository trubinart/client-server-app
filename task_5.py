import subprocess
import locale

def_coding = locale.getpreferredencoding()
list = ['yandex.ru', 'youtube.com']
comand = 'ping'

for i in list:
    subproc_ping = subprocess.Popen([comand, i], stdout=subprocess.PIPE)
    num = 0
    for line in subproc_ping.stdout:
        if num > 5:
            break
        num +=1
        print(line.decode('utf-8').replace('\n', ''))