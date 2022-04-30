from App import db
from flask import Blueprint,jsonify
import requests

from App.model.localidades.mesoregiao import MesoRegiao

routesIBGE = Blueprint('routesIBGE',__name__)


#Adiciona Região 1 passo
@routesIBGE.route('/search/ibge/add/regiao')
def addregiao_ibge():
    from App.views.localidades import regiao
    from App.model.localidades.regiao import Regiao

    url = 'https://servicodados.ibge.gov.br/api/v1/localidades/regioes'
    response = requests.get(url)
    regioes_json = response.json()
    for regiaojson in regioes_json:
        reg = regiao.get_regiao(regiaojson["id"])
        if not reg:
            newregiao = Regiao(id=regiaojson["id"],nome=regiaojson["nome"],sigla=regiaojson["sigla"])
            db.session.add(newregiao)
            db.session.commit()

    return jsonify(regioes_json)

#Adiciona UF 2 passo
@routesIBGE.route('/search/ibge/add/uf')
def adduf_ibge():
    from App.views.localidades import uf
    from App.model.localidades.uf import UF

    url = 'https://servicodados.ibge.gov.br/api/v1/localidades/estados'
    response = requests.get(url)
    ufs_json = response.json()
    for ufjson in ufs_json:
        reg = uf.get_uf(ufjson["id"])
        if not reg:
            newuf = UF(id=ufjson["id"],nome=ufjson["nome"],sigla=ufjson["sigla"],idregiao=ufjson["regiao"]["id"])
            db.session.add(newuf)
            db.session.commit()

    return jsonify(ufs_json)

#Adiciona MesoRegioes 3 passo
@routesIBGE.route('/search/ibge/add/mesoregioes')
def addmesoregiao_ibge():
    from App.views.localidades import mesoregiao
    from App.model.localidades.mesoregiao import MesoRegiao

    url = 'https://servicodados.ibge.gov.br/api/v1/localidades/mesorregioes'
    response = requests.get(url)
    mesoregioes_json = response.json()
    for mesoregiaojson in mesoregioes_json:
        reg = mesoregiao.get_mesoregiao(mesoregiaojson["id"])
        if not reg:
            newmesoregiao = MesoRegiao(id=mesoregiaojson["id"],nome=mesoregiaojson["nome"],iduf=mesoregiaojson["UF"]["id"])
            db.session.add(newmesoregiao)
            db.session.commit()

    return jsonify(mesoregioes_json)


#Adiona MicroRegião passo 4
@routesIBGE.route('/search/ibge/add/microregiao')
def addmicroregiao_ibge():
    from App.views.localidades import microregiao
    from App.model.localidades.microregiao import MicroRegiao

    url = 'https://servicodados.ibge.gov.br/api/v1/localidades/microrregioes'
    response = requests.get(url)
    microregioes_json = response.json()
    for microregiaojson in microregioes_json:
        reg = microregiao.get_microregiao(microregiaojson["id"])
        if not reg:
            newmicroregiao = MicroRegiao(id=microregiaojson["id"],nome=microregiaojson["nome"],
                                       idmesoregiao=microregiaojson["mesorregiao"]["id"])
            db.session.add(newmicroregiao)
            db.session.commit()

    return jsonify(microregioes_json)

#Aciona Cidade passo 5
@routesIBGE.route('/search/ibge/add/cidades')
def addcidades_ibge():
    from App.views.localidades import cidades
    from App.model.localidades.cidades import Cidades

    url = 'https://servicodados.ibge.gov.br/api/v1/localidades/municipios'
    response = requests.get(url)
    cidades_json = response.json()
    for cidade_json in cidades_json:
        reg = cidades.get_cidade(cidade_json["id"])
        if not reg:
            newmcidade = Cidades(id=cidade_json["id"],nome=cidade_json["nome"],
                                 idmicroregiao=cidade_json["microrregiao"]["id"],
                                 iduf=cidade_json["microrregiao"]["mesorregiao"]["UF"]["id"])
            db.session.add(newmcidade)
            db.session.commit()

    return jsonify(cidades_json)