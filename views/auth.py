from start import app, render
from bottle import request, response, redirect
from transaction.auth import authenticate, register
from models import * 

@app.get('/')
def index():
    render_info = {
        'user'          :   request.user,
        'index'         :   True,
    }
    return render('index.html')(**render_info) 

@app.get('/index/dessert/<dessert_id:int>')
def index_item(dessert_id):
    render_info = {
        'user'    :   request.user,
        'dessert' :   Dessert.get(dessert_id),
    }
    return render('core/dessert_item.html')(**render_info)

@app.get('/index/dessert_list')
def index_item_list():
    desserts = Dessert.get_all()
    render_info = {
        'user'    :   request.user,
        'dessert_list' : desserts, 
    }
    return render('core/dessert_list.html')(**render_info) 

@app.get('/index/dessert_rec_list')
def index_rec_list():
    render_info = {
        'user'    :   request.user,
        'rec_list' : Dessert.get_all(),
    }
    return render('core/dessert_rec_list.html')(**render_info) 

@app.post('/index/dessert/<dessert_id:int>/buy')
def index(dessert_id):
    json = request.json
    num = json['num']
    dessert = Dessert.get(dessert_id)
    order = Order(request.user.id)


@app.get('/signin')
def sign_in_get():
    return render('signin.html')(signin=True)

@app.post('/signin')
def sign_in_post():
    username = request.forms.get('username')
    password = request.forms.get('password')
    user = authenticate(username, password)
    if user:
        redirect('/')
    return render('signin.html')(error="Wrong username or password") 

@app.get('/register')
def register_get():
    return render('register.html')(register=True)

@app.post('/register')
def register_post():
    username = request.forms.get('username')
    password = request.forms.get('password')
    passwordr = request.forms.get('passwordr')
    if password != passwordr:
        return render('register.html')(register=True, error="password error")
    status, info = register(username=username, password=password)
    if not status:
        return render('register.html')(regisetr=True, error=info)
    redirect('/')


@app.route('/signout')
def sign_out():
    s = request.environ.get('beaker.session')
    s.delete()
    redirect('/')
