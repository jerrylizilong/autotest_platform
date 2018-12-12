import os,platform,datetime,time
import pytest
from app import config
from app.db import test_unittest_manage
currentPath = os.path.dirname(os.path.abspath(__file__))

def run_all():
    nowTime = time.strftime("%Y-%m-%d_%H_%M_%S", time.localtime())
    reportName = 'unittest_' + str(nowTime)
    reportFileName = reportName + '.html'
    test_folder = config.unittestPath
    reportNameFull = os.path.join(config.reportPath , reportFileName)

    start_time = datetime.datetime.now()
    pytest.main([test_folder,'--html=%s' %reportNameFull,'-o log_cli=true -o log_cli_level=INFO'])
    end_time = datetime.datetime.now()

    # 插入数据库
    test_unittest_manage.test_unittest_manage().new_unittest_case(reportName, start_time, end_time, reportFileName)


# run_test()

