import os
import secrets
from PIL import Image
from flask import url_for
from flask_mail import Message
from william_web_server import app, mail


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, file_extension = os.path.splitext(form_picture.filename)
    picture_filename = random_hex + file_extension
    picture_path = os.path.join(app.root_path, "static/user_profile_pics", picture_filename)
    # form_picture.save(picture_path)

    output_img_size = (100, 100)
    thumbnail_img = Image.open(form_picture)
    thumbnail_img.thumbnail(output_img_size)
    thumbnail_img.save(picture_path)

    return picture_filename


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('关于重置【乐学偶得】账号信息的邮件',
                  sender='William<williamjiamin@163.com>',
                  recipients=[user.email])
    msg.body = f'''您正在进行【乐学偶得】忘记密码操作，请点击下列链接进行密码重置：
{url_for('reset_token', token=token, _external=True)}
'''
    mail.send(msg)
