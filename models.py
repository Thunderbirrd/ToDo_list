from database import db
from flask import session
from datetime import datetime
from sqlalchemy import func, asc, select
import json
import random


class Model:
    errors = []

    def validate(self):
        self.errors = []
        return len(self.errors) == 0

    def save(self):
        if self.validate():
            print(self.id)
            if self.id is None:
                db.session.add(self)
                print(2)
            db.session.commit()
            return True
        else:
            return False


class User(db.Model, Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    login = db.Column(db.String, unique=True)
    password = db.Column(db.String)

    def __init__(self, login, password=""):
        self.login = login
        self.password = password

    @staticmethod
    def auth(login, password):
        return db.session.query(User).filter(User.login == login).filter(User.password == password).first()


class Task(db.Model, Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    name = db.column(db.String)
    text = db.Column(db.String)
    status = db.Column(db.Boolean)
    author_id = db.column(db.Integer, db.ForeignKey(User.id))
    date = db.Column(db.DATETIME)

    def __init__(self, name, author_id, date, status=False):
        self.name = name
        self.status = status
        self.author_id = author_id
        self.date = date





