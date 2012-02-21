from sqlalchemy import Column, Integer, String, ForeignKey, Table, Text, DateTime, Boolean
from sqlalchemy.orm import backref, mapper, relation, sessionmaker, relationship
from meta import Base, obj2dict

user_role = Table('user_role', Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id')),
    Column('role_id', Integer, ForeignKey('role.id')),
)

role_perm = Table('role_perm', Base.metadata,
    Column('role_id', Integer, ForeignKey('role.id')),
    Column('perm_id', Integer, ForeignKey('perm.id')),
)

