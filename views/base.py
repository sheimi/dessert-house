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

@app.route('/ajax/signout')
def sign_out():
    s = request.environ.get('beaker.session')
    s.delete()
    return {"success" : True}

@app.route('/ajax/cart')
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
    print order.is_complete
    if not order.order_items:
        return { "success": False}
    order.update(is_complete=True)
    print order.is_complete
    return {"success": True}
