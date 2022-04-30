from App import db
from marshmallow_sqlalchemy import ModelSchema, fields
from App.schema.localidades.localidades import CidadesSchema


class Hospitais(db.Model):
    __tablename__ = 'hospitais'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)

class SchemaHospitais(ModelSchema):
    class Meta:
        model = Hospitais