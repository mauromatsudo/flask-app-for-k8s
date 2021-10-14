from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import getenv, path
from os.path import abspath
from dotenv import load_dotenv

def set_string():
    proj_env = abspath('/home/mmatsudo/teste/flask-contacts/.env')
    load_dotenv(dotenv_path=proj_env)
    db_user_password = getenv('db_user_password')
    db_username = 'root'
    MYSQL_SERVICE_HOST = getenv("MYSQL_SERVICE_HOST")
    MYSQL_DATABASE_PORT = getenv("MYSQL_DATABASE_PORT")
    db_name = getenv('db_name')
    return f'mysql+pymysql://{db_username}:{db_user_password}@{MYSQL_SERVICE_HOST}:{MYSQL_DATABASE_PORT}/{db_name}'

#db_name = getenv('db_name')
connect_string = set_string()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'{connect_string}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Contact(db.Model):


    __tablename__ = 'contacts'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    surname = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(200), nullable=True, unique=True)
    phone = db.Column(db.String(20), nullable=True, unique=False)

    def __repr__(self):
        return '<Contacts %r>' % self.name
