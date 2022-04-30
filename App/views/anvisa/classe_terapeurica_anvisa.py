from App.model.anvisa.classe_terapeutica_anvisa import ClasseTerapeurica_anvisa,SchemaClasseTerapeutica_anvisa
from App import db
from flask import request
from flask_paginate import  get_page_args
from App.funcs.getpagination import get_pagination,preenche_pagination

def get_classe_terapeutica(desc=''):
    filter = ClasseTerapeurica_anvisa.descricao==desc
    classe = ClasseTerapeurica_anvisa.query.filter(filter).first()
    if classe:
        return classe
    return None

def get_classes_terapeutica_json():
    try:
        if request.method == 'GET':

            desc= request.args.get('desc') if request.args.get('desc') != None else ''
            page = request.args.get('page') if request.args.get('page') != None else '1'
            per_page = request.args.get('per_page') if request.args.get('per_page') != None else '50'

            filter = ClasseTerapeurica_anvisa.descricao.like("%"+desc+"%")

            classes = ClasseTerapeurica_anvisa.query.\
            filter(filter).\
            paginate(page=int(page), per_page=int(per_page), error_out=False)

            if classes:
                page, per_page, offset = get_page_args()
                pagination = get_pagination(
                    page=page,
                    per_page=per_page,
                    total=classes.total,
                    record_name="classes_terapeutica_anvisa"
                )

                schema = SchemaClasseTerapeutica_anvisa()
                return {'data':schema.dump(classes.items,many=True),
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



def add_classe_terapeurica(desc):
     try:
        if len(desc) > 0:
            classe = ClasseTerapeurica_anvisa()
            classe.descricao = desc
            db.session.add(classe)
            db.session.commit()

            return {'data':
                        {'id':classe.id,
                         'descricao':classe.descricao
                         },
                    'result': True}
     except:
         return {'data':{},'result':False}