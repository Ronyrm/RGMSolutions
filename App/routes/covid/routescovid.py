"""
Este trabalho utilizou dados disponibilizados pelo repositório COVID-19 Data Sharing/BR,
disponível em: “ https://repositoriodatasharingfapesp.uspdigital.usp.br/".
"""

from flask import Blueprint,request,jsonify,render_template
from App.views.covid import pacientes_covid,hospitais,exames_covid,analitos_covid,exames_pacientes_covid
routescovid = Blueprint('routescovid',__name__)


# -------------------------------------  HOSPITAIS ----------------------------
@routescovid.route('/add/covid/hospital',methods=['POST'])
def add_hospital():
    if request.method == 'POST':
        data = request.form
        if data['name'] != None:
            hospital = hospitais.add_hospital(data['name'])
            if hospital:
                return jsonify({'data':{'id':hospital.id,
                                        'name':hospital.name
                                        },
                                'result':True})
    return jsonify({'data':{},'result':False})

@routescovid.route('/get/covid/hospitais/json',methods=['GET'])
def get_hospitais_json():
    return  jsonify(hospitais.get_hospitais_json())

# -------------------------------------  PACIENTES ----------------------------
@routescovid.route('/add/covid/paciente',methods=['POST'])
def add_paciente():
    if request.method == 'POST':
        data = request.form
        pacient = pacientes_covid.add_paciente(data)
        if pacient:
            return jsonify({'data':{'id':pacient.id,
                                    'idpaciente':pacient.idpaciente},
                            'result':True})
    return jsonify({'data':{},'result':True})

@routescovid.route('/get/covid/pacientes/json',methods=['GET'])
def get_pacientes_json():
    pacientes_covid.get_pacientes_json()

# -------------------------------------  Exames ----------------------------
@routescovid.route('/add/covid/exame',methods=['POST'])
def add_exame():
    if request.method == 'POST':
        data = request.form
        if data['desc'] != None:
            exame = exames_covid.add_exame(data['name'])
            if exame:
                return jsonify({'data':{'id':exame.id,
                                        'descricao':exame.descricao
                                        },
                                'result':True
                                })
    return jsonify({'data':{},'result':False})


@routescovid.route('/get/covid/exames/json',methods=['GET'])
def get_exames_json():
    return exames_covid.get_exames_json()


# -------------------------------------  Analitos ----------------------------
@routescovid.route('/add/covid/analitos',methods=['POST'])
def add_analitos():
    if request.method == 'POST':
        data = request.form
        if data['desc'] != None:
            analito = analitos_covid.add_analito(data['name'],data['idexame'])
            if analito:
                return jsonify({'data':{'id':analito.id,
                                        'descricao':analito.descricao
                                        },
                                'result':True
                                })
    return jsonify({'data':{},'result':False})


@routescovid.route('/get/covid/analitos/json',methods=['GET'])
def get_analitos_json():
    return analitos_covid.get_analitos_json()



# -------------------------------------  Exames Pacientes Covid ----------------------------
@routescovid.route('/add/covid/exame/paciente/',methods=['POST'])
def add_exame_paciente():
    if request.method == 'POST':
        data = request.form
        examepaciente = exames_pacientes_covid.add_exame_paciente(data)
        if examepaciente:
            return jsonify({'data':{'id':examepaciente.id,
                                    'datacoleta':examepaciente.datacoleta
                                    },
                                'result':True
                                })
    return jsonify({'data':{},'result':False})

#@routescovid.route('/get/covid/exame/paciente/json',methods=['GET'])
#def get_exame_paciente_json():
#    return exames_pacientes_covid.get_exames_pacientes_json()




# ------------------------------- Funções e SQL COVID --------------------------
@routescovid.route('/update/analitos/valorreferencia')
def update_analitos_valref():
    from App.views.covid.covid_sql_func import search_ref_analito
    return search_ref_analito()


# Captura os Exames Relacionandos ao paciente
@routescovid.route('/get/covid/exames/pacientes/json',methods=['GET'])
def get_exames_pacientes_by_idpaciente():
    return exames_pacientes_covid.get_exames_pacientes_json()


# Abre Pagina Web Exames Relacionandos ao paciente
@routescovid.route('/get/exames/paciente/main',methods=['GET'])
def main_exames_paciente():
    codpaciente = '0'
    if request.method == 'GET':
        codpaciente = request.args.get('codpaciente') if request.args.get('codpaciente') != None else '0'
        pageatual = request.args.get('pageatual') if request.args.get('pageatual') != None else '1'
        per_page = request.args.get('per_page') if request.args.get('per_page') != None else '50'
        idexame = request.args.get('idexame') if request.args.get('idexame') != None else ''
        idanalito = request.args.get('idanalito') if request.args.get('idanalito') != None else ''
        idhospital = request.args.get('idhospital') if request.args.get('idhospital') != None else ''
        tpfiltro = request.args.get('tpfiltro') if request.args.get('tpfiltro') != None else '0'
        resultado = request.args.get('resultado') if request.args.get('resultado') != None else ''
        vlresultado = request.args.get('vlresultado') if request.args.get('vlresultado') != None else ''
        tpoperadorresultado = request.args.get('tpoperadorresultado') if request.args.get('tpoperadorresultado') != None else ''
        tpoperadoridade = request.args.get('tpoperadoridade') if request.args.get('tpoperadoridade') != None else ''
        idade = request.args.get('idade') if request.args.get('idade') != None else None
        sexo = request.args.get('sexo') if request.args.get('sexo') != None else None

        return render_template('layouts/covid/exames_paciente/main.html',
                                codpaciente=codpaciente,
                                pageatual=pageatual,
                                per_page=per_page,
                                idhospital=idhospital,
                                idexame=idexame,
                                idanalito=idanalito,
                                tpfiltro=tpfiltro,
                                resultado=resultado,
                                vlresultado=vlresultado,
                                tpoperadorresultado=tpoperadorresultado,
                                tpoperadoridade=tpoperadoridade,
                                idade = idade,
                                sexo = sexo
                                )

# Busca total exames de um determinado paciente e agrupo por data
@routescovid.route('/get/total/exames/paciente/data/json', methods=['GET'])
def get_tot_reg_by_data_idpaciente():
    return jsonify(exames_pacientes_covid.get_tot_reg_by_data_idpaciente())

# get pacientes json
@routescovid.route('/get/pacientes/json', methods=['GET'])
def get_paciente_exames_analito_total_reg_json():
    return jsonify(pacientes_covid.get_paciente_exames_analito_total_reg())

@routescovid.route('/sishealth/get/pacientes/main', methods=['GET'])
def get_paciente_main():
    return pacientes_covid.get_paciente_main()