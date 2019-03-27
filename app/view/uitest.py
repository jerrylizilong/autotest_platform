from flask import Blueprint,render_template, jsonify, request, redirect
from app import log
from app.view import viewutil,user
from app.db import test_case_manage,test_batch_manage,test_suite_manage,test_keyword_manage
import pyecharts

mod = Blueprint('uitest', __name__,
                        template_folder='templates/uitest')


@mod.route('/test_suites')
@user.authorize
def test_suite():

    return render_template("uitest/test_suite.html")

@mod.route('/test_cases')
@user.authorize
def test_cases():

    return render_template("uitest/test_cases.html")

@mod.route('/add_test_case', methods=['POST', 'GET'])
@user.authorize
def save_new_test_case():
    log.log().logger.info(request)
    if request.method == 'GET':
        log.log().logger.info('post')
        return render_template("uitest/new_test_cases.html")
    if request.method == 'POST':
        info = request.form
        log.log().logger.info('info : %s' %info)
        name = viewutil.getInfoAttribute(info,'name')
        module = viewutil.getInfoAttribute(info,'module')
        description = viewutil.getInfoAttribute(info,'description')
        steps = viewutil.getInfoAttribute(info,'steps')
        log.log().logger.info("steps: %s" %steps)
        steps=steps.replace('"',"'")
        log.log().logger.info("steps: %s" %steps)
        type = viewutil.getInfoAttribute(info,'type')
        if module == '' or name == '' or steps=='' or type=='':
            return '必填字段不得为空！'
        else:
            if type=='公共用例':
                isPublic = 1
            else:
                isPublic = 0
            test_case_manage.test_case_manage().new_test_case(module, name, steps, description, isPublic)
        return redirect('test_cases')

@mod.route('/edit_test_case', methods=['POST', 'GET'])
@user.authorize
def edit_test_case():
    log.log().logger.info(request)
    if request.method == 'GET':
        log.log().logger.info('post')
        info = request.values
        log.log().logger.info('info : %s' %info)
        id = viewutil.getInfoAttribute(info, 'id')
        log.log().logger.info('id: %s'%id)
        return render_template("uitest/edit_test_cases2.html", id=id)
    if request.method == 'POST':
        info = request.form
        log.log().logger.info('info : %s' %info)
        id = viewutil.getInfoAttribute(info, 'id')
        name = viewutil.getInfoAttribute(info,'name')
        module = viewutil.getInfoAttribute(info,'module')
        description = viewutil.getInfoAttribute(info,'description')
        steps = viewutil.getInfoAttribute(info,'steps')
        log.log().logger.info("steps: %s" %steps)
        steps=steps.replace('"',"'")
        log.log().logger.info("steps: %s" %steps)
        type = viewutil.getInfoAttribute(info,'type')
        if module == '' or name == '' or steps=='' or type=='':
            return '必填字段不得为空！'
        else:
            if type=='公共用例':
                isPublic = 1
            else:
                isPublic = 0
            test_case_manage.test_case_manage().update_test_case(id, ['module', 'name', 'steps', 'description', 'isPublicFunction'], [module, name, steps, description, isPublic])
            return render_template("uitest/test_batch2.html",id=id,type='test_suite')

@mod.route('/copy_test_case', methods=['POST', 'GET'])
@user.authorize
def copy_test_case():
    log.log().logger.info(request)
    log.log().logger.info(request.method)
    # log.log().logger.info(request.value)
    if request.method == 'GET':
        log.log().logger.info('post')
        result = jsonify({'code': 500, 'msg': 'should be get!'})
        return result
    if request.method == 'POST':
        info = request.form
        log.log().logger.info('info :  %s' %info)
        id = viewutil.getInfoAttribute(info, 'id')
        log.log().logger.info(id)
        if id=='':
            result = jsonify({'code': 500, 'msg': 'test case is not found!'})
        else:
            result0 = test_case_manage.test_case_manage().copy_test_case(id)
            if result0:
                result = jsonify({'code': 200, 'msg': 'copy success!'})
            else:
                result = jsonify({'code': 500, 'msg': 'test case is not found!'})
        return result

@mod.route('/copy_test_suite', methods=['POST', 'GET'])
@user.authorize
def copy_test_suite():
    log.log().logger.info(request)
    log.log().logger.info(request.method)
    # log.log().logger.info(request.value)
    if request.method == 'GET':
        log.log().logger.info('post')
        result = jsonify({'code': 500, 'msg': 'should be get!'})
        return result
    if request.method == 'POST':
        info = request.form
        log.log().logger.info('info :  %s' %info)
        id = viewutil.getInfoAttribute(info, 'id')
        log.log().logger.info("id: %s" %id)
        if id=='':
            result = jsonify({'code': 500, 'msg': 'test suite is not found!'})
        else:
            import random, time
            batchId = str(random.randint(10000, 99999)) + str(time.time())
            test_suite_manage.test_suite_manage().copy_test_suite(id, batchId)
            newId = test_suite_manage.test_suite_manage().show_test_suites(["batchId"], [batchId], ['id'], 1)
            log.log().logger.info('newid %s' %newId)
            if len(newId):
                ext = newId[0]['id']
                log.log().logger.info('ext is: %s, id is: %s' %(ext, id))
                if ext !='0':
                    test_batch_manage.test_batch_manage().copy_test_batch(ext, id)
                message = 'success！'
                code = 200
                result = jsonify({'code': 200, 'msg': 'copy success!'})
            else:
                result = jsonify({'code': 500, 'msg': 'test suite is not found!'})
        return result

@mod.route('/delete_test_case', methods=['POST', 'GET'])
@user.authorize
def delete_test_case():
    log.log().logger.info(request)
    if request.method == 'GET':
        log.log().logger.info('post')
        info = request.values
        log.log().logger.info('info : %s' %info)
        id = viewutil.getInfoAttribute(info, 'id')
        log.log().logger.info('id: %s' %id)
        return render_template("uitest/test_cases.html")
    if request.method == 'POST':
        info = request.form
        log.log().logger.info('info : %s' %info)
        id = viewutil.getInfoAttribute(info, 'id')
        act = viewutil.getInfoAttribute(info, 'act')
        if act == 'del':
            test_case_manage.test_case_manage().update_test_case(id, ['status'], [0])
            code = 200
            message = 'delete success!'
        else:
            code=500
            message = 'act is not del!'
        result = jsonify({'code': code, 'msg': message})
        return result,{'Content-Type': 'application/json'}

@mod.route('/test_case.json', methods=['POST', 'GET'])
@user.authorize
def search_test_cases():
    if request.method == 'POST':
        log.log().logger.info('post')
    if request.method == 'GET':
        info = request.values
        log.log().logger.info('info : %s' %info)
        limit = info.get('limit', 10)  # 每页显示的条数
        offset = info.get('offset', 0)  # 分片数，(页码-1)*limit，它表示一段数据的起点
        log.log().logger.info('get %s' %limit)
        log.log().logger.info('get  offset %s' %offset)
        id = viewutil.getInfoAttribute(info,'id')
        module = viewutil.getInfoAttribute(info, 'module')
        type = viewutil.getInfoAttribute(info, 'type')
        log.log().logger.info('module: %s' %module)
        module = module.split(',')
        log.log().logger.info(module)
        name = viewutil.getInfoAttribute(info, 'name')
        conditionList = ['name']
        valueList = [name]
        if type == 'unattach' and 'public' in module:
            module.remove('public')
        elif type!='test_case':
            if len(module) !=0 and module[0] != 'All' and module[0] != '':
                conditionList.append('module')
                valueList.append(module)
            log.log().logger.info('info content: id- %s, module - %s, name - %s, type - %s' %(id,module, name, type))
        else:
            conditionList = ['id']
            valueList = [id]
            log.log().logger.info('info content: id- %s, module - %s, name - %s, type - %s' %(id,module,name, type))
        # else:
        fieldlist = []
        rows = 1000
        if type =='unattach':
            caseList = test_case_manage.test_case_manage().show_test_cases_unattach(id, conditionList, valueList, fieldlist, rows)
        else:
            caseList = test_case_manage.test_case_manage().show_test_cases(conditionList, valueList, fieldlist, rows)
        log.log().logger.info(caseList)
        data = caseList
        if type=='test_case':
            data1 = jsonify({'total': len(data), 'rows': data[0]})
        else:
            data1 = jsonify({'total': len(data), 'rows': data[int(offset):int(offset)+int(limit)]})
        log.log().logger.info('data1: %s' %data1)
        return data1,{'Content-Type': 'application/json'}


@mod.route('/test_suite.json', methods=['POST', 'GET'])
@user.authorize
def search_test_suite():
    if request.method == 'POST':
        log.log().logger.info('post')
    if request.method == 'GET':
        info = request.values
        log.log().logger.info('info : %s' %info)
        limit = info.get('limit', 10)  # 每页显示的条数
        offset = info.get('offset', 0)  # 分片数，(页码-1)*limit，它表示一段数据的起点
        log.log().logger.info('get %s' %limit)
        log.log().logger.info('get  offset %s' %offset)
        id = viewutil.getInfoAttribute(info,'id')
        type = viewutil.getInfoAttribute(info, 'type')
        log.log().logger.info('type %s' %type)
        run_type = viewutil.getInfoAttribute(info, 'run_type')
        status = viewutil.getInfoAttribute(info, 'status')
        name = viewutil.getInfoAttribute(info, 'name')
        if id =='':
            if status == 'All':
                status = ''
            log.log().logger.info('info content: %s, %s, %s, %s' %(id,status,run_type, name))
            conditionList = ['status','run_type','name']
            valueList = [status,run_type,name]
        else:
            if type == 'testview':
                statusList = test_batch_manage.test_batch_manage().show_test_batch_status(id)
            else:
                statusList = []
            log.log().logger.info('info content: %s, %s, %s, %s' %(id,status,run_type, name))
            conditionList = ['id']
            valueList = [id]
        fieldlist = []
        rows = 1000
        caseList = test_suite_manage.test_suite_manage().show_test_suites(conditionList, valueList, fieldlist, rows)
        log.log().logger.info(caseList)
        data = caseList
        if id !='':
            data1 = jsonify({'total': len(data), 'rows': data[0],'status':statusList})
        else:
            data1 = jsonify({'total': len(data), 'rows': data[int(offset):int(offset)+int(limit)]})
        log.log().logger.info('data1: %s' %data1)
        return data1,{'Content-Type': 'application/json'}

@mod.route('/add_test_suite.json', methods=['POST', 'GET'])
@user.authorize
def save_new_test_suite():
    log.log().logger.info(request)
    if request.method == 'GET':
        log.log().logger.info('post')
        return render_template("uitest/new_test_suite.html")
    if request.method == 'POST':
        info = request.values
        log.log().logger.info('info :%s' %info)
        name = viewutil.getInfoAttribute(info,'name')
        run_type = viewutil.getInfoAttribute(info,'run_type')
        description = viewutil.getInfoAttribute(info,'description')
        if run_type == '' or name == '' :
            message =  '必填字段不得为空！'
            code = 500
        else:
            import random, time
            batchId = str(random.randint(10000, 99999)) + str(time.time())
            test_suite_manage.test_suite_manage().new_test_suite(name, run_type, description, batchId)
            newId = test_suite_manage.test_suite_manage().show_test_suites(["batchId"], [batchId], ['id'], 1)
            log.log().logger.info('newid %s' %newId)
            if len(newId):
                ext=newId[0]['id']
                log.log().logger.info('ext %s' %ext)
                message = 'success！'
                code = 200
                # return redirect('attach_test_batch?test_suite_id=%s' %ext)
            else:
                ext=''
                message =  'add failed！'
                code = 500
            result = jsonify({'code': code, 'msg': message,'ext':ext})
            log.log().logger.info(result)
            # log.log().logger.info('code is : %s'%result['code'])
            return result

@mod.route('/add_test_suite', methods=['POST', 'GET'])
@user.authorize
def add_test_suite():
    log.log().logger.info(request)
    return render_template("uitest/new_test_suite.html")


@mod.route('/test_batch.json', methods=['POST', 'GET'])
@user.authorize
def search_test_batch():
    if request.method == 'POST':
        log.log().logger.info('post')
    if request.method == 'GET':
        info = request.values
        log.log().logger.info('info : %s' %info)
        limit = info.get('limit', 10)  # 每页显示的条数
        offset = info.get('offset', 0)  # 分片数，(页码-1)*limit，它表示一段数据的起点
        log.log().logger.info('get %s' %limit)
        log.log().logger.info('get  offset %s' %offset)
        id = viewutil.getInfoAttribute(info,'id')
        name = viewutil.getInfoAttribute(info, 'name')
        status = viewutil.getInfoAttribute(info, 'status')
        module = viewutil.getInfoAttribute(info, 'module')
        ipVal = viewutil.getInfoAttribute(info, 'ipVal')
        browser_type = viewutil.getInfoAttribute(info, 'browser_type')
        type = viewutil.getInfoAttribute(info, 'type')
        log.log().logger.info('module: %s' %module)
        log.log().logger.info('ipVal %s' %ipVal)
        module = module.split(',')
        log.log().logger.info(module)
        valueList = []
        conditionList = []
        if id == '':
            data1 = jsonify({'total': 0, 'rows': []})
        else:
            if name != '':
                conditionList.append('name')
                valueList.append(name)
            if status != '':
                conditionList.append('status')
                valueList.append(status)
            if len(module) !=0 and module[0] != 'All' and module[0] != '':
                conditionList.append('module')
                valueList.append(module)
            ipList = ipVal.split(',')
            for j in range(len(ipList)):
                if ipList[j] !='':
                    conditionList.append('ip')
                    valueList.append(ipList[j])
            fieldlist = []
            rows = 1000
            if type == "" or type=='test_suite':
                conditionList.append('test_suite_id')
                valueList.append(id)
                caseList = test_batch_manage.test_batch_manage().show_test_batch(conditionList, valueList, fieldlist, rows)
                log.log().logger.info("caseList %s" %caseList)
                data = caseList
            elif type=='test_case':
                conditionList.append('test_case_id')
                valueList.append(id)
                caseList = test_batch_manage.test_batch_manage().show_test_batch(conditionList, valueList, fieldlist, rows)
                log.log().logger.info(caseList)
                data = caseList
            else:
                caseList = test_case_manage.test_case_manage().show_test_cases_unattach(id, conditionList, valueList, fieldlist, rows)
                log.log().logger.info(caseList)
                data = caseList
            data1 = jsonify({'total': len(data), 'rows': data[int(offset):int(offset)+int(limit)]})
            log.log().logger.info('data1: %s' %data1)
        return data1,{'Content-Type': 'application/json'}

@mod.route('/test_batch_detail_old', methods=['POST', 'GET'])
@user.authorize
def test_batch_detail():
    log.log().logger.info(request)
    if request.method == 'GET':
        log.log().logger.info('post')
        info = request.values
        log.log().logger.info('info :  %s' %info)
        id = viewutil.getInfoAttribute(info, 'test_suite_id')
        log.log().logger.info('id: %s' %id)
        return render_template("uitest/test_batch_detail.html",id=id)
        # return render_template("uitest/test_batch_report.html", id=id)
    else:
        return render_template('test_suite.html')

@mod.route('/attach_test_batch', methods=['POST', 'GET'])
@user.authorize
def attach_test_batch():
    log.log().logger.info(request)
    if request.method == 'GET':
        log.log().logger.info('post')
        info = request.values
        log.log().logger.info('info :  %s' %info)
        id = viewutil.getInfoAttribute(info, 'test_suite_id')
        log.log().logger.info('id: %s' %id)
        return render_template("uitest/attach_test_batch.html",id=id)
    else:
        return render_template("uitest/test_suite.html")

@mod.route('/attach_test_batch.json', methods=['POST', 'GET'])
@user.authorize
def attach_test_batch_to_suite():
    log.log().logger.info(request)
    if request.method == 'POST':
        log.log().logger.info('post')
        result = jsonify({'code': 500, 'msg': 'post'})
        return result
    else:
        log.log().logger.info(request.values)
        # log.log().logger.info(request.form)
        info = request.values
        test_suite_id = viewutil.getInfoAttribute(info,'test_suite_id')
        ipVal = viewutil.getInfoAttribute(info, 'ipVal')
        browser_list = viewutil.getInfoAttribute(info, 'browser_list')
        browser_list = browser_list.split(',')
        rows = viewutil.getInfoAttribute(info,'datarow')
        log.log().logger.info("ipVal %s" %ipVal)
        log.log().logger.info('%s, %s' %(test_suite_id,rows))
        rows = rows.split(',')
        log.log().logger.info(rows)
        idrows = []
        for i in range(1,len(rows)):
            idrows.append(rows[i])
        log.log().logger.info(idrows)
        ipList = ipVal.split(',')
        for j in range(len(ipList)):
            if ipList[j] == '':
                result0 = test_batch_manage.test_batch_manage().batch_new_testcase(test_suite_id, idrows,browser_type_list=browser_list)
            else:
                result0 = test_batch_manage.test_batch_manage().batch_new_testcase_IP(test_suite_id, idrows, ipList[j])
        if result0 == 0:
            result = jsonify({'code': 500, 'msg': 'error, please check selected test cases!'})
        else:
            result = jsonify({'code': 200, 'msg': 'message'})
        return result


@mod.route('/general_test_batch', methods=['POST', 'GET'])
@user.authorize
def general_test_batch():
    log.log().logger.info(request)
    if request.method == 'POST':
        log.log().logger.info('post')
        info = request.values
        log.log().logger.info('info :  %s' %info)
        id = viewutil.getInfoAttribute(info, 'test_suite_id')
        log.log().logger.info('id: %s' %id)
        return render_template("uitest/general_test_batch.html",id=id)
    if request.method == 'POST':
        info = request.form
        log.log().logger.info('info :  %s' %info)
        id = viewutil.getInfoAttribute(info, 'id')
        name = viewutil.getInfoAttribute(info,'name')
        run_type = viewutil.getInfoAttribute(info,'run_type')
        description = viewutil.getInfoAttribute(info,'description')
        if run_type == '' or name == '':
            message =  '必填字段不得为空！'
            code = 500
        else:
            test_suite_manage.test_suite_manage().update_test_suite(id, ['name', 'run_type', 'description'], [name, run_type, description])
            message = 'success！'
            code = 200
        result = jsonify({'code': code, 'msg': message})
        return render_template("uitest/test_suite.html")

@mod.route('/edit_test_suite', methods=['POST', 'GET'])
@user.authorize
def edit_test_suite():
    log.log().logger.info(request)
    if request.method == 'GET':
        log.log().logger.info('post')
        info = request.values
        log.log().logger.info('info :  %s' %info)
        id = viewutil.getInfoAttribute(info, 'id')
        log.log().logger.info('id: %s' %id)
        return render_template("uitest/edit_test_suite.html",id=id)
    if request.method == 'POST':
        info = request.form
        log.log().logger.info('info : %s' %info)
        id = viewutil.getInfoAttribute(info, 'id')
        name = viewutil.getInfoAttribute(info,'name')
        run_type = viewutil.getInfoAttribute(info,'run_type')
        description = viewutil.getInfoAttribute(info,'description')
        if run_type == '' or name == '':
            message =  '必填字段不得为空！'
            code = 500
        else:
            test_suite_manage.test_suite_manage().update_test_suite(id, ['name', 'run_type', 'description'], [name, run_type, description])
            message = 'success！'
            code = 200
        result = jsonify({'code': code, 'msg': message})
        return render_template("uitest/test_suite.html")

@mod.route('/delete_test_suite', methods=['POST', 'GET'])
@user.authorize
def delete_test_suite():
    log.log().logger.info(request)
    if request.method == 'GET':
        log.log().logger.info('post')
        info = request.values
        log.log().logger.info('info :  %s' %info)
        id = viewutil.getInfoAttribute(info, 'id')
        log.log().logger.info('id: %s' %id)
        return render_template("uitest/test_suite.html")
    if request.method == 'POST':
        info = request.form
        log.log().logger.info('info : %s' %info)
        id = viewutil.getInfoAttribute(info, 'id')
        act = viewutil.getInfoAttribute(info, 'act')
        if act == 'del':
            test_suite_manage.test_suite_manage().update_test_suite(id, ['isDeleted'], [1])
            code = 200
            message = 'delete success!'
        else:
            code=500
            message = 'act is not del!'
        result = jsonify({'code': code, 'msg': message})
        return result,{'Content-Type': 'application/json'}


@mod.route('/view_test_suite_screenshot', methods=['POST', 'GET'])
@user.authorize
def view_test_suite_screenshot():
    log.log().logger.info(request)
    if request.method == 'GET':
        log.log().logger.info('post')
        info = request.values
        log.log().logger.info('info : %s' %info)
        id = viewutil.getInfoAttribute(info, 'id')
        test_batch_id = viewutil.getInfoAttribute(info, 'test_batch_id')
        type = viewutil.getInfoAttribute(info, 'type')
        index = viewutil.getInfoAttribute(info, 'index')
        if index=='':
            index = 1
        else:
            index = int(index)+1
        log.log().logger.info('id: %s' %id)
        log.log().logger.info('test_batch_id: %s' %test_batch_id)
        data = test_batch_manage.test_batch_manage().show_test_batch(['id'], [id], ['screenshot'], 1)
        log.log().logger.info(data)
        if data[0]['screenshot'] is None:
            imgUrl0 = []
        elif len(data[0]['screenshot']):
            log.log().logger.info('%s, %s' %(len(data[0]['screenshot']),data[0]['screenshot']))
            imgUrl0 = data[0]['screenshot'].split("'")
        else:
            imgUrl0 = []
        imgUrl = []
        imgTitle=[]
        for i in range(len(imgUrl0)):
            if i>0 and i<len(imgUrl0)-1 and len(imgUrl0[i])>5:
                imgUrl.append(imgUrl0[i].replace('\\','/'))
                imgTitle.append(imgUrl0[i])
                log.log().logger.info('%s, %s, %s '%(imgUrl0[i],len(imgUrl0[i]),i))

        if len(imgUrl)== 0:
            return render_template('uitest/view_test_suite_screenshot.html',imgTitle='no screenshot!', imgCnt =len(imgUrl),id = id,test_batch_id=test_batch_id,type=type )
        else:
            log.log().logger.info(imgUrl)
            index = index % len(imgUrl)
            return render_template('uitest/view_test_suite_screenshot.html', imgUrl =imgUrl[index], index = index, id = id,imgTitle = imgTitle[index],imgCnt =len(imgUrl),test_batch_id=test_batch_id,type=type)



@mod.route('/runtest.json', methods=['POST', 'GET'])
@user.authorize
def runtest():
    log.log().logger.info(request)
    if request.method == 'POST':
        log.log().logger.info('post')
        result = jsonify({'code': 500, 'msg': 'should be get!'})
        return result
    else:
        log.log().logger.info(request.values)
        # log.log().logger.info(request.form)
        info = request.values
        id = viewutil.getInfoAttribute(info,'id')
        test_case_id = viewutil.getInfoAttribute(info,'test_case_id')
        ipVal = viewutil.getInfoAttribute(info, 'ipVal')
        type = viewutil.getInfoAttribute(info,'type')
        if type == 'test_suite':
            test_suite_manage.test_suite_manage().new_test_run_list(id)
            result = jsonify({'code': 200, 'msg': 'success!'})
        elif type =='test_suite_rerun_all':
            ipList = ipVal.split(',')
            for i in range(len(ipList)):
                test_suite_manage.test_suite_manage().new_test_run_list(id)
                if ipList[i] == '':
                    test_batch_manage.test_batch_manage().rerun_test_batch(id, 'all')
                else:
                    test_batch_manage.test_batch_manage().rerun_test_batch_Ip(id, 'all', ipList[i])

            result = jsonify({'code': 200, 'msg': 'success!'})
        elif type =='test_suite_rerun_part':
            test_suite_manage.test_suite_manage().new_test_run_list(id)
            test_batch_manage.test_batch_manage().rerun_test_batch(id, 'part')
            result = jsonify({'code': 200, 'msg': 'success!'})
        elif type =='test_batch':
            # test_suite_manage.test_suite_manage().new_test_run_list(id)
            test_batch_manage.test_batch_manage().rerun_test_batch_record(id,test_case_id)
            result = jsonify({'code': 200, 'msg': 'success!'})
        elif type == 'test_case':
            ipList = ipVal.split(',')
            for i in range(len(ipList)):
                if ipList[i] == '':
                    test_batch_manage.test_batch_manage().batch_new_testcase('0', [id])
                else:
                    test_batch_manage.test_batch_manage().batch_new_testcase_IP('0', [id], str(ipList[i]))
            result = jsonify({'code': 200, 'msg': 'success!'})
        else:
            result = jsonify({'code': 500, 'msg': 'type is not defined!'})
        return result



@mod.route('/test_case_runhistory', methods=['POST', 'GET'])
@user.authorize
def test_case_runhistory():
    log.log().logger.info(request)
    if request.method == 'GET':
        log.log().logger.info('post')
        info = request.values
        log.log().logger.info('info :  %s' %info)
        id = viewutil.getInfoAttribute(info, 'id')
        log.log().logger.info('id: %s' %id)
        if len(test_case_manage.test_case_manage().show_test_cases(['id'], [id], [], 2))==1:
            return render_template("uitest/test_batch2.html",id=id,type='test_case',test_suite_id='')
        else:
            return render_template("uitest/test_cases.html")
    else:
        return render_template("uitest/test_cases.html")

@mod.route('/runall')
def runall():
    log.log().logger.info(request)
    import os
    os.system('/opt/flask/flask/runall.sh')
    return render_template("index.html")

@mod.route('/testkeywords')
@user.authorize
def testkeywords():

    return render_template("uitest/test_keywords.html")


@mod.route('/test_keywords.json', methods=['POST', 'GET'])
@user.authorize
def test_keywords():
    if request.method == 'POST':
        log.log().logger.info('post')
    if request.method == 'GET':
        info = request.values
        log.log().logger.info('info : %s' %info)
        limit = info.get('limit', 10)  # 每页显示的条数
        offset = info.get('offset', 0)  # 分片数，(页码-1)*limit，它表示一段数据的起点
        log.log().logger.info('get %s' %limit)
        log.log().logger.info('get  offset %s' %offset)
        id = viewutil.getInfoAttribute(info, 'id')
        keyword = viewutil.getInfoAttribute(info, 'keyword')
        if id=='':
            conditionList = ['keyword']
            valueList = [keyword]
        else:
            conditionList = ['id']
            valueList = [id]
        fieldlist = []
        rows = 1000
        caseList = test_keyword_manage.test_keyword_manage().show_test_keywords(conditionList, valueList, fieldlist, rows)
        log.log().logger.info(caseList)
        data = caseList
        data1 = jsonify({'total': len(data), 'rows': data[int(offset):int(offset)+int(limit)]})
        log.log().logger.info('data1: %s' %data1)
        return data1,{'Content-Type': 'application/json'}


@mod.route('/add_test_keyword', methods=['POST', 'GET'])
@user.authorize
def new_test_keyword():
    return render_template("uitest/new_test_keyword.html")


@mod.route('/add_test_keyword.json', methods=['POST', 'GET'])
@user.authorize
def save_new_test_keyword():
    log.log().logger.info(request)
    info = request.form
    log.log().logger.info('info : %s' %info)
    name = viewutil.getInfoAttribute(info,'name')
    paraCount = viewutil.getInfoAttribute(info,'paraCount')
    description = viewutil.getInfoAttribute(info,'description')
    template = viewutil.getInfoAttribute(info,'template')
    example = viewutil.getInfoAttribute(info, 'example')
    result0 = test_keyword_manage.test_keyword_manage().new_test_keyword(name, paraCount, description, template,example)
    return redirect('/testkeywords')

@mod.route('/edit_test_keyword', methods=['POST', 'GET'])
@user.authorize
def edit_test_keyword():
    log.log().logger.info(request)
    print(request)
    if request.method == 'GET':
        log.log().logger.info('post')
        info = request.values
        log.log().logger.info('info : %s' %info)
        id = viewutil.getInfoAttribute(info, 'id')
        log.log().logger.info('id: %s'%id)
        return render_template("uitest/edit_test_keyword.html",id=id)
    if request.method == 'POST':
        info = request.form
        log.log().logger.info('info : %s' %info)
        print(info)
        id = viewutil.getInfoAttribute(info, 'id')
        name = viewutil.getInfoAttribute(info,'name')
        paraCount = viewutil.getInfoAttribute(info,'paraCount')
        description = viewutil.getInfoAttribute(info,'description')
        template = viewutil.getInfoAttribute(info,'template')
        example = viewutil.getInfoAttribute(info, 'example')
        result = test_keyword_manage.test_keyword_manage().update_test_keyword(id,["keyword", "paraCount", "description", "template","example"],[name, paraCount, description, template,example])
        return redirect('/testkeywords')

@mod.route('/copy_test_keyword', methods=['POST', 'GET'])
@user.authorize
def copy_test_keyword():
    log.log().logger.info(request)
    log.log().logger.info(request.method)
    # log.log().logger.info(request.value)
    if request.method == 'GET':
        log.log().logger.info('post')
        result = jsonify({'code': 500, 'msg': 'should be get!'})
        return result
    if request.method == 'POST':
        info = request.form
        log.log().logger.info('info :  %s' %info)
        id = viewutil.getInfoAttribute(info, 'id')
        log.log().logger.info(id)
        if id=='':
            result = jsonify({'code': 500, 'msg': 'test keyword is not found!'})
        else:
            result0 = test_keyword_manage.test_keyword_manage().copy_test_keyword(id)
            if result0:
                result = jsonify({'code': 200, 'msg': 'copy success!'})
            else:
                result = jsonify({'code': 500, 'msg': 'test keyword is not found!'})
        return result,{'Content-Type': 'application/json'}

@mod.route('/delete_test_keyword', methods=['POST', 'GET'])
@user.authorize
def delete_test_keyword():
    log.log().logger.info(request)
    if request.method == 'GET':
        log.log().logger.info('post')
        info = request.values
        log.log().logger.info('info : %s' %info)
        id = viewutil.getInfoAttribute(info, 'id')
        log.log().logger.info('id: %s' %id)
        return render_template("uitest/test_cases.html")
    if request.method == 'POST':
        info = request.form
        log.log().logger.info('info : %s' %info)
        id = viewutil.getInfoAttribute(info, 'id')
        act = viewutil.getInfoAttribute(info, 'act')
        if act == 'del':
            test_keyword_manage.test_keyword_manage().update_test_keyword(id, ['status'], [0])
            code = 200
            message = 'delete success!'
        else:
            code=500
            message = 'act is not del!'
        result = jsonify({'code': code, 'msg': message})
        return result,{'Content-Type': 'application/json'}

@mod.route('/test_batch_runhistory_report', methods=['POST', 'GET'])
@user.authorize
def test_case_runhistory_report2():
    REMOTE_HOST = "https://pyecharts.github.io/assets/js"
    bar = pyecharts.Pie()
    bar.add("Sports", ["Football", "Basketball", "Baseball", "Tennis", "Swimming"], [23, 34, 45, 56, 67],
            is_more_utils=True)

    log.log().logger.info(request)
    if request.method == 'GET':
        log.log().logger.info('post')
        info = request.values
        log.log().logger.info('info :  %s' %info)
        id = viewutil.getInfoAttribute(info, 'id')
        log.log().logger.info('id: %s' %id)
        if len(test_case_manage.test_case_manage().show_test_cases(['id'], [id], [], 2))==1:
            return render_template("uitest/test_batch_result.html",id=id,type='test_case',test_suite_id='',
                                   myechart=bar.render_embed(),host=REMOTE_HOST,script_list=bar.get_js_dependencies())
        else:
            return render_template("uitest/test_cases.html")
    else:
        return render_template("uitest/test_cases.html")


@mod.route('/test_batch_detail', methods=['POST', 'GET'])
@user.authorize
def test_batch_detail_report():
    REMOTE_HOST = "https://pyecharts.github.io/assets/js"
    bar = pyecharts.Pie()
    bar.width=700
    bar.height=400
    log.log().logger.info(request)
    if request.method == 'GET':
        log.log().logger.info('post')
        info = request.values
        log.log().logger.info('info :  %s' %info)
        id = viewutil.getInfoAttribute(info, 'test_suite_id')
        log.log().logger.info('id: %s' %id)
        statusList = test_batch_manage.test_batch_manage().show_test_batch_status(id)
        nameList , valueList = bar.cast(statusList)
        bar.add("results", ['失败','待执行','执行中','成功'], valueList[0:4],
                is_more_utils=True,is_area_show=True,is_label_show=True,legend_pos="50%")
        return render_template("uitest/test_batch_detail_report.html",id=id,
                                   myechart=bar.render_embed(),host=REMOTE_HOST,script_list=bar.get_js_dependencies())
        # return render_template("uitest/test_batch_report.html", id=id)
    else:
        return render_template('test_suite.html')


@mod.route('/test_public_test_cases.json', methods=['POST', 'GET'])
@user.authorize
def test_public_test_cases():
    if request.method == 'POST':
        log.log().logger.info('post')
    if request.method == 'GET':
        info = request.values
        log.log().logger.info('info : %s' % info)

        conditionList = ['id']
        valueList = [id]
        fieldlist = []
        rows = 1000
        caseList = test_case_manage.test_case_manage().show_test_public_cases()
        log.log().logger.info(caseList)
        data = caseList
        data1 = jsonify({'total': len(data), 'rows': data})
        log.log().logger.info('data1: %s' % data1)
        return data1, {'Content-Type': 'application/json'}


@mod.route('/test_keywords_options.json', methods=['POST', 'GET'])
@user.authorize
def test_keywords_options():
    if request.method == 'POST':
        log.log().logger.info('post')
    if request.method == 'GET':
        info = request.values
        log.log().logger.info('info : %s' % info)

        conditionList = ['id']
        valueList = [id]
        fieldlist = []
        rows = 1000
        caseList = test_keyword_manage.test_keyword_manage().show_test_keywords_options()
        log.log().logger.info(caseList)
        data = caseList
        data1 = jsonify({'total': len(data), 'rows': data})
        log.log().logger.info('data1: %s' % data1)
        return data1, {'Content-Type': 'application/json'}
