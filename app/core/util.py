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

        screen_shot_path = config.screen_shot_path
        nowTime = time.strftime("%Y-%m-%d_%H_%M_%S", time.localtime())
        normalfile = str(caseNo)+'_success' + nowTime + '.png'
        errorfile = str(caseNo)+'_error' + nowTime + '.png'

        normalfilename = os.path.join(screen_shot_path,'normalScreenShot',normalfile)
        normalfilename1 = os.path.join('static','screenshot','normalScreenShot',normalfile)

        errorfilename = os.path.join(screen_shot_path,'errorScreenShot',errorfile)
        errorfilename1 = os.path.join('static','screenshot','errorScreenShot',errorfile)

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

