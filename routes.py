from app import app
from flask import render_template, redirect, url_for, request, flash, session
import json
import re
from models import User, Task


def auth():
    return session.get('auth') is not None


@app.route('/register', methods=["GET", "POST"])
def register():
    if auth():
        return redirect(url_for("index"))

    if request.form:
        login = request.form.get("login")
        password = request.form.get("password")

        if User.check_login(login) == 1 and User.check_pass(password) == 1:
            user = User.auth(login, password)

            if user:
                return json.dumps({'resultCode': 1})

            user = User(login, password)
            user.save()

            return json.dumps(
                {
                    'resultCode': 0,
                    'data': {
                        'login': login,
                        'password': password,
                        'user_id': user.id
                    }
                }
            )

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if auth():
        return redirect(url_for("index"))

    if request.form:
        login = request.form.get("login")
        password = request.form.get("password")
        user = User.auth(login, password)

        if user:
            session["auth"] = user.id
            return redirect(url_for("index"))
        else:
            flash("Wrong login and/or password")
    return render_template('login.html')


@app.route('/logout', methods=["GET", "POST"])
def logout():
    session['auth'] = None
    return redirect(url_for("login"))


@app.route('/add-task', methods=['POST'])
def add_task():
    task = Task(name=request.form.get('task'))
    task.save()
    return redirect(url_for('index'))


@app.route('/check', methods=['POST'])
def check():
    ids = []

    for row in request.form:
        search = re.search("^task-([\d]+)$", row)
        if search is not None:
            ids.append(int(search.group(1)))

    for task in Task.get_all():
        task.status = task.id in ids
        task.save()

    return redirect(url_for('index'))


@app.route('/')
def index():
    tasks = Task.get_all()
    return render_template('index.html', tasks=tasks)
