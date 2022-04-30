from flask import Blueprint,jsonify,request
from App.views.bolsavalores import subsetor_bolsa
routessubsetorbolsa = Blueprint('routessubsetorbolsa',__name__)

@routessubsetorbolsa.route('/get/subsetores/all/bolsavalores')
def get_all_subsetor():
    return jsonify(subsetor_bolsa.get_all_subsetoresbolsa())

@routessubsetorbolsa.route('/add/subsetor/bolsavalores',methods=['GET'])
def add_subsetor():
    if request.method == 'GET':
        if len(request.args.get('name') >= 0):
            return jsonify(subsetor_bolsa.add_subsetor(request.args.get('name')))
    return jsonify({'data':{},'result':False})
