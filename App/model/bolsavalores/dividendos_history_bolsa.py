from App import db
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, fields
from .empresa_bolsa import SchemaEmpresaBolsa

class DividendosBolsa(db.Model):
    __tablename__ = 'dividendos_history_bolsa'
    idpapel = db.Column(db.Integer,db.ForeignKey('empresas_bolsa.id'),primary_key=True,nullable=False)
    papel = db.relationship("EmpresaBolsa")
    dt_pagto = db.Column(db.Date,primary_key=True,nullable=False)
    valor = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3))

class SchemaDividendosBolsa(SQLAlchemyAutoSchema):
    class Meta:
        model = DividendosBolsa
    #papel = fields.Nested(SchemaEmpresaBolsa)