#!/usr/bin/python
from core import db
from pymongo.errors import DuplicateKeyError
from bottle import route, run, template, redirect
from bottle import static_file, request, post , get , response
from bson.objectid import ObjectId
import hashlib


def session_is_set():
  global setting
  cookie = request.get_cookie("user_id")
  if cookie:
    username = db.users.find_one({'_id':ObjectId(str(cookie))})
    setting['session'] = username['username']

@route('/')
def home():
  session_is_set()
  return template('templates/index.html',title='Home Page',base='',setting=setting)

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
  session_is_set()
  return template('templates/register.html',setting = setting)

@route('/user/login')
def login():
  session_is_set()
  return template('templates/login.html',setting = setting)

@route('/user/logout')
def logout():
  global setting
  response.delete_cookie('user_id', path='/')
  setting.pop('session')
  return redirect("/")

@post('/users/login/check')
def login_check():
    global setting
    _user = request.forms.get('username', None).lower()
    _pass = request.forms.get('password', None)
    check = db.users.find_one({'username': _user, 'password': hashlib.md5(str(_pass)).hexdigest()})
    if check:
        response.set_cookie('user_id', str(check['_id']), path='/')
        return redirect('/')
    setting['error'] = 'Authentication failed!'
    return template('templates/login.html', setting=setting)
    
@post('/register')
def form_submit():
  global setting
  f = request.forms.get('firstname', None)
  l = request.forms.get('lastname', None)
  u = request.forms.get('username', None).lower()
  p = request.forms.get('password', None)
  e = request.forms.get('email', None)
  g = request.forms.get('gender', None)
  c = request.forms.get('country', None)
  data = dict(
    firstname=f, 
    lastname=l ,
    username=u , 
    password=hashlib.md5(str(p)).hexdigest() ,
    email=e,
    gender=g, 
    country=c)
  try:
    #db['users'].insert_one(data)
    db.users.insert_one(data)
  except DuplicateKeyError:
    setting['error'] = 'Duplicate username'
    return template('templates/register.html', setting=setting)
  return redirect("/user/show")

@route('/user/show')
def successful():
  global setting
  session_is_set()
  data = list(db.users.find().limit(10))
  return template('templates/table.html', param=data,setting=setting)

setting = {}

if __name__ == '__main__':
  run(host='0.0.0.0', port=8080, debug=True)
