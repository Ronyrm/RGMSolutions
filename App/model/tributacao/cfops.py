from App import db
from marshmallow_sqlalchemy import ModelSchema

class CFOPs(db.Model):
    __tablename__ = 'cfops'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    numcfop = db.Column(db.String(5), nullable=False)
    descricao = db.Column(db.String(100), nullable=False)

class SchemaCFOPs(ModelSchema):
    class Meta:
        model = CFOPs