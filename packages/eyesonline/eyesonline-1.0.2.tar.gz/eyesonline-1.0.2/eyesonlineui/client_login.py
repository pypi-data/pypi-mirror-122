import requests, socketio

loginurl = "http://localhost:8080/login"
payload ={'email':'a@a.com','password':'a','remember':'true'}

session = requests.session()
r = session.post(loginurl, payload)
if r.status_code == 200:
	print(session.cookies.get_dict())
	token = 'remember_token='
	token += session.cookies['remember_token']
	token += '; session='
	token += session.cookies['session']
	
# standard Python
sio = socketio.Client()

sio.connect('http://localhost:8080',headers={'Cookie': token}, namespaces=['/classroom'])

