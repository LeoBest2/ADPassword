# coding=utf-8
#

from ldap3 import Server, Connection, RESTARTABLE, set_config_parameter, MODIFY_REPLACE
from ldap3.core.exceptions import LDAPInvalidCredentialsResult, LDAPConstraintViolationResult, \
    LDAPInsufficientAccessRightsResult


# https://ldap3.readthedocs.io/installation.html#global-configuration
set_config_parameter('RESTARTABLE_TRIES', 1)


class AD(object):
    def __init__(self, server, admin, admin_pwd, search_base, netbios):
        self.s = Server(server)
        self.ss = Server(server, use_ssl=True)
        self.admin_c = Connection(self.ss, '%s\%s' % (netbios, admin), admin_pwd, auto_bind=True,
                                  client_strategy=RESTARTABLE, raise_exceptions=True)
        self.search_base = search_base
        self.netbios = netbios

    def is_auth(self, user, pwd, max_recurse=1):
        u"""接受用户SamAccountName和密码\n返回(True or False, message)"""
        if max_recurse < 0:
            return False, u'该用户下次登陆必须修改密码，设置pwdLastSet=-1失败'
        try:
            c = Connection(self.s, '%s\%s' % (self.netbios, user), pwd, auto_bind=True, raise_exceptions=True)
            c.unbind()
            return True, ''
        except LDAPInvalidCredentialsResult as e:
            if '52e' in e.message:
                return False, u'用户名或密码不正确!'
            elif '775' in e.message:
                return False, u'账号已锁定，请联系管理员或等待自动解锁!'
            elif '533' in e.message:
                return False, u'账号已禁用!'
            elif '773' in e.message:
                # 账号下次登陆必须修改密码导致的绑定不成功，取消该设置并再认证一次
                self.admin_c.search(self.search_base, '(SamAccountName=%s)' % user, attributes=['pwdLastSet'])
                dn = self.admin_c.entries[0].entry_dn
                self.admin_c.modify(dn, {'pwdLastSet': [(MODIFY_REPLACE, ['-1'])]})
                return self.is_auth(user, pwd, max_recurse=max_recurse-1)
            else:
                return False, u'认证失败，请联系管理员检查该账号!'

    def modify_password(self, user, old_password, new_password):
        u"""接受用户SamAccountName、旧密码、新密码\n返回(True or False, message)"""
        try:
            ret, msg = self.is_auth(user, old_password)
            if not ret:
                return ret, msg
            self.admin_c.search(self.search_base, '(SamAccountName=%s)' % user,
                                attributes=['pwdLastSet'])
            if len(self.admin_c.entries) == 0:
                return False, u'用户名或密码不正确!'
            entry = self.admin_c.entries[0]
            # 检测密码最短使用时间未实现
            # ......
            # 使用old_password和new_password修改用户密码时候， 必须设置该用户下次登陆必须修改密码，才有效
            self.admin_c.modify(entry.entry_dn, {'pwdLastSet': [(MODIFY_REPLACE, ['0'])]})
            self.admin_c.extend.microsoft.modify_password(user=entry.entry_dn, old_password=old_password,
                                                          new_password=new_password)
            # 密码修改成功，会自动清除下次登陆必须修改密码标志
            return True, ''
        except LDAPInsufficientAccessRightsResult:
            return False, u'无权修改该用户密码!'
        except LDAPConstraintViolationResult as e:
            # 取消用户下次登陆必须修改密码设定
            self.admin_c.modify(entry.entry_dn, {'pwdLastSet': [(MODIFY_REPLACE, ['-1'])]})
            if '00000005' in e.message:
                return False, u'该用户不允许修改密码!'
            if '0000052D' in e.message:
                return False, u'新密码不符合策略要求!'
            if '00000056' in e.message:
                return False, u'用户名或密码不正确!'
            return False, u'修改账号密码错误：%s!' % e.message
