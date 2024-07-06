import os
#from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#from flask_marshmallow import Marshmallow
from flask_migrate import Migrate

# Load environment variables from .env file
#load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)

#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/databasename'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:29122003@localhost:5432/people'
#app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI', 'postgresql://username:password@localhost/databasename')

app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your_secret_key_here')

db = SQLAlchemy(app)
#ma = Marshmallow(app)
migrate = Migrate(app, db)
