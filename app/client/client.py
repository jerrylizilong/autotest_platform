import os, subprocess,platform,socket
## 修改host 为对应服务器地址
host = 'localhost'
serverPort = 9998
port0 = '4444'

def connectDevcie():
    '''''检查设备是否连接成功，如果成功返回True，否则返回False'''
    try:
        '''''获取设备列表信息，并用"\r\n"拆分'''
        deviceInfo = str(subprocess.check_output('adb devices')).split("\\r\\n")
        print(deviceInfo)
        '''''如果没有链接设备或者设备读取失败，第二个元素为空'''
        if deviceInfo[1] == '':
            return False
        else:
            print(deviceInfo[1])
            return True
    except Exception as e:
        print( "Device Connect Fail:", e)

def IsOpen(ip,port):
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        s.connect((ip,int(port)))
        s.shutdown(2)
        #利用shutdown()函数使socket双向数据传输变为单向数据传输。shutdown()需要一个单独的参数，
        #该参数表示了如何关闭socket。具体为：0表示禁止将来读；1表示禁止将来写；2表示禁止将来读和写。
        print ('%s is open' % port )
        return True
    except:
        print( '%s is down' % port  )
        return False

def newHub(isOpen):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 建立连接:
    try:
        s.connect(( host, serverPort))
        # 接收欢迎消息:
        print(s.recv(1024).decode('utf-8'))
        data = str(port0).encode('utf-8')
        print(data)
        s.send(data)
        print(s.recv(1024).decode('utf-8'))
        if not isOpen:
            os.system('java -jar "selenium-server-standalone-3.11.0.jar" -port %s' %port0)
    except:
        print('host is not avaiable')

if platform.system() == 'Windows':
    newHub(IsOpen('127.0.0.1', port0))
else:
    print('other system is not supported yet !')
