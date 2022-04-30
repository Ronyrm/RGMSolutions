from App import db
from marshmallow_sqlalchemy import ModelSchema, fields


class CotacoesBolsa(db.Model):
    __tablename__ = 'cotacoes_bolsa'
    idpapel = db.Column(db.Integer,db.ForeignKey('empresas_bolsa.id'),primary_key=True,nullable=False)
    papel = db.relationship("EmpresaBolsa")
    dt_cotacao = db.Column(db.Date,primary_key=True,nullable=False)
    val_compra = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3))
    val_venda = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3))
    val_anterior_close = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3))
    val_atual = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3))
    perc_dif = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=2))
    val_dif = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3))
    val_max_day = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3))
    val_min_day = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3))
    val_tot_receita = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3))
    val_vpa = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3))
    val_lucro_liquido = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3))
    val_fluxo_cx = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3))
    val_empresa = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3))
    val_mercado = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3))
    num_tot_acoes = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3))
    val_ebitda = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3))
    val_tot_debito = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3))
    val_lucro_bruto = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3))
    val_fluxo_cx_operacional = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3))
    val_fluxo_cx_livre_alavanc = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3))
    val_patr_liquido = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3))
    val_lpa = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3))
    val_p_l = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3))
    val_p_vpa = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3))
    val_p_ebit = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3))
    val_empresa_val_ebit = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3))
    val_empresa_val_rec = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3))
    val_rec_acao = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3))
    val_roe = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3))
    val_mrg_lucro = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3))
    perc_tx_pagto_divi = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=2))
    val_tx_dividendo = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3))
    ex_date_dividend = db.Column(db.Date)
    perc_dividendo_yield = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=2))




class SchemaCotacoesBolsa(ModelSchema):
    class Meta:
        model = CotacoesBolsa
