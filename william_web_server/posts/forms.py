from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    title = StringField("文章标题", validators=[DataRequired(message="发文章必须要写文章标题哦～")])
    content = TextAreaField("文章内容", validators=[DataRequired(message="发文章必须要有文章内容哦～")])
    submit = SubmitField("点我发表文章")
