from app.core import log, buildCase, atx_steps
from app.db import test_batch_manage
import requests


class atx_core():

    # run a signle case.
    # the main method
    def run_case(self, steps, caseNo, deviceList=[]):
        search_result = test_batch_manage.test_batch_manage().search_test_batch_detail1(caseNo, ['ip'])
        if len(search_result):
            log.log().logger.info(search_result)
            log.log().logger.info(deviceList)
            if search_result['ip']:
                deviceList = [search_result['ip']]
                log.log().logger.info(deviceList)
        step_name = ''
        steps = steps.split(',')
        steps = buildCase.buildCase().readPublic(steps)
        step0 = steps[0].split('|')
        if len(step0) != 2:
            log.log().logger.error('android init is not defined!')
            return 2, 'init', []
        elif step0[0] != 'Android':
            log.log().logger.error('android init is not defined!')
            return 2, 'init', []
        else:
            package = step0[1]
            isConnected, device0, u = atx_steps.atx_driver().connectDevice(package, deviceList)
            log.log().logger.info(' is %s connected?  %s' % (device0, isConnected))
            if isConnected:
                log.log().logger.info('start runnning test on %s' % device0)
                screenFileList = []
                result = 1
                for step in steps:
                    log.log().logger.info('current step is: %s' % step)
                    if len(step) == 0:
                        pass
                    else:
                        step = step.split('|')
                        # log().logger.info(step)
                        if len(step) >= 1:
                            step_name = step[0]
                            log.log().logger.info(step_name)
                            if len(step) > 1:
                                detail = step[1].split('@@')
                                log.log().logger.info(detail)
                            else:
                                detail = []
                            trytime = 3
                            while trytime:
                                log.log().logger.info('try time: %s' % (4 - trytime))
                                try:
                                    u, result, screenFileList = atx_steps.atx_driver().run_step(u, step_name, detail,
                                                                                                caseNo, screenFileList)
                                except requests.exceptions.ConnectionError as e:
                                    log.log().logger.error(e)
                                    result = 2

                                if result == 2:
                                    log.log().logger.error('failed at %s : %s, try again!' % (step_name, detail))
                                    trytime += -1
                                else:
                                    trytime = 0
                                    log.log().logger.info('finish step %s : %s.' % (step_name, detail))
                            if trytime == 0 and result == 2:
                                log.log().logger.error('failed at %s : %s after trying 3 times!' % (step_name, detail))
                                break

                        else:
                            pass
                return result, step_name, screenFileList
            else:
                log.log().logger.info('package is not found in any device!')
                return 2, 'package not found', []
