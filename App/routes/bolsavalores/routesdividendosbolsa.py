from flask import request,jsonify,Blueprint
from App.views.bolsavalores import dividendos_history_bolsa
from App.funcs.funcs import format_date_yyyymmaa

routesdividendosbolsa = Blueprint('routesdividendosbolsa',__name__)

@routesdividendosbolsa.route('/get/dividendos/all/empresa/<name>')
def get_all_dividendos_by_papel(name):
    jsonify(dividendos_history_bolsa.get_all_dividendos_by_idpapel(name))

@routesdividendosbolsa.route('/add/dividendos/empresa',methods=['POST'])
def add_dividendo():
    if request.method == 'POST':
        data = request.form
        jsonify({'result':dividendos_history_bolsa.add_dividendos(data)})
    jsonify({'result':False})

@routesdividendosbolsa.route('/get/dividendos/empresa/interval/data/<papel>/<dt_ini>/<dt_fim>')
def get_all_dividendos_by_papel_intervaldata(papel,dt_ini,dt_fim):
    return jsonify(dividendos_history_bolsa.get_dividendos_by_idpapel_and_intervaldate(papel,
                                                                                format_date_yyyymmaa(dt_ini),
                                                                                format_date_yyyymmaa(dt_fim)))


@routesdividendosbolsa.route('/get/dividendos/empresa/interval/mensal/<papel>/<dt_ini>/<dt_fim>')
def get_all_dividendos_by_papel_intervalmensal(papel, dt_ini, dt_fim):
    try:
        return dividendos_history_bolsa.get_dividendos_mesano_by_idpapel_and_interval_mensal(papel,
                                                                                                     format_date_yyyymmaa(dt_ini),
                                                                                                     format_date_yyyymmaa(dt_fim))
    except Exception as e:
        return jsonify({'error':str(e)})

@routesdividendosbolsa.route('/get/total/dividendos/ano/<papel>')
def get_valor_total_diviendos_12ult_meses(papel):
  return jsonify(dividendos_history_bolsa.get_valor_total_diviendos_12ult_meses(papel))