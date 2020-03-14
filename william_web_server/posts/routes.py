from flask import Blueprint, render_template, url_for, redirect, request, flash, abort
from flask_login import current_user, login_required
from william_web_server import db
from william_web_server.models import Post
from william_web_server.posts.forms import PostForm

posts = Blueprint('posts', __name__)


@posts.route("/post/new", methods=["GET", "POST"])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("您的文章已经成功发布", 'success')
        return redirect(url_for('main.index'))
    return render_template("create_post.html", title="写新文章", form=form, legend="写新文章")


@posts.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("post.html", title=post.title, post=post)


@posts.route("/post/<int:post_id>/update", methods=["GET", "POST"])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash("您的文章已经进行了更新！", "success")
        return redirect(url_for("posts.post", post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content

    return render_template("create_post.html", title="更新文章", form=form, legend="更新文章")


@posts.route("/post/<int:post_id>/delete", methods=["POST"])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('您的文章已经删除', 'success')
    return redirect(url_for('main.index'))
