from sqlalchemy import Column, Integer, String, ForeignKey, Table, Text, DateTime, Boolean
from sqlalchemy.orm import backref, mapper, relation, sessionmaker, relationship
from meta import Base, obj2dict
from datetime import datetime as dt, timedelta as td
import uuid
from meta import session

class DessertType(Base):
    __tablename__ = 'dtype'

    show = {
        'header' : ['Dessert Type Name'],
        'show'   : [('name', 'typename')],
        }
      
    id = Column(Integer, primary_key=True)
    typename = Column(String)

    def __init__(self, typename):
        self.typename = typename

    def __repr__(self):
        return "<DessertType ('%s')>" % (self.typename)
    
    def to_dict(self):
        td = obj2dict(self)
        td['desserts'] = [i.id for i in self.desserts]
        return td

    @staticmethod
    def get(type_id):
        type = session.query(DessertType).filter_by(id=type_id).first()
        return type 

    @staticmethod
    def get_all():
        types = session.query(DessertType).all()
        return types

    @staticmethod
    def get_mul(types_id):
        nodes = ['dtype.id=%s' % i for i in types_id]
        q = ' or '.join(nodes)
        q = '(%s)' % q
        dtype = session.query(DessertType).filter(q).all()
        return dtype

    @staticmethod
    def count(ft=None):
        if not ft:
            return session.query(DessertType).count()
        else:
            return session.query(DessertType).filter(ft).count()
        
    def add(self):
        session.add(self)
        session.commit()

    def delete(self):
        session.delete(self)
        session.commit()

    def update(self, **argv):
        self.typename = argv.get('typename', self.typename)
        session.commit()

class Dessert(Base):
    __tablename__ = 'dessert'

    show = {
        'header' : ['Dessert Name'],
        'show'   : [('name', 'dname')],
        }
      

    id = Column(Integer, primary_key=True)
    dname = Column(String)
    des = Column(String)
    img = Column(String)
    type_id = Column(Integer, ForeignKey('dtype.id'))
    num = Column(Integer)
    price = Column(Integer)

    dessert_type = relation(DessertType, backref='desserts')

    def __init__(self, dessert_name, num=100, price=100):
        self.dname = dessert_name 
        self.img = str(uuid.uuid4())
        self.num = num 
        self.price = price

    def __repr__(self):
        return "<Dessert ('%s')>" % (self.dname)

    def to_dict(self):
        td = obj2dict(self)
        return td

    @staticmethod
    def get(d_id):
        dessert = session.query(Dessert).filter_by(id=d_id).first()
        return dessert

    @staticmethod
    def get_all():
        desserts = session.query(Dessert).all()
        return desserts 

    @staticmethod
    def get_mul(ids):
        nodes = ['dessert.id=%s' % i for i in ids]
        q = ' or '.join(nodes)
        q = '(%s)' % q
        desserts = session.query(Dessert).filter(q).all()
        return desserts

    @staticmethod
    def count(ft=None):
        if not ft:
            return session.query(Dessert).count()
        else:
            return session.query(Dessert).filter(ft).count()
        
    def add(self):
        session.add(self)
        session.commit()

    def delete(self):
        session.delete(self)
        session.commit()

    def update(self, **argv):
        self.dname = argv.get('dessert_name', self.dname)
        self.type_id = argv.get('type', self.type_id)
        self.des = argv.get('des', self.des)
        self.num = argv.get('num', self.num)
        self.price = argv.get('price', self.price)
        session.commit()

