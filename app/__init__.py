from flask import Flask
from flask_bootstrap import Bootstrap
from app.view import user,uitest,utils,apinew,minder,minderfiles

app = Flask(__name__)
app.config.from_object('config')
bootstrap = Bootstrap(app)
app.register_blueprint(user.mod)
app.register_blueprint(uitest.mod)
app.register_blueprint(utils.mod)
app.register_blueprint(apinew.mod)
app.register_blueprint(minder.mod)
app.register_blueprint(minderfiles.mod)
from app import views
