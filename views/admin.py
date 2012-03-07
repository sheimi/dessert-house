from start import app, render
from bottle import request, response, redirect
from transaction.auth import authenticate, register
from util.plugins import signin_required, has_perm
from models import *

table_count = 10 

@app.get('/admin')
@app.get('/admin/index')
@has_perm('can_view_admin')
def index_admin():
    render_argv = {
        'user'  : request.user,
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
    page = int(request.GET.get('page', '0'))
    start = page * table_count + 1
    end = (page + 1) * table_count + 1
    user_list = User.get_mul(range(start, end))
    render_argv = {
        'user_list' : user_list,
        'page' : page,
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

@app.get('/admin/dessert/table')
@has_perm('can_view_admin')
def dessert_table():
    page = int(request.GET.get('page', '0'))
    start = page * table_count + 1
    end = (page + 1) * table_count + 1
    dessert_list = Dessert.get_mul(range(start, end))
    render_argv = {
        'dessert_list' : dessert_list,
        'page'      : page,
    }
    return render('admin/dessert/item-table.html')(**render_argv)


@app.get('/admin/order')
@has_perm('can_view_admin')
def order_admin_index():
    render_argv = {
        'user' : request.user,
        'admin_order' : True,
    }
    return render('admin/order/index.html')(**render_argv)

@app.get('/admin/order/table')
def order_table():
    page = int(request.GET.get('page', '0'))
    start = page * table_count + 1
    end = (page + 1) * table_count + 1
    item_list= Order.get_mul(range(start, end))
    render_argv = {
        'orders' : item_list,
        'page'      : page,
    }
    return render('admin/order/order_list.html')(**render_argv)

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
    page = int(request.GET.get('page', '0'))
    start = page * table_count + 1
    end = (page + 1) * table_count + 1
    obj = globals()[modules[module]]
    item_list= obj.get_mul(range(start, end))
    render_argv = {
        'item_list' : item_list,
        'table_show': obj.show,
        'module'    : module,
        'page'      : page,
    }
    return render('admin/item_table.html')(**render_argv)


@app.get('/admin/<module>/pagination')
def item_pagination(module):
    obj = globals()[modules[module]]

    page = int(request.GET.get('page', '0'))
    count = obj.count()
    page_max = count / table_count
    if page_max != 0 and count % table_count == 0:
        page_max = page_max - 1
    if page <= 5 and page_max > 9:
        pages = range(0, 10)
    elif page <= 5 and page_max <= 9:
        pages = range(0, page_max + 1)
    elif page >= 5 and page_max < page + 5:
        pages = range(page_max - 9, page_max + 1)
    else:
        pages = range(page - 5, page + 5)
    render_argv = {
        'page' : page,
        'pages': pages,
        'page_max': page_max,
        'module'    : module,
    }
    return render('admin/table_pagination.html')(**render_argv)
    
