from app import useDB,log
import string

class test_keyword_manage:

    def show_test_keywords(self,conditionList, valueList, fieldlist,rows):
        results = []
        if len(conditionList) and conditionList[0]=='id':
            sql = 'select id, keyword, paraCount, template, example,description from test_keyword where status = 1 and id =' + str(
                valueList[0]) + ' order by id desc limit 1;'
        else:
            sql = 'select id, keyword, paraCount, template, example,description from test_keyword where status = 1 and keyword like "%' + str(valueList[0]) + '%" order by id desc limit '+ str(rows)+';'
        print(sql)
        cases = useDB.useDB().search(sql)
        print(cases)
        log.log().logger.info('cases : %s'%cases)
        for i in range(len(cases)):
            result = {}
            result['id'] = cases[i][0]
            result['keyword'] = cases[i][1]
            result['paraCount'] = cases[i][2]
            result['template'] = cases[i][3]
            result['example'] = cases[i][4]
            result['description'] = cases[i][5]
            results.append(result)
        print(results)
        return results

    def new_test_keyword(self,name, paraCount, description, template,example):
        sql = "insert into test_keyword (keyword, paraCount, description, template,example) values ('%s','%s','%s','%s','%s');" %(name, paraCount, description, template,example)
        print(sql)
        useDB.useDB().insert(sql)
        return True

    def copy_test_keyword(self,id):
        result = self.show_test_keywords(['id'],[id],[],1)
        print(result)
        if len(result):
            result=result[0]
            result = self.new_test_keyword(result["keyword"]+'_copy',result["paraCount"],result["description"],result["template"],result['example'])
        else:
            result = 0
        return result


    def update_test_keyword(self,id,fieldlist,valueList):
        update_value = "%s = '%s'" %(fieldlist[0],valueList[0])
        for i in range(1,len(fieldlist)):
            update_value += ", %s = '%s'" %(fieldlist[i],str(valueList[i]).replace("'",'"'))
        sql = string.Template('update test_keyword set $field where id = $id;')
        sql = sql.substitute(field = update_value, id = id)
        print(sql)
        useDB.useDB().insert(sql)
        return 1

    def show_test_keywords_options(self):
        results = []
        sql = 'select keyword from test_keyword where status = 1 ;'
        cases = useDB.useDB().search(sql)
        print(cases)
        log.log().logger.info('cases : %s' % cases)
        for i in range(len(cases)):
            results.append(cases[i][0])
        return results
