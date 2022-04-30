from App import db
from marshmallow_sqlalchemy import ModelSchema, fields
from .empresa_bolsa import SchemaEmpresaBolsa

class CotacaoPricesHistory(db.Model):
    __tablename__ = 'cotacao_prices_history_bolsa'
    idpapel = db.Column(db.Integer,db.ForeignKey('empresas_bolsa.id'),primary_key=True,nullable=False)
    papel = db.relationship("EmpresaBolsa")
    dt_cotacao = db.Column(db.Date,primary_key=True,nullable=False)
    val_abertura = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3))
    val_maior = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3))
    val_menor = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3))
    val_fechamento = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3))
    volume = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3))
    val_dividendos = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3))
    val_divacoes = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3))

class SchemaCotacaoPricesHistory(ModelSchema):
    class Meta:
        model = CotacaoPricesHistory
    #papel = fields.Nested(SchemaEmpresaBolsa)