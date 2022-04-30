from App import db

class Regiao(db.Model):
    __tablename__ = 'regiao'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    sigla = db.Column(db.String(2))