from scapy.all import *

def packet_callback(packet):
    # 提取以太网头部
    ethernet_header = packet.getlayer(Ether)
    if ethernet_header is not None:
        # 提取源MAC地址和目标MAC地址
        source_mac = ethernet_header.src
        dest_mac = ethernet_header.dst
        # 打印MAC地址
        print(f"源MAC地址：{source_mac}")
        print(f"目标MAC地址：{dest_mac}")

    # 提取IP头部
    ip_header = packet.getlayer(IP)
    if ip_header is not None:
        # 提取源IP地址和目标IP地址
        source_ip = ip_header.src
        dest_ip = ip_header.dst
        # 打印IP地址
        print(f"源IP地址：{source_ip}")
        print(f"目标IP地址：{dest_ip}")

    print("")

# 设置嗅探过滤器
filter_str = "ip"

# 开始嗅探数据包
sniff(filter=filter_str, prn=packet_callback)
