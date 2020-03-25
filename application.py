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
    return Usuario.query.get(int(user_id))

@app.route("/")
def index():
    books = Book.query.limit(10).all()
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
        user = Usuario.query.filter_by(username=name, password=psw).first()
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
        user = Usuario.query.filter_by(username=username).first()
        if user:
            return render_template("error.html", message="Username already exists")
        nuevo = Usuario(name=name.capitalize(), username=username, password=psw)
        db.session.add(nuevo)   
        db.session.commit()
        login_user(nuevo)
        return redirect(url_for('books'))

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route("/books", methods=["GET", "POST"])
@login_required
def books():
    if request.method == 'POST':
        search = request.form.get("search") 
        books = Book.query.filter(Book.title.like(f"%{search}%") | Book.author.like(f"%{search}%") | Book.isbn.like(f"%{search}%")).all()
        if not books:
            return render_template("books.html", message="Book not found", name = current_user.name)
    if  request.method == 'GET':
        books = Book.query.limit(30).all()
    return render_template("books.html", books=books, name = current_user.name)

@app.route("/books/<int:book_id>", methods=["GET", "POST"])
@login_required
def book(book_id):
    libro = Book.query.get(book_id)
    if libro is None:
        return render_template("error.html", message="No such book.")

    if request.method == 'POST':
        # Make sure the user no comments before.
        rev = Review.query.filter_by(user_id=current_user.id, book_id=book_id).first()
        if rev:
            return render_template("error.html", message="You already commented this post")
        rating = request.form.get("rating") 
        description = request.form.get("description") 
        libro.add_review(rating, description, current_user.id)

    reviews = Review.query.filter_by(book_id=book_id).all()
    return render_template("book.html", book=libro, reviews=reviews, name = current_user.name)