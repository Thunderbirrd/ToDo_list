from app import app
from database import db
import routes
from models import User, Task, Locale

db.create_all()


@app.context_processor
def include_permission_class():
    return {'User': User, 'Locale': Locale}


if __name__ == '__main__':
    app.run(host='0.0.0.0')
