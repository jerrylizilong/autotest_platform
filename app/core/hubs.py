from app import useDB, config
from app.core import log,util
import json
class hubs():
    def IsOpen(self,ip, port):
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((ip, int(port)))
            s.shutdown(2)
            # 利用shutdown()函数使socket双向数据传输变为单向数据传输。shutdown()需要一个单独的参数，
            # 该参数表示了如何关闭socket。具体为：0表示禁止将来读；1表示禁止将来写；2表示禁止将来读和写。
            # log.log().logger.info('%s is open' % port)
            return True
        except:
            log.log().logger.info('%s is down' % port)
            return False

    def updateHub(self,ip, port,androidConnect, status):
        if port == 'all':
            useDB.useDB().insert("update test_hubs set status = 0 where ip = '%s';" % (ip))
            log.log().logger.info('update hub to unavailable: %s' % (ip))
        elif status == '1':
            sql = "select status from test_hubs where ip = '%s' and port = '%s' limit 1;" % (ip, port)
            result = useDB.useDB().search(sql)
            if androidConnect == '':
                if len(result) == 0:
                    useDB.useDB().insert("insert into test_hubs (ip, port) values ('%s','%s');" % (ip, port))
                    log.log().logger.info('add new hub to available: %s:%s' % (ip, port))
                elif result[0][0] != 1:
                    useDB.useDB().insert(
                        "update test_hubs set status = 1 where ip = '%s' and port = '%s' limit 1;" %(ip, port))
                    log.log().logger.info('update hub to available: %s:%s' % (ip, port))
                else:
                    log.log().logger.info('hub already available: %s:%s' % (ip, port))
            else:
                if len(result) == 0:
                    useDB.useDB().insert("insert into test_hubs (ip, port,androidConnect) values ('%s','%s',%s);" % (
                    ip, port, androidConnect))
                    log.log().logger.info('add new hub to available: %s:%s, %s' % (ip, port, androidConnect))
                elif result[0][0] != 1:
                    useDB.useDB().insert(
                        "update test_hubs set status = 1,androidConnect = %s where ip = '%s' and port = '%s' limit 1;" % (
                        androidConnect, ip, port))
                    log.log().logger.info('update hub to available: %s:%s,%s' % (ip, port, androidConnect))
                else:
                    log.log().logger.info('hub already available: %s:%s,%s' % (ip, port, androidConnect))
        elif status == '0':
            sql = "select status from test_hubs where ip = '%s' and port = '%s' limit 1;" % (ip, port)
            result = useDB.useDB().search(sql)
            if len(result) == 0:
                log.log().logger.info('hub does not exist: %s:%s, %s' % (ip, port,androidConnect))
            else:
                useDB.useDB().insert(
                    "update test_hubs set status = 0, androidConnect = 0 where ip = '%s' and port = '%s' limit 1;" % (ip, port))
                log.log().logger.info('update hub to unavailable: %s:%s' % (ip, port))


    def showHubs(self,runType):
        if runType == 'Android' or runType == 'iOS':
            sql = "select ip, port from test_hubs where status = '1' and androidConnect = '1';"
        else:
            sql = "select ip, port from test_hubs where status = '1';"
        result = useDB.useDB().search(sql)
        hubs = []
        if len(result):
            for hub in result:
                if self.IsOpen(hub[0],hub[1]):
                    hubs.append(hub)
                else:
                    self.updateHub(hub[0],hub[1],'0','0')
        if len(hubs) == 0:
            log.log().logger.error('no hubs is availabe!')
        return hubs

    def checkHubs(self):
        sql = "select ip, port from test_hubs;"
        result = useDB.useDB().search(sql)
        hubs = []
        if len(result):
            for hub in result:
                if self.IsOpen(hub[0],hub[1]):
                    hubs.append(hub)
                    self.updateHub(hub[0], hub[1],'', '1')
                else:
                    self.updateHub(hub[0], hub[1],'0','0')
        if len(hubs) == 0:
            log.log().logger.error('no hubs is availabe!')
        else:
            # log.log().logger.info('availables hubs are :')
            for i in range(len(hubs)):
                log.log().logger.info(hubs[i][0] + ':' + hubs[i][1])
        return hubs


    def searchHubs(self,id=''):
        if id!='':
            sql = "select id, ip, port, androidConnect,status from test_hubs where id = %s limit 1;" %str(id)
        else:
            sql = "select id, ip, port, androidConnect,status from test_hubs;"
        list = useDB.useDB().search(sql)
        log.log().logger.info('cases : %s' %list)
        results = []
        for i in range(len(list)):
            result = {}
            result['id'] = list[i][0]
            result['ip'] = list[i][1]
            result['port'] = list[i][2]
            result['androidConnect'] = list[i][3]
            result['status'] = list[i][4]
            results.append(result)
        return results

    def getDevices(self):
        url = config.ATXHost + '/list'
        response, content = util.util().send(url)
        content = json.loads(content)
        deviceList = []
        for device in content:
            if device['present']:
                deviceList.append(device['ip'] + ':7912')
            else:
                # log.log().logger.info(device['ip'] + ' is not ready!')
                pass
        return deviceList

    # 获取设备列表信息
    def getDevicesList(self):
        url = config.ATXHost + '/list'
        response, content = util.util().send(url)
        content = json.loads(content)
        deviceLists = []
        for device in content:
            deviceList = {}
            if device['present']:
                deviceList["ip"] = device['ip'] + ':7912'
                deviceList["model"] = device['model']
                deviceLists.append(deviceList)
            else:
                log.log().logger.info(device['ip'] + ' is not ready!')
        return deviceLists
