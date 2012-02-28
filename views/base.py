from start import app, render
from bottle import request, response, redirect
from transaction.auth import authenticate, register
from util.plugins import signin_required, has_perm
from models import *

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
    return {"success" : True}

@app.get('/ajax/cart')
def user_cart():
    if not request.user:
        return ""
    user = request.user  
    orders = user.orders
    order = [ x for x in orders if not x.is_complete]
    if order:
        order = order[0]
    else:
        order = Order(user.id)
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
    order.update(is_complete=True)
    return {"success": True}

@app.get('/ajax/reserve')
def user_reserve():
    if not request.user:
        return ""
    user = request.user
    reservations = user.reservations
    res = [ x for x in reservations if not x.is_complete]
    if res:
        res = res[0]
    else:
        res = Reservation(user.id)
        res.add()
    user.res = res
    return render('base/reservation.html')(user=user, num=len(res.reservation_items))

@app.get('/ajax/reserve/<res_id:int>')
def confirm_reserve(res_id):
    user = request.user
    res = Reservation.get(res_id)
    o_time = res.o_time
    if o_time:
        year, month, day = str(o_time.year), str(o_time.month), str(o_time.day)
        month = month if len(month) == 2 else '0' + month
        day = day if len(day) == 2 else '0' + day
        o_time = '%s/%s/%s' % (month, day, year)
    return render('base/reservation_confirm.html')(user=user, res=res, o_time=o_time)

@app.post('/ajax/reserve/<res_id:int>')
def confirm_reserve_post(res_id):
    res = Reservation.get(res_id)
    if not res.reservation_items:
        return { "success": False}
    if not res.o_time:
        return { "success": False}
    res.update(is_complete=True)
    return {"success": True}

