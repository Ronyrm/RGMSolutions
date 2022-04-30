from flask import jsonify,Blueprint,request
from App.views.bolsavalores import cotacoes_bolsa
from App.funcs.funcs import format_date_yyyymmaa
routescotacoesbolsa = Blueprint('routescotacoesbolsa',__name__)

@routescotacoesbolsa.route('/get/cotacoes/empresa/data/<name>/<dtcotacao>')
def get_cotacoes_by_name_data(name,dtcotacao):
    return jsonify(cotacoes_bolsa.get_cotacao_by_papel_and_date(name,format_date_yyyymmaa(dtcotacao)))


@routescotacoesbolsa.route('/add/cotacao/empresa',methods=['POST'])
def add_cotacao_empresa():
    if request.method == 'POST':
        data = request.form
    return jsonify(cotacoes_bolsa.add_cotacao(data))
