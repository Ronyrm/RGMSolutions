from flask import Blueprint,request,jsonify
from App.views.bolsavalores import balancopatrimonial_bolsa

routesbalancopatrimonial = Blueprint('routesbalancopatrimonial',__name__)

@routesbalancopatrimonial.route('/get/balanco/patrimonial/trimenstral/all/<papel>')
def get_balanco_patrimonial_all(papel):
    return jsonify(balancopatrimonial_bolsa.get_balancopatrimonial_all_by_papel_json(papel))

@routesbalancopatrimonial.route('/add/balanco/patrimonial', methods=['POST'])
def add_balanco_patrimonial():
    if request.method == 'POST':
        data = request.form
        return jsonify(balancopatrimonial_bolsa.add_balanco_patrimonial(data))