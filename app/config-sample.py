"""
    ad-password.config
    ~~~~~~~~~~~~~~~~~~

    :time 2019/5/15 19:33
    :copyright: (c) 2019 by Leo.
    :license: BSD, see LICENSE for more details.
"""

# 域信息配置
NETBIOS_NAME = 'TEST'
SERVER = '172.25.1.3'
BIND_USER = 'test@test.com'
BIND_PWD = 'Aa123456'
SEARCH_BASE = 'dc=test,dc=com'
MAIL_SUFFIX = 'test.com'

# 网站信息配置
TITLE = '域账号密码修改'
COPYRIGHT = 'Copyright © 2019 test.com  All rights reserved.'

# 允许查看日志信息的人员
log_admin = [
    'test',     # 管理员1
    'test1',    # 管理员2
    'test2'     # 管理员3
]

SECRET_KEY = 'Ik69htKpOjurZ2wA'
SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite3'
SQLALCHEMY_TRACK_MODIFICATIONS = False
