import sqlalchemy as sa
from sqlalchemy import orm

import meta
#from models.member import * 

from models.other_tables import *
from models.user import User
from models.usertype import UserType
from models.role import Role
from models.perm import Permission
from models.order import Order, OrderItem
from models.dessert import Dessert, DessertType 
from models.decision import Decision

def init_model(engine):
  """Call me before using any of the tables or classes in the model"""
  meta.Session.configure(bind=engine)
  meta.engine = engine

modules = {
    'decision'      :       'Decision',
    'user'          :       'User',
    'type'          :       'UserType',
    'role'          :       'Role',
    'perm'          :       'Permission',
    'order'         :       'Order',
    'order_item'    :       'OrderItem',
    'dessert'       :       'Dessert',
    'dtype'         :       'DessertType',
}
