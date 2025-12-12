from App import db
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema,fields
from App.model.tributacao.segmentos_cest import SchemaSegmentosCest
from App.model.tributacao.ncms import SchemaNCMS
class Cests(db.Model):
    __tablename__ = 'cests'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    codcest = db.Column(db.String(10), nullable=False)
    descricao = db.Column(db.String(100), nullable=False)
    numitem = db.Column(db.String(5))
    codncm =  db.Column(db.String(8))
    idncm = db.Column(db.Integer,db.ForeignKey('ncms.id'))
    idsegmentocest = db.Column(db.Integer,db.ForeignKey('segmentos_cest.id'))
    anexo = db.Column(db.String(50))
    segmentocest = db.relationship("SegmentosCest")
    ncm = db.relationship("NCMS")

class SchemaCests(SQLAlchemyAutoSchema):
    class Meta:
        model = Cests
    segmentocest = fields.Nested(SchemaSegmentosCest)
    ncm = fields.Nested(SchemaNCMS)