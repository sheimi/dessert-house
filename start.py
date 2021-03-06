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
    perm_admin_edit = Permission('can_edit_admin')
    perm_leader = Permission('can_decide')
    #init role
    role_admin = Role('admin')
    role_mem = Role('member')
    role_leader = Role('leader')
    #init type
    utypea = UserType('memberA', 95, 100)
    utypeb = UserType('memberB', 90, 150)
    utypec = UserType('memberC', 85, 200)
    #init user
    user = User('sheimi', 'zhang')
    nuser = User('shaymin', 'zhang')
    session = Session()
    session.add_all([role_admin, role_mem, role_leader, user, nuser])
    session.commit()
    #config relation
    role_admin.perms.append(perm_admin)
    role_leader.perms.append(perm_leader)
    role_leader.perms.append(perm_admin)
    role_admin.perms.append(perm_admin_edit)
    user.roles.append(role_admin)
    nuser.roles.append(role_leader)
    nuser.usertype = utypea
    session.commit()
    
    dt1 = DessertType('Cake')
    dt2 = DessertType('Ice Cream')
    dt3 = DessertType('Fruit')
    session.add_all([dt1, dt2, dt3])
    session.commit()

    d0 = Dessert('Goblet')
    d1 = Dessert('Lemon')
    d2 = Dessert('Buttermilk')
    d3 = Dessert('Chocolate')
    d4 = Dessert('Fruit')
    d5 = Dessert('Valentine')
    d6 = Dessert('Lemon Cake')
    d7 = Dessert('Exotic Fruits')
    d8 = Dessert('Fresh Fruit')
    d9 = Dessert('Chocolate Ice')

    d0.des, d0.type_id = 'This is Description ~~~~~~~', 2
    d1.des, d1.type_id = 'This is Description ~~~~~~~', 3
    d2.des, d2.type_id = 'This is Description ~~~~~~~', 1
    d3.des, d3.type_id = 'This is Description ~~~~~~~', 1
    d4.des, d4.type_id = 'This is Description ~~~~~~~', 3
    d5.des, d5.type_id = 'This is Description ~~~~~~~', 1
    d6.des, d6.type_id = 'This is Description ~~~~~~~', 1
    d7.des, d7.type_id = 'This is Description ~~~~~~~', 3
    d8.des, d8.type_id = 'This is Description ~~~~~~~', 3
    d9.des, d9.type_id = 'This is Description ~~~~~~~', 2

    d0.img = '13569b64-b9e3-4c3a-8a1d-5f794a723d8c'
    d1.img = '83289d63-b49b-4d70-b47a-08d43cdd940e'
    d2.img = 'adc15f11-3f8c-4e33-aba3-a199d2d47da9'
    d3.img = '3426bba5-03e2-4c46-bbd3-dfc7afdbe372'
    d4.img = '4ddc429e-c202-4fbe-8481-59738bc29a88'
    d5.img = '359e9e89-a6f9-44ca-bbef-46e49a490d5a'
    d6.img = '59465deb-26e8-493c-ba40-5c4b96362594'
    d7.img = '59e46ac2-0193-4f57-ae10-3c00a1bf2d3b'
    d8.img = 'c549125d-0f4f-417a-9813-7ea208573681'
    d9.img = '2c70a62e-a09c-4b55-906b-ba7f4bba04e8'
    
    session.add_all([d0, d1, d2, d3, d4, d5, d6, d7, d8, d9])
    session.commit()
    decision = Decision(content="test", title="title")
    decision.add()

    d = Dessert.get_all()

def testdb():
    from models import member
    from meta import Session
    Session.query(member.User).all()

def runserver():
    from views import auth, user, rest, member, admin, base, analysis
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
    bottle.run(app=sapp, reloader=True, host='0.0.0.0', port=8080)

def random_data():
    from transaction import random_model as rd
    for i in range(30):
        rd.random_dessert()
    print "finished"
    for i in range(100):
        rd.random_user()
    print "finished"
    rd.random_order_g()
    print "finished"

if __name__ == '__main__':
    #syncdb()
    #random_data()
    runserver()
  
