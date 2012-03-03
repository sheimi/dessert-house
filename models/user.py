from sqlalchemy import Column, Integer, String, ForeignKey, Table, Text, DateTime, Boolean
from sqlalchemy.orm import backref, mapper, relation, sessionmaker, relationship
from meta import Base, obj2dict
from datetime import datetime as dt, timedelta as td
from meta import session

from models.other_tables import *
from models.usertype import UserType

class User(Base):
    __tablename__ = 'user'

    show = {
        'header' : ['User Name', 'Is Active'],
        'show'   : [('name', 'username'), ('name', 'is_active')],
        }

    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)

    register_time = Column(DateTime)
    expire_time = Column(DateTime)
    type_id = Column(Integer, ForeignKey('usertype.id'))
    is_active = Column(Boolean)

    age = Column(Integer)
    gender = Column(Integer) #boy 1 or girl 2 or default 0
    email = Column(String)
    address = Column(String)
    img = Column(String)

    usertype = relation(UserType, backref='users')

    roles = relationship('Role', secondary=user_role, backref='users')

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.register_time = dt.now()
        self.expire_time = dt.now()
        self.is_active = True
        self.gender = 0

    def __repr__(self):
        return "<User('%s')>" % (self.username)

    def to_dict(self):
        td = obj2dict(self)
        td['roles'] = [i.id for i in self.roles]
        td['expire_time'] = str(self.expire_time)
        td['register_time'] = str(self.register_time)
        return td

    def is_expired(self):
        if not self.usertype:
            return False
        return self.expire_time < dt.now()

    def contains_role(self, rolename):
        for role in self.roles:
            if role.rolename == rolename:
                return True
        return False

    def has_perm(self, permname):
        for role in self.roles:
            for perm in role.perms:
                if permname == perm.permname:
                    return True
        return False

    @staticmethod
    def get_by_id(user_id):
        user = session.query(User).filter_by(id=user_id).first()
        return user

    @staticmethod
    def get(user_id):
        user = session.query(User).filter_by(id=user_id).first()
        return user

    @staticmethod
    def get_by_name(username):
        user = session.query(User).filter_by(username=username).first()
        return user

    @staticmethod
    def get_all(active=None):
        if active == None:
            users = session.query(User).all()
        else:
            users = session.query(User).filter_by(is_active=active).all()
        return users

    @staticmethod
    def get_mul(users_id, active=None):
        nodes = ['user.id=%s' % i for i in users_id]
        q = ' or '.join(nodes)
        q = '(%s)' % q
        if active == None:
            users = session.query(User).filter(q).all()
        else:
            users = session.query(User).filter(q).filter_by(is_active=active).all()
        return users

    @staticmethod
    def count(ft=None):
        if not ft:
            return session.query(User).count()
        else:
            return session.query(User).filter(ft).count()

    def deactivate(self):
        self.is_active = False
        session.commit()

    def delete(self):
        session.delete(self)
        session.commit()

    def add(self):
        session.add(self)
        session.commit()

    def update(self, **argv):
        from models.role import Role
        self.username = argv.get('username', self.username)
        self.password = argv.get('password', self.password)
        self.type_id = argv.get('type', self.type_id)
        self.age = argv.get('age', self.age)
        self.address = argv.get('address', self.address)
        self.email = argv.get('email', self.email)
        self.gender = argv.get('gender', self.gender)
        if 'roles' in argv:
            roles_to_add = argv['roles']['add'] and Role.get_mul(argv['roles']['add']) or None
            roles_to_remove = argv['roles']['remove'] and Role.get_mul(argv['roles']['remove']) or None
            self.change_roles(roles_to_remove, roles_to_add)
        if 'recharge' in argv:
            self.recharge(argv['recharge'])
        session.commit()

    def change_roles(self, d_roles=None, a_roles=None):
        if d_roles:
            for role in d_roles:
                self.roles.remove(role)
        if a_roles:
            for role in a_roles:
                self.roles.append(role)
        session.commit()

    def activate(self):
        self.is_active = True
        session.commit()
  
    def recharge(self, d=1):
        self.expire_time += td(365 * d)
        session.commit()
