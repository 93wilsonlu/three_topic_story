from . import post
from flask_login import login_required, current_user
from .form import FormEditPost
from .model import Post
from three_topic_story import db, tags
from flask import flash, render_template, redirect, url_for
from random import randint


@post.route('/new_post', methods=['GET', 'POST'])
@login_required
def new_post():
    form = FormEditPost()

    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            tags=form.tags.data,
            body=form.body.data,
            author_id=current_user.id,
            private=form.private.data,
        )
        db.session.add(post)
        db.session.commit()
        flash('完成')
        return redirect(url_for('main.index'))
        # return redirect(url_for('post.read_post', id=post.id))

    current_tags = []
    for i in range(3):
        current_tags.append(tags[randint(0, len(tags) - 1)])
    form.tags.data = tags_string = ','.join(current_tags)

    return render_template('post/edit.html', form=form, tags_string=tags_string, is_new=True)
