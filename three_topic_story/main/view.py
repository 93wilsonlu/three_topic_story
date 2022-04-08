from three_topic_story.main import main
from flask import render_template
from three_topic_story.account.model import User
from three_topic_story.post.model import Post


@main.route('/')
def index():
    return render_template('main/index.html')


@main.route('/profile/<string:username>')
def profile(username):
    return render_template('main/profile.html', target_user=User.query.filter_by(username=username).first())


@main.route('/post_list/')
@main.route('/post_list/<int:page>/')
def post_list(page=1):
    posts = Post.query.filter_by(
        private=False).paginate(page, 1, False)
    return render_template('main/post_list.html', posts=posts)
