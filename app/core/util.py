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
            log.log().logger.info(screen_shot_path)
            normalfilename =  screen_shot_path + 'normalScreenShot\\'  + str(caseNo)+'_success' + nowTime + '.jpg'
            errorfilename =  screen_shot_path + 'errorScreenShot\\'  + str(caseNo)+'_error' + nowTime + '.jpg'
            normalfilename1 =  '\\' +screen_shot_path1 + '\\' + 'normalScreenShot' + '\\' + str(caseNo)+'_success' + nowTime + '.jpg'
            errorfilename1 = '\\' + screen_shot_path1 + '\\' + 'errorScreenShot' + '\\' + str(caseNo)+'_error' + nowTime + '.jpg'
        else:
            screen_shot_path = config.screen_shot_path
            screen_shot_path1 = 'static/screenshot'
            normalfilename = screen_shot_path  + 'normalScreenShot' + '/'+ str(caseNo)+'_success' + nowTime + '.jpg'
            errorfilename = screen_shot_path  + 'errorScreenShot' + '/' + str(caseNo)+'_error' + nowTime + '.jpg'
            normalfilename1 =  '/' + screen_shot_path1 + '/' + 'normalScreenShot' + '/' + str(
                caseNo) + '_success' + nowTime + '.jpg'
            errorfilename1 =  '/' + screen_shot_path1 + '/' + 'errorScreenShot' + '/' + str(caseNo) + '_error' + nowTime + '.jpg'
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