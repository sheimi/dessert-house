from start import app, render
from bottle import request, response, redirect
from models import *

@app.get('/rest/<m_type>/<m_id>')
def rest_query(m_type, m_id):
    if m_type == 'Reservation':
        m_type = 'Order'
    model = globals()[m_type]
    obj = model.get(m_id)
    m_name = m_type.lower()
    if obj:
        request.result_status['success'] = True
        request.result_status[m_name] = obj.to_dict()
    else:
        request.result_status['success'] = False
        request.result_status['message'] = 'No such %s' % m_name
    return request.result_status


@app.put('/rest/<m_type>/<m_id>')
def rest_update(m_type, m_id):
    if m_type == 'Reservation':
        m_type = 'Order'
    model = globals()[m_type]
    obj = model.get(m_id)
    m_name = m_type.lower()
    if obj:
        json = request.json
        obj.update(**json)
        request.result_status['success'] = True
        request.result_status[m_name]= obj.to_dict()
    else:
        request.result_status['success'] = False
        request.result_status['message'] = 'No such %s' %m_name
    return request.result_status

@app.delete('/rest/<m_type>/<m_id>')
def rest_delete(m_type, m_id):
    if m_type == 'Reservation':
        m_type = 'Order'
    model = globals()[m_type]
    obj = model.get(m_id)
    m_name = m_type.lower()
    if obj:
        obj.delete()
        request.result_status['success'] = True
    else:
        request.result_status['success'] = False
        request.result_status['message'] = 'No such %s' %m_name
    return request.result_status

@app.post('/rest/<m_type>')
def rest_add(m_type):
    if m_type == 'Reservation':
        m_type = 'Order'
    json = request.json
    model = globals()[m_type]
    obj = model(**json)
    m_name = m_type.lower()
    obj.add()
    if obj:
        request.result_status['success'] = True
        request.result_status[m_name]= obj.to_dict()
    else:
        request.result_status['success'] = False
    return request.result_status

