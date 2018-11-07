from app.core import log, atx_steps
from app.db import test_batch_manage
from retrying import retry

class atx_core():

    # run a signle case.
    # the main method
    def run_case(self,id,package,newstep,case,screenFileList,deviceList = []):
        result = '2'
        stepN = 'init'
        search_result = test_batch_manage.test_batch_manage().search_test_batch_detail1(id, ['ip'])
        if len(search_result):
            log.log().logger.info(search_result)
            log.log().logger.info(deviceList)
            if search_result['ip']:
                deviceList = [search_result['ip']]
                log.log().logger.info(deviceList)

        isConnected,device0,u = atx_steps.atx_driver().connectDevice(package,deviceList)
        log.log().logger.info(' is %s connected?  %s' %(device0, isConnected))
        if isConnected:
            for i in range(len(newstep)):
                stepN = case[i].replace('"', "'")
                u, result, screenFileList = self.do_step(u,newstep[i], stepN,id,screenFileList)
                if result=='2':
                    break
            return result,stepN,screenFileList
        else:
            log.log().logger.info('package is not found in any device!')
            return '2', 'package not found', []


    @retry(stop_max_attempt_number=3,wait_fixed=5000)
    def do_step(self,u, steps,case,id,screenFileList):
        keyword = steps[0]
        log.log().logger.info("id ： %-10d |  关键字： %-20s |  步骤：%-60s | 命令： %s" % (id, keyword, case, steps[1]))
        if keyword == '截图':
            result,screenFileList = atx_steps.atx_driver().take_screenshot(u,'normal', id, screenFileList)
        else:
            u, result, screenFileList=atx_steps.atx_driver().run_step(u, keyword, steps[1], id, screenFileList)
        try:
            assert result == '1'
        except AssertionError as e:
            print(e)
        return u,result, screenFileList

