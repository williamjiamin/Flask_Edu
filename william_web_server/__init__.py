# -*- coding: utf-8 -*-
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

app=Flask(__name__)

app.config["SECRET_KEY"]="6b7c1127809fd65913025625d0c08bc2"
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///site.db'

db = SQLAlchemy(app)
bcrypt =Bcrypt(app)
login_manager =LoginManager(app)
login_manager.login_message_category = 'info'
login_manager.login_message = u"这位小伙伴不好意思鸭，这里是只有会员才能接触的世界"
login_manager.login_view ='login'

app.config['MAIL_SERVER'] = 'smtp.163.com'
# 163:Non SSL: 25/ SSL:465/994
app.config['MAIL_PORT'] = 25
# app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')
mail = Mail(app)



from william_web_server import routes





# 关于加密补充：1）明文储存——————不需要破解 2）对称加密——————破解难度中等（但是前提是key必须要保密）3）HASH (单项、特殊（salt）)
# 1）saltRounds:正数
# 2）myPassword:明文密码字符串
# 3）salt:128bit, 22字符
# 4）myHash：循环加salt进行hash得到的结果