from app import app
from flask import render_template, redirect, url_for, request, flash, session
import json
import datetime
import re
from werkzeug.security import generate_password_hash, check_password_hash
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
        password_confirm = request.form.get("password-confirm")
        if password != password_confirm:
            flash("Passwords are different")
        elif login == "":
            flash("Login must be set")
        elif password == "":
            flash("Password must be set")
        elif User.check_login(login) == 1 and User.check_pass(password) == 1:
            user = User(login, generate_password_hash(password))
            user.save()
            flash("Register successful")
            return redirect(url_for("login"))

        elif User.check_login(login) != 1:
            flash(User.check_login(login))
        elif User.check_pass(password) != 1:
            flash(User.check_pass(password))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if auth():
        return redirect(url_for("index"))

    if request.form:
        login = request.form.get("login")
        password = request.form.get("password")
        user = User.get_user_by_login(login)

        if user and check_password_hash(user.password, password):
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
    if not auth():
        return redirect(url_for("login"))
    user = User.get_current_user()
    name = request.form.get("name")
    if Task.check_if_task_is_unique_today(user.id, name):
        task = Task(name=name, text=request.form.get("text"), author_id=user.id)
        task.save()
    return redirect(url_for('index'))


@app.route('/check', methods=['POST'])
def check():
    ids = []
    user = User.get_current_user()
    for row in request.form:
        search = re.search("^task-([\d]+)$", row)
        if search is not None:
            ids.append(int(search.group(1)))

    for task in Task.get_users_tasks(user.id):
        task.status = task.id in ids
        task.set_status(task.status)

    return redirect(url_for('index'))


@app.route('/check_archive', methods=['POST'])
def check_archive():
    ids = []
    user = User.get_current_user()
    for row in request.form:
        search = re.search("^task-([\d]+)$", row)
        if search is not None:
            ids.append(int(search.group(1)))

    for task in Task.get_users_archive(user.id):
        task.status = task.id in ids
        task.set_status(task.status)

    return redirect(url_for('archive'))


@app.route('/tasks_in_period', methods=['POST'])
def period():
    user = User.get_current_user()
    s1 = request.form.get("start_date")
    s2 = request.form.get("finish_date")
    if str(s1) != "" and str(s2) != "":
        date1 = datetime.date(int(s1[:4]), int(s1[5:7]), int(s1[-2:]))
        date2 = datetime.date(int(s2[:4]), int(s2[5:7]), int(s2[-2:]))
        if date1 <= date2:
            tasks = Task.get_all_users_task_in_period(user.id, date1, date2)
            return render_template('archive.html', tasks=tasks)
        else:
            return redirect(url_for('archive'))
    return redirect(url_for('archive'))


@app.route('/archive')
def archive():
    if not auth():
        return redirect(url_for("login"))
    user = User.get_current_user()
    tasks = Task.get_users_archive(user.id)
    return render_template('archive.html', tasks=tasks)


@app.route('/all_tasks')
def all_tasks():
    if not auth():
        return redirect(url_for("login"))
    user = User.get_current_user()
    tasks = Task.get_all(user.id)
    return render_template('all_tasks.html', tasks=tasks)


@app.route('/set_locale/<rg>')
def set_locale(rg):
        session["locale"] = rg
        return redirect(url_for("index"))


@app.route('/delete_task', methods=['POST'])
def delete_task():
    if not auth():
        return redirect(url_for("login"))
    user = User.get_current_user()
    name = request.form.get("task_to_delete")
    Task.delete_task(user.id, name)
    return redirect(url_for('index'))


@app.route('/')
def index():
    if not auth():
        return redirect(url_for("login"))
    user = User.get_current_user()
    tasks = Task.get_users_tasks(user.id)
    return render_template('index.html', tasks=tasks)
