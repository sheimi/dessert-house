from sqlalchemy import Column, Integer, String, ForeignKey, Table, Text, DateTime, Boolean
from sqlalchemy.orm import backref, mapper, relation, sessionmaker, relationship
from meta import Base, obj2dict
from datetime import datetime as dt, timedelta as td

from meta import session

from models.other_tables import *

class Role(Base):
    __tablename__ = 'role'

    show = {
        'header' : ['Role Name'],
        'show'   : [('name', 'rolename')],
        }

    id = Column(Integer, primary_key=True)
    rolename = Column(String)

    perms = relationship('Permission', secondary=role_perm, backref='roles')

    def __init__(self, rolename):
        self.rolename = rolename

    def __repr__(self):
        return "<Role('%s')>" % self.rolename

    def to_dict(self):
        td = obj2dict(self)
        td['users'] = [i.id for i in self.users]
        td['perms'] = [i.id for i in self.perms]
        return td

    def contains_perm(self, permname):
        for perm in self.perms:
            if perm.permname == permname:
                return True
        return False

    @staticmethod
    def get(role_id):
        role = session.query(Role).filter_by(id=role_id).first()
        return role

    @staticmethod
    def get_all():
      roles = session.query(Role).all()
      return roles

    @staticmethod
    def get_mul(roles_id):
        nodes = ['role.id=%s' % i for i in roles_id]
        q = ' or '.join(nodes)
        q = '(%s)' % q
        roles = session.query(Role).filter(q).all()
        return roles 

    def delete(self):
        session.delete(self)
        session.commit()
 
    def add(self):
        session.add(self)
        session.commit()

    def update(self, **argv):
        from models.perm import Permission
        self.rolename = argv.get('rolename', self.rolename)
        if 'perms' in argv:
            perms_to_add = argv['perms']['add'] and Permission.get_mul(argv['perms']['add']) or None
            perms_to_remove = argv['perms']['remove'] and Permission.get_mul(argv['perms']['remove']) or None
            self.change_perms(perms_to_remove, perms_to_add)
        session.commit()

    def change_perms(self, d_perms=None, a_perms=None):
        if d_perms:
            for perm in d_perms:
                self.perms.remove(perm)
        if a_perms:
            for perm in a_perms:
                self.perms.append(perm)
        session.commit()

