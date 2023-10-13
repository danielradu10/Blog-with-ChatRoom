import random

from flask import Flask, Response, session
from flask import render_template
from werkzeug.utils import secure_filename, redirect
#render template ne va permite sa folosim metoda render template si sa returnam un template
from flask import url_for
#url_for gaseste pathurile exacte catre routes
from flask_sqlalchemy import SQLAlchemy
from flask import request as request

import os
from flask_socketio import SocketIO, join_room, send, emit

from Utilizator import Utilizator

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
UPLOAD_FOLDER = './static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
SQLALCHEMY_BINDS = {
    "blogs": 'sqlite:///' + os.path.join(basedir, 'database.db')
}
database = SQLAlchemy(app)
socketio = SocketIO(app)

utilizator = None

#create database model
class Users(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(200), nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.id

class BlogArticle(database.Model):

    id = database.Column(database.Integer, primary_key=True)
    title = database.Column(database.String(200), nullable=False)
    author = database.Column(database.String(200), nullable=False)
    text = database.Column(database.String(3000), nullable = False)
    image = database.Column(database.String(200))



logged : bool = False

posts = [
    {'singer': 'Abel',
     'title': 'After Hours',
     'release_date': '2021'},
    {
     'singer': 'The Motans',
     'title': 'Tu',
     'release_date': '2020'
    }
]

#just me tryng some things
@app.route("/", methods = ["POST", "GET"])
def first_page():
    logged = False
    mail = request.form.get('mail')
    password = request.form.get('password')
    username = request.form.get('Username')
    print("SIDDDDDDDDDDD")
    session['username'] = username

    if 'file' not in request.files:
        print("hmmm")
        return render_template('first_page.html', title='Log In', logged=logged)

    image = request.files['file']
    if os.path.exists("descarcare.jpg"):
        print("Era deja salvagt un fisier cu descarcare.jpg")
        os.remove("descarcare.jpg")
    image.save(os.path.abspath("descarcare.jpg"))

    global utilizator
    utilizator = Utilizator(mail, password, username, image)

    print("Aici")
    print("N am ajuns")
    message = utilizator.validate()
    if(message == "Conectare reusita!"):
        return render_template('home.html', postshtml = BlogArticle.query.all())
    else:
        logged = True
        return render_template('first_page.html', mesaj=message, logged = logged)

@app.route("/myprofile/", methods=['GET', 'POST'])
def profile():
    print("Salut sunt in profile")
    if request.method == "POST":
        print("E post ")
        if request.form['create_button'] == "Creeaza postare":
            print("Vrea sa posteze")
            return redirect(url_for("createarticle"))
        elif request.form['not_create_button'] == "Nu creeaza postare":
            print("Nu vrea sa posteze")
        else:
            print("Nu imi dau seama")
    elif request.method == "GET":
        print("Nu inteleg.. e get")
        print("Aici am ajuns?")
        global utilizator
        return render_template('profile.html', profile_picture="images/" + utilizator.getProfilePicture(), user_name=session['username'])

@app.route("/myprofile/create_article", methods=['GET', 'POST'])
def createarticle():
    print("Am intrat in create article")
    titlu = request.form.get("titlu")
    text = request.form.get("text")

    if 'imagine_articol' not in request.files:
        print("hmmm")
        return render_template('create_article.html')

    image = request.files['imagine_articol']
    savedname = image.filename
    if os.path.exists(savedname):
        print("Era deja salvagt un fisier cu descarcare.jpg")
        savedname += random.Random.randint(0,100)


    path = os.path.join(app.config['UPLOAD_FOLDER'],savedname)
    image.save(path)

    if request.method == "POST":
        print("E post ")
        if request.form['done_button'] == "Done":
            print("A apasat done")
            article = BlogArticle(title=titlu, text=text, author=utilizator.getName(), image=path)
            database.session.add(article)
            database.session.commit()

            print(titlu)
            print(text)
            return redirect(url_for('home'))
    elif request.method == "GET":
        print("E get in create article")
        return render_template('create_article.html')

#decoratorii adauga functionalitati noi unor functii deja existente
#route decorators
@app.route("/home", methods=['GET', 'POST'])
def home():
    postari = BlogArticle.query.all()
    if (len(postari) == 0):
        print("Nici macar o postare")
    return render_template('home.html', postshtml=postari)
    # variabila noastra se va numi in html code -> "postshtml" (asa o vom accesa)
    # si ea este egala cu posts din appul nostru

@app.route("/about")
def about():
    return render_template('about.html', title='Daniel Project')

@app.route("/chatroom")
def chatroom():
    print("Sunt in chatroom")
    global utilizator

    return render_template('chatroom.html')

@app.route("/games")
def games():
    return render_template('games.html')


@socketio.on('connect')
def test_connect(data):
    emit("message_received", {"username": session['username'], "mesaj": "s-a conectat"})
    print(session['username'] + " s-a conectat!")


@socketio.on('enter_pressed')
def enter_pressed(mesaj: str):
    print(session["username"] + mesaj)
    emit("message_received", {"username": session['username'], "mesaj": mesaj}, broadcast=True)

@socketio.on("click_pressed")
def click_pressed(data):
    print(session["username"] + " a apasat la " + str(data))





if __name__ == "__main__":
    with app.app_context():
        database.create_all()
    socketio.run(app, allow_unsafe_werkzeug=True, debug=True)
