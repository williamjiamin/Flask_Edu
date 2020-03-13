from flask import Blueprint, request, render_template
from william_web_server.models import Post

main = Blueprint('main', __name__)


@main.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(per_page=3)
    return render_template("main.html", posts=posts)


@main.route('/about')
def about():
    return render_template("about.html", title="关于乐学偶得")
