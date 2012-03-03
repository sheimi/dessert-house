from sqlalchemy import Column, Integer, String, ForeignKey, Table, Text, DateTime, Boolean
from sqlalchemy.orm import backref, mapper, relation, sessionmaker, relationship
from meta import Base, obj2dict
from meta import session


class UserType(Base):
    __tablename__ = 'usertype'

    show = {
        'header' : ['Type Name'],
        'show'   : [('name', 'typename')],
        }
      

    id = Column(Integer, primary_key=True)
    typename = Column(String)
    discount = Column(Integer)
    fee = Column(Integer)

    def __init__(self, typename, discount, fee):
        self.typename = typename
        self.discount = discount
        self.fee = fee

    def __repr__(self):
        return "<UserType('%s')>" % (self.typename)

    def to_dict(self):
        td = obj2dict(self)
        td['users'] = [i.id for i in self.users]
        return td

    @staticmethod
    def get(type_id):
        usertype = session.query(UserType).filter_by(id=type_id).first()
        return usertype

    @staticmethod
    def get_all():
        types = session.query(UserType).all()
        return types

    @staticmethod
    def get_mul(types_id):
        nodes = ['usertype.id=%s' % i for i in types_id]
        q = ' or '.join(nodes)
        q = '(%s)' % q
        types = session.query(UserType).filter(q).all()
        return types

    @staticmethod
    def count(ft=None):
        if not ft:
            return session.query(UserType).count()
        else:
            return session.query(UserType).filter(ft).count()
        
    def add(self):
        session.add(self)
        session.commit()

    def delete(self):
        session.delete(self)
        session.commit()

    def update(self, **argv):
        self.typename = argv.get('typename', self.typename)
        self.discount = argv.get('discount', self.discount)
        self.fee = argv.get('fee', self.fee)
        session.commit()
