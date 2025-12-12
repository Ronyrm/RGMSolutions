from App import db
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

class CFOPs(db.Model):
    __tablename__ = 'cfops'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    numcfop = db.Column(db.String(5), nullable=False)
    descricao = db.Column(db.String(100), nullable=False)

class SchemaCFOPs(SQLAlchemyAutoSchema):
    class Meta:
        model = CFOPs