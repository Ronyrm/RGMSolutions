from flask import Blueprint,jsonify,render_template
from App.views.pandas import import_contacts,read_medicamentos_anvisa,read_data_covid
routespandas= Blueprint('routespandas',__name__)


# Convert csv em json
@routespandas.route('/pandas/converter/csv/json', methods=['POST'])
def convert_csvtojson_contact():
    return import_contacts.csv_to_json()

# Chama tela principal conversor csv em json
@routespandas.route('/main/pandas/converter/csv/json')
def main_convert_csvtojson_contact():
    return render_template('layouts/pandas/convert_csv_to_json/main.html')


@routespandas.route('/pandas/read/medicamentos_anvisa/xls/csv',methods=['POST'])
def read_medicamentos_anvisa_xls_to_csv():
    return jsonify(read_medicamentos_anvisa.read_medicamentos_anvisa_xls_to_csv())


# CONVERTE DADOS CSV MEDICAMENTOS ANVISA PARA O BANCO DE DADOS
@routespandas.route('/pandas/read/medicamentos_anvisa/csv/db',methods=['POST'])
def read_medicamentos_anvisa_xls_to_db():
    return jsonify(read_medicamentos_anvisa.read_medicamentos_anvisa_csv_db())


# ------------------------------- Albert Einstein ---------------------------
@routespandas.route('/pandas/read/covid19/cadastro/pacientes/eisntein',methods=['POST'])
def read_data_covid19_paciente_einstein():
    return jsonify(read_data_covid.read_covid19_pacientes_einstein_csv())


@routespandas.route('/pandas/read/covid19/exames/pacientes/eisntein',methods=['POST'])
def read_data_covid19_exames_einstein():
    return jsonify(read_data_covid.read_covid19_exames_einstein_csv())

@routespandas.route('/pandas/readwrite/covid19/exames/pacientes/eisntein/two')
def readwrite_data_covid19_exames_einstein_two():
    return jsonify(read_data_covid.readwrite_covid_exames_eistein_csv_mydb_two())


# ------------------------------- Hospital das Clinicas São Paulo ---------------------------
@routespandas.route('/pandas/read/covid19/cadastro/pacientes/hc',methods=['POST'])
def read_data_covid19_paciente_hc():
    return jsonify(read_data_covid.read_covid19_pacientes_hc_csv())


@routespandas.route('/pandas/readwrite/covid19/exames/pacientes/hc/two')
def read_data_covid19_exames_hc():
    return jsonify(read_data_covid.read_covid19_exames_hc_csv())
