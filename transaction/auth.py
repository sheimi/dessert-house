from bottle import request, response
from meta import session
from models import User

def authenticate(username, password):
  user = session.query(User).filter_by(username=username, password=password).first()
  if user:
    s = request.environ.get('beaker.session')
    s['user'] = user.id
    return user
  return None

def register(**argv):
  user = session.query(User).filter_by(username=argv["username"]).first()
  if user:
    return False, "username exist"
  user = User(username=argv["username"], password=argv["password"])
  session.add(user)
  session.commit()
  s = request.environ.get('beaker.session')
  s['user'] = user.id
  return True, "success"
