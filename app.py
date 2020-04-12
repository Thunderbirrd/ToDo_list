from flask import Flask
from flask_session import Session

app = Flask(__name__)
app.secret_key = 'asdasfasfasfagasgas'
app.config.from_pyfile('hello.cfg')

Session(app)
