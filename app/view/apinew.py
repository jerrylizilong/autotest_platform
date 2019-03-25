from flask import Blueprint,render_template, jsonify, request,redirect
from app import log
from app.view import viewutil,user
from app.api_new import api_manage
from app.db import test_api_new_manange

mod = Blueprint('apinew', __name__,
                        template_folder='templates')


#########################api自动化功能开发开始###############################################
#api功能主页
@mod.route('/test_api_new')
@user.authorize
def test_api():
    return render_template("apinew/test_api_new.html")

#api查询
@mod.route('/test_api_new.json', methods=['POST', 'GET'])
@user.authorize
def search_test_api():
    if request.method == 'POST':
        log.log().logger.info('post')
    if request.method == 'GET':
        info = request.values
        log.log().logger.info('info : %s' %info)
        limit = info.get('limit', 10)  # 每页显示的条数
        offset = info.get('offset', 0)  # 分片数，(页码-1)*limit，它表示一段数据的起点
        log.log().logger.info('get %s' %limit)
        log.log().logger.info('get  offset %s' %offset)

        type = viewutil.getInfoAttribute(info, 'type')
        id = viewutil.getInfoAttribute(info, 'id')
        name = viewutil.getInfoAttribute(info, 'name')
        product = viewutil.getInfoAttribute(info, 'product')
        module = viewutil.getInfoAttribute(info, 'module')
        conditionList = ['id','name','product','module']
        valueList = [id,name,product,module]
        fieldlist = []
        rows = 1000
        caseList = test_api_new_manange.test_api_new_manange().show_test_api(conditionList, valueList, fieldlist, rows,type=type)
        log.log().logger.info(caseList)
        data = caseList
        data1 = jsonify({'total': len(data), 'rows': data[int(offset):int(offset) + int(limit)]})
        log.log().logger.info('data1: %s' %data1)
        return data1, {'Content-Type': 'application/json'}
#api新增界面入口与新增成功跳转
@mod.route('/add_test_api_new', methods=['GET'])
@user.authorize
def new_test_api():
    log.log().logger.info(request)
    if request.method == 'GET':
        log.log().logger.info('post')
        return render_template("apinew/new_test_api.html")

#api新增界面入口与新增成功跳转
@mod.route('/add_test_api_new.json', methods=['POST'])
@user.authorize
def save_new_test_api():
    log.log().logger.info(request)
    if request.method == 'POST':
        info = request.form
        log.log().logger.info('info :  %s' %info)
        name = viewutil.getInfoAttribute(info, 'name')
        description = viewutil.getInfoAttribute(info, 'description')
        module = viewutil.getInfoAttribute(info, 'module')
        product = viewutil.getInfoAttribute(info, 'product')
        url = viewutil.getInfoAttribute(info, 'url')
        paras = viewutil.getInfoAttribute(info, 'paras')
        osign_list = viewutil.getInfoAttribute(info, 'osign_list')
        osign_list=osign_list.replace('[','').replace(']','').replace("'",'').replace(" ",'')
        result = test_api_new_manange.test_api_new_manange().new_test_api(product,module,name,url,paras,osign_list,description)
        if result:
            code = 200
            message = 'success'
        else:
            code = 500
            message = 'failed'
        data1 = jsonify({'code': code, 'msg': message})
        log.log().logger.info('data1: %s' % data1)
        return data1, {'Content-Type': 'application/json'}


@mod.route('/split_test_api_url.json', methods=['POST', 'GET'])
@user.authorize
def split_test_api_url():
    if request.method == 'POST':
        log.log().logger.info('post')
    if request.method == 'GET':
        info = request.values
        log.log().logger.info('info : %s' % info)

        url = viewutil.getInfoAttribute(info, 'url')
        api_info = api_manage.api_manage().split_api_info(url)
        data1 = jsonify(api_info)
        log.log().logger.info('data1: %s' % data1)
        return data1, {'Content-Type': 'application/json'}

#api删除s
@mod.route('/delete_test_api_new', methods=['POST', 'GET'])
@user.authorize
def delete_test_api():
    log.log().logger.info(request)
    if request.method == 'GET':
        log.log().logger.info('post')
        info = request.values
        log.log().logger.info('info :  %s' %info)
        id = viewutil.getInfoAttribute(info, 'id')
        log.log().logger.info('id: %s' %id)
        return render_template("apinew/test_api_new.html")
    if request.method == 'POST':
        info = request.form
        log.log().logger.info('info :  %s' %info)
        id = viewutil.getInfoAttribute(info, 'id')
        result = test_api_new_manange.test_api_new_manange().del_test_api(id)
        if result:
            code = 200
            message = 'delete success!'
        else:
            code = 500
            message = 'please try again!'
        result = jsonify({'code': code, 'msg': message})
        return result, {'Content-Type': 'application/json'}
#api修改页面入口
@mod.route('/edit_test_api_new', methods=['POST', 'GET'])
@user.authorize
def edit_test_api():
    log.log().logger.info(request)
    if request.method == 'GET':
        log.log().logger.info('post')
        info = request.values
        log.log().logger.info('info :  %s' %info)
        id = viewutil.getInfoAttribute(info, 'id')
        log.log().logger.info('id: %s' %id)
        return render_template("apinew/edit_test_api.html", id=id)

#api 修改保存
@mod.route('/update_test_api_new.json', methods=['POST'])
@user.authorize
def update_test_api_new():
    log.log().logger.info(request)
    if request.method == 'POST':
        info = request.form
        log.log().logger.info('info :  %s' %info)
        id = viewutil.getInfoAttribute(info, 'id')
        name = viewutil.getInfoAttribute(info, 'name')
        description = viewutil.getInfoAttribute(info, 'description')
        module = viewutil.getInfoAttribute(info, 'module')
        product = viewutil.getInfoAttribute(info, 'product')
        url = viewutil.getInfoAttribute(info, 'url')
        paras = viewutil.getInfoAttribute(info, 'paras')
        osign_list = viewutil.getInfoAttribute(info, 'osign_list')
        result = test_api_new_manange.test_api_new_manange().update_test_api(id,fieldlist=['product','module','name','url','paras','osign_list','description'] ,valueList=[product,module,name,url,paras,osign_list,description])
        if result:
            data1 = jsonify({'code':200})
        else:
            data1 = jsonify({'code':500})
        log.log().logger.info('data1: %s' % data1)
        return data1, {'Content-Type': 'application/json'}



# 手工测试某个ｕｒｌ  页面
@mod.route('/test_api_new_test', methods=['GET'])
@user.authorize
def test_api_single_test_page():
    log.log().logger.info(request)
    if request.method == 'GET':
        log.log().logger.info(request.values)
        info = request.values
        id = viewutil.getInfoAttribute(info, 'id')
        return render_template('apinew/test_api_case_new_run.html',id=id)

# 手工测试某个ｕｒｌ
@mod.route('/test_api_new_run.json', methods=['POST'])
@user.authorize
def test_api_single_test():
    log.log().logger.info(request)
    if request.method == 'POST':
        log.log().logger.info(request.values)
        info = request.values
        url = viewutil.getInfoAttribute(info, 'url')
        import json
        from app.api_new import api_manage
        response, content = api_manage.api_manage().sendRequest(url)
        log.log().logger.info(response)
        log.log().logger.info(content)
        result = jsonify({'code': 200, 'rows': [{'response': str(response), 'content': content}]})
        return result


#重算签名
@mod.route('/test_api_reosign_new.json', methods=['POST', 'GET'])
@user.authorize
def test_api_reosign():
    log.log().logger.info(request)
    if request.method == 'POST':
        log.log().logger.info('post')
        result = jsonify({'code': 500, 'msg': 'should be get!'})
        return result
    else:
        log.log().logger.info(request.values)
        info = request.values
        osign_list = viewutil.getInfoAttribute(info, 'osign_list').split(',')
        context=viewutil.getInfoAttribute(info, 'context')
        import json
        context = json.loads(context)
        # print(type(context))
        # print(context['appId'])
          # print(osign,context)
        log.log().logger.info('context is : %s' %context)
        print(len(osign_list),osign_list,'osign info')
        if len(osign_list)>1:
            log.log().logger.info('osign is not empty!')
            from app.api_new import api_manage
            appKey='abc'
            context= api_manage.api_manage().api_osign(osign_list=osign_list,para_info=context,appkey=appKey)
            log.log().logger.info(context['osign'])
            result = jsonify({'code': 200, 'rows': [{'context': str(context)}]})
        else:
            log.log().logger.info('osign list is empty!')
            result = jsonify({'code': 200, 'rows': [{'context': str(context)}]})
        return result



#api查询url
@mod.route('/test_api_host.json', methods=['GET'])
@user.authorize
def search_test_api_host_manage():
    if request.method == 'GET':
        info = request.values
        log.log().logger.info('info : %s' %info)
        type = viewutil.getInfoAttribute(info, 'type')
        from app.api_new import paras
        hostList = paras.paraValues().Hosts
        data1 = jsonify({'total': len(hostList), 'rows': hostList})
        log.log().logger.info('data1: %s' %data1)
        return data1, {'Content-Type': 'application/json'}


# #########################api suit自动化功能开发开始###############################################
# #api功能主页
# @mod.route('/test_api_new_suit')
# @user.authorize
# def test_api_suit():
#     return render_template("apinew/test_api_new_suit.html")
# #api查询
# @mod.route('/test_api_new_suit.json', methods=['POST', 'GET'])
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
#         id = viewutil.getInfoAttribute(info, 'id')
#         name = viewutil.getInfoAttribute(info, 'name')
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
# @mod.route('/add_test_api_suit', methods=['POST', 'GET'])
# @user.authorize
# def save_new_test_api_suit():
#     log.log().logger.info(request)
#     if request.method == 'GET':
#         log.log().logger.info('post')
#         return render_template("apinew/new_test_api_suit.html")
#     if request.method == 'POST':
#         info = request.form
#         log.log().logger.info('info : %s' %info)
#         name = viewutil.getInfoAttribute(info, 'name')
#         description = viewutil.getInfoAttribute(info, 'description')
#         apiUrl = viewutil.getInfoAttribute(info, 'apiUrl')
#         if name == '':
#             return '必填字段不得为空！'
#         else:
#             test_api_suit_manage.test_api_suit_manage().new_test_api_suit(name, description, '', apiUrl)
#             return render_template("apinew/test_api_new_suit.html")
# #api删除
# @mod.route('/delete_test_api_suit', methods=['POST', 'GET'])
# @user.authorize
# def delete_test_api_suit():
#     log.log().logger.info(request)
#     if request.method == 'GET':
#         log.log().logger.info('post')
#         info = request.values
#         log.log().logger.info('info : %s' %info)
#         id = viewutil.getInfoAttribute(info, 'id')
#         log.log().logger.info('id: %s' %id)
#         return render_template("apinew/test_api_new_suit.html")
#     if request.method == 'POST':
#         info = request.form
#         log.log().logger.info('info : %s' %info)
#         id = viewutil.getInfoAttribute(info, 'id')
#         act = viewutil.getInfoAttribute(info, 'act')
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
# @mod.route('/edit_test_api_suit', methods=['POST', 'GET'])
# @user.authorize
# def edit_test_api_suit():
#     log.log().logger.info(request)
#     if request.method == 'GET':
#         log.log().logger.info('post')
#         info = request.values
#         log.log().logger.info('info :  %s' %info)
#         id = viewutil.getInfoAttribute(info, 'id')
#         log.log().logger.info('id: %s' %id)
#         return render_template("apinew/edit_test_api_suit.html", id=id)
#     if request.method == 'POST':
#         info = request.form
#         log.log().logger.info('info : %s' %info)
#         id = viewutil.getInfoAttribute(info, 'id')
#         name = viewutil.getInfoAttribute(info, 'name')
#         description = viewutil.getInfoAttribute(info, 'description')
#         if name == '':
#             return '必填字段不得为空！'
#         else:
#             test_api_suit_manage.test_api_suit_manage().update_test_api_suit(id, ['name', 'description'], [name, description])
#             return render_template("apinew/test_api_new_suit.html", id=id)
# #复制
# @mod.route('/copy_test_api_suite', methods=['POST', 'GET'])
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
#         id = viewutil.getInfoAttribute(info, 'id')
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
# @mod.route('/attach_test_api_batch', methods=['POST', 'GET'])
# @user.authorize
# def attach_test_api_batch():
#     log.log().logger.info(request)
#     if request.method == 'GET':
#         log.log().logger.info('post')
#         info = request.values
#         log.log().logger.info('info :  %s' %info)
#         id = viewutil.getInfoAttribute(info, 'test_suite_id')
#         log.log().logger.info('id: %s' %id)
#         return render_template("apinew/attach_test_api_batch.html", id=id)
#     else:
#         return render_template("apinew/test_api_new_suite.html")
#
# # 未关联api
# @mod.route('/test_api_new_no_suit.json', methods=['POST', 'GET'])
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
#         id = viewutil.getInfoAttribute(info, 'id')
#         suite_id = viewutil.getInfoAttribute(info, 'suite_id')
#         name = viewutil.getInfoAttribute(info, 'name')
#         module = viewutil.getInfoAttribute(info, 'module')
#         conditionList = ['id', 'name','module']
#         valueList = [id, name,module]
#         fieldlist = []
#         rows = 1000
#         caseList = test_api_suit_manage.test_api_suit_manage().show_test_api_no_suit(conditionList, valueList, fieldlist, rows, suite_id)
#         log.log().logger.info(caseList)
#         data = caseList
#         data1 = jsonify({'total': len(data), 'rows': data[int(offset):int(offset) + int(limit)]})
#         log.log().logger.info('data1: %s' %data1)
#         return data1, {'Content-Type': 'application/json'}
# #新增关联测试
# @mod.route('/attach_test_api_batch.json', methods=['POST', 'GET'])
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
#         test_suite_id = viewutil.getInfoAttribute(info, 'test_suite_id')
#         moduleVal = viewutil.getInfoAttribute(info, 'moduleVal')
#         rows = viewutil.getInfoAttribute(info, 'datarow')
#         log.log().logger.info('test suite id: %s, rows: %s' %(test_suite_id, rows))
#         rows = rows.split(',')
#         log.log().logger.info(rows)
#         idrows = []
#         for i in range(1, len(rows)):
#             idrows.append(rows[i])
#         log.log().logger.info(idrows)
#         result0 = test_api_suit_manage.test_api_suit_manage().new_test_api_batch_suit(test_suite_id, idrows, moduleVal)
#         if result0 == 0:
#             result = jsonify({'code': 500, 'msg': 'error, please check selected test cases!'})
#         else:
#             result = jsonify({'code': 200, 'msg': 'message'})
#         return result
# #已关联api主页
# @mod.route('/test_api_new_batch_url', methods=['POST', 'GET'])
# @user.authorize
# def test_api_batch_url():
#     log.log().logger.info(request)
#     if request.method == 'GET':
#         import pyecharts
#         REMOTE_HOST = "https://pyecharts.github.io/assets/js"
#         bar = pyecharts.Pie()
#         bar.width = 700
#         bar.height = 400
#         log.log().logger.info('post')
#         info = request.values
#         log.log().logger.info('info :  %s' %info)
#         batch_id = viewutil.getInfoAttribute(info, 'test_suite_id')
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
#         bar.add("results", ['失败','待执行','执行完成','成功'], [resultNoPass,resultWait,resultPending,resultPass],
#                 is_more_utils=True,is_area_show=True,is_label_show=True,legend_pos="50%")
#         return render_template("apinew/test_api_new_batch_url.html", batch_id=batch_id,resultPass=resultPass,resultNoPass=resultNoPass,resultPending=resultPending,resultWait=resultWait,resultSum=resultSum,passRate=passRate,myechart=bar.render_embed(),host=REMOTE_HOST,script_list=bar.get_js_dependencies())
#     else:
#         return render_template("apinew/test_api_new_suite.html")
#
# #查看本批次执行全部用例
# @mod.route('/test_api_new_batch_all', methods=['POST', 'GET'])
# @user.authorize
# def test_api_batch_all():
#     log.log().logger.info(request)
#     if request.method == 'GET':
#         import pyecharts
#         REMOTE_HOST = "https://pyecharts.github.io/assets/js"
#         bar = pyecharts.Pie()
#         bar.width = 700
#         bar.height = 400
#         log.log().logger.info('post')
#         info = request.values
#         log.log().logger.info('info :  %s' %info)
#         batch_id = viewutil.getInfoAttribute(info, 'test_suite_id')
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
#         bar.add("results", ['失败','待执行','执行完成','成功'], [resultNoPass,resultWait,resultPending,resultPass],
#                 is_more_utils=True,is_area_show=True,is_label_show=True,legend_pos="50%")
#         return render_template("apinew/test_api_new_batch_all.html", batch_id=batch_id,resultPass=resultPass,resultNoPass=resultNoPass,resultPending=resultPending,resultWait=resultWait,resultSum=resultSum,passRate=passRate,myechart=bar.render_embed(),host=REMOTE_HOST,script_list=bar.get_js_dependencies())
#     else:
#         return render_template("apinew/test_api_new_suite.html")
#
# # 查询执行全部用例
# @mod.route('/test_api_new_batch_al.json', methods=['POST', 'GET'])
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
#         batch_id = viewutil.getInfoAttribute(info, 'batch_id')
#         result = viewutil.getInfoAttribute(info, 'result')
#         type = viewutil.getInfoAttribute(info, 'type')
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
# @mod.route('/test_api_new_has_suit.json', methods=['POST', 'GET'])
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
#         id = viewutil.getInfoAttribute(info, 'id')
#         batch_id = viewutil.getInfoAttribute(info, 'batch_id')
#         name = viewutil.getInfoAttribute(info, 'name')
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
# @mod.route('/test_api_new_runhistory', methods=['POST', 'GET'])
# @user.authorize
# def test_api_runhistory():
#     log.log().logger.info(request)
#     if request.method == 'GET':
#         log.log().logger.info('post')
#         info = request.values
#         log.log().logger.info('info :  %s' %info)
#         url_id = viewutil.getInfoAttribute(info, 'url_id')
#         batch_id = viewutil.getInfoAttribute(info, 'batch_id')
#         source = viewutil.getInfoAttribute(info, 'source')
#         if source =='':
#             source = 'batch'
#         import pyecharts
#         REMOTE_HOST = "https://pyecharts.github.io/assets/js"
#         bar = pyecharts.Pie()
#         bar.width = 700
#         bar.height = 400
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
#         bar.add("results", ['失败', '待执行', '执行完成', '成功'], [resultNoPass, resultWait, resultPending, resultPass],
#                 is_more_utils=True, is_area_show=True, is_label_show=True, legend_pos="50%")
#         return render_template("apinew/test_api_new_runhistory.html", source = source, batch_id=batch_id,url_id=url_id,batch_url_id=batch_url_id,resultPass=resultPass,resultNoPass=resultNoPass,resultPending=resultPending,resultWait=resultWait,resultSum=resultSum,passRate=passRate,myechart=bar.render_embed(),host=REMOTE_HOST,script_list=bar.get_js_dependencies())
#     else:
#         return render_template("apinew/test_api_new_suite.html")
# #执行结果
# @mod.route('/test_api_new_runhistory.json', methods=['POST', 'GET'])
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
#         id = viewutil.getInfoAttribute(info, 'id')
#         batch_url_id = viewutil.getInfoAttribute(info, 'batch_url_id')
#         type = viewutil.getInfoAttribute(info, 'type')
#         result = viewutil.getInfoAttribute(info, 'result')
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
# @mod.route('/test_api_new_batch_url.json', methods=['POST', 'GET'])
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
#         batch_id = viewutil.getInfoAttribute(info, 'batch_id')
#         url_id = viewutil.getInfoAttribute(info, 'url_id')
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
# @mod.route('/test_api_new_batch_case_detail')
# @user.authorize
# def test_api_batch_case_detail():
#     info = request.values
#     log.log().logger.info('info : %s' %info)
#     id = viewutil.getInfoAttribute(info, 'id')
#     batch_id = viewutil.getInfoAttribute(info, 'batch_id')
#     url_id = viewutil.getInfoAttribute(info, 'url_id')
#     log.log().logger.info('batch_id : %s' %batch_id)
#     log.log().logger.info('url_id :  %s' %url_id)
#     return render_template("apinew/test_api_new_batch_case_detail.html",id=id,batch_id=batch_id,url_id=url_id)
#
# #测试用例详情
# @mod.route('/test_api_new_case_run')
# @user.authorize
# def test_api_case_run():
#     info = request.values
#     log.log().logger.info('info : %s' %info)
#     id = viewutil.getInfoAttribute(info, 'id')
#     batch_id = viewutil.getInfoAttribute(info, 'batch_id')
#     url_id = viewutil.getInfoAttribute(info, 'url_id')
#     log.log().logger.info('batch_id : %s' %batch_id)
#     log.log().logger.info('url_id :  %s' %url_id)
#     return render_template("apinew/test_api_new_case_run.html",id=id,batch_id=batch_id,url_id=url_id)
#
# #直接测试某个ｕｒｌ
# @mod.route('/runurltest.json', methods=['POST', 'GET'])
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
#         id = viewutil.getInfoAttribute(info, 'id')
#         apiUrl=viewutil.getInfoAttribute(info, 'apiUrl')
#         from app.apinew import run_case
#         test_case_id,run_result = run_case.test_url_from_admin(id, apiUrl)
#         if run_result=='1':
#             result = jsonify({'code': 200,'test_case_id':test_case_id, 'msg': 'success!'})
#         else:
#             result = jsonify({'code': 500, 'msg': 'type is not defined!'})
#         return result
#
#
# #手工测试某个ｕｒｌ
# @mod.route('/test_api_new_single_test1.json', methods=['POST', 'GET'])
# @user.authorize
# def test_api_single_test1():
#     log.log().logger.info(request)
#     if request.method == 'POST':
#         log.log().logger.info('post')
#         result = jsonify({'code': 500, 'msg': 'should be get!'})
#         return result
#     else:
#         log.log().logger.info(request.values)
#         info = request.values
#         url = viewutil.getInfoAttribute(info, 'url')
#         from app.apinew import util
#         response, content = util.util().send(url)
#         log.log().logger.info(response)
#         log.log().logger.info(content)
#         result = jsonify({'code': 200, 'rows':[{'response':str(response), 'content': content}]})
#         return result

#
# @mod.route('/runapinew.json', methods=['POST', 'GET'])
# @user.authorize
# def runapinew():
#     log.log().logger.info(request)
#     if request.method == 'POST':
#         log.log().logger.info('post')
#         result = jsonify({'code': 500, 'msg': 'should be get!'})
#         return result
#     else:
#         log.log().logger.info(request.values)
#         # log.log().logger.info(request.form)
#         info = request.values
#         id = viewutil.getInfoAttribute(info, 'id')
#         type = viewutil.getInfoAttribute(info, 'type')
#         runtype = viewutil.getInfoAttribute(info, 'runtype')
#         if runtype == 'part':
#             runtype = '1'
#         else:
#             runtype = '0'
#         if type == 'test_batch':
#             test_api_suit_manage.test_api_suit_manage().update_api_test_batch_url([], id, runtype)
#             result = jsonify({'code': 200, 'msg': 'success!'})
#         elif type == 'test_case':
#             # test_api_suit_manage.test_api_suit_manage().update_api_test_batch_url([],id,runtype)
#             from app.apinew import run_case
#             run_case.run_single_test(id)
#             result = jsonify({'code': 200, 'msg': 'success!'})
#         else:
#             result = jsonify({'code': 500, 'msg': 'type is not defined!'})
#         return result
#
#
#
# #刷新前置数据
# @mod.route('/test_api_new_refresh_prepose.json', methods=['POST', 'GET'])
# @user.authorize
# def test_api_refresh_prepose():
#     log.log().logger.info(request)
#     if request.method == 'POST':
#         log.log().logger.info('post')
#         result = jsonify({'code': 500, 'msg': 'should be get!'})
#         return result
#     else:
#         log.log().logger.info(request.values)
#         info = request.values
#         url_id = viewutil.getInfoAttribute(info, 'url_id')
#         batch_id = viewutil.getInfoAttribute(info, 'batch_id')
#         apiUrl=viewutil.getInfoAttribute(info, 'url')
#         # id = viewutil.getInfoAttribute(info, 'id')
#         from app.apinew import run_case
#         api_prepose.update_prepose(batch_id=batch_id, current_id=url_id, url=apiUrl)
#         run_case.test_url_from_admin(url_id, apiUrl)
#         result = jsonify({'code': 200})
#         return result