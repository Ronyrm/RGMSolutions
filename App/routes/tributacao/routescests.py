from flask import Blueprint,jsonify
from App.views.tributacao import cests
from App.model.tributacao.segmentos_cest import SegmentosCest
from App.model.tributacao.cests import Cests

routescests = Blueprint('routescests',__name__)


@routescests.route('/get/tributacao/segmentoscest/json',methods=['GET'])
def get_segmentoscests():
    return jsonify(cests.get_SegmentosCest())


@routescests.route('/get/tributacao/cests/json',methods=['GET'])
def get_cests():
    return jsonify(cests.get_Cests())

@routescests.route('/insert/tributacao/segmentoscest',methods=['POST'])
def insert_into_Segmentos():
    return jsonify(cests.insert_into_sql(SegmentosCest))

@routescests.route('/insert/tributacao/cests',methods=['POST'])
def insert_into_Cests():
    return jsonify(cests.insert_into_sql(Cests))
