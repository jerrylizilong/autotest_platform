from selenium import webdriver
from selenium.common.exceptions import *
from app.core import log,hubs
import http

class coredriver():

    def serverUrl(self,servers):
        server_url = {}
        import random
        i = random.randint(0,100)%len(servers)
        log.log().logger.debug('%s, %s' %(i,len(servers)))
        server_url['hostname']=servers[i][0]
        server_url['port'] = servers[i][1]
        return "http://%s:%s/wd/hub" %(server_url['hostname'],server_url['port'])

        # init the driver. if runType is Android, the package is required

    def iniDriver(self, runType,devicename = ''):
        log.log().logger.debug('RUNTYPE is : %s' %runType)
        servers = hubs.hubs().showHubs(runType)
        log.log().logger.debug(servers)
        if len(servers):
            server_url = self.serverUrl(servers)
            if runType == 'Chrome':
                desired_caps_web = webdriver.DesiredCapabilities.CHROME.copy()
                deviceList = ['Galaxy S5', 'Nexus 5X', 'Nexus 6P', 'iPhone 6', 'iPhone 6 Plus', 'iPad', 'iPad Pro']
                if devicename!='' :
                    if devicename not in deviceList:
                        devicename = deviceList[2]
                    chrome_option = {
                        'args': ['lang=en_US','start-maximized'],
                        'extensions': [], 'mobileEmulation': {'deviceName': ''}

                    }
                    chrome_option['mobileEmulation']['deviceName'] = devicename
                else:
                    chrome_option = {
                        'args': ['lang=en_US','--start-maximized'],
                        'extensions': []
                    }
                desired_caps_web['goog:chromeOptions']=chrome_option
            elif runType == 'Firefox':
                desired_caps_web = webdriver.DesiredCapabilities.FIREFOX.copy()
            else:
                log.log().logger.error("browser not support! %s " %runType)
                return 0
            log.log().logger.debug(desired_caps_web)
            retry = 2
            while retry:
                try:
                    log.log().logger.debug("start session %s time!" %(3-retry))
                    driver = webdriver.remote.webdriver.WebDriver(command_executor=server_url,desired_capabilities=desired_caps_web)
                    break
                except WebDriverException as e:
                    log.log().logger.info(e)
                    # retry +=-1
                except ConnectionResetError as e:
                    log.log().logger.info(e)
                except http.client.RemoteDisconnected as e:
                    log.log().logger.info(e)
                    # retry +=-1
                finally:
                    retry +=-1
            if retry == 0:
                return 0
            else:
                if devicename =='':
                    try:
                        driver.maximize_window()
                        if driver.get_window_size()['height']<1920:
                            log.log().logger.debug(driver.get_window_size()['height'])
                            driver.set_window_size(1920, 1080)   #最大化失败，则手动
                    except WebDriverException as e:
                        # log.log().logger.info(e)
                        try:
                            driver.set_window_size(1920, 1080)   #最大化失败，则手动
                        except WebDriverException as e:
                            log.log().logger.info(e)
                return driver
        else:
            return 0