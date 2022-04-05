from flask_login import current_user
from flask import request, flash, redirect, url_for, render_template

def init_errorhandler(app):
    @app.before_request
    def before_request():
        if (current_user.is_authenticated and
                not current_user.confirm and
                request.endpoint != 'main.index' and
                'account' not in request.endpoint and
                request.endpoint != 'static'):
            flash('請驗證您的帳號')
            return redirect(url_for('account.setting'))

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.errorhandler(401)
    def unauthorized(e):
        flash('請先登入')
        return redirect(url_for('account.login'))
