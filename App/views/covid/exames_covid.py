from App.model.covid.exames_covid import SchemaExames,Exames_covid
from App import db
from flask import request
from App.funcs.getpagination import  get_pagination, preenche_pagination
from flask_paginate import get_page_args


def get_exame(desc):
    return Exames_covid.query.filter(Exames_covid.descricao==desc).all()


def get_exames_json():
    try:
        if request.method == 'GET':
            desc = request.args.get("desc") if request.args.get("desc") != None else ''
            filterexames = Exames_covid.id != -1 if desc != '' else Exames_covid.descricao.like('%'+desc+'%')
            exames = Exames_covid.query.filter(filterexames).order_by(Exames_covid.id.asc()).all()
            if exames:
                schema = SchemaExames()
                return {'data': schema.dump(exames, many=True),
                        'result': True,
                        'desc': desc,
                        'mensagem': 'sucesso'
                        }
            else:
                return {'data': {}, 'result': False, 'desc': desc,
                        'mensagem': 'Nenhum registro encotrado'}
    except:
        pass

    return {'data': {}, 'result': False, 'pagination': {}, 'desc': desc,
            'mensagem': 'Nenhum registro encotrado'}


def add_exame(desc):
    try:
        exame = Exames_covid()
        exame.descricao = desc
        db.session.add(exame)
        db.session.commit()
        return exame
    except:
        return None

