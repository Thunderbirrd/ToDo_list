from flask_sqlalchemy import SQLAlchemy
from app import app
from flask_session import Session

db = SQLAlchemy(app)

Session(app)
