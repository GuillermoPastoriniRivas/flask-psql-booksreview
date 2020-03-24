from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = 'clavesecreta'
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return usuario.query.get(int(user_id))

@app.route("/")
def index():
    books = book.query.limit(30).all()
    return render_template("index.html", books=books)

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == 'GET':
        return render_template("login.html")

    if request.method == 'POST':
         # Get form information.
        name = request.form.get("username")
        psw = request.form.get("password")

        # Make sure the user and password are correct.
        user = usuario.query.filter_by(username=name, password=psw).first()
        if not user:
            return render_template("login.html", message="Invalid username or password ")
        login_user(user)
        return redirect(url_for('books'))

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == 'GET':
        return render_template("signup.html")

    if request.method == 'POST':
            # Get form information.
        name = request.form.get("name") 
        username = request.form.get("username")
        psw = request.form.get("password")
       
        # Make sure the user exists.
        user = usuario.query.filter_by(username=username).first()
        if user:
            return render_template("error.html", message="Username already exists")
        nuevo = usuario(name=name, username=username, password=psw)
        db.session.add(nuevo)   
        db.session.commit()
        return redirect(url_for('login'))

@app.route("/books")
@login_required
def books():
    books = book.query.limit(30).all()
    return render_template("books.html", books=books, name = current_user.name)