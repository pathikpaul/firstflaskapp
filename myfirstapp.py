#########################################
##    bento/centos-7.2  (came with Python 2.7.5 installed)
#########################################
##    sudo yum install python-virtualenv
##    mkdir myproject
##    cd myproject
##    python2 -m virtualenv venv
##    cd /home/hadoop/myproject
##    . venv/bin/activate
##    pip install Flask==1.1.2
##    vi myfirstapp.py
##    export  FLASK_ENV=development
##    export  FLASK_APP=myfirstapp
##    flask run 
##    flask run --host=192.168.77.10
#########################################
import json
import flask
import platform
import socket
from datetime import datetime
from flask import Flask,render_template,request,abort,redirect,url_for

app = Flask(__name__)

PageVisistedCount=0
@app.route('/info')
def info():
    global PageVisistedCount
    PageVisistedCount=PageVisistedCount+1
    FlaskVersion=flask.__version__
    myhostname = socket.gethostname()
    myip_address = socket.gethostbyname(myhostname)
    myString=("Hello, World!"+"</br>"
             +"FlaskVersion="+FlaskVersion+"</br>"
             +"Running At: "+str(datetime.now())+"</br>"
             +"OS: "+str(platform.platform())+"</br>"
             +"Release: "+str(platform.linux_distribution())+"</br>"
             +"Hostname: "+myhostname+"</br>"
             +"IP Address: "+myip_address+"</br>"
             +"</br>"
             +"</br>"
             +"PageVisisted: "+str(PageVisistedCount)+" times</br>"
             )
    return myString

@app.route('/')
def welcome():
   return render_template("welcome.html",notes=notes)

@app.route('/note/<int:index>')
def note_view(index):
    try:
        if index<= len(notes)-1:
            return render_template("note.html", note=notes[index],index=index,max_index=len(notes)-1)
        else:
            return render_template("welcome.html",notes=notes)
    except IndexError:
        abort(404)

@app.route('/delete_note/<int:index>',methods=["GET","POST"])
def delete_note(index):
    if request.method == "GET":
        return render_template("delete_note.html",note=notes[index],index=index)
    if request.method == "POST":
        try:
            notes.pop(index)
            write_note(notes)
            if index<= len(notes)-1:
                return render_template("note.html", note=notes[index],index=index)
            else:
                return render_template("welcome.html",notes=notes)
        except IndexError:
            abort(404)
@app.route('/add_note',methods=["GET","POST"])
def add_note():
    if request.method == "GET":
        return render_template("add_note.html")
    if request.method == "POST":
        note={'topic': request.form["topic"], 'comment': request.form["comment"]}
        notes.append(note)
        write_note(notes)
        return redirect(url_for('note_view', index=len(notes)-1))

def read_notes():
    with open("notes_db.json") as f:
        return json.load(f)
def write_note(list_of_notes):
    with open("notes_db.json", 'w') as f:
        return json.dump(list_of_notes, f)
notes=read_notes()

#app.run(host='192.168.77.10',port=5000)

