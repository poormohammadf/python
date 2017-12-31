#!/usr/bin/python
from core import db
from pymongo.errors import DuplicateKeyError
from bottle import route, run, template, redirect
from bottle import static_file, request, post , get , response
from bson.objectid import ObjectId
import hashlib

config = {}

def session_is_set():
  global config
  cookie = request.get_cookie("user_id")
  if cookie:
    username = db.users.find_one({'_id':ObjectId(str(cookie))})
    config['session'] = username['username']

@route('/')
def home():
  global config
  session_is_set()
  return template('templates/index.html',title='Home Page',base='',config=config)

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
  return template('templates/register.html',config = config)

@route('/user/login')
def login():
  session_is_set()
  return template('templates/login.html',config = config)

@route('/user/logout')
def logout():
  response.delete_cookie('user_id', path='/')
  return redirect("/")

@post('/users/login/check')
def login_check():
    global config
    _user = request.forms.get('username', None).lower()
    _pass = request.forms.get('password', None)
    check = db.users.find_one({'username': _user, 'password': hashlib.md5(str(_pass)).hexdigest()})
    if check:
        response.set_cookie('user_id', str(check['_id']), path='/')
        return redirect('/')
    config['error'] = 'Authentication failed!'
    return template('templates/login.html', config=config)
    
@post('/register')
def form_submit():
  global config
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
    config['error'] = 'duplicate'
    return template('templates/register.html', config=config)
  return redirect("/user/show")

@route('/user/show')
def successful():
  session_is_set()
  data = list(db.users.find().limit(10))
  return template('templates/table.html', param=data,config=config)


if __name__ == '__main__':
  run(host='0.0.0.0', port=8080, debug=True)
