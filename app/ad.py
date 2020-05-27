"""
    ad-password.ad
    ~~~~~~~~~~~~~~~~~~
    验证域账号和密码是否正确 & 修改域账号密码

    :time 2019/5/19 15:15
    :copyright: (c) 2019 by Leo.
    :license: BSD, see LICENSE for more details.
"""

from ldap3 import Server, Connection, set_config_parameter
from ldap3.core.exceptions import LDAPInvalidCredentialsResult, LDAPInsufficientAccessRightsResult, \
    LDAPConstraintViolationResult, LDAPException

from app.config import SERVER, BIND_USER, BIND_PWD, NETBIOS_NAME, SEARCH_BASE


set_config_parameter('RESTARTABLE_TRIES', 1)
_server = Server(SERVER, use_ssl=True)
_conn = Connection(server=_server, user=BIND_USER, password=BIND_PWD, auto_bind=True, raise_exceptions=True)


__all__ = ['is_user_authenticated', 'modify_user_password']


def is_user_authenticated(account, pwd, ignore_must_change_password_at_logon=False):
    """
    验证域账号和密码是否正确

    :param account: str : SamAccountName
    :param pwd: str
    :param ignore_must_change_password_at_logon: bool :
            供修改密码使用,设置为True时当检测到用户必须修改密码时通过验证(只有密码正确且设置了用户下次登录必须修改密码时候才返回错误代码773)，
            返回(True, ''), 否则返回(False, msg)
    :return: tuple : (True or False: bool, msg: str)
    """
    try:
        with Connection(server=_server, user=r'%s\%s' % (NETBIOS_NAME, account), password=pwd,
                        auto_bind=True, raise_exceptions=True):
            return True, ''
    except LDAPInvalidCredentialsResult as e:
        """
        http://www-01.ibm.com/support/docview.wss?uid=swg21290631
        525	user not found
        52e	invalid credentials
        530	not permitted to logon at this time
        531	not permitted to logon at this workstation
        532	password expired
        533 account disabled 
        534	The user has not been granted the requested logon type at this machine
        701	account expired
        773	user must reset password
        775	user account locked
        """
        if '52e' in e.message:
            msg = '账号或密码不正确!'
        elif '773' in e.message:
            if ignore_must_change_password_at_logon:
                return True, ''
            msg = '该账号必须修改密码后才能登陆!'
        elif '775' in e.message:
            msg = '该账号已锁定, 请联系管理员解锁!'
        elif '525' in e.message:
            msg = '用户不存在!'
        elif '530' in e.message:
            msg = '当前时间段不允许登陆!'
        elif '532' in e.message:
            msg = '密码已过有效期, 请联系管理员重置!'
        elif '533' in e.message:
            msg = '该账号已被禁用, 请联系管理员!'
        elif '534' in e.message:
            msg = '未在此计算机上为用户授予所请求的登录类型!'
        elif '701' in e.message:
            msg = '该账号已过期, 请联系管理员!'
        else:
            msg = e.message
        return False, msg


def modify_user_password(account, old_pwd, new_pwd):
    """
    修改域账号密码

    :param account: str: 域账号
    :param old_pwd: str: 旧密码
    :param new_pwd: str: 新密码
    :return: tuple : (True or False: bool, msg: str)
    """
    sucessed, msg = is_user_authenticated(account, old_pwd, ignore_must_change_password_at_logon=True)
    if not sucessed:
        return False, msg
    try:
        _conn.search(SEARCH_BASE, '(SamAccountName=%s)' % account)
        if len(_conn.entries) == 0:
            return False, '无法找到该账号DistinguishedName!'
        _dn = _conn.entries[0].entry_dn
        _conn.extend.microsoft.modify_password(_dn, new_password=new_pwd, old_password=old_pwd)
        return True, ''
    except LDAPConstraintViolationResult as e:
        if '00000005' in e.message:
            msg = '该账号不允许修改密码!'
        elif '0000052D' in e.message:
            msg = '新密码不符合策略要求!'
        elif '00000056' in e.message:
            msg = '用户名或密码不正确!'
        else:
            msg = e.message
        return False, msg
    except LDAPInsufficientAccessRightsResult:
        return False, u'无权修改该账号密码!'
    except LDAPException as e:
        return False, '服务器错误: %s' % e
