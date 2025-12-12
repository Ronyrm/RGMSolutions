# P/L: PREÇO SOBRE O LUCRO | VPA: valor patrimonial por ação | LPA = Lucro por ação
"""

VPA =  é o valor patrimonial liquido divido pela numeros de acoes totais
Formula = val_vpa = val_patr_liq / num_acoes

LPA = primeiro encontra o LPA(lucro por ação): é o Lucro liquido divido pela numeros de acoes totais
Formula = val_lpa = val_luc_liq_12mes / num_acoes

P/L : é o preço sobre o Lucro por acao(LPA)
Formula = val_p_l = val_cotacao/LPA

P/VP = val_p_vpa = val_cotacao/VPA. Se estiver abaixo de 1, desvalorizada, o valor cotado no dia menor que o VPA


"""

# ROE: PREÇO SOBRE O LUCRO
"""
Lucro Liquido divido pelo patrimonio liquido
Formula = val_roe = val_luc_liq_12mes / vl_patr_liq 
"""

from App import db
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema,fields

class EmpresaBolsa(db.Model):
    __tablename__ = 'empresas_bolsa'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    papel = db.Column(db.String(10), nullable=False)
    name = db.Column(db.String(200))
    val_cotacao = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3))
    val_cotacao_anterior = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3))
    val_dif_cotacao = db.Column(db.NUMERIC(precision=8, asdecimal=False, scale=3))
    perc_dif_cotacao = db.Column(db.NUMERIC(precision=8, asdecimal=False, scale=2))
    val_margliq = db.Column(db.NUMERIC(precision=8, asdecimal=False, scale=3))
    val_p_l = db.Column(db.NUMERIC(precision=8, asdecimal=False, scale=3))
    val_p_vp = db.Column(db.NUMERIC(precision=8, asdecimal=False, scale=3))
    val_psr = db.Column(db.NUMERIC(precision=8, asdecimal=False, scale=3))
    val_divyield = db.Column(db.NUMERIC(precision=8, asdecimal=False, scale=3))
    perc_divyield = db.Column(db.NUMERIC(precision=8, asdecimal=False, scale=2))
    val_p_ativo = db.Column(db.NUMERIC(precision=8, asdecimal=False, scale=3))
    val_p_capgiro = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3))
    val_p_ebit = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3))
    val_p_ativocircliq = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3))
    val_ev_ebit = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3))
    val_ev_ebitda = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3))
    perc_mrg_ebit = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=2))
    perc_mrg_liq = db.Column(db.NUMERIC(precision=8, asdecimal=False, scale=2))
    val_liq_corrent = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3))
    val_roic = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3))
    val_roe = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3))
    val_liq_2meses = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3))
    val_patr_liq = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3))
    val_div_liq_patr = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=2))
    perc_cresc_rec_5a = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=2))
    val_div_liq_ebitda = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=2))
    val_mercado = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3))
    num_acoes = db.Column(db.BigInteger)
    val_firma = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3))
    dt_ult_balanco = db.Column(db.Date)
    dt_ult_cotacao = db.Column(db.Date)
    tipo = db.Column(db.String(10))
    val_min_52sem = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3))
    val_max_52sem = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3))
    val_med_2mes = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3))
    val_lpa = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3))
    val_vpa  = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3))
    val_luc_liq_12mes = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3))
    val_luc_liq_3mes = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3))
    val_luc_liq_atual = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3))
    val_rec_liq_12mes = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3))
    val_rec_liq_3mes = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3))
    val_ebit_liq_12mes = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3))
    val_ebit_liq_3mes = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3))
    val_balanc_patr_atv = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3))
    val_balanc_patr_atv_circ = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3))
    val_balanc_patr_disp = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3))
    val_balanc_patr_div_bruta = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3))
    val_balanc_patr_div_liq = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3))
    val_tot_debito = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3))
    val_lucro_bruto = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3))
    val_fluxo_cx_operacional = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3))
    val_fluxo_cx_livre_alavanc = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3))
    val_rec_acao = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3))
    val_mrg_lucro = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3))
    perc_tx_pagto_divi = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=2))
    ex_date_dividend = db.Column(db.Date)
    val_empresa_val_ebit = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3))
    desc_empresa = db.Column(db.Text)
    val_patrimonio_passado = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3))
    ativa = db.Column(db.String(1), nullable=False)
    idsetor = db.Column(db.Integer, db.ForeignKey('setores_bolsa.id'))
    setor = db.relationship("SetorBolsa")
    indicador = db.Column(db.String(1), nullable=False, default='N')
    idsubsetor = db.Column(db.Integer, db.ForeignKey('sub_setores_bolsa.id'))
    subsetor = db.relationship("SubSetorBolsa")
    avgvolume = db.Column(db.NUMERIC(precision=16, asdecimal=False, scale=3))




from App.model.bolsavalores.setor_bolsa import SchemaSetorBolsa
from App.model.bolsavalores.subsetor_bolsa import SchemaSubSetorBolsa

class SchemaEmpresaBolsa(SQLAlchemyAutoSchema):
    class Meta:
        model = EmpresaBolsa
    setor = fields.Nested(SchemaSetorBolsa)
    subsetor = fields.Nested(SchemaSubSetorBolsa)

