两种不同方式的端口扫描方法：
port.py：基于socket库的端口扫描工具
nmap_scan.py：基于nmap的端口扫描工具
两款工具使用方法相同

例如：
python port.py 192.168.1.1-255 0-65535 400
python nmap_scan.py 192.168.1.1-255 0-65535 400