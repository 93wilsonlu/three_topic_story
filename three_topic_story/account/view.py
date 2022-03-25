from . import account
from .form import FormRegister
from .model import User
from .. import app, db
from ..sendmail import send_mail
from flask import redirect, render_template, flash, url_for


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
        #  產生用戶認證令牌
        token = user.create_confirm_token()
        #  寄出帳號啟動信件
        send_mail(sender=app.config.get('MAIL_USERNAME'),
                  recipients=[user.email],
                  subject='Activate your account',
                  template='account/mail/confirm_mail',
                  mailtype='html',
                  user=user,
                  token=token)

        flash('Check Your Email and Activate Your Account')
        return redirect(url_for('main.index'))
    return render_template('account/register.html', form=form)
