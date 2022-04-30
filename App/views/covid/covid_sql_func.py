import json

from App import engine
from sqlalchemy.sql import text
import re
from flask import jsonify

def search_ref_analito():
    erro = {}
    updt = {}
    sql = 'SELECT * from analitos_covid'
    with engine.connect() as conn:
        try:
            result = conn.execute(text(sql))
            i = 0
            for row in result:
                idanalito = str(row[0])
                descricao = row[1]
                sql_ref = "SELECT idexame,valreferencia,unidademedida, COUNT(*)\n"\
                      "FROM exames_pacientes_covid WHERE idanalito="+idanalito+" GROUP BY 1,2,3"
                resultchild = conn.execute(text(sql_ref))
                for rowchild in resultchild:
                    try:
                        descvalref = rowchild[1]
                        unmed = rowchild[2]

                        if descvalref != None:
                            valref = re.split('\s',descvalref)
                            try:
                                valref_min = re.findall(r"[-+]?\d*\.\d+|\d+",valref[0])
                                valref_min = valref_min[0]
                            except:
                                valref_min = None
                            try:
                                if valref[2]:
                                    valref_max = re.findall(r"[-+]?\d*\.\d+|\d+",valref[2])
                                    valref_max = valref_max[0]
                            except:
                                valref_max = None
                        else:
                            valref_min = None
                            valref_max = None

                        sql_update = 'UPDATE analitos_covid SET valref_max={}, valref_min = {},'\
                        'descvalref = {}, unidademedida={} WHERE id={}'.format(str(valref_max) if valref_max != None else 'NULL',
                                                             str(valref_min) if valref_min != None else 'NULL',
                                                             "'"+str(descvalref)+"'" if descvalref != None else 'NULL',
                                                             "'"+unmed+"'" if unmed != None else 'NULL',
                                                             idanalito)

                        conn.execute(text(sql_update))
                        print('Passou:'+idanalito)
                        updt[i] = 'Passou: '+descricao
                    except:
                        erro[i] = 'Error: '+descricao
                        print('Error:'+idanalito)
                    i +=1
        finally:
            conn.close()
    return jsonify({'error':erro,'update':updt,'finalizado':True})


def call_procedure_insert_exame_paciente(data):
    #CALL insert_exame_paciente('Dosagem de D-Dímero','D-Dímero','00006490d57666d73747c29c01079b60b1353002',
    #'2020-06-04','HOSP','863',863,'ng/mL FEU','<=500',@outsaida);
    #SELECT(@outsaida);
    sql = text("CALL insert_exame_paciente('{}', '{}', '{}', '{}','{}','{}','{}','{}', '{}', @outsaida);"\
        .format(data['exame'],
                data['analito'],
                data['paciente'],
                data['datacoleta'],
                data['origem'],
                data['resultado'],
                data['valresultado'],
                data['unidademedida'],
                data['valreferencia']))
    print(sql)
    from App import db
    try:
        conn = engine.raw_connection()
        paramenterout="@outsaida"
        cursor = conn.cursor()
        parameter = [data['exame'],
                data['analito'],
                data['paciente'],
                data['datacoleta'],
                data['origem'],
                data['resultado'],
                data['valresultado'],
                data['unidademedida'],
                data['valreferencia'], paramenterout]
        cursor.callproc('insert_exame_paciente',parameter)
        results = list(cursor.fetchall())
        cursor.close()
        conn.commit()
    finally:
        conn.close()