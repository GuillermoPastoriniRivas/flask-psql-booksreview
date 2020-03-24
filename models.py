import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class Usuario(db.Model, UserMixin):

    __tablename__ = 'usuario'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    username = db.Column(db.String(16), unique=True, nullable=False)
    password = db.Column(db.String(16), nullable=False)

class Book(db.Model):

    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(16), unique=True, nullable=False)   
    title = db.Column(db.String(16), nullable=False)
    author = db.Column(db.String(16), nullable=False)
    publicationyear = db.Column(db.Integer, nullable=False)

    def add_review(self, rating, description, user_id):
        b = Review(rating=rating, description=description, book_id=self.id, user_id=user_id)
        db.session.add(b)
        db.session.commit()

class Review(db.Model):

    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(256), nullable=True)