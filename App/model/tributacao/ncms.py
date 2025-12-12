from App import db
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

class NCMS(db.Model):
    __tablename__ = 'ncms'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    codncm = db.Column(db.String(10), nullable=False)
    descricao = db.Column(db.String(200), nullable=False)
    grau = db.Column(db.Integer)
    grau1 = db.Column(db.String(2))
    grau2 = db.Column(db.String(2))
    grau3 = db.Column(db.String(2))
    grau4 = db.Column(db.String(2))
    idncm_pai =  db.Column(db.Integer,db.ForeignKey('ncms.id'))
    codncm_pai = db.Column(db.String(10))
    codigo = db.Column(db.String(8), nullable=False, unique=True)
    data_inicio = db.Column(db.Date)
    data_final = db.Column(db.Date)
    unidade = db.Column(db.String(2))
    desc_unidade = db.Column(db.String(50))
    status = db.Column(db.String(1))


class SchemaNCMS(SQLAlchemyAutoSchema):
    class Meta:
        model = NCMS