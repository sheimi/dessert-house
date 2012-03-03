from sqlalchemy import Column, Integer, String, ForeignKey, Table, Text, DateTime, Boolean
from sqlalchemy.orm import backref, mapper, relation, sessionmaker, relationship
from meta import Base, obj2dict
from datetime import datetime as dt, timedelta as td
import uuid
from meta import session

from models.user import User
from models.product import Product
from util.util import str2date 

class Order(Base):
    __tablename__ = 'order'

    id = Column(Integer, primary_key=True)

    create_date  = Column(DateTime)     #date the order created
    confirm_date = Column(DateTime)     #date the order confirmed 
    send_date    = Column(DateTime)     #date the order will be sent

    user_id = Column(Integer, ForeignKey('user.id'))
    discount = Column(Integer)

    is_order     = Column(Boolean)      #order: true   reservation: false
    is_confirmed = Column(Boolean)      #is confirmed
    is_complete  = Column(Boolean)      #is the order conplete


    user = relation(User, backref='orders')

    def __init__(self, user, discount=100, is_order=True):

        self.create_date = dt.now()

        self.user_id = user
        self.discount = discount

        self.is_order       = is_order
        self.is_complete    = False
        self.is_confirmed   = False

    def __repr__(self):
        return "<Order %d>" % self.id

    def to_dict(self):
        td = obj2dict(self)
        td['create_date']   = str(self.create_date)
        td['confirm_date']  = str(self.confirm_date)
        td['send_date']     = str(self.send_date)
        td['total_price'] = self.total_price()
        return td

    @staticmethod
    def get(o_id):
        order = session.query(Order).filter_by(id=o_id).first()
        return order

    @staticmethod
    def get_all(order_type=None):
        if order_type == 'order':
            order = session.query(Order).filter(is_order=True).all()
        elif order_type == 'reservation':
            reservation = session.query(Order).filter(is_order=False).all()
        else:
            orders = session.query(Order).all()
        return orders

    @staticmethod
    def get_mul(ids):
        nodes = ['order.id=%s' % i for i in ids]
        q = ' or '.join(nodes)
        q = '(%s)' % q
        orders = session.query(Order).filter(q).all()
        return orders

    @staticmethod
    def count(ft=None):
        if not ft:
            return session.query(Order).count()
        else:
            return session.query(Order).filter(ft).count()

    def add(self):
        session.add(self)
        session.commit()

    def delete(self):
        session.delete(self)
        session.commit()

    def update(self, **argv):

        self.user_id        = argv.get('user', self.user_id)
        self.discount       = argv.get('discount', self.discount)

        self.is_complete    = argv.get('is_complete', self.is_complete)
        self.is_order       = argv.get('is_order', self.is_order) 
        self.is_confirmed   = argv.get('is_confirmed', self.is_confirmed)

        confirm_date = argv.get('confirm_date', None)
        send_date    = argv.get('send_date', None)   
        if send_date:
            self.send_date = str2date(send_date)
        if confirm_date:
            self.confirm_date = str2date(confirm_date)
            if self.is_order:
                self.send_date = self.confirm_date
                self.is_complete = self.is_confirmed
        session.commit()

    def total_price(self):
        return sum([x.total_price() for x in self.order_items])


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
        td['order_total_price'] = self.order.total_price() 
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

    @staticmethod
    def count(ft=None):
        if not ft:
            return session.query(OrderItem).count()
        else:
            return session.query(OrderItem).filter(ft).count()


    def add(self):
        session.add(self)
        session.commit()

    def delete(self):
        session.delete(self)
        session.commit()

    def update(self, **argv):
        self.num = argv.get('num', self.num)
        self.product_id= argv.get('product', self.product_id)
        self.order_id = argv.get('order', self.order_id)
        session.commit()

    def total_price(self):
        return self.num * self.product.price
