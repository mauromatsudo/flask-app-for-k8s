from flask_sqlalchemy import SQLAlchemy
from faker import Factory
from sqlalchemy import create_engine
from models import db, Contact, set_string
from os import getenv

connect_string = set_string()
db_name = getenv('db_name')
engine = create_engine(connect_string)
connection = engine.connect()
connection.execute(f'CREATE DATABASE {db_name}')

fake = Factory.create()
db.drop_all()
db.create_all()
# Make 100 fake contacts
for num in range(100):
    fullname = fake.name().split()
    name = fullname[0]
    surname = ' '.join(fullname[1:])
    email = fake.email()
    phone = fake.phone_number()
    # Save in database
    mi_contacto = Contact(name=name, surname=surname, email=email, phone=phone)
    db.session.add(mi_contacto)

db.session.commit()