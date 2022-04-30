from App.model.bolsavalores.prices_cotacao_history_bolsa import CotacaoPricesHistory,SchemaCotacaoPricesHistory
from App.model.bolsavalores.empresa_bolsa import EmpresaBolsa
from App import db
from sqlalchemy.sql import and_,or_,func
from sqlalchemy import cast,Numeric,BigInteger,Integer
from flask import request
from App.funcs.funcs import CustomJSONEncoder
import json
import decimal

def get_price_cotacao_by_papel_date(papel,dt):

    price = CotacaoPricesHistory.query.\
             filter(and_(CotacaoPricesHistory.dt_cotacao == dt,CotacaoPricesHistory.idpapel == papel)).first()
    return price

# filtra cotacao por periodo de data agrupando por dia
def get_prices_cotacao_by_papel_dates(papel,dtini,dtfim):
    if request.method == 'GET':
        sfieldsvisu = request.args.get('fields') if request.args.get('fields') != None else ''
        if sfieldsvisu != '':
            sfieldsvisu = sfieldsvisu.split(',')

    try:
        int(papel)
        tipefilter = CotacaoPricesHistory.idpapel == papel
    except:
        tipefilter = EmpresaBolsa.papel==papel

    filter = and_(CotacaoPricesHistory.dt_cotacao.between(dtini,dtfim), tipefilter)

    prices = CotacaoPricesHistory.query.\
        join(EmpresaBolsa, CotacaoPricesHistory.idpapel == EmpresaBolsa.id).\
        filter(filter).\
        order_by(CotacaoPricesHistory.dt_cotacao).all()
    if prices:
        if not sfieldsvisu:
            schema = SchemaCotacaoPricesHistory()
        else:
            schema = SchemaCotacaoPricesHistory(only=sfieldsvisu)

        return {'data':schema.dump(prices,many=True),'result':True}
    return {'data':{},'result':False}

# Filtra Valor cotação agrupando por mes/ano
def get_prices_cotacao_by_papel_dates_mensal(papel,dtini,dtfim):
    typeFieldValue = Numeric(10, 2)
    if request.method == 'GET':
        tpFieldValor = request.args.get('tpfield') if request.args.get('tpfield') != None else ''
        if tpFieldValor != '':
            if tpFieldValor == 'integer':
                typeFieldValue = BigInteger
    try:
        int(papel)
        tipefilter = CotacaoPricesHistory.idpapel == papel
    except:
        tipefilter = EmpresaBolsa.papel == papel


    prices = db.session.query(func.date_format(CotacaoPricesHistory.dt_cotacao, '%m/%Y'),
                              cast(func.avg(CotacaoPricesHistory.val_fechamento),typeFieldValue)). \
        join(EmpresaBolsa, CotacaoPricesHistory.idpapel == EmpresaBolsa.id). \
        filter(CotacaoPricesHistory.dt_cotacao.between(dtini, dtfim)). \
        filter(tipefilter). \
        group_by(func.date_format(CotacaoPricesHistory.dt_cotacao, '%m/%Y')). \
        order_by(CotacaoPricesHistory.dt_cotacao).all()
    tbjson = ''
    # for row in prices:
    prices = json.dumps(prices, cls=CustomJSONEncoder)
    prices = json.loads(prices)
    return {'data':prices }


def get_prices_cotacao_by_papel_dates_anual(papel, anoini, anofim):
    typeFieldValue = Numeric(10, 2)
    if request.method == 'GET':
        tpFieldValor = request.args.get('tpfield') if request.args.get('tpfield') != None else ''
        if tpFieldValor != '':
            if tpFieldValor == 'integer':
                typeFieldValue = BigInteger

    try:
        int(papel)
        tipefilter = CotacaoPricesHistory.idpapel == papel
    except:
        tipefilter = EmpresaBolsa.papel == papel

    prices = db.session.query(func.date_format(CotacaoPricesHistory.dt_cotacao, '%Y'),
                              cast(func.avg(CotacaoPricesHistory.val_fechamento), typeFieldValue)). \
        join(EmpresaBolsa, CotacaoPricesHistory.idpapel == EmpresaBolsa.id). \
        filter(CotacaoPricesHistory.dt_cotacao.between(anoini,anofim)). \
        filter(tipefilter). \
        group_by(func.date_format(CotacaoPricesHistory.dt_cotacao, '%m/%Y')). \
        order_by(CotacaoPricesHistory.dt_cotacao).all()
    tbjson = ''
    # for row in prices:
    prices = json.dumps(prices, cls=CustomJSONEncoder)
    prices = json.loads(prices)
    return {'data': prices}


def get_prices_cotacao_ibovespa():
    if request.method == 'GET':
        tpfiltro = request.args.get('tpfiltro') if request.args.get('tpfiltro') != None else ''
        tpfiltro = int(tpfiltro if tpfiltro != '' else '0')
        tpgrupo = request.args.get('tpgrupo') if request.args.get('tpgrupo') != None else ''
        tpgrupo = int(tpgrupo if tpgrupo != '' else '0')

        order_by = CotacaoPricesHistory.dt_cotacao.asc()
        limite = 0
        grupo = func.date_format(CotacaoPricesHistory.dt_cotacao, '%d/%m/%Y')
        if tpgrupo == 1:
            grupo = func.date_format(CotacaoPricesHistory.dt_cotacao, '%m/%Y')
        elif tpgrupo == 2:
            grupo = func.date_format(CotacaoPricesHistory.dt_cotacao, '%Y')

        where = CotacaoPricesHistory.idpapel != -1
        if tpfiltro == 0:
            dtIni = request.args.get('dtini') if request.args.get('dtini') != None else ''
            dtFim = request.args.get('dtfim') if request.args.get('dtfim') != None else ''
            where = CotacaoPricesHistory.dt_cotacao.between(dtIni,dtFim)
        elif tpfiltro == 1:
            mesIni = int(request.args.get('mesini') if request.args.get('mesini') != None else '0')
            mesFim = int(request.args.get('mesfim') if request.args.get('mesfim') != None else '0')
            ano = request.args.get('ano') if request.args.get('ano') != None else '0'
            where = and_(cast(func.date_format(CotacaoPricesHistory.dt_cotacao, '%m'),Integer).between(mesIni,mesFim),
                         func.date_format(CotacaoPricesHistory.dt_cotacao, '%Y')==ano)
        elif tpfiltro == 2:
            anoIni = int(request.args.get('anoini') if request.args.get('anoini') != None else '0')
            anoFim = int(request.args.get('anofim') if request.args.get('anofim') != None else '0')
            where = cast(func.date_format(CotacaoPricesHistory.dt_cotacao, '%Y'),Integer).between(anoIni,anoFim)
        elif tpfiltro == 3:
            mes    = int(request.args.get('mes') if request.args.get('mes') != None else '0')
            anoIni = int(request.args.get('anoini') if request.args.get('anoini') != None else '0')
            anoFim = int(request.args.get('anofim') if request.args.get('anofim') != None else '0')
            where = and_(cast(func.date_format(CotacaoPricesHistory.dt_cotacao, '%Y'), Integer).between(anoIni, anoFim),
                         cast(func.date_format(CotacaoPricesHistory.dt_cotacao, '%m'), Integer) == mes)
        elif tpfiltro == 4:
            rankingpnt = request.args.get('rankingpnt') if request.args.get('rankingpnt') != None else 'DESC'
            limite = int(request.args.get('limitepnt') if request.args.get('limitepnt') != None else '0')
            anoIni = int(request.args.get('anoini') if request.args.get('anoini') != None else '0')
            anoFim = int(request.args.get('anofim') if request.args.get('anofim') != None else '0')
            where = cast(func.date_format(CotacaoPricesHistory.dt_cotacao, '%Y'), Integer).between(anoIni, anoFim)
            if rankingpnt == 'DESC':
                order_by =  cast(func.max(CotacaoPricesHistory.val_fechamento), Integer).desc()
            else:
                order_by = cast(func.max(CotacaoPricesHistory.val_fechamento), Integer).asc()

        fieldValueTotal = cast(func.sum(CotacaoPricesHistory.val_fechamento), Integer)

        if tpfiltro !=  0 and tpfiltro != 4:
            fieldValueTotal = cast(func.avg(CotacaoPricesHistory.val_fechamento), Integer)
        elif tpfiltro == 4:
            fieldValueTotal = cast(func.max(CotacaoPricesHistory.val_fechamento), Integer)

        prices = db.session.query(grupo,fieldValueTotal) \
        .join(EmpresaBolsa,CotacaoPricesHistory.idpapel==EmpresaBolsa.id) \
        .filter(where,EmpresaBolsa.papel=='^BVSP') \
        .group_by(grupo) \
        .order_by(order_by)\
        .limit(limite if limite != 0 else 9999999999999)

        #listprices = []

        try:
            pricesjson = json.dumps([row for row in prices.all()])
            #for price in prices.all():
            #    listprices.append(price)

            #jsonprices = json.dumps(pricesjson)
            #jsonprices = json.loads(jsonprices)
            return {'data': json.loads(pricesjson),'result':True}
        except Exception as e:
            return {'data': str(e)}



    return {'data': {}, 'result':False}


# ADICIONA PRECOS COTAÇÃO
def add_price_cotacao(data):
    price = get_price_cotacao_by_papel_date(data['idpapel'],data['dt_cotacao'])
    add = False
    if not price:
        price = CotacaoPricesHistory()
        add = True

    price.idpapel = data['idpapel']
    price.dt_cotacao = data['dt_cotacao']
    price.volume = data['volume']
    price.val_fechamento = data['val_fechamento']
    price.val_maior = data['val_maior']
    price.val_menor = data['val_menor']
    price.val_abertura = data['val_abertura']
    price.val_dividendos = data['val_dividendos']
    price.val_divacoes = data['val_divacoes']
    try:
        if add:
            db.session.add(price)

        db.session.commit()
        return True
    except:
        return False