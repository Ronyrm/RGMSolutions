from App.model.covid.exames_covid import SchemaExames
from App.model.covid.analitos_covid import SchemaAnalitos
from App.model.covid.pacientes_covid import SchemaPacientes
from App.model.covid.hospitais_covid import SchemaHospitais
from App import db
from marshmallow_sqlalchemy import ModelSchema,fields


class Exames_pacientes_covid(db.Model):
    __tablename__ = 'exames_pacientes_covid'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idpaciente = db.Column(db.Integer,db.ForeignKey('pacientes_covid.id'))
    paciente = db.relationship("Pacientes_covid")
    datacoleta = db.Column(db.Date)
    origem = db.Column(db.String(4)) #LAB ou HOSP
    idexame = db.Column(db.Integer,db.ForeignKey('exames_covid.id'))
    exame = db.relationship("Exames_covid")
    idanalito = db.Column(db.Integer, db.ForeignKey('analitos_covid.id'))
    analito = db.relationship("Analitos_covid")
    resultado = db.Column(db.String(50))
    valresultado = db.Column(db.NUMERIC(precision=8, asdecimal=False, scale=3))
    unidademedida = db.Column(db.String(20))
    valreferencia = db.Column(db.String(20))
    idhospital = db.Column(db.Integer, db.ForeignKey('hospitais.id'))
    hospital = db.relationship("Hospitais")
    observacao = db.Column(db.TEXT)


class SchemaExamesPacientesCovid(ModelSchema):
    class Meta:
        model = Exames_pacientes_covid

    paciente = fields.Nested(SchemaPacientes)
    exame = fields.Nested(SchemaExames)
    analito = fields.Nested(SchemaAnalitos)
    hospital = fields.Nested(SchemaHospitais)