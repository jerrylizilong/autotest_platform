from app import useDB,config
from app.core import log
import time,platform,os
import httplib2,json
class util():
    def getTeseCases(self,test_suite_id):
        case = useDB.useDB().search('select id, steps,browser_type from test_batch where test_suite_id = "%s" and status in ("0") limit 1000 ;' % test_suite_id) #and status = "2" limit 1
        # log.log().logger.info(case)
        return case

    def getTeseCasesATX(self,ip='', all=False, isRunning=False):
        if all:
            case = useDB.useDB().search('select id, steps,browser_type from test_batch where test_suite_id in (SELECT id FROM test_suite WHERE STATUS  in (0,2) AND run_type IN ("0" ,"Android")) and status ="0" limit 1000 ;' )
        elif isRunning:
            case = useDB.useDB().search(
                'select id, steps,browser_type from test_batch where test_suite_id in (SELECT id FROM test_suite WHERE  STATUS in (0,2) AND run_type IN ("0" ,"Android")) and status in ("4") and ip = "%s" limit 1000 ;' % ip)
        else:
            case = useDB.useDB().search('select id, steps,browser_type from test_batch where test_suite_id in (SELECT id FROM test_suite WHERE  STATUS in (0,2) AND run_type IN ("0" ,"Android")) and status in ("0") and ip = "%s" limit 1000 ;' %ip) #and status = "2" limit 1
        log.log().logger.info(case)
        return case

    def screenshot(self,screenShotType, caseNo):

        nowTime = time.strftime("%Y-%m-%d_%H_%M_%S", time.localtime())
        if platform.system() == 'Windows':
            screen_shot_path = config.screen_shot_path
            screen_shot_path1 = 'static\\screenshot\\'
            log.log().logger.debug(screen_shot_path)
            normalfilename =  screen_shot_path + 'normalScreenShot\\'  + str(caseNo)+'_success' + nowTime + '.png'
            errorfilename =  screen_shot_path + 'errorScreenShot\\'  + str(caseNo)+'_error' + nowTime + '.png'
            normalfilename1 =  '\\' +screen_shot_path1 + '\\' + 'normalScreenShot' + '\\' + str(caseNo)+'_success' + nowTime + '.png'
            errorfilename1 = '\\' + screen_shot_path1 + '\\' + 'errorScreenShot' + '\\' + str(caseNo)+'_error' + nowTime + '.png'
        else:
            screen_shot_path = config.screen_shot_path
            screen_shot_path1 = 'static/screenshot'
            normalfilename = screen_shot_path  + 'normalScreenShot' + '/'+ str(caseNo)+'_success' + nowTime + '.png'
            errorfilename = screen_shot_path  + 'errorScreenShot' + '/' + str(caseNo)+'_error' + nowTime + '.png'
            normalfilename1 =  '/' + screen_shot_path1 + '/' + 'normalScreenShot' + '/' + str(
                caseNo) + '_success' + nowTime + '.png'
            errorfilename1 =  '/' + screen_shot_path1 + '/' + 'errorScreenShot' + '/' + str(caseNo) + '_error' + nowTime + '.png'
        if screenShotType == 'error':
            return errorfilename,errorfilename1
        else:
            return normalfilename,normalfilename1

    def send(self,url):
        http = httplib2.Http(timeout=30)
        response = {}
        content = {}
        headers = {'Content-type': 'application/json;charset=utf8'}
        try:
            # print('url is :', url)
            response, content = http.request(url, 'GET')
            content = content.decode('utf-8')
        except httplib2.ServerNotFoundError as e:
            content["code"] = "Error"
            content["message"] = str(e)
            log.log().logger.error(e)
        except Exception as e:
            content["code"] = "Error"
            content["message"] = str(e)
            log.log().logger.error(e)
        return response, content

    def md5(self,preosign):
        import hashlib
        m = hashlib.md5()
        preosign = preosign.encode('utf-8')
        m.update(preosign)
        return m.hexdigest()

    def sendEmail(self,to_email, msg1,filename):
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart,MIMEBase
        from email.header import Header
        from email.mime.image import MIMEImage
        from email import encoders
        from email.utils import parseaddr,formataddr

        import smtplib
        from app import config
        server_host = config.server_host
        server_port = config.server_port
        from_email = config.from_email
        server_user = config.server_user
        server_password = config.server_password

        def _format_addrs(s):
            name,addr = parseaddr(s)
            return formataddr((Header(name,'utf-8').encode(),addr))

        # msg = MIMEText(msg1,'plain','utf-8')
        msg = MIMEMultipart()


        msg['From']=_format_addrs('Autotest platform: %s' %from_email)
        msg['To']=_format_addrs('User : %s' %to_email)
        msg['Subject']=Header(msg1,'utf-8').encode()

        msg.attach(MIMEText(msg1,'plain','utf-8'))
        # msg.attach()
        fp =  open(file=filename.replace(u'\u202a',''),mode='rb')
        msgImage = MIMEImage(fp.read())
        msgImage['Content-Type'] = 'application/octet-stream'
        msgImage['Content-Disposition'] = 'attachment;filename="1.png"'
        fp.close()
        # msgImage.add_header('Content-ID', '<image1>')
        msg.attach(msgImage)
        server = smtplib.SMTP(server_host,server_port)
        server.starttls()
        server.set_debuglevel(1)


        try:
            server.login(server_user,server_password)
            server.sendmail(from_email,[to_email],msg.as_string())
        except smtplib.SMTPAuthenticationError as e:
            print(e)
        except smtplib.SMTPDataError as e:
            print(e)
        server.quit()
