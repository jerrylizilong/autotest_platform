from flask import Blueprint,render_template, jsonify, request,session
from app import log
from app.view import viewutil,user
from app.db import test_unittest_manage

mod = Blueprint('unittest', __name__,
                        template_folder='templates')

#
# @mod.route('/')
# @mod.route('/index')
# @user.authorize
# def index():
#     list = session.get('user', None)
#     username = list[0]["username"]
#     return render_template("util/index.html", message='Hello, %s' % username)
#
# @mod.route('/test')
# def index1():
#     user = { 'nickname': 'Miguel' } # fake user
#     return render_template("util/500.html")
#
# @mod.errorhandler(404)
# def page_not_found(e):
#     return render_template('util/404.html',message = 'Sorry , page not found!'), 404
#
#
# @mod.errorhandler(500)
# def internal_server_error(e):
#     return render_template('util/500.html', message = 'Something is wrong ,please retry !'), 500
#


#单元测试列表
@mod.route('/unittest_record.json', methods=['POST', 'GET'])
@user.authorize
def test_unittest_result():
    if request.method == 'POST':
        log.log().logger.info('post')
        result = jsonify({'code': 500, 'msg': 'should be get!'})
        return result
    else:
        info = request.values
        log.log().logger.info('info :  %s' %info)
        name = viewutil.getInfoAttribute(info, 'name')
        limit = info.get('limit', 10)  # 每页显示的条数
        offset = info.get('offset', 0)  # 分片数，(页码-1)*limit，它表示一段数据的起点
        data= test_unittest_manage.test_unittest_manage().show_unittest_records(['name'], [name], [], 100)
        data1 = jsonify({'total': len(data), 'rows': data[int(offset):int(offset) + int(limit)]})
        log.log().logger.info('data1: %s' %data1)
        return data1, {'Content-Type': 'application/json'}

# 单元测试详情
@mod.route('/unittest')
@user.authorize
def unittest_records():
    return render_template("util/unittest_records.html")

# 单元测试详情
@mod.route('/view_unitest_result')
@user.authorize
def view_unitest_result():
    info = request.values
    log.log().logger.info('info : %s' %info)
    id = viewutil.getInfoAttribute(info, 'id')
    # from app import test_unittest_manage
    data = test_unittest_manage.test_unittest_manage().show_unittest_records(['id'], [id], [], 100)
    if len(data):
        filename = data[0]['file_name']
        return render_template("util/unittest_detail.html",file_name='/view_unitest_results?id='+id)
    else:
        return render_template("util/unittest_records.html")

# 单元测试详情
@mod.route('/view_unitest_results')
@user.authorize
def view_unitest_results():
    info = request.values
    log.log().logger.info('info : %s' %info)
    id = viewutil.getInfoAttribute(info, 'id')
    # from app import test_unittest_manage
    data = test_unittest_manage.test_unittest_manage().show_unittest_records(['id'], [id], [], 100)
    if len(data):
        filename = data[0]['file_name']
        return render_template("reports/"+filename)
    else:
        return render_template("util/unittest_records.html")


@mod.route('/run_unittest.json', methods=['POST', 'GET'])
@user.authorize
def run_unittest():
    log.log().logger.info(request)
    log.log().logger.info('run unittest')
    if request.method == 'POST':
        log.log().logger.info('post')
        result = jsonify({'code': 500, 'msg': 'should be get!'})
        return result
    else:
        from app.test import test_run_all
        log.log().logger.info('start run unittest')
        test_run_all.run_all()
        result = jsonify({'code': 200, 'msg': 'success!'})

        return result


# 节点管理
@mod.route('/testhubs')
@user.authorize
def testhubs():
    return render_template("util/hubs.html")

@mod.route('/check_hubs.json', methods=['POST', 'GET'])
@user.authorize
def check_hubs():
    log.log().logger.info(request)
    log.log().logger.info('check_hubs')
    if request.method == 'POST':
        log.log().logger.info('post')
        result = jsonify({'code': 500, 'msg': 'should be get!'})
        return result
    else:
        from app.core import hubs
        log.log().logger.info('start checking hubs')
        hubs.hubs().checkHubs()
        result = jsonify({'code': 200, 'msg': 'success!'})

        return result

#节点列表
@mod.route('/search_hubs.json', methods=['POST', 'GET'])
@user.authorize
def search_hubs():
    if request.method == 'POST':
        log.log().logger.info('post')
        result = jsonify({'code': 500, 'msg': 'should be get!'})
        return result
    else:
        info = request.values
        log.log().logger.info('info :  %s' %info)
        # name = viewutil.getInfoAttribute(info, 'name')
        limit = info.get('limit', 10)  # 每页显示的条数
        offset = info.get('offset', 0)  # 分片数，(页码-1)*limit，它表示一段数据的起点
        from app.core import hubs
        # data= test_unittest_manage.test_unittest_manage().show_unittest_records(['name'], [name],[],100)
        data = hubs.hubs().searchHubs()
        data1 = jsonify({'total': len(data), 'rows': data[int(offset):int(offset) + int(limit)]})
        log.log().logger.info('data1: %s' %data1)
        return data1, {'Content-Type': 'application/json'}

# 测试节点详情详情
@mod.route('/view_hub')
@user.authorize
def view_hub():
    return render_template("util/view_hub.html")



#检查登录信息是否正确
@mod.route('/getDevicesList.json', methods=['POST', 'GET'])
def getDevicesList():
    #获取列表
    from app.core import hubs
    list=hubs.hubs().getDevicesList()
    log.log().logger.info('list %s' %list)
    result = jsonify({'msg': list})
    return result, {'Content-Type': 'application/json'}

def hBody(j, needRE):
    import json,re
    body = json.dumps(j, default=lambda j: j.__dict__, sort_keys=True, skipkeys=True)
    if needRE == '1':
        body = re.sub(r'\\', '', body)
        body = json.loads(body)
    return body