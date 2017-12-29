#!/usr/bin/python
from core import db
from pymongo.errors import DuplicateKeyError
from bottle import route, run, template, redirect
from bottle import static_file, request, post , get , response
from bson.objectid import ObjectId
<<<<<<< HEAD
import hashlib

=======
>>>>>>> 1285da2320f2bc3fd9bfe519e67b4c88ec5f72e8

@route('/')
def home():
  cookie = request.get_cookie("user_id")
  if cookie:
    username = db.users.find_one({'_id':ObjectId(str(cookie))})
    return template("Hello {{name}}. Welcome back.", name=username['username'])
  return template('templates/index.html',title='Home Page',base='')

"""--------------load static files which are comprised of javascript and stylesheet and image--------------"""
@route('/statics/css/<filename:re:.*\.css>')
def send_css(filename):
  return static_file(filename, root='statics/css')

@route('/statics/js/<filename:re:.*\.js>')
def send_js(filename):
  return static_file(filename, root='statics/js')
"""--------------------------------------------------------------------------------------------------------"""

@route('/user/register')
def register():
  return template('templates/register.html',param = {})

@route('/user/login')
def login():
  return template('templates/login.html',param = {})

@post('/users/login/check')
def login_check():
    data = {}
    _user = request.forms.get('username', None).lower()
    _pass = request.forms.get('password', None)
<<<<<<< HEAD
    check = db.users.find_one({'username': _user, 'password': hashlib.md5(str(_pass)).hexdigest()})
=======
    check = db.users.find_one({'username': _user, 'password': _pass})
>>>>>>> 1285da2320f2bc3fd9bfe519e67b4c88ec5f72e8
    if check:
        response.set_cookie('user_id', str(check['_id']), path='/')
        return redirect('/')
    data['error'] = 'Authentication failed!'
    return template('templates/login.html', param=data)
    
@post('/register')
def form_submit():
  f = request.forms.get('firstname', None)
  l = request.forms.get('lastname', None)
  u = request.forms.get('username', None).lower()
  p = request.forms.get('password', None)
  e = request.forms.get('email', None)
  g = request.forms.get('gender', None)
  c = request.forms.get('country', None)
<<<<<<< HEAD
  data = dict(firstname=f, lastname=l ,username=u , password=hashlib.md5(str(p)).hexdigest() ,email=e,country=c , gender=g)
=======
  data = dict(firstname=f, lastname=l ,username=u , password=p ,email=e,country=c , gender=g)
>>>>>>> 1285da2320f2bc3fd9bfe519e67b4c88ec5f72e8
  try:
    #db['users'].insert_one(data)
    db.users.insert_one(data)
  except DuplicateKeyError:
    data = {}
    data['error'] = 'duplicate'
    return template('templates/register.html', param=data)
  return redirect("/user/show")

@route('/user/show')
def successful():
  data = list(db.users.find().limit(10))
  return template('templates/table.html', param=data)


if __name__ == '__main__':
  run(host='0.0.0.0', port=8080, debug=True)
