
# 端口扫描
# ip段输入格式：x.x.x.x-x.x.x.x
import nmap
import socket
import sys
from queue import Queue
from threading import Thread, Lock

jobs = Queue()
lock = Lock()

r = sys.argv
THNUM = 10
PORTRANGE = []
IP = []
FLAG = True # 是否非法输入
IP_NUM = 0 # ip段总ip数
'''
ip = r[1]
端口号 = r[2]
线程数 = r[3] 
'''

def get_tnum():
    global THNUM
    THNUM = int(r[3])

# 解析IP地址
def get_ip():
    global IP
    global FLAG
    global IP_NUM
    ip_start = r[1].split('-')[0]
    ip_end = r[1].split('-')[1]

    s0 = int(ip_start.split('.')[0])
    s1 = int(ip_start.split('.')[1])
    s2 = int(ip_start.split('.')[2])
    s3 = int(ip_start.split('.')[3])

    e0 = int(ip_end.split('.')[0])
    e1 = int(ip_end.split('.')[1])
    e2 = int(ip_end.split('.')[2])
    e3 = int(ip_end.split('.')[3])

    if s0 < 0 or s0 > 255:
        FLAG = False
    if s1 < 0 or s1 > 255:
        FLAG = False
    if s2 < 0 or s2 > 255:
        FLAG = False
    if s3 < 0 or s3 > 255:
        FLAG = False
    if e0 < 0 or e0 > 255:
        FLAG = False
    if e1 < 0 or e1 > 255:
        FLAG = False
    if e2 < 0 or e2 > 255:
        FLAG = False
    if e3 < 0 or e3 > 255:
        FLAG = False

    if e3 < s3:
        e2 -= 1
        e3 += 256
    IP_NUM += (e3 - s3) * 1
    if e2 < s2:
        e1 -= 1
        e2 += 256
    IP_NUM += (e2 - s2) * 256
    if e1 < s1:
        e0 -= 1
        e1 += 256
    IP_NUM += (e1 - s1) * 256 * 256
    IP_NUM += (e0 - s0) * 256 * 256 * 256

    IP.append(ip_start)
    for _ in range(IP_NUM):
        s3 += 1
        if s3 > 255:
            s3 -= 255
            s2 += 1
        if s2 > 255:
            s2 -= 255
            s1 += 1
        if s1 > 255:
            s1 -= 255
            s0 += 1
        IP.append(str(s0) + "." + str(s1) + "." + str(s2) + "." + str(s3))

# 解析端口范围
def get_port():
    global FLAG
    port_start = int(r[2].split('-')[0])
    port_end = int(r[2].split('-')[1])
    if port_start < 0 or port_start > 65535:
        FLAG = False
    if port_end < 0 or port_end > 65535:
        FLAG = False
    for port in range(port_start, port_end + 1):
        PORTRANGE.append(port)

# 检查端口是否开放
def scan(address: tuple) -> bool:
    # 实例化nmap端口扫描对象
    nm = nmap.PortScanner()
    state=''
    # 执行scan()函数
    try:
        nm.scan(address[0], str(address[1]))
        # 获取tcp协议对应的端口状态
        state = nm[address[0]]['tcp'][address[1]]['state']
    except Exception as e:
        pass
    if state == "open":
        return True
    return False

# ip:port => 元组
# (ip,port)

class Product(Thread):
    def run(self) -> None:
        global  PORTRANGE
        for port in PORTRANGE:
            for i in IP:
                jobs.put((i,port)) # 元组 （ip，port）

class Customer(Thread):
    def run(self) -> None:
        while True:
            address = jobs.get()
            if scan(address):
                lock.acquire()
                print(f'*{address[0]}:{address[1]}\tOPEN')
                lock.release()
            jobs.task_done()

def main():
    global IP_NUM
    global FLAG
    if IP_NUM < 0 or not FLAG:
        print("非法输入！")
        sys.exit()

    p = Product()
    p.daemon = True
    p.start()

    for _ in range(THNUM):
        c = Customer()
        c.daemon = True
        c.start()

    jobs.join()



if __name__ == '__main__':
    get_ip()
    get_port()
    get_tnum()
    main()

