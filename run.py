from app import app
from flask import request, session
from database import db
import json
from models import User, Task

db.create_all()

if __name__ == '__main__':
    app.run()
