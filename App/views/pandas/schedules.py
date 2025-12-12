import json
import os
import pandas as pd
from App.model.pandas.schedules import Schedules
from flask_paginate import get_page_args, get_page_parameter, Pagination
from flask import render_template,request,send_file,current_app
from App.schema.pandas.pandas import SchedulesSchema
from sqlalchemy import and_
from sqlalchemy.sql.expression import func

def get_schedules(page,per_page):
        gerarcsv = request.args.get('gerarcsv') if request.args.get('gerarcsv') != None else 'N'

        ckb_dt = request.args.get('ckb_dt') if request.args.get('ckb_dt') != None else 'N'

        ckb_phone = request.args.get('ckb_phone') if request.args.get('ckb_phone') != None else 'N'
        ckb_nome = request.args.get('ckb_nome') if request.args.get('ckb_nome') != None else 'N'
        edtnome = request.args.get('edtnome') if request.args.get('edtnome') != None else ''

        ckb_localidade = request.args.get('ckb_localidade') if request.args.get('ckb_localidade') != None else 'N'
        ckb_nolocalidade = request.args.get('ckb_nolocalidade') if request.args.get('ckb_nolocalidade') != None else 'N'
        uf = request.args.get('uf') if request.args.get('uf') != None else '0'
        idcidade = request.args.get('idcidade') if request.args.get('idcidade') != None else '0'

        totcarphone = 8 if ckb_phone=='S' else -1
        if ckb_localidade == 'N':
            schedules = Schedules.query.\
                        filter(and_(func.length(Schedules.home_phone_two)>totcarphone,
                                Schedules.birthyday!=None if ckb_dt=='S' else Schedules.id>-1,
                                Schedules.idcidade==None if ckb_nolocalidade=='S' else Schedules.id>-1,
                                Schedules.name.like(edtnome+'%') if ckb_nome=='S' else Schedules.id>-1)).\
                        paginate(page=int(page),per_page=int(per_page), error_out=False)
        else:
            if idcidade != '0' and len(idcidade) > 0:
                schedules = Schedules.query. \
                            filter(and_(func.length(Schedules.home_phone_two) > totcarphone,
                                Schedules.birthyday != None if ckb_dt == 'S' else Schedules.id > -1,
                                Schedules.idcidade == idcidade,
                                Schedules.name.like(edtnome + '%') if ckb_nome == 'S' else Schedules.id > -1)). \
                            paginate(page=int(page), per_page=int(per_page), error_out=False)
            else:
                from App.model.localidades.uf import UF
                from App.model.localidades.cidades import Cidades
                schedules = Schedules.query. \
                    join(Cidades,Schedules.idcidade==Cidades.id). \
                    join(UF,Cidades.iduf==UF.id).\
                    filter(and_(func.length(Schedules.home_phone_two) > totcarphone,
                                Schedules.birthyday != None if ckb_dt == 'S' else Schedules.id > -1,
                                UF.sigla==uf,
                                Schedules.name.like(edtnome + '%') if ckb_nome == 'S' else Schedules.id > -1)). \
                    paginate(page=int(page), per_page=int(per_page), error_out=False)
        if schedules:
            page, per_page, offset = get_page_args()

            from App.funcs.getpagination import get_pagination
            pagination = get_pagination(
                page=page,
                per_page=per_page,
                total=schedules.total,
                record_name="Contatos",

            )
            schedulesschema = SchedulesSchema(exclude=['internet_free_busy'])
            resultschedules = schedulesschema.dump(schedules.items,many=True)



            result = True if schedules.total > 0 else False
            ckb_nome = 'checked' if ckb_nome == 'S' else ' '
            ckb_dt = 'checked' if ckb_dt == 'S' else ' '
            ckb_phone = 'checked' if ckb_phone == 'S' else ' '
            ckb_localidade = 'checked' if ckb_localidade == 'S' else ' '
            ckb_nolocalidade = 'checked' if ckb_nolocalidade == 'S' else ' '

            from App.views.localidades.cidades import get_cidade
            cidade = ''
            if idcidade != '0':
                cidade = get_cidade(idcidade)[0]
                cidade = cidade.nome


            edtnome = edtnome

            if gerarcsv == 'S':
                try:
                    localesave = 'App/'+current_app.config['DOWNLOAD_FOLDER']
                    filename = 'contact_renzo.csv'

                    spath = os.path.join(localesave, filename)

                    if os.path.exists(spath):
                        os.remove(spath)

                    df = pd.DataFrame(resultschedules)
                    df.to_csv(spath)
                except:
                    gerarcsv = 'N'

            return render_template('layouts/pandas/schedules/main.html',
                                   schedules= resultschedules,
                                   pagination= pagination,
                                   result=result,
                                   ckb_nome=ckb_nome,
                                   ckb_dt=ckb_dt,
                                   ckb_phone=ckb_phone,
                                   edtnome=edtnome,
                                   ckb_localidade=ckb_localidade,
                                   ckb_nolocalidade=ckb_nolocalidade,
                                   cidade=cidade,
                                   uf=uf,
                                   arqcsv_gerado=True if gerarcsv=='S' else False)


def get_schedules_by_name(name):
    """schedule = Schedules.query.filter(Schedules.name==name).all()
    if schedule:
        return schedule"""
    return None

def download_schedules_csv():
    localesave = current_app.config['DOWNLOAD_FOLDER']
    filename = 'contact_renzo.csv'


    return send_file(localesave+filename,as_attachment=True)