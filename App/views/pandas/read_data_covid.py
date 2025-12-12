from flask import request,current_app
from werkzeug.utils import secure_filename
import os
import pandas as pd
from App.views.localidades.cidades import get_cidade_by_uf
from App.views.localidades.uf import get_uf_by_sigla
from App.views.covid.pacientes_covid import get_paciente_by_idpaciente,add_paciente
from App.views.covid.hospitais import get_hostital_by_name,add_hospital
from App.funcs.funcs import format_date_yyyymmaa
from App.views.covid.exames_covid import get_exame,add_exame
from App.views.covid.analitos_covid import get_analito,add_analito
from App.views.covid.exames_pacientes_covid import add_exame_paciente
from App.views.covid.pacientes_covid import get_paciente_by_idpaciente
from datetime import datetime
import re
from App.funcs.dbfuncs import execute_procedure_db
def return_data_frame():
    file_csv = None
    if request.method == 'POST':
        if 'file_csv' in request.files:
            file_csv = request.files['file_csv']
    if file_csv:
        filename = secure_filename(file_csv.filename)
        localesave = current_app.config['UPLOAD_FOLDER']
        spath = os.path.join(localesave, filename)
        if os.path.exists(spath):
            os.remove(spath)
        file_csv.save(spath)

        dataframe = pd.read_csv(spath,sep='|',engine = 'python', encoding = "UTF-8")
        return dataframe
    return None


def verify_exame_in_db(desc):
    exame = get_exame(desc)
    if exame:
        return exame[0].id
    else:
        exame = add_exame(desc)
        return exame.id


def verify_analito_in_db(desc,idexame):
    analito = get_analito(desc,idexame)
    if analito:
        return analito[0].id
    else:
        analito = add_analito(desc,idexame)
        return analito.id

def verify_paciente_in_db(idpaciente):
    paciente = get_paciente_by_idpaciente(idpaciente)
    if paciente:
        return paciente[0].id,paciente[0].idhospital
    else:
        return None,None

#----------------- ALBERT IENSTEIN SÃO PAULO ------------------------

def read_covid19_pacientes_einstein_csv():
    if request.method == 'POST':
        file_csv = None
        idhospital = None
        data = request.form
        namehospital = data['name']
        hospital = get_hostital_by_name(namehospital)

        if not hospital:
            hospital = add_hospital(namehospital)
            idhospital = hospital.id
        else:
            idhospital = hospital[0].id

        dataframe = return_data_frame()
        print(dataframe)
        totalreg = len(dataframe)
        cont = 1
        strtemp_dupli = ''
        info = dataframe.info
        for rowpai in dataframe.values:
            data = rowpai[0].split('|')
            paciente = get_paciente_by_idpaciente(data[0])
            if not paciente:
                uf = data[3]
                citydata = data[4]
                if citydata != 'MMMM':
                    cidade = get_cidade_by_uf(uf,citydata)
                    idcidade = None
                    iduf = None
                    if cidade:
                        idcidade = cidade[0].id
                        iduf = cidade[0].iduf
                else:
                    idcidade = None
                    iduf = None
                    tbuf = get_uf_by_sigla(uf)
                    if tbuf:
                        iduf = tbuf[0].id
                data_tb = {'idpaciente':data[0],
                           'genero':data[1],
                           'anonascimento':data[2],
                           'iduf':iduf,
                           'idcidade':idcidade,
                           'cepreduzido':data[5],
                           'siglapais':data[6],
                           'idhospital':idhospital
                           }
                result = add_paciente(data_tb)
                print('Paciente ins:. ' + result.idpaciente)
            else:
                strtemp_dupli += "\nPos:"+str(cont)+' | Paciente ins:. '+ paciente[0].idpaciente

            print('Pos:'+ str(cont) + ' de ' + str(totalreg))
            cont += 1

        return {'result_dupli':strtemp_dupli}



def read_covid19_exames_einstein_csv():

    dataframe = pd.read_csv('App/static/img/uploads/EINSTEIN_Exames_2.csv',
                            sep='|', engine='python', encoding="UTF-8")


    totalreg = 1
    cont = 1
    totpassou = 1
    dtnow = datetime.now().strftime('%H:%M:%S')
    for rowpai in dataframe.values:
        if cont == 126:
            print('Assssss')
            cont = cont
        data = rowpai
        idpaciente = verify_paciente_in_db(data[0])
        idexame = verify_exame_in_db(data[3])
        idanalito = verify_analito_in_db(data[4],idexame)

        resultado = data[5] if len(data[5].strip()) > 0 else None
        unidademedida = None if pd.isna(data[6]) else data[6]
        valref = None if pd.isna(data[7]) else data[7]

        try:
            vlresultado = float(data[5])
        except:
            vlresultado = None

        if resultado == None and unidademedida == None and vlresultado == None and  valref==None:
            print('Passou tot:' + str(totpassou))
            totpassou += 1
        else:
            data_tb = {'idpaciente': idpaciente,
                    'datacoleta': format_date_yyyymmaa(data[1]),
                    'origem': data[2],
                    'idexame':idexame,
                    'idanalito':idanalito,
                    'resultado':resultado,
                    'valresultado':vlresultado,
                    'unidademedida':unidademedida,
                    'valreferencia': valref
                    }
            try:
                result = add_exame_paciente(data_tb)
                if result:
                    print('Inserindo:'+ str(result.id))
            except:
                print('Erro ao inserir idpaciente:'+data[0])
                break;

        print('Pos:' + str(cont)+ ' total de: 1048576')
        cont += 1
    dtfim = datetime.now().strftime('%H:%M:%S')
    return {'finalizado':True,'total':cont,'total_no_insert':totpassou,
            'Hora_inicio':str(dtnow),'Hora_fim':str(dtfim),}


def readwrite_covid_exames_eistein_csv_mydb_two():

    dataframe = pd.read_csv('App/static/img/uploads/EINSTEIN_Exames_2.csv',
                            sep='|', engine='python', encoding="UTF-8")
    totpassou = 1
    totalreg = len(dataframe.values)
    dtnow = datetime.now().strftime('%H:%M:%S')
    for cont in range(1612485,totalreg):
        rowpai = dataframe.values[cont]
        data = rowpai
        descexame = data[3]
        descanalito = data[4]

        resultado = data[5] if len(str(data[5]).strip()) > 0 else None
        unidademedida = None if pd.isna(data[6]) else data[6]
        valref = None if pd.isna(data[7]) else data[7]

        try:
            vlresultado = float(data[5])
        except:
            vlresultado = None


        if resultado == None and unidademedida == None and vlresultado == None and valref == None:
            print('Passou tot:' + str(totpassou))
            totpassou += 1
        else:

            parameter = [descexame,descanalito,data[0],format_date_yyyymmaa(data[1]),data[2],
                         resultado if resultado != None else 'NULL',
                         str(vlresultado) if vlresultado != None else 0,
                          unidademedida if unidademedida != None else '',
                          valref if valref != None else 'NULL']

            try:
                result = execute_procedure_db('insert_exame_paciente',parameter)
                print('Pos: ' + str(cont) + ' total:' +str(totalreg))
            except:
                print('Pos: '+str(cont)+' Erro ao inserir idpaciente:' + data[0])
                print(parameter)


    dtfim = datetime.now().strftime('%H:%M:%S')
    return {'finalizado': True, 'total': cont, 'total_no_insert': totpassou,
            'Hora_inicio': str(dtnow), 'Hora_fim': str(dtfim), }


#----------------- HOSPITAL DAS CLINICAS SÃO PAULO ------------------------

def read_covid19_pacientes_hc_csv():
    file_csv = None
    idhospital = None
    if request.method == 'POST':
        data = request.form
        namehospital = data['name']
        hospital = get_hostital_by_name(namehospital)

        if not hospital:
            hospital = add_hospital(namehospital)
            idhospital = hospital.id
        else:
            idhospital = hospital[0].id

        if 'file_csv' in request.files:
            file_csv = request.files['file_csv']

    if file_csv:
        filename = secure_filename(file_csv.filename)
        localesave = current_app.config['UPLOAD_FOLDER']

        spath = os.path.join(localesave, filename)

        if os.path.exists(spath):
            os.remove(spath)

        file_csv.save(spath)

        dataframe = pd.read_csv(spath)
        print(dataframe)
        totalreg = len(dataframe)
        cont = 1
        strtemp_dupli = ''
        info = dataframe.info
        for rowpai in dataframe.values:
            data = rowpai[0].split('|')
            paciente = get_paciente_by_idpaciente(data[0])
            if not paciente:
                uf = data[4]
                citydata = data[5]
                if citydata != 'MMMM':
                    cidade = get_cidade_by_uf(uf, citydata)
                    idcidade = None
                    iduf = None
                    if cidade:
                        idcidade = cidade[0].id
                        iduf = cidade[0].iduf
                else:
                    idcidade = None
                    iduf = None
                    tbuf = get_uf_by_sigla(uf)
                    if tbuf:
                        iduf = tbuf[0].id
                data_tb = {'idpaciente':data[0],
                           'genero':data[1],
                           'anonascimento':data[2],
                           'iduf':iduf,
                           'idcidade':idcidade,
                           'cepreduzido':data[6],
                           'siglapais':data[3],
                           'idhospital':idhospital
                           }
                result = add_paciente(data_tb)
                print('Paciente ins:. ' + result.idpaciente)
            else:
                strtemp_dupli += "\nPos:"+str(cont)+' | Paciente ins:. '+ paciente[0].idpaciente

            print('Pos:'+ str(cont) + ' de ' + str(totalreg))
            cont += 1

        return {'result_dupli':strtemp_dupli}

def read_covid19_exames_hc_csv():
    print('Preparando....')
    dataframe = pd.read_csv('App/static/img/uploads/HC_EXAMES_1.csv',
                            sep='|', engine='python', encoding="UTF-8")
    totpassou = 1
    totalreg = len(dataframe.values)
    dtnow = datetime.now().strftime('%H:%M:%S')
    print('A começar....')
    for cont in range(1507804, totalreg):
        rowpai = dataframe.values[cont]

        resultado = rowpai[6] if len(str(rowpai[6]).strip()) > 0 else None
        resultado = None if pd.isna(resultado) else resultado
        unidademedida = None if pd.isna(rowpai[7]) else rowpai[7]
        valref = None if pd.isna(rowpai[8]) else rowpai[8]
        observacao = None
        if valref != None and valref.rfind(';') != -1:
            valref = valref[0:valref.find(';')]
            observacao = valref[valref.rfind(';')+1:len(valref)]

        try:
            vlresultado = float(rowpai[6])
            vlresultado = None if pd.isna(vlresultado) else vlresultado
        except:
            vlresultado = None


        if resultado == None and unidademedida == None and vlresultado == None and valref == None:
            print('Passou tot:' + str(totpassou))
            totpassou += 1
        else:

            parameter = [rowpai[4], rowpai[5], rowpai[0], rowpai[2], rowpai[3],
                         resultado if resultado != None else 'NULL',
                         str(vlresultado) if vlresultado != None else 0,
                         unidademedida if unidademedida != None else '',
                         valref if valref != None else 'NULL',
                         observacao if observacao != None else 'NULL']

            try:
                result = execute_procedure_db('insert_exame_paciente', parameter)
                print('Pos: ' + str(cont) + ' total:' + str(totalreg))
            except:
                print('Pos: ' + str(cont) + ' Erro ao inserir idpaciente:' + rowpai[0])
                print(parameter)

    dtfim = datetime.now().strftime('%H:%M:%S')
    return {'finalizado': True, 'total': totalreg,
            'Hora_inicio': str(dtnow), 'Hora_fim': str(dtfim), }