import json
from flask import jsonify
from config import UPLOAD_FOLDER
import requests
#from IPython.core.display import display
from bs4 import BeautifulSoup
import  pandas as pd
from  pandas_datareader  import  data as web
import  matplotlib.pyplot as plt
import re
import datetime
from App import translator
# -------------------------- BUSCA DADOS TEMPERATURA POR LONGITUDE E LATITUDE --------------------------
def search_dados_temperatura_lat_lon(lat,lon,units):
    chavekey='078e25e1759b62d7d25ad0f48217d730'

    url = f'https://api.openweathermap.org/data/2.5/weather?units={units}&lat={lat}&lon={lon}&appid={chavekey}'
    print(url)
    req = requests.get(url)
    try:
        return req.json()
    except:
        return None

    #try:
    #    import pyowm
    #    owm = pyowm.OWM(chavekey)
    #    obs = owm.weather_at_place('Muriaé,BR')
    #    return obs.get_weather()
    #except:
    #    return None


# -------------------------- BUSCA DADOS TEMPERATURA POR LATITUDE E LONGITUDE --------------------------
def search_dados_temperatura_lat_log(lat,lon,units):
    chavekey = '078e25e1759b62d7d25ad0f48217d730'

    url = f'https://api.openweathermap.org/data/2.5/weather?units={units}&lat={lat}&lon={lon}&appid={chavekey}'
    print(url)
    req = requests.get(url)
    try:
        return req.json()
    except:
        return None


# -------------------------- BUSCA DADOS TEMPERATURA POR CIDADE,UF --------------------------
def search_dados_temperatura_city(city, units):
    chavekey = '078e25e1759b62d7d25ad0f48217d730'

    url = f'https://api.openweathermap.org/data/2.5/weather?units={units}&q={city}&appid={chavekey}'
    print(url)
    req = requests.get(url)
    try:
        return req.json()
    except:
        return None


# -------------------------- BUSCA DADOS LATITUDE E LONGITUDE GEOLOCATOR --------------------------
def search_latitude_longitude_geolocator(strcyte):
    from geopy import Nominatim
    geolocator = Nominatim(user_agent="sisnutri")
    try:
        result = geolocator.geocode(strcyte)
        return result
    except:
        return None


# -------------------------- RASTREIA OBJETO DOS CORREIOS VIA CODIGO = RETURN JSON --------------------------
def search_tracker_correios(codigo):
    from App.views.packagetrack import update_status_track
    req = requests.post('https://www2.correios.com.br/sistemas/rastreamento/ctrl/ctrlRastreamento.cfm?',
                        data={'objetos': codigo})

    soup = BeautifulSoup(req.text, 'html.parser')
    i = 0
    data = {}

    soupinfo = soup.find(attrs={"class": "info alert"})
    if soupinfo != None:
        text = re.sub('\n', " ", soupinfo.text)
        text = re.sub('\r', ' ', text)
        text = re.sub('\t', ' ', text)
        newdict = {0: text.strip()+' Ou código inválido!'}
        data.update(newdict)
        update_status_track(codigo, 'N')
        return {'data': data,'tot':1}

    for soupchildren in soup.find_all(attrs={"class": "listEvent sro"}):
        j = 1
        newdict = {i:{}}
        for td in soupchildren.find_all("td"):
            newdict[i].update({j:{}})

            text = re.sub('\n'," ",td.text)
            text = re.sub('\r',' ',text)
            text = re.sub('\t', ' ', text)

            text = re.sub('       ',' - ',text)
            text = re.sub('Clique aqui Minhas Importações',' ',text)
            text = re.sub('Informar nº do documento para a fiscalização e entrega do seu objeto',
                          '<br>Caso não informou o nº do documento <a target="_blank" href="https://www2.correios.com.br/sistemas/rastreamento/default.cfm?objetos='+codigo+'">Clique Aqui</a>',text)
            newdict[i][j] = text
            j+=1
        data.update(newdict)


        i+=1
    import json
    tot = len(data)

    if data[0][2].strip() == ' Objeto entregue ao destinatário  '.strip():
        update_status_track(codigo,'E')
    else:
        update_status_track(codigo, 'P')

    return {'data':data,'tot':tot}


# -------------------------- TRADUZ DETERMINADO TEXTO EM INGLES OU VICE-VERSA EM PORTUGUES = RETURN JSON --------------------------
def translate(txttranslate,src='',dest=''):
    if src == '' and dest == '':
        detect = translator.detect(txttranslate)

        if detect.lang=='en':
            dest = 'pt'
            src = 'en'
        else:
            dest = 'en'
            src = 'pt'


    translation = translator.translate(txttranslate,src=src,dest=dest)
    traducao = translation.text
    origin = translation.origin
    strjson = {
        'src':translation.src,
        'dest': translation.dest,
        'origin':origin,
        'traducao':traducao
        }
    return strjson


# -------------------------- BUSCA DADOS LOCALIDADE DE ACORDO COM O CEP INFORMADO = RETURN JSON --------------------------
def busca_dados_CEP(cep):
    ceporg = re.sub('[^a-zA-Z0-9 \n\.]', '', cep)
    req = requests.get('https://viacep.com.br/ws/'+ceporg+'/json/')
    if req.status_code==200:
        data = req.json()
    else:
        data = {'erro':True}
    return data


# ENviar SMS TWILIO -Continuação
def sendsms_twilio(msgsms,phone):
    from config import TWILIO_ACCOUNT_SID,TWILIO_AUTH_TOKEN
    from twilio.rest import Client

    account_sid = TWILIO_ACCOUNT_SID
    auth_token = TWILIO_AUTH_TOKEN
    client = Client(account_sid, auth_token)
    mensagem = client.messages.create(to=phone,
                                      from_='+5532984422783',
                                      body=msgsms)
    result = mensagem.sid()
    return  result


# -------------------------- BUSCA COTAÇÕES BOLSA DE VALORES --------------------------

def extract_html_in_text_source(url):
    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
  "X-Requested-With": "XMLHttpRequest"}
    source=requests.get(url, headers=headers).text
    return source


def search_cotacoes_bolsa_valores():
    url = 'https://www.fundamentus.com.br/resultado.php'

    # url = 'https://www.infomoney.com.br/cotacoes/ibovespa'
    #url = 'https://br.financas.yahoo.com/noticias/acoes-mais-negociadas?_device=desktop&device=desktop&failsafe=1&ynet=0&offset=0&count=1000'
    resp = extract_html_in_text_source(url)
    # soup = BeautifulSoup(req.text, 'html.parser')
    df = pd.read_html(resp, decimal=',', thousands='.', encoding="UTF-8")[0]
    resjson = df.to_json()

    for row in range(0, len(df.values)):
        item = df.values[row]
        print(item)
    return  json.loads(resjson)

def finance_cotacao(name):
    import os
    start = datetime.datetime(2021,9,1)
    end = datetime.datetime(2021,9,30)
    listname = name.split(',')
    df = web.DataReader(listname,data_source='yahoo',start=start,end=end)

    #display(df)
    #df['Adj Close'].plot(figsize=(15,10))

    spath = os.path.join(UPLOAD_FOLDER, f'grafic_{name}.png')
    if os.path.exists(spath):
        os.remove(spath)

    plt.savefig(spath)
    #generate_qrcode_myzap()
    resultjson = df.to_json()
    resultjson = json.loads(resultjson)
    return resultjson


def generate_qrcode_myzap():
    import qrcode
    data = 'https://api.whatsapp.com/send?phone=5532984422783'
    img = qrcode.make(data)
    img.save(UPLOAD_FOLDER+'qrcode_rony.png')
