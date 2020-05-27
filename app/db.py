"""
    ad-password.db
    ~~~~~~~~~~~~~~~~~~

    :time 2019/5/15 19:45
    :copyright: (c) 2019 by Leo.
    :license: BSD, see LICENSE for more details.
"""

from datetime import datetime

from flask_login import LoginManager, UserMixin

from . import app, db

__all__ = ['db', 'Admin', 'Log']

# https://flask-login.readthedocs.io/en/latest/
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(account):
    return Admin(account)


class Admin(UserMixin):
    """登陆用户对象

    https://flask-login.readthedocs.io/en/latest/
    """
    def __init__(self, account):
        self.account = account

    def get_id(self):
        return self.account


class Log(db.Model):
    """
    数据库日志
    """
    id = db.Column(db.Integer, primary_key=True)
    account = db.Column(db.String(128), nullable=False)
    ip = db.Column(db.String(64))
    date = db.Column(db.DateTime, default=datetime.now)
