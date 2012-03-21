from models import *
from numpy import *
from scipy.optimize import leastsq


def cal_linear(result):

    def line(p, y, x):
        def func(x, p):
            a, b = p
            return a * x + b
        return y - func(x, p)

    def line_func(a, b):
        return lambda x: a * x + b

    size = len(result)
    x, y = zip(*enumerate(result))
    x, y = x[:-1], y[:-1]
    y = [i[1]['num'] for  i in y]
    x, y = array(x), array(y)
    r, null = leastsq(line, (0, 0), args=(y, x))
    func = line_func(r[0], r[1])
    return [[0, func(0)], [size, func(size)]]



def get_month(month):
    month_list = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                  'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    return month_list[month-1]


def get_order_line_month(order_type=None):
    orders = Order.get_all(order_type=order_type)
    render = {} 
    for order in orders:
        if not order.confirm_date:
            continue
        month = order.confirm_date.month
        if month in render.keys():
            render[month]['num'] += 1 
        else:
            render[month] = {
                'key' :   get_month(month),
                'num'   :   1,
            }
    so = render.items()
    result = sorted(so, key=lambda a: a[0])
    render = {
        "linear" : cal_linear(result),
        "result" : result,
    }
    return render 
    
def get_order_line_day(order_type=None, delta=3):
    orders = Order.get_all(order_type=order_type)
    render = {} 
    for order in orders:
        if not order.confirm_date:
            continue
        month = order.confirm_date.month
        day = order.confirm_date.day
        key = month * 40 + day / delta 
        if key in render.keys():
            render[key]['num'] += 1 
        else:
            render[key] = {
                'key'   :   "%s %d" % (get_month(month), day),
                'num'   :   1,
            }
    so = render.items()
    result = sorted(so, key=lambda a: a[0])
    render = {
        "linear" : cal_linear(result),
        "result" : result,
    }
    return render 
    

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
        if user.age and user.age != 'None':
            age = user.age
            group = age / 10 * 10
            group = '%d-%d' % (group, group + 10)
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

def get_address_share():
    users = User.get_all()
    render = {}
    for user in users:
        address = user.address
        if not address:
            continue
        if address in render.keys():
            render[address] += 1
        else:
            render[address] = 1
    return {'data':render}

