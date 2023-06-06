import nmap
def NmapScan(address:tuple):#输入单个ip，判断ip是否存活,存活返回True
    # 实例化nmap端口扫描对象
    scaner = nmap.PortScanner()
    state=''
    # 执行scan()函数
    try:
        scaner.scan(address[0], address[1])
        # 获取tcp协议对应的端口状态
        state = scaner[address[0]]['tcp'][int(address[1])]['state']
        print(state)
    except Exception as e:
        pass
    if state == "open":
        return True
    return False
print(NmapScan(("192.168.2.133","135")))
