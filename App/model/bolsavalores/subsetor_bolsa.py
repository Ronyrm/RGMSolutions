from App import db
from marshmallow_sqlalchemy import ModelSchema, fields


class SubSetorBolsa(db.Model):
    __tablename__ = 'sub_setores_bolsa'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)

class SchemaSubSetorBolsa(ModelSchema):
    class Meta:
        model = SubSetorBolsa