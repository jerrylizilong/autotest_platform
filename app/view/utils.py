from flask import Blueprint,render_template, jsonify, request,redirect,url_for
from app import log, config
from app.core import hubs
from app.view import viewutil,user
from app.db import test_unittest_manage

mod = Blueprint('unittest', __name__,
                        template_folder='templates')



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
        from app.test import run_unittest
        log.log().logger.info('start run unittest')
        run_unittest.run_all()
        result = jsonify({'code': 200, 'msg': 'success!'})

        return result


@mod.route('/assets/style.css', methods=['GET'])
def get_media():
    return redirect(url_for('static',filename='assets/style.css'))



# 节点管理
@mod.route('/testhubs')
@user.authorize
def testhubs():
    return render_template("util/hubs.html",port=4444)

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
        log.log().logger.info('start checking hubs')
        hubs.hubs().checkHubs()
        result = jsonify({'code': 200, 'msg': 'success!'})

        return result


@mod.route('/add_hub.json', methods=['POST', 'GET'])
def add_hub():
    info = request.values
    log.log().logger.info('info : %s' %info)
    host = viewutil.getInfoAttribute(info, 'host')
    port = viewutil.getInfoAttribute(info, 'port')
    status=viewutil.getInfoAttribute(info, 'status')
    hubs.hubs().updateHub(host,port,'0',status)
    result = jsonify({'code': 200, 'msg': '新增成功'})
    return result, {'Content-Type': 'application/json'}



#新增节点
@mod.route('/add_hub')
@user.authorize
def new_hub():
    return render_template("util/new_hub.html",port=4444)

#新增节点
@mod.route('/edit_hub')
@user.authorize
def edit_hub():
    info = request.values
    id = viewutil.getInfoAttribute(info, 'id')
    data = hubs.hubs().searchHubs(id)
    if len(data):
        host = data[0]['ip']
        port = data[0]['port']
    else:
        host = ''
        port = 4444
    return render_template("util/new_hub.html", host=host,port=port)


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
    return render_template("util/view_hub.html", host=config.ATXHost)



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