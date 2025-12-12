from App import db
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema,fields
from App.schema.localidades.localidades import CidadesSchema
from .hospitais_covid import SchemaHospitais
class Pacientes_covid(db.Model):
    __tablename__ = 'pacientes_covid'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idpaciente = db.Column(db.String(100), nullable=False,unique=True)
    genero = db.Column(db.String(1)) # F - Feminino M - Masculino
    anonascimento = db.Column(db.Integer)
    siglapais = db.Column(db.String(2))
    iduf = db.Column(db.Integer,db.ForeignKey('uf.id'))
    idcidade = db.Column(db.Integer,db.ForeignKey('cidades.id'))
    cidade = db.relationship("Cidades")
    cepreduzido = db.Column(db.String(5))
    idhospital = db.Column(db.Integer,db.ForeignKey('hospitais.id'))
    hospital = db.relationship("Hospitais")

class SchemaPacientes(SQLAlchemyAutoSchema):
    class Meta:
        model = Pacientes_covid
    cidade = fields.Nested(CidadesSchema)
    hospital = fields.Nested(SchemaHospitais)