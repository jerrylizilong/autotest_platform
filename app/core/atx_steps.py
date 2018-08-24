import requests
import time

import uiautomator2 as ut2

from app.core import log, util, buildCase, hubs


class atx_driver():

    # connect to an availble android device.   if deviceList is not given, it will try to connect to availbe device in database.
    def connectDevice(self, package, deviceList=[]):
        if len(deviceList) == 0:
            deviceList = hubs.hubs().getDevices()
        isConnected = 0
        device0 = ''
        for device in deviceList:
            isConnected, u = self.init(device)
            if isConnected:
                if self.start_app(u, package) != 0:
                    device0 = device
                    return isConnected, device0, u
                else:
                    isConnected = 0
                    device0 = ''
                    log.log().logger.error('package not found!')
        return 0, '', ''

    # init and try to unlock the device.
    def init(self, device=''):
        log.log().logger.info('trying to connect device : %s' % device)
        try:
            u = ut2.connect(device)
            log.log().logger.info(u.device_info)
            isConnected = 1
        except requests.exceptions.ConnectionError as e:
            log.log().logger.error(e)
            isConnected = 0
            u = ''
        return isConnected, u

    # 通过 adb 查询当前包是否已安装。 需要USB 链接，暂时不是使用。
    def is_app_exist0(self, package):
        import subprocess
        cmd = 'dumpsys package %s | grep version' % package
        cmds = [cmd, "exit", ]

        pipe = subprocess.Popen("adb shell", stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        code = pipe.communicate(("\n".join(cmds) + "\n").encode())

        log.log().logger.info(code)
        return 'versionCode' in str(code)

    # 通过 adb 查询当前包是否已安装。 不需要USB 链接，目前使用
    def is_app_exist(self, u, package):
        cmd = 'dumpsys package %s | grep version' % package
        result = u.adb_shell(cmd)
        log.log().logger.info(result)
        return 'versionCode' in str(result)

    # start the testing app.    for example , com.ghw.sdk2
    def start_app(self, u, package):
        # try to unlock device.
        try:
            log.log().logger.info('trying to unlock...')
            u.unlock()
        except requests.exceptions.ReadTimeout as e:
            log.log().logger.error(e)
            try:
                log.log().logger.info('trying to unlock again...')
                u.app_start('xdf.android_unlock')
            except requests.exceptions.ReadTimeout as e:
                log.log().logger.error(e)
        time.sleep(2)
        log.log().logger.info('trying to swipe up...')
        u.swipe_points([(0.509, 0.601), (0.503, 0.149)], 0.2)
        time.sleep(2)
        log.log().logger.info('trying to start app...')
        u.app_clear(package)
        u.app_start(package, stop=True, unlock=True)
        time.sleep(2)
        if self.is_app_exist(u, package):
            log.log().logger.info('package found, start testing!')
            time.sleep(2)
            u1, result1 = self.click(u, 'name', '允许')
            time.sleep(1)
            if result1 == 2:
                u1, result1 = self.click(u, 'name', '始终允许')
                time.sleep(1)
            if result1 == 2:
                u1, result1 = self.click(u, 'name', 'ALLOW')
                time.sleep(1)
            return u
        else:
            log.log().logger.error('package is not found in this device , try to connect another !')
            return 0

    # save a screenshot to corresponding folder.
    def take_screenshot(self, u, type, caseNo, screenFileList):
        fileName, fileName1 = util.util().screenshot(type, caseNo)
        image = u.screenshot()
        image.save(fileName)
        screenFileList.append(fileName1)
        return screenFileList

    # type text into the target element.
    # method :  id, name     the method used to locate the target element.
    # resource_id : target element's attribute, with which to locate target.
    def type_text(self, u, method, resource_id, text):
        if method == 'id':
            if u(resourceId=resource_id).exists:
                u(resourceId=resource_id).send_keys(text)
                time.sleep(1)
                result = 1
                u.adb_shell('input', 'keyevent', 'BACK')
                time.sleep(1)
            else:
                log.log().logger.error(u"出错了，没有找到元素！ by %s , %s" % (method, resource_id))
                result = 2
        elif method == 'name':
            if u(text=resource_id).exists:
                u(text=resource_id).send_keys(text)
                time.sleep(1)
                result = 1
                u.adb_shell('input', 'keyevent', 'BACK')
                time.sleep(1)
            else:
                log.log().logger.error(u"出错了，没有找到元素！ by %s , %s" % (method, resource_id))
                result = 2
        elif method == 'class':
            if u(className=resource_id).exists:
                u(className=resource_id).send_keys(text)
                time.sleep(1)
                result = 1
                u.adb_shell('input', 'keyevent', 'BACK')
                time.sleep(1)
            else:
                log.log().logger.error(u"出错了，没有找到元素！ by %s , %s" % (method, resource_id))
                result = 2
        else:
            log.log().logger.error(u"元素方法未定义！ %s" % method)
            result = 2
        return u, result

    def click(self, u, by, text):
        result = 2
        if by == 'name':
            u, result = self.click_text(u, text)
        elif by == 'id':
            u, result = self.click_id(u, text)
        elif by == 'description':
            u, result = self.click_description(u, text)
        elif by == 'class':
            u, result = self.click_class(u, text)
        return u, result

    # click an element locating by it's text name.
    def click_text(self, u, text):
        if u(text=text).exists:
            u(text=text).click()
            time.sleep(1)
            result = 1
        else:
            log.log().logger.error(u"出错了，没有找到元素！ by %s , %s" % ('text', text))
            result = 2
        return u, result

    # click an element locating by it's resourceId.
    def click_id(self, u, id):
        if u(resourceId=id).exists:
            u(resourceId=id).click()
            time.sleep(1)
            result = 1
        else:
            log.log().logger.error(u"出错了，没有找到元素！ by %s , %s" % ('id', id))
            result = 2
        return u, result

    # click an element locating by it's description.
    def click_description(self, u, id):
        if u(description=id).exists:
            u(description=id).click()
            time.sleep(1)
            result = 1
        else:
            log.log().logger.error(u"出错了，没有找到元素！ by %s , %s" % ('description', id))
            result = 2
        return u, result

    # click an element locating by it's className.
    def click_class(self, u, id):
        if u(className=id).exists:
            u(className=id).click()
            time.sleep(1)
            result = 1
        else:
            log.log().logger.error(u"出错了，没有找到元素！ by %s , %s" % ('className', id))
            result = 2
        return u, result

    # Send event to data collection.     used to test sending data in SDK demo.
    def sendData(self, u, name):
        u, result = self.click_text(u, name)
        time.sleep(2)
        if result == 1:
            if u(text='发送').exists:
                u, result = self.click_text(u, '发送')
            else:
                u, result = self.click_text(u, 'SEND')
            u.adb_shell('input', 'keyevent', 'BACK')
            time.sleep(1)
        return u, result

    # run step.
    # if a new step type is defined, it should be added to the step_name list.
    def run_step(self, u, step_name, detail, caseNo, screenFileList):
        result = 1
        if step_name == 'Android':
            time.sleep(1)
        elif step_name == '点击':
            u, result = self.click(u, detail[0], detail[1])
        elif step_name == '尝试点击':
            self.click(u, detail[0], detail[1])
        elif step_name == '等待':
            time.sleep(int(detail[0]))
        elif step_name == '发送':
            u, result = self.sendData(u, detail[0])
        elif step_name == '填写':
            u, result = self.type_text(u, detail[0], detail[1], detail[2])
        elif step_name == '返回':
            u.adb_shell('input', 'keyevent', 'BACK')
            time.sleep(1)
        elif step_name == '截图':
            screenFileList = self.take_screenshot(u, 'normal', caseNo, screenFileList)
        else:
            result = 2
            log.log().logger.error('method is not defined : %s' % step_name)
        if result == 0:
            log.log().logger.error('package is not fould!')
        elif result == 2:
            screenFileList = self.take_screenshot(u, 'fail', caseNo, screenFileList)
        return u, result, screenFileList
