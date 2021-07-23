from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db_user_password = os.getenv('db_user_password')
db_username = 'root'
db_name = 'book'
MYSQL_SERVICE_HOST = os.getenv("MYSQL_SERVICE_HOST")
MYSQL_DATABASE_PORT = os.getenv("MYSQL_DATABASE_PORT")
app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///book.sqlite'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/book'
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{db_username}:{db_user_password}@{MYSQL_SERVICE_HOST}:{MYSQL_DATABASE_PORT}/{db_name}'
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
