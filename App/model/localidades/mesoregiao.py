from App import db

class MesoRegiao(db.Model):
    __tablename__ = 'mesoregiao'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    iduf = db.Column(db.Integer,db.ForeignKey('uf.id'))
    uf = db.relationship("UF")
