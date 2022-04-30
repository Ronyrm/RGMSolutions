from App import db
from marshmallow_sqlalchemy import ModelSchema,fields
from App.model.covid.exames_covid import SchemaExames

class Analitos_covid(db.Model):
    __tablename__ = 'analitos_covid'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descricao = db.Column(db.String(100), nullable=False)
    valref_min = db.Column(db.NUMERIC(precision=8, asdecimal=False, scale=3))
    valref_max = db.Column(db.NUMERIC(precision=8, asdecimal=False, scale=3))
    descvalref = db.Column(db.String(50))
    idexame = db.Column(db.Integer, db.ForeignKey('exames_covid.id'))
    unidademedida = db.Column(db.String(20))
    exame = db.relationship("Exames_covid")



class SchemaAnalitos(ModelSchema):
    class Meta:
        model = Analitos_covid
    exame: fields.Nested(SchemaExames)