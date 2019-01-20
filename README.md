## 使用前提

**域控必须启用ldaps**

[https://blog.csdn.net/LeoForBest/article/details/75204649](https://blog.csdn.net/LeoForBest/article/details/75204649)

## 修改配置文件`config.py`

```python
# coding=utf-8
#

config = {
    'title': u'TEST域账号密码修改',
    'ldap': {
        'netbios': 'TEST',
        'domain_dns': 'test.com',
        'server': '192.168.241.135',
        'bind_user': 'leo',
        'bind_pwd': 'Aa123456',
        'search_base': 'dc=test,dc=com',
    },
    'log_pwd': 'Aa123456',
    'SECRET_KEY': 'Ik69htKpOjurZ2wA'
}
```

## 运行`run.py`，本地测试

- 安装依赖库

```bash
pip install -r requirements.txt
```

- 双击运行run.py测试

![](./ad.gif)


## 部署