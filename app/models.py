# coding=utf-8
#

from app import db


class Log(db.Model):
    l_id = db.Column(db.Integer, primary_key=True)
    sam = db.Column(db.String(64), unique=False, nullable=False)
    date = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return 'Log %r' % self.sam
