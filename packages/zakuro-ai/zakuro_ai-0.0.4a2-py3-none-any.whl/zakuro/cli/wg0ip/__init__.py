import netifaces as ni

def main():
    ip = ni.ifaddresses('wg0')[ni.AF_INET][0]['addr']
    print(ip)
