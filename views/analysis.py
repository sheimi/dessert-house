from start import app, render
from bottle import request, response, redirect
from models import *
from transaction.analysis import *

@app.get('/analysis/chart-nav')
def char_nav():
    return render('analysis/chart_nav.html')()

@app.get('/analysis/overview.js')
def overview():
    render_argv = {
    }
    return render('analysis/overview.js')(**render_argv)

@app.get('/analysis/dt-pie.js')
def dt_pie():
    render_argv = {
        'title'     : 'Dessert Share Chart',
        'datas'     : get_dtype_share(),
    }
    return render('analysis/pie.js')(**render_argv)

@app.get('/analysis/gender-pie.js')
def gender_pie():
    render_argv = {
        'title'     : 'Gender Share Chart',
        'datas'     : get_gender_share(),
    }
    return render('analysis/pie.js')(**render_argv)
