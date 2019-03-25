import string
from app import useDB,log


class test_api_new_manange():
    #新增接口测试用例
    def new_test_api(self,product,module,name,url,paras,osign_list,description):
        paras = paras.replace('"',"'")
        sql = string.Template('insert into api_new (product,module,name,url,paras,osign_list,description) values ("$product","$module","$name","$url","$paras","$osign_list","$description");')
        sql = sql.substitute(product=product,module=module,name=name,url=url,paras=paras,osign_list=osign_list,description=description)
        try:
            useDB.useDB().insert(sql)
            result = 1
        except :
            result = 0
        return result

    #查询测试用例配置信息
    def show_test_api(self, conditionList, valueList, fieldlist, rows,type='all'):
        from app.api_new import api_manage
        import json
        print(conditionList, valueList, fieldlist, rows)
        condition = ''
        if len(conditionList)!=0:
            for i in range(len(conditionList)):
                if str(conditionList[i])=='id':
                    if str(valueList[i])!='':
                        condition += ' and ' + str(conditionList[i]) + ' =' + str(valueList[i])
                elif str(valueList[i])!='':
                    condition += ' and ' + str(conditionList[i]) + ' like "%' + str(valueList[i]) + '%"'
        results = []
        sql = 'select id,product,module,name,url,paras,osign_list,description from api_new where 1=1 and status=1'+str(condition)+ ' order by id desc limit ' + str(rows) + ';'
        list = useDB.useDB().search(sql)
        log.log().logger.info('cases : %s ' %list)
        for i in range(len(list)):
            result = {}
            result['id'] = list[i][0]
            result['product'] = list[i][1]
            result['module'] = list[i][2]
            result['name'] = list[i][3]
            result['url'] = list[i][4]
            paras = list[i][5].replace("'",'"')
            if type=='default':
                paras = api_manage.api_manage().get_api_paras(para_info=json.loads(paras),type='default')
            elif type=='ramdon':
                paras = api_manage.api_manage().get_api_paras(para_info=json.loads(paras),type='ramdon')
            result['paras'] = json.dumps(paras).replace('"',"'")
            result['osign_list'] = list[i][6]
            result['description'] = list[i][7]
            results.append(result)
        return results


    #删除接口测试用例
    def del_test_api(self,id):
        return self.update_test_api(id,fieldlist=['status'],valueList=['0'])

    #修改接口测试用例
    def update_test_api(self,id,fieldlist,valueList):
        update_value = '%s = "%s"' %(fieldlist[0],valueList[0].replace('"',"'"))
        for i in range(1,len(fieldlist)):
            update_value += ', %s = "%s"' %(fieldlist[i],valueList[i].replace('"',"'"))
        sql = string.Template('update api_new set $field where id = "$id";')
        sql = sql.substitute(field = update_value, id = id)
        try:
            useDB.useDB().insert(sql)
            result = 1
        except :
            result = 0
        return result
