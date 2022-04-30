from flask import Blueprint,jsonify,request
from App.views.bolsavalores import setor_bolsa
routessetorbolsa = Blueprint('routessetorbolsa',__name__)

@routessetorbolsa.route('/get/setores/all/bolsavalores')
def get_all_setor():
    return jsonify(setor_bolsa.get_all_setoresbolsa())


@routessetorbolsa.route('/add/setor/bolsavalores',methods=['GET'])
def add_setor():
    if request.method == 'GET':
        if len(request.args.get('name') >= 0):
            return jsonify(setor_bolsa.add_setor(request.args.get('name')))
    return jsonify({'data':{},'result':False})
