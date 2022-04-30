from App.model.anvisa.medicamentos_anvisa import Medicamentos_anvisa,SchemaMedicamentos_anvisa
from App.model.anvisa.laboratorios_anvisa import Laboratorios_anvisa
from App.model.anvisa.classe_terapeutica_anvisa import ClasseTerapeurica_anvisa
from App.model.anvisa.tiposmedicamentos_anvisa import TiposMedicamentos_anvisa
from App.model.anvisa.substancia_anvisa import Substancias_anvisa
from App import db
from sqlalchemy import and_
from flask import request
from App.funcs.getpagination import get_pagination,preenche_pagination
from flask_paginate import get_page_args



def get_medicamento_by_desc_and_apresentacao(desc,apresentacao):
    filter = and_(Medicamentos_anvisa.descricao==desc,Medicamentos_anvisa.apresentacao==apresentacao)
    medicamento = Medicamentos_anvisa.query.filter(filter).first()
    if medicamento:
        return medicamento
    return None


def get_medicamentos_json():
    try:
        if request.method == 'GET':

            desc = request.args.get('desc') if request.args.get('desc') != None else ''
            tpfiltro = request.args.get('tpfiltro') if request.args.get('tpfiltro') != None else '0'
            page = request.args.get('page') if request.args.get('page') != None else '1'
            per_page = request.args.get('per_page') if request.args.get('per_page') != None else '50'

            filter = Medicamentos_anvisa.descricao.like(desc)
            join_union = ''
            if tpfiltro == '0':
                filter = Medicamentos_anvisa.descricao.like("%"+desc+"%")
                join_union = ''
            elif tpfiltro == '1': # POR APRESENTACAO
                filter = Medicamentos_anvisa.apresentacao.like("%"+desc+"%")
                join_union = ''
            elif tpfiltro == '2': # SUBSTANCIA
                filter = Substancias_anvisa.descricao.like("%"+desc+"%")
                join_union = (Substancias_anvisa, Medicamentos_anvisa.idsubstancia == Substancias_anvisa.id)
            elif tpfiltro == '3': # CLASSE TERAPEUTICA
                filter = ClasseTerapeurica_anvisa.descricao.like("%"+desc+"%")
                join_union = (ClasseTerapeurica_anvisa, Medicamentos_anvisa.idclasseterapeurica == ClasseTerapeurica_anvisa.id)
            elif tpfiltro == '4': #LABORATORIO NOME
                filter = Laboratorios_anvisa.name.like("%"+desc+"%")
                join_union = (Laboratorios_anvisa, Medicamentos_anvisa.idlaboratorio == Laboratorios_anvisa.id)
            elif tpfiltro == '5': # TIPO MEDICAMENTO
                filter = TiposMedicamentos_anvisa.descricao.like("%"+desc+"%")
                join_union = (TiposMedicamentos_anvisa, Medicamentos_anvisa.idtipomedicamento == TiposMedicamentos_anvisa.id)
            elif tpfiltro == '6': # Tarja
                filter = Medicamentos_anvisa.tarja.like("%"+desc+"%")
                join_union = ''

            if join_union != '':
                meds = Medicamentos_anvisa.query. \
                    order_by(Medicamentos_anvisa.descricao.asc()).\
                    join(join_union) .\
                    filter(filter). \
                    paginate(page=int(page), per_page=int(per_page), error_out=False)
            else:
                meds = Medicamentos_anvisa.query. \
                    order_by(Medicamentos_anvisa.descricao.asc()). \
                    filter(filter). \
                    paginate(page=int(page), per_page=int(per_page), error_out=False)

            if meds:
                page, per_page, offset = get_page_args()
                pagination = get_pagination(
                    page=page,
                    per_page=per_page,
                    total=meds.total,
                    record_name="laboratorios_anvisa"
                )

                schema = SchemaMedicamentos_anvisa()
                return {'data': schema.dump(meds.items, many=True),
                        'pagination': preenche_pagination(pagination),
                        'result': True,
                        'desc': desc,
                        'mensagem': 'sucesso',
                        'tpfiltro': tpfiltro
                        }
            else:
                return {'data': {}, 'result': False, 'pagination': {}, 'desc': desc,
                        'mensagem': 'Nenhum registro encotrado'}
    except:
        pass
    return {'data': {}, 'result': False, 'pagination': {}, 'desc': '','mensagem': 'erro ao executar consulta'}


def add_medicamento(data):
    # try:
        medicamento = Medicamentos_anvisa()
        medicamento.descricao = data['descricao']
        medicamento.ean1 = data['ean1']
        medicamento.ean2 = data['ean2']
        medicamento.ean3 = data['ean3']
        medicamento.apresentacao = data['apresentacao']
        medicamento.codggrem = data['codggrem']
        medicamento.registro = data['registro']
        medicamento.tarja = data['tarja']
        medicamento.idsubstancia = data['idsubstancia']
        medicamento.idlaboratorio = data['idlaboratorio']
        medicamento.idtipomedicamento = data['idtipomedicamento']
        medicamento.idclasseterapeurica = data['idclasseterapeurica']
        db.session.add(medicamento)
        db.session.commit()

        return {'data':
                    {
                        'id':medicamento.id,
                        'descricao':medicamento.descricao,
                        'apresentacao':medicamento.apresentacao,
                    },
                'result':True}
    # except:
    #     return {'data':{},'result':True}]