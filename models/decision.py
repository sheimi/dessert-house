from sqlalchemy import Column, Integer, String, ForeignKey, Table, Text, DateTime, Boolean
from sqlalchemy.orm import backref, mapper, relation, sessionmaker, relationship
from meta import Base, obj2dict
from datetime import datetime as dt, timedelta as td
import uuid
from meta import session

from models.user import User
from models.dessert import Dessert
from util.util import str2date 

class Decision(Base):
    __tablename__ = 'decision'

    show = {
        'header' : ['Decision'],
        'show'   : [('name', 'title')],
        }

    id = Column(Integer, primary_key=True)

    create_date  = Column(DateTime)     #date the order created
    title = Column(String)
    content = Column(String)

    def __init__(self, title, content):

        self.create_date = dt.now()
        self.content = content
        self.title = title

    def __repr__(self):
        return "<Decision %d>" % self.content

    def to_dict(self):
        td = obj2dict(self)
        td['create_date']   = str(self.create_date)
        return td

    @staticmethod
    def get(id):
        decision = session.query(Decision).filter_by(id=id).first()
        return decision 

    @staticmethod
    def get_all():
        decisions = session.query(Order).all()
        return decisions 

    @staticmethod
    def get_mul(ids):
        nodes = ['"decision".id=%s' % i for i in ids]
        q = ' or '.join(nodes)
        q = '(%s)' % q
        decision = session.query(Decision).filter(q).all()
        return decision 

    @staticmethod
    def count(ft=None):
        if not ft:
            return session.query(Decision).count()
        else:
            return session.query(Decision).filter(ft).count()

    def add(self):
        session.add(self)
        session.commit()

    def delete(self):
        session.delete(self)
        session.commit()

    def update(self, **argv):
        self.content = argv.get('content', self.content)
        self.title = argv.get('title', self.title)
        session.commit()

