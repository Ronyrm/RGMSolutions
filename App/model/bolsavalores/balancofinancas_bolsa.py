from App import db
from marshmallow_sqlalchemy import ModelSchema, fields


class BalancoFinancas(db.Model):
    __tablename__ = 'balancofinancas_bolsa'
    idpapel = db.Column(db.Integer,db.ForeignKey('empresas_bolsa.id'),primary_key=True,nullable=False)
    papel = db.relationship("EmpresaBolsa")
    dt_apuracao = db.Column(db.Date,primary_key=True,nullable=False)
    val_pesquisa_desenvolvimento = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3)) # Research Development
    val_encargos_contabil = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3)) # Effect Of Accounting Charges
    val_lucro_antes_imposto = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3)) # Income Before Tax
    val_particacap_minoritario = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3)) # Minority Interest
    val_lucro_liquido = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3)) # Net Income
    val_venda_adm_geral = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3)) # Selling General Administrative
    var_lucro_bruto = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3)) #Gross Profit
    val_ebit = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3)) # Ebit
    val_renda_operacional = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3)) # Operating Income
    val_outras_despesas_operacional = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3)) #Other Operating Expenses
    val_despesas_juros = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3)) # Interest Expense
    val_itens_extraodinarios = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3)) # Extraordinary Items
    val_nao_recorrente = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3)) #Non Recurring
    val_outros_itens = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3)) # Other Items
    val_despesas_IR = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3)) # Income Tax Expense
    val_rendimento_total = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3)) # Total Revenue
    val_despesas_operacionais_total = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3)) # Total Operating Expenses
    val_custos_receitas = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3)) # Cost Of Revenue
    val_outras_receita_despesas_liquida = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3)) # Total Other Income Expense Net
    val_operacaoes_descotinuada = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3)) # Discontinued Operations
    val_lucro_liquido_operacoes_continuas = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3)) # Net Income From Continuing Ops
    val_lucro_liquido_acoes_ordinarias = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3)) # Long Term Debt

class SchemaBalancoFinancasBolsa(ModelSchema):
    class Meta:
        model = BalancoFinancas