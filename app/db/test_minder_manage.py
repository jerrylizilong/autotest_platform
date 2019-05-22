from app import useDB,log
import string

class test_minder_manage:
    def __init__(self):
        self.status = 0
        self.name = ''

    def new_minder(self,module,name,description, content='{}'):
        import random, time
        batchId = str(random.randint(10000, 99999)) + str(time.time())
        content = str(content).replace('"','\\"')
        sql = string.Template('insert into test_minder (module,name,description,content,batchId) values ("$module","$name","$description","$content","$batchId");')
        sql = sql.substitute(name = name, module = module, description=description, content=content,batchId=batchId)
        print(sql)
        useDB.useDB().insert(sql)
        minders = test_minder_manage().show_test_minders(conditionList=['batchId'],
                                                                            valueList=[batchId],
                                                                            rows=1)
        result = {}
        if len(minders):
            result['id'] = minders[0]['id']
            result['code']=1
        else:
            result['code']=0
            result['id'] =''
        return result

    def copy_test_minder(self,id):
        # module, name, steps, description, isPublic
        searchresult = self.show_test_minders(['id'],[id],1)
        result ={'code':0}
        if len(searchresult):
            searchresult=searchresult[0]
            result = self.new_minder(name = searchresult['name'], module = searchresult['module'], description=searchresult['description'], content=searchresult['content'])
        return result


    def update_test_minder(self,id,fieldlist,valueList):
        update_value = '%s = "%s"' %(fieldlist[0],str(valueList[0]).replace('"','\\"'))
        for i in range(1,len(fieldlist)):
            print(fieldlist[i])
            # if fieldlist[i]=='content':
            update_value += ', %s = "%s"' %(fieldlist[i],str(valueList[i]).replace('"','\\"'))
            # else:
                # update_value += ', %s = "%s"' %(fieldlist[i],valueList[i])
        sql = string.Template('update test_minder set $field where id = "$id";')
        sql = sql.substitute(field = update_value, id = id)
        useDB.useDB().insert(sql)


    def show_test_minders(self,conditionList, valueList, rows):
        fieldlist = ['id', 'module', 'name',  'description','content']
        search_value = fieldlist[0]
        for i in range(1,len(fieldlist)):
            search_value = search_value + ','+fieldlist[i]
        condition = ''
        for i in range(len(conditionList)):
            if valueList[i] !='':
                if conditionList[i]=='id':
                    condition += ' and %s = "%s"' %(conditionList[i],valueList[i])
                else:
                    condition += ' and '+str(conditionList[i]) +' like "%'+str(valueList[i])+'%"'
        results = []

        sql = 'select ' + search_value + ' from test_minder where status = 1 ' + str(condition) + ' order by id desc limit '+ str(rows)+';'
        print(sql)
        cases = useDB.useDB().search(sql)
        log.log().logger.info('cases : %s'%cases)
        for i in range(len(cases)):
            result = {}
            result['id'] = cases[i][0]
            result['module'] = cases[i][1]
            result['name'] = cases[i][2]
            result['description'] = cases[i][3]
            result['content'] = cases[i][4]
            results.append(result)
        return results


    def show_test_cases_unattach(self,test_suite_id,conditionList, valueList, fieldlist,rows):
        fieldlist = ['id', 'module', 'name', 'steps', 'description','isPublicFunction']
        search_value = fieldlist[0]
        for i in range(1,len(fieldlist)):
            search_value = search_value + ','+fieldlist[i]
        results = []
        log.log().logger.info('%s, %s, %s, %s, %s' %(test_suite_id,conditionList, valueList, fieldlist,rows))
        condition = ''
        for i in range(len(conditionList)):
            if i == 0:
                if conditionList[i]=='module':
                    log.log().logger.info(valueList[i])
                    moduleList = ''
                    for j in range(len(valueList[i])):
                        if j :
                            moduleList += ','
                        moduleList += '"'+valueList[i][j]+'"'
                    condition += str(conditionList[i]) + ' in (' + str(moduleList) + ')'
                else:
                    condition += str(conditionList[i]) +' like "%'+str(valueList[i])+'%"'
            else:
                if conditionList[i] == 'module':
                    log.log().logger.info(valueList[i])
                    moduleList = ''
                    for j in range(len(valueList[i])):
                        if j :
                            moduleList += ','
                        moduleList += '"'+valueList[i][j]+'"'
                    condition += ' and ' + str(conditionList[i]) +  ' in (' + str(moduleList) + ')'
                else:
                    condition += ' and '+str(conditionList[i]) +' like "%'+str(valueList[i])+'%"'
        if condition !='':
            condition += ' and '
        sql = 'select ' + search_value + ' from test_case where status = 1 and isPublicFunction=0 and '+ str(condition) +' id not in (select distinct test_case_id from test_batch where test_suite_id = '+test_suite_id+' )  order by module desc;'
        cases = useDB.useDB().search(sql)
        log.log().logger.info('cases : %s'%cases)
        for i in range(len(cases)):
            result = {}
            result['id'] = cases[i][0]
            result['module'] = cases[i][1]
            result['name'] = cases[i][2]
            result['steps'] = cases[i][3]
            result['description'] = cases[i][4]
            result['isPublic'] = cases[i][5]
            results.append(result)
        return results



