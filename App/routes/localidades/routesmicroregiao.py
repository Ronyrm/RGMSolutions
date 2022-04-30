from flask import Blueprint
from flask import jsonify,request
from App.views.localidades import microregiao
from App.schema.localidades.localidades import MicroRegiaoSchema


routesmicroregiao = Blueprint('routesmicroregiao',__name__)

# BUSCA MICROREGIAO POR ID, SE FOR 0, RETORNA TODOS
@routesmicroregiao.route('/microregiao/<idmicroregiao>', methods=['GET'])
def get_all_regiao(idmicroregiao):
    microregiaoschema = MicroRegiaoSchema(only=['id','nome','mesoregiao.id'])
    result = microregiao.get_microregiao(idmicroregiao)
    return jsonify({'data':microregiaoschema.dump(result,many=True)})

@routesmicroregiao.route('/microregiao/uf/<iduf>', methods=['GET'])
def get_microregiao_by_uf(iduf):
    microregiaoschema = MicroRegiaoSchema()
    result = microregiao.get_by_uf_microregiao(iduf)
    return jsonify({'data':microregiaoschema.dump(result,many=True)})

@routesmicroregiao.route('/get/microregiao/regiao/<iduf>', methods=['GET'])
def get_microregiao_by_regiao(iduf):
    data = []
    if len(request.args)>0:
        data = request.args.get('dataonly').split(',')

    if len(data)>0 and data[0]!='':
        microregiaoschema = MicroRegiaoSchema(only=data)
    else:
        microregiaoschema = MicroRegiaoSchema()

    result = microregiao.get_by_regiao_microregiao(iduf)
    return jsonify({'data':microregiaoschema.dump(result,many=True)})
