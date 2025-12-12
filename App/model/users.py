from App import db
import datetime
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(60), nullable=False, unique=True)
    create_on = db.Column(db.DateTime, default=datetime.datetime.now())

    def __init__(self, username, password, name, email):
        self.username = username
        self.password = password
        self.name = name
        self.email = email



#class SchemaUsers(SQLAlchemyAutoSchema):
#    class Meta:
#        model = Users


