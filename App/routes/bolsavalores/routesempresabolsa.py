from flask import Blueprint,jsonify,request,render_template
from App.views.bolsavalores import empresa_bolsa
from App.funcs.funcs import format_date_yyyymmaa

routesempresabolsa = Blueprint('routesempresabolsa',__name__)


@routesempresabolsa.route('/bolsavalores/empresas/main')
def main_bolsavalores_main():
    empresas = empresa_bolsa.get_all_empresabolsa()
    return render_template('layouts/bolsa_valores/update_data_empresas/main.html',tabempresas=empresas)


@routesempresabolsa.route('/get/empresa/all/bolsavalores')
def get_all_empresas():
    return jsonify(empresa_bolsa.get_all_empresabolsa(tipo=0,limit=-1))


@routesempresabolsa.route('/update/empresas/bolsavalores/fundamentus')
def update_papel_empresas():
    return jsonify(empresa_bolsa.update_papel_of_fundamentus())


@routesempresabolsa.route('/get/cotacao/empresas/yfinance/<name>/<dt_start>/<dt_end>')
def capture_detail_yfinance(name,dt_start,dt_end):
    from App.funcs.funcs import format_date_yyyymmaa
    return jsonify(empresa_bolsa.capture_detail_yfinance(name,format_date_yyyymmaa(dt_start),format_date_yyyymmaa(dt_end)))


@routesempresabolsa.route('/get/cotacao/yahoo/empresas/<name>/<dt_start>')
def capture_val_cotacao_datareader_yahoo(name,dt_start):

    return jsonify(empresa_bolsa.capture_val_cotacao_datareader_yahoo(name,format_date_yyyymmaa(dt_start)))

#atualiza dividendos por papel
@routesempresabolsa.route('/get/update/papel/divindedos/<papel>/<dt_ini>/<dt_fim>/<acao>')
def get_update_divindedos_papel(papel,dt_ini,dt_fim,acao):
    return jsonify(empresa_bolsa.get_update_dividendos_by_papel(papel,
                                                                format_date_yyyymmaa(dt_ini),
                                                                format_date_yyyymmaa(dt_fim),
                                                                acao))

@routesempresabolsa.route('/update/papel/all/<dt_ini>/<dt_fim>')
def update_all_papel(dt_ini,dt_fim):
    return jsonify(empresa_bolsa.update_data_papel_with_yfinance(format_date_yyyymmaa(dt_ini),
                                                                 format_date_yyyymmaa(dt_fim)))

@routesempresabolsa.route('/update/papel/bolsa/valores/<idpapel>/<papel>/<dt_ini>/<dt_fim>')
def update_by_papel(idpapel,papel,dt_ini,dt_fim):
    return jsonify(empresa_bolsa.update_data_papel_with_yfinance_by_papel(idpapel,
                                                                 papel,
                                                                 dt_ini,
                                                                 dt_fim))
@routesempresabolsa.route('/update/papel/bolsa/info/<idpapel>/<papel>')
def get_update_info_yfinance_by_papel(idpapel,papel):
    return jsonify(empresa_bolsa.get_update_info_yfinance_by_papel(idpapel,papel))

@routesempresabolsa.route('/get/tickers/statusinvest/cvc',methods=['POST'])
def convert_tickers_csv_statusinvest():
    return jsonify(empresa_bolsa.convert_tickers_csv_statusinvest())


@routesempresabolsa.route('/get/info/ibovespa')
def get_info_Ibovespa():
    return jsonify(empresa_bolsa.get_info_Ibovespa())

@routesempresabolsa.route('/update/prices/ibovespa/<dt_ini>/<dt_fim>')
def update_prices_Ibovespa(dt_ini,dt_fim):
    return jsonify(empresa_bolsa.update_History_Values_Ibovespa(format_date_yyyymmaa(dt_ini),
                                                                format_date_yyyymmaa(dt_fim)))