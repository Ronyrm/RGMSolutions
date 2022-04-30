# P/L: PREÇO SOBRE O LUCRO
"""
LPA = val_ primeiro encontra o LPA(lucro por ação): é o Lucro liquido divido pela numeros de acoes totais

"""
import datetime
import json
from datetime import  timedelta

from flask.helpers import total_seconds

from App.funcs.funcs import format_date_yyyymmaa
import numpy
import requests
import re


from App import db
from sqlalchemy.sql import and_,func
import pandas as pd
from App.model.bolsavalores.empresa_bolsa import EmpresaBolsa,SchemaEmpresaBolsa
from App.views.bolsavalores.subsetor_bolsa import get_subsetor_by_name,add_subsetor
from App.views.bolsavalores.setor_bolsa import get_setor_by_name,add_setor
from App.views.bolsavalores.dividendos_history_bolsa import add_dividendos,get_all_dividendos_by_idpapel,get_dividendos_by_idpapel_and_intervaldate,get_valor_total_diviendos_12ult_meses
from App.views.bolsavalores.cotacoes_bolsa import add_cotacao
from App.views.bolsavalores.prices_cotacao_history_bolsa import add_price_cotacao
from App.model.bolsavalores.prices_cotacao_history_bolsa import CotacaoPricesHistory
from App.model.bolsavalores.cotacao_bolsa import CotacoesBolsa
from App.views.bolsavalores.balancopatrimonial_bolsa import add_balanco_patrimonial,get_balanco_mais_recente
from App.views.bolsavalores.balancofinancas_bolsa import get_balancofinancas_by_papel_data

from App.model.bolsavalores.balancofinancas_bolsa import BalancoFinancas

from flask import jsonify,request
from App.views.several import translate

import yfinance as yf
yf.pdr_override()


def get_empresabolsa_by_papel(name):
    return EmpresaBolsa.query.filter(EmpresaBolsa.papel==name).all()


def get_empresabolsa_by_papel_dtultcotacao(name,dtcotacao):
    return EmpresaBolsa.query.\
        filter(and_(EmpresaBolsa.papel == name,
                                          EmpresaBolsa.dt_ult_cotacao == dtcotacao)).all()


def get_all_empresabolsa():
    tipo = 0
    limit = -1
    ativa = 'W'
    orderby = 0
    tipoorder = 'ASC'

    filterpl = ''
    filterpvpa = ''
    filterdividends = ''
    filtersetor = ''
    filtervalcotacao = ''

    arraypl = []
    arraypvpa = []
    arraydividends = []
    arraysetor = []
    arrayvalcotacao = []


    if request.method == 'GET':
        try:
            tipo = int(request.args.get('tipo') if request.args.get('tipo') != None else '0')
            limit = int(request.args.get('limit') if request.args.get('limit') != None else '0')
            ativa = request.args.get('ativa') if request.args.get('ativa') != None else 'W'
            tipoorder = request.args.get('tipoorder') if request.args.get('tipoorder') != None else 'ASC'
            orderby =  int(request.args.get('orderby') if request.args.get('orderby') != None else '0')

            filterpl = request.args.get('filterpl') if request.args.get('filterpl') != None else ''
            if filterpl != '':
                arraypl = filterpl.split(',')

            filterpvpa = request.args.get('filterpvpa') if request.args.get('filterpvpa') != None else ''
            if filterpvpa != '':
                arraypvpa = filterpvpa.split(',')

            filterdividends = request.args.get('filterdividends') if request.args.get('filterdividends') != None else ''
            if filterdividends != '':
                arraydividends = filterdividends.split(',')

            filtersetor = request.args.get('filtersetor') if request.args.get('filtersetor') != None else ''
            if filtersetor != '':
                arraysetor = filtersetor.split(',')

            filtervalcotacao = request.args.get('filtervalcotacao') if request.args.get('filtervalcotacao') != None else ''
            if filtervalcotacao != '':
                arrayvalcotacao = filtervalcotacao.split(',')

            filterind = request.args.get('filteind') if request.args.get('filterind') != None else 'N'
            filterind = EmpresaBolsa.indicador == filterind

        except:
            pass

        order_BY = EmpresaBolsa.papel.asc() if tipoorder == 'ASC' else EmpresaBolsa.papel.desc()
        if orderby == 1:
            order_BY = EmpresaBolsa.val_cotacao.asc() if tipoorder == 'ASC' else EmpresaBolsa.val_cotacao.desc()
        elif orderby == 2:
            order_BY = EmpresaBolsa.val_divyield.asc() if tipoorder == 'ASC' else EmpresaBolsa.val_divyield.desc()
        elif orderby == 3:
            order_BY = EmpresaBolsa.val_p_l.asc() if tipoorder == 'ASC' else EmpresaBolsa.val_p_l.desc()
        elif orderby == 4:
            order_BY = EmpresaBolsa.perc_dif_cotacao.asc() if tipoorder == 'ASC' else EmpresaBolsa.perc_dif_cotacao.desc()
        elif orderby == 5:
            orderby = EmpresaBolsa.val_p_vp.asc() if tipoorder == 'ASC' else EmpresaBolsa.val_p_vp.desc()


        if ativa != 'W':
            filter_ativa = EmpresaBolsa.ativa == ativa
        else:
            filter_ativa = EmpresaBolsa.ativa != ativa

        only = ['id', 'papel', 'name', 'setor', 'subsetor','perc_divyield',
                    'val_divyield','val_cotacao','dt_ult_cotacao','ex_date_dividend']


        if tipo == 0: # Todos os Simbolos
            empresas = EmpresaBolsa.query.\
                filter(and_(EmpresaBolsa.id!=-1,filter_ativa,filterind)).\
                order_by(order_BY).all()
        # Simbolos que contenha cotações = 1 e os que  nao apresentam = 2
        elif tipo == 1 or tipo==2:

            sub_query = db.session. \
                query(CotacaoPricesHistory.idpapel). \
                group_by(CotacaoPricesHistory.idpapel). \
                having(func.count(CotacaoPricesHistory.idpapel) > 0). \
                subquery()
            filterempresa = EmpresaBolsa.id.in_(sub_query) if tipo == 1 else ~EmpresaBolsa.id.in_(sub_query)
            empresas = EmpresaBolsa.query. \
                filter(and_(filterempresa,filter_ativa,filterind)).all()

        # Simbolos que apresentam maior pagamentos de dividendos nos ultimos 5 anos
        elif tipo == 3:
            from App.model.bolsavalores.dividendos_history_bolsa import  DividendosBolsa

            dtfim = datetime.datetime.now()
            dtini = dtfim - timedelta(days=365.25*5)

            dtini = dtini.strftime('%Y-%m-%d')
            dtfim = dtfim.strftime('%Y-%m-%d')
            sub_query = db.session.query(DividendosBolsa.idpapel).\
                join(CotacoesBolsa,DividendosBolsa.idpapel==CotacoesBolsa.idpapel).\
                filter(DividendosBolsa.dt_pagto.between(dtini,dtfim)).\
                group_by(DividendosBolsa.idpapel).\
                order_by(func.sum(DividendosBolsa.valor).desc())

            if limit != -1:
                empresas = EmpresaBolsa.query. \
                    filter(and_(EmpresaBolsa.id.in_(sub_query),filter_ativa,filterind)). \
                    order_by(order_BY).\
                    limit(limit).all()
            else:
                empresas = EmpresaBolsa.query. \
                    filter(and_(EmpresaBolsa.id.in_(sub_query),filter_ativa,filterind)).\
                    order_by(order_BY).all()
        # Simbolos que apresentam maior percentual dividendos yield atualmente
        elif tipo == 4:
            only = ['id', 'papel', 'name', 'setor', 'subsetor', 'perc_divyield',
                    'val_divyield','val_cotacao','dt_ult_cotacao',
                    'val_roe','val_lpa','val_vpa','val_p_l','val_p_vp',
                    'val_patr_liq','ex_date_dividend','desc_empresa','num_acoes','val_luc_liq_12mes']
            empresas = EmpresaBolsa.query.filter(and_(EmpresaBolsa.perc_divyield > 0,filter_ativa,filterind)).\
                order_by(order_BY)
            empresas = empresas.limit(limit).all() if limit != -1 else empresas.all()
        elif tipo == 5:
            # Setores
            if filtersetor != '':
                filtersetor = EmpresaBolsa.idsetor.in_(arraysetor)
            else:
                filtersetor = EmpresaBolsa.id != -1

            # PL
            if filterpl != '':
                filterpl = EmpresaBolsa.val_p_l.between(arraypl[0],arraypl[1])
            else:
                filterpl = EmpresaBolsa.id != -1

            # P/VPA
            if filterpvpa != '':
                filterpvpa = EmpresaBolsa.val_p_vp.between(arraypvpa[0], arraypvpa[1])
            else:
                filterpvpa = EmpresaBolsa.id != -1

            # Dividendos
            if filterdividends != '':
                filterdividends = EmpresaBolsa.perc_divyield.between(arraydividends[0],arraydividends[1])
            else:
                filterdividends = EmpresaBolsa.id != -1

            # Dividendos
            if filtervalcotacao != '':
                    filtervalcotacao = EmpresaBolsa.val_cotacao.between(arrayvalcotacao[0], arrayvalcotacao[1])
            else:
                filtervalcotacao = EmpresaBolsa.id != -1


            only = ['id', 'papel', 'name', 'setor', 'subsetor', 'perc_divyield',
                    'val_divyield', 'val_cotacao', 'dt_ult_cotacao',
                    'val_roe', 'val_lpa', 'val_vpa', 'val_p_l', 'val_p_vp',
                    'val_patr_liq', 'ex_date_dividend', 'desc_empresa', 'num_acoes', 'val_luc_liq_12mes']
            empresas = EmpresaBolsa.query.filter(and_(filterpl,filterpvpa, filterdividends, filtersetor,
                                                      filtervalcotacao, filter_ativa,filterind)). \
                order_by(order_BY)
            if limit == 0:
                empresas = empresas.all()
            else:
                empresas = empresas.limit(limit).all() if limit != -1 else empresas.all()





        #schema = SchemaEmpresaBolsa(only=only)
        schema = SchemaEmpresaBolsa()
        return {'data':schema.dump(empresas,many=True),
                'total':len(empresas),
                'only':only,
                'tipo':tipo,
                'limit': limit,
                'ativa': ativa,
                'orderby': orderby,
                'tipoorder': tipoorder,
                'filterpl': arraypl,
                'filterpvpa':arraypvpa,
                'filterdividends': arraydividends,
                'filtersetor': arraysetor,
                'filtervalcotacao': arrayvalcotacao
        }


def add_empresa(data):

    def verify_setor(name):
        if name == None:
            return None
        getsetor = get_setor_by_name(name)
        if getsetor:
            return getsetor[0].id
        return add_setor(name)['data']['id']

    def verify_subsetor(name):
        if name == None:
            return None
        getsubsetor = get_subsetor_by_name(name)
        if getsubsetor:
            return getsubsetor[0].id
        return add_subsetor(name)['data']['id']


    getempresa = get_empresabolsa_by_papel_dtultcotacao(data['papel'],data['dt_ult_cotacao'])
    add = False
    if not getempresa:
        empresa = EmpresaBolsa()
        add = True
    else:
        empresa = EmpresaBolsa.query.get(getempresa[0].id)

    try:
        empresa.papel = data['papel']
        empresa.name = data['name']
        empresa.idsetor = verify_setor(data['setor'])
        empresa.idsubsetor = verify_subsetor(data['subsetor'])
        empresa.perc_cresc_rec_5a = data['perc_cresc_rec_5a']
        empresa.perc_divyield = data['perc_divyield']
        empresa.perc_mrg_ebit = data['perc_mrg_ebit']
        empresa.perc_mrg_liq = data['perc_mrg_liq']
        empresa.val_cotacao = data['val_cotacao']
        empresa.dt_ult_cotacao = data['dt_ult_cotacao']
        empresa.val_div_liq_ebitda = data['val_div_liq_ebitda']
        empresa.val_div_liq_patr = data['val_div_liq_patr']
        empresa.val_ev_ebit = data['val_ev_ebit']
        empresa.val_ev_ebitda = data['val_ev_ebitda']
        empresa.val_firma = data['val_firma']
        empresa.val_liq_2meses = data['val_liq_2meses']
        empresa.val_liq_corrent = data['val_liq_corrent']
        empresa.val_margliq = data['val_margliq']
        empresa.val_mercado = data['val_mercado']
        empresa.val_p_ativo = data['val_p_ativo']
        empresa.val_p_ativocircliq = data['val_p_ativocircliq']
        empresa.val_p_capgiro = data['val_p_capgiro']
        empresa.val_p_ebit = data['val_p_ebit']
        empresa.val_p_l = data['val_p_l']
        empresa.val_p_vp = data['val_p_vp']
        empresa.val_patr_liq = data['val_patr_liq']
        empresa.val_psr = data['val_psr']
        empresa.val_roe = data['val_roe']
        empresa.val_roic = data['val_roic']
        empresa.dt_ult_balanco = data['dt_ult_balanco']
        empresa.num_acoes = data['num_acoes']
        empresa.val_min_52sem = data['val_min_52sem']
        empresa.val_max_52sem = data['val_max_52sem']
        empresa.val_med_2mes = data['val_med_2mes']
        empresa.tipo = data['tipo']
        empresa.val_lpa = data['val_lpa']
        empresa.val_vpa = data['val_vpa']

        empresa.val_balanc_patr_atv = data['val_balanc_patr_atv']
        empresa.val_balanc_patr_atv_circ = data['val_balanc_patr_atv_circ']
        empresa.val_balanc_patr_disp = data['val_balanc_patr_disp']
        empresa.val_balanc_patr_div_bruta = data['val_balanc_patr_div_bruta']
        empresa.val_balanc_patr_div_liq = data['val_balanc_patr_div_liq']
        empresa.val_luc_liq_12mes = data['val_luc_liq_12mes']
        empresa.val_luc_liq_3mes = data['val_luc_liq_3mes']
        empresa.val_rec_liq_12mes = data['val_rec_liq_12mes']
        empresa.val_rec_liq_3mes = data['val_rec_liq_3mes']
        empresa.val_ebit_liq_12mes = data['val_ebit_liq_12mes']
        empresa.val_ebit_liq_3mes = data['val_ebit_liq_3mes']
        empresa.val_divyield = empresa.val_cotacao * (empresa.perc_divyield / 100)

        if add:
            db.session.add(empresa)
        db.session.commit()
        return {'id':empresa.id,'papel':empresa.papel}
    except:
        pass
    return {}


def update_papel_of_fundamentus():

    def returndate(sdate):
        if len(sdate) == 10:
            dia = int(sdate[0:2])
            mes = int(sdate[3:5])
            ano = int(sdate[6:10])
            return datetime.date(ano,mes,dia)
        return None

    def return_float(str):
        if type(str) == float:
            return str
        res = re.sub('%','', str)
        res = res.replace('.','')
        res = re.sub(',','.',res)

        if len(res) == 0:
             return None
        return float(res)

    from config import UPLOAD_FOLDER
    import os


    from  bs4 import BeautifulSoup
    from App.funcs.funcs import format_date_yyyymmaa

    url = 'https://www.fundamentus.com.br/resultado.php'
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"}

    resp = requests.get(url,headers=headers).text
    #soup = BeautifulSoup(res.text,'lxml')
    #table = soup.find_all(id='resultado')[0]


    spath = os.path.join(UPLOAD_FOLDER,'arqhtml.txt')
    with open(spath,'w') as arq:
         arq.write(resp)

    df = pd.read_html(resp, decimal=',', thousands='.', encoding="UTF-8")[0]

    df = df[df['Cotação'] > 0]
    df['Cresc. Rec.5a'] = (df['Cresc. Rec.5a'].str.strip('%'))
    for row in range(106, len(df.values)):
        print('Linha {}'.format(str(row)))
        item = df.values[row]
        url = 'https://www.fundamentus.com.br/detalhes.php?papel='+item[0]
        resp = requests.get(url, headers=headers).text
        soup = BeautifulSoup(resp,'lxml')
        tables = soup.find_all('table')

        # captura tabela dados:  empresa, setor e sub setor e data ultima cotação,media valor necociado em 2 meses,
        # cotacao min e maxima

        tableone = tables[0]
        df_tb = pd.read_html(str(tableone),decimal=',', thousands='.', encoding="UTF-8")[0]
        tipo = df_tb[1][1]
        nameempresa = df_tb[1][2]
        setor = df_tb[1][3] if not pd.isna(df_tb[1][3]) else None
        subsetor = df_tb[1][4] if not pd.isna(df_tb[1][4]) else None
        dt_ult_cotacao = format_date_yyyymmaa(df_tb[3][1])
        val_min_52sem = return_float(df_tb[3][2])
        val_max_52sem = return_float(df_tb[3][3])
        val_med_2mes = return_float(df_tb[3][4])

        # captura tabela dados: valor firma, mercado, total de acoes e data ultimo balanço
        tabletwo = tables[1]
        df_tb = pd.read_html(str(tabletwo), decimal=',', thousands='.', encoding="UTF-8")[0]

        if type(df_tb[1][0]) == numpy.int64:
            val_mercado = df_tb[1][0]
        else:
            val_mercado = return_float(df_tb[1][0]) if len(df_tb[1][0]) > 1 else None

        if type(df_tb[1][1]) == numpy.int64:
            val_firma = df_tb[1][1]
        else:
            val_firma = return_float(df_tb[1][1]) if len(df_tb[1][1]) > 1 else None

        dt_ult_balanco = format_date_yyyymmaa(df_tb[3][0])

        if returndate(df_tb[3][0]) < datetime.date(2021,1,1):
           continue

        totacoes = df_tb[3][1]

        # captura tabela dados: valor firma, mercado, total de acoes e data ultimo balanço
        tabletree = tables[2]
        df_tb = pd.read_html(str(tabletree), decimal=',', thousands='.', encoding="UTF-8")[0]
        val_lpa = float(df_tb[5][1])
        val_vpa = float(df_tb[5][2])

        if val_vpa > 0:
            print(val_vpa)

        tablefour = tables[3]
        df_tb = pd.read_html(str(tablefour), decimal=',', thousands='.', encoding="UTF-8")[0]
        try:
            val_balanc_patr_atv = float(df_tb[1][1])
        except:
            val_balanc_patr_atv = None

        try:
            val_balanc_patr_atv_circ = float(df_tb[1][3])
        except:
            val_balanc_patr_atv_circ = None
        try:
            val_balanc_patr_disp = float(df_tb[1][2])
        except:
            val_balanc_patr_disp = None
        try:
            val_balanc_patr_div_bruta = float(df_tb[3][1])
        except:
            val_balanc_patr_div_bruta = None
        try:
            val_balanc_patr_div_liq = float(df_tb[3][2])
        except:
            val_balanc_patr_div_liq = None

        tablefive = tables[4]
        df_tb = pd.read_html(str(tablefive), decimal=',', thousands='.', encoding="UTF-8")[0]

        try:
            val_luc_liq_12mes = float(df_tb[1][4])
        except:
            val_luc_liq_12mes = None
        try:
            val_luc_liq_3mes = float(df_tb[3][4])
        except:
            val_luc_liq_3mes = None
        try:
            val_rec_liq_12mes = float(df_tb[1][2])
        except:
            val_rec_liq_12mes = None
        try:
            val_rec_liq_3mes = float(df_tb[3][2])
        except:
            val_rec_liq_3mes = None
        try:
            val_ebit_liq_12mes = float(df_tb[1][3])
        except:
            val_ebit_liq_12mes = None
        try:
            val_ebit_liq_3mes = float(df_tb[3][3])
        except:
            val_ebit_liq_3mes = None

        data = {'papel': item[0],
                'name':nameempresa,
                'val_lpa':val_lpa,
                'val_vpa':val_vpa,
                'val_cotacao': return_float(item[1]),
                'val_p_l': return_float(item[2]),
                'val_p_vp': return_float(item[3]),
                'val_psr': return_float(item[4]),
                'perc_divyield': return_float(item[5]),
                'val_p_ativo': return_float(item[6]),
                'val_p_capgiro': return_float(item[7]),
                'val_p_ebit': return_float(item[8]),
                'val_p_ativocircliq': return_float(item[9]),
                'val_ev_ebit': return_float(item[10]),
                'val_ev_ebitda': return_float(item[11]),
                'perc_mrg_ebit': return_float(item[12]),
                'perc_mrg_liq': return_float(item[13]),
                'val_liq_corrent': return_float(item[14]),
                'val_roic': return_float(item[15]),
                'val_roe': return_float(item[16]),
                'val_liq_2meses': return_float(item[17]),
                'val_patr_liq': return_float(item[18]),
                'val_div_liq_patr': return_float(item[19]),
                'perc_cresc_rec_5a': return_float(item[20]),
                'setor':setor,
                'subsetor':subsetor,
                'val_div_liq_ebitda':None,
                'val_firma':val_firma,
                'val_margliq':None,
                'val_mercado':val_mercado,
                'dt_ult_balanco':dt_ult_balanco,
                'dt_ult_cotacao':dt_ult_cotacao,
                'num_acoes':totacoes,
                'val_min_52sem':val_min_52sem,
                'val_max_52sem':val_max_52sem,
                'val_med_2mes': val_med_2mes,
                'tipo': tipo,
                'val_balanc_patr_atv' : val_balanc_patr_atv,
                'val_balanc_patr_atv_circ' : val_balanc_patr_atv_circ,
                'val_balanc_patr_disp' : val_balanc_patr_disp,
                'val_balanc_patr_div_bruta' : val_balanc_patr_div_bruta,
                'val_balanc_patr_div_liq' : val_balanc_patr_div_liq,
                'val_luc_liq_12mes' : val_luc_liq_12mes,
                'val_luc_liq_3mes' : val_luc_liq_3mes,
                'val_rec_liq_12mes' : val_rec_liq_12mes,
                'val_rec_liq_3mes' : val_rec_liq_3mes,
                'val_ebit_liq_12mes' : val_ebit_liq_12mes,
                'val_ebit_liq_3mes' : val_ebit_liq_3mes

        }
        empresa = add_empresa(data)
        if empresa:
            json_info_empresa = capture_info_empresa(empresa['papel'])
            if len(json_info_empresa) > 0:
                addcotacao = False
                try:
                    datacot = {
                        'dt_cotacao':data['dt_ult_cotacao'],
                        'idpapel':empresa['id'],
                        'val_compra': json_info_empresa['bid'],
                        'val_venda': json_info_empresa['ask'],
                        'val_anterior_close': json_info_empresa['previousClose'],
                        'val_atual': json_info_empresa['currentPrice'],
                        'val_max_day': json_info_empresa['dayHigh'],
                        'val_min_day': json_info_empresa['dayLow']
                    }
                    addcotacao = add_cotacao(datacot)
                except:
                    print('Nao')
                    pass

                print('Papel:{}, cotacao adicionada? {}'.format(empresa['papel'],addcotacao))


        print(item)
    return get_all_empresabolsa()


def capture_detail_yfinance(name,dt_start,dt_end):

    listname  = '{}.SA'.format(name) if name != '^BVSP' else '^BVSP'

    from yahoofinancials import YahooFinancials
    yahf = YahooFinancials(listname)
    #balancet  = yahf.get_financial_stmts('quartely','balance')
    #dividend = yahf.get_dividend_yield()
    #income_statement_data_qt = yahf.get_financial_stmts('quarterly', 'income')
    #all_statement_data_qt = yahf.get_financial_stmts('quarterly', ['income', 'cash', 'balance'])
    #apple_earnings_data = yahf.get_stock_earnings_data()
    #apple_net_income = yahf.get_net_income()
    prices_cot = {}
    if name !='^BVSPe':
        try:
            historical_stock_prices = yahf.get_historical_price_data(dt_start, dt_end, 'daily')
            prices_cot = historical_stock_prices[listname]['prices']
        except:
            pass

    msft = yf.Ticker(listname)
    #old = msft.history(start=dt_start,end=dt_end)
    #balancte_sheet = msft.get_balance_sheet(freq='yearly')
    # dta_ = yf.download(listname,start=dt_start,end=dt_end)
    # data = pdr.get_data_yahoo(listname,start=dt_start,end=dt_end)
    #
    #
    return {
    #         'balancet': balancet,
    #         'income_statement_data_qt':income_statement_data_qt,
    #         'all_statement_data_qt':all_statement_data_qt,
    #         'apple_earnings_data':apple_earnings_data,
    #         'apple_net_income':apple_net_income,
            'prices_cot':prices_cot,
            # 'dividend':dividend,
            'info': msft.info
     #       'balancte_sheet' : balancte_sheet
    }

# captura
def capture_val_cotacao_datareader_yahoo(name,start):

    #end = datetime.datetime.strptime(start,'%Y-%m-%d').date() + datetime.timedelta(days=1)
    #end = end.strftime('%Y-%m-%d')

    msft = yf.Ticker(name)

    #from pandas_datareader import data as web
    #from yahoofinancials import YahooFinancials
    #yahf = YahooFinancials(name)
    #print(yahf)
    #atual_cotacao_dia = yahf.get_historical_price_data(start, end, 'daily')
    #json_prices = atual_cotacao_dia[name]['prices'][0]
    #json_prices_div = yahf.get_daily_dividend_data(start,end)
    #for row in json_prices:
    #    print(row)


    return { 'info':msft.info}


    msft = yf.Ticker(listname)


def capture_info_empresa(name):
    msft = yf.Ticker('{}.SA'.format(name))
    return msft.info

# BUSCA E ATUALIZA TODOS OS DIVIDENDOS
def get_update_dividendos_by_papel(papel,dt_ini,dt_fim,acao):
    # se acao igual a 0 busca todos os dividendos do determinado papel
    ticker = papel
    if not re.search('.SA',papel):
        ticker = '{}.SA'.format(papel)
    try:
        dividends = yf.Ticker(ticker).dividends
        dividends = dividends if acao == '0' else dividends.loc[format_date_yyyymmaa(dt_ini):format_date_yyyymmaa(dt_fim)]
        array_datas = dividends.axes[0]
    except:
        return {'data': {}, f'mensagem': f'Erro ao encontrar Papel: {papel}'}
    cont = 0
    empresa = get_empresabolsa_by_papel(papel.replace('.SA',''))
    if not empresa:
        return {'data':{},'mensagem':'Empresa não encontrada'}
    idpapel = empresa[0].id

    for row in dividends:
        dt_pagto = array_datas[cont].strftime('%Y-%m-%d')
        data = {
            'idpapel': idpapel,
            'dt_pagto' : dt_pagto,
            'valor': row
        }
        print('Gravou Dividendo na data: {} :  {}'.format(dt_pagto,add_dividendos(data)))
        cont +=1

    return get_all_dividendos_by_idpapel(idpapel) if acao == '0'  else get_dividendos_by_idpapel_and_intervaldate(idpapel,dt_ini,dt_fim)

# ATUALIZA TODAS AS EMPRESAS

def up_cotacoes(df_cotacoes,idpapel):
    array_datas = df_cotacoes.axes[0]
    cont = 0
    for row in df_cotacoes.values:
        dt_cotacao = array_datas[cont].strftime('%Y-%m-%d')
        data = {
            'idpapel': idpapel,
            'dt_cotacao': dt_cotacao,
            'val_abertura': row[0],
            'val_maior': row[1],
            'val_menor': row[2],
            'val_fechamento': row[3],
            'volume': row[4],
            'val_dividendos': row[5],
            'val_divacoes': row[6]
        }
        print('Gravou Cotação na data: {} :  {}'.format(dt_cotacao, add_price_cotacao(data)))
        cont +=1


def update_data_papel_with_yfinance(dtini,dtfim):
    empresas = get_all_empresabolsa()

    def up_dividendos(df_dividendos,idpapel):
        array_datas = df_dividendos.axes[0]
        cont = 0
        for row in df_dividendos:
            dt_pagto = array_datas[cont].strftime('%Y-%m-%d')
            data = {
                'idpapel': idpapel,
                'dt_pagto': dt_pagto,
                'valor': row
            }
            print('Gravou Dividendo na data: {} :  {}'.format(dt_pagto, add_dividendos(data)))
            cont+=1

    if empresas:
        for empresa in empresas['data']:
            yftk = yf.Ticker('{}.SA'.format(empresa['papel']))

            dividendos = yftk.dividends
            dividendos = dividendos.loc[dtini:dtfim]

            up_dividendos(dividendos,empresa['id'])

            hist_prices = yftk.history(start=dtini,end=dtfim)
            up_cotacoes(hist_prices,empresa['id'])

    return jsonify({'atualizado':True})


# ATUALIZA DADOS ATUAIS DIARIO DE UMA DETERMINADA  EMPRESA
def update_dados_empresa(datacot):
    try:
        empresa = EmpresaBolsa.query.get(datacot['idpapel'])
        if empresa:
            jsonTotalDiv12 = get_valor_total_diviendos_12ult_meses(datacot['idpapel'])

            empresa.perc_divyield = jsonTotalDiv12['perc_div_yield']
            empresa.val_divyield = jsonTotalDiv12['valor_div_yield']
            empresa.val_lpa = datacot['val_lpa']
            empresa.val_vpa = datacot['val_vpa']
            empresa.val_firma = datacot['val_empresa']
            empresa.val_empresa = datacot['val_empresa']
            empresa.val_mercado = datacot['val_mercado']
            empresa.val_cotacao = datacot['val_atual']
            empresa.val_cotacao_anterior = datacot['val_anterior_close'] if datacot['val_anterior_close'] != None else 0
            empresa.val_dif_cotacao = empresa.val_cotacao - empresa.val_cotacao_anterior
            empresa.perc_dif_cotacao = 0 if empresa.val_cotacao_anterior == 0 else ((empresa.val_cotacao * 100) / empresa.val_cotacao_anterior) - 100
            empresa.perc_dif_cotacao = 0 if empresa.perc_dif_cotacao == None else empresa.perc_dif_cotacao
            empresa.dt_ult_cotacao = datacot['dt_cotacao']
            empresa.val_patr_liq = datacot['val_patr_liquido']
            empresa.num_acoes = datacot['num_tot_acoes']
            empresa.val_luc_liq_12mes = datacot['val_lucro_liquido12']
            empresa.val_luc_liq_3mes = datacot['val_lucro_liquido3']
            empresa.val_luc_liq_atual = datacot['val_lucro_liquido']
            empresa.val_roe = round((empresa.val_luc_liq_atual / empresa.val_patr_liq) * 100,2)
            empresa.val_ebit_liq_12mes = datacot['val_ebitda']
            empresa.val_tot_debito = datacot['val_tot_debito']
            empresa.val_lucro_bruto = datacot['val_lucro_bruto']
            empresa.val_fluxo_cx_operacional = datacot['val_fluxo_cx_operacional']
            empresa.val_fluxo_cx_livre_alavanc = datacot['val_fluxo_cx_livre_alavanc']
            empresa.val_p_l = datacot['val_p_l']
            empresa.val_p_vp = datacot['val_p_vpa']
            empresa.val_p_ebit = datacot['val_p_ebit']
            empresa.val_rec_acao = datacot['val_rec_acao']
            empresa.val_mrg_lucro = datacot['val_mrg_lucro']
            empresa.perc_tx_pagto_divi = datacot['perc_tx_pagto_divi']
            empresa.ex_date_dividend = datacot['ex_date_dividend']
            empresa.val_empresa_val_ebit = datacot['val_empresa_val_ebit']
            empresa.dt_ult_cotacao = datacot['dt_cotacao']
            empresa.val_patrimonio_passado = datacot['val_patrimonio_passado']
            empresa.ativa = 'S'
            if datacot['desc_empresa'] != None:
                json_transale = translate(datacot['desc_empresa'],'en','pt')
                empresa.desc_empresa = json_transale['traducao']

            db.session.commit()
            return True
    except:
        pass
    return False



def up_history_cotacoes(df_cotacoes,idpapel):
    array_datas = df_cotacoes.axes[0]
    cont = 0
    result = True
    msgErro = ''
    for row in df_cotacoes.values:
        dt_cotacao = array_datas[cont].strftime('%Y-%m-%d')
        try:
            data = {
                'idpapel': idpapel,
                'dt_cotacao': dt_cotacao,
                'val_abertura': round(row[0],3),
                'val_maior': round(row[1],3),
                'val_menor': round(row[2],3),
                'val_fechamento': round(row[3],3),
                'volume': row[4],
                'val_dividendos': round(row[5],3),
                'val_divacoes': round(row[6],3)
            }
            print('Gravou Cotação na data: {} :  {}'.format(dt_cotacao, add_price_cotacao(data)))
        except:
            msgErro += dt_cotacao+', '
        cont +=1
    msg = 'Sucesso'
    if len(msgErro) > 0:
        result = False
        msgErro = 'Erro ao gravar a(s) data(s):'+msgErro[0:len(msgErro)-2]
        msg = 'Erro'



    return {'result':result,'msgErro':msgErro,'msg':msg}

def update_data_papel_with_yfinance_by_papel(idpapel,papel,dtini,dtfim):

    def up_balance_trimenstral(df_balance_sheet):
        if len(df_balance_sheet) == 0 :
            return None
        array_datas = df_balance_sheet.axes[1]
        cont = 0
        val_patrimonio = 0
        def capture_value(namefield,dt_):
            try:
                return df_balance_sheet.loc[namefield,dt_][0]
            except:
                return None

        for dt_row in array_datas:
            dt_balanco = dt_row.strftime('%Y-%m-%d')
            if val_patrimonio == 0:
                val_patrimonio = capture_value('Total Stockholder Equity',dt_balanco)


            data_balanco = {
                'idpapel':idpapel,
                'dt_apuracao': dt_balanco,
                'val_ativos_intagiveis' : capture_value('Intangible Assets',dt_balanco),
                'val_total_passivos': capture_value('Total Liab',dt_balanco),
                'val_patrimonio_liquido': capture_value('Total Stockholder Equity',dt_balanco),
                'val_particacap_minoritario': capture_value('Minority Interest',dt_balanco),
                'val_outros_passivos_correntes': capture_value('Other Current Liab',dt_balanco),
                'val_total_ativos': capture_value('Total Assets',dt_balanco),
                'tot_acoes_ordinaria': capture_value('Common Stock',dt_balanco),
                'val_outros_ativos_correntes': capture_value('Other Current Assets',dt_balanco),
                'val_lucros_acumulados': capture_value('Retained Earnings',dt_balanco),
                'val_outros_debitos_obrigacoes': capture_value('Other Liab',dt_balanco),
                'val_good_will': capture_value('Good Will',dt_balanco),
                'tot_acoes_tesouraria': capture_value('Treasury Stock',dt_balanco),
                'val_outros_ativos': capture_value('Other Assets',dt_balanco),
                'val_dinheiro_cx': capture_value('Cash',dt_balanco),
                'val_passivo_circulante': capture_value('Total Current Liabilities',dt_balanco),
                'val_cobranca_diferida_longoprazo': capture_value('Deferred Long Term Asset Charges',dt_balanco),
                'val_debito_curtolongoprazo': capture_value('Short Long Term Debt',dt_balanco),
                'val_outro_patrimonio_liquido': capture_value('Other Stockholder Equity',dt_balanco),
                'tot_ativos_imobilizados': capture_value('Property Plant Equipment',dt_balanco),
                'tot_ativos_circulantes': capture_value('Total Current Assets',dt_balanco),
                'val_investimento_longoprazo': capture_value('Long Term Investments',dt_balanco),
                'val_ativos_tangiveis_liquidos': capture_value('Net Tangible Assets',dt_balanco),
                'val_investimento_curtoprazo': capture_value('Short Term Investments',dt_balanco),
                'val_contas_areceber_liquidas': capture_value('Net Receivables',dt_balanco),
                'val_divida_longoprazo': capture_value('Long Term Debt',dt_balanco),
                'val_inventario': capture_value('Inventory',dt_balanco),
                'val_contas_apagar': capture_value('Accounts Payable',dt_balanco)
            }
            addbalanco =  add_balanco_patrimonial(data_balanco)
            print(f"Balanco Patrimonial do papel : {papel} na data {dt_balanco} add com sucesso? Resp:.{'Sim' if addbalanco else 'Não'}")
        return  val_patrimonio
    def up_dividendos(df_dividendos,idpapel):
        array_datas = df_dividendos.axes[0]
        cont = 0
        for row in df_dividendos:
            dt_pagto = array_datas[cont].strftime('%Y-%m-%d')
            data = {
                'idpapel': idpapel,
                'dt_pagto': dt_pagto,
                'valor': row
            }
            print('Gravou Dividendo na data: {} :  {}'.format(dt_pagto, add_dividendos(data)))
            cont+=1
    def cotacao_now(dfinfo,idpapel,val_patrimonio_passado,val_lucroliquido12,val_lucroliquido3):
        addcotacao = False
        try:
            numactions = None if  dfinfo['netIncomeToCommon'] == None or dfinfo['trailingEps'] == None \
                else int(dfinfo['netIncomeToCommon'] / dfinfo['trailingEps'])
            datacot = {
                'val_lucro_liquido12':val_lucroliquido12,
                'val_lucro_liquido3': val_lucroliquido3,
                'desc_empresa':dfinfo['longBusinessSummary'],
                'val_patrimonio_passado':val_patrimonio_passado,
                'dt_cotacao': datetime.datetime.now().strftime('%y-%m-%d'),
                'idpapel': idpapel,
                'val_compra': dfinfo['bid'],
                'val_venda': dfinfo['ask'],
                'val_anterior_close': dfinfo['previousClose'],
                'val_atual': dfinfo['currentPrice'],
                'val_max_day': dfinfo['dayHigh'],
                'val_min_day': dfinfo['dayLow'],
                'val_tot_receita' : dfinfo['totalRevenue'],
                'val_vpa' : dfinfo['bookValue'],
                'val_lucro_liquido' : dfinfo['netIncomeToCommon'],
                'val_fluxo_cx' : dfinfo['totalCash'],
                'val_empresa' : dfinfo['enterpriseValue'],
                'val_mercado' : dfinfo['marketCap'],
                'num_tot_acoes' : numactions,
                'val_ebitda' : dfinfo['ebitda'],
                'val_tot_debito' : dfinfo['totalDebt'],
                'val_lucro_bruto' : dfinfo['grossProfits'],
                'val_fluxo_cx_operacional' : dfinfo['operatingCashflow'],
                'val_fluxo_cx_livre_alavanc' : dfinfo['freeCashflow'],
                'val_patr_liquido' : None if numactions == None or  dfinfo['bookValue'] == None else numactions * dfinfo['bookValue'],
                'val_lpa' : dfinfo['trailingEps'],
                'val_p_l' : None if numactions == None or
                                    dfinfo['netIncomeToCommon'] == None or
                                    dfinfo['currentPrice'] == None
                                 else (dfinfo['currentPrice'] /  (dfinfo['netIncomeToCommon'] / numactions)),
                'val_p_vpa' : None if dfinfo['bookValue'] == None or  dfinfo['currentPrice'] == None else dfinfo['currentPrice'] / dfinfo['bookValue'],
                'val_p_ebit' : None if dfinfo['ebitda'] == None or
                                       dfinfo['currentPrice'] == None or
                                       numactions == None
                                    else ((dfinfo['currentPrice'] / dfinfo['ebitda'] / numactions)),
                'val_rec_acao' : None if dfinfo['totalRevenue'] == None or
                                         numactions == None
                                      else dfinfo['totalRevenue'] / numactions,
                'val_roe' : None if dfinfo['netIncomeToCommon'] == None or
                                    numactions == None or
                                    dfinfo['bookValue'] == None
                                 else (((dfinfo['netIncomeToCommon'] / numactions) * dfinfo['bookValue']) *100),
                'val_mrg_lucro' :  None if dfinfo['netIncomeToCommon'] == None or
                                    dfinfo['totalRevenue'] == None
                                 else ((dfinfo['netIncomeToCommon'] / dfinfo['totalRevenue']) * 100),
                'perc_tx_pagto_divi' : None if dfinfo['payoutRatio'] == None else round(dfinfo['payoutRatio'] * 100,2),
                'ex_date_dividend': None if dfinfo['exDividendDate'] == None else  (datetime.datetime.fromtimestamp(int(dfinfo['exDividendDate'])) + timedelta(days=1)).strftime('%Y-%m-%d'),
                'val_empresa_val_ebit': dfinfo['enterpriseToEbitda'],
                'val_empresa_val_rec': dfinfo['enterpriseToRevenue'],
                'val_tx_dividendo': dfinfo['dividendRate'],
                'perc_dividendo_yield': None if dfinfo['dividendYield'] == None else round(
                    (dfinfo['dividendYield'] * 100),1)
            }
            upt_empresa = update_dados_empresa(datacot)
            addcotacao = add_cotacao(datacot)
        except:
            pass
        return addcotacao

    totdiv = 0
    try:
        if papel != '^BVSP':
            yftk = yf.Ticker('{}.SA'.format(papel))
            totdiv = len(yftk.actions)
        else:
            yf.Ticker(papel)
            totdiv = 1
    except:
        totdiv = -1

    if totdiv > 0:
        try:
            df_balancetFinancials = yftk.quarterly_financials
            if len(df_balancetFinancials) > 0:
                update_balanco_finances_yfinance_by_papel(df_balancetFinancials,idpapel)
                lucroliquido12meses = df_balancetFinancials.loc['Net Income'].sum()
                lucroliquido3meses = df_balancetFinancials.loc['Net Income'].iloc[0]
                get_val_patrimonio = up_balance_trimenstral(yftk.quarterly_balancesheet)

            dfinfo = yftk.info

            dividendos = yftk.dividends
            if len(dividendos) > 0:
                dividendos = dividendos.loc[dtini:dtfim]
                if len(dividendos) > 0:
                    up_dividendos(dividendos, idpapel)

            addcotacao = cotacao_now(dfinfo,idpapel,get_val_patrimonio,lucroliquido12meses,lucroliquido3meses)


            hist_prices = yftk.history(start=dtini,end=dtfim)
            if len(hist_prices)>0:
                up_history_cotacoes(hist_prices,idpapel)

            return {'atualizado':True,'totdiv': totdiv,'papel': papel}
        except:
            pass

    return {'atualizado': False,'totdiv': totdiv,'papel': papel}


def get_update_info_yfinance_by_papel(idpapel,papel):
    result = False

    totdiv = True
    try:
        if papel != '^BVSP':
            yftk = yf.Ticker('{}.SA'.format(papel))
        else:
            yf.Ticker(papel)
    except:
        totdiv = False

    if totdiv:
        dfinfo = yftk.info
        if dfinfo['regularMarketPrice'] != None:


            maxreg = get_balanco_mais_recente(idpapel)
            val_patrimonio_passado = maxreg[0].val_patrimonio_liquido if maxreg else None

            df_balancetFinancials = yftk.quarterly_financials
            if len(df_balancetFinancials)>0:
                lucroliquido12meses = df_balancetFinancials.loc['Net Income Applicable To Common Shares'].sum()
                lucroliquido3meses = df_balancetFinancials.loc['Net Income Applicable To Common Shares'].iloc[0]

            try:
                numactions = None if dfinfo['netIncomeToCommon'] == None or dfinfo['trailingEps'] == None \
                else int(dfinfo['netIncomeToCommon'] / dfinfo['trailingEps'])

                datacot = {
                    'desc_empresa': dfinfo['longBusinessSummary'],
                    'val_patrimonio_passado': val_patrimonio_passado,
                    'dt_cotacao': datetime.datetime.now().strftime('%y-%m-%d'),
                    'idpapel': idpapel,
                    'val_compra': dfinfo['bid'],
                    'val_venda': dfinfo['ask'],
                    'val_anterior_close': dfinfo['previousClose'],
                    'val_atual': dfinfo['currentPrice'],
                    'val_max_day': dfinfo['dayHigh'],
                    'val_min_day': dfinfo['dayLow'],
                    'val_tot_receita': dfinfo['totalRevenue'],
                    'val_vpa': dfinfo['bookValue'],
                    'val_lucro_liquido': dfinfo['netIncomeToCommon'],
                    'val_lucro_liquido12': lucroliquido12meses,
                    'val_lucro_liquido3': lucroliquido3meses,
                    'val_fluxo_cx': dfinfo['totalCash'],
                    'val_empresa': dfinfo['enterpriseValue'],
                    'val_mercado': dfinfo['marketCap'],
                    'num_tot_acoes': numactions,
                    'val_ebitda': dfinfo['ebitda'],
                    'val_tot_debito': dfinfo['totalDebt'],
                    'val_lucro_bruto': dfinfo['grossProfits'],
                    'val_fluxo_cx_operacional': dfinfo['operatingCashflow'],
                    'val_fluxo_cx_livre_alavanc': dfinfo['freeCashflow'],
                    'val_patr_liquido': None if numactions == None or dfinfo['bookValue'] == None else numactions * dfinfo[
                        'bookValue'],
                    'val_lpa': dfinfo['trailingEps'],
                    'val_p_l': None if numactions == None or
                                       dfinfo['netIncomeToCommon'] == None or
                                       dfinfo['currentPrice'] == None
                    else (dfinfo['currentPrice'] / (dfinfo['netIncomeToCommon'] / numactions)),
                    'val_p_vpa': None if dfinfo['bookValue'] == None or dfinfo['currentPrice'] == None else dfinfo[
                                                                                                                'currentPrice'] /
                                                                                                            dfinfo[
                                                                                                                'bookValue'],
                    'val_p_ebit': None if dfinfo['ebitda'] == None or
                                          dfinfo['currentPrice'] == None or
                                          numactions == None
                    else ((dfinfo['currentPrice'] / dfinfo['ebitda'] / numactions)),
                    'val_rec_acao': None if dfinfo['totalRevenue'] == None or
                                            numactions == None
                    else dfinfo['totalRevenue'] / numactions,
                    'val_roe': None if dfinfo['netIncomeToCommon'] == None or
                                       numactions == None or
                                       dfinfo['bookValue'] == None
                    else (((dfinfo['netIncomeToCommon'] / numactions) * dfinfo['bookValue']) * 100),
                    'val_mrg_lucro': None if dfinfo['netIncomeToCommon'] == None or
                                             dfinfo['totalRevenue'] == None
                    else ((dfinfo['netIncomeToCommon'] / dfinfo['totalRevenue']) * 100),
                    'perc_tx_pagto_divi': None if dfinfo['payoutRatio'] == None else round(dfinfo['payoutRatio'] * 100, 2),
                    'ex_date_dividend': None if dfinfo['exDividendDate'] == None else (
                                datetime.datetime.fromtimestamp(int(dfinfo['exDividendDate'])) + timedelta(
                            days=1)).strftime('%Y-%m-%d'),
                    'val_empresa_val_ebit': dfinfo['enterpriseToEbitda'],
                    'val_empresa_val_rec': dfinfo['enterpriseToRevenue'],
                    'val_tx_dividendo': dfinfo['dividendRate'],
                    'perc_dividendo_yield': None if dfinfo['dividendYield'] == None else round(
                        (dfinfo['dividendYield'] * 100), 1)
                }
                result = update_dados_empresa(datacot)
            except:
                pass

    if result:
        empresa = get_empresabolsa_by_papel(papel)
        schema = SchemaEmpresaBolsa()
        return  {'data': schema.dump(empresa,many=True), 'result':result}
    else:
        return {'data': {}, 'result': result}


def update_balanco_finances_yfinance_by_papel(dffincances,idpapel):

    def capture_value(namefield, dt_):
        try:
            val =  dffincances.loc[namefield, dt_][0]
            if pd.isna(val):
                return  None
            return val
        except:
            return None
    if len(dffincances) == 0:
        return None
    array_datas = dffincances.axes[1]

    for dt_row in array_datas:
        dt_apuracao = dt_row.strftime('%Y-%m-%d')
        try:
            balanco = get_balancofinancas_by_papel_data(idpapel,dt_apuracao)
            add = False
            if not balanco:
                balanco = BalancoFinancas()
                add = True
            balanco.idpapel = idpapel
            balanco.dt_apuracao = dt_apuracao
            balanco.val_pesquisa_desenvolvimento = capture_value('Research Development',dt_apuracao)
            balanco.val_encargos_contabil = capture_value('Effect Of Accounting Charges',dt_apuracao)
            balanco.val_lucro_antes_imposto = capture_value('Income Before Tax',dt_apuracao)
            balanco.val_particacap_minoritario = capture_value('Minority Interest',dt_apuracao)
            balanco.val_lucro_liquido = capture_value('Net Income',dt_apuracao)
            balanco.val_venda_adm_geral = capture_value('Selling General Administrative',dt_apuracao)
            balanco.var_lucro_bruto = capture_value('Gross Profit',dt_apuracao)
            balanco.val_ebit = capture_value('Ebit',dt_apuracao)
            balanco.val_renda_operacional = capture_value('Operating Income',dt_apuracao)
            balanco.val_outras_despesas_operacional = capture_value('Other Operating Expenses',dt_apuracao)
            balanco.val_despesas_juros = capture_value('Interest Expense',dt_apuracao)
            balanco.val_itens_extraodinarios = capture_value('Extraordinary Items',dt_apuracao)
            balanco.val_nao_recorrente = capture_value('Non Recurring',dt_apuracao)
            balanco.val_outros_itens = capture_value('Other Items',dt_apuracao)
            balanco.val_despesas_IR = capture_value('Income Tax Expense',dt_apuracao)
            balanco.val_rendimento_total = capture_value('Total Revenue',dt_apuracao)
            balanco.val_despesas_operacionais_total = capture_value('Total Operating Expenses',dt_apuracao)
            balanco.val_custos_receitas = capture_value('Cost Of Revenue',dt_apuracao)
            balanco.val_outras_receita_despesas_liquida = capture_value('Total Other Income Expense Net',dt_apuracao)
            balanco.val_operacaoes_descotinuada = capture_value('Discontinued Operations',dt_apuracao)
            balanco.val_lucro_liquido_operacoes_continuas = capture_value('Net Income From Continuing Ops',dt_apuracao)
            balanco.val_lucro_liquido_acoes_ordinarias = capture_value('Long Term Debt',dt_apuracao)

            if add: db.session.add(balanco)
            db.session.commit()
        except:
            print(f'Erro ao gravar balancete financas data {dt_apuracao} para o papel {idpapel}')
            pass


def convert_tickers_csv_statusinvest():
    class simbolsStatus:
        def __init__(self, simbol,info):
            self.simbol = simbol
            self.info =info

        def toJSON(self):
            return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


    from werkzeug.utils import secure_filename
    from App import app
    import os
    if request.method == 'POST':
        if 'filecsv' in request.files:
            filecsv = request.files['filecsv']

            filename = secure_filename(filecsv.filename)
            localsaver = app.config['UPLOAD_FOLDER']
            spath = os.path.join(localsaver,filename)
            if os.path.exists(spath):
                os.remove(spath)
            filecsv.save(spath)
            simbols = None
            df = None
            try:
                df = pd.read_csv(spath,delimiter=';')
                simbols = df.loc[:, 'TICKER']

            except:
                pass

            for index, simbol in enumerate(simbols):
                rowsimbol = df.loc[df['TICKER'] == simbol]
                preco = rowsimbol['PRECO'][index]
                print(simbol)

            empresas = get_all_empresabolsa(0)
            totalencontrada = 0
            totalnaoencontrada = 0
            arrayNaoEncontrada = []
            totEmpresas = len(empresas['data'])
            for index,empresa in enumerate(empresas['data']):
                print(f'Pos:{str(index)} de {str(totEmpresas)}')
                dfemp =  df.loc[df['TICKER'] == empresa['papel']]
                ativa = 'S'
                if len(dfemp) == 0:

                    simboltt = simbolsStatus(empresa['papel'],False)
                    arrayNaoEncontrada.append(json.loads(simboltt.toJSON()))
                    totalnaoencontrada +=1
                    ativa = 'N'
                else:
                    totalencontrada +=1

                empresa = EmpresaBolsa.query.filter(EmpresaBolsa.papel == empresa['papel']).first()
                if empresa:
                    empresa.ativa = ativa
                    db.session.commit()

            print(f'Total Encontradas: {totalencontrada}, Total Não Encontradas: {totalnaoencontrada} \n')
            print(arrayNaoEncontrada)

            return arrayNaoEncontrada


def get_info_Ibovespa():
    empresa = EmpresaBolsa.query.filter(EmpresaBolsa.papel=='^BVSP').first()
    if empresa:
        yfBov = yf.Ticker('^BVSP')
        try:
            empresa.val_cotacao_anterior = yfBov.info['previousClose']
            empresa.val_cotacao = yfBov.info['regularMarketPrice']
            empresa.val_dif_cotacao = empresa.val_cotacao - empresa.val_cotacao_anterior
            empresa.perc_dif_cotacao = ((empresa.val_cotacao / empresa.val_cotacao_anterior * 100) - 100)
            empresa.avgvolume = yfBov.info['averageVolume']
            db.session.commit()

            empresa = get_empresabolsa_by_papel('^BVSP')
            schema = SchemaEmpresaBolsa()

            return {'data':schema.dump(empresa,many=True),'result':True}

        except:
            pass
    return {'data':{},'result':False}

def update_History_Values_Ibovespa(dtini,dtfim):
    empresa = EmpresaBolsa.query.filter(EmpresaBolsa.papel == '^BVSP').first()
    if empresa:
        yfBov = yf.Ticker('^BVSP')
        history = yfBov.history(start=dtini,end=dtfim)
        if len(history)>0:
            return up_history_cotacoes(history,empresa.id)
        else:
            return {'result':True,'msg':'Vazio'}
