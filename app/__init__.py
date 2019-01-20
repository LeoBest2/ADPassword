# coding=utf-8
#

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config


app = Flask(__name__)
app.config['SECRET_KEY'] = config['SECRET_KEY']
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///log.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

import views
