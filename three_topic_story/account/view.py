from . import account
from .form import FormRegister
from .model import User
from .. import db
from ..sendmail import send_mail
from flask import redirect, render_template, flash, url_for, current_app, request
from flask_login import login_required, current_user


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

        flash('註冊成功，請確認您的信箱')
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
        flash('驗證成功')
        flash('請重新登入您的帳號')
        # TODO: logout
    else:
        flash('無效的網址')
    return redirect(url_for('main.index'))


@account.route('/resend_confirm_email')
@login_required
def resend_confirm_email():
    token = current_user.create_confirm_token()
    send_mail(sender=current_app.config.get('MAIL_USERNAME'),
              recipients=[current_user.email],
              subject='驗證您的帳戶',
              template='account/mail/confirm_mail',
              mailtype='html',
              user=current_user,
              token=token)
    flash('確認信已送出，請查看您的信箱')
    return redirect(url_for('main.index'))


@account.before_app_request
def before_request():
    if (current_user.is_authenticated and
            not current_user.confirm and
            request.endpoint not in ['resend_confirm_email', 'logout', 'user_confirm'] and
            request.endpoint != 'static'):
        flash('請驗證您的帳號')
        return redirect(url_for('resend_confirm_email'))
