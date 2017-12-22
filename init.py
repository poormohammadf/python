#!/usr/bin/python
import shelve
from bottle import route, run, template, redirect
from bottle import static_file, request, post

@route('/')
def index():
  return template('templates/index.html')

"""--------------load static files which are comprised of javascript and stylesheet and image--------------"""
@route('/statics/css/<filename:re:.*\.css>')
def send_css(filename):
  return static_file(filename, root='statics/css')

@route('/statics/js/<filename:re:.*\.js>')
def send_js(filename):
  return static_file(filename, root='statics/js')
"""--------------------------------------------------------------------------------------------------------"""

@route('/templates/<name>')
def read_temp_register(name):
  return template('templates/register.html', name=name)

"""@route('/templates/<name>')
def read_temp_login(name):
  return template('templates/login.html', name=name)"""

@post('/form-submit-r')#for seo it is better to use hyphen instead of underline
def form_submit():
  f = request.forms.get('firstname', None)
  l = request.forms.get('lastname', None)
  u = request.forms.get('username', None)
  p = request.forms.get('password', None)
  e = request.forms.get('email', None)
  g = request.forms.get('gender', None)
  c = request.forms.get('country', None)
  sh = shelve.open('db.db')
  sh[u] = dict(firstname=f, lastname=l ,username=u , password=p ,email=e,country=c , gender=g)
  sh.close()
  return redirect("/successful")

@route('/successful')
def successful():
  conn = shelve.open('db.db')
  data = conn.items()
  conn.close()
  return template('templates/table.html', data=data)

if __name__ == '__main__':
  run(host='0.0.0.0', port=8080, debug=True)


