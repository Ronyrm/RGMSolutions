from flask import  Blueprint
from App.views import several,bot_twilio
from flask import  jsonify,request

routesseveral = Blueprint('routesseveral',__name__)

@routesseveral.route('/translate',methods=['GET'])
def translate():
    return several.translate()


@routesseveral.route('/bottwilio',methods=['POST'])
def bottwilio():
    resp = bot_twilio.bottwilio()
    return resp


@routesseveral.route('/get/cep/<cep>',methods=['GET'])
def soma(cep):
    return several.busca_dados_CEP(cep)


# SMS TWILIO - INCOMPLETO FALTA TESTE
@routesseveral.route('/sendsms/twilio',methods=['POST'])
def sendsms_twilio():
    if request.method == 'POST':
        data = request.form
        msgsms = data['msgsms']
        phone = data['phone']
        several.sendsms_twilio(msgsms,phone)


# BUSCA RASTREAMENTO CORREIOS
@routesseveral.route('/get/tracker/correios',methods=['POST'])
def trackercorreios():
    from App.views.several import search_tracker_correios
    if request.method == 'POST':
        data = request.form
        return jsonify(search_tracker_correios(data['codigo']))


# BUSCA DADOS CLIMATICOS ATRAVES DA LOCALIZAÇÃO: LATITUDE E LONGITUDE
@routesseveral.route('/get/clima/latlon/<lat>/<lon>')
def get_clima_by_lat_lon(lat,lon):
    units = 'metric'  # metric = Celsius, imperial = Fahrenheit, default = Kelvin
    return jsonify(several.search_dados_temperatura_lat_log(lat,lon,units))


# BUSCA DADOS CLIMATICOS ATRAVES DA LOCALIZAÇÃO: POR NOME CIDADE
@routesseveral.route('/get/clima/cidade/<city>')
def get_clima_by_cidade(city):
    units = 'metric'  # metric = Celsius, imperial = Fahrenheit, default = Kelvin
    return jsonify(several.search_dados_temperatura_city(city,units))


#BUSCA DADOS CLIMATICOS ATRAVES LATITUDE E LONGITUDE, BIBLIOTECA GEOLOCATOR-PYTHON
@routesseveral.route('/get/clima/geolocator/cidade/<city>')
def get_clima_by_cidade_geolocator(city):
    import json
    result = several.search_latitude_longitude_geolocator(city)
    result = result.raw
    result_json = json.dumps(result)
    return result

# TRADUZ TEXTO
@routesseveral.route('/post/translate',methods=['POST'])
def post_translate():
    if request.method == 'POST':
        data= request.form
        src,dest = '',''

        try:
            src = data['src'] if data['src'] != None else ''
        except:
            pass
        try:
            dest = data['dest'] if data['dest'] != None else ''
        except:
            pass
        cond = several.translate(data['texttranslate'],
                                 src,dest)

        return jsonify(cond)


# BUSCA COTAÇÃO BOLSA DE VALORES
@routesseveral.route('/get/cotacoes/bolsa')
def search_cotacoes_bolsa_valores():
    return jsonify(several.search_cotacoes_bolsa_valores())

# BUSCA COTAÇÃO BOLSA DE VALORES
@routesseveral.route('/get/finance/ibovespa/<name>')
def get_finance_ibovespa(name):
    return  jsonify(several.finance_cotacao(name))
