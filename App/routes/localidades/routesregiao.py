from flask import Blueprint
from App.views.localidades import regiao
from App.schema.localidades.localidades import RegiaoSchema
from flask import jsonify

routesregiao = Blueprint('routesregiao',__name__)


@routesregiao.route('/get/all/localidade/regiao/<idregiao>', methods=['GET'])
def get_regiao(idregiao):
    try:
        regschema = RegiaoSchema()
        region = regiao.get_regiao(idregiao)
        return jsonify({'data':regschema.dump(region,many=True)})
    except:
        return jsonify({'data': {},'erro':True})
