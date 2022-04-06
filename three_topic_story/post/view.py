from . import post
from flask_login import login_required, current_user
from .form import FormEditPost
from .model import Post
from three_topic_story import db, tags
from flask import current_app, flash, render_template, redirect, url_for
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
        flash('完成', 'success')
        return redirect(url_for('post.read_post', id=post.id))

    current_tags = []
    for i in range(3):
        current_tags.append(tags[randint(0, len(tags) - 1)])
    form.tags.data = tags_string = ','.join(current_tags)

    return render_template('post/edit_post.html', form=form, tags_string=tags_string, is_new=True)


@post.route('/<int:id>')
def read_post(id):
    post = Post.query.filter_by(id=id).first_or_404()
    if post.private and (not current_user.is_authenticated or post.author_id != current_user.id):
        flash('該文章已設為私人', 'warning')
        return redirect(url_for('main.index'))
    return render_template('post/read_post.html', post=post)


@post.route('/edit_post/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_post(id):
    post = Post.query.filter_by(id=id).first_or_404()
    if post.author_id != current_user.id:
        flash('這不是您的文章', 'warning')
        return redirect(url_for('main.index'))

    form = FormEditPost()

    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        post.private = form.private.data
        db.session.add(post)
        db.session.commit()
        flash('完成', 'success')
        return redirect(url_for('post.read_post', id=post.id))

    form.title.data = post.title
    tags_string = form.tags.data = post.tags
    form.body.data = post.body
    form.private.data = post.private

    return render_template('post/edit_post.html', form=form, tags_string=tags_string, is_new=False)
