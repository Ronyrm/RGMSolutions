from App import db
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, fields


class BalancoPatrimonial(db.Model):
    __tablename__ = 'balancopatrimonial_bolsa'
    idpapel = db.Column(db.Integer,db.ForeignKey('empresas_bolsa.id'),primary_key=True,nullable=False)
    papel = db.relationship("EmpresaBolsa")
    dt_apuracao = db.Column(db.Date,primary_key=True,nullable=False)
    val_ativos_intagiveis = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3)) # Intangible Assets
    val_total_passivos = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3)) # Total Liab
    val_patrimonio_liquido = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3)) # Total Stockholder Equity
    val_particacap_minoritario = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3)) # Minority Interest
    val_outros_passivos_correntes = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3)) # Other Current Liab
    val_total_ativos = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3)) # Total Assets
    tot_acoes_ordinaria = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3)) # Common Stock
    val_outros_ativos_correntes = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3)) # Other Current Assets
    val_lucros_acumulados = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3)) # Retained Earnings
    val_outros_debitos_obrigacoes = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3)) # Other Liab
    val_good_will = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3)) # Good Will
    tot_acoes_tesouraria = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3)) #Treasury Stock
    val_outros_ativos = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3)) # Other Assets
    val_dinheiro_cx = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3)) #cash
    val_passivo_circulante = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3)) # Total Current Liabilities
    val_cobranca_diferida_longoprazo = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3)) # Deferred Long Term Asset Charges
    val_debito_curtolongoprazo = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3)) # Short Long Term Debt
    val_outro_patrimonio_liquido = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3)) # Other Stockholder Equity
    tot_ativos_imobilizados = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3)) # Property Plant Equipment
    tot_ativos_circulantes = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3)) # Total Current Assets
    val_investimento_longoprazo = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3)) # Long Term Investments
    val_ativos_tangiveis_liquidos = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3)) #Net Tangible Assets
    val_investimento_curtoprazo = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3)) # Short Term Investiments
    val_contas_areceber_liquidas = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3)) # Net Receivables
    val_divida_longoprazo = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3)) # Long Term Debt
    val_inventario = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3)) # Inventory
    val_contas_apagar = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3)) #Accounts Payable


class SchemaBalancoPatrimonialBolsa(SQLAlchemyAutoSchema):
    class Meta:
        model = BalancoPatrimonial
