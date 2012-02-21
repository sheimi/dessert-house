from bottle import request, response, redirect
from meta import Session
from models import User

def set_user(callback):
  def wrapper(*args, **kawrgs):
    s = request.environ.get('beaker.session')
    user_id = s.get('user', 0)
    if user_id:
      session = Session()
      user = session.query(User).filter_by(id=user_id).first()
      request.user = user
    else:
      request.user = None
    request.result_status = {}
    body = callback(*args, **kawrgs)
    return body
  return wrapper

from start import settings
from functools import wraps

REDIRECT_URL = settings['signin_url']

def user_passes_test(test_func, redirect_url=REDIRECT_URL):
  """ 
  Decorator for views that checks that the user passes the given test,
  redirecting to the log-in page if necessary. The test should be a callable
  that takes the user object and returns True if the user passes.
  """

  def decorator(func):
    @wraps(func)
    def _wrapped_view(*args, **kwargs):
      if test_func(request.user):
        return func(*args, **kwargs)
      redirect(redirect_url)
    return _wrapped_view
  return decorator

def signin_required(func, login_url=REDIRECT_URL):
  act_dec = user_passes_test(
      lambda u: u != None,
      login_url,
      )
  return act_dec(func)

def has_perm(perm, redirect_url=REDIRECT_URL):
  def _has_perm(func, redirect=redirect_url):
    act_dec = user_passes_test(
        lambda u: u != None and u.has_perm(perm),
        redirect_url,
        )
    return act_dec(func)
  return _has_perm
