"""
    ad-password.__init__
    ~~~~~~~~~~~~~~~~~~

    :time 2019/5/15 19:32
    :copyright: (c) 2019 by Leo.
    :license: BSD, see LICENSE for more details.
"""

from logging import Formatter, ERROR
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

__all__ = ['app', 'db']


app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)


# 配置日志
formatter = Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
error_file_handler = RotatingFileHandler('error.log', maxBytes=4 * 1024 * 1024, encoding='utf-8')
error_file_handler.setLevel(ERROR)
error_file_handler.setFormatter(formatter)
app.logger.addHandler(error_file_handler)

from . import view      # noqa
