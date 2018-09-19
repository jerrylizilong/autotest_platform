from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.mime.image import MIMEImage
from email.utils import parseaddr, formataddr

import smtplib
from app import config
from app.core import log


class sendEmail(object):
    def __init__(self):
        self.server_host = config.smtp_server_host
        self.server_port = config.smtp_server_port
        self.from_email = config.smtp_from_email
        self.default_to_email=config.smtp_default_to_email
        self.server_user = config.smtp_server_user
        self.server_password = config.smtp_server_password

    def _format_addrs(self,s):
        name, addr = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(), addr))

    def init_MIMEMultipart(self,to_email,title,content,filename=''):
        msg = MIMEMultipart()
        msg['From'] = self._format_addrs('Autotest platform: %s' % self.from_email)
        msg['To'] = self._format_addrs('User : %s' % to_email)
        msg['Subject'] = Header(title, 'utf-8').encode()
        msg.attach(MIMEText(content, 'plain', 'utf-8'))
        if filename !='':
            fp = open(file=filename.replace(u'\u202a', ''), mode='rb')
            msgImage = MIMEImage(fp.read())
            msgImage['Content-Type'] = 'application/octet-stream'
            msgImage['Content-Disposition'] = 'attachment;filename="1.png"'
            fp.close()
            msg.attach(msgImage)
        return msg

    def init_server(self):
        server = smtplib.SMTP(self.server_host, self.server_port)
        server.starttls()
        server.set_debuglevel(1)
        return server

    def sendEmail(self, to_email,title = 'test result', content='', filename=''):
        filename.replace("\\", '/')
        server = self.init_server()
        msg = self.init_MIMEMultipart(to_email,title,content,filename)
        try:
            server.login(self.server_user, self.server_password)
            server.sendmail(self.from_email, [to_email], msg.as_string())
        except smtplib.SMTPAuthenticationError as e:
            print(e)
        except smtplib.SMTPDataError as e:
            print(e)
        server.quit()

    def send_test_result(self,test_suit_id,to_email= []):
        if len(to_email)==0:
            to_email = [self.default_to_email]
        from app.db import test_batch_manage,test_suite_manage
        test_suit_id = str(test_suit_id)
        result = test_batch_manage.test_batch_manage().show_test_batch_status(test_suit_id)
        # print(result)
        test_title = 'test result for batch : ' + test_suit_id +'-'+test_suite_manage.test_suite_manage().search_test_suite(test_suit_id,'name')[0][0]
        test_result = 'id: %s, 总用例数：%s,  成功用例数：%s, 失败用例数: %s, 通过率： %s , 报告地址： %s' % (
            test_suit_id, result['total'], result['success'], result['fail'], result['successRate'],
            config.flask_host + '/test_batch_detail?test_suite_id=' + test_suit_id)
        self.sendEmail(to_email,test_title,test_result)

    def send_test_results(self,test_suite_list):
        for test_suite_id in test_suite_list:
            send_time = 3
            while send_time:
                log.log().logger.info('sending email for test suite: %s' % str(test_suite_id))
                try:
                    self.send_test_result(test_suite_id)
                    log.log().logger.info('sended email for test suite: %s' % str(test_suite_id))
                    break
                except:
                    log.log().logger.info('send error for the %s time!' %(4-send_time))
                    send_time += -1
