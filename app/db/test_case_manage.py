from app import useDB,log
import string

class test_case_manage:
    def __init__(self):
        self.status = 0
        self.name = ''

    def new_test_case(self,module,name,steps,description, isPublic):
        sql = string.Template('insert into test_case (module,name,steps,description,isPublicFunction) values ("$module","$name","$steps","$description",$isPublic);')
        sql = sql.substitute(name = name, module = module, steps = steps,description=description, isPublic=isPublic)
        useDB.useDB().insert(sql)

    def copy_test_case(self,id):
        # module, name, steps, description, isPublic
        result = self.show_test_cases(['id'],[id],[],1)
        if len(result):
            result=result[0]
            sql = string.Template('insert into test_case (module,name,steps,description,isPublicFunction) values ("$module","$name","$steps","$description",$isPublic);')
            sql = sql.substitute(name = result['name'], module = result['module'], steps = result['steps'],description=result['description'], isPublic=result['isPublic'])
            useDB.useDB().insert(sql)
            result = 1
        else:
            result = 0
        return result


    def update_test_case(self,id,fieldlist,valueList):
        update_value = '%s = "%s"' %(fieldlist[0],valueList[0])
        for i in range(1,len(fieldlist)):
            update_value += ', %s = "%s"' %(fieldlist[i],valueList[i])
        sql = string.Template('update test_case set $field where id = "$id";')
        sql = sql.substitute(field = update_value, id = id)
        useDB.useDB().insert(sql)

    def search_test_case(self,idList,fieldlist):
        id_value = str(idList[0])
        for i in range(1,len(idList)):
            id_value +=  ','+str(idList[i])
        search_value = fieldlist[0]
        for i in range(1,len(fieldlist)):
            search_value = search_value + ','+fieldlist[i]
        sql = 'select ' + search_value + ' from test_case where id in ( ' + str(id_value) + ') order by id desc;'
        resultlist = useDB.useDB().search(sql)
        return resultlist

    def show_test_public_cases(self):
        results = []
        sql = 'select name from test_case where status = 1 and isPublicFunction = 1 ;'
        cases = useDB.useDB().search(sql)
        print(cases)
        log.log().logger.info('cases : %s' % cases)
        for i in range(len(cases)):
            results.append(cases[i][0])
        return results


    def show_test_cases(self,conditionList, valueList, fieldlist,rows):
        if len(fieldlist)==0:
            fieldlist = ['id', 'module', 'name', 'steps', 'description','isPublicFunction']
        search_value = fieldlist[0]
        for i in range(1,len(fieldlist)):
            search_value = search_value + ','+fieldlist[i]
        condition = ''
        for i in range(len(conditionList)):
            if i == 0:
                if conditionList[i] == 'module':
                    log.log().logger.info(valueList[i])
                    moduleList = ''
                    for j in range(len(valueList[i])):
                        if j:
                            moduleList += ','
                        moduleList += '"' + valueList[i][j] + '"'
                    condition += str(conditionList[i]) + ' in (' + str(moduleList) + ')'
                else:
                    condition += str(conditionList[i]) + ' like "%' + str(valueList[i]) + '%"'
            else:
                if conditionList[i] == 'module':
                    log.log().logger.info(valueList[i])
                    moduleList = ''
                    for j in range(len(valueList[i])):
                        if j:
                            moduleList += ','
                        moduleList += '"' + valueList[i][j] + '"'
                    condition += ' and ' + str(conditionList[i]) + ' in (' + str(moduleList) + ')'
                else:
                    condition += ' and ' + str(conditionList[i]) + ' like "%' + str(valueList[i]) + '%"'
                # if condition != '':
                #     condition += ' and '
        results = []

        sql = 'select ' + search_value + ' from test_case where ' + str(condition) + ' and status = 1  order by id desc limit '+ str(rows)+';'
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

    #
    # def show_test_keywords(self,conditionList, valueList, fieldlist,rows):
    #     results = []
    #     sql = 'select id, keyword, paraCount, template, example,description from test_keyword where keyword like "%' + str(valueList[0]) + '%" order by id desc limit '+ str(rows)+';'
    #     cases = useDB.useDB().search(sql)
    #     log.log().logger.info('cases : %s'%cases)
    #     for i in range(len(cases)):
    #         result = {}
    #         result['id'] = cases[i][0]
    #         result['keyword'] = cases[i][1]
    #         result['paraCount'] = cases[i][2]
    #         result['template'] = cases[i][3]
    #         result['example'] = cases[i][4]
    #         result['description'] = cases[i][5]
    #         results.append(result)
    #     return results
