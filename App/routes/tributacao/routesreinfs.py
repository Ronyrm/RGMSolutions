from flask import Blueprint,jsonify
from App.views.tributacao import reinfs
routesreinfs = Blueprint('routesreinfs',__name__)

@routesreinfs.route('/get/tributacao/reinfs/json',methods=['GET'])
def get_reinfs():
    return jsonify(reinfs.get_REINFs())

@routesreinfs.route('/insert/tributacao/reinfs',methods=['POST'])
def insert_into_reinfs():
    return jsonify(reinfs.insert_into_sql())
