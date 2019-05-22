from flask import Blueprint,render_template, jsonify, request, redirect
from app import log
from app.view import viewutil,user
from app.db import test_minder_manage

mod = Blueprint('minder', __name__,
                        template_folder='templates/minder')

@mod.route('/save_new_test_minder.json', methods=['POST'])
@user.authorize
def save_new_test_minder():
    log.log().logger.info(request)
    if request.method == 'GET':
        log.log().logger.info('post')
        return redirect("/test_minders")
    if request.method == 'POST':
        info = request.values
        log.log().logger.info('info :%s' %info)
        id = viewutil.getInfoAttribute(info,'id')
        type = viewutil.getInfoAttribute(info,'type')
        name = viewutil.getInfoAttribute(info,'name')
        module = viewutil.getInfoAttribute(info,'module')
        description = viewutil.getInfoAttribute(info,'description')
        minder_id = ''
        if name == '' :
            message =  '必填字段不得为空！'
            code = 500
        else:
            if type == 'add':
                minders =test_minder_manage.test_minder_manage().new_minder(module,name,  description)
                if minders['code']:
                    minder_id = minders['id']
                    message = 'success！'
                    code = 200
                else:
                    message = '保存失败！'
                    code = 500
            else:
                test_minder_manage.test_minder_manage().update_test_minder(id=id,
                                                                           fieldlist=['name', 'module', 'description'],
                                                                           valueList=[name, module, description])
                message = 'success！'
                code = 200
                minder_id = id
        result = jsonify({'code': code, 'msg': message,'id':minder_id})
        log.log().logger.info(result)
        log.log().logger.info('code is : %s'%code)
        # return redirect("/test_minders")
        return result,{'Content-Type': 'application/json'}

@mod.route('/save_test_minder_content.json', methods=['POST', 'GET'])
@user.authorize
def save_test_minder_content():
    log.log().logger.info(request)
    if request.method == 'GET':
        log.log().logger.info('post')
        return redirect("/test_minders")
    if request.method == 'POST':
        info = request.values
        log.log().logger.info('info :%s' %info)
        id = viewutil.getInfoAttribute(info,'id')
        content = viewutil.getInfoAttribute(info,'content')
        minder_id = ''
        if content == '':
            message =  '必填字段不得为空！'
            code = 500
        else:
            test_minder_manage.test_minder_manage().update_test_minder(id=id, fieldlist=['content'],valueList=[content])
            message = 'success！'
            code = 200
        result = jsonify({'code': code, 'msg': message})
        log.log().logger.info(result)
        log.log().logger.info('code is : %s'%code)
        return result


@mod.route('/copy_test_minder.json', methods=['POST', 'GET'])
@user.authorize
def copy_test_minder():
    log.log().logger.info(request)
    if request.method == 'GET':
        log.log().logger.info('post')
        return redirect("test_minders")
    if request.method == 'POST':
        info = request.values
        log.log().logger.info('info :%s' %info)
        id = viewutil.getInfoAttribute(info,'id')
        print(id)
        if id == '' :
            message =  '必填字段不得为空！'
            code = 500
        else:
            result = test_minder_manage.test_minder_manage().copy_test_minder(id)
            if result['code']:
                message = 'success！'
                code = 200
                id = result['id']
            else:
                message = 'error！'
                code = 500

        result = jsonify({'code': code, 'msg': message,'id':id})
        log.log().logger.info(result)
        log.log().logger.info('code is : %s'%code)
        return result,{'Content-Type': 'application/json'}

@mod.route('/delete_test_minder.json', methods=['POST', 'GET'])
@user.authorize
def delete_test_minder():
    log.log().logger.info(request)
    if request.method == 'GET':
        log.log().logger.info('post')
        return redirect("test_minders")
    if request.method == 'POST':
        info = request.values
        log.log().logger.info('info :%s' %info)
        id = viewutil.getInfoAttribute(info,'id')
        print(id)
        if id == '' :
            message =  'minder 不存在！'
            code = 500
        else:
            test_minder_manage.test_minder_manage().update_test_minder(id=id,fieldlist=['status'],valueList=[0])
            message = 'success！'
            code = 200

        result = jsonify({'code': code, 'msg': message})
        log.log().logger.info(result)
        log.log().logger.info('code is : %s'%code)
        return result


@mod.route('/edit_minder_json')
@user.authorize
def edit_test_minder_json_page():
    log.log().logger.info(request)
    if request.method == 'POST':
        log.log().logger.info('POST')
        return redirect("test_minders")
    if request.method == 'GET':
        info = request.values
        log.log().logger.info('info :%s' %info)
        minder_id = viewutil.getInfoAttribute(info,'id')
        return render_template("minder/index.html",minder_id=minder_id)

@mod.route('/view_minder_json')
# @user.authorize
def view_test_minder_json_page():
    log.log().logger.info(request)
    if request.method == 'POST':
        log.log().logger.info('POST')
        return redirect("test_minders")
    if request.method == 'GET':
        info = request.values
        log.log().logger.info('info :%s' %info)
        minder_id = viewutil.getInfoAttribute(info,'id')
        return render_template("minder/view.html",minder_id=minder_id)

@mod.route('/edit_minder')
@user.authorize
def edit_test_minder_page():
    log.log().logger.info(request)
    if request.method == 'POST':
        log.log().logger.info('POST')
        return redirect("test_minders")
    if request.method == 'GET':
        info = request.values
        log.log().logger.info('info :%s' %info)
        minder_id = viewutil.getInfoAttribute(info,'id')
        return render_template("minder/edit_test_minder.html",minder_id=minder_id)

@mod.route('/test_minders')
@user.authorize
def test_minders():
    return render_template("minder/test_minders.html")

@mod.route('/add_test_minder')
@user.authorize
def add_test_minder_page():
    return render_template("minder/new_test_minder.html")


@mod.route('/get_minders.json', methods=['POST', 'GET'])
# @user.authorize
def get_minders():
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
        name = viewutil.getInfoAttribute(info, 'name')
        type = viewutil.getInfoAttribute(info, 'type')
        log.log().logger.info('module: %s' %module)
        rows = 100
        if id !='':
           data = test_minder_manage.test_minder_manage().show_test_minders( conditionList=['id'],valueList=[id],rows=rows)
           if type == 'edit':
                data1 = jsonify({'code':200,'minder':data[0]})
           else:
               data1 = jsonify({'code': 200, 'content': data[0]['content']})
        else:
            data = test_minder_manage.test_minder_manage().show_test_minders( conditionList=['module','name'],valueList=[module,name],rows=rows)
            data1 = jsonify({'total': len(data), 'rows': data[int(offset):int(offset) + int(limit)]})
        # print(data)

        log.log().logger.info('data1: %s' %data1)
        return data1,{'Content-Type': 'application/json'}

