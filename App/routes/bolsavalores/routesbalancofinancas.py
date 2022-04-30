from flask import Blueprint, request, jsonify
from App.views.bolsavalores import balancofinancas_bolsa

routesbalancofinancas = Blueprint('routesbalancofinancas',__name__)

@routesbalancofinancas.route('/get/balanco/financas/bolsavalores/<papel>/json')
def get_balancofinancas_json_by_papel(papel):
    return jsonify(balancofinancas_bolsa.get_balancofinancas_json_by_papel(papel))

