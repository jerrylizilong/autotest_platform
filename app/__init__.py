from flask import Flask
from flask_bootstrap import Bootstrap
from app.view import user,uitest,utils

app = Flask(__name__)
app.config.from_object('config')
bootstrap = Bootstrap(app)
app.register_blueprint(user.mod)
app.register_blueprint(uitest.mod)
app.register_blueprint(utils.mod)
from app import views
