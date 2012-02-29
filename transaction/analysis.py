from models import *

def get_dtype_share():
    ois = OrderItem.get_all()
    render = {}
    for oi in ois:
        name = oi.product.dessert.dessert_type.typename 
        if name in render.keys():
            render[name] += oi.num 
        else:
            render[name] = oi.num 
    s = sum(render.values())
    return {'data':render, 'sum': s}

def set_dtype_share():
    pass
