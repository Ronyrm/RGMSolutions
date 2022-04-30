from App.model.anvisa.substancia_anvisa import Substancias_anvisa,SchemaSubstancia_anvisa
from App import db
from flask import request
from App.funcs.getpagination import get_pagination,preenche_pagination
from flask_paginate import get_page_args

def get_substancia_by_id(id):
    return Substancias_anvisa.query.filter(Substancias_anvisa.id==id).all()


def get_substancia_anvisa(desc=''):
    filter = Substancias_anvisa.descricao==desc
    sub = Substancias_anvisa.query.filter(filter).first()
    if sub:
        return sub
    return None


def get_substancias_json():
    try:
        if request.method == 'GET':

            desc = request.args.get('desc') if request.args.get('desc') != None else ''
            page = request.args.get('page') if request.args.get('page') != None else '1'
            per_page = request.args.get('per_page') if request.args.get('per_page') != None else '50'

            filter = Substancias_anvisa.descricao.like("%" + desc + "%")

            subs = Substancias_anvisa.query. \
                filter(filter). \
                paginate(page=int(page), per_page=int(per_page), error_out=False)

            if subs:
                page, per_page, offset = get_page_args()
                pagination = get_pagination(
                    page=page,
                    per_page=per_page,
                    total=subs.total,
                    record_name="substancias_anvisa"
                )

                schema = SchemaSubstancia_anvisa()
                return {'data': schema.dump(subs.items, many=True),
                        'pagination': preenche_pagination(pagination),
                        'result': True,
                        'desc': desc,
                        'mensagem': 'sucesso'
                        }
            else:
                return {'data': {}, 'result': False, 'pagination': {}, 'desc': desc,
                        'mensagem': 'Nenhum registro encotrado'}
    except:
        pass
    return {'data': {}, 'result': False, 'pagination': {}, 'desc': '','mensagem': 'erro ao executar consulta'}



def add_substancia_anvisa(desc):
    try:
        if len(desc) > 0:
            sub = Substancias_anvisa()
            sub.descricao = desc
            db.session.add(sub)
            db.session.commit()

            return {'data':
                        {'id':sub.id,
                         'descricao':sub.descricao
                         },
                    'result':True}
    except:
        return {'data':{},'result':False}