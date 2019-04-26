import time

from app.core import process, log
from app.db import test_task_manage


def main():
    """
    查找待执行的测试用例列表，并执行。
    :return:
    """
    idList1 = test_task_manage.test_task_manage().test_case_list(isATX=True)
    if len(idList1):
        process.process().atxMain()
        result2 = 0
    else:
        result2=1
    result = result2
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