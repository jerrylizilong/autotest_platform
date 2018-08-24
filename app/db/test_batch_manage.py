import string

from app import useDB, log
from app.db import test_case_manage, test_suite_manage


class test_batch_manage(object):
    def __init__(self):
        self.status = 0
        self.name = ''

    def new_test_batch(self,test_suite_id, test_case_id,name, steps,browser_type='Chrome'):
        log.log().logger.info('%s,%s,%s,%s' %(test_case_id,test_suite_id,name,steps))
        steps.replace('"','""')
        import re
        steps = re.sub('"', '""', steps)
        sql = string.Template('insert into test_batch (test_suite_id, test_case_id, name,steps,browser_type) values ("$test_suite_id","$test_case_id","$name","$steps","$browser_type");')
        sql = sql.substitute(test_suite_id = test_suite_id, test_case_id = test_case_id,steps=steps, name = name,browser_type=browser_type)
        useDB.useDB().insert(sql)

    def new_test_batch_IP(self, test_suite_id, test_case_id, name, steps,ip):
        log.log().logger.info('%s,%s,%s,%s' %(test_case_id, test_suite_id, name, steps))
        steps.replace('"', '""')
        import re
        steps = re.sub('"', '""', steps)
        sql = string.Template(
            'insert into test_batch (test_suite_id, test_case_id, name,steps,ip) values ("$test_suite_id","$test_case_id","$name","$steps","$ip");')
        sql = sql.substitute(test_suite_id=test_suite_id, test_case_id=test_case_id, steps=steps, name=name,ip=ip)
        useDB.useDB().insert(sql)

    def search_test_batch(self,id):
        sql = string.Template('select steps from test_batch where id = "$id";')
        sql = sql.substitute(id = id)
        return useDB.useDB().search(sql)[0]

    def search_test_batch_detail(self ):
        sql = 'select * from test_batch limit 10;'
        results = useDB.useDB().search(sql)
        users = []
        data = {}
        for r in results:
            user = {}
            user['id'] = r[0]
            user['batch_id'] = r[1]
            user['case_id'] = r[2]
            user['status'] = r[3]
            user['steps'] = r[4]
            users.append(user)

        data['code'] = 0
        data['cases'] = users
        log.log().logger.info(users)
        return users

    def search_test_batch_detail(self,id,fieldlist):
        search_value = fieldlist[0]
        for i in range(1,len(fieldlist)):
            search_value = search_value + ','+fieldlist[i]
        sql = 'select ' + search_value + ' from test_case where id = "' + str(id) + '";'
        result = useDB.useDB().search(sql)
        log.log().logger.info(result)
        if len(result):
            result = result[0]
            results = {}
            results['id'] = id
            for i in range(len(fieldlist)):
                results[fieldlist[i]] = result[i]
        else:
            results = []
        return results


    def search_test_batch_detail1(self,id,fieldlist):
        search_value = fieldlist[0]
        for i in range(1,len(fieldlist)):
            search_value = search_value + ','+fieldlist[i]
        sql = 'select ' + search_value + ' from test_batch where id = "' + str(id) + '";'
        result = useDB.useDB().search(sql)
        log.log().logger.info(result)
        if len(result):
            result = result[0]
            results = {}
            results['id'] = id
            for i in range(len(fieldlist)):
                results[fieldlist[i]] = result[i]
        else:
            results = []
        return results

    def update_test_batch(self,id,fieldlist,valuelist):
        update_value = ''
        for i in range(len(fieldlist)):
            update_value = update_value+' %s = "%s"' %(str(fieldlist[i]),str(valuelist[i]))
            if i < len(fieldlist)-1 :
                update_value = update_value+','
        sql = 'update test_batch set '+update_value+ ' where id = %s ;'% str(id)
        useDB.useDB().insert(sql)

    def rerun_test_batch(self,id, type):
        if type =='all':
            sql = 'select id,test_case_id from test_batch where test_suite_id = %s ;' % str(id)
        elif type == 'part':
            sql = 'select id,test_case_id from  test_batch where test_suite_id = %s and status in (2,3,4);' % (str(id))
        result = useDB.useDB().search(sql)
        if len(result):
            for case in result:
                steps = useDB.useDB().search('select steps from test_case where id = %s;' %case[1])
                if len(steps):
                    steps=steps[0][0]
                    steps.replace('"', '""')
                    import re
                    steps = re.sub('"', '""', steps)
                    useDB.useDB().insert('update test_batch set status=0, steps = "%s" where id = %s ;' % (steps,case[0]) )
                    log.log().logger.info('update test_batch set status=0, steps = "%s" where id = %s ;' % (steps,case[0]) )
                    # log.log().logger.info(steps[0])

    def rerun_test_batch_record(self,id,test_case_id):
        sql = 'update test_suite set status = 0,runCount=1 where id = (select test_suite_id from test_batch where id = %s);' % id
        useDB.useDB().insert(sql)
        # steps = useDB.useDB().insert('select steps from test_case where id = (select test_case_id from test_batch where id = %s);' %id)
        sql = 'update test_batch set status=0, steps =(select steps from test_case where id = %s) where id = %s ;' %(test_case_id,id)
        # print(sql)
        useDB.useDB().insert(sql)


    def rerun_test_batch_Ip(self, id, type,ip):
        if type == 'all':
            sql = 'select id,test_case_id from test_batch where test_suite_id = %s ;' % str(id)
        elif type == 'part':
            sql = 'select id,test_case_id from  test_batch where test_suite_id = %s and status in (2,3);' % (str(id))
        result = useDB.useDB().search(sql)
        if len(result):
            for case in result:
                steps = useDB.useDB().search('select steps from test_case where id = %s;' % case[1])
                if len(steps):
                    steps = steps[0][0]
                    steps.replace('"', '""')
                    import re
                    steps = re.sub('"', '""', steps)
                    sql = string.Template('update test_batch set status=0, steps = "$steps" where id = $id and ip="$ip"  ;')
                    sql = sql.substitute(steps=steps, id= case[0],ip=ip)
                    useDB.useDB().insert(sql)
                    log.log().logger.info(steps[0])


    def batch_new_testcase(self,test_suite_id, test_case_id_list,browser_type_list=['']):
        support_browser = ['Chrome','Firefox','']
        run_type = test_suite_manage.test_suite_manage().search_test_suite(test_suite_id, 'run_type')
        if run_type =='Chrome':
            test_case_id_list = self.remove_android(test_case_id_list)
        log.log().logger.info('%s, %s' %(test_case_id_list, len(test_case_id_list)))
        if len(test_case_id_list)==0:
            result = 0
        else:
            for test_case_id in test_case_id_list:
                steps = test_case_manage.test_case_manage().search_test_case([test_case_id], ['name', 'steps'])
                log.log().logger.info('%s, %s， %s' %(steps,steps[0][0], steps[0][1]))
                if len(steps):
                    for browser_type in browser_type_list:
                        if browser_type not in support_browser:
                            log.log().logger.info('%s browser is not support!' %browser_type)
                        else:
                            self.new_test_batch(test_suite_id, test_case_id,steps[0][0], steps[0][1],browser_type=browser_type)
                else:
                    log.log().logger.info('test case not exist!')
                result = 1
        return result

    #重写
    def batch_new_testcase_IP(self, test_suite_id, test_case_id_list,ip):
        run_type = test_suite_manage.test_suite_manage().search_test_suite(test_suite_id, 'run_type')
        if run_type == 'Chrome':
            test_case_id_list = self.remove_android(test_case_id_list)
        log.log().logger.info('%s, %s' %(test_case_id_list, len(test_case_id_list)))
        if len(test_case_id_list) == 0:
            result = 0
        else:
            for test_case_id in test_case_id_list:
                steps = test_case_manage.test_case_manage().search_test_case([test_case_id], ['name', 'steps'])
                log.log().logger.info('%s, %s,%s' %(steps, steps[0][0], steps[0][1]))
                if len(steps):
                    self.new_test_batch_IP(test_suite_id, test_case_id, steps[0][0], steps[0][1],ip)
                else:
                    log.log().logger.info('test case not exist!')
                result = 1
        return result

    def remove_android(self, test_case_id_list):
        caseList = ''
        for i in range(len(test_case_id_list)):
            if i :
                caseList =caseList+','+ str(test_case_id_list[i])
            else:
                caseList = caseList + str(test_case_id_list[i])
        sql = 'select id from test_case where module !="android" and id in (%s);' %caseList
        result = useDB.useDB().search(sql)
        log.log().logger.info(result)
        newIdList = []
        for id in result:
            newIdList.append(id[0])
        log.log().logger.info(newIdList)
        return newIdList

    def show_test_batch(self,conditionList, valueList, fieldlist,rows):
        if len(fieldlist)==0:
            fieldlist = ['id','test_case_id',  'name', 'status', 'steps','runtime','message','screenshot','test_suite_id','ip','browser_type']
        search_value = fieldlist[0]
        for i in range(1,len(fieldlist)):
            search_value = search_value + ','+fieldlist[i]
        condition = ''
        search_type1 = ''
        search_type2=''
        for i in range(len(conditionList)):
            if str(conditionList[i])=='id':
                search_type1 = '="'
                search_type2 = '"'
            else:
                search_type1 = ' like "%'
                search_type2 = '%"'
            if i == 0:
                condition += str(conditionList[i]) +search_type1+str(valueList[i])+search_type2
                # condition += str(conditionList[i]) + ' like "%' + str(valueList[i]) + '%"'
            else:
                condition += ' and '+str(conditionList[i]) +search_type1+str(valueList[i])+search_type2
                # condition += ' and ' + str(conditionList[i]) + ' like "%' + str(valueList[i]) + '%"'
        results = []
        sql = 'select ' + search_value + ' from test_batch where ' + str(condition) + ' order by id desc limit '+ str(rows)+';'
        cases = useDB.useDB().search(sql)
        log.log().logger.info('cases : %s ' %cases)
        for i in range(len(cases)):
            result = {}
            for j in range(len(fieldlist)):
                if fieldlist[j]=='runtime' and  cases[i][j] is not None:
                    result0 = cases[i][j].strftime('%Y-%m-%d %H:%M:%S')
                elif fieldlist[j]=='status':
                    if cases[i][3] == 0:
                        result0 = '0-待执行'
                    elif cases[i][3] == 1:
                        result0 = '1-执行成功'
                    elif cases[i][3] == 4:
                        result0 = '4-执行中'
                    elif cases[i][3] == 2:
                        result0 = '2-执行失败'
                    elif cases[i][3] == 3:
                        result0 = '3-无法执行'
                    else:
                        result0 = 'cases[i][3]'
                else:
                    result0 = cases[i][j]
                result[fieldlist[j]]=result0
            results.append(result)
        log.log().logger.info("results is :%s" %results)
        return results


    def show_test_batch_status(self,test_suite_id):
        results = []
        sql = 'select status, count(*) from test_batch where test_suite_id = ' + str(test_suite_id) + ' group by status;'
        cases = useDB.useDB().search(sql)
        log.log().logger.info('cases : %s' %cases)
        results = {}
        notrun =0
        pending=0
        success=0
        running = 0
        fail=0
        for case in cases:
            log.log().logger.info(case)
            if case[0]==0:
                pending = case[1]
            elif case[0]==1:
                success = case[1]
            elif case[0]==2:
                fail = case[1]
            elif case[0] == 3:
                notrun = case[1]
            elif case[0] == 4:
                running = case[1]
        total = pending+notrun+success+fail+running
        if total>0:
            successRate = (success/total)*100
            log.log().logger.info('%s, %s' %(total,successRate))
        else:
            successRate = 0
        results['pending'] = str(pending+notrun)
        results['success'] = str(success)
        results['fail'] = str(fail)
        results['running']= str(running)
        results['total'] = str(total)
        results['successRate']=str(round(successRate,2))+'%'
        log.log().logger.info(results)
        return results

    def copy_test_batch(self,new_test_suite_id, old_test_suite_id):
        sql = 'select test_case_id from test_batch where test_suite_id = "%s";' %old_test_suite_id
        result = useDB.useDB().search(sql)
        log.log().logger.info(result)
        idList = []
        if len(result):
            for id in result:
                log.log().logger.info(id)
                idList.append(id[0])

        return self.batch_new_testcase(new_test_suite_id,idList)

    def search_done_test_suite(self):
        sql = 'SELECT id FROM test_suite WHERE (STATUS = 0 OR STATUS = 2 ) ; '
        result = useDB.useDB().search(sql)
        check_result = ''
        if len(result):
            for id in result:
                sql = 'SELECT COUNT(1) FROM test_batch WHERE test_suite_id = %s AND STATUS in (0,4);' %id
                result1 = useDB.useDB().search(sql)
                # print(result1[0][0])
                if len(result1) and (result1[0][0]==0):
                    if check_result !='':
                        check_result += ','
                    check_result +=(str(id[0]))
                    # print(check_result)
        return check_result


    def set_test_running(self,id,deviceList=[]):
        if len(deviceList):
            sql = 'update test_batch set status = 4, ip = "%s" where id = %s ;' % (deviceList[0], id)
        else:
            sql = 'update test_batch set status = 4 where id = %s ;' %(id)
        useDB.useDB().insert(sql)

    def set_test_end(self,result, nowTime, currentStep, screenFileList,id):
        if  currentStep == 'package not found':
            sql = 'update test_batch set status = 0, ip = "" where id = %s ;' %id
        else:
            if result == '1':
                message = ''
            else:
                message = currentStep
            sql = 'update test_batch set status = "%s", runtime = "%s", message= "%s", screenshot  = "%s" where id = %s ;' %(result, nowTime, message, screenFileList,id)
        useDB.useDB().insert(sql)