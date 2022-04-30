
import requests

from App.views.bolsavalores import prices_cotacao_history_bolsa
from flask import jsonify,Blueprint
from App.funcs.funcs import format_date_yyyymmaa
routespricescotacaobolsa = Blueprint('routespricescotacaobolsa',__name__)

@routespricescotacaobolsa.route('/get/prices/cotacao/history/<papel>/<dtini>/<dtfim>')
def get_prices_cotacao_by_papel_dates(papel,dtini,dtfim):
    return jsonify(prices_cotacao_history_bolsa.get_prices_cotacao_by_papel_dates(papel,
                                                                                  format_date_yyyymmaa(dtini),
                                                                                  format_date_yyyymmaa(dtfim)))

@routespricescotacaobolsa.route('/get/prices/cotacao/history/mensal/<papel>/<dtini>/<dtfim>')
def get_prices_cotacao_by_papel_dates_mensal(papel,dtini,dtfim):
    return jsonify(prices_cotacao_history_bolsa.get_prices_cotacao_by_papel_dates_mensal(papel,
                                                                                  format_date_yyyymmaa(dtini),
                                                                                  format_date_yyyymmaa(dtfim)))

@routespricescotacaobolsa.route('/get/prices/cotacao/history/ibovespa')
def get_prices_coatacao_ibovespa():
    return jsonify(prices_cotacao_history_bolsa.get_prices_cotacao_ibovespa())