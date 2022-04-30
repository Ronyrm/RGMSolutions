from flask import Blueprint
from App.views.localidades import cidades
from flask import jsonify,request
from App.schema.localidades.localidades import CidadesSchema

routescidades = Blueprint('routescidades',__name__)


#Pesquisa Cidade Por id ou por nome
@routescidades.route('/get/cidade/<idcidade>', methods=['GET'])
def get_cidade(idcidade):
    try:
        data = []
        if len(request.args) > 0:
            data = request.args.get('dataonly').split(',')

        if len(data) > 0 and data[0] != '':
            cidadesschema = CidadesSchema(only=data)
        else:
            cidadesschema = CidadesSchema()

        cidade = cidades.get_cidade(idcidade)
        return jsonify({'data':cidadesschema.dump(cidade,many=True)})
    except:
        return jsonify({'data': {},'erro':True})

#Pesquisa Cidade Por id ou por nome
@routescidades.route('/get/cidade/UF/<iduf>', methods=['GET'])
def get_cidade_by_uf(iduf):
    try:
        data = []
        nomecity = ''
        if len(request.args) > 0:
            try:
                data = request.args.get('dataonly').split(',')
            except:
                data = []
            nomecity = request.args.get('nome')
            if nomecity == None:
                nomecity = ''

        if len(data) > 0 and data[0] != '':
            cidadesschema = CidadesSchema(only=data)
        else:
            cidadesschema = CidadesSchema()

        cidade = cidades.get_cidade_by_uf(iduf,nomecity)
        return jsonify({'data':cidadesschema.dump(cidade,many=True)})
    except:
        return jsonify({'data': {},'erro':True})



