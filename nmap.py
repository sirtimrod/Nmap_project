from excelWrite import writeExcel
import socket
import sys
import threading
import time
from queue import Queue


socket.setdefaulttimeout(0.5)
print_lock = threading.Lock()
print('-' * 35)
target = input('Enter the host to be scanned: ')
t_IP = socket.gethostbyname(target)
print('Starting scan on host: ', t_IP)
print('-' * 35)
print('Enter ports')
first_port = input('Enter the first port: ')
last_port = input('Enter the last port: ')
print('-' * 35)
ports = []
services =[]
versions =[]

'''Функция portscan через потоки пытается подключиться к выбранным портам и после удачного подключения собирает в список только открытые порты'''
def portscan(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        con = s.connect((t_IP, port))
        with print_lock:
            print(port, '/tcp open')
            global ports
            ports.append(port)
        con.close()
    except:
        pass

'''Функция servisescan вывод сервисы, запущенный на портах. Также собирает сервисы открытых портов в список'''
def servisescan(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.setdefaulttimeout(1)
    try:
        s.connect((t_IP, port))
        service = socket.getservbyport(port)
        print(port, service)
        global services
        services.append(service)
        s.close()
    except:
        print("Port", port, "have unknown service")
        badService = 'Unknown service'
        services.append(badService)

'''Функция bannergrabbing отсылает запрос на порт и после записывает ответ в котором содержится версия запущенного сервиса'''
def bannergrabbing(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s = socket.socket()
        s.connect((t_IP, port))
        s.sendall(b'/\n\n') #тут посылается запрос на нужный порт
        sendBytes = s.recv(1024) #таким образом считываются нужные байты ответа
        # getStr = sendBytes.decode("utf-8")
        global versions
        print(port)
        print(sendBytes)
        versions.append(sendBytes)
        s.close()
    except:
        print("Port", port, "have unknown version of service")
        badVersion = 'Unknown version'
        versions.append(badVersion)


def threader():
    while True:
        worker = q.get()
        portscan(worker)
        q.task_done()

q = Queue()
startTime = time.time()

for x in range(100):
    t = threading.Thread(target=threader)
    t.daemon = True
    t.start()

for worker in range(int(first_port), int(last_port)):
    q.put(worker)

q.join()
print('-' * 35)
print('Time taken:', time.time() - startTime)
print('-' * 35)
print(ports)
print('-' * 35)

for port in ports:
    servisescan(port)
print('-' * 35)

for port in ports:
    bannergrabbing(port)
    print('-' * 60)

print(services)
print(versions)

excelFile = writeExcel(target, t_IP, ports, services, versions)
excelFile.write_ports()
excelFile.write_services()
excelFile.write_versions()
excelFile.save_all()

