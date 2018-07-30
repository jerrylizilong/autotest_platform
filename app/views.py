# from functools import wraps

from flask import render_template, jsonify, request, session, redirect
from app.view import user
from app import app, config, log
# from app.core import util
# from app.db import test_api_manage, test_api_metadata_type_manage, test_unittest_manage,test_case_manage, test_suite_manage, test_batch_manage, test_api_rule_manage, test_api_metadata_manage, \
#     test_api_suit_manage, test_api_url_param_manage, test_file_manage, test_user_manage



@app.route('/')
@app.route('/index')
@user.authorize
def index():
    list = session.get('user', None)
    username = list[0]["username"]
    return render_template("util/index.html", message='Hello, %s' % username)

@app.route('/test')
def index1():
    user = { 'nickname': 'Miguel' } # fake user
    return render_template("util/500.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('util/404.html',message = 'Sorry , page not found!'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('util/500.html', message = 'Something is wrong ,please retry !'), 500


#
# #========================登录模块开始====================================#
# #设置登录认证
# def authorize(fn):
#     @wraps(fn)
#     def wrapper():
#         user = session.get('user', None)
#         if user:
#             log.log().logger.info ("已登录")
#             return fn()
#         else:
#             log.log().logger.info ("未登录")
#             return render_template("util/login.html")
#     return wrapper
#
# #登录页面
# @app.route('/login')
# def login():
#     return render_template("util/login.html")
#
# #检查登录信息是否正确
# @app.route('/checklogin.json', methods=['POST', 'GET'])
# def checklogin():
#     username = request.values.get("username")
#     password = request.values.get("password")
#     log.log().logger.info('username : %s' %username)
#     log.log().logger.info('password : %s' %password)
#     if username=='' or password=='':
#         result = jsonify({'msg': '用户名或密码不能为空'})
#     else:
#         #MD5加密密码
#         md5Password=util.util().md5(password)
#         log.log().logger.info('password : %s' %md5Password)
#         #检查数据是否存在该用户
#         list= test_user_manage.test_user_manage().checklogin(username, md5Password)
#         log.log().logger.info('list : %s' %list)
#         if(len(list)>0):
#             result = jsonify({'msg': '登录成功'})
#             #登录成功设置会话
#             session['user'] = list
#         else:
#             result = jsonify({'msg': '用户名或密码错误'})
#     return result, {'Content-Type': 'application/json'}
#
#
# #登出
# @app.route('/loginout')
# def loginout():
#     session['user']=None
#     return render_template("login.html")
#
#
#
# @app.route('/edit_user_password', methods=['POST', 'GET'])
# @user.authorize
# def edit_user_password():
#     log.log().logger.info(request)
#     return render_template("edit_user_password.html")
#
# @app.route('/user_password.json', methods=['POST', 'GET'])
# def user_password():
#     list = session.get('user', None)
#     id = list[0]["id"]
#     log.log().logger.info('id: %s' %id)
#     info = request.values
#     log.log().logger.info('info : %s' %info)
#     password = getInfoAttribute(info, 'password')
#     log.log().logger.info('password : %s' %password)
#     md5Password = util.util().md5(password)
#     log.log().logger.info('md5Password : %s' %md5Password)
#     test_user_manage.test_user_manage().update_user_password(id, ['password'], [md5Password])
#     result = jsonify({'msg': '修改密码成功'})
#     return result, {'Content-Type': 'application/json'}
#
# #=========================登录模块结束===============================================#


#
# @app.route('/test_suites')
# @user.authorize
# def test_suite():
#
#     return render_template("test_suite.html")
#
# @app.route('/test_cases')
# @user.authorize
# def test_cases():
#
#     return render_template("test_cases.html")
#
# @app.route('/add_test_case', methods=['POST', 'GET'])
# @user.authorize
# def save_new_test_case():
#     log.log().logger.info(request)
#     if request.method == 'GET':
#         log.log().logger.info('post')
#         return render_template("new_test_cases.html")
#     if request.method == 'POST':
#         info = request.form
#         log.log().logger.info('info : %s' %info)
#         name = getInfoAttribute(info,'name')
#         module = getInfoAttribute(info,'module')
#         description = getInfoAttribute(info,'description')
#         steps = getInfoAttribute(info,'steps')
#         log.log().logger.info("steps: %s" %steps)
#         steps=steps.replace('"',"'")
#         log.log().logger.info("steps: %s" %steps)
#         type = getInfoAttribute(info,'type')
#         if module == '' or name == '' or steps=='' or type=='':
#             return '必填字段不得为空！'
#         else:
#             if type=='公共用例':
#                 isPublic = 1
#             else:
#                 isPublic = 0
#             test_case_manage.test_case_manage().new_test_case(module, name, steps, description, isPublic)
#         # return render_template("test_cases.html")
#         return redirect('/test_cases')
#
# @app.route('/edit_test_case', methods=['POST', 'GET'])
# @user.authorize
# def edit_test_case():
#     log.log().logger.info(request)
#     if request.method == 'GET':
#         log.log().logger.info('post')
#         info = request.values
#         log.log().logger.info('info : %s' %info)
#         id = getInfoAttribute(info, 'id')
#         log.log().logger.info('id: %s'%id)
#         return render_template("edit_test_cases.html",id=id)
#     if request.method == 'POST':
#         info = request.form
#         log.log().logger.info('info : %s' %info)
#         id = getInfoAttribute(info, 'id')
#         name = getInfoAttribute(info,'name')
#         module = getInfoAttribute(info,'module')
#         description = getInfoAttribute(info,'description')
#         steps = getInfoAttribute(info,'steps')
#         log.log().logger.info("steps: %s" %steps)
#         steps=steps.replace('"',"'")
#         log.log().logger.info("steps: %s" %steps)
#         type = getInfoAttribute(info,'type')
#         if module == '' or name == '' or steps=='' or type=='':
#             return '必填字段不得为空！'
#         else:
#             if type=='公共用例':
#                 isPublic = 1
#             else:
#                 isPublic = 0
#             test_case_manage.test_case_manage().update_test_case(id, ['module', 'name', 'steps', 'description', 'isPublicFunction'], [module, name, steps, description, isPublic])
#             return render_template("test_batch2.html",id=id,type='test_suite')
#
# @app.route('/copy_test_case', methods=['POST', 'GET'])
# @user.authorize
# def copy_test_case():
#     log.log().logger.info(request)
#     log.log().logger.info(request.method)
#     # log.log().logger.info(request.value)
#     if request.method == 'GET':
#         log.log().logger.info('post')
#         result = jsonify({'code': 500, 'msg': 'should be get!'})
#         return result
#     if request.method == 'POST':
#         info = request.form
#         log.log().logger.info('info :  %s' %info)
#         id = getInfoAttribute(info, 'id')
#         log.log().logger.info(id)
#         if id=='':
#             result = jsonify({'code': 500, 'msg': 'test case is not found!'})
#         else:
#             result0 = test_case_manage.test_case_manage().copy_test_case(id)
#             if result0:
#                 result = jsonify({'code': 200, 'msg': 'copy success!'})
#             else:
#                 result = jsonify({'code': 500, 'msg': 'test case is not found!'})
#         return result
#
# @app.route('/copy_test_suite', methods=['POST', 'GET'])
# @user.authorize
# def copy_test_suite():
#     log.log().logger.info(request)
#     log.log().logger.info(request.method)
#     # log.log().logger.info(request.value)
#     if request.method == 'GET':
#         log.log().logger.info('post')
#         result = jsonify({'code': 500, 'msg': 'should be get!'})
#         return result
#     if request.method == 'POST':
#         info = request.form
#         log.log().logger.info('info :  %s' %info)
#         id = getInfoAttribute(info, 'id')
#         log.log().logger.info("id: %s" %id)
#         if id=='':
#             result = jsonify({'code': 500, 'msg': 'test suite is not found!'})
#         else:
#             import random, time
#             batchId = str(random.randint(10000, 99999)) + str(time.time())
#             test_suite_manage.test_suite_manage().copy_test_suite(id, batchId)
#             newId = test_suite_manage.test_suite_manage().show_test_suites(["batchId"], [batchId], ['id'], 1)
#             log.log().logger.info('newid %s' %newId)
#             if len(newId):
#                 ext = newId[0]['id']
#                 log.log().logger.info('ext is: %s, id is: %s' %(ext, id))
#                 if ext !='0':
#                     test_batch_manage.test_batch_manage().copy_test_batch(ext, id)
#                 message = 'success！'
#                 code = 200
#                 result = jsonify({'code': 200, 'msg': 'copy success!'})
#             else:
#                 result = jsonify({'code': 500, 'msg': 'test suite is not found!'})
#         return result
#
# @app.route('/delete_test_case', methods=['POST', 'GET'])
# @user.authorize
# def delete_test_case():
#     log.log().logger.info(request)
#     if request.method == 'GET':
#         log.log().logger.info('post')
#         info = request.values
#         log.log().logger.info('info : %s' %info)
#         id = getInfoAttribute(info, 'id')
#         log.log().logger.info('id: %s' %id)
#         return render_template("test_cases.html")
#     if request.method == 'POST':
#         info = request.form
#         log.log().logger.info('info : %s' %info)
#         id = getInfoAttribute(info, 'id')
#         act = getInfoAttribute(info, 'act')
#         if act == 'del':
#             test_case_manage.test_case_manage().update_test_case(id, ['status'], [0])
#             code = 200
#             message = 'delete success!'
#         else:
#             code=500
#             message = 'act is not del!'
#         result = jsonify({'code': code, 'msg': message})
#         return result,{'Content-Type': 'application/json'}
#
# @app.route('/test_case.json', methods=['POST', 'GET'])
# @user.authorize
# def search_test_cases():
#     if request.method == 'POST':
#         log.log().logger.info('post')
#     if request.method == 'GET':
#         info = request.values
#         log.log().logger.info('info : %s' %info)
#         limit = info.get('limit', 10)  # 每页显示的条数
#         offset = info.get('offset', 0)  # 分片数，(页码-1)*limit，它表示一段数据的起点
#         log.log().logger.info('get %s' %limit)
#         log.log().logger.info('get  offset %s' %offset)
#         id = getInfoAttribute(info,'id')
#         module = getInfoAttribute(info, 'module')
#         type = getInfoAttribute(info, 'type')
#         log.log().logger.info('module: %s' %module)
#         module = module.split(',')
#         log.log().logger.info(module)
#         name = getInfoAttribute(info, 'name')
#         conditionList = ['name']
#         valueList = [name]
#         if type == 'unattach' and 'public' in module:
#             module.remove('public')
#         elif type!='test_case':
#             if len(module) !=0 and module[0] != 'All' and module[0] != '':
#                 conditionList.append('module')
#                 valueList.append(module)
#             log.log().logger.info('info content: id- %s, module - %s, name - %s, type - %s' %(id,module, name, type))
#         else:
#             conditionList = ['id']
#             valueList = [id]
#             log.log().logger.info('info content: id- %s, module - %s, name - %s, type - %s' %(id,module,name, type))
#         # else:
#         fieldlist = []
#         rows = 1000
#         if type =='unattach':
#             caseList = test_case_manage.test_case_manage().show_test_cases_unattach(id, conditionList, valueList, fieldlist, rows)
#         else:
#             caseList = test_case_manage.test_case_manage().show_test_cases(conditionList, valueList, fieldlist, rows)
#         log.log().logger.info(caseList)
#         data = caseList
#         if type=='test_case':
#             data1 = jsonify({'total': len(data), 'rows': data[0]})
#         else:
#             data1 = jsonify({'total': len(data), 'rows': data[int(offset):int(offset)+int(limit)]})
#         log.log().logger.info('data1: %s' %data1)
#         return data1,{'Content-Type': 'application/json'}
#
#
# @app.route('/test_suite.json', methods=['POST', 'GET'])
# @user.authorize
# def search_test_suite():
#     if request.method == 'POST':
#         log.log().logger.info('post')
#     if request.method == 'GET':
#         info = request.values
#         log.log().logger.info('info : %s' %info)
#         limit = info.get('limit', 10)  # 每页显示的条数
#         offset = info.get('offset', 0)  # 分片数，(页码-1)*limit，它表示一段数据的起点
#         log.log().logger.info('get %s' %limit)
#         log.log().logger.info('get  offset %s' %offset)
#         id = getInfoAttribute(info,'id')
#         type = getInfoAttribute(info, 'type')
#         log.log().logger.info('type %s' %type)
#         run_type = getInfoAttribute(info, 'run_type')
#         status = getInfoAttribute(info, 'status')
#         name = getInfoAttribute(info, 'name')
#         if id =='':
#             if status == 'All':
#                 status = ''
#             log.log().logger.info('info content: %s, %s, %s, %s' %(id,status,run_type, name))
#             conditionList = ['status','run_type','name']
#             valueList = [status,run_type,name]
#         else:
#             if type == 'testview':
#                 statusList = test_batch_manage.test_batch_manage().show_test_batch_status(id)
#             else:
#                 statusList = []
#             log.log().logger.info('info content: %s, %s, %s, %s' %(id,status,run_type, name))
#             conditionList = ['id']
#             valueList = [id]
#         fieldlist = []
#         rows = 1000
#         caseList = test_suite_manage.test_suite_manage().show_test_suites(conditionList, valueList, fieldlist, rows)
#         log.log().logger.info(caseList)
#         data = caseList
#         if id !='':
#             data1 = jsonify({'total': len(data), 'rows': data[0],'status':statusList})
#         else:
#             data1 = jsonify({'total': len(data), 'rows': data[int(offset):int(offset)+int(limit)]})
#         log.log().logger.info('data1: %s' %data1)
#         return data1,{'Content-Type': 'application/json'}
#
# @app.route('/add_test_suite', methods=['POST', 'GET'])
# @user.authorize
# def save_new_test_suite():
#     log.log().logger.info(request)
#     if request.method == 'GET':
#         log.log().logger.info('post')
#         return render_template("new_test_suite.html")
#     if request.method == 'POST':
#         info = request.form
#         log.log().logger.info('info :%s' %info)
#         name = getInfoAttribute(info,'name')
#         run_type = getInfoAttribute(info,'run_type')
#         description = getInfoAttribute(info,'description')
#         if run_type == '' or name == '' :
#             message =  '必填字段不得为空！'
#             code = 500
#         else:
#             import random, time
#             batchId = str(random.randint(10000, 99999)) + str(time.time())
#             test_suite_manage.test_suite_manage().new_test_suite(name, run_type, description, batchId)
#             newId = test_suite_manage.test_suite_manage().show_test_suites(["batchId"], [batchId], ['id'], 1)
#             log.log().logger.info('newid %s' %newId)
#             if len(newId):
#                 ext=newId[0]['id']
#                 log.log().logger.info('ext %s' %ext)
#                 message = 'success！'
#                 code = 200
#             else:
#                 ext=''
#                 message =  'add failed！'
#                 code = 500
#         result = jsonify({'code': code, 'msg': message,'ext':ext})
#         return result
#
# @app.route('/test_batch.json', methods=['POST', 'GET'])
# @user.authorize
# def search_test_batch():
#     if request.method == 'POST':
#         log.log().logger.info('post')
#     if request.method == 'GET':
#         info = request.values
#         log.log().logger.info('info : %s' %info)
#         limit = info.get('limit', 10)  # 每页显示的条数
#         offset = info.get('offset', 0)  # 分片数，(页码-1)*limit，它表示一段数据的起点
#         log.log().logger.info('get %s' %limit)
#         log.log().logger.info('get  offset %s' %offset)
#         id = getInfoAttribute(info,'id')
#         name = getInfoAttribute(info, 'name')
#         status = getInfoAttribute(info, 'status')
#         module = getInfoAttribute(info, 'module')
#         ipVal = getInfoAttribute(info, 'ipVal')
#         type = getInfoAttribute(info, 'type')
#         log.log().logger.info('module: %s' %module)
#         log.log().logger.info('ipVal %s' %ipVal)
#         module = module.split(',')
#         log.log().logger.info(module)
#         valueList = []
#         conditionList = []
#         if id == '':
#             data1 = jsonify({'total': 0, 'rows': []})
#         else:
#             if name != '':
#                 conditionList.append('name')
#                 valueList.append(name)
#             if status != '':
#                 conditionList.append('status')
#                 valueList.append(status)
#             if len(module) !=0 and module[0] != 'All' and module[0] != '':
#                 conditionList.append('module')
#                 valueList.append(module)
#             ipList = ipVal.split(',')
#             for j in range(len(ipList)):
#                 if ipList[j] !='':
#                     conditionList.append('ip')
#                     valueList.append(ipList[j])
#             fieldlist = []
#             rows = 1000
#             if type == "" or type=='test_suite':
#                 conditionList.append('test_suite_id')
#                 valueList.append(id)
#                 caseList = test_batch_manage.test_batch_manage().show_test_batch(conditionList, valueList, fieldlist, rows)
#                 log.log().logger.info("caseList %s" %caseList)
#                 data = caseList
#             elif type=='test_case':
#                 conditionList.append('test_case_id')
#                 valueList.append(id)
#                 caseList = test_batch_manage.test_batch_manage().show_test_batch(conditionList, valueList, fieldlist, rows)
#                 log.log().logger.info(caseList)
#                 data = caseList
#             else:
#                 caseList = test_case_manage.test_case_manage().show_test_cases_unattach(id, conditionList, valueList, fieldlist, rows)
#                 log.log().logger.info(caseList)
#                 data = caseList
#             data1 = jsonify({'total': len(data), 'rows': data[int(offset):int(offset)+int(limit)]})
#             log.log().logger.info('data1: %s' %data1)
#         return data1,{'Content-Type': 'application/json'}
#
# @app.route('/test_batch_detail', methods=['POST', 'GET'])
# @user.authorize
# def test_batch_detail():
#     log.log().logger.info(request)
#     if request.method == 'GET':
#         log.log().logger.info('post')
#         info = request.values
#         log.log().logger.info('info :  %s' %info)
#         id = getInfoAttribute(info, 'test_suite_id')
#         log.log().logger.info('id: %s' %id)
#         return render_template("test_batch_detail.html",id=id)
#         # return render_template("test_batch_report.html", id=id)
#     else:
#         return render_template('test_suite.html')
#
# @app.route('/attach_test_batch', methods=['POST', 'GET'])
# @user.authorize
# def attach_test_batch():
#     log.log().logger.info(request)
#     if request.method == 'GET':
#         log.log().logger.info('post')
#         info = request.values
#         log.log().logger.info('info :  %s' %info)
#         id = getInfoAttribute(info, 'test_suite_id')
#         log.log().logger.info('id: %s' %id)
#         return render_template("attach_test_batch.html",id=id)
#     else:
#         return render_template("test_suite.html")
#
# @app.route('/attach_test_batch.json', methods=['POST', 'GET'])
# @user.authorize
# def attach_test_batch_to_suite():
#     log.log().logger.info(request)
#     if request.method == 'POST':
#         log.log().logger.info('post')
#         result = jsonify({'code': 500, 'msg': 'post'})
#         return result
#     else:
#         log.log().logger.info(request.values)
#         # log.log().logger.info(request.form)
#         info = request.values
#         test_suite_id = getInfoAttribute(info,'test_suite_id')
#         ipVal = getInfoAttribute(info, 'ipVal')
#         rows = getInfoAttribute(info,'datarow')
#         log.log().logger.info("ipVal %s" %ipVal)
#         log.log().logger.info('%s, %s' %(test_suite_id,rows))
#         rows = rows.split(',')
#         log.log().logger.info(rows)
#         idrows = []
#         for i in range(1,len(rows)):
#             idrows.append(rows[i])
#         log.log().logger.info(idrows)
#         ipList = ipVal.split(',')
#         for j in range(len(ipList)):
#             if ipList[j] == '':
#                 result0 = test_batch_manage.test_batch_manage().batch_new_testcase(test_suite_id, idrows)
#             else:
#                 result0 = test_batch_manage.test_batch_manage().batch_new_testcase_IP(test_suite_id, idrows, ipList[j])
#         if result0 == 0:
#             result = jsonify({'code': 500, 'msg': 'error, please check selected test cases!'})
#         else:
#             result = jsonify({'code': 200, 'msg': 'message'})
#         return result
#
#
# @app.route('/general_test_batch', methods=['POST', 'GET'])
# @user.authorize
# def general_test_batch():
#     log.log().logger.info(request)
#     if request.method == 'POST':
#         log.log().logger.info('post')
#         info = request.values
#         log.log().logger.info('info :  %s' %info)
#         id = getInfoAttribute(info, 'test_suite_id')
#         log.log().logger.info('id: %s' %id)
#         return render_template("general_test_batch.html",id=id)
#     if request.method == 'POST':
#         info = request.form
#         log.log().logger.info('info :  %s' %info)
#         id = getInfoAttribute(info, 'id')
#         name = getInfoAttribute(info,'name')
#         run_type = getInfoAttribute(info,'run_type')
#         description = getInfoAttribute(info,'description')
#         if run_type == '' or name == '':
#             message =  '必填字段不得为空！'
#             code = 500
#         else:
#             test_suite_manage.test_suite_manage().update_test_suite(id, ['name', 'run_type', 'description'], [name, run_type, description])
#             message = 'success！'
#             code = 200
#         result = jsonify({'code': code, 'msg': message})
#         return render_template("test_suite.html")
#
# @app.route('/edit_test_suite', methods=['POST', 'GET'])
# @user.authorize
# def edit_test_suite():
#     log.log().logger.info(request)
#     if request.method == 'GET':
#         log.log().logger.info('post')
#         info = request.values
#         log.log().logger.info('info :  %s' %info)
#         id = getInfoAttribute(info, 'id')
#         log.log().logger.info('id: %s' %id)
#         return render_template("edit_test_suite.html",id=id)
#     if request.method == 'POST':
#         info = request.form
#         log.log().logger.info('info : %s' %info)
#         id = getInfoAttribute(info, 'id')
#         name = getInfoAttribute(info,'name')
#         run_type = getInfoAttribute(info,'run_type')
#         description = getInfoAttribute(info,'description')
#         if run_type == '' or name == '':
#             message =  '必填字段不得为空！'
#             code = 500
#         else:
#             test_suite_manage.test_suite_manage().update_test_suite(id, ['name', 'run_type', 'description'], [name, run_type, description])
#             message = 'success！'
#             code = 200
#         result = jsonify({'code': code, 'msg': message})
#         return render_template("test_suite.html")
#
# @app.route('/delete_test_suite', methods=['POST', 'GET'])
# @user.authorize
# def delete_test_suite():
#     log.log().logger.info(request)
#     if request.method == 'GET':
#         log.log().logger.info('post')
#         info = request.values
#         log.log().logger.info('info :  %s' %info)
#         id = getInfoAttribute(info, 'id')
#         log.log().logger.info('id: %s' %id)
#         return render_template("test_suite.html")
#     if request.method == 'POST':
#         info = request.form
#         log.log().logger.info('info : %s' %info)
#         id = getInfoAttribute(info, 'id')
#         act = getInfoAttribute(info, 'act')
#         if act == 'del':
#             test_suite_manage.test_suite_manage().update_test_suite(id, ['isDeleted'], [1])
#             code = 200
#             message = 'delete success!'
#         else:
#             code=500
#             message = 'act is not del!'
#         result = jsonify({'code': code, 'msg': message})
#         return result,{'Content-Type': 'application/json'}
#
#
# @app.route('/view_test_suite_screenshot', methods=['POST', 'GET'])
# @user.authorize
# def view_test_suite_screenshot():
#     log.log().logger.info(request)
#     if request.method == 'GET':
#         log.log().logger.info('post')
#         info = request.values
#         log.log().logger.info('info : %s' %info)
#         id = getInfoAttribute(info, 'id')
#         test_batch_id = getInfoAttribute(info, 'test_batch_id')
#         type = getInfoAttribute(info, 'type')
#         index = getInfoAttribute(info, 'index')
#         if index=='':
#             index = 1
#         else:
#             index = int(index)+1
#         log.log().logger.info('id: %s' %id)
#         log.log().logger.info('test_batch_id: %s' %test_batch_id)
#         data = test_batch_manage.test_batch_manage().show_test_batch(['id'], [id], ['screenshot'], 1)
#         log.log().logger.info(data)
#         if data[0]['screenshot'] is None:
#             imgUrl0 = []
#         elif len(data[0]['screenshot']):
#             log.log().logger.info('%s, %s' %(len(data[0]['screenshot']),data[0]['screenshot']))
#             imgUrl0 = data[0]['screenshot'].split("'")
#         else:
#             imgUrl0 = []
#         imgUrl = []
#         imgTitle=[]
#         for i in range(len(imgUrl0)):
#             if i>0 and i<len(imgUrl0)-1 and len(imgUrl0[i])>5:
#                 imgUrl.append(imgUrl0[i].replace('\\','/'))
#                 imgTitle.append(imgUrl0[i])
#                 log.log().logger.info('%s, %s, %s '%(imgUrl0[i],len(imgUrl0[i]),i))
#
#         if len(imgUrl)== 0:
#             return render_template('view_test_suite_screenshot.html',imgTitle='no screenshot!', imgCnt =len(imgUrl),id = id,test_batch_id=test_batch_id,type=type )
#         else:
#             log.log().logger.info(imgUrl)
#             index = index % len(imgUrl)
#             return render_template('view_test_suite_screenshot.html', imgUrl =imgUrl[index], index = index, id = id,imgTitle = imgTitle[index],imgCnt =len(imgUrl),test_batch_id=test_batch_id,type=type)
#
#
#
# @app.route('/runtest.json', methods=['POST', 'GET'])
# @user.authorize
# def runtest():
#     log.log().logger.info(request)
#     if request.method == 'POST':
#         log.log().logger.info('post')
#         result = jsonify({'code': 500, 'msg': 'should be get!'})
#         return result
#     else:
#         log.log().logger.info(request.values)
#         # log.log().logger.info(request.form)
#         info = request.values
#         id = getInfoAttribute(info,'id')
#         ipVal = getInfoAttribute(info, 'ipVal')
#         type = getInfoAttribute(info,'type')
#         if type == 'test_suite':
#             test_suite_manage.test_suite_manage().new_test_run_list(id)
#             result = jsonify({'code': 200, 'msg': 'success!'})
#         elif type =='test_suite_rerun_all':
#             ipList = ipVal.split(',')
#             for i in range(len(ipList)):
#                 test_suite_manage.test_suite_manage().new_test_run_list(id)
#                 if ipList[i] == '':
#                     test_batch_manage.test_batch_manage().rerun_test_batch(id, 'all')
#                 else:
#                     test_batch_manage.test_batch_manage().rerun_test_batch_Ip(id, 'all', ipList[i])
#
#             result = jsonify({'code': 200, 'msg': 'success!'})
#         elif type =='test_suite_rerun_part':
#             test_suite_manage.test_suite_manage().new_test_run_list(id)
#             test_batch_manage.test_batch_manage().rerun_test_batch(id, 'part')
#             result = jsonify({'code': 200, 'msg': 'success!'})
#         elif type == 'test_case':
#             ipList = ipVal.split(',')
#             for i in range(len(ipList)):
#                 if ipList[i] == '':
#                     test_batch_manage.test_batch_manage().batch_new_testcase('0', [id])
#                 else:
#                     test_batch_manage.test_batch_manage().batch_new_testcase_IP('0', [id], str(ipList[i]))
#             result = jsonify({'code': 200, 'msg': 'success!'})
#         else:
#             result = jsonify({'code': 500, 'msg': 'type is not defined!'})
#         return result
#
#
#
# @app.route('/test_case_runhistory', methods=['POST', 'GET'])
# @user.authorize
# def test_case_runhistory():
#     log.log().logger.info(request)
#     if request.method == 'GET':
#         log.log().logger.info('post')
#         info = request.values
#         log.log().logger.info('info :  %s' %info)
#         id = getInfoAttribute(info, 'id')
#         log.log().logger.info('id: %s' %id)
#         if len(test_case_manage.test_case_manage().show_test_cases(['id'], [id], [], 2))==1:
#             return render_template("test_batch2.html",id=id,type='test_case',test_suite_id='')
#         else:
#             return render_template("test_cases.html")
#     else:
#         return render_template("test_cases.html")
#
# @app.route('/runall')
# def runall():
#     log.log().logger.info(request)
#     import os
#     os.system('/opt/flask/flask/runall.sh')
#     return render_template("index.html")
#


def getInfoAttribute(info,field):
    try:
        value = info.get(field)
    except:
        value = ''
    if value == None:
        value = ''
    return value


#
# #########################api自动化功能开发开始###############################################
# #api功能主页
# @app.route('/test_api')
# @user.authorize
# def test_api():
#     return render_template("test_api.html")
# #api查询
# @app.route('/test_api.json', methods=['POST', 'GET'])
# @user.authorize
# def search_test_api():
#     if request.method == 'POST':
#         log.log().logger.info('post')
#     if request.method == 'GET':
#         info = request.values
#         log.log().logger.info('info : %s' %info)
#         limit = info.get('limit', 10)  # 每页显示的条数
#         offset = info.get('offset', 0)  # 分片数，(页码-1)*limit，它表示一段数据的起点
#         log.log().logger.info('get %s' %limit)
#         log.log().logger.info('get  offset %s' %offset)
#
#         id = getInfoAttribute(info, 'id')
#         name = getInfoAttribute(info, 'name')
#         conditionList = ['id','name']
#         valueList = [id,name]
#         fieldlist = []
#         rows = 1000
#         caseList = test_api_manage.test_api_manage().show_test_api(conditionList, valueList, fieldlist, rows)
#         log.log().logger.info(caseList)
#         data = caseList
#         data1 = jsonify({'total': len(data), 'rows': data[int(offset):int(offset) + int(limit)]})
#         log.log().logger.info('data1: %s' %data1)
#         return data1, {'Content-Type': 'application/json'}
# #api新增界面入口与新增成功跳转
# @app.route('/add_test_api', methods=['POST', 'GET'])
# @user.authorize
# def save_new_test_api():
#     log.log().logger.info(request)
#     if request.method == 'GET':
#         log.log().logger.info('post')
#         return render_template("new_test_api.html")
#     if request.method == 'POST':
#         info = request.form
#         log.log().logger.info('info :  %s' %info)
#         name = getInfoAttribute(info, 'name')
#         description = getInfoAttribute(info, 'description')
#         url = getInfoAttribute(info, 'url')
#         para = getInfoAttribute(info, 'para')
#         signMothed = getInfoAttribute(info, 'signMothed')
#         signList = getInfoAttribute(info, 'signList')
#         method = getInfoAttribute(info, 'method')
#         status=1
#         # if name == '' or url == '' or para == '':
#         if name == '':
#             return '必填字段不得为空！'
#         else:
#             import random, time
#             batchId = str(random.randint(10000, 99999)) + str(time.time())
#             id = test_api_manage.test_api_manage().new_test_api(name, description, url, para, signMothed, signList, method, status, batchId)
#             # if id !='':
#                 # from app.apitest import runCase
#                 # runCase.test_update_osignNameList(id)
#             return render_template("edit_test_api.html",id=id)
# #api删除
# @app.route('/delete_test_api', methods=['POST', 'GET'])
# @user.authorize
# def delete_test_api():
#     log.log().logger.info(request)
#     if request.method == 'GET':
#         log.log().logger.info('post')
#         info = request.values
#         log.log().logger.info('info :  %s' %info)
#         id = getInfoAttribute(info, 'id')
#         log.log().logger.info('id: %s' %id)
#         return render_template("test_api.html")
#     if request.method == 'POST':
#         info = request.form
#         log.log().logger.info('info :  %s' %info)
#         id = getInfoAttribute(info, 'id')
#         act = getInfoAttribute(info, 'act')
#         if act == 'del':
#             test_api_manage.test_api_manage().del_test_api(id, ['status'], ['0'])
#             code = 200
#             message = 'delete success!'
#         else:
#             code = 500
#             message = 'act is not del!'
#         result = jsonify({'code': code, 'msg': message})
#         return result, {'Content-Type': 'application/json'}
# #api修改
# @app.route('/edit_test_api', methods=['POST', 'GET'])
# @user.authorize
# def edit_test_api():
#     log.log().logger.info(request)
#     if request.method == 'GET':
#         log.log().logger.info('post')
#         info = request.values
#         log.log().logger.info('info :  %s' %info)
#         id = getInfoAttribute(info, 'id')
#         log.log().logger.info('id: %s' %id)
#         return render_template("edit_test_api.html", id=id)
#     if request.method == 'POST':
#         info = request.form
#         log.log().logger.info('info : %s' %info)
#         id = getInfoAttribute(info, 'id')
#         name = getInfoAttribute(info, 'name')
#         description = getInfoAttribute(info, 'description')
#         url = getInfoAttribute(info, 'url')
#         para = getInfoAttribute(info, 'para')
#         signMothed = getInfoAttribute(info, 'signMothed')
#         signList = getInfoAttribute(info, 'signList')
#         method = getInfoAttribute(info, 'method')
#         if name == '' or url == '' or para == '':
#             return '必填字段不得为空！'
#         else:
#             test_api_manage.test_api_manage().update_test_api(id, ['name', 'description', 'url', 'para', 'signMothed', 'signList', 'method'], [name, description, url, para, signMothed, signList, method])
#             from app.apitest import runCase
#             runCase.test_update_osignNameList(id)
#             return render_template("test_api.html", id=id)
# #api查询url
# @app.route('/test_api_url_manage.json', methods=['POST', 'GET'])
# @user.authorize
# def search_test_api_url_manage():
#     if request.method == 'POST':
#         log.log().logger.info('post')
#     if request.method == 'GET':
#         info = request.values
#         log.log().logger.info('info : %s' %info)
#         conditionList = []
#         valueList = []
#         fieldlist = []
#         rows = 1000
#         caseList = test_api_manage.test_api_manage().show_test_api_manage(conditionList, valueList, fieldlist, rows)
#         log.log().logger.info(caseList)
#         data = caseList
#         data1 = jsonify({'total': len(data), 'rows': data})
#         log.log().logger.info('data1: %s' %data1)
#         return data1, {'Content-Type': 'application/json'}
#
# @app.route('/copy_test_api', methods=['POST', 'GET'])
# @user.authorize
# def copy_test_api():
#     log.log().logger.info(request)
#     log.log().logger.info(request.method)
#     # log.log().logger.info(request.value)
#     if request.method == 'GET':
#         log.log().logger.info('post')
#         result = jsonify({'code': 500, 'msg': 'should be get!'})
#         return result
#     if request.method == 'POST':
#         info = request.form
#         log.log().logger.info('info :  %s' %info)
#         id = getInfoAttribute(info, 'id')
#         log.log().logger.info(id)
#         if id == '':
#             result = jsonify({'code': 500, 'msg': 'test case is not found!'})
#         else:
#             result0 = test_api_manage.test_api_manage().copy_test_api(id)
#             if result0:
#                 result = jsonify({'code': 200, 'msg': 'copy success!'})
#             else:
#                 result = jsonify({'code': 500, 'msg': 'test case is not found!'})
#         return result
#
#
#
# # 测试用例执行结果主页
# @app.route('/test_api_batch_history', methods=['POST', 'GET'])
# @user.authorize
# def test_api_batch_history():
#     log.log().logger.info(request)
#     if request.method == 'GET':
#         log.log().logger.info('post')
#         info = request.values
#         log.log().logger.info('info : %s' %info)
#         id = getInfoAttribute(info, 'id')
#         log.log().logger.info('id: %s' %id)
#         return render_template("test_api_batch_history.html", id=id)
#     else:
#         return render_template("test_api.html")
#
# # 查询测试用例所有的批次
# @app.route('/test_api_batch_history.json', methods=['POST', 'GET'])
# @user.authorize
# def search_test_api_batch_history():
#     if request.method == 'POST':
#         log.log().logger.info('post')
#     if request.method == 'GET':
#         info = request.values
#         log.log().logger.info('info :  %s' %info)
#         limit = info.get('limit', 10)  # 每页显示的条数
#         offset = info.get('offset', 0)  # 分片数，(页码-1)*limit，它表示一段数据的起点
#         log.log().logger.info('get %s' %limit)
#         log.log().logger.info('get  offset %s' %offset)
#         url_id = getInfoAttribute(info, 'id')
#         name = getInfoAttribute(info, 'name')
#         conditionList = ['url_id', 'name']
#         valueList = [url_id, name]
#         fieldlist = []
#         rows = 1000
#         caseList = test_api_manage.test_api_manage().show_test_api_batch_history(conditionList, valueList, fieldlist, rows)
#         log.log().logger.info(caseList)
#         data = caseList
#         data1 = jsonify({'total': len(data), 'rows': data[int(offset):int(offset) + int(limit)]})
#         log.log().logger.info('data1: %s' %data1)
#         return data1, {'Content-Type': 'application/json'}
#
# # 可编辑参数主页
# @app.route('/test_api_para_type', methods=['POST', 'GET'])
# @user.authorize
# def test_api_para_type():
#     log.log().logger.info(request)
#     if request.method == 'GET':
#         log.log().logger.info('post')
#         info = request.values
#         log.log().logger.info('info : %s' %info)
#         id = getInfoAttribute(info, 'id')
#         log.log().logger.info('id: %s' %id)
#         para = getInfoAttribute(info, 'para')
#         log.log().logger.info('para: %s' %para)
#         return render_template("test_api_para_type.html", id=id,para=para)
#     else:
#         return render_template("test_api.html")
#
# #url 参数主页
# @app.route('/test_api_url_param')
# @user.authorize
# def test_api_url_param():
#     info = request.values
#     urlId = getInfoAttribute(info, 'urlId')
#     log.log().logger.info('urlId %s' %urlId)
#     return render_template("test_api_url_param.html",urlId=urlId)
#
# @app.route('/test_api_url_param.json', methods=['POST', 'GET'])
# @user.authorize
# def search_test_api_url_param():
#     if request.method == 'POST':
#         log.log().logger.info('post')
#     if request.method == 'GET':
#         info = request.values
#         log.log().logger.info('info : %s' %info)
#         limit = info.get('limit', 10)  # 每页显示的条数
#         offset = info.get('offset', 0)  # 分片数，(页码-1)*limit，它表示一段数据的起点
#         log.log().logger.info('get %s' %limit)
#         log.log().logger.info('get  offset %s' %offset)
#
#         id = getInfoAttribute(info, 'id')
#         name = getInfoAttribute(info, 'name')
#         urlId = getInfoAttribute(info, 'urlId')
#         log.log().logger.info('get  offset %s' %offset)
#         conditionList = ['id', 'name','urlId']
#         valueList = [id, name,urlId]
#         fieldlist = []
#         rows = 1000
#         caseList = test_api_url_param_manage.test_api_url_param_manage().show_test_api_url_param(conditionList,
#                                                                                                  valueList, fieldlist,
#                                                                                                  rows)
#         log.log().logger.info(caseList)
#         data = caseList
#         data1 = jsonify({'total': len(data), 'rows': data[int(offset):int(offset) + int(limit)]})
#         log.log().logger.info('data1: %s' %data1)
#         return data1, {'Content-Type': 'application/json'}
#
# # api新增界面入口与新增成功跳转
# @app.route('/add_test_api_url_param', methods=['POST', 'GET'])
# @user.authorize
# def save_new_test_api_url_param():
#     log.log().logger.info(request)
#     if request.method == 'GET':
#         info = request.values
#         urlId = getInfoAttribute(info, 'urlId')
#         log.log().logger.info('urlId :  %s' %urlId)
#         return render_template("new_test_api_url_param.html",urlId=urlId)
#     if request.method == 'POST':
#         info = request.form
#         log.log().logger.info('info :  %s' %info)
#         lenth = getInfoAttribute(info, 'lenth')
#         order = getInfoAttribute(info, 'order')
#         type = getInfoAttribute(info, 'type')
#         name = getInfoAttribute(info, 'name')
#         isNull = getInfoAttribute(info, 'isNull')
#         enumValue = getInfoAttribute(info, 'enumValue')
#         urlId = getInfoAttribute(info, 'urlId')
#         if name == '':
#             return '必填字段不得为空！'
#         else:
#             test_api_url_param_manage.test_api_url_param_manage().new_test_api_url_param(lenth, order, type, name, isNull, enumValue, urlId)
#             return render_template("test_api_url_param.html",urlId=urlId)
#
# # api删除
# @app.route('/delete_test_api_url_param', methods=['POST', 'GET'])
# @user.authorize
# def delete_test_api_url_param():
#     log.log().logger.info(request)
#     if request.method == 'GET':
#         log.log().logger.info('post')
#         info = request.values
#         log.log().logger.info('info :  %s' %info)
#         id = getInfoAttribute(info, 'id')
#         log.log().logger.info('id: %s' %id)
#         urlId = getInfoAttribute(info, 'urlId')
#         log.log().logger.info('urlId: %s' %urlId)
#         return render_template("test_api_url_param.html",urlId=urlId)
#     if request.method == 'POST':
#         info = request.form
#         log.log().logger.info('info :  %s' %info)
#         id = getInfoAttribute(info, 'id')
#         act = getInfoAttribute(info, 'act')
#         if act == 'del':
#             test_api_url_param_manage.test_api_url_param_manage().del_test_api_url_param(id)
#             code = 200
#             message = 'delete success!'
#         else:
#             code = 500
#             message = 'act is not del!'
#         result = jsonify({'code': code, 'msg': message})
#         return result, {'Content-Type': 'application/json'}
#
# # api修改
# @app.route('/edit_test_api_url_param', methods=['POST', 'GET'])
# @user.authorize
# def edit_test_api_url_param():
#     log.log().logger.info(request)
#     if request.method == 'GET':
#         log.log().logger.info('post')
#         info = request.values
#         log.log().logger.info('info : %s' %info)
#         id = getInfoAttribute(info, 'id')
#         log.log().logger.info('id: %s' %id)
#         urlId = getInfoAttribute(info, 'urlId')
#         log.log().logger.info('urlId: %s' %urlId)
#         return render_template("edit_test_api_url_param.html", id=id,urlId=urlId)
#     if request.method == 'POST':
#         info = request.form
#         log.log().logger.info('info : %s' %info)
#         id = getInfoAttribute(info, 'id')
#         lenth = getInfoAttribute(info, 'lenth')
#         order = getInfoAttribute(info, 'order')
#         type = getInfoAttribute(info, 'type')
#         name = getInfoAttribute(info, 'name')
#         isNull = getInfoAttribute(info, 'isNull')
#         enumValue = getInfoAttribute(info, 'enumValue')
#         urlId = getInfoAttribute(info, 'urlId')
#         if name == '':
#             return '必填字段不得为空！'
#         else:
#             test_api_url_param_manage.test_api_url_param_manage().update_test_api_url_param(id, ['lenth', '`order`', 'type', '`name`', 'isNull', 'enumValue'], [lenth, order, type, name, isNull, enumValue])
#             return render_template("test_api_url_param.html", id=id,urlId=urlId)
#
#
#
# @app.route('/save_test_api_url_param', methods=['POST', 'GET'])
# @user.authorize
# def save_test_api_url_param():
#     log.log().logger.info(request)
#     if request.method == 'GET':
#         log.log().logger.info('post')
#         info = request.values
#         log.log().logger.info('info :  %s' %info)
#         id = getInfoAttribute(info, 'id')
#         log.log().logger.info('id: %s' %id)
#         urlId = getInfoAttribute(info, 'urlId')
#         log.log().logger.info('urlId: %s' %urlId)
#         return render_template("test_api_url_param.html", urlId=urlId)
#     if request.method == 'POST':
#         info = request.form
#         log.log().logger.info('info : %s' %info)
#         id = getInfoAttribute(info, 'id')
#         act = getInfoAttribute(info, 'act')
#         if act == 'save':
#             conditionList = [ 'urlId']
#             valueList = [id]
#             fieldlist = []
#             rows = 1000
#             list = test_api_url_param_manage.test_api_url_param_manage().find_test_api_url_param(conditionList, valueList, fieldlist, rows)
#             log.log().logger.info('list: %s' %list)
#             #拼接参数
#             paramStr=''
#             for i in range(len(list)):
#                 log.log().logger.info('list: %s' %list[i])
#                 paramStr+=str(list[i])
#             log.log().logger.info('paramStr: %s' %paramStr)
#             #替换字符串
#             paramStr=paramStr.replace('{','')
#             paramStr = paramStr.replace('}', '||')
#             paramStr=paramStr.rstrip('||')
#             log.log().logger.info('paramStrenen: %s' %paramStr)
#             #更新参数
#             test_api_url_param_manage.test_api_url_param_manage().update_test_api_url(id, ['para'], [paramStr])
#             code = 200
#             message = 'save success!'
#         else:
#             code = 500
#             message = 'act is not save!'
#         result = jsonify({'code': code, 'msg': message})
#         return result, {'Content-Type': 'application/json'}
#
#
# #api参数编辑
# @app.route('/test_api_url_param_edit_bootstrap')
# @user.authorize
# def test_api_url_param_edit_bootstrap():
#     info = request.values
#     urlId = getInfoAttribute(info, 'urlId')
#     para = getInfoAttribute(info, 'para')
#     log.log().logger.info('urlId %s' %urlId)
#     log.log().logger.info('para %s' %para)
#     return render_template("edit_test_api_url_param_bootstrap.html", urlId=urlId,para=para)
#
# #api参数保存
# @app.route('/test_api_url_param_save')
# def test_api_url_param_save():
#     info = request.values
#     id = getInfoAttribute(info, 'urlId')
#     para = getInfoAttribute(info, 'para')
#     log.log().logger.info('id %s' %id)
#     log.log().logger.info('para %s' %para)
#     test_api_manage.test_api_manage().update_test_api(id, ['para'], [para])
#     return render_template("edit_test_api.html", id=id)
#
#
#
#
# #########################api自动化功能开发结束###############################################
#
# #########################api test rule自动化功能开发开始###############################################
# #api功能主页
# @app.route('/test_api_rule')
# @user.authorize
# def test_api_rule():
#     return render_template("test_api_rule.html")
# #api查询
# @app.route('/test_api_rule.json', methods=['POST', 'GET'])
# def search_test_api_rule():
#     if request.method == 'POST':
#         log.log().logger.info('post')
#     if request.method == 'GET':
#         info = request.values
#         log.log().logger.info('info : %s' %info)
#         limit = info.get('limit', 10)  # 每页显示的条数
#         offset = info.get('offset', 0)  # 分片数，(页码-1)*limit，它表示一段数据的起点
#         log.log().logger.info('get %s' %limit)
#         log.log().logger.info('get  offset %s' %offset)
#
#         id = getInfoAttribute(info, 'id')
#         name = getInfoAttribute(info, 'name')
#         conditionList = ['id','name']
#         valueList = [id,name]
#         fieldlist = []
#         rows = 1000
#         caseList = test_api_rule_manage.test_api_rule_manage().show_test_api_rule(conditionList, valueList, fieldlist, rows)
#         log.log().logger.info(caseList)
#         data = caseList
#         data1 = jsonify({'total': len(data), 'rows': data[int(offset):int(offset) + int(limit)]})
#         log.log().logger.info('data1: %s' %data1)
#         return data1, {'Content-Type': 'application/json'}
# #api新增界面入口与新增成功跳转
# @app.route('/add_test_api_rule', methods=['POST', 'GET'])
# @user.authorize
# def save_new_test_api_rule():
#     log.log().logger.info(request)
#     if request.method == 'GET':
#         log.log().logger.info('post')
#         return render_template("new_test_api_rule.html")
#     if request.method == 'POST':
#         info = request.form
#         log.log().logger.info('info : %s' %info)
#         name = getInfoAttribute(info, 'name')
#         description = getInfoAttribute(info, 'description')
#         if name == '':
#             return '必填字段不得为空！'
#         else:
#             test_api_rule_manage.test_api_rule_manage().new_test_api_rule(name, description)
#             return render_template("test_api_rule.html")
# #api删除
# @app.route('/delete_test_api_rule', methods=['POST', 'GET'])
# @user.authorize
# def delete_test_api_rule():
#     log.log().logger.info(request)
#     if request.method == 'GET':
#         log.log().logger.info('post')
#         info = request.values
#         log.log().logger.info('info : %s' %info)
#         id = getInfoAttribute(info, 'id')
#         log.log().logger.info('id: %s' %id)
#         return render_template("test_api_rule.html")
#     if request.method == 'POST':
#         info = request.form
#         log.log().logger.info('info : %s' %info)
#         id = getInfoAttribute(info, 'id')
#         act = getInfoAttribute(info, 'act')
#         if act == 'del':
#             test_api_rule_manage.test_api_rule_manage().del_test_api_rule(id)
#             code = 200
#             message = 'delete success!'
#         else:
#             code = 500
#             message = 'act is not del!'
#         result = jsonify({'code': code, 'msg': message})
#         return result, {'Content-Type': 'application/json'}
# #api修改
# @app.route('/edit_test_api_rule', methods=['POST', 'GET'])
# @user.authorize
# def edit_test_api_rule():
#     log.log().logger.info(request)
#     if request.method == 'GET':
#         log.log().logger.info('post')
#         info = request.values
#         log.log().logger.info('info :  %s' %info)
#         id = getInfoAttribute(info, 'id')
#         log.log().logger.info('id: %s' %id)
#         return render_template("edit_test_api_rule.html", id=id)
#     if request.method == 'POST':
#         info = request.form
#         log.log().logger.info('info : %s' %info)
#         id = getInfoAttribute(info, 'id')
#         name = getInfoAttribute(info, 'name')
#         description = getInfoAttribute(info, 'description')
#         if name == '':
#             return '必填字段不得为空！'
#         else:
#             test_api_rule_manage.test_api_rule_manage().update_test_api_rule(id, ['name', 'description'], [name, description])
#             return render_template("test_api_rule.html", id=id)
# #########################api test rule自动化功能开发结束###############################################
#
#
# #########################api metadata自动化功能开发开始###############################################
# #api功能主页
# @app.route('/test_api_metadata')
# @user.authorize
# def test_api_metadata():
#     return render_template("test_api_metadata.html")
# #api查询
# @app.route('/test_api_metadata.json', methods=['POST', 'GET'])
# @user.authorize
# def search_test_api_metadata():
#     if request.method == 'POST':
#         log.log().logger.info('post')
#     if request.method == 'GET':
#         info = request.values
#         log.log().logger.info('info : %s' %info)
#         limit = info.get('limit', 10)  # 每页显示的条数
#         offset = info.get('offset', 0)  # 分片数，(页码-1)*limit，它表示一段数据的起点
#         log.log().logger.info('get %s' %limit)
#         log.log().logger.info('get  offset %s' %offset)
#
#         id = getInfoAttribute(info, 'id')
#         name = getInfoAttribute(info, 'name')
#         conditionList = ['id','name']
#         valueList = [id,name]
#         fieldlist = []
#         rows = 1000
#         caseList = test_api_metadata_manage.test_api_metadata_manage().show_test_api_metadata(conditionList, valueList, fieldlist, rows)
#         log.log().logger.info(caseList)
#         data = caseList
#         data1 = jsonify({'total': len(data), 'rows': data[int(offset):int(offset) + int(limit)]})
#         log.log().logger.info('data1: %s' %data1)
#         return data1, {'Content-Type': 'application/json'}
# #api新增界面入口与新增成功跳转
# @app.route('/add_test_api_metadata', methods=['POST', 'GET'])
# @user.authorize
# def save_new_test_api_metadata():
#     log.log().logger.info(request)
#     if request.method == 'GET':
#         log.log().logger.info('post')
#         return render_template("new_test_api_metadata.html")
#     if request.method == 'POST':
#         info = request.form
#         log.log().logger.info('info :  %s' %info)
#         index = getInfoAttribute(info, 'index')
#         metadata_id = getInfoAttribute(info, 'metadata_id')
#         name = getInfoAttribute(info, 'name')
#         value = getInfoAttribute(info, 'value')
#         if name == '':
#             return '必填字段不得为空！'
#         else:
#             test_api_metadata_manage.test_api_metadata_manage().new_test_api_metadata(index, metadata_id, name, value)
#             return render_template("test_api_metadata.html")
# #api删除
# @app.route('/delete_test_api_metadata', methods=['POST', 'GET'])
# @user.authorize
# def delete_test_api_metadata():
#     log.log().logger.info(request)
#     if request.method == 'GET':
#         log.log().logger.info('post')
#         info = request.values
#         log.log().logger.info('info : %s' %info)
#         id = getInfoAttribute(info, 'id')
#         log.log().logger.info('id: %s' %id)
#         return render_template("test_api_metadata.html")
#     if request.method == 'POST':
#         info = request.form
#         log.log().logger.info('info : %s' %info)
#         id = getInfoAttribute(info, 'id')
#         act = getInfoAttribute(info, 'act')
#         if act == 'del':
#             test_api_metadata_manage.test_api_metadata_manage().del_test_api_metadata(id)
#             code = 200
#             message = 'delete success!'
#         else:
#             code = 500
#             message = 'act is not del!'
#         result = jsonify({'code': code, 'msg': message})
#         return result, {'Content-Type': 'application/json'}
# #api修改
# @app.route('/edit_test_api_metadata', methods=['POST', 'GET'])
# @user.authorize
# def edit_test_api_metadata():
#     log.log().logger.info(request)
#     if request.method == 'GET':
#         log.log().logger.info('post')
#         info = request.values
#         log.log().logger.info('info :  %s' %info)
#         id = getInfoAttribute(info, 'id')
#         log.log().logger.info('id: %s' %id)
#         return render_template("edit_test_api_metadata.html", id=id)
#     if request.method == 'POST':
#         info = request.form
#         log.log().logger.info('info : %s' %info)
#         id = getInfoAttribute(info, 'id')
#         index = getInfoAttribute(info, 'index')
#         metadata_id = getInfoAttribute(info, 'metadata_id')
#         name = getInfoAttribute(info, 'name')
#         value = getInfoAttribute(info, 'value')
#         if name == '':
#             return '必填字段不得为空！'
#         else:
#             test_api_metadata_manage.test_api_metadata_manage().update_test_api_metadata(id, ['`index`', 'metadata_id', 'name', 'value'], [index, metadata_id, name, value])
#             return render_template("test_api_metadata.html", id=id)
#
# # 复制
# @app.route('/cope_test_api_metadata', methods=['POST', 'GET'])
# @user.authorize
# def cope_test_api_metadata():
#     log.log().logger.info(request)
#     log.log().logger.info(request.method)
#     # log.log().logger.info(request.value)
#     if request.method == 'GET':
#         log.log().logger.info('post')
#         result = jsonify({'code': 500, 'msg': 'should be get!'})
#         return result
#     if request.method == 'POST':
#         info = request.form
#         log.log().logger.info('info :  %s' % info)
#         id = getInfoAttribute(info, 'id')
#         log.log().logger.info('id: %s' % id)
#         if id == '':
#             result = jsonify({'code': 500, 'msg': 'test suite is not found!'})
#         else:
#             # 根据ID复制一条记录
#             copeResult = test_api_metadata_manage.test_api_metadata_manage().show_test_api_metadata(["id"], [id], ['id'], 1)
#             log.log().logger.info(copeResult)
#             index = copeResult[0]["index"]
#             metadata_id = copeResult[0]["metadata_id"]
#             name = copeResult[0]["name"]
#             value = copeResult[0]["value"]
#             test_api_metadata_manage.test_api_metadata_manage().new_test_api_metadata(index, metadata_id, name, value)
#             result = jsonify({'code': 200, 'msg': 'copy success!'})
#         return result
# #########################api metadata自动化功能开发结束###############################################
#
# #########################api metadata type自动化功能开发开始###############################################
# #api功能主页
# @app.route('/test_api_metadata_type')
# @user.authorize
# def test_api_metadata_type():
#     return render_template("test_api_metadata_type.html")
# #api查询
# @app.route('/test_api_metadata_type.json', methods=['POST', 'GET'])
# @user.authorize
# def search_test_api_metadata_type():
#     if request.method == 'POST':
#         log.log().logger.info('post')
#     if request.method == 'GET':
#         info = request.values
#         log.log().logger.info('info : %s' %info)
#         #dataType=json 返回json， 否则返回分页json
#         dataType = getInfoAttribute(info, 'dataType')
#         if dataType=='json':
#             id = getInfoAttribute(info, 'id')
#             name = getInfoAttribute(info, 'name')
#             conditionList = ['id', 'name']
#             valueList = [id, name]
#             fieldlist = []
#             rows = 1000
#             caseList = test_api_metadata_type_manage.test_api_metadata_type_manage().show_test_api_metadata_type(conditionList, valueList, fieldlist, rows)
#             log.log().logger.info(caseList)
#             data = caseList
#             data1 = jsonify({'total': len(data), 'rows': data})
#             log.log().logger.info('data1: %s' %data1)
#
#         else:
#             limit = info.get('limit', 10)  # 每页显示的条数
#             offset = info.get('offset', 0)  # 分片数，(页码-1)*limit，它表示一段数据的起点
#             log.log().logger.info('get %s' %limit)
#             log.log().logger.info('get  offset %s' %offset)
#
#             id = getInfoAttribute(info, 'id')
#             name = getInfoAttribute(info, 'name')
#             conditionList = ['id','name']
#             valueList = [id,name]
#             fieldlist = []
#             rows = 1000
#             caseList = test_api_metadata_type_manage.test_api_metadata_type_manage().show_test_api_metadata_type(conditionList, valueList, fieldlist, rows)
#             log.log().logger.info(caseList)
#             data = caseList
#             data1 = jsonify({'total': len(data), 'rows': data[int(offset):int(offset) + int(limit)]})
#             log.log().logger.info('data1: %s' %data1)
#         return data1, {'Content-Type': 'application/json'}
# #api新增界面入口与新增成功跳转
# @app.route('/add_test_api_metadata_type', methods=['POST', 'GET'])
# @user.authorize
# def save_new_test_api_metadata_type():
#     log.log().logger.info(request)
#     if request.method == 'GET':
#         log.log().logger.info('post')
#         return render_template("new_test_api_metadata_type.html")
#     if request.method == 'POST':
#         info = request.form
#         log.log().logger.info('info :  %s' %info)
#         name = getInfoAttribute(info, 'name')
#         type = getInfoAttribute(info, 'type')
#         description = getInfoAttribute(info, 'description')
#         if name == '':
#             return '必填字段不得为空！'
#         else:
#             test_api_metadata_type_manage.test_api_metadata_type_manage().new_test_api_metadata_type(name, type, description)
#             return render_template("test_api_metadata_type.html")
# #api删除
# @app.route('/delete_test_api_metadata_type', methods=['POST', 'GET'])
# @user.authorize
# def delete_test_api_metadata_type():
#     log.log().logger.info(request)
#     if request.method == 'GET':
#         log.log().logger.info('post')
#         info = request.values
#         log.log().logger.info('info :  %s' %info)
#         id = getInfoAttribute(info, 'id')
#         log.log().logger.info('id: %s' %id)
#         return render_template("test_api_metadata_type.html")
#     if request.method == 'POST':
#         info = request.form
#         log.log().logger.info('info : %s' %info)
#         id = getInfoAttribute(info, 'id')
#         act = getInfoAttribute(info, 'act')
#         if act == 'del':
#             test_api_metadata_type_manage.test_api_metadata_type_manage().del_test_api_metadata_type(id)
#             code = 200
#             message = 'delete success!'
#         else:
#             code = 500
#             message = 'act is not del!'
#         result = jsonify({'code': code, 'msg': message})
#         return result, {'Content-Type': 'application/json'}
# #api修改
# @app.route('/edit_test_api_metadata_type', methods=['POST', 'GET'])
# @user.authorize
# def edit_test_api_metadata_type():
#     log.log().logger.info(request)
#     if request.method == 'GET':
#         log.log().logger.info('post')
#         info = request.values
#         log.log().logger.info('info : %s' %info)
#         id = getInfoAttribute(info, 'id')
#         log.log().logger.info('id: %s' %id)
#         return render_template("edit_test_api_metadata_type.html", id=id)
#     if request.method == 'POST':
#         info = request.form
#         log.log().logger.info('info : %s' %info)
#         id = getInfoAttribute(info, 'id')
#         name = getInfoAttribute(info, 'name')
#         type = getInfoAttribute(info, 'type')
#         description = getInfoAttribute(info, 'description')
#         if name == '':
#             return '必填字段不得为空！'
#         else:
#             test_api_metadata_type_manage.test_api_metadata_type_manage().update_test_api_metadata_type(id, ['name', 'type', 'description'], [name, type, description])
#             return render_template("test_api_metadata_type.html", id=id)
#
#
# #复制
# @app.route('/cope_test_api_metadata_type', methods=['POST', 'GET'])
# @user.authorize
# def cope_test_api_metadata_type():
#     log.log().logger.info(request)
#     log.log().logger.info(request.method)
#     # log.log().logger.info(request.value)
#     if request.method == 'GET':
#         log.log().logger.info('post')
#         result = jsonify({'code': 500, 'msg': 'should be get!'})
#         return result
#     if request.method == 'POST':
#         info = request.form
#         log.log().logger.info('info :  %s' %info)
#         id = getInfoAttribute(info, 'id')
#         log.log().logger.info('id: %s' %id)
#         if id == '':
#             result = jsonify({'code': 500, 'msg': 'test suite is not found!'})
#         else:
#             #根据ID复制一条记录
#             copeResult= test_api_metadata_type_manage.test_api_metadata_type_manage().show_test_api_metadata_type(["id"], [id], ['id'], 1)
#             log.log().logger.info(copeResult)
#             name = copeResult[0]["name"]
#             type = copeResult[0]["type"]
#             description = copeResult[0]["description"]
#             test_api_metadata_type_manage.test_api_metadata_type_manage().new_test_api_metadata_type(name, type, description)
#             result = jsonify({'code': 200, 'msg': 'copy success!'})
#         return result
# #########################api test rule自动化功能开发结束###############################################
#
#
#
# #########################api suit自动化功能开发开始###############################################
# #api功能主页
# @app.route('/test_api_suit')
# @user.authorize
# def test_api_suit():
#     return render_template("test_api_suit.html")
# #api查询
# @app.route('/test_api_suit.json', methods=['POST', 'GET'])
# @user.authorize
# def search_test_api_suit():
#     if request.method == 'POST':
#         log.log().logger.info('post')
#     if request.method == 'GET':
#         info = request.values
#         log.log().logger.info('info : %s' %info)
#         limit = info.get('limit', 10)  # 每页显示的条数
#         offset = info.get('offset', 0)  # 分片数，(页码-1)*limit，它表示一段数据的起点
#         log.log().logger.info('get %s' %limit)
#         log.log().logger.info('get  offset %s' %offset)
#
#         id = getInfoAttribute(info, 'id')
#         name = getInfoAttribute(info, 'name')
#         conditionList = ['id','name']
#         valueList = [id,name]
#         fieldlist = []
#         rows = 1000
#         caseList = test_api_suit_manage.test_api_suit_manage().show_test_api_suit(conditionList, valueList, fieldlist, rows)
#         log.log().logger.info(caseList)
#         data = caseList
#         data1 = jsonify({'total': len(data), 'rows': data[int(offset):int(offset) + int(limit)]})
#         log.log().logger.info('data1: %s' %data1)
#         return data1, {'Content-Type': 'application/json'}
# #api新增界面入口与新增成功跳转
# @app.route('/add_test_api_suit', methods=['POST', 'GET'])
# @user.authorize
# def save_new_test_api_suit():
#     log.log().logger.info(request)
#     if request.method == 'GET':
#         log.log().logger.info('post')
#         return render_template("new_test_api_suit.html")
#     if request.method == 'POST':
#         info = request.form
#         log.log().logger.info('info : %s' %info)
#         name = getInfoAttribute(info, 'name')
#         description = getInfoAttribute(info, 'description')
#         apiUrl = getInfoAttribute(info, 'apiUrl')
#         if name == '':
#             return '必填字段不得为空！'
#         else:
#             test_api_suit_manage.test_api_suit_manage().new_test_api_suit(name, description, '', apiUrl)
#             return render_template("test_api_suit.html")
# #api删除
# @app.route('/delete_test_api_suit', methods=['POST', 'GET'])
# @user.authorize
# def delete_test_api_suit():
#     log.log().logger.info(request)
#     if request.method == 'GET':
#         log.log().logger.info('post')
#         info = request.values
#         log.log().logger.info('info : %s' %info)
#         id = getInfoAttribute(info, 'id')
#         log.log().logger.info('id: %s' %id)
#         return render_template("test_api_suit.html")
#     if request.method == 'POST':
#         info = request.form
#         log.log().logger.info('info : %s' %info)
#         id = getInfoAttribute(info, 'id')
#         act = getInfoAttribute(info, 'act')
#         if act == 'del':
#             test_api_suit_manage.test_api_suit_manage().del_test_api_suit(id)
#             code = 200
#             message = 'delete success!'
#         else:
#             code = 500
#             message = 'act is not del!'
#         result = jsonify({'code': code, 'msg': message})
#         return result, {'Content-Type': 'application/json'}
# #api修改
# @app.route('/edit_test_api_suit', methods=['POST', 'GET'])
# @user.authorize
# def edit_test_api_suit():
#     log.log().logger.info(request)
#     if request.method == 'GET':
#         log.log().logger.info('post')
#         info = request.values
#         log.log().logger.info('info :  %s' %info)
#         id = getInfoAttribute(info, 'id')
#         log.log().logger.info('id: %s' %id)
#         return render_template("edit_test_api_suit.html", id=id)
#     if request.method == 'POST':
#         info = request.form
#         log.log().logger.info('info : %s' %info)
#         id = getInfoAttribute(info, 'id')
#         name = getInfoAttribute(info, 'name')
#         description = getInfoAttribute(info, 'description')
#         if name == '':
#             return '必填字段不得为空！'
#         else:
#             test_api_suit_manage.test_api_suit_manage().update_test_api_suit(id, ['name', 'description'], [name, description])
#             return render_template("test_api_suit.html", id=id)
# #复制
# @app.route('/copy_test_api_suite', methods=['POST', 'GET'])
# @user.authorize
# def copy_test_api_suite():
#     log.log().logger.info(request)
#     log.log().logger.info(request.method)
#     # log.log().logger.info(request.value)
#     if request.method == 'GET':
#         log.log().logger.info('post')
#         result = jsonify({'code': 500, 'msg': 'should be get!'})
#         return result
#     if request.method == 'POST':
#         info = request.form
#         log.log().logger.info('info :  %s' %info)
#         id = getInfoAttribute(info, 'id')
#         log.log().logger.info('id: %s' %id)
#         if id == '':
#             result = jsonify({'code': 500, 'msg': 'test suite is not found!'})
#         else:
#             import random, time
#             #随机获取batchId
#             batchId = str(random.randint(10000, 99999)) + str(time.time())
#             #根据ID复制一条记录
#             test_api_suit_manage.test_api_suit_manage().copy_test_api_suite(id, batchId)
#             #根据batchId，返回记录Id
#             newId = test_api_suit_manage.test_api_suit_manage().show_test_api_suit(["batchId"], [batchId], ['id'], 1)
#             log.log().logger.info('newid %s' %newId)
#             if len(newId):
#                 ext = newId[0]['id']
#                 log.log().logger.info('ext: %s, id :%s'%(ext, id))
#                 if ext != '0':
#                     #根据Id，复制批次并插入批次
#                     test_api_suit_manage.test_api_suit_manage().copy_test_api_batch(ext, id, batchId)
#                 message = 'success！'
#                 code = 200
#                 result = jsonify({'code': 200, 'msg': 'copy success!'})
#             else:
#                 result = jsonify({'code': 500, 'msg': 'test suite is not found!'})
#         return result
# #关联测试主页
# @app.route('/attach_test_api_batch', methods=['POST', 'GET'])
# @user.authorize
# def attach_test_api_batch():
#     log.log().logger.info(request)
#     if request.method == 'GET':
#         log.log().logger.info('post')
#         info = request.values
#         log.log().logger.info('info :  %s' %info)
#         id = getInfoAttribute(info, 'test_suite_id')
#         log.log().logger.info('id: %s' %id)
#         return render_template("attach_test_api_batch.html", id=id)
#     else:
#         return render_template("test_api_suite.html")
#
# # 未关联api
# @app.route('/test_api_no_suit.json', methods=['POST', 'GET'])
# @user.authorize
# def test_api_no_suit():
#     if request.method == 'POST':
#         log.log().logger.info('post')
#     if request.method == 'GET':
#         info = request.values
#         log.log().logger.info('info :  %s' %info)
#         limit = info.get('limit', 10)  # 每页显示的条数
#         offset = info.get('offset', 0)  # 分片数，(页码-1)*limit，它表示一段数据的起点
#         log.log().logger.info('get %s' %limit)
#         log.log().logger.info('get  offset %s' %offset)
#         id = getInfoAttribute(info, 'id')
#         suite_id = getInfoAttribute(info, 'suite_id')
#         name = getInfoAttribute(info, 'name')
#         conditionList = ['id', 'name']
#         valueList = [id, name]
#         fieldlist = []
#         rows = 1000
#         caseList = test_api_suit_manage.test_api_suit_manage().show_test_api_no_suit(conditionList, valueList, fieldlist, rows, suite_id)
#         log.log().logger.info(caseList)
#         data = caseList
#         data1 = jsonify({'total': len(data), 'rows': data[int(offset):int(offset) + int(limit)]})
#         log.log().logger.info('data1: %s' %data1)
#         return data1, {'Content-Type': 'application/json'}
# #新增关联测试
# @app.route('/attach_test_api_batch.json', methods=['POST', 'GET'])
# @user.authorize
# def attach_test_api_batch_to_suite():
#     log.log().logger.info(request)
#     if request.method == 'POST':
#         log.log().logger.info('post')
#         result = jsonify({'code': 500, 'msg': 'post'})
#         return result
#     else:
#         log.log().logger.info(request.values)
#         # log.log().logger.info(request.form)
#         info = request.values
#         test_suite_id = getInfoAttribute(info, 'test_suite_id')
#         moduleVal = getInfoAttribute(info, 'moduleVal')
#         rows = getInfoAttribute(info, 'datarow')
#         log.log().logger.info('test suite id: %s, rows: %s' %(test_suite_id, rows))
#         rows = rows.split(',')
#         log.log().logger.info(rows)
#         idrows = []
#         for i in range(1, len(rows)):
#             idrows.append(rows[i])
#         log.log().logger.info(idrows)
#         # import random, time
#         # batchId = str(random.randint(10000, 99999)) + str(time.time())
#         result0 = test_api_suit_manage.test_api_suit_manage().new_test_api_batch_suit(test_suite_id, idrows, moduleVal)
#         # from apitest import runCase
#         # runCase.runCase()
#         if result0 == 0:
#             result = jsonify({'code': 500, 'msg': 'error, please check selected test cases!'})
#         else:
#             result = jsonify({'code': 200, 'msg': 'message'})
#         return result
# #已关联api主页
# @app.route('/test_api_batch_url', methods=['POST', 'GET'])
# @user.authorize
# def test_api_batch_url():
#     log.log().logger.info(request)
#     if request.method == 'GET':
#         log.log().logger.info('post')
#         info = request.values
#         log.log().logger.info('info :  %s' %info)
#         batch_id = getInfoAttribute(info, 'test_suite_id')
#         log.log().logger.info('batch_id: %s' %batch_id)
#         resultWait=0
#         resultNoPass=0
#         resultPass=0
#         resultPending =0
#         result = test_api_suit_manage.test_api_suit_manage().show_batch_cases_result_group(batch_id=batch_id)
#         log.log().logger.info('result is : %s' %result)
#         for i in range(len(result)):
#             if result[i]['result']==0:
#                 resultWait = int(result[i]['count'])
#             elif result[i]['result']==1:
#                 resultPass = int(result[i]['count'])
#             elif result[i]['result']==2:
#                 resultNoPass = int(result[i]['count'])
#             elif result[i]['result']==3:
#                 resultPending = int(result[i]['count'])
#         log.log().logger.info('%s, %s, %s, %s' %(resultWait,resultNoPass,resultPass,resultPending))
#         resultSum = resultWait+resultNoPass+resultPass+resultPending
#         if resultSum!=0:
#             passRate=str(round(resultPass/resultSum*100,2))+'%'
#         else:
#             passRate=0
#         log.log().logger.info('passRate :  %s' %passRate)
#
#         return render_template("test_api_batch_url.html", batch_id=batch_id,resultPass=resultPass,resultNoPass=resultNoPass,resultPending=resultPending,resultWait=resultWait,resultSum=resultSum,passRate=passRate)
#     else:
#         return render_template("test_api_suite.html")
#
# #查看本批次执行全部用例
# @app.route('/test_api_batch_all', methods=['POST', 'GET'])
# @user.authorize
# def test_api_batch_all():
#     log.log().logger.info(request)
#     if request.method == 'GET':
#         log.log().logger.info('post')
#         info = request.values
#         log.log().logger.info('info :  %s' %info)
#         batch_id = getInfoAttribute(info, 'test_suite_id')
#         log.log().logger.info('batch_id: %s' %batch_id)
#         resultWait=0
#         resultNoPass=0
#         resultPass=0
#         resultPending =0
#         result = test_api_suit_manage.test_api_suit_manage().show_batch_cases_result_group(batch_id=batch_id)
#         log.log().logger.info('result is :', result)
#         for i in range(len(result)):
#             if result[i]['result']==0:
#                 resultWait = int(result[i]['count'])
#             elif result[i]['result']==1:
#                 resultPass = int(result[i]['count'])
#             elif result[i]['result']==2:
#                 resultNoPass = int(result[i]['count'])
#             elif result[i]['result']==3:
#                 resultPending = int(result[i]['count'])
#         log.log().logger.info('%s, %s, %s, %s' %(resultWait,resultNoPass,resultPass,resultPending))
#         resultSum = resultWait+resultNoPass+resultPass+resultPending
#         if resultSum!=0:
#             passRate=str(round(resultPass/resultSum*100,2))+'%'
#         else:
#             passRate=0
#         log.log().logger.info('passRate : %s' %passRate)
#
#         return render_template("test_api_batch_all.html", batch_id=batch_id,resultPass=resultPass,resultNoPass=resultNoPass,resultPending=resultPending,resultWait=resultWait,resultSum=resultSum,passRate=passRate)
#     else:
#         return render_template("test_api_suite.html")
#
# # 查询执行全部用例
# @app.route('/test_api_batch_al.json', methods=['POST', 'GET'])
# @user.authorize
# def search_api_batch_all():
#     if request.method == 'POST':
#         log.log().logger.info('post')
#     if request.method == 'GET':
#         info = request.values
#         log.log().logger.info('info :  %s' %info)
#         limit = info.get('limit', 10)  # 每页显示的条数
#         offset = info.get('offset', 0)  # 分片数，(页码-1)*limit，它表示一段数据的起点
#         log.log().logger.info('get %s' %limit)
#         log.log().logger.info('get  offset %s' %offset)
#         batch_id = getInfoAttribute(info, 'batch_id')
#         result = getInfoAttribute(info, 'result')
#         type = getInfoAttribute(info, 'type')
#
#         conditionList = ['batch_id','result','type']
#         valueList = [batch_id,result,type]
#         fieldlist = []
#         rows = 1000
#         caseList = test_api_suit_manage.test_api_suit_manage().show_api_runhistory_all(conditionList, valueList, fieldlist, rows)
#         log.log().logger.info(caseList)
#         data = caseList
#         data1 = jsonify({'total': len(data), 'rows': data[int(offset):int(offset) + int(limit)]})
#         log.log().logger.info('data1: %s' %data1)
#         return data1, {'Content-Type': 'application/json'}
#
# # 查询已关联url
# @app.route('/test_api_has_suit.json', methods=['POST', 'GET'])
# @user.authorize
# def test_api_has_suit():
#     if request.method == 'POST':
#         log.log().logger.info('post')
#     if request.method == 'GET':
#         info = request.values
#         log.log().logger.info('info :  %s' %info)
#         limit = info.get('limit', 10)  # 每页显示的条数
#         offset = info.get('offset', 0)  # 分片数，(页码-1)*limit，它表示一段数据的起点
#         log.log().logger.info('get limit %s' %limit)
#         log.log().logger.info('get  offset %s' %offset)
#         id = getInfoAttribute(info, 'id')
#         batch_id = getInfoAttribute(info, 'batch_id')
#         name = getInfoAttribute(info, 'name')
#         log.log().logger.info('name %s' %name)
#         conditionList = ['id', 'name']
#         valueList = [id, name]
#         fieldlist = []
#         rows = 1000
#         caseList = test_api_suit_manage.test_api_suit_manage().show_test_api_has_suit(conditionList, valueList, fieldlist, rows, batch_id)
#         log.log().logger.info(caseList)
#         data = caseList
#         data1 = jsonify({'total': len(data), 'rows': data[int(offset):int(offset) + int(limit)]})
#         log.log().logger.info('data1: %s' %data1)
#         return data1, {'Content-Type': 'application/json'}
#
# #查看执行结果主页
# @app.route('/test_api_runhistory', methods=['POST', 'GET'])
# @user.authorize
# def test_api_runhistory():
#     log.log().logger.info(request)
#     if request.method == 'GET':
#         log.log().logger.info('post')
#         info = request.values
#         log.log().logger.info('info :  %s' %info)
#         url_id = getInfoAttribute(info, 'url_id')
#         batch_id = getInfoAttribute(info, 'batch_id')
#         source = getInfoAttribute(info, 'source')
#         if source =='':
#             source = 'batch'
#         log.log().logger.info('url_id :  %s' %url_id)
#         log.log().logger.info('batch_id :  %s' %batch_id)
#         conditionList = ['batch_id', 'url_id']
#         valueList = [batch_id, url_id]
#         fieldlist = []
#         caseList = test_api_suit_manage.test_api_suit_manage().show_batch_url(conditionList, valueList, fieldlist)
#         batch_url_id=caseList[0]["batch_url_id"]
#         log.log().logger.info('batch_url_id : %s' %batch_url_id)
#         # #通过率
#         resultWait=0
#         resultNoPass=0
#         resultPass=0
#         resultPending =0
#         result = test_api_suit_manage.test_api_suit_manage().show_batch_cases_result_group(batch_url_id=batch_url_id)
#         log.log().logger.info('result is : %s' %result)
#         for i in range(len(result)):
#             if result[i]['result']==0:
#                 resultWait = int(result[i]['count'])
#             elif result[i]['result']==1:
#                 resultPass = int(result[i]['count'])
#             elif result[i]['result']==2:
#                 resultNoPass = int(result[i]['count'])
#             elif result[i]['result']==3:
#                 resultPending = int(result[i]['count'])
#         log.log().logger.info('%s, %s ,%s ,%s ' %(resultWait,resultNoPass,resultPass,resultPending))
#         resultSum = resultWait+resultNoPass+resultPass+resultPending
#         if resultSum!=0:
#             passRate=str(round(resultPass/resultSum*100,2))+'%'
#         else:
#             passRate=0
#         log.log().logger.info('passRate :  %s' %passRate)
#         return render_template("test_api_runhistory.html", source = source, batch_id=batch_id,url_id=url_id,batch_url_id=batch_url_id,resultPass=resultPass,resultNoPass=resultNoPass,resultPending=resultPending,resultWait=resultWait,resultSum=resultSum,passRate=passRate)
#     else:
#         return render_template("test_api_suite.html")
# #执行结果
# @app.route('/test_api_runhistory.json', methods=['POST', 'GET'])
# @user.authorize
# def search_test_api_runhistory():
#     if request.method == 'POST':
#         log.log().logger.info('post')
#     if request.method == 'GET':
#         info = request.values
#         log.log().logger.info('info : %s' %info)
#         limit = info.get('limit', 10)  # 每页显示的条数
#         offset = info.get('offset', 0)  # 分片数，(页码-1)*limit，它表示一段数据的起点
#         log.log().logger.info('get %s' %limit)
#         rows = 1000
#         log.log().logger.info('get  offset %s' %offset)
#         id = getInfoAttribute(info, 'id')
#         batch_url_id = getInfoAttribute(info, 'batch_url_id')
#         type = getInfoAttribute(info, 'type')
#         result = getInfoAttribute(info, 'result')
#         conditionList = ['batch_url_id','result','type','id']
#         valueList = [batch_url_id,result,type,id]
#         fieldlist = []
#         caseList = test_api_suit_manage.test_api_suit_manage().show_api_runhistory(conditionList, valueList, fieldlist, rows)
#         log.log().logger.info('caselist: %s' %caseList)
#         data = caseList
#         data1 = jsonify({'total': len(data), 'rows': data[int(offset):int(offset) + int(limit)]})
#         log.log().logger.info('data1: %s' %data1)
#         return data1, {'Content-Type': 'application/json'}
#
# #根据batch_url_id 查询结果
# @app.route('/test_api_batch_url.json', methods=['POST', 'GET'])
# @user.authorize
# def search_test_api_batch_url():
#     if request.method == 'POST':
#         log.log().logger.info('post')
#     if request.method == 'GET':
#         info = request.values
#         log.log().logger.info('info :  %s' %info)
#         limit = info.get('limit', 10)  # 每页显示的条数
#         offset = info.get('offset', 0)  # 分片数，(页码-1)*limit，它表示一段数据的起点
#         log.log().logger.info('get limit %s' %limit)
#         log.log().logger.info('get  offset %s' %offset)
#         batch_id = getInfoAttribute(info, 'batch_id')
#         url_id = getInfoAttribute(info, 'url_id')
#         conditionList = ['batch_id', 'url_id']
#         valueList = [batch_id, url_id]
#         fieldlist = []
#         caseList = test_api_suit_manage.test_api_suit_manage().show_batch_url(conditionList, valueList, fieldlist)
#         log.log().logger.info('caselist: %s' %caseList)
#         data = caseList
#         data1 = jsonify({'total': len(data), 'rows': data[int(offset):int(offset) + int(limit)]})
#         log.log().logger.info('data1: %s' %data1)
#         return data1, {'Content-Type': 'application/json'}
#
# #测试用例详情
# @app.route('/test_api_batch_case_detail')
# @user.authorize
# def test_api_batch_case_detail():
#     info = request.values
#     log.log().logger.info('info : %s' %info)
#     id = getInfoAttribute(info, 'id')
#     batch_id = getInfoAttribute(info, 'batch_id')
#     url_id = getInfoAttribute(info, 'url_id')
#     log.log().logger.info('batch_id : %s' %batch_id)
#     log.log().logger.info('url_id :  %s' %url_id)
#     return render_template("test_api_batch_case_detail.html",id=id,batch_id=batch_id,url_id=url_id)
#
# #测试用例详情
# @app.route('/test_api_case_run')
# @user.authorize
# def test_api_case_run():
#     info = request.values
#     log.log().logger.info('info : %s' %info)
#     id = getInfoAttribute(info, 'id')
#     batch_id = getInfoAttribute(info, 'batch_id')
#     url_id = getInfoAttribute(info, 'url_id')
#     log.log().logger.info('batch_id : %s' %batch_id)
#     log.log().logger.info('url_id :  %s' %url_id)
#     return render_template("test_api_case_run.html",id=id,batch_id=batch_id,url_id=url_id)
#
# #直接测试某个ｕｒｌ
# @app.route('/runurltest.json', methods=['POST', 'GET'])
# @user.authorize
# def runurltest():
#     log.log().logger.info(request)
#     if request.method == 'POST':
#         log.log().logger.info('post')
#         result = jsonify({'code': 500, 'msg': 'should be get!'})
#         return result
#     else:
#         log.log().logger.info(request.values)
#         info = request.values
#         id = getInfoAttribute(info, 'id')
#         apiUrl=getInfoAttribute(info, 'apiUrl')
#         from app.apitest import runCase
#         test_case_id,run_result = runCase.test_url(id,apiUrl)
#         if run_result=='1':
#             result = jsonify({'code': 200,'test_case_id':test_case_id, 'msg': 'success!'})
#         else:
#             result = jsonify({'code': 500, 'msg': 'type is not defined!'})
#         return result
#
#
# #手工测试某个ｕｒｌ
# @app.route('/test_api_single_test.json', methods=['POST', 'GET'])
# @user.authorize
# def test_api_single_test():
#     log.log().logger.info(request)
#     if request.method == 'POST':
#         log.log().logger.info('post')
#         result = jsonify({'code': 500, 'msg': 'should be get!'})
#         return result
#     else:
#         log.log().logger.info(request.values)
#         info = request.values
#         url = getInfoAttribute(info, 'url')
#         context=getInfoAttribute(info, 'context')
#         import json
#         context = json.loads(context)
#         from app.apitest import util
#         # response, content = util.util().send(url+'?'+paraList)
#         response, content = util.util().sendbody(url, context)
#         log.log().logger.info(response)
#         log.log().logger.info(content)
#         result = jsonify({'code': 200, 'rows':[{'response':str(response), 'content': content}]})
#         # print(result)
#         return result
#
#
#
# #重算签名
# @app.route('/test_api_reosign.json', methods=['POST', 'GET'])
# @user.authorize
# def test_api_reosign():
#     log.log().logger.info(request)
#     if request.method == 'POST':
#         log.log().logger.info('post')
#         result = jsonify({'code': 500, 'msg': 'should be get!'})
#         return result
#     else:
#         log.log().logger.info(request.values)
#         info = request.values
#         url_id = getInfoAttribute(info, 'url_id')
#         url = getInfoAttribute(info, 'url')
#         context=getInfoAttribute(info, 'context')
#         import json
#         context = json.loads(context)
#         log.log().logger.info('osign is : %s' %context['osign'])
#         if context['osign']!='':
#             log.log().logger.info('osign is not empty!')
#             from app.apitest import dataBasic,runCase,basicData
#             url, sign, parameters,signMothed = runCase.getUrl(url_id)
#             context['appKey']=basicData.get_appKey(context['appId'])
#             context['osign'] = dataBasic.getOsign(parameters,sign,context,signMothed)
#             del context['appKey']
#             log.log().logger.info(context['osign'])
#             result = jsonify({'code': 200, 'rows': [{'context': str(context)}]})
#         else:
#             log.log().logger.info('osign is empty!')
#             result = jsonify({'code': 500, 'msg': 'osign not defined!'})
#         return result
#
#
# @app.route('/runapitest.json', methods=['POST', 'GET'])
# @user.authorize
# def runapitest():
#     log.log().logger.info(request)
#     if request.method == 'POST':
#         log.log().logger.info('post')
#         result = jsonify({'code': 500, 'msg': 'should be get!'})
#         return result
#     else:
#         log.log().logger.info(request.values)
#         # log.log().logger.info(request.form)
#         info = request.values
#         id = getInfoAttribute(info, 'id')
#         type = getInfoAttribute(info, 'type')
#         runtype = getInfoAttribute(info, 'runtype')
#         if runtype == 'part':
#             runtype = '1'
#         else:
#             runtype = '0'
#         if type == 'test_batch':
#             test_api_suit_manage.test_api_suit_manage().update_api_test_batch_url([], id, runtype)
#             result = jsonify({'code': 200, 'msg': 'success!'})
#         elif type == 'test_case':
#             # test_api_suit_manage.test_api_suit_manage().update_api_test_batch_url([],id,runtype)
#             from app.apitest import runCase
#             runCase.runsingletest(id)
#             result = jsonify({'code': 200, 'msg': 'success!'})
#         else:
#             result = jsonify({'code': 500, 'msg': 'type is not defined!'})
#         return result
#
# #########################api test rule自动化功能开发结束###############################################

# #单元测试列表
# @app.route('/unittest_record.json', methods=['POST', 'GET'])
# @user.authorize
# def test_unittest_result():
#     if request.method == 'POST':
#         log.log().logger.info('post')
#         result = jsonify({'code': 500, 'msg': 'should be get!'})
#         return result
#     else:
#         info = request.values
#         log.log().logger.info('info :  %s' %info)
#         name = getInfoAttribute(info, 'name')
#         limit = info.get('limit', 10)  # 每页显示的条数
#         offset = info.get('offset', 0)  # 分片数，(页码-1)*limit，它表示一段数据的起点
#         data= test_unittest_manage.test_unittest_manage().show_unittest_records(['name'], [name], [], 100)
#         data1 = jsonify({'total': len(data), 'rows': data[int(offset):int(offset) + int(limit)]})
#         log.log().logger.info('data1: %s' %data1)
#         return data1, {'Content-Type': 'application/json'}
#
# # 单元测试详情
# @app.route('/unittest')
# @user.authorize
# def unittest_records():
#     return render_template("unittest_records.html")
#
# # 单元测试详情
# @app.route('/view_unitest_result')
# @user.authorize
# def view_unitest_result():
#     info = request.values
#     log.log().logger.info('info : %s' %info)
#     id = getInfoAttribute(info, 'id')
#     from app import test_unittest_manage
#     data = test_unittest_manage.test_unittest_manage().show_unittest_records(['id'], [id], [], 100)
#     if len(data):
#         filename = data[0]['file_name']
#         return render_template('unittest_detail.html',file_name='/view_unitest_results?id='+id)
#     else:
#         return render_template("unittest_records.html")
#
# # 单元测试详情
# @app.route('/view_unitest_results')
# @user.authorize
# def view_unitest_results():
#     info = request.values
#     log.log().logger.info('info : %s' %info)
#     id = getInfoAttribute(info, 'id')
#     from app import test_unittest_manage
#     data = test_unittest_manage.test_unittest_manage().show_unittest_records(['id'], [id], [], 100)
#     if len(data):
#         filename = data[0]['file_name']
#         return render_template('reports'+'/'+filename)
#     else:
#         return render_template("unittest_records.html")
#
#
# @app.route('/run_unittest.json', methods=['POST', 'GET'])
# @user.authorize
# def run_unittest():
#     log.log().logger.info(request)
#     log.log().logger.info('run unittest')
#     if request.method == 'POST':
#         log.log().logger.info('post')
#         result = jsonify({'code': 500, 'msg': 'should be get!'})
#         return result
#     else:
#         from app.test import test_run_all
#         log.log().logger.info('start run unittest')
#         test_run_all.run_all()
#         result = jsonify({'code': 200, 'msg': 'success!'})
#
#         return result

# # 节点管理
# @app.route('/testhubs')
# @user.authorize
# def testhubs():
#     return render_template("hubs.html")
#
# @app.route('/check_hubs.json', methods=['POST', 'GET'])
# @user.authorize
# def check_hubs():
#     log.log().logger.info(request)
#     log.log().logger.info('check_hubs')
#     if request.method == 'POST':
#         log.log().logger.info('post')
#         result = jsonify({'code': 500, 'msg': 'should be get!'})
#         return result
#     else:
#         from app.core import hubs
#         log.log().logger.info('start checking hubs')
#         hubs.hubs().checkHubs()
#         result = jsonify({'code': 200, 'msg': 'success!'})
#
#         return result
#
# #节点列表
# @app.route('/search_hubs.json', methods=['POST', 'GET'])
# @user.authorize
# def search_hubs():
#     if request.method == 'POST':
#         log.log().logger.info('post')
#         result = jsonify({'code': 500, 'msg': 'should be get!'})
#         return result
#     else:
#         info = request.values
#         log.log().logger.info('info :  %s' %info)
#         # name = getInfoAttribute(info, 'name')
#         limit = info.get('limit', 10)  # 每页显示的条数
#         offset = info.get('offset', 0)  # 分片数，(页码-1)*limit，它表示一段数据的起点
#         from app.core import hubs
#         # data= test_unittest_manage.test_unittest_manage().show_unittest_records(['name'], [name],[],100)
#         data = hubs.hubs().searchHubs()
#         data1 = jsonify({'total': len(data), 'rows': data[int(offset):int(offset) + int(limit)]})
#         log.log().logger.info('data1: %s' %data1)
#         return data1, {'Content-Type': 'application/json'}
#
# # 单元测试详情
# @app.route('/view_hub')
# @user.authorize
# def view_hub():
#     return render_template('view_hub.html')


# #########################脚本管理功能开发开始###############################################
# # 脚本功能主页
# @app.route('/test_file')
# @user.authorize
# def test_file():
#     return render_template("test_file.html")
#
# # api查询
# @app.route('/search_test_file.json', methods=['POST', 'GET'])
# @user.authorize
# def search_test_file():
#     if request.method == 'POST':
#         log.log().logger.info('post')
#     if request.method == 'GET':
#         info = request.values
#         log.log().logger.info('info : %s' %info)
#         # dataType=json 返回json， 否则返回分页json
#         dataType = getInfoAttribute(info, 'dataType')
#         limit = info.get('limit', 10)  # 每页显示的条数
#         offset = info.get('offset', 0)  # 分片数，(页码-1)*limit，它表示一段数据的起点
#         log.log().logger.info('get %s' %limit)
#         log.log().logger.info('get  offset %s' %offset)
#         id = getInfoAttribute(info, 'id')
#         name = getInfoAttribute(info, 'name')
#         conditionList = ['id', 'name']
#         valueList = [id, name]
#         fieldlist = []
#         rows = 1000
#         caseList = test_file_manage.test_file_mange().show_test_file(
#             conditionList, valueList, fieldlist, rows)
#         log.log().logger.info(caseList)
#         data = caseList
#         data1 = jsonify({'total': len(data), 'rows': data[int(offset):int(offset) + int(limit)]})
#         log.log().logger.info('data1: %s' %data1)
#         return data1, {'Content-Type': 'application/json'}
#
# # api新增界面入口与新增成功跳转
# @app.route('/add_test_file', methods=['POST', 'GET'])
# @user.authorize
# def add_test_file():
#     from app import config
#     import os
#     from werkzeug import secure_filename
#     import time
#     log.log().logger.info(request)
#     if request.method == 'GET':
#         log.log().logger.info('post')
#         return render_template("new_test_file.html")
#     if request.method == 'POST':
#         info = request.form
#         log.log().logger.info('info :  %s' %info)
#         name = getInfoAttribute(info, 'name')
#         description = getInfoAttribute(info, 'description')
#         if name == '':
#             return '必填字段不得为空！'
#         else:
#             f = request.files['myfile']  # 从表单的file字段获取文件，myfile为该表单的name值
#             fname = secure_filename(f.filename)
#             fname = str(int(time.time())) + fname
#             log.log().logger.info (fname)
#             if not (fname==''):
#                 import platform
#                 if platform.system()=='Windows':
#                     # 文件上传路径
#                     dirPath = config.uploadFilePathWin
#                 else:
#                     dirPath = config.uploadFilePathLinux
#                 f.save(os.path.join(dirPath, fname))  # 保存文件到upload目录
#             #保存数据到数据库
#             test_file_manage.test_file_mange().new_test_file(name, fname, description)
#             return render_template("test_file.html")
#
# # api删除
# @app.route('/delete_test_file', methods=['POST', 'GET'])
# @user.authorize
# def delete_test_file():
#     log.log().logger.info(request)
#     if request.method == 'GET':
#         log.log().logger.info('post')
#         info = request.values
#         log.log().logger.info('info : %s' %info)
#         id = getInfoAttribute(info, 'id')
#         log.log().logger.info('id: %s' %id)
#         return render_template("test_file.html")
#     if request.method == 'POST':
#         info = request.form
#         log.log().logger.info('info :  %s' %info)
#         id = getInfoAttribute(info, 'id')
#         filePath=getInfoAttribute(info, 'filePath')
#         log.log().logger.info('filePath :  %s' %filePath)
#         act = getInfoAttribute(info, 'act')
#         if act == 'del':
#             test_file_manage.test_file_mange().del_test_file(id)
#             code = 200
#             message = 'delete success!'
#         else:
#             code = 500
#             message = 'act is not del!'
#         result = jsonify({'code': code, 'msg': message})
#         return result, {'Content-Type': 'application/json'}
#
# # api修改
# @app.route('/edit_test_file', methods=['POST', 'GET'])
# @user.authorize
# def edit_test_file():
#     from app import config
#     import os
#     from werkzeug import secure_filename
#     import time
#     log.log().logger.info(request)
#     if request.method == 'GET':
#         log.log().logger.info('post')
#         info = request.values
#         log.log().logger.info('info :  %s' %info)
#         id = getInfoAttribute(info, 'id')
#         log.log().logger.info('id: %s' %id)
#         return render_template("edit_test_file.html", id=id)
#     if request.method == 'POST':
#         info = request.form
#         log.log().logger.info('info : %s' %info)
#         id = getInfoAttribute(info, 'id')
#         name = getInfoAttribute(info, 'name')
#         description = getInfoAttribute(info, 'description')
#         if name == '':
#             return '必填字段不得为空！'
#         else:
#             f = request.files['myfile']  # 从表单的file字段获取文件，myfile为该表单的name值
#             fname = secure_filename(f.filename)
#             fname = str(int(time.time())) + fname
#             log.log().logger.info (fname)
#             if not (fname==''):
#                 import platform
#                 if platform.system()=='Windows':
#                     # 文件上传路径
#                     dirPath = config.uploadFilePathWin
#                 else:
#                     dirPath = config.uploadFilePathLinux
#                 f.save(os.path.join(dirPath, fname))  # 保存文件到upload目录
#             test_file_manage.test_file_mange().update_test_file(id, ['name', 'fileName', 'description'], [name, fname, description])
#             return render_template("test_file.html", id=id)
#
# #run_test_file
# # 执行脚本
# @app.route('/run_test_file', methods=['POST', 'GET'])
# @user.authorize
# def run_test_file():
#     if request.method == 'Get':
#         log.log().logger.info('Get')
#         result = jsonify({'code': 500, 'msg': 'should be post!'})
#         return result
#     else:
#         info = request.values
#         log.log().logger.info('info :  %s' %info)
#         id = getInfoAttribute(info,'id')
#         result="0"
#         try:
#             test_file_manage.test_file_mange().stop_test_file()
#             test_file_manage.test_file_mange().update_test_file(id, ['runStatus'], [1])
#             result = "1"
#         except:
#             result = "0"
#         return result
#
# #下载服务器文件
# @app.route('/load_test_file', methods=['POST', 'GET'])
# @user.authorize
# def load_test_file():
#     from flask import make_response, send_file
#     info = request.values
#     log.log().logger.info('info :  %s' %info)
#     fileName = getInfoAttribute(info, 'filePath')
#     import platform
#     if platform.system() == 'Windows':
#         # 文件上传路径
#         dirPath = config.uploadFilePathWin
#     else:
#         dirPath = config.uploadFilePathLinux
#     filePath = dirPath+fileName
#     #获取服务器文件
#     response = make_response(send_file(filePath))
#     #获取文件名
#     filelist = filePath.split("\\")
#     fileName=filelist[len(filelist)-1]
#     log.log().logger.info('fileName :  %s' %fileName)
#     response.headers["Content-Disposition"] = "attachment; filename="+fileName+";"
#     return response
#
# @app.route('/rerun_locust')
# @user.authorize
# def rerun_locust():
#     log.log().logger.info(request)
#     import os
#     os.system('/opt/flask/flask/rerun_locust.sh')
#     return render_template("test_file.html")
# #########################脚本管理功能开发结束###############################################


#
# #检查登录信息是否正确
# @app.route('/getDevicesList.json', methods=['POST', 'GET'])
# def getDevicesList():
#     #获取列表
#     from app.core import hubs
#     list=hubs.hubs().getDevicesList()
#     log.log().logger.info('list %s' %list)
#     result = jsonify({'msg': list})
#     return result, {'Content-Type': 'application/json'}
#

