import nmap

def main():
    nm = nmap.PortScanner()
    ips = list(nm.scan(hosts='10.13.13.0/24', arguments='-n -sP')["scan"].keys())
    print(ips)

