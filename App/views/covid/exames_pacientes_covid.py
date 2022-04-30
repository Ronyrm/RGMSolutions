import json
import pandas as pd

from App import db,engine
from flask import request,jsonify
from App.funcs.getpagination import get_pagination, preenche_pagination
from flask_paginate import get_page_args
from App.model.covid.exames_pacientes_covid import Exames_pacientes_covid,SchemaExamesPacientesCovid
from App.model.covid.analitos_covid import Analitos_covid
from App.model.covid.exames_covid import Exames_covid
from App.model.covid.pacientes_covid import Pacientes_covid
from sqlalchemy.sql import and_

def get_exames_pacientes_json():
    from sqlalchemy.sql import and_
    try:
        if request.method == 'GET':
            desc = request.args.get("desc") if request.args.get("desc") != None else ''
            page = request.args.get("page") if request.args.get("page") != None else '1'
            per_page = request.args.get("per_page") if request.args.get("per_page") != None else '50'
            tpfiltro = int(request.args.get("tpfiltro") if request.args.get("tpfiltro") != None else '0')
            orberby = request.args.get("orderby") if request.args.get("orderby") != None else '0'
            datacoleta = request.args.get("datacoleta")
            descfiltro = request.args.get("descfiltro") if request.args.get("descfiltro") != None else '0'

            filter_datacoleta = (Exames_pacientes_covid.datacoleta == datacoleta if datacoleta != None else Exames_pacientes_covid.id != -1)

            filter = ''
            union = ''
            if tpfiltro == 0: ## Filtra por codpaciente
                filter = Pacientes_covid.idpaciente == desc
                union = (Pacientes_covid,Exames_pacientes_covid.idpaciente == Pacientes_covid.id)
            elif tpfiltro == 1: # Filtra por código paciente e descrição analito
                filter = (and_(Pacientes_covid.idpaciente==desc, Analitos_covid.descricao.like('%'+descfiltro+'%')))
                union = (Analitos_covid,Exames_pacientes_covid.idanalito == Analitos_covid.id)
            elif tpfiltro == 2:
                filter = (and_(Pacientes_covid.idpaciente==desc, Exames_covid.descricao.like('%'+descfiltro+'%')))
                union = (Exames_covid,Exames_pacientes_covid.idexame == Exames_covid.id)

            if orberby == '0':
                orberby = (Exames_pacientes_covid.datacoleta)



            examespaciente = Exames_pacientes_covid.query.\
                join(union).\
                filter(and_(filter,filter_datacoleta)).\
                order_by(orberby).\
                paginate(page=int(page),per_page=int(per_page), error_out=False)

            if examespaciente:
                page, per_page, offset = get_page_args()
                pagination = get_pagination(
                    page=page,
                    per_page=per_page,
                    total=examespaciente.total,
                    record_name="exames_paciente_covid"
                )

                schema = SchemaExamesPacientesCovid()
                return {'data': schema.dump(examespaciente.items, many=True),
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

    return {'data': {}, 'result': False, 'pagination': {}, 'desc': desc,
            'mensagem': 'Nenhum registro encotrado'}

def add_exame_paciente(data):
    try:
        examepaciente = Exames_pacientes_covid()
        examepaciente.idpaciente = data["idpaciente"]
        examepaciente.idanalito = data["idanalito"]
        examepaciente.idexame = data["idexame"]
        examepaciente.datacoleta = data["datacoleta"]
        examepaciente.origem = data["origem"]
        examepaciente.resultado = data["resultado"]
        examepaciente.valresultado = data["valresultado"]
        examepaciente.unidademedida = data["unidademedida"]
        examepaciente.valreferencia = data["valreferencia"]
        examepaciente.observacao = data["observacao"]
        examepaciente.idhospital = data["idhospital"]
        db.session.add(examepaciente)
        db.session.commit()
        return examepaciente

    except:
        return None

def get_tot_reg_by_data_idpaciente():
    import simplejson
    from sqlalchemy import select
    from sqlalchemy.sql import func
    if request.method == 'GET':
        desc = request.args.get("desc") if request.args.get("desc") != None else ''
        if desc != '':
            from App.views.covid.pacientes_covid import get_paciente_by_idpaciente
            paciente = get_paciente_by_idpaciente(desc)
            if paciente:
                examespaciente = db.session.\
                    query(Exames_pacientes_covid.datacoleta,func.count(Exames_pacientes_covid.idpaciente).label('total')).\
                    filter(Exames_pacientes_covid.idpaciente==paciente[0].id).\
                    group_by(Exames_pacientes_covid.datacoleta).\
                    order_by(Exames_pacientes_covid.datacoleta).all()

                data = {}
                cont = 0
                for dt, total in examespaciente:
                    row = {'datacoleta': {'date':dt,'ano':str(dt.year),'mes':str(dt.month).zfill(2),'dia':str(dt.day).zfill(2)}, 'total': total}
                    data[cont] = row
                    cont += 1
                idade = 2020-paciente[0].anonascimento
                sexo = 'Masculino' if paciente[0].genero == 'M' else 'Feminino' if paciente[0].genero == 'F' else 'Sem Definição'
                hospital = paciente[0].hospital.name
                return {'data': data,'paciente':{'idade': idade,
                                                 'genero': sexo,
                                                 'hospital': hospital,
                                                 }
                        }

