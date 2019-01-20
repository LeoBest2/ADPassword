# coding=utf-8
#

from app import app, db
from sqlalchemy import desc
from config import config
from app.ad import AD
from flask import render_template, request, jsonify, session, redirect
from models import Log
from datetime import datetime

__ad = AD(config['ldap']['server'], config['ldap']['bind_user'], config['ldap']['bind_pwd'],
          config['ldap']['search_base'], config['ldap']['netbios'])


@app.context_processor
def inject_domain():
    count = Log.query.count()
    return {'domain': config['ldap']['domain_dns'], 'title': config['title'], 'count': count}


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html', domain=config['ldap']['domain_dns'])
    user, pwd, new_pwd = request.form['user'], request.form['pwd'], request.form['newPwd']
    ret, msg = __ad.is_auth(user, pwd)
    if not ret:
        return jsonify({'success': False, 'result': msg})
    ret, msg = __ad.modify_password(user, pwd, new_pwd)
    if ret:
        log = Log(sam=user, date=datetime.now())
        db.session.add(log)
        db.session.commit()
        return jsonify({'success': True, 'result': ''})
    return jsonify({'success': False, 'result': msg})


@app.route('/log')
def logs():
    if session.get('login') == '1':
        login = True
    else:
        login = False
    return render_template('log.html', domain=config['ldap']['domain_dns'], login=login)


@app.route('/log/login', methods=['POST'])
def log_login():
    if request.form['pwd'] == config['log_pwd']:
        session['login'] = '1'
    return ''


@app.route('/log/logoff')
def log_logoff():
    session['login'] = '0'
    return redirect('/')


@app.route('/log/json')
def json():
    if session.get('login') != '1':
        return ''
    data = Log.query.order_by(desc('l_id')).limit(100)
    d = [{'name': x.sam, 'date': x.date.strftime("%Y/%m/%d-%H:%M:%S")} for x in data]
    for i in range(len(d)):
        d[i]['id'] = i + 1
    return jsonify(d)
