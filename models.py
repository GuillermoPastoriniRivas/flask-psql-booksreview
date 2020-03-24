import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class usuario(db.Model, UserMixin):

    __tablename__ = 'usuario'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    username = db.Column(db.String(16), unique=True, nullable=False)
    password = db.Column(db.String(16), nullable=False)

class book(db.Model, UserMixin):

    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(16), unique=True, nullable=False)   
    title = db.Column(db.String(16), nullable=False)
    author = db.Column(db.String(16), nullable=False)
    publicationyear = db.Column(db.Integer, nullable=False)