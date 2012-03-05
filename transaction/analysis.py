from models import *

def get_dtype_share():
    ois = OrderItem.get_all()
    render = {}
    for oi in ois:
        name = oi.dessert.dessert_type.typename 
        if name in render.keys():
            render[name] += oi.num 
        else:
            render[name] = oi.num 
    return {'data':render}

def get_dessert_share():
    ois = OrderItem.get_all()
    render = {}
    for oi in ois:
        name = oi.dessert.dname
        if name in render.keys():
            render[name] += oi.num 
        else:
            render[name] = oi.num 
    return {'data':render}


def set_dtype_share():
    pass

def get_gender_share():
    users = User.get_all()
    render = {'male': 0, 'female':0, 'others':0}
    for user in users:
        gender = user.gender
        if gender == 1:
            render['male'] += 1
        elif gender == 2:
            render['female'] += 1
        else:
            render['others'] += 1
    return {'data':render}
