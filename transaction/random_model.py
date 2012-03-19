from models import *
import random
import string
from datetime import datetime as dt
from util import util

def random_img():
    img = [ '13569b64-b9e3-4c3a-8a1d-5f794a723d8c',
            '83289d63-b49b-4d70-b47a-08d43cdd940e',
            'adc15f11-3f8c-4e33-aba3-a199d2d47da9',
            '3426bba5-03e2-4c46-bbd3-dfc7afdbe372',
            '4ddc429e-c202-4fbe-8481-59738bc29a88',
            '359e9e89-a6f9-44ca-bbef-46e49a490d5a',
            '59465deb-26e8-493c-ba40-5c4b96362594',
            '59e46ac2-0193-4f57-ae10-3c00a1bf2d3b',
            'c549125d-0f4f-417a-9813-7ea208573681',
            '2c70a62e-a09c-4b55-906b-ba7f4bba04e8',]
    return random.choice(img) 

def random_name(bit, bit_min = 0, min_l = 2, max_l = 6):
    for b in range(bit_min, bit):
        yield ''.join(random.choice(string.ascii_letters) for x in range(random.randint(min_l, max_l))) 


def random_dtype():
    pass

def random_dessert():
    dts = DessertType.get_all()
    dt = random.choice(dts).id
    name = ' '.join(random_name(2))
    des = ' '.join(random_name(20))
    img = random_img()
    d = Dessert(name)
    d.des = des
    d.img = img
    d.type_id = dt
    d.num = random.randint(50, 100)
    d.price = random.randint(20, 100)
    d.add()
    return d

def random_address():
    address_pool = ['Gulou', 'Qixia', 'XuanWu', 'Jiangling', 'Pukou']
    return random.choice(address_pool)

def random_utype():
    pass

def random_user():
    uts = UserType.get_all()
    ut = random.choice(uts).id
    username = ' '.join(random_name(2))
    password = 'zhang'
    is_active = random.choice([True, False])
    age = random.randint(10, 100)
    gender = random.randint(0, 3)
    email = '@'.join(random_name(2)) + '.com'
    address = random_address()
    u = User(username, password)
    u.is_active = is_active
    u.age = age
    u.gender = gender
    u.email = email
    u.address = address
    u.roles.append(Role.get(2))
    u.add()
    return u


from datetime import datetime, timedelta

def daterange(start_date, end_date):
    for n in range((end_date - start_date).days):
        yield start_date + timedelta(n)

def random_order(single_date, min_item=1, max_item=20):

    desserts = Dessert.get_all()
    user = random.choice(User.get_all()).id
    order = Order(user)
    order.add()
    for i in range(random.randint(min_item, max_item)):
        d = random.choice(desserts)
        oi = OrderItem(random.randint(1, 30), d.id, order.id, d.price)
        oi.add()
    order.update(is_confirmed=True, confirm_date=util.date2str(single_date))
    return order

def random_res(single_date, min_item=1, max_item=20):
    desserts = Dessert.get_all()
    user = random.choice(User.get_all()).id
    order = Order(user, is_order=False)
    order.add()
    for i in range(random.randint(min_item, max_item)):
        d = random.choice(desserts)
        oi = OrderItem(random.randint(1, 30), d.id, order.id, d.price)
        oi.add()
    order.update(is_confirmed=True, confirm_date=util.date2str(single_date), is_complete=True, send_date=util.date2str(single_date))
    return order

def random_order_g():
    start_date = dt(2012, 1, 1) 
    end_date = dt(2012, 3, 19)
    for i, single_date in enumerate(daterange(start_date, end_date)):
        for num in range(random.randint(i+20, i+40)): 
            random_order(single_date)
        for num in range(random.randint(i+10, i+40)): 
            random_res(single_date)
        print single_date


