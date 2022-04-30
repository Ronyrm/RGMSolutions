from App import db
from marshmallow_sqlalchemy import ModelSchema, fields


class SetorBolsa(db.Model):
    __tablename__ = 'setores_bolsa'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)

class SchemaSetorBolsa(ModelSchema):
    class Meta:
        model = SetorBolsa