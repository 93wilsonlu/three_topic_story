from . import main
from flask import render_template
from three_topic_story.account.model import User


@main.route('/')
def index():
    return render_template('main/index.html')


@main.route('/profile/<string:username>')
def profile(username):
    return render_template('main/profile.html', target_user=User.query.filter_by(username=username).first())
