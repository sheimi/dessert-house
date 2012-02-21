from start import app, render
from bottle import request, response, redirect
from models import User, Role 

@app.delete('/rest/User/<user_id>/deactivate')
def user_deactivate(user_id):
  user = User.get_by_id(user_id)
  if user:
    user.deactivate()
    request.result_status['success'] = True
  else:
    request.result_status['success'] = False
    request.result_status['message'] = 'No such user'
  return request.result_status

@app.post('/rest/User/<user_id>/activate')
def user_activate(user_id):
  user = User.get_by_id(user_id)
  if user:
    user.activate()
    request.result_status['success'] = True
    request.result_status['user'] = user.to_dict()
  else:
    request.result_status['success'] = False
    request.result_status['message'] = 'No such user'
  return request.result_status
