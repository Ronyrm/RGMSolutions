from flask import Blueprint
from App.views.localidades import mesoregiao
from flask import render_template,request,jsonify
from App.schema.localidades.localidades import MesoRegiaoSchema

routesmesoregiao = Blueprint('routesmesoregiao',__name__)


# BUSCA MESOREGIAO POR ID ou POR NOME, SE FOR 0, RETORNA TODOS
@routesmesoregiao.route('/mesoregiao/<idmesoregiao>', methods=['GET'])
def get_all_regiao(idmesoregiao):
    mesoregiaoschema = MesoRegiaoSchema()
    result = mesoregiao.get_mesoregiao(idmesoregiao)
    return jsonify({'data':mesoregiaoschema.dump(result,many=True)})


# BUSCA MESOREGIAO POR IDUF OU SIGLA UF
@routesmesoregiao.route('/mesoregiao/uf/<iduf>', methods=['GET'])
def get_mesoregiao_by_uf(iduf):
    mesoregiaoschema = MesoRegiaoSchema(only=['id','nome','uf.sigla','uf.nome','uf.regiao.nome'])
    result = mesoregiao.get_by_uf_mesoregiao(iduf)
    return jsonify({'data':mesoregiaoschema.dump(result,many=True)})

# BUSCA MESOREGIAO POR REGIAO: ID NOME OU SIGLA OU SIGLA UF
@routesmesoregiao.route('/get/mesoregiao/regiao/<idregiao>', methods=['GET'])
def get_mesoregiao_by_regiao(idregiao):
    data = []
    if len(request.args) > 0:
        data = request.args.get('dataonly').split(',')

    if len(data) > 0 and data[0] != '': # Ex: get ?dataonly=id,nome,uf.sigla,uf.nome,uf.regiao.nome
        mesoregiaoschema = MesoRegiaoSchema(only=data)
    else:
        mesoregiaoschema = MesoRegiaoSchema()

    result = mesoregiao.get_by_regiao_mesoregiao(idregiao)
    return jsonify({'data':mesoregiaoschema.dump(result,many=True)})
