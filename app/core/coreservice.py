import time

from app.core import process, log
from app.db import test_task_manage


def main():

    idList = test_task_manage.test_task_manage().test_suite_list()
    idList1 = test_task_manage.test_task_manage().test_case_list()
    if len(idList):
        for caselist in idList:
            test_suite_id = caselist[0]
            runType = str(caselist[1])
            if runType =='0' or runType =='Android':
                threadNum = 1
                runType ='Android'
            elif runType =='1' or runType =='iOS':
                threadNum = 1
                runType ='iOS'
            elif  runType =='2' or runType =='Chrome':
                threadNum = 6
                runType = 'Chrome'
            else:
                threadNum = 0
                runType = ''
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