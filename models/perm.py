from sqlalchemy import Column, Integer, String, ForeignKey, Table, Text, DateTime, Boolean
from sqlalchemy.orm import backref, mapper, relation, sessionmaker, relationship
from meta import Base, obj2dict
from datetime import datetime as dt, timedelta as td
from meta import session
from models.other_tables import *


class Permission(Base):
    __tablename__ = 'perm'

    id = Column(Integer, primary_key=True)
    permname = Column(String)

    show = {
        'header' : ['Permission Name'],
        'show'   : [('name', 'permname')],
        }
      
    def __init__(self, permname):
        self.permname = permname

    def __repr__(self):
        return "<Perm('%s')>" % self.permname

    def to_dict(self):
        td = obj2dict(self)
        td['roles'] = [i.id for i in self.roles]
        return td

    @staticmethod
    def get(perm_id):
        perm = session.query(Permission).filter_by(id=perm_id).first()
        return perm

    @staticmethod
    def get_all():
        perms = session.query(Permission).all()
        return perms

    @staticmethod
    def get_mul(perms_id):
        nodes = ['perm.id=%s' % i for i in perms_id]
        q = ' or '.join(nodes)
        q = '(%s)' % q
        perms = session.query(Permission).filter(q).all()
        return perms

    def add(self):
        session.add(self)
        session.commit()

    def delete(self):
        session.delete(self)
        session.commit()

    def update(self, **argv):
        self.permname = argv.get('permname', self.permname)
        session.commit()

