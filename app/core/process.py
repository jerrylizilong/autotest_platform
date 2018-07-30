import queue
import threading
import time
from multiprocessing.dummy import Pool as ThreadPool
import urllib,http

import requests
from selenium.common.exceptions import *
from selenium.webdriver.support.select import Select
from app import useDB, config
from app.core import buildCase, log, hubs, coredriver, util, extend
from app.db import test_task_manage,test_batch_manage

isUseATX = config.isUseATX

class process():

# run the case
    def main(self,case,deviceList=[]):
        result = 1
        id = case[0]
        test_batch_manage.test_batch_manage().set_test_running(id,deviceList)
        browserType = case[2]
        case = case[1]
        screenFileList = []
        devicename = ''
        log.log().logger.info('current case is : %s' %case)
        newstep = buildCase.buildCase().getCase(case)
        if len(newstep):
            runType = newstep[0][0]
            if len(newstep[0][1]) == 1 :
                if newstep[0][1][0]!='1':
                    package = newstep[0][1][0]
            if runType != 'Chrome' :
                log.log().logger.info('runtype is wrong : %s' %runType)
            else:
                # 使用 selenium 执行 web 用例
                if browserType !=''and devicename =='':
                    runType = browserType
                driver = coredriver.coredriver().iniDriver(runType,devicename=devicename)
                result = '2'
                stepN = 'init'
                if driver == 0: # 没有可执行的节点，无法执行
                    log.log().logger.info('cannot run without available hubs!')
                    result = '3'
                    stepN = 'init'
                else:
                    if len(newstep)<2:   # 用例中没有执行步骤，无法执行
                        result = '3'
                        stepN = 'no steps!'
                    else:
                        for i in range(1,len(newstep)):   # 开始逐个步骤执行
                            steps = newstep[i]
                            keyword = steps[0]
                            comed , element = buildCase.buildCase().build_case(keyword, steps[1])   # 转换为可执行语句
                            stepN = keyword
                            tryTimes = 0
                            result = '2'
                            while 1:
                                if keyword=='验证文字':
                                    result = extend.extend().assert_element_text(driver,comed)
                                elif keyword=='验证文字非':
                                    result = extend.extend().assert_element_text(driver,comed,isNot=True)
                                elif keyword=='验证':
                                    result = extend.extend().assert_text(driver,comed)
                                elif keyword=='截图':
                                    result, screenFileList = extend.extend().screenshot(driver,id,screenFileList)
                                else:
                                    try:
                                        log.log().logger.info(comed)
                                        result = '1'
                                        exec(comed)   #执行语句
                                    except requests.exceptions.HTTPError as e:
                                        log.log().logger.error(e)
                                        result = '2'
                                    except urllib.error.URLError as e:
                                        log.log().logger.error(e)
                                        result = '2'
                                    except NoSuchElementException as e:
                                        log.log().logger.error(e)
                                        try:
                                            driver.accept_alert()
                                        except :
                                            log.log().logger.error('no alert')
                                        try:
                                            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
                                        except :
                                            log.log().logger.error('cannot scroll')
                                        result = '2'
                                    except AttributeError as e:
                                        log.log().logger.info(e)
                                        try:
                                            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
                                        except :
                                            log.log().logger.error('cannot scroll')
                                        result = '2'
                                    except WebDriverException as e:
                                        log.log().logger.error(e)
                                        try:
                                            driver.accept_alert()
                                        except :
                                            log.log().logger.error('no alert')
                                        result = '2'
                                    except StaleElementReferenceException as e:
                                        log.log().logger.info(e)
                                        result = '2'
                                    except http.client.RemoteDisconnected as e:
                                        log.log().logger.info(e)
                                        result = '2'
                                if result == '2' :   # 步骤失败时，重试3次
                                    tryTimes +=1
                                    time.sleep(2)
                                else:
                                    break
                                log.log().logger.info('try times :%s, result is: %s' %(tryTimes, result))
                                if result == '2' and tryTimes ==3:  # 失败3次，自动截图
                                    retryScreenshot = 2
                                    while retryScreenshot:
                                        try:
                                            result, screenFileList =extend.extend().screenshot(driver,id,screenFileList,True)
                                            break
                                        except WebDriverException as e:
                                            log.log().logger.error(e)
                                            driver.switch_to_default_content()
                                            retryScreenshot +=-1
                                # break
                                if result == '2' and tryTimes >=3:  # 失败3次，跳出
                                    break
                            if result == '2' :  # 失败3次，跳出
                                break
                    try:
                        driver.quit()
                    except WebDriverException as e:
                        log.log().logger.error(e)
                        try:
                            driver.close()
                        except WebDriverException as e:
                            log.log().logger.error(e)
        else:
            result = '3'
            stepN = '公共方法不存在!'
        import datetime
        log.log().logger.info('id is %s, result is %s, stepname is %s' %(id,result,stepN))
        # 记录用例执行结果
        test_batch_manage.test_batch_manage().set_test_end(result, datetime.datetime.now(), stepN, screenFileList,id)
        return result

# multiple run, for webdriver , the thread could by more than 1.
    def multipleRun(self,caselist, threadNum):
        pool = ThreadPool(threadNum)
        pool.map(self.main, caselist)
        pool.close()
        pool.join()

    def runmain(self,test_suite_id,threadNum, runType ):
        Hubs = hubs.hubs().showHubs(runType)
        if len(Hubs) ==0:
            log.log().logger.error('cannot run for no available hubs!')
        else:
            self.multipleRun(util.util().getTeseCases(test_suite_id),threadNum)
            test_task_manage.test_task_manage().update_test_suite_check()

