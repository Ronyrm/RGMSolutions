from App import db
import datetime


class Vendedor(db.Model):
    __tablename__ = 'vendedor'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rg = db.Column(db.String(20))
    titulo = db.Column(db.String(20))
    orgaoemissor = db.Column(db.String(20))
    cpfcnpj = db.Column(db.String(20))
    datacadastro = db.Column(db.DateTime, default=datetime.datetime.now())
    comissao = db.Column(db.NUMERIC(precision=8, asdecimal=False, scale=3))
    idpessoa = db.Column(db.Integer, db.ForeignKey('pessoa.id'))
    pessoa = db.relationship("Pessoa")

