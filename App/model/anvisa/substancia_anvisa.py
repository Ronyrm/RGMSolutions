from App import db
from marshmallow_sqlalchemy import ModelSchema

class Substancias_anvisa(db.Model):
    __tablename__ = 'substancias_anvisa'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descricao = db.Column(db.String(500), nullable=False)

class SchemaSubstancia_anvisa(ModelSchema):
    class Meta:
        model = Substancias_anvisa
