from flask import Blueprint,render_template, jsonify, request, session,redirect
from app import log
from app.view import viewutil
from functools import wraps
from app.core import util
from app.db import test_user_manage

mod = Blueprint('user', __name__,
                        template_folder='templates')

#========================登录模块开始====================================#
#设置登录认证
def authorize(fn):
    @wraps(fn)
    def wrapper():
        user = session.get('user', None)
        if user:
            log.log().logger.info ("已登录")
            return fn()
        else:
            log.log().logger.info ("未登录")
            return render_template("util/login.html")
    return wrapper

#登录页面
@mod.route('/login')
def login():
    return render_template("util/login.html")

#检查登录信息是否正确
@mod.route('/checklogin.json', methods=['POST', 'GET'])
def checklogin():
    username = request.values.get("username")
    password = request.values.get("password")
    log.log().logger.info('username : %s' %username)
    log.log().logger.info('password : %s' %password)
    if username=='' or password=='':
        result = jsonify({'msg': '用户名或密码不能为空'})
    else:
        #MD5加密密码
        md5Password=util.util().md5(password)
        log.log().logger.info('password : %s' %md5Password)
        #检查数据是否存在该用户
        list= test_user_manage.test_user_manage().checklogin(username, md5Password)
        log.log().logger.info('list : %s' %list)
        if(len(list)>0):
            result = jsonify({'msg': '登录成功'})
            #登录成功设置会话
            session['user'] = list
        else:
            result = jsonify({'msg': '用户名或密码错误'})
    return result, {'Content-Type': 'application/json'}


#登出
@mod.route('/loginout')
def loginout():
    session['user']=None
    return render_template("util/login.html")



@mod.route('/edit_user_password', methods=['POST', 'GET'])
@authorize
def edit_user_password():
    log.log().logger.info(request)
    return render_template("util/edit_user_password.html")

@mod.route('/user_password.json', methods=['POST', 'GET'])
@authorize
def user_password():
    list = session.get('user', None)
    id = list[0]["id"]
    log.log().logger.info('id: %s' %id)
    info = request.values
    log.log().logger.info('info : %s' %info)
    password = viewutil.getInfoAttribute(info, 'password')
    log.log().logger.info('password : %s' %password)
    if len(password):
        md5Password = util.util().md5(password)
        log.log().logger.info('md5Password : %s' %md5Password)
        test_user_manage.test_user_manage().update_user_password(id, ['password'], [md5Password])
        result = jsonify({'code':200,'msg': '修改密码成功'})
    else:
        result = jsonify({'code':500,'msg': '密码不得为空！'})
    return result, {'Content-Type': 'application/json'}


#新增用户
@mod.route('/add_user')
@authorize
def new_user():
    return render_template("util/new_user.html")


@mod.route('/users.json', methods=['POST', 'GET'])
@authorize
def show_users():
    users = test_user_manage.test_user_manage().show_users(username='')
    data1 = jsonify({'total': len(users), 'rows': users})
    log.log().logger.info('data1: %s' %data1)
    return data1,{'Content-Type': 'application/json'}

#用户列表
@mod.route('/users')
@authorize
def users():
    return render_template("util/users.html")


@mod.route('/add_user.json', methods=['POST', 'GET'])
def add_user():
    list = session.get('user', None)
    info = request.values
    log.log().logger.info('info : %s' %info)
    username = viewutil.getInfoAttribute(info, 'username')
    password = viewutil.getInfoAttribute(info, 'password')
    log.log().logger.info('password : %s' %password)
    md5Password = util.util().md5(password)
    log.log().logger.info('md5Password : %s' %md5Password)
    result0 = test_user_manage.test_user_manage().new_user(username,md5Password)
    if result0:
        result = jsonify({'code':200,'msg': '新增成功'})
        return result,{'Content-Type': 'application/json'}
    else:
        result = jsonify({'code':500,'msg': '用户已存在！'})
        return result,{'Content-Type': 'application/json'}

#=========================登录模块结束===============================================#

