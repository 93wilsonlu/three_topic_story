from three_topic_story import db
from three_topic_story.main import main
from flask import current_app, render_template
from three_topic_story.account.model import User
from three_topic_story.post.model import Post
import sqlalchemy


@main.route('/')
def index():
    posts = Post.query.filter_by(private=False).order_by(
        Post.edit_date.desc()).limit(10).all()
    post_sub = Post.query.group_by(Post.author_id).with_entities(
        Post.author_id, sqlalchemy.func.count(Post.author_id).label('count')).subquery()
    users = User.query.join(
        post_sub, User.id == post_sub.c.author_id).order_by(post_sub.c.count.asc()).limit(10).all()
    return render_template('main/index.html', posts=posts, users=users)


@main.route('/profile/<string:username>')
def profile(username):
    return render_template('main/profile.html', target_user=User.query.filter_by(username=username).first())


@main.route('/post_list/')
@main.route('/post_list/<int:page>/')
def post_list(page=1):
    posts = Post.query.filter_by(
        private=False).paginate(page, 20, False)
    return render_template('main/post_list.html', posts=posts)
