import queue
import threading
import time
from multiprocessing.dummy import Pool as ThreadPool
from retrying import retry
from selenium.common.exceptions import *
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from app import config
from app.core import buildCase, log, hubs, coredriver, util, atx_core,extend
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
        package = ''
        log.log().logger.info('开始执行 id ： %-10d | 用例 ：%s ' %(id,case))
        newstep,case = buildCase.buildCase().getCase(case)
        # print(newstep,case)
        if len(newstep):
            runType = newstep[0][0]
            if len(newstep[0][1]) == 1 :
                if newstep[0][1][0]!='1':
                    package = newstep[0][1][0]
            newstep.remove(newstep[0])
            case.remove(case[0])
            if runType == 'Android' and isUseATX:
                # 使用 atx 执行 Android 用例
                result, stepN,screenFileList = atx_core.atx_core().run_case(id,package,newstep,case,screenFileList,deviceList=deviceList)
                log.log().logger.info('%s, %s, %s' %(result, stepN,screenFileList))
            else:
                # 使用 selenium 执行 web 用例
                result,stepN,screenFileList = self.run_selenium(id,runType,package,newstep,case,screenFileList)
        else:
            result = '3'
            stepN = '公共方法不存在!'
        import datetime
        log.log().logger.info('id is %s, result is %s, stepname is %s' %(id,result,stepN))
        # 记录用例执行结果
        test_batch_manage.test_batch_manage().set_test_end(result, datetime.datetime.now(), stepN, screenFileList,id)
        return result


    def run_selenium(self,id,runType,package,newstep,case,screenFileList):
        # print(id,runType,package,newstep,case,screenFileList)
        result = '2'
        stepN = 'init'
        if runType != '' and package == '':
            driver = coredriver.coredriver().iniDriver(runType, devicename=package)
            if driver == 0:  # 没有可执行的节点，无法执行
                log.log().logger.info('cannot run without available hubs!')
                result = '3'
            else:
                if len(newstep) < 2:  # 用例中没有执行步骤，无法执行
                    result = '3'
                    stepN = 'no steps!'
                else:
                    for i in range(len(newstep)):  # 开始逐个步骤执行
                        stepN = case[i].replace('"', "'")
                        try:
                            result, stepN, screenFileList = self.do_step(driver, newstep[i], stepN, id, screenFileList)
                        except:
                            log.log().logger.error('id ： %-10d | 失败步骤：%s ' % (id, stepN))
                            result ='2'
                        if result == '2':
                            trytime = 2
                            while trytime:
                                try:
                                    result, screenFileList = extend.extend().screenshot(driver, id, screenFileList,
                                                                                         True)
                                    break
                                except UnexpectedAlertPresentException as e:
                                    log.log().logger.info(e)
                                    time.sleep(5)
                                    try:
                                        driver.switch_to.alert.accept()
                                    except:
                                        log.log().logger.error('no alert')
                                trytime += -1
                            break
                # for android driver ,the ending should by driver.quite();  for webdriver ,the ending is driver.close()

                try:
                    driver.quit()
                except WebDriverException as e:
                    log.log().logger.error(e)
                    try:
                        driver.close()
                    except WebDriverException as e:
                        log.log().logger.error(e)
        return result,stepN,screenFileList



    @retry(stop_max_attempt_number=3,wait_fixed=5000)
    def do_step(self,driver,steps,case,id,screenFileList):
        keyword = steps[0]
        stepN = keyword
        comed, element = buildCase.buildCase().build_case(keyword, steps[1])  # 转换为可执行语句
        result = '2'
        log.log().logger.info("id ： %-10d |  关键字： %-20s |  步骤：%-60s | 命令： %s" %(id, keyword,case, comed))
        try:
            if comed != '':
                if keyword == '截图':
                    result, screenFileList = extend.extend().screenshot(driver, id, screenFileList)
                else:
                    exec(comed)  # 执行语句
                    result = '1'
        except UnexpectedAlertPresentException as e:
            log.log().logger.info(e)
            try:
                driver.switch_to.alert.accept()
                result = '1'
            except :
                log.log().logger.error('no alert')
        else:
            stepN = 'no comed to run!'
        return result,stepN,screenFileList





    # multiple run, for android , the tread is 1; for webdriver , the thread could by more than 1.
    def multipleRun(self,caselist, threadNum):
        pool = ThreadPool(threadNum)
        pool.map(self.main, caselist)
        pool.close()
        pool.join()

    def runmain(self,test_suite_id,threadNum, runType ):
        if runType == 'Android' and isUseATX:
            Hubs = hubs.hubs().getDevices()
            log.log().logger.debug('Run type is ATX and usable devices are %s' %Hubs)
        else:
            Hubs = hubs.hubs().showHubs(runType)
        if len(Hubs) ==0:
            log.log().logger.debug('cannot run for no available hubs!')
        elif runType == 'Android' and isUseATX:
            self.atxMain()
        else:
            self.multipleRun(util.util().getTeseCases(test_suite_id),threadNum)
            test_task_manage.test_task_manage().update_test_suite_check()

    def atxMain(self):
        q = queue.Queue()
        Hubs = hubs.hubs().getDevices()
        alllist = util.util().getTeseCasesATX(all=True)
        if len(Hubs) and len(alllist):
            count = 0
            threads = []
            for i in range(len(Hubs)):
                j = Hubs[i]
                threads.append(MyThread(q, i, j))
            for mt in threads:
                mt.start()
                log.log().logger.info("start time: %s" %time.ctime())

        elif len(alllist):
            log.log().logger.debug('no device is avaible!')
        else:
            log.log().logger.debug('no test case is needed!')


class MyThread(threading.Thread):
    def __init__(self, q, t, j):
        super(MyThread, self).__init__()
        self.q = q
        self.t = t
        self.j = j

    def run(self):
        list0 = util.util().getTeseCasesATX(self.j,isRunning=True)
        if len(list0):
            log.log().logger.info('case still running !')
        else:
            list = util.util().getTeseCasesATX(self.j)
            if len(list):
                log.log().logger.info('start test by single devices :%s ' %list[0][0] )
                self.q.put(u"打点我是第%d个线程，ip: %s, 测试用例：%s" % (self.t, self.j,list[0][0]))
                log.log().logger.info(u"打点我是第%d个线程，ip: %s, 测试用例：%s" % (self.t, self.j,list[0][0]))
                process().main(list[0])
                time.sleep(2)
            else:
                list2 = util.util().getTeseCasesATX(all=True)
                log.log().logger.info('current list lenth is: %s'%len(list2))
                if len(list2):
                    try:
                        case = list2[self.t]
                    except:
                        case=list2[0]
                        log.log().logger.info('current ip is : %s'%str(self.j))
                    log.log().logger.info('start test by multiple devices :%s ' % case[0])
                    self.q.put(u"我是第%d个线程，ip: %s, 测试用例：%s" % (self.t, self.j, case[0]))
                    log.log().logger.info(u"打点我是第%d个线程，ip: %s, 测试用例：%s" % (self.t, self.j, case[0]))
                    process().main(case,deviceList=[str(self.j)])
                    time.sleep(3)
                else:
                    log.log().logger.info('no case !')
