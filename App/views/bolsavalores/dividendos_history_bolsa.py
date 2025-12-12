import json

import sqlalchemy
from App.model.bolsavalores.dividendos_history_bolsa import DividendosBolsa,SchemaDividendosBolsa
from App.model.bolsavalores.empresa_bolsa import EmpresaBolsa
from App import db
from sqlalchemy.sql import and_,or_,func
from sqlalchemy import cast,FLOAT
from flask import request
import pandas as pd
from datetime import datetime,timedelta

from flask_marshmallow import Marshmallow


def get_dividendos_by_idpapel_and_data(idpapel,datapagto):
    return DividendosBolsa.query.filter(and_(DividendosBolsa.idpapel == idpapel,
                                             DividendosBolsa.dt_pagto==datapagto)).all()



def get_all_dividendos_by_idpapel(idpapel):
    dividendos = DividendosBolsa.query.\
        join(EmpresaBolsa,DividendosBolsa.idpapel==EmpresaBolsa.id).\
        filter(or_(DividendosBolsa.idpapel==idpapel,EmpresaBolsa.papel==idpapel)).all()
    if dividendos:
        schema = SchemaDividendosBolsa()
        result_json = schema.dump(dividendos,many=True)
        df = pd.DataFrame(result_json)
        df_data = df.loc[:,['dt_pagto','valor']]

        groupby_ano = df_data.groupby(pd.DatetimeIndex(df['dt_pagto']).to_period('Y')).sum()
        groupby_mes = df_data.groupby(pd.DatetimeIndex(df['dt_pagto']).to_period('M')).sum()
        return {'data':result_json,'total':df['valor'].sum(),
                'total_ano':json.loads(groupby_ano.to_json()),
                'total_mes':json.loads(groupby_mes.to_json())}
    return {'data':{},'total':0}


def get_dividendos_by_idpapel_and_intervaldate(papel,dt_ini,dt_fim):
    try:
        int(papel)
        tipefilter = DividendosBolsa.idpapel == papel
    except:
        tipefilter = EmpresaBolsa.papel==papel

    dividendos = DividendosBolsa.query.\
        join(EmpresaBolsa,DividendosBolsa.idpapel==EmpresaBolsa.id).\
        filter(and_(DividendosBolsa.dt_pagto.between(dt_ini,dt_fim),
                    tipefilter)).\
        order_by(DividendosBolsa.dt_pagto).all()
    if dividendos:

        schema = SchemaDividendosBolsa()
        result_json = schema.dump(dividendos,many=True)
        df = pd.DataFrame(result_json)

        return {'data': result_json,'total':df['valor'].sum()}
    return {'data':{},'total':0}


def get_dividendos_mesano_by_idpapel_and_interval_mensal(papel,dt_ini,dt_fim):

    tpdate = 0
    if request.method == 'GET':
        tpdate = int(request.args.get('tpdate') if request.args.get('tpdate') != None else '0')

    if tpdate == 0:
        tpdate = func.date_format(DividendosBolsa.dt_pagto, '%m/%Y')
    elif tpdate == 1:
        tpdate = cast(func.date_format(DividendosBolsa.dt_pagto, '%Y'),sqlalchemy.Integer)
    try:
        int(papel)
        tipefilter = DividendosBolsa.idpapel == papel
    except:
        tipefilter = EmpresaBolsa.papel==papel

    try:
        dividendos = db.session.query(tpdate,
                                      func.sum(DividendosBolsa.valor)).\
            join(EmpresaBolsa,DividendosBolsa.idpapel==EmpresaBolsa.id).\
            filter(DividendosBolsa.dt_pagto.between(dt_ini,dt_fim)).\
            filter(tipefilter).\
            group_by(tpdate).\
            order_by(DividendosBolsa.dt_pagto).all()
        data = []
        for row in dividendos:
            data.append(list(row))
        jsonDiv = json.dumps(data)
        jsonDiv = json.loads(jsonDiv)

        return {'data':jsonDiv,'result':True,'total':len(dividendos),'error':''}
    except Exception as e:
        return {'data':{},'result':False,'total':0,'error': str(e),'error':'teste'}

    


def add_dividendos(data):
    dividendo = DividendosBolsa.query.filter(and_(DividendosBolsa.idpapel == data['idpapel'],
                                             DividendosBolsa.dt_pagto==data['dt_pagto'])).first()
    try:
        add = False
        if not dividendo:
            dividendo = DividendosBolsa()
            add = True

        dividendo.idpapel = data['idpapel']
        dividendo.dt_pagto = data['dt_pagto']
        dividendo.valor = data['valor']
        if add:
            db.session.add(dividendo)
        db.session.commit()
        return True
    except:
        return False


def get_valor_total_diviendos_12ult_meses(papel):
    filterpapel = DividendosBolsa.idpapel == papel
    try:
        int(papel)
    except:
        filterpapel = EmpresaBolsa.papel == papel

    dtfim = datetime.now()
    dtini = dtfim - timedelta(days=365.25)

    dtini = dtini.strftime('%Y-%m-%d')
    dtfim = dtfim.strftime('%Y-%m-%d')

    regtotal = db.session.query(
        cast(func.round((func.sum(DividendosBolsa.valor) * 100) / EmpresaBolsa.val_cotacao,2),FLOAT),
        func.sum(DividendosBolsa.valor)).\
        join(EmpresaBolsa,DividendosBolsa.idpapel==EmpresaBolsa.id).\
        filter(and_(filterpapel,DividendosBolsa.dt_pagto.between(dtini,dtfim)))
    regtotal = regtotal.all()
    if regtotal:
        return {'perc_div_yield':regtotal[0][0],'valor_div_yield':regtotal[0][1]}