from App import db

class UF(db.Model):
    __tablename__ = 'uf'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    sigla = db.Column(db.String(2))
    idregiao = db.Column(db.Integer,db.ForeignKey('regiao.id'))
    regiao = db.relationship("Regiao")

