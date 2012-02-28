from sqlalchemy import Column, Integer, String, ForeignKey, Table, Text, DateTime, Boolean
from sqlalchemy.orm import backref, mapper, relation, sessionmaker, relationship
from meta import Base, obj2dict
from datetime import datetime as dt, timedelta as td
import uuid
from meta import session

from models.user import User
from models.product import Product

class Reservation(Base):
    __tablename__ = 'reservation'

    id = Column(Integer, primary_key=True)
    r_time = Column(DateTime)
    o_time = Column(DateTime)
    discount = Column(Integer)
    is_complete = Column(Boolean)
    is_finished = Column(Boolean)
    user_id = Column(Integer, ForeignKey('user.id'))

    user = relation(User, backref='reservations')

    def __init__(self, user, discount=100):
        self.r_time = dt.now()
        self.is_complete = False
        self.is_finished = False
        self.user_id = user
        self.discount = discount

    def __repr__(self):
        return "<Reservateion %d>" % self.id

    def to_dict(self):
        td = obj2dict(self)
        td['r_time'] = str(self.r_time)
        td['o_time'] = str(self.o_time)
        td['total_price'] = self.total_price()
        return td

    @staticmethod
    def get(o_id):
        reservation = session.query(Reservation).filter_by(id=o_id).first()
        return reservation

    @staticmethod
    def get_all():
        reservations = session.query(Reservation).all()
        return reservations

    @staticmethod
    def get_mul(ids):
        nodes = ['reservation.id=%s' % i for i in ids]
        q = ' or '.join(nodes)
        q = '(%s)' % q
        reservations = session.query(Reservation).filter(q).all()
        return reservations

    def add(self):
        session.add(self)
        session.commit()

    def delete(self):
        session.delete(self)
        session.commit()

    def update(self, **argv):
        o_time= argv.get('o_time', None)
        if o_time:
           o_time = [int(x) for x in o_time.split('/')]
           o_time = dt(o_time[2], o_time[0], o_time[1])
        self.user_id = argv.get('user', self.user_id)
        self.is_complete = argv.get('is_complete', self.is_complete)
        self.discount = argv.get('discount', self.discount)
        self.o_time = o_time if o_time else self.o_time 
        session.commit()

    def total_price(self):
        return sum([x.total_price() for x in self.reservation_items])

class ReservationItem(Base):
    __tablename__ = 'reservation_item'

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('product.id'))
    reservation_id = Column(Integer, ForeignKey('reservation.id'))
    num = Column(Integer)

    product = relation(Product, backref='reservation_items')
    reservation = relation(Reservation, backref='reservation_items')

    def __init__(self, num, product, reservation):
        self.num = num
        self.product_id = product
        self.reservation_id = reservation

    def __repr__(self):
        return '<RItem>'

    def to_dict(self):
        td = obj2dict(self)
        td['res_total_price'] = self.reservation.total_price()
        return td

    @staticmethod
    def get(o_id):
        reservation_item = session.query(ReservationItem).filter_by(id=o_id).first()
        return reservation_item

    @staticmethod
    def get_all():
        reservations = session.query(ReservationItem).all()
        return reservations

    @staticmethod
    def get_mul(ids):
        nodes = ['reservation_item.id=%s' % i for i in ids]
        q = ' or '.join(nodes)
        q = '(%s)' % q
        reservations = session.query(ReservationItem).filter(q).all()
        return reservations

    def add(self):
        session.add(self)
        session.commit()

    def delete(self):
        session.delete(self)
        session.commit()

    def update(self, **argv):
        self.num = argv.get('num', self.num)
        self.product_id = argv.get('product', self.product_id)
        self.reservation_id = argv.get('reservation', self.reservation_id)
        print self.id
        session.commit()

    def total_price(self):
        return self.num * self.product.price 
