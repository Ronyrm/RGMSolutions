from App import db
import datetime


class Unalimento(db.Model):
    __tablename__ = 'unidademedidaalimento'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    descricao = db.Column(db.String(50), nullable=False, unique=False)
    sigla = db.Column(db.String(3), nullable=False, unique=True)