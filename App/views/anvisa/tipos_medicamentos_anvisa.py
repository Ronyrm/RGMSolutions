from App.model.anvisa.tiposmedicamentos_anvisa import TiposMedicamentos_anvisa,SchemaTiposMedicamentos_anvisa
from App import db
from flask import request
from App.funcs.getpagination import get_pagination,preenche_pagination
from flask_paginate import get_page_args


def get_tipo_medicamento(desc):
    filter = TiposMedicamentos_anvisa.descricao==desc
    tpmedicamento = TiposMedicamentos_anvisa.query.filter(filter).first()
    if tpmedicamento:
        return tpmedicamento
    return None


def get_tipos_medicamentos_json():
    try:
        if request.method == 'GET':

            desc = request.args.get('desc') if request.args.get('desc') != None else ''
            page = request.args.get('page') if request.args.get('page') != None else '1'
            per_page = request.args.get('per_page') if request.args.get('per_page') != None else '50'

            filter = TiposMedicamentos_anvisa.descricao.like("%" + desc + "%")

            tps_medicamentos = TiposMedicamentos_anvisa.query. \
                filter(filter). \
                paginate(page=int(page), per_page=int(per_page), error_out=False)

            if tps_medicamentos:
                page, per_page, offset = get_page_args()
                pagination = get_pagination(
                    page=page,
                    per_page=per_page,
                    total=tps_medicamentos.total,
                    record_name="tipos_medicamentos_anvisa"
                )

                schema = SchemaTiposMedicamentos_anvisa()
                return {'data': schema.dump(tps_medicamentos.items, many=True),
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


def add_tipo_medicamento(desc):
    # try:
        if len(desc) > 0 :
            tpmedicamento = TiposMedicamentos_anvisa()
            tpmedicamento.descricao=desc
            db.session.add(tpmedicamento)
            db.session.commit()

            return {'data': {'id':tpmedicamento.id,'descricao':tpmedicamento.descricao},
                    'result': True}
    # except:
    #     return {'data':{},'result':False}