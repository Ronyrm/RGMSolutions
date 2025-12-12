from App import db
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema,fields
from App.model.anvisa.classe_terapeutica_anvisa import SchemaClasseTerapeutica_anvisa
from App.model.anvisa.substancia_anvisa import SchemaSubstancia_anvisa
from App.model.anvisa.laboratorios_anvisa import SchemaLaboratorios_anvisa
from App.model.anvisa.tiposmedicamentos_anvisa import SchemaTiposMedicamentos_anvisa


class Medicamentos_anvisa(db.Model):
    __tablename__ = 'medicamentos_anvisa'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descricao = db.Column(db.String(100), nullable=False)
    apresentacao = db.Column(db.String(100), nullable=False)
    codggrem = db.Column(db.String(15))
    registro = db.Column(db.String(13))
    ean1 = db.Column(db.String(13))
    ean2 = db.Column(db.String(13))
    ean3 = db.Column(db.String(13))
    idsubstancia = db.Column(db.Integer, db.ForeignKey('substancias_anvisa.id'))
    substancia = db.relationship("Substancias_anvisa")
    idlaboratorio = db.Column(db.Integer, db.ForeignKey('laboratorios_anvisa.id'))
    laboratorio = db.relationship("Laboratorios_anvisa")
    idclasseterapeurica = db.Column(db.Integer, db.ForeignKey('classe_terapeutica_anvisa.id'))
    classeterapeurica = db.relationship("ClasseTerapeurica_anvisa")
    idtipomedicamento = db.Column(db.Integer, db.ForeignKey('tiposmedicamentos_anvisa.id'))
    tipomedicamento = db.relationship("TiposMedicamentos_anvisa")
    tarja = db.Column(db.String(50))

class SchemaMedicamentos_anvisa(SQLAlchemyAutoSchema):
    class Meta:
        model = Medicamentos_anvisa

    substancia = fields.Nested(SchemaSubstancia_anvisa)
    laboratorio = fields.Nested(SchemaLaboratorios_anvisa)
    classeterapeurica = fields.Nested(SchemaClasseTerapeutica_anvisa)
    tipomedicamento = fields.Nested(SchemaTiposMedicamentos_anvisa)

