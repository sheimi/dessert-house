from start import app, render
from bottle import request, response, redirect
from models import *
from transaction.analysis import *

@app.get('/analysis/tooltip')
def tooltip():
    return render('analysis/tooltip.html')()

@app.get('/analysis/overview.js')
def overview():
    render_argv = {
    }
    return render('analysis/overview.js')(**render_argv)

@app.get('/analysis/dt-pie.js')
def dt_pie():
    render_argv = {
        'datas'     : get_dtype_share(),
    }
    return render('analysis/dt_pie.js')(**render_argv)
