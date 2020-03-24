from flask import Flask, render_template, jsonify, request
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

@app.route("/login")
def login():
    
    return render_template("login.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")


@app.route("/books")
def books():

    # Get form information.
    name = request.form.get("username")
    psw = request.form.get("password")
    try:
        username = str(request.form.get("username"))
    except ValueError:
        return render_template("error.html", message="Enter an username.")

    # Make sure the user exists.
    user = usuario.query.filter_by(username=name, password=psw).first()
    if not user:
        return render_template("error.html", message="Invalid username or password ")

    login_user(user)
    return render_template("books.html")