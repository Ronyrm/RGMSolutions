from App import db
from marshmallow_sqlalchemy import ModelSchema

class ClasseTerapeurica_anvisa(db.Model):
    __tablename__ = 'classe_terapeutica_anvisa'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descricao = db.Column(db.String(500), nullable=False)

class SchemaClasseTerapeutica_anvisa(ModelSchema):
    class Meta:
        model = ClasseTerapeurica_anvisa
