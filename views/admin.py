from start import app, render
from bottle import request, response, redirect
from transaction.auth import authenticate, register
from util.plugins import signin_required, has_perm
from models import *

@app.get('/admin')
@app.get('/admin/index')
@has_perm('can_view_admin')
def index_admin():
    render_argv = {
        'user'  : request.user,
        'member_center' : True,
        'admin_index': True,
    }
    return render('admin/index.html')(**render_argv)


@app.get('/admin/user/<user_id:int>')
@has_perm('can_view_admin')
def user_item(user_id):
    u = User.get_by_id(user_id)
    roles = Role.get_all()
    render_argv = {
        'user'  : u,
        'roles' : roles,
        'type_list' : UserType.get_all(),
    }
    return render('admin/user/item-detail.html')(**render_argv)

@app.get('/admin/user/table')
def user_table():
    start = request.GET.get('start', 0);
    end = request.GET.get('end', 20);
    user_list = User.get_mul(range(start, end))
    render_argv = {
        'user_list' : user_list,
    }
    return render('admin/user/item-table.html')(**render_argv)


@app.get('/admin/role/<role_id:int>')
@has_perm('can_view_admin')
def role_item(role_id):
    role = Role.get(role_id)
    perms = Permission.get_all()
    render_argv = {
        'role'  : role,
        'perms' : perms,
    }
    return render('admin/role/item-detail.html')(**render_argv)

@app.get('/admin/type/<type_id:int>')
@has_perm('can_view_admin')
def type_item(type_id):
    usertype = UserType.get(type_id)
    render_argv = {
        'type' : usertype,
    }
    return render('admin/type/item-detail.html')(**render_argv)


@app.get('/admin/perm/<perm_id:int>')
@has_perm('can_view_admin')
def perm_item(perm_id):
    perm = Permission.get(perm_id)
    render_argv = {
        'perm' : perm,
    }
    return render('admin/perm/item-detail.html')(**render_argv)

@app.get('/admin/dessert/<dessert_id:int>')
@has_perm('can_view_admin')
def dessert_item(dessert_id):
    render_argv = {
        'dessert' : Dessert.get(dessert_id),
        'type_list' : DessertType.get_all(),
    }
    return render('admin/dessert/item-detail.html')(**render_argv)

@app.get('/admin/dtype/<dtype_id:int>')
@has_perm('can_view_admin')
def dtype_item(dtype_id):
    render_argv = {
        'type' : DessertType.get(dtype_id),
    }
    return render('admin/dtype/item-detail.html')(**render_argv)

@app.get('/admin/product/<product_id:int>')
@has_perm('can_view_admin')
def product_item(product_id):
    render_argv = {
        'product' : Product.get(product_id),
        'dessert_list' : Dessert.get_all(),
    }
    return render('admin/product/item-detail.html')(**render_argv)


@app.get('/admin/product/table')
@has_perm('can_view_admin')
def product_table():
    start = request.GET.get('start', 0);
    end = request.GET.get('end', 20);
    product_list = Product.get_mul(range(start, end))
    render_argv = {
        'product_list' : product_list,
    }
    return render('admin/product/item-table.html')(**render_argv)


@app.get('/admin/dessert/table')
@has_perm('can_view_admin')
def dessert_table():
    start = request.GET.get('start', 0);
    end = request.GET.get('end', 20);
    dessert_list = Dessert.get_mul(range(start, end))
    render_argv = {
        'dessert_list' : dessert_list,
    }
    return render('admin/dessert/item-table.html')(**render_argv)


@app.get('/admin/<module>/add')
@has_perm('can_view_admin')
def item_add(module):
    render_argv = {
        'dessert_list' : Dessert.get_all(),
    }
    return render('admin/%s/item-add.html' % module)(**render_argv)

@app.get('/admin/<module>')
@has_perm('can_view_admin')
def item_admin(module):
    render_argv = {
        'user'            : request.user,
        'admin_' + module : True,
        'module'          : module,
        'module_l'        : modules[module],
    }
    return render('admin/item_admin_index.html')(**render_argv)



@app.get('/admin/<module>/table')
@has_perm('can_view_admin')
def item_table(module):
    start = request.GET.get('start', 0);
    end = request.GET.get('end', 20);
    obj = globals()[modules[module]]
    item_list= obj.get_mul(range(start, end))
    render_argv = {
        'item_list' : item_list,
        'table_show': obj.show,
        'module'    : module,
    }
    return render('admin/item_table.html')(**render_argv)
