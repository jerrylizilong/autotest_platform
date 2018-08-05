DBtype =  '2'   # '1' : sqlite,  2: mysql
host='localhost'
port='3306'
user='root'
password='jerryli'
database='test_auto_new'

isUseATX=True

import os,platform
currentPath = os.path.dirname(os.path.abspath(__file__))
print(currentPath)
if platform.system()=='Windows':
    logPath = currentPath + '\\log\\'
    reportPathWin = currentPath + '\\templates\\reports\\'
    unittestPathWin = currentPath + '\\test\\'
    screen_shot_path = currentPath + '\\static\\screenshot\\'
else:
    reportPathLinux =currentPath + '/templates/reports/'
    unittestPathLinux = currentPath + '/test/'
    logPath = currentPath + '/log/'
    screen_shot_path = currentPath +'/static/screenshot/'




