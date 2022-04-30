from App.model.anvisa.tabpreco_medicamentos_anvisa import TabPrecoMedicamentos_anvisa,SchemaTabPrecoMedicamentos_anvisa
from App.model.anvisa.medicamentos_anvisa import Medicamentos_anvisa
from App import db
from flask import request
from App.funcs.getpagination import get_pagination,preenche_pagination
from flask_paginate import get_page_args

def get_tabpreco_by_idmedicamento(idmedicamento):
    filter = TabPrecoMedicamentos_anvisa.idmedicamento == idmedicamento
    tabpreco = TabPrecoMedicamentos_anvisa.query.filter(filter).first()
    if tabpreco:
        return tabpreco
    return None


def get_tabpreco_by_idmedicamento_json(idmedicamento):
    try:
        filter = TabPrecoMedicamentos_anvisa.idmedicamento == idmedicamento
        tabpreco = TabPrecoMedicamentos_anvisa.query.filter(filter).all()
        if tabpreco:
            schema = SchemaTabPrecoMedicamentos_anvisa()
            res = schema.dump(tabpreco, many=True)
            return {'data': res,
                    'result': True,
                    'mensagem': 'sucesso'
                    }
    except:
        pass

    return {'data': {}, 'result': False,'mensagem': 'sucesso'}




def get_tabpreco_by_desc_medicmento_json():
    if request.method == 'GET':
        desc = request.args.get('desc') if request.args.get('desc') != None else ''
        page = request.args.get('page') if request.args.get('page') != None else '1'
        per_page = request.args.get('per_page') if request.args.get('per_page') != None else '50'

        tabpreco = TabPrecoMedicamentos_anvisa.query.\
            join(Medicamentos_anvisa, TabPrecoMedicamentos_anvisa.idmedicamento==Medicamentos_anvisa.id).\
            filter(Medicamentos_anvisa.descricao.like("%"+desc+"%")).\
            paginate(page=int(page),per_page=int(per_page),error_out=False)

        if tabpreco:
            page, per_page, offset = get_page_args()
            pagination = get_pagination(
                page=page,
                per_page=per_page,
                total=tabpreco.total,
                record_name="tabpreco_medicamento_anvisa"
            )

            schema = SchemaTabPrecoMedicamentos_anvisa()
            return {'data': schema.dump(tabpreco.items, many=True),
                    'pagination': preenche_pagination(pagination),
                    'result': True,
                    'desc': desc,
                    'mensagem': 'sucesso'
                    }
        else:
            return {'data': {}, 'result': False, 'pagination': {}, 'desc': desc,
                    'mensagem': 'Nenhum registro encotrado'}


def add_tabpreco_medicamento(data):
    # try:
        tabpreco = TabPrecoMedicamentos_anvisa()
        tabpreco.idmedicamento = data['idmedicamento']
        tabpreco.cap = data['cap']
        tabpreco.icms0 = data['icms0']
        tabpreco.analise_recursal = data['analise_recursal']
        tabpreco.comercializacao2019 = data['comercializacao2019']
        tabpreco.confaz87 = data['confaz87']
        tabpreco.list_piscofins = data['list_piscofins']
        tabpreco.regime_preco = data['regime_preco']
        tabpreco.restr_hospitalar = data['restr_hospitalar']
        tabpreco.vl_pf0 = data['vl_pf0']
        tabpreco.vl_pf12 = data['vl_pf12']
        tabpreco.vl_pf17 = data['vl_pf17']
        tabpreco.vl_pf17alc = data['vl_pf17alc']
        tabpreco.vl_pf18 = data['vl_pf18']
        tabpreco.vl_pf18alc = data['vl_pf18alc']
        tabpreco.vl_pf20 = data['vl_pf20']
        tabpreco.vl_pf175 = data['vl_pf175']
        tabpreco.vl_pf175alc = data['vl_pf175alc']
        tabpreco.vl_pfsemimposto = data['vl_pfsemimposto']
        tabpreco.vl_pmc0 = data['vl_pmc0']
        tabpreco.vl_pmc12 = data['vl_pmc12']
        tabpreco.vl_pmc17 = data['vl_pmc17']
        tabpreco.vl_pmc17alc = data['vl_pmc17alc']
        tabpreco.vl_pmc18 = data['vl_pmc18']
        tabpreco.vl_pmc18alc = data['vl_pmc18alc']
        tabpreco.vl_pmc20 = data['vl_pmc20']
        tabpreco.vl_pmc175 = data['vl_pmc175']
        tabpreco.vl_pmc175alc = data['vl_pmc175alc']

        db.session.add(tabpreco)
        db.session.commit()


        return {'data': {'id':tabpreco.idmedicamento},'result':True}
    # except:
    #     return {'data':{},'result':False}
