from flask import render_template, session
from app.view import user
from app import app

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

def getInfoAttribute(info,field):
    try:
        value = info.get(field)
    except:
        value = ''
    if value == None:
        value = ''
    return value

