from App import db

class MicroRegiao(db.Model):
    __tablename__ = 'microregiao'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    idmesoregiao = db.Column(db.Integer,db.ForeignKey('mesoregiao.id'))
    mesoregiao = db.relationship("MesoRegiao")
