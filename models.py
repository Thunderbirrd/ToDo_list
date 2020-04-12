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

    def set_login(self, new_login):
        self.login = new_login
        self.save()

    def set_password(self, new_pass):
        self.password = new_pass
        self.save()

    def get_active_tasks(self):
        return Task.get_users_tasks(self.id)

    def get_archive(self):
        return Task.get_users_archive(self.id)

    def get_all_tasks(self):
        return Task.get_all_tasks(self.id)

    @staticmethod
    def check_login(login):
        login = str(login)
        if login in User.get_all_login():
            return "User with this login already exists"
        elif len(login) < 5:
            return "Login must be at least 5 symbols"
        elif not login[0].isalpha():
            return "Login should starts with a letter"
        else:
            return 1

    @staticmethod
    def check_pass(password):
        password = str(password)
        if len(password) < 8:
            return "Password should be at least 8 symbols"
        elif password.isnumeric() or password.isalpha() or password.lower() == password or password.upper() == password:
            return "Password should consists of at least: 1 upper case letter, 1 lower case and one number"
        elif password == "qwerty123":
            return "Very bad password, dude)"
        else:
            return 1

    @staticmethod
    def get_login_by_id(i):
        user = db.session.query(User).filter(User.id == i).first()
        return user.login

    @staticmethod
    def get_all_login():
        user_list = list(db.session.query(User))
        login_list = []
        for user in user_list:
            login_list.append(user.id)

    @staticmethod
    def auth(login, password):
        return db.session.query(User).filter(User.login == login).filter(User.password == password).first()


class Task(db.Model, Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    name = db.column(db.String)
    text = db.Column(db.String)
    status = db.Column(db.Boolean)  # True = active, False = archived
    author_id = db.column(db.Integer, db.ForeignKey(User.id))
    date = db.Column(db.DateTime)

    def __init__(self, name, author_id, status=False):
        self.name = name
        self.status = status
        self.author_id = author_id
        self.date = datetime.now().replace(second=0, microsecond=0)

    def set_status(self, status):
        self.status = status
        self.save()

    def set_text(self, text):
        self.text = text
        self.save()

    def set_name(self, name):
        self.name = name
        self.save()

    @staticmethod
    def get_archive():
        tasks = list(db.session.query(Task).filter(not Task.status))
        archive = []

        for task in tasks:
            archive.append(Task.get_task_by_id(task.id))

        return archive

    @staticmethod
    def get_active_tasks():
        tasks = list(db.session.query(Task).filter(Task.status))
        archive = []

        for task in tasks:
            archive.append(Task.get_task_by_id(task.id))

        return archive

    @staticmethod
    def get_task_by_id(i):
        task = db.session.query(Task).filter(Task.id == i).first()
        return {
            "name": task.name,
            "text": task.text,
            "status": task.status,
            "date": task.date,
            "author_id": task.author_id,
            "author_login": User.get_login_by_id(task.author_id)
        }

    @staticmethod
    def get_users_tasks(user_id):
        tasks = list(db.session.query(Task).filter(Task.author_id == user_id).filter(Task.status))
        return_list = []
        for task in tasks:
            return_list.append(Task.get_task_by_id(task.id))

        return return_list

    @staticmethod
    def get_users_archive(user_id):
        tasks = list(db.session.query(Task).filter(Task.author_id == user_id).filter(not Task.status))
        return_list = []
        for task in tasks:
            return_list.append(Task.get_task_by_id(task.id))

        return return_list

    @staticmethod
    def get_all_tasks(user_id):
        tasks = list(db.session.query(Task).filter(Task.author_id == user_id))
        return_list = []
        for task in tasks:
            return_list.append(Task.get_task_by_id(task.id))

        return return_list
