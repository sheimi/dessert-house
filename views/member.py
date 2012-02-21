from start import app, render
from bottle import request, response, redirect
from transaction.auth import authenticate, register
from util.plugins import signin_required, has_perm

@app.get('/member')
@app.get('/member/index')
@signin_required
def member_center():
  render_argv = {
    'user'  : request.user,
    'member_center' : True,
  }
  return render('member/index.html')(**render_argv)


@app.post('/member/profile/img')
def up_load_image():
  datafile = request.POST.get('file')
  with open('./static/img/profile/%d.png' % request.user.id, 'w') as f :
    f.write(datafile.file.read())
  return {"result": "success"} 

@app.post('/admin/dessert/upload/<dessert_id:int>')
def upload_dessert_image(dessert_id):
  from models import Dessert
  datafile = request.POST.get('file')
  with open('./static/img/dessert/%s.png' % Dessert.get(dessert_id).img, 'w') as f :
    f.write(datafile.file.read())
  return {"result": "success"} 
