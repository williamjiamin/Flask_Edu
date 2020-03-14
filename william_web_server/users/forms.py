from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from william_web_server.models import User
from flask_login import current_user


class RegistrationForm(FlaskForm):
    username = StringField("昵称", validators=[DataRequired(message="虽然英雄无名，但是还请大侠写一个名字呗"),
                                             Length(min=2, max=20, message="不好意思，昵称至少要2——20字符之间哦~")])
    email = StringField("邮箱信息", validators=[DataRequired(message="大侠，现在是21世纪，留个邮箱好联系啊，飞鸽传书臣妾做不到啊！"),
                                            Email(message="大神，您是穿越过来的吗？email的格式是yourname@188.com这样的~")])
    password = PasswordField("密码", validators=[DataRequired(message="额滴个神啊，大锅您不输入密码怎么注册啊！")])
    confirm_password = PasswordField("再次确认你的密码", validators=[DataRequired(message="额滴个神啊，大锅您不输入密码怎么注册啊！"),
                                                             EqualTo("password", message="这位高手，别逗我玩了，您两次输入的密码不一样啊！")])
    submit = SubmitField("点击注册")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("不好意思鸭，这位小伙伴，这个用户名已经有人注册了呢~要不，咱换一个？")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("不好意思鸭，这位小伙伴，这个email(伊妹儿)已经有人注册了呢~要不，咱换一个？")


class UpdateAccountForm(FlaskForm):
    username = StringField("昵称", validators=[DataRequired(message="虽然英雄无名，但是还请大侠写一个名字呗"),
                                             Length(min=2, max=20, message="不好意思，昵称至少要2——20字符之间哦~")])
    email = StringField("邮箱信息", validators=[DataRequired(message="大侠，现在是21世纪，留个邮箱好联系啊，飞鸽传书臣妾做不到啊！"),
                                            Email(message="大神，您是穿越过来的吗？email的格式是yourname@188.com这样的~")])
    picture = FileField("点我上传头像", validators=[FileAllowed(["jpg", "png"], message="不好意思，目前只支持上传jpg与png格式的头像哦～")])
    submit = SubmitField("点我更新个人信息")

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("不好意思鸭，这位小伙伴，这个用户名已经有人注册了呢~要不，咱换一个？")

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError("不好意思鸭，这位小伙伴，这个email(伊妹儿)已经有人注册了呢~要不，咱换一个？")


class LoginForm(FlaskForm):
    email = StringField("邮箱信息", validators=[DataRequired(), Email()])
    password = PasswordField("密码", validators=[DataRequired()])
    remember = BooleanField("点我记住密码，下次就不用再输入密码了哟~")
    submit = SubmitField("点击登录")


class RequestResetForm(FlaskForm):
    email = StringField("邮箱信息",
                        validators=[DataRequired(message="大侠，你不是忘记密码了吗？写个邮箱好帮你找回啊！"),
                                    Email(message="大神，您是穿越过来的吗？email的格式是yourname@188.com这样的~")])
    submit = SubmitField("点我找回密码")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('您确定是这个email吗？我们查询不到以这个email注册的账号哦～如果您未注册，可以先注册账号哦～')


class ResetPasswordForm(FlaskForm):
    password = PasswordField("密码", validators=[DataRequired(message="额滴个神啊，大锅您不输入密码怎么帮您设置新密码啊！")])
    confirm_password = PasswordField("再次确认你的密码",
                                     validators=[DataRequired(message="额滴个神啊，大锅您不输入密码怎么帮您设置新密码啊！"),
                                                 EqualTo("password", message="这位高手，别逗我玩了，您两次输入的密码不一样啊！")])
    submit = SubmitField("点击重置密码")
