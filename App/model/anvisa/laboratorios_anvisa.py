from App import db
from marshmallow_sqlalchemy import ModelSchema

class Laboratorios_anvisa(db.Model):
    __tablename__ = 'laboratorios_anvisa'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cnpj = db.Column(db.String(14), nullable=False)
    name = db.Column(db.String(100), nullable=False)

class SchemaLaboratorios_anvisa(ModelSchema):
    class Meta:
        model = Laboratorios_anvisa
