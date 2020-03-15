# -*- coding: utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from william_web_server.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_message_category = 'info'
login_manager.login_message = u"这位小伙伴不好意思鸭，这里是只有会员才能接触的世界"
login_manager.login_view = 'users.login'

mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from william_web_server.users.routes import users
    from william_web_server.posts.routes import posts
    from william_web_server.main.routes import main
    from william_web_server.errors.handlers import errors

    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app

# 关于加密补充：1）明文储存——————不需要破解 2）对称加密——————破解难度中等（但是前提是key必须要保密）3）HASH (单项、特殊（salt）)
# 1）saltRounds:正数
# 2）myPassword:明文密码字符串
# 3）salt:128bit, 22字符
# 4）myHash：循环加salt进行hash得到的结果
