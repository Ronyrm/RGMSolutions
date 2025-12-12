from App import db
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
class SegmentosCest(db.Model):
    __tablename__ = 'segmentos_cest'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descricao = db.Column(db.String(100), nullable=False)
    codsegmentocest = db.Column(db.String(2))

class SchemaSegmentosCest(SQLAlchemyAutoSchema):
    class Meta:
        model = SegmentosCest