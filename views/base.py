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
