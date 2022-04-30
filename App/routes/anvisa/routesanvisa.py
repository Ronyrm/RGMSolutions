from flask import Blueprint,request,jsonify,render_template
from App.views.anvisa import substancias_anvisa
from App.views.anvisa import tipos_medicamentos_anvisa
from App.views.anvisa import laboratorios_anvisa
from App.views.anvisa import classe_terapeurica_anvisa
from App.views.anvisa import medicamentos_anvisa
from App.views.anvisa import tabpreco_medicamento_anvisa

routesanvisa = Blueprint('routesanvisa',__name__)


@routesanvisa.route('/anvisa/main')
def main_anvisa():
    return render_template('layouts/anvisa/main.html')


#________________________________SUBSTANCIA________________________________#



# GET SUBSTANCIA
@routesanvisa.route('/get/anvisa/substancia',methods=['GET'])
def get_substancia():
    if request.method == 'GET':
        desc = request.args.get('desc') if request.args.get('desc') != None  else ''
        return jsonify(substancias_anvisa.get_substancia_anvisa(desc))



@routesanvisa.route('/get/anvisa/substancias/json',methods=['GET'])
def get_substancia_json():
    return jsonify(substancias_anvisa.get_substancias_json())


# ADD SUBSTANCIA
@routesanvisa.route('/add/anvisa/substancia',methods=['POST'])
def add_substancia():
    if request.method == 'POST':
        data = request.form

        result = substancias_anvisa.add_substancia_anvisa(data['desc'])
        return jsonify(result)
    return jsonify({'result':False,'data':{}})





#________________________________TIPO MEDICAMENTO________________________________#

# GET TIPO MEDICAMENTO
@routesanvisa.route('/get/anvisa/tipomedicamento',methods=['GET'])
def get_tipomedicamento():
    if request.method == 'GET':
        desc = request.args.get('desc') if request.args.get('desc') != None  else ''

        return jsonify(tipos_medicamentos_anvisa.get_tipo_medicamento(desc))


@routesanvisa.route('/get/anvisa/tiposmedicamentos/json',methods=['GET'])
def get_tiposmedicamentos_json():
    return jsonify(tipos_medicamentos_anvisa.get_tipos_medicamentos_json())


# ADD TIPOMEDICAMENTO
@routesanvisa.route('/add/anvisa/tipomedicamento',methods=['POST'])
def add_tipomedicamento():
    if request.method == 'POST':
        data = request.form

        result = tipos_medicamentos_anvisa.add_tipo_medicamento(data['desc'])
        return jsonify(result)
    return jsonify({'result':False,'data':{}})




#________________________________LABORATORIO________________________________#

# GET LABORATORIO POR DESCRICAO OU CNPJ
@routesanvisa.route('/get/anvisa/laboratorio',methods=['GET'])
def get_laboratorio():
    if request.method == 'GET':
        q = request.args.get('q') if request.args.get('q') != None  else ''
        tp_filtro = request.args.get('tpfiltro') if request.args.get('tpfiltro') != None  else ''

        return jsonify(laboratorios_anvisa.get_laboratorio(q,tp_filtro))

# GET LABORATORIOS
@routesanvisa.route('/get/anvisa/laboratorios/json',methods=['GET'])
def get_laboratorios_json():
    return jsonify(laboratorios_anvisa.get_laboratorios_json())


# ADD LABORATORIOS
@routesanvisa.route('/add/anvisa/laboratorio',methods=['POST'])
def add_laboratorio():
    if request.method == 'POST':
        data = request.form

        result = laboratorios_anvisa.add_laboratorio(data['name'],data['cnpj'])
        return jsonify(result)
    return jsonify({'result':False,'data':{}})


#________________________________CLASSE TERAPEUTICA________________________________#

# GET CLASSE TERAPEUTICA
@routesanvisa.route('/get/anvisa/classeterapeutica',methods=['GET'])
def get_classeterapeurica():
    if request.method == 'GET':
        desc = request.args.get('desc') if request.args.get('desc') != None  else ''

        return jsonify(classe_terapeurica_anvisa.get_classe_terapeutica(desc))


# ADD CLASSE TERAPEUTICA
@routesanvisa.route('/add/anvisa/classeterapeutica',methods=['POST'])
def add_classeterapeurica():
    if request.method == 'POST':
        data = request.form

        result = classe_terapeurica_anvisa.add_classe_terapeurica(data['desc'])
        return jsonify(result)
    return jsonify({'result':False,'data':{}})


# GET CLASSES TERAPEUTICAS
@routesanvisa.route('/get/anvisa/classesterapeutica/json',methods=['GET'])
def get_classes_terapeutica_json():
    return jsonify(classe_terapeurica_anvisa.get_classes_terapeutica_json())


#________________________________MEDICAMENTOS________________________________#

# GET MEDIAMENTO
@routesanvisa.route('/get/anvisa/medicamento',methods=['GET'])
def get_medicamento():
    if request.method == 'GET':
        desc = request.args.get('desc') if request.args.get('desc') != None  else ''
        apresentacao = request.args.get('apresentacao') if request.args.get('apresentacao') != None else ''

        return jsonify(medicamentos_anvisa.get_medicamento_by_desc_and_apresentacao(desc,apresentacao))


# ADD MEDICAMENTO
@routesanvisa.route('/add/anvisa/medicamento',methods=['POST'])
def add_medicamento():
    if request.method == 'POST':
        data = request.form

        result = medicamentos_anvisa.add_medicamento(data)
        return jsonify(result)
    return jsonify({'result':False,'data':{}})


# GET MEDICAMENTOS
@routesanvisa.route('/get/anvisa/medicamentos/json',methods=['GET'])
def get_medicamentos_json():
    return jsonify(medicamentos_anvisa.get_medicamentos_json())



#________________________________TABELA DE PRECOS MEDIAMENTO________________________________#
# GET TABELA DE PRECOS MEDIAMENTO
@routesanvisa.route('/get/anvisa/medicamento/<idmedicamento>/tabelapreco',methods=['GET'])
def get_tabpreco_medicamento(idmedicamento):

    return jsonify(tabpreco_medicamento_anvisa.get_tabpreco_by_idmedicamento(idmedicamento))



@routesanvisa.route('/get/anvisa/medicamento/<idmedicamento>/tabelapreco/json',methods=['GET'])
def get_tabpreco_medicamento_json(idmedicamento):

    return jsonify(tabpreco_medicamento_anvisa.get_tabpreco_by_idmedicamento_json(idmedicamento))



# GET TABELA DE PRECOS MEDIAMENTO por descricao do medicamento
@routesanvisa.route('/get/anvisa/tabelapreco/medicamentos',methods=['GET'])
def get_tabpreco_medicamento_by_desc_medicamento():
    return jsonify(tabpreco_medicamento_anvisa.get_tabpreco_by_desc_medicmento_json())




# ADD  TABELA DE PRECOS MEDICAMENTOS
@routesanvisa.route('/add/anvisa/medicamento/tabelapreco',methods=['POST'])
def add_tabpreco_medicamento():
    if request.method == 'POST':
        data = request.form
        result = tabpreco_medicamento_anvisa.add_tabpreco_medicamento(data)
        return jsonify(result)
    return jsonify({'result':False,'data':{}})