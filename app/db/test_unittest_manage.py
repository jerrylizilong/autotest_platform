from app import useDB,log
import string

class test_unittest_manage:

    def new_unittest_case(self,reportName, start_time, end_time, reportFileName):
        sql = 'insert into unittest_record (name,start_time,end_time,file_name) values ("%s","%s","%s","%s");' % (
        reportName, start_time, end_time, reportFileName)
        useDB.useDB().insert(sql)

    def show_unittest_records(self,conditionList, valueList, fieldlist,rows):
        if len(fieldlist)==0:
            fieldlist = ['id',  'name', 'start_time', 'end_time','file_name']
        search_value = fieldlist[0]
        for i in range(1,len(fieldlist)):
            search_value = search_value + ','+fieldlist[i]
        condition = ''
        for i in range(len(conditionList)):
            if i == 0:
                condition += str(conditionList[i]) + ' like "%' + str(valueList[i]) + '%"'
            else:
                condition += ' and ' + str(conditionList[i]) + ' like "%' + str(valueList[i]) + '%"'

        results = []

        sql = 'select ' + search_value + ' from unittest_record where ' + str(condition) + 'order by id desc limit '+ str(rows)+';'
        cases = useDB.useDB().search(sql)
        log.log().logger.info('cases : %s' %cases)
        for i in range(len(cases)):
            result = {}
            result['id'] = cases[i][0]
            result['name'] = cases[i][1]
            result['start_time'] = cases[i][2].strftime('%Y-%m-%d %H:%M:%S')
            result['end_time'] = cases[i][3].strftime('%Y-%m-%d %H:%M:%S')
            result['file_name'] = cases[i][4]
            results.append(result)
        # log.log().logger.info(results)
        return results

