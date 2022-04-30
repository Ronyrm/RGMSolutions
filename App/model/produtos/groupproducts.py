from App import db
import datetime

class GroupProducts(db.Model):
    __tablename__ = 'grupoprodutos'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descricao = db.Column(db.String(50), nullable=False)
    create_on = db.Column(db.DateTime, default=datetime.datetime.now())
