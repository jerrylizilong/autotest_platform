import time

from app.core import process, log
from app.db import test_task_manage


def main():

    idList = test_task_manage.test_task_manage().test_suite_list(runtype='0')
    idList1 = test_task_manage.test_task_manage().test_case_list(isATX=True)
    if len(idList):
        for caselist in idList:
            test_suite_id = caselist[0]
            runType = str(caselist[1])
            if runType =='0' or runType =='Android':
                threadNum = 1
                runType ='Android'
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