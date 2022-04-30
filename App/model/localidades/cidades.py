from App import db

class Cidades(db.Model):
    __tablename__ = 'cidades'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    idmicroregiao = db.Column(db.Integer,db.ForeignKey('microregiao.id'))
    iduf = db.Column(db.Integer,db.ForeignKey('uf.id'))
    microregiao = db.relationship("MicroRegiao")

