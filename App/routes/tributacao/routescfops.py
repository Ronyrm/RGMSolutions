from flask import Blueprint,jsonify
from App.views.tributacao import cfops

routescfops = Blueprint('routescfops',__name__)

@routescfops.route('/get/tributacao/cfops/json',methods=['GET'])
def get_cfops():
    return jsonify(cfops.get_CFOPs())

@routescfops.route('/insert/tributacao/cfops',methods=['POST'])
def insert_into_CFOPs():
    return jsonify(cfops.insert_into_sql())