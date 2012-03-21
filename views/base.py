from start import app, render
from bottle import request, response, redirect
from transaction.auth import authenticate, register
from util.plugins import signin_required, has_perm
from models import *
from datetime import datetime as dt
from util.util import date2str

@app.get('/ajax/account')
def account_info():
    argv = {
        'user'    :   request.user,
    }
    if request.GET.get("signin", None):
        argv['signin'] = True
    else:
        argv['signin'] = False 
    if request.GET.get("register", None):
        argv['register'] = True
    else:
        argv['register'] = False 
    return render('base/account_info.html')(**argv)

@app.get('/ajax/signin')
def signin_get():
    return render('base/signin.html')()


@app.get('/ajax/register')
def register_get():
    return render('base/register.html')()

@app.post('/ajax/signin')
def signin_post():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    user = authenticate(username, password)
    if user:
        return {"success" : True}
    return {"success" : False}

@app.post('/ajax/register')
def register_post():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    status, info = register(username=username, password=password)
    if not status:
        return {"success": False, "message": info} 
    return {"success" : True}

@app.get('/ajax/signout')
def sign_out():
    s = request.environ.get('beaker.session')
    s.delete()
    return redirect('/')
    return {"success" : True}

@app.get('/ajax/cart')
def user_cart():
    if not request.user:
        return ""
    user = request.user  
    orders = user.orders
    order = [ x for x in orders if not x.is_complete and x.is_order]
    if order:
        order = order[0]
    else:
        order = Order(user.id)
        if user.usertype:
            order.discount = user.usertype.discount
        order.add()
    user.cart = order
    return render('base/cart.html')(user=user, num=len(order.order_items))

@app.get('/ajax/buy/<order_id:int>')
def check_out(order_id):
    user = request.user
    order = Order.get(order_id)
    return render('base/order_confirm.html')(user=user, order=order)

@app.post('/ajax/buy/<order_id:int>')
def check_out_post(order_id):
    order = Order.get(order_id)
    if not order.order_items:
        return { "success": False}
    order.update(is_confirmed=True, confirm_date=date2str(dt.today()))
    return {"success": True}

@app.post('/ajax/item/additem')
def add_item():
    json = request.json
    try:
        dessert = Dessert.get(json['dessert'])
        dessert.num -= json['num']
        dessert.update()
        oi = OrderItem(**json) 
        oi.add()
    except:
        return {"success" : False}
    return {"success" : True}

@app.post('/ajax/item/cnum/<item_id:int>')
def change_num(item_id):
    json = request.json
    if "num" in json:
        oi = OrderItem.get(item_id)
        delta = oi.num - json['num']
        oi.dessert.num -= delta
        oi.num = json['num']
        oi.update()
        return {"success" : True, "orderitem": oi.to_dict()}
    else:
        return {"success" : False}


@app.get('/ajax/reserve')
def user_reserve():
    if not request.user:
        return ""
    user = request.user
    res = user.orders
    res = [ x for x in res if not x.is_confirmed and not x.is_order]
    if res:
        res = res[0]
    else:
        res = Order(user.id, is_order=False)
        if user.usertype:
            res.discount = user.usertype.discount
        res.add()
    user.res = res
    return render('base/reservation.html')(user=user, num=len(res.order_items))


@app.get('/ajax/reserve/<res_id:int>')
def confirm_reserve(res_id):
    user = request.user
    res = Order.get(res_id)
    if res.send_date:
        send_date= date2str(res.send_date)
    else:
        send_date= None
    return render('base/reservation_confirm.html')(
            user=user, res=res, send_date=send_date)

@app.post('/ajax/reserve/<res_id:int>')
def confirm_reserve_post(res_id):
    res = Order.get(res_id)
    if not res.order_items:
        return { "success": False}
    if not res.send_date:
        return { "success": False}
    res.update(is_confirmed=True, confirm_date=date2str(dt.today()))
    return {"success": True}

