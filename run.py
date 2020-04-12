from app import app
from database import db
from models import User, Task

db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0')
