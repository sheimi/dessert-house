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

def get_age_share():
    users = User.get_all()
    render = {'None' : 0}
    for user in users:
        if user.age:
            age = user.age
            group = age / 10 * 10
            group = '%s-%s' % (group, group + 10)
            if group in render.keys():
                render[group] += 1
            else:
                render[group] = 1
        else:
            render['None'] += 1
    return {'data':render}

def get_activate_share():
    users = User.get_all()
    render = {'activated' : 0, 'inactivated' : 0}
    for user in users:
        if user.is_active:
            render['activated'] += 1
        else:
            render['inactivated'] += 1
    return {'data':render}
