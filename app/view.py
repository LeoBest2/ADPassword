"""
    ad-password.view
    ~~~~~~~~~~~~~~~~~~

    :time 2019/5/15 19:33
    :copyright: (c) 2019 by Leo.
    :license: BSD, see LICENSE for more details.
"""

import traceback
from functools import wraps

from flask import request, render_template, jsonify, url_for, redirect
from flask_login import login_required, login_user, logout_user

from . import app
from .config import TITLE, COPYRIGHT, MAIL_SUFFIX, log_admin
from .ad import modify_user_password, is_user_authenticated
from .db import db, Admin, Log


@app.context_processor
def default_context():
    return dict(title=TITLE, copyright=COPYRIGHT, mail_suffix=MAIL_SUFFIX)


@app.route('/', methods=['GET', 'POST'])
def index():
    """修改密码首页"""
    if request.method == 'GET':
        return render_template('index.html')
    _form = request.form
    account, old_pwd, new_pwd = _form.get('account'), _form.get('oldPwd'), _form.get('newPwd')
    if None in (account, old_pwd, new_pwd):
        return jsonify({'err': -1, 'msg': '请求参数不正确!'})
    successed, msg = modify_user_password(account, old_pwd, new_pwd)
    if successed:
        log = Log(account=account, ip=request.headers.get('X-Forwarded-For', request.remote_addr))
        db.session.add(log)
        db.session.commit()
        return jsonify({'err': 0, 'msg': msg})
    return jsonify({'err': 2, 'msg': msg})


@app.route('/login', methods=['GET', 'POST'])
def login():
    """查看日志登陆页面"""
    if request.method == 'GET':
        return render_template('login.html')
    account, pwd = request.form.get('account'), request.form.get('pwd')
    successed, msg = is_user_authenticated(account, pwd)
    if successed:
        if account not in log_admin:
            return jsonify({'err': -1, 'msg': '该账号没有权限查看日志!'})
        admin = Admin(account)
        login_user(admin)
        return jsonify({'err': 0, 'msg': url_for('log_index', _external=True)})
    return jsonify({'err': -1, 'msg': msg})


@app.route('/log_index', methods=['GET', 'POST'])
@login_required
def log_index():
    """查看日志页面
    """
    if request.method == 'GET':
        count = Log.query.count()
        return render_template('log_index.html', count=count)
    _logs = Log.query.order_by(Log.id.desc()).limit(1000).all()
    ret = list(map(lambda x: {'account': x.account, 'ip': x.ip, 'date': x.date.strftime('%Y-%m-%d %H:%M:%S')}, _logs))
    return jsonify(ret)


@app.route('/logoff')
@login_required
def logoff():
    logout_user()
    return redirect(url_for('index'))


@app.errorhandler(Exception)
def page_500(e):
    app.logger.error(traceback.format_exc())
    return render_template('500.html', e=e), 500
