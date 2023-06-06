import nmap
import sys
from queue import Queue
from threading import Thread,Lock

lock=Lock()
r=sys.argv
ip=r[1]
port=r[2]
IP=[]
PORT=[]
IP_1=[]
tumber=r[3]
close = ['closed', 'unfiltered', 'closed | filtered']#包含nmap扫端口关闭的几种情况，用来判断端口是否关闭
addre=Queue()#用于存放ip跟port组成的元组，用来控制线程结束

def get_ip():#用来解析ip，将字符串解析为ip所组成的列表
    global IP
    global ip
    ip_str=ip[:ip.rfind('.')+1]
    ip_start=int(ip[ip.rfind('.')+1:ip.find('-')])
    ip_end=int(ip[ip.find('-')+1:])
    for i in range(ip_start,ip_end+1):
        IP.append(ip_str+str(i))

def get_port():#用于解析端口字符串，转化为端口所组成的列表
    global port
    global PORT
    # split（）：用指定字符分割字符串，分割后的结果仍然为列表
    port_start = int(port.split('-')[0])  # 获取端口范围的起始值
    port_end = int(port.split('-')[1])  # 获取端口范围的结束值
    for i in range(port_start, port_end + 1):  # 左闭右开区间，end需要+1
        PORT.append(i)
def ip_true():#用来判断输入的ip跟端口的格式是否正确，ip不大于255.255.255。255，不小于0.0.0.0，端口不小于0，不大于65535，前面输入的ip不大于后面输入的ip，前面输入的端口不大于后面输入的端口2
    global ip
    global port
    ip_str=ip.split('.')
    #print(ip_str[3])
    port_str=port.split('-')
    ip_str_str=ip_str[3].split('-')
    if (int(ip_str[0])<0)or(int(ip_str[0])>255) or (int(ip_str[1])<0)or(int(ip_str[1])>255) or (int(ip_str[2])<0)or(int(ip_str[2])>255) or(int(ip_str_str[0])<0)or(int(ip_str_str[0])>255)or(int(ip_str_str[1])<0)or(int(ip_str_str[1])>255)or(int(ip_str_str[0])>int(ip_str_str[1])):
        print("输入的ip格式不对")
        sys.exit()#如果格式不对，直接停止程序
    #print(port_str)
    if(int(port_str[0])<0)or(int(port_str[0])>65535)or(int(port_str[1])<0)or(int(port_str[1])>65535)or(int(port_str[0])>int(port_str[1])):
        print("输入端口格式不对")
        sys.exit()#端口格式不对结束程序
def Tuple():#将ip所组成的列表和port所组成的列表遍历，组成一个由ip和port共同组成的元组并存入队列中用于控制多线程结束
    global IP_1
    global PORT
    global addre
    for i in IP_1:
        for j in PORT:
            add=(i,str(j))
            #print(add)
            addre.put(add)#将组成的元组存入addre（队列）

def NmapScan(targetIP):#输入单个ip，判断ip是否存活,存活返回True
    nm = nmap.PortScanner()#创建Portscanner对象
    try:
        result = nm.scan(hosts=targetIP, arguments='-sn -PE')#发送icmp数据包，判断该ip是否存活
        state = result['scan'][targetIP]['status']['state']
        return True#nmap扫描未存活的ip会报错，如果没有报错则确定为存活的ip
    except Exception as e:
        pass
def ip_server():#根据上面Nmapscan函数判断存活ip，将存活的ip全部存入一个新的数组中
    global IP
    global IP_1
    for i in IP:
        if NmapScan(i)==True:
            IP_1.append(i)



def port_server(address:tuple):#给定一个ip和port构成的元组，端口开放返回True
    ip=address[0]
    port=address[1]
    scan=nmap.PortScanner()
    scan.scan(ip,port,"-sV")
    #print(scan.all_hosts())
    for ip in scan.all_hosts():
        for port in scan[ip].all_tcp():
            status=scan[ip]['tcp'][port]["state"]
            if status not in close:
                return True



class Customer(Thread):  # 消费者
    def run(self) -> None:
        while True:
            address = addre.get()  # 从队列中取
            if port_server(address):  # 判断返回值
                lock.acquire()  # 加锁，一行只能打印一个
                print(f'【*】{address[0]}\t{address[1]}\tOPEN')
                lock.release()

            addre.task_done()  # 做完通知队列

def main():
    ip_true()#判断ip，port是否正确
    get_ip()#解析ip
    get_port()#解析端口
    ip_server()#将存活ip存入新的列表中
    Tuple()#将ip和port组成元组并存入队列中
    global tumber#线程
    for _ in range(int(tumber)):#启动多线程，并设置为守护线程
        c = Customer()
        c.daemon = True
        c.start()

    addre.join()


if __name__ == '__main__':
    main()












