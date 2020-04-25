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
import os.path

application = Flask(__name__)

PageVisistedCount=0
@application.route('/info')
def info():
    global PageVisistedCount
    PageVisistedCount=PageVisistedCount+1
    FlaskVersion=flask.__version__
    myhostname = socket.gethostname()
    #myip_address = socket.gethostbyname(myhostname)
    myString=("Hello, World!"+"</br>"
             +"FlaskVersion="+FlaskVersion+"</br>"
             +"Running At: "+str(datetime.now())+"</br>"
             +"OS: "+str(platform.platform())+"</br>"
             +"Release: "+str(platform.linux_distribution())+"</br>"
             +"Hostname: "+myhostname+"</br>"
             +"</br>"
             +"</br>"
             +"PageVisisted: "+str(PageVisistedCount)+" times</br>"
             )
    return myString

@application.route('/')
def welcome():
   return render_template("welcome.html",notes=notes)

@application.route('/note/<int:index>')
def note_view(index):
    try:
        if index<= len(notes)-1:
            return render_template("note.html", note=notes[index],index=index,max_index=len(notes)-1)
        else:
            return render_template("welcome.html",notes=notes)
    except IndexError:
        abort(404)

@application.route('/delete_note/<int:index>',methods=["GET","POST"])
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
@application.route('/add_note',methods=["GET","POST"])
def add_note():
    if request.method == "GET":
        return render_template("add_note.html")
    if request.method == "POST":
        note={'topic': request.form["topic"], 'comment': request.form["comment"]}
        notes.append(note)
        write_note(notes)
        return redirect(url_for('note_view', index=len(notes)-1))

def read_notes():
    if os.path.exists("notes_db.json"):
        with open("notes_db.json") as f:
            return json.load(f)
    else:
       return ([{"topic": "T1", "comment": "comment one"}, {"topic": "T2", "comment": "comment two"}, {"topic": "T3", "comment": "comment three"}, {"topic": "T4 ", "comment": "comment four"}])

def write_note(list_of_notes):
    if os.path.exists("notes_db.json"):
        with open("notes_db.json", 'w') as f:
            return json.dump(list_of_notes, f)

notes=read_notes()

if __name__ == "__main__":
    application.debug = True
    #application.run(host='192.168.77.10')
    application.run()
