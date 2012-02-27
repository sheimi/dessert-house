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

    dessert_type = relation(DessertType, backref='desserts')

    def __init__(self, dessert_name):
        self.dname = dessert_name 
        self.img = str(uuid.uuid4())

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
        session.commit()

class Product(Base):
    __tablename__ = 'product'

    show = {
        'header' : ['Dessert Name'],
        'show'   : [('name', 'dname')],
        }
      
    id = Column(Integer, primary_key=True)
    dessert_id = Column(Integer, ForeignKey('dessert.id'))
    date = Column(DateTime)
    num = Column(Integer)
    price = Column(Integer)

    dessert = relation(Dessert, backref='products')

    def __init__(self, num, price, dessert):
        self.date = dt.now()
        self.num = num
        self.price = price
        self.dessert_id = dessert

    def __repr__(self):
        return "<Product of (%s)" % (self.dessert.dname)

    def to_dict(self):
        td = obj2dict(self)
        td['date'] = str(self.date)
        return td

    @staticmethod
    def get(p_id):
        product = session.query(Product).filter_by(id=p_id).first()
        return product

    @staticmethod
    def get_all():
        products = session.query(Product).all()
        return products

    @staticmethod
    def get_mul(ids):
        nodes = ['product.id=%s' % i for i in ids]
        q = ' or '.join(nodes)
        q = '(%s)' % q
        products = session.query(Product).filter(q).all()
        return products

    def add(self):
        session.add(self)
        session.commit()

    def delete(self):
        session.delete(self)
        session.commit()

    def update(self, **argv):
        self.num = argv.get('num', self.num)
        self.price = argv.get('price', self.price)
        self.dessert_id = argv.get('dessert', self.dessert)
        session.commit()
