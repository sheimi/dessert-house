#!/usr/bin/env python
import bottle
from bottle import route, static_file
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from jinja2 import Environment, FileSystemLoader
from beaker.middleware import SessionMiddleware
from models import * 

#the app

settings = {
    'signin_url' : '/signin',
}

session_opts = {
    'session.type': 'file',
    'session.cookie_expires': 30000,
    'session.data_dir': './data',
    'session.auto': True
}
app = bottle.app()
sapp = SessionMiddleware(app, session_opts)


def render(template):
    env = Environment(loader=FileSystemLoader('templates'))
    return env.get_template(template).render

#the start functions

def syncdb():
    from meta import Base, engine, Session 
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    #init data base
    #init perm
    perm_admin = Permission('can_view_admin')
    #init role
    role_admin = Role('admin')
    role_mem = Role('member')
    #init type
    utypea = UserType('memberA', 95, 100)
    utypeb = UserType('memberB', 90, 150)
    utypec = UserType('memberC', 85, 200)
    #init user
    user = User('sheimi', 'zhang')
    nuser = User('shaymin', 'zhang')
    session = Session()
    session.add_all([role_admin, role_mem, user, nuser])
    session.commit()
    #config relation
    role_admin.perms.append(perm_admin)
    user.roles.append(role_admin)
    nuser.roles.append(role_mem)
    nuser.usertype = utypea
    session.commit()
  

def testdb():
    from models import member
    from meta import Session
    Session.query(member.User).all()

def run():
    from views import auth, user, rest, member, admin, base
    from util.plugins import set_user
    from bottle import install 

    @route('/static/<path:path>', name='static')
    def static_files(path):
        return static_file(path, root='./static/')
    @route('/favicon.ico', name='static')
    def favicon():
        return static_file('img/favicon.png', root='./static/')

    bottle.install(set_user)
    bottle.debug(True)
    bottle.run(app=sapp, reloader=True, server='tornado', host='0.0.0.0', port=8080)

if __name__ == '__main__':
    import sys
    try:
        cmd = sys.argv[1]
        globals()[cmd]()
    except:
        run()
  
