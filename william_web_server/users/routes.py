from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import login_user, current_user, logout_user, login_required
from william_web_server import db, bcrypt
from william_web_server.models import User, Post
from william_web_server.users.forms import (RegistrationForm, LoginForm,
                                            UpdateAccountForm, RequestResetForm,
                                            ResetPasswordForm)
from william_web_server.users.utils import save_picture, send_reset_email

users = Blueprint('users', __name__)


@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        # db.create_all()
        db.session.add(user)
        db.session.commit()
        flash(f'您的账号已经成功注册咯~欢迎【{form.username.data}】加入乐学偶得的大家庭，也欢迎关注乐学偶得公众号哟：乐学Fintech', 'success')
        return redirect(url_for('login'))
    return render_template("register.html", title="乐学偶得注册界面", form=form)


@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("index"))
        else:
            flash("Oops，登录失败，客官要不再想想您的email与密码是否正确呢？", "danger")

    return render_template("login.html", title="乐学偶得登录界面", form=form)


@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("index"))


@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("您的信息已经成功更新", "success")
        return redirect(url_for("account"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for("static", filename="user_profile_pics/" + current_user.image_file)
    return render_template("account.html", title="我的个人账户页面", image_file=image_file, form=form)


@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()) \
        .paginate(page=page, per_page=1)
    return render_template('user_posts.html', posts=posts, user=user)


@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('已经将重置密码邮件发送到您的邮箱，请注意及时查收并设置新的密码', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='邮箱重置密码页面', form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('不好意思，您的验证标识不正确，请重试', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash(f'您的密码已经成功修改~欢迎您回到乐学偶得的大家庭，也欢迎关注乐学偶得公众号哟：乐学Fintech', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='输入新密码页面', form=form)
