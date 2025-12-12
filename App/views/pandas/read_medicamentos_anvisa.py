import pandas as pd
from flask import request,current_app
from werkzeug.utils import secure_filename
import os

def read_medicamentos_anvisa_xls_to_csv():
    filexls = None
    if request.method == 'POST':
        if 'filexls' in request.files:
            filexls = request.files['filexls']

    if filexls:
        filename = secure_filename(filexls.filename)
        localesave = current_app.config['UPLOAD_FOLDER']

        spath = os.path.join(localesave, filename)

        if os.path.exists(spath):
            os.remove(spath)

        filexls.save(spath)

        dataframe = pd.read_excel(spath)
        dataframe.to_csv(localesave+'medicamentosanvisa.csv')
        return {}

def read_medicamentos_anvisa_csv_db():
    from App.views.anvisa.func_anvisa import add_arq_csv_in_db
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

        dataframe = pd.read_csv(spath)
        print(dataframe)

        for rowpai in dataframe.values:
            print(rowpai[1] + rowpai[2])
            add_arq_csv_in_db(rowpai)
        return {'result':'Finalizado'}




