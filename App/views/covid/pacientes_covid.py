from App import db
from flask import request,render_template
from App.model.covid.pacientes_covid import Pacientes_covid,SchemaPacientes
from App.model.localidades.cidades import Cidades
from App.model.covid.exames_pacientes_covid import Exames_pacientes_covid
from App.funcs.getpagination import get_pagination,preenche_pagination
from flask_paginate import get_page_args
from sqlalchemy.sql import func, and_

def get_paciente(id):
    paciente = Pacientes_covid.query.get(id)

    return paciente

def get_paciente_by_idpaciente(idpaciente):
    return Pacientes_covid.query.filter(Pacientes_covid.idpaciente==idpaciente).all()


def get_pacientes_json():
    if request.method == 'GET':
        q = request.args.get("q") if request.args.get("q") != None else ''
        page = request.args.get("page") if request.args.get("page") != None else '1'
        per_page = request.args.get("per_page") if request.args.get("per_page") != None else '50'
        tpfiltro = int(request.args.get("tpfiltro") if request.args.get("tpfiltro") != None else '0')

        if tpfiltro == 0: # por nome cidade
            filter = Cidades.nome.like("%"+q+"%")
        elif tpfiltro == 1: # por sexo
            filter = Pacientes_covid.genero == q
        elif tpfiltro == 2: # por ano de nascimento
            filter = Pacientes_covid.anonascimento == q
        elif tpfiltro == 3:
            filter = Pacientes_covid.iduf == q

        pacientes = Pacientes_covid.query.\
            join(Cidades,Pacientes_covid.idcidade,Cidades.id).\
            filter(filter).\
            paginate(page=int(page),per_page=int(per_page),error_out=False)


def add_paciente(data):
    try:
        paciente = Pacientes_covid()
        paciente.idpaciente = data["idpaciente"]
        paciente.iduf = data["iduf"]
        paciente.idcidade = data["idcidade"]
        paciente.genero = data["genero"]
        paciente.anonascimento = data["anonascimento"]
        paciente.cepreduzido = data["cepreduzido"]
        paciente.siglapais = data["siglapais"]
        paciente.idhospital = data["idhospital"]
        db.session.add(paciente)
        db.session.commit()
        return paciente
    except:
        return None


def get_paciente_exames_analito_total_reg():
    if request.method == 'GET':
        idhospital = request.args.get('idhospital')
        idexame = request.args.get('idexame')
        idanalito = request.args.get('idanalito')
        resultado = request.args.get('resultado')
        page = request.args.get('page') if request.args.get('page') != None else '1'
        per_page = request.args.get('per_page') if request.args.get('per_page') != None else '20'
        tpfiltro = request.args.get('tpfiltro') if request.args.get('tpfiltro') != None else '0'


        filterpac = Pacientes_covid.id != -1
        if tpfiltro == '0':
            filterpac = (Pacientes_covid.idhospital==idhospital) if idhospital != None else filterpac
        elif tpfiltro == '1': # Filtra Paciente de acordo com o exame e o resultado

            filterexame = Exames_pacientes_covid.idexame == idexame \
                if idexame != None else Exames_pacientes_covid.id != -1
            filteranalito = Exames_pacientes_covid.idanalito == idanalito \
                if idanalito != None else Exames_pacientes_covid.id != -1
            filterhospital = Exames_pacientes_covid.idhospital == idhospital \
                if idhospital != None else Exames_pacientes_covid.id != -1
            filterresultado = Exames_pacientes_covid.resultado == resultado \
                if resultado != None else Exames_pacientes_covid.id != -1

            sub_query = db.session. \
                query(Exames_pacientes_covid.idpaciente). \
                filter(and_(filterexame,
                            filterhospital,
                            filterresultado,
                            filteranalito)). \
                group_by(Exames_pacientes_covid.idpaciente). \
                having(func.count(Exames_pacientes_covid.idexame) > 0). \
                subquery()
            filterpac = Pacientes_covid.id.in_(sub_query)


        pacientes = Pacientes_covid.query. \
            filter(filterpac). \
            paginate(page=int(page), per_page=int(per_page), error_out=True)

        if pacientes:
            page, per_page, offset = get_page_args()
            pagination = get_pagination(
                page=page,
                per_page=per_page,
                total=pacientes.total,
                record_name="paciente_covid"
            )
            schema = SchemaPacientes()
            return {'data': schema.dump(pacientes.items, many=True),
                    'pagination': preenche_pagination(pagination),
                    'result': True,
                    'desc': idhospital,
                    'mensagem': 'sucesso',
                    'resultado': resultado,
                    'idhospital': idhospital,
                    'idexame': idexame,
                    'tpfiltro': tpfiltro,
                    'idanalito': idanalito,
                    }



def get_paciente_main():

    if request.method == 'GET':
        idhospital = request.args.get('idhospital') if not request.args.get('idhospital') in ('',None) else None
        idexame = request.args.get('idexame') if not request.args.get('idexame') in ('',None) else None
        idanalito = request.args.get('idanalito') if not request.args.get('idanalito') in ('',None) else None
        resultado = request.args.get('resultado')
        vlresultado = request.args.get('vlresultado') if not request.args.get('vlresultado') in('',None) else None
        tpoperadorresultado = request.args.get('tpoperadorresultado') if not request.args.get('tpoperadorresultado') in('',None) else None
        page = request.args.get('page') if request.args.get('page') != None else '1'
        per_page = request.args.get('per_page') if request.args.get('per_page') != None else '20'
        tpfiltro = request.args.get('tpfiltro') if request.args.get('tpfiltro') != None else '0'
        tpoperadoridade = request.args.get('tpoperadoridade') if not request.args.get('tpoperadoridade') in('',None) else None
        idade = request.args.get('idade') if not request.args.get('idade') in('',None) else None
        sexo = request.args.get('sexo') if not request.args.get('sexo') in('',None) else None
        idadede = request.args.get('idadede') if not request.args.get('idadede') in('',None) else None
        idadeate = request.args.get('idadeate') if not request.args.get('idadeate') in ('', None) else None
        filterpac = Pacientes_covid.id != -1

        if sexo == 'W':
            filtersexo = and_(Pacientes_covid.genero != 'F',Pacientes_covid.genero != 'M')
        else:
            filtersexo = Pacientes_covid.genero == sexo if sexo != None else Pacientes_covid.id != -1

        filteridade = Pacientes_covid.id != -1
        if tpoperadoridade == '0':
            filteridade = 2020 - Pacientes_covid.anonascimento == idade
        elif tpoperadoridade == '1':
            filteridade = 2020 - Pacientes_covid.anonascimento > idade
        elif tpoperadoridade == '2':
            filteridade = 2020 - Pacientes_covid.anonascimento >= idade
        elif tpoperadoridade == '3':
            filteridade = 2020 - Pacientes_covid.anonascimento < idade
        elif tpoperadoridade == '4':
            filteridade = 2020 - Pacientes_covid.anonascimento <= idade
        elif tpoperadoridade == '5':
            filteridade = and_(2020 - Pacientes_covid.anonascimento >= idadede,2020 - Pacientes_covid.anonascimento <= idadeate) if idadede != None and idadeate != None else Pacientes_covid.id != -1

        if tpfiltro == '0':
            filterpac = (Pacientes_covid.idhospital == idhospital) if idhospital != None and idhospital != '' else filterpac
        elif tpfiltro == '1':  # Filtra Paciente de acordo com o exame e o resultado

            filterexame = Exames_pacientes_covid.idexame == idexame \
                if idexame != None else Exames_pacientes_covid.id != -1
            filteranalito = Exames_pacientes_covid.idanalito == idanalito \
                if idanalito != None else Exames_pacientes_covid.id != -1
            filterhospital = Exames_pacientes_covid.idhospital == idhospital \
                if idhospital != None else Exames_pacientes_covid.id != -1
            filterresultado = Exames_pacientes_covid.resultado == resultado \
                if resultado != None else Exames_pacientes_covid.id != -1

            filtervlresultado = Exames_pacientes_covid.id != -1

            if tpoperadorresultado == '0': #vlresultado igual que
                filtervlresultado = Exames_pacientes_covid.valresultado == vlresultado
            elif tpoperadorresultado == '1': # vlresultado maior que
                filtervlresultado = Exames_pacientes_covid.valresultado > vlresultado
            elif tpoperadorresultado == '2': # vlresultado maior igual que
                filtervlresultado = Exames_pacientes_covid.valresultado >= vlresultado
            elif tpoperadorresultado == '3': # vlresultado menor que
                filtervlresultado = Exames_pacientes_covid.valresultado < vlresultado
            elif tpoperadorresultado == '4': # vlresultado menor igual que
                filtervlresultado = Exames_pacientes_covid.valresultado <= vlresultado


            sub_query = db.session. \
                query(Exames_pacientes_covid.idpaciente). \
                filter(and_(filterexame,
                            filterhospital,
                            filterresultado,
                            filtervlresultado,
                            filteranalito)). \
                group_by(Exames_pacientes_covid.idpaciente). \
                having(func.count(Exames_pacientes_covid.idexame) > 0). \
                subquery()
            filterpac = Pacientes_covid.id.in_(sub_query)

        pacientes = Pacientes_covid.query. \
            filter(and_(and_(filtersexo,filteridade),filterpac)).\
            paginate(page=int(page), per_page=int(per_page), error_out=True)

        if pacientes:
            page, per_page, offset = get_page_args()
            pagination = get_pagination(
                page=page,
                per_page=per_page,
                total=pacientes.total,
                record_name="paciente_covid"
            )
            schema = SchemaPacientes()
            return render_template('layouts/covid/pacientes/main.html',
                            tbpacientes=schema.dump(pacientes.items, many=True),
                            pagination=preenche_pagination(pagination),
                            result=True,
                            idexame=idexame,
                            tpfiltro=tpfiltro,
                            idanalito=idanalito,
                            resultado=resultado,
                            idhospital=idhospital,
                            tpoperadorresultado=tpoperadorresultado,
                            tpoperadoridade=tpoperadoridade,
                            idade=idade,
                            sexo = sexo,
                            vlresultado=vlresultado,
                            mensagem= 'sucesso')

    return render_template('layouts/covid/pacientes/main.html',
                           tbpacientes={},
                           pagination={},
                           result=False,
                           idexame='0',
                           tpfiltro='0',
                           idanalito='0',
                           resultado='',
                           idhospital='0',
                           tpoperador='',
                           vlresultado='',
                           mensagem='erro')