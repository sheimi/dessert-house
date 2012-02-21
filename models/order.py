from sqlalchemy import Column, Integer, String, ForeignKey, Table, Text, DateTime, Boolean
from sqlalchemy.orm import backref, mapper, relation, sessionmaker, relationship
from meta import Base, obj2dict
from datetime import datetime as dt, timedelta as td
import uuid
from meta import session

from models.user import User
from models.product import Product

class Order(Base):
    __tablename__ = 'order'

    id = Column(Integer, primary_key=True)
    o_time = Column(DateTime)
    user_id = Column(Integer, ForeignKey('user.id'))
    discount = Column(Integer)

    user = relation(User, backref='orders')

    def __init__(self, user, discount=100):
        self.o_time = dt.now()
        self.user_id = user
        self.discount = discount

    def __repr__(self):
        return "<Order %d>" % self.id

    def to_dict(self):
        td = obj2dict(self)
        td['o_time'] = str(self.o_time)
        return td

    @staticmethod
    def get(o_id):
        order = session.query(Order).filter_by(id=o_id).first()
        return order

    @staticmethod
    def get_all():
        orders = session.query(Order).all()
        return orders

    @staticmethod
    def get_mul(ids):
        nodes = ['order.id=%s' % i for i in ids]
        q = ' or '.join(nodes)
        q = '(%s)' % q
        orders = session.query(Order).filter(q).all()
        return orders

    def add(self):
        session.add(self)
        session.commit()

    def delete(self):
        session.delete(self)

    def update(self, **argv):
        self.user_id = argv.get('user', self.user_id)
        self.discount = argv.get('discount', self.discount)
        session.commit()


class OrderItem(Base):
    __tablename__ = 'order_item'

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('product.id'))
    order_id = Column(Integer, ForeignKey('order.id'))
    num = Column(Integer)

    product = relation(Product, backref='order_items')
    order = relation(Order, backref='order_items')

    def __init__(self, num, product, order):
        self.num = num
        self.product_id = product
        self.order_id = order

    def __repr__(self):
        return '<RItem>'

    def to_dict(self):
        td = obj2dict(self)
        return td

    @staticmethod
    def get(o_id):
        order_item = session.query(OrderItem).filter_by(id=o_id).first()
        return order_item

    @staticmethod
    def get_all():
        order_items = session.query(OrderItem).all()
        return order_items 

    @staticmethod
    def get_mul(ids):
        nodes = ['order_item.id=%s' % i for i in ids]
        q = ' or '.join(nodes)
        q = '(%s)' % q
        order_items = session.query(OrderItem).filter(q).all()
        return order_items 

    def add(self):
        session.add(self)
        session.commit()

    def delete(self):
        session.delete(self)

    def update(self, **argv):
        self.num = argv.get('num', self.num)
        self.product_id= argv.get('product', self.product_id)
        self.order_id = argv.get('order', self.order_id)
        session.commit()

