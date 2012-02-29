from start import app, render
from bottle import request, response, redirect
from models import *
from transaction.analysis import *

@app.get('/analysis/overview')
def overview():
    render_argv = {
    }
    return render('analysis/overview.html')(**render_argv)

@app.get('/analysis/dt-pie')
def dt_pie():
    render_argv = {
        'datas'     : get_dtype_share(),
    }
    print render_argv
    return render('analysis/dt_pie.html')(**render_argv)
