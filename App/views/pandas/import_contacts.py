import re

from App import db

import pandas as pd
from werkzeug.utils import secure_filename
import os
import json
from flask import  request,current_app
from App.views.localidades.cidades import get_cidade_by_uf_and_city
from App.funcs.funcs import format_date_yyyymmaa
def csv_to_json():
    # formata de o campo for tipo float, colocando como string vazia
    def format_cp(val):
        if type(val) == float:
            return ''
        return val
    # busca idcidade
    def return_idcidade(city, state):
        cidade = get_cidade_by_uf_and_city(state,city)
        if cidade:
            return cidade.id
        return None


    filesvc = None
    if request.method == 'POST':
        if 'filecsv' in request.files:
            filesvc = request.files['filecsv']

    if filesvc:
        filename = secure_filename(filesvc.filename)
        localesave = current_app.config['UPLOAD_FOLDER']


        spath = os.path.join(localesave,filename)

        if os.path.exists(spath):
            os.remove(spath)

        filesvc.save(spath)

        dataframe = pd.read_csv(spath)

        #dataframe = dataframe.filter(regex='(?!=^nan)')
        array_reg = dataframe.to_numpy()
        array_index = dataframe.index.values
        i = 0

        from App.model.pandas.schedules import Schedules
        from App.views.pandas.schedules import get_schedules_by_name
        from App.views.several import busca_dados_CEP
        for row_pai in array_index:
            if not get_schedules_by_name(row_pai):
                schedule = Schedules()
                schedule.name = format_cp(row_pai)
                array_contato = array_reg[i]
                schedule.first_name = format_cp(array_contato[0])
                schedule.middle_name = format_cp(array_contato[1])
                schedule.last_name = format_cp(array_contato[2])
                schedule.title = format_cp(array_contato[3])
                schedule.suffix = format_cp(array_contato[4])
                schedule.initials = format_cp(array_contato[5])
                schedule.webpage = format_cp(array_contato[6])
                schedule.birthyday =  format_date_yyyymmaa(format_cp(array_contato[7]))

                schedule.gender = format_cp(array_contato[8])
                schedule.anniversay = format_cp(array_contato[9])
                schedule.location = format_cp(array_contato[10])
                schedule.language = format_cp(array_contato[11])
                schedule.internet_free_busy = format_cp(array_contato[12])
                schedule.notes = format_cp(array_contato[13])
                schedule.email_address_one = format_cp(array_contato[14])
                schedule.email_address_two = format_cp(array_contato[15])
                schedule.email_address_tree = format_cp(array_contato[16])
                schedule.primary_phone = format_cp(array_contato[17])
                schedule.home_phone_one = format_cp(array_contato[18])
                schedule.home_phone_two = format_cp(array_contato[19])
                schedule.mobile_phone = format_cp(array_contato[20])
                schedule.company_main_phone = format_cp(array_contato[37])
                schedule.company_business_phone_one = format_cp(array_contato[38])
                schedule.company_business_phone_two = format_cp(array_contato[39])
                schedule.assistents_phone = format_cp(array_contato[41])
                schedule.company = format_cp(array_contato[42])
                schedule.job_title = format_cp(array_contato[43])
                schedule.departament = format_cp(array_contato[44])
                schedule.ofice_location = format_cp(array_contato[45])
                schedule.profission = format_cp(array_contato[47])
                schedule.account = format_cp(array_contato[48])
                schedule.business_address = format_cp(array_contato[49])
                schedule.business_street_one = format_cp(array_contato[50])
                schedule.business_street_two = format_cp(array_contato[51])
                schedule.business_street_tree = format_cp(array_contato[52])
                schedule.business_address_po_box = format_cp(array_contato[53])
                schedule.business_city = format_cp(array_contato[54])
                tam = len(schedule.business_city)
                if tam > 0 :
                    pos = tam - 3
                    city = re.sub(',', '', schedule.business_city[0:pos])
                    state = schedule.business_city[tam - 2:tam]
                    idcidade = return_idcidade(city,state)
                    if idcidade:
                        schedule.idcidade = idcidade
                schedule.business_code_postal = format_cp(array_contato[55])

                """try:
                    if len(schedule.business_code_postal)>0:
                        cep_json = busca_dados_CEP(schedule.business_code_postal)
                        schedule.idcidade = cep_json["ibge"]
                except:
                    pass"""

                schedule.business_country = format_cp(array_contato[56])
                schedule.outher_phone = format_cp(array_contato[57])
                db.session.add(schedule)
                db.session.commit()
            i+=1

        print(array_reg)
        sjson = dataframe.to_json(orient="split")
        return json.dumps(json.loads(sjson),indent=4)