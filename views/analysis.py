from start import app, render
from bottle import request, response, redirect
from models import *
from transaction.analysis import *

@app.get('/analysis/chart-nav')
def char_nav():
    return render('analysis/chart_nav.html')()

@app.get('/analysis/overview.js')
def overview():
    return render('analysis/overview.js')()

@app.get('/analysis/order-month-line.js')
def order_month_line():
    return render('analysis/line.js')(title='Order Line', items=get_order_line_month())

@app.get('/analysis/order-day-line.js')
def order_day_line():
    return render('analysis/line.js')(title='Order Day Line', items=get_order_line_day())

@app.get('/analysis/res-month-line.js')
def res_month_line():
    return render('analysis/line.js')(title='Reservation Line', items=get_order_line_month('reservation'))

@app.get('/analysis/res-day-line.js')
def res_day_line():
    return render('analysis/line.js')(title='Reservation Day Line', items=get_order_line_day('reservation'))

@app.get('/analysis/dt-pie.js')
def dt_pie():
    render_argv = {
        'title'     : 'Dessert Type Share Chart',
        'datas'     : get_dtype_share(),
    }
    return render('analysis/pie.js')(**render_argv)

@app.get('/analysis/dst-pie.js')
def dst_pie():
    render_argv = {
        'title'     : 'Dessert Share Chart',
        'datas'     : get_dessert_share(),
    }
    return render('analysis/pie.js')(**render_argv)

@app.get('/analysis/gender-pie.js')
def gender_pie():
    render_argv = {
        'title'     : 'Gender Share Chart',
        'datas'     : get_gender_share(),
    }
    return render('analysis/pie.js')(**render_argv)

@app.get('/analysis/age-pie.js')
def age_pie():
    render_argv = {
        'title'     : 'Age Share Chart',
        'datas'     : get_age_share(),
    }
    return render('analysis/pie.js')(**render_argv)

@app.get('/analysis/activate-pie.js')
def activate_pie():
    render_argv = {
        'title'     : 'Activate Share Chart',
        'datas'     : get_activate_share(),
    }
    return render('analysis/pie.js')(**render_argv)


@app.get('/analysis/address-pie.js')
def address_pie():
    render_argv = {
        'title'     : 'Address Share Chart',
        'datas'     : get_address_share(),
    }
    return render('analysis/pie.js')(**render_argv)


