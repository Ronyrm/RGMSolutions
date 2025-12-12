from App import db
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

class Substancias_anvisa(db.Model):
    __tablename__ = 'substancias_anvisa'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descricao = db.Column(db.String(500), nullable=False)

class SchemaSubstancia_anvisa(SQLAlchemyAutoSchema):
    class Meta:
        model = Substancias_anvisa
