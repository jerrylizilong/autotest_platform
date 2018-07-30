import datetime
import platform
import time
import unittest

import HTMLReport

from app import config
from app.db import test_unittest_manage
from app.test import log


def run_all():
    # 通过配置项，读取报告的存储路径 reportPath
    if platform.system() == 'Windows':
        reportPath = config.reportPathWin
        currentPath=config.unittestPathWin
    else:
        reportPath = config.reportPathLinux
        currentPath = config.unittestPathLinux
    # 获取当前路径
    # currentPath = os.getcwd()
    log.log().logger.info('reportPath is %s: ' %reportPath)
    log.log().logger.info('currentPath is %s: ' %currentPath)
    nowTime = time.strftime("%Y-%m-%d_%H_%M_%S", time.localtime())
    reportName = 'unittest_'+str(nowTime)
    reportFileName = reportName+'.html'

    suite = unittest.TestSuite()
    loader = unittest.TestLoader()
    # 执行当前  test 路径下的所以  test 类
    suite.addTests(loader.discover(currentPath))

    # 测试用例执行器
    runner = HTMLReport.TestRunner(report_file_name=reportName,  # 报告文件名，默认“test”
                                   output_path=reportPath,  # 保存文件夹名，默认“report”
                                   verbosity=3,  # 控制台输出详细程度，默认 2
                                   title='测试报告',  # 报告标题，默认“测试报告”
                                   description='无测试描述',  # 报告描述，默认“无测试描述”
                                   thread_count=1,  # 并发线程数量（无序执行测试），默认数量 1
                                   sequential_execution=True  # 是否按照套件添加(addTests)顺序执行，
                                   # 会等待一个addTests执行完成，再执行下一个，默认 False
                                   )
    # 执行测试用例套件
    start_time =datetime.datetime.now()
    runner.run(suite)
    end_time = datetime.datetime.now()

    #插入数据库
    test_unittest_manage.test_unittest_manage().new_unittest_case(reportName, start_time, end_time, reportFileName)

