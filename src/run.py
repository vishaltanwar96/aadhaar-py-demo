import os

from flask import Flask
from flask_wtf.csrf import CSRFProtect

from app.blueprints import core

app = Flask(__name__)
CSRFProtect(app)


app.register_blueprint(core)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

if __name__ == "__main__":
    app.run()
