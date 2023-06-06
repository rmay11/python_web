import sys
import socket
from queue import Queue
from threading import Thread,Lock

#对输入格式进行解析获得参数
HOST=Queue()#存放address的队列
#print("工具使用格式为:nmap.py ip.start~ip.end port.start~port.end")
r=sys.argv
lock=Lock()
IP=r[1]
PORT=r[2]
thnum=int(r[3])
#print(f"你扫描的ip为：{IP}")
#print(f"你要扫描的port为：{PORT}")

def ip_true():#判断ip和port格式是否正确
    global IP
    global PORT
    ip_str=IP.split('.')
    #print(ip_str[3])
    port_str=PORT.split('~')
    ip_str_str=ip_str[3].split('~')
    if (int(ip_str[0])<0)or(int(ip_str[0])>255) or (int(ip_str[1])<0)or(int(ip_str[1])>255) or (int(ip_str[2])<0)or(int(ip_str[2])>255) or(int(ip_str_str[0])<0)or(int(ip_str_str[0])>255)or(int(ip_str_str[1])<0)or(int(ip_str_str[1])>255)or(int(ip_str_str[0])>int(ip_str_str[1])):
        print("输入的ip格式不对")
        sys.exit()
    #print(port_str)
    if(int(port_str[0])<0)or(int(port_str[0])>65535)or(int(port_str[1])<0)or(int(port_str[1])>65535)or(int(port_str[0])>int(port_str[1])):
        print("输入端口格式不对")
        sys.exit()

def Tuple(ip:str,port:str):#产生由ip，port组合的元组，并将元组存入队列中
    global HOST
    ip_str=ip[:ip.rfind('.')+1]
    ip_id=int(ip[ip.rfind('.')+1:ip.rfind('~')])
    ip_end=int(ip[ip.rfind('~')+1:])
    port_str=int(port[:port.rfind('~')])
    port_end=int(port[port.rfind('~')+1:])
    for i in range(ip_id,ip_end+1):
        host=ip_str+str(i)
        for port in range(port_str,port_end+1):
            address=(host,port)
            #print(address)
            HOST.put(address)


def scan(address:tuple)->bool:#使用套接字发送连接请求，分析返回请求来判断端口是否打开
    h=socket.socket()#创建套接字
    r=h.connect_ex(address)
    h.settimeout(1)#设置超时
    if r==0 :
        return True
    return False

class works(Thread):#消费者
    def run(self) -> None:
        while True:
            add=HOST.get()#从队列中获取（先进先出）
            if scan(add):
                lock.acquire()#上锁
                print(f"{add}      OPEN")
                lock.release()#解锁

            HOST.task_done()


ip_true()
Tuple(IP,PORT)

for _ in range(thnum):#启动多线程并设置为守护线程，当队列中元组取尽，多线程停止
    work=works()
    work.daemon=True
    work.start()
HOST.join()





