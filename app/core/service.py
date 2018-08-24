import threading, socket
import time
from app.core import log1,hubs

def tcplink(sock, addr):
    log1.log().logger.info('Accept new connection from %s:%s...' % addr)
    sock.send(b'Welcome!')
    while True:
        try:
            data = sock.recv(1024)
            # print(data.decode('utf-8'))
        except ConnectionResetError:
            hubs.hubs().updateHub(ip,'all','0','0')
            break
        time.sleep(1)
        ip = addr[0]
        port = data.decode('utf-8')
        # print(data.decode('utf-8'))
        if not data :
            break
        elif data.decode('utf-8') == 'exit':
            hubs.hubs().updateHub(ip,'all','0','0')
            break
        sock.send(('Hello, %s!' % data.decode('utf-8')).encode('utf-8'))
        log1.log().logger.info(data)
        androidConnect = '0'
        hubs.hubs().updateHub(ip,port,androidConnect,'1')

    log1.log().logger.info('Connection from %s:%s closed.' % addr)
    hubs.hubs().showHubs('')

def serveice():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0',9998))
    s.listen(5)
    log1.log().logger.info("waiting for connections...")
    while True:
        # 接受一个新连接:
        hubs.hubs().showHubs('')
        sock, addr = s.accept()
        # 创建新线程来处理TCP连接:
        t = threading.Thread(target=tcplink, args=(sock, addr))
        t.start()

serveice()



