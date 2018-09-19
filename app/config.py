DBtype =  '2'   # '1' : sqlite,  2: mysql
host='localhost'
port='3306'
user='root'
password='yourpassword'
database='test_auto_new'

isUseATX=True
ATXHost = 'http://localhost:8000'

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

is_email_enable = False
flask_host = 'http://localhost:5000'  # 邮件中的报告链接会使用
smtp_server_host = 'smtp.163.com'
smtp_server_port = '25'
smtp_from_email = 'youraccount@163.com'
smtp_default_to_email = 'youraccount@163.com'
smtp_server_user = smtp_from_email
smtp_server_password = 'yourpassword'

