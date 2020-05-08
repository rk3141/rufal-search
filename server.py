from flask import Flask,render_template
from scanner import WebPages,LookFor
from urllib import parse

app = Flask('Rufal',static_folder='./',template_folder='./')
app.config['SECRET_KEY'] = 'rufal_abcd@123'

# socketio = SocketIO(app)
@app.route('/')
def index():
     return render_template('search.html')
@app.route('/lookfor/<q>')
def lookfor(q):
     return '<head><link rel="stylesheet" href="../style.css"></head>' + render_template('search.html') + '<br>' + LookFor(q,'pages')

app.run('',port=80,debug=True)