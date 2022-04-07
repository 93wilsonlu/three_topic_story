from . import account
from .form import FormRegister, FormLogin, FormSetting, FormChangePassword, FormForgotPassword, FormResetPassword
from .model import User
from three_topic_story import db, uploads_images
from three_topic_story.sendmail import send_mail
from flask import redirect, render_template, flash, url_for, current_app, request
from flask_login import login_required, current_user, login_user, logout_user
import hashlib
import time


@account.route('register', methods=['GET', 'POST'])
def register():
    form = FormRegister()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        db.session.add(user)
        db.session.commit()

        token = user.create_confirm_token()
        send_mail(sender=current_app.config.get('MAIL_USERNAME'),
                  recipients=[user.email],
                  subject='驗證您的帳戶',
                  template='account/mail/confirm_mail',
                  mailtype='html',
                  user=user,
                  token=token)

        flash('註冊成功，請確認您的信箱', 'success')
        return redirect(url_for('main.index'))
    return render_template('account/register.html', form=form)


@account.route('/user_confirm/<token>')
def user_confirm(token):
    user = User()
    data = user.validate_confirm_token(token)
    if data:
        user = User.query.filter_by(id=data.get('user_id')).first()
        user.confirm = True
        db.session.add(user)
        db.session.commit()
        flash('驗證成功', 'success')
        if not current_user.is_authenticated:
            flash('請重新登入您的帳號', 'warning')
    else:
        flash('無效的網址', 'error')
    return redirect(url_for('main.index'))


@account.route('/resend_confirm_email')
@login_required
def resend_confirm_email():
    if not current_user.confirm:
        token = current_user.create_confirm_token()
        send_mail(sender=current_app.config.get('MAIL_USERNAME'),
                  recipients=[current_user.email],
                  subject='驗證您的帳戶',
                  template='account/mail/confirm_mail',
                  mailtype='html',
                  user=current_user,
                  token=token)
        flash('確認信已送出，請查看您的信箱')
    return redirect(url_for('account.setting'))


@account.route('/login', methods=['GET', 'POST'])
def login():
    form = FormLogin()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if user.check_password(form.password.data):
                login_user(user, form.remember_me.data)
                next = request.args.get('next')
                return redirect(next or url_for('main.index'))
            else:
                flash('帳號/密碼錯誤', 'error')
        else:
            flash('帳號/密碼錯誤', 'error')
    return render_template('account/login.html', form=form)


@account.route('/setting', methods=['GET', 'POST'])
def setting():
    form = FormSetting()
    if form.validate_on_submit():
        if form.avatar.data:
            alternative_name = current_user.username + str(time.time())
            alternative_name = hashlib.md5(
                alternative_name.encode('utf-8')).hexdigest()
            file_name = uploads_images.save(form.avatar.data, folder='avatar',
                                            name=alternative_name + '.')
            current_user.avatar_url = uploads_images.url(file_name)

        current_user.email = form.email.data
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        db.session.commit()
        flash('更新成功', 'success')
        return redirect(url_for('account.setting'))
    form.email.data = current_user.email
    form.username.data = current_user.username
    form.about_me.data = current_user.about_me
    return render_template('account/setting.html', form=form)


@account.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = FormChangePassword()
    if form.validate_on_submit():
        if current_user.check_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            db.session.commit()
            flash('更新成功', 'success')
            return redirect(url_for('account.change_password'))
        else:
            flash('舊密碼錯誤', 'error')
    return render_template('account/change_password.html', form=form)


@account.route('/logout')
@login_required
def logout():
    logout_user()
    flash('登出成功', 'success')
    return redirect(url_for('main.index'))


@account.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))

    form = FormForgotPassword()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.create_confirm_token()
            send_mail(sender=current_app.config.get('MAIL_USERNAME'),
                      recipients=[user.email],
                      subject='Reset Your Password',
                      template='account/mail/reset_password_mail',
                      mailtype='html',
                      user=current_user,
                      token=token)
            flash('已送出，請確認您的信箱', 'success')
            return redirect(url_for('account.login'))
    return render_template('account/forgot_password.html', form=form)


@account.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))

    form = FormResetPassword()
    user = User()
    data = user.validate_confirm_token(token)

    if not data:
        flash('無效的網址', 'error')
        return redirect(url_for('main.index'))

    user = User.query.filter_by(id=data.get('user_id')).first()
    if not user:
        flash('帳戶不存在', 'error')
        return redirect(url_for('main.index'))

    if form.validate_on_submit():
        user.password = form.password.data
        db.session.commit()
        flash('已重設您的密碼，請重新登入', 'success')
        return redirect(url_for('account.login'))
    return render_template('account/reset_password.html', form=form)
