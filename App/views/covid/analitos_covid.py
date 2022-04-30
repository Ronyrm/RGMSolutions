from App.model.covid.analitos_covid import SchemaAnalitos, Analitos_covid
from App import db
from flask import request
from App.funcs.getpagination import get_pagination, preenche_pagination
from flask_paginate import get_page_args
from sqlalchemy import and_


def get_analito(desc,idexame):
    return Analitos_covid.query.\
        filter(and_(Analitos_covid.descricao == desc,
                    Analitos_covid.idexame==idexame)).all()


def get_analitos_json():
    try:
        if request.method == 'GET':
            idexame = request.args.get("idexame") if request.args.get("idexame") != None else ''
            desc = request.args.get("desc") if request.args.get("desc") != None else ''

            filteranalitos = Analitos_covid.id !=-1 if desc =='' else Analitos_covid.descricao.like('%' + desc + '%')
            filterexame = Analitos_covid.id !=-1 if idexame in ('','0') else Analitos_covid.idexame==idexame
            analitos = Analitos_covid.query.filter(and_(filteranalitos,filterexame)).all()
            if analitos:
                schema = SchemaAnalitos()
                return {'data': schema.dump(analitos, many=True),
                        'result': True,
                        'desc': desc,
                        'mensagem': 'sucesso'
                        }
            else:
                return {'data': {}, 'result': False,'desc': desc,
                        'mensagem': 'Nenhum registro encotrado'}
    except:
        pass

    return {'data': {}, 'result': False, 'pagination': {}, 'desc': desc,
            'mensagem': 'Nenhum registro encotrado'}


def add_analito(desc,idexame):
    try:
        analito = Analitos_covid()
        analito.descricao = desc
        analito.idexame = idexame
        db.session.add(analito)
        db.session.commit()
        return analito
    except:
        return None

def update_analito(data):
    analito = Analitos_covid.query.id(data["id"])
    if analito:
        analito.descricao = data["descricao"]
        analito.idexame = data["exame"]
        analito.descvalref = data["descvalref"]
        analito.valref_min = data["valref_min"]
        analito.valref_max = data["valref_max"]
        db.session.commit()
        return analito
    return None
