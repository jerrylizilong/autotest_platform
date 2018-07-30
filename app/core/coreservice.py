import time

from app.core import process, log
from app.db import test_task_manage


def main():
    test_task_manage.test_task_manage().update_test_suite_check()
    idList = test_task_manage.test_task_manage().test_suite_list()
    idList1 = test_task_manage.test_task_manage().test_case_list()
    # log.log().logger.info(idList)
    result1=0
    result2=0
    if len(idList):
        for caselist in idList:
            test_suite_id = caselist[0]
            runType = str(caselist[1])
            if runType =='0' or runType =='Android':
                threadNum = 1
                runType ='Android'
            elif  runType =='2' or runType =='Chrome':
                threadNum = 6
                runType = 'Chrome'
            else:
                threadNum = 0
                runType = ''
            if runType == '':
                test_task_manage.test_task_manage().update_test_suite(test_suite_id, '3')
            else:
                test_task_manage.test_task_manage().update_test_suite(test_suite_id, '2')
                process.process().runmain(test_suite_id, threadNum, runType)
        result1 = 0
    else:
        result1=1
    if len(idList1):
        threadNum = 1
        process.process().multipleRun(idList1, threadNum)
        result2 = 0
    else:
        result2=1
    result = result1 +result2
    return result



def coreservice():
    while (1):
        if(main()):
            time.sleep(6)

coreservice()