import time

from app.core import process, log
from app.db import test_task_manage


def main():
    """
    分别查找待执行的测试用例集， 和测试用例列表，并执行。
    :return:
    """

    idList = test_task_manage.test_task_manage().test_suite_list()
    if len(idList):
        for caselist in idList:
            test_suite_id = caselist[0]
            runType = str(caselist[1])
            if  runType =='2' or runType =='Chrome':
                threadNum = 6
                runType = 'Chrome'
                process.process().runmain(test_suite_id, threadNum, runType)
        result1 = 0
    else:
        result1=1
    idList1 = test_task_manage.test_task_manage().test_case_list()
    if len(idList1):
        threadNum = 6
        process.process().multipleRun(idList1, threadNum)
        result2 = 0
    else:
        result2=1
    result = result1 +result2
    return result



def coreservice():
    """
    如果有待执行用例，则马上执行； 如果没有待执行的用例，则等待6秒进行下一次轮询。
    :return:
    """
    while (1):
        if(main()):
            time.sleep(6)

coreservice()