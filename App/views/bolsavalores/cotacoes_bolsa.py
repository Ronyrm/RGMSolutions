from App.model.bolsavalores.cotacao_bolsa import CotacoesBolsa,SchemaCotacoesBolsa
from App import db
from sqlalchemy.sql import and_


def get_cotacao_by_papel_and_date(idpapel,dtcot):
    return CotacoesBolsa.query.\
        filter(and_(CotacoesBolsa.idpapel==idpapel,CotacoesBolsa.dt_cotacao==dtcot)).all()


def add_cotacao(data):
    getCotacao = get_cotacao_by_papel_and_date(data['idpapel'],data['dt_cotacao'])
    add = True

    if getCotacao:
        cotacao = CotacoesBolsa.query.\
        filter(and_(CotacoesBolsa.idpapel == data['idpapel'],
                    CotacoesBolsa.dt_cotacao == data['dt_cotacao'])).one()
    else:
        cotacao = CotacoesBolsa()
        db.session.add(cotacao)

    try:
        cotacao.dt_cotacao = data['dt_cotacao']
        cotacao.idpapel = data['idpapel']
        cotacao.val_compra = data['val_compra']
        cotacao.val_venda = data['val_venda']
        cotacao.val_anterior_close = data['val_anterior_close']
        cotacao.val_atual = data['val_atual']
        cotacao.val_dif = cotacao.val_anterior_close - cotacao.val_atual
        cotacao.perc_dif = ((cotacao.val_atual * 100) / cotacao.val_anterior_close) - 100
        cotacao.val_max_day = data['val_max_day']
        cotacao.val_min_day = data['val_min_day']
        cotacao.val_tot_receita = data['val_tot_receita']
        cotacao.val_vpa = data['val_vpa']
        cotacao.val_lucro_liquido = data['val_lucro_liquido']
        cotacao.val_fluxo_cx = data['val_fluxo_cx']
        cotacao.val_empresa = data['val_empresa']
        cotacao.val_mercado = data['val_mercado']
        cotacao.num_tot_acoes = data['num_tot_acoes']
        cotacao.val_ebitda = data['val_ebitda']
        cotacao.val_tot_debito = data['val_tot_debito']
        cotacao.val_lucro_bruto = data['val_lucro_bruto']
        cotacao.val_fluxo_cx_operacional = data['val_fluxo_cx_operacional']
        cotacao.val_fluxo_cx_livre_alavanc = data['val_fluxo_cx_livre_alavanc']
        cotacao.val_patr_liquido = data['val_patr_liquido']
        cotacao.val_lpa = data['val_lpa']
        cotacao.val_p_l = data['val_p_l']
        cotacao.val_p_vpa = data['val_p_vpa']
        cotacao.val_p_ebit = data['val_p_ebit']
        cotacao.val_rec_acao = data['val_rec_acao']
        cotacao.val_roe = data['val_roe']
        cotacao.val_mrg_lucro = data['val_mrg_lucro']
        cotacao.perc_tx_pagto_divi = data['perc_tx_pagto_divi']
        cotacao.ex_date_dividend = data['ex_date_dividend']
        cotacao.val_empresa_val_ebit = data['val_empresa_val_ebit']
        cotacao.val_empresa_val_rec = data['val_empresa_val_rec']
        cotacao.val_tx_dividendo = data['val_tx_dividendo']
        cotacao.perc_dividendo_yield =  data['perc_dividendo_yield']

        db.session.commit()
        return True
    except:
        return False