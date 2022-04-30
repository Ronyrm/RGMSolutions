from App import db
from App.model.anvisa.laboratorios_anvisa import Laboratorios_anvisa,SchemaLaboratorios_anvisa
from App.funcs.getpagination import get_pagination,preenche_pagination
from flask_paginate import get_page_args
from flask import request
import re

# CAPTURA UM LABORATORIO POR DESCRICAO OU CNPJ
def get_laboratorio(q='',tpfiltro=0):
    # tpfiltro = 0 : filtra por descricao, tpfiltro = 1 : filtra por cnpj
    filter = ''
    if tpfiltro == 0:
        filter = Laboratorios_anvisa.name==q
    elif tpfiltro == 1:
        vlcnpj = re.sub('\W','',q)
        filter = Laboratorios_anvisa.cnpj==vlcnpj

    labs = Laboratorios_anvisa.query.filter(filter).first()
    if labs:
        return labs
    return None

# CAPTURA LABORATORIOS POR DESCRICAO> ?tbfiltro=0&desc='xxxx' OU POR CNPJ>> ?tbfiltro=1&desc='xxxx'
def get_laboratorios_json():
    try:
        if request.method == 'GET':

            desc = request.args.get('desc') if request.args.get('desc') != None else ''
            tpfiltro = request.args.get('tpfiltro') if request.args.get('tpfiltro') != None else '0'
            page = request.args.get('page') if request.args.get('page') != None else '1'
            per_page = request.args.get('per_page') if request.args.get('per_page') != None else '50'

            filter = Laboratorios_anvisa.name.like('%'+desc+'%')
            if tpfiltro == 0:
                filter = Laboratorios_anvisa.name.like('%'+desc+'%')
            elif tpfiltro == 1:
                vlcnpj = re.sub('\W', '', desc)
                filter = Laboratorios_anvisa.cnpj == vlcnpj
            elif tpfiltro == 2:
                vlcnpj = re.sub('\W', '', desc)
                filter = Laboratorios_anvisa.cnpj.like(vlcnpj+"%")

            labs = Laboratorios_anvisa.query. \
                filter(filter). \
                paginate(page=int(page), per_page=int(per_page), error_out=False)

            if labs:
                page, per_page, offset = get_page_args()
                pagination = get_pagination(
                    page=page,
                    per_page=per_page,
                    total=labs.total,
                    record_name="laboratorios_anvisa"
                )

                schema = SchemaLaboratorios_anvisa()
                return {'data': schema.dump(labs.items, many=True),
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

# ADICIONA UM NOVO LABORATORIO
def add_laboratorio(name,cnpj):
    try:
        if len(name)>0 and len(cnpj):
            cnpj = re.sub('\W','',cnpj)

            lab = Laboratorios_anvisa()
            lab.name = name
            lab.cnpj = cnpj
            db.session.add(lab)
            db.session.commit()


            return {'data':
                        {'id':lab.id,
                         'name':lab.name,
                         'cnpj':lab.cnpj
                         },
                    'result':True}
    except:
        return {'data':{},'result':False}