import sqlalchemy

from App import db
from App.model.dieta import Dieta
from App.model.itemdieta import ItemDieta
from flask import jsonify, request
from App.model.refeicao import Refeicao
from App.schema.schema import DietaSchema
from App.schema.schema import ItemDietaSchema
import datetime


def post_dieta_json(idrefeicao):
    descricao = request.json['descricao']
    try:
        data = request.json['data']
    except:
        data = datetime.datetime.now().date()

    dietaexiste = getdietarefeicao_id_data(idrefeicao,data)
    if dietaexiste:
        refeicao = Refeicao.query.get(idrefeicao)
        ano = data[0:4]
        mes = data[5:7]
        dia = data[8:10]

        databr = dia+'/'+mes+'/'+ano
        dieta_schema = DietaSchema()
        result = dieta_schema.dump(dietaexiste)

        return jsonify({'message': 'Refeição: '+refeicao.descricao+
                        ' encontra-se já lançada para esta data: '+databr, 'data': result}), 201

    mesano = request.json['mesano']
    totalcarbo = request.json['totalcarbo']
    totalproteina = request.json['totalproteina']
    totalgordura = request.json['totalgordura']
    totalfibras = request.json['totalfibras']
    totalsodio = request.json['totalsodio']
    totalcalorias = request.json['totalcalorias']




    dieta = Dieta(descricao=descricao,data=data,mesano=mesano,totalcarbo=totalcarbo,
                  totalproteina=totalproteina,totalgordura=totalgordura, totalfibras=totalfibras,
                 totalsodio=totalsodio, totalcalorias=totalcalorias, idrefeicao=idrefeicao)
    db.session.add(dieta)
    db.session.commit()
    dieta_schema = DietaSchema()
    result = dieta_schema.dump(dieta)
    return jsonify({'message': 'successfully fetched', 'data': result}), 201

def getdietarefeicao_id_data(idrefeicao,data):
    from sqlalchemy import and_
    try:
        dieta = Dieta.query.filter(and_(Dieta.idrefeicao == idrefeicao, Dieta.data == data)).all()
        return dieta
    except:
        return None

def post_dieta():

    if request.method == 'POST':
        data = request.form
        idrefeicao = data['edtidrefeicao']
        idmetaatleta = data['edtidmetaatleta']
        mesano = data['edtmesano']
        totalcarbo = data['edttotalcarbo']
        totalproteina = data['edttotalproteina']
        totalgordura = data['edttotalgordura']
        totalfibras = data['edttotalfibras']
        totalsodio = data['edttotalsodio']
        totalcalorias = data['edttotalcalorias']

    return jsonify({'data':{}})

def getdietarefeicao(idrefeicao,data):
    try:
        dieta = getdietarefeicao_id_data(idrefeicao,data)
        totalreg = 0
        totalitens = 0
        if dieta:
            totalreg = len(dieta)
            dietaschema = DietaSchema()
            result = dietaschema.dump(dieta, many=True)
            dietatemp = result[0]
            iddieta = dietatemp['id']
            itemdieta = getitensdieta(iddieta)
            resultitem = {}

            if itemdieta:
                totalitens = len(itemdieta)
                itemdietaschema = ItemDietaSchema()
                resultitem = itemdietaschema.dump(itemdieta,many=True)

            return jsonify({'data': result, 'totreg': totalreg, 'dataitem': resultitem, 'totitens': totalitens})
        else:
            return jsonify({'data': {}, 'totreg': totalreg, 'dataitem': {}, 'totitens': totalitens})
    except:
        return None


def getitensdieta(iddieta):
    try:
       return ItemDieta.query.filter(ItemDieta.iddieta==iddieta).all()
    except:
        return None

def totalkcaldieta(idmeta,data):
    from sqlalchemy import and_
    from sqlalchemy.sql.expression import func, cast

    try:
        sumdieta = Dieta.query.filter(and_(Dieta.idmetaatleta==idmeta,Dieta.data==data)).\
            with_entities(cast(func.round(func.ifnull(func.sum(Dieta.totalcalorias),0)), sqlalchemy.Float).label('totalkcal'),
                          cast(func.round(func.ifnull(func.sum(Dieta.totalcarbo),0)), sqlalchemy.Float).label('totalcarbo'),
                          cast(func.round(func.ifnull(func.sum(Dieta.totalproteina),0)), sqlalchemy.Float).label('totalproteina'),
                          cast(func.round(func.ifnull(func.sum(Dieta.totalgordura),0)), sqlalchemy.Float).label('totalgordura'),
                          cast(func.round(func.ifnull(func.sum(Dieta.totalfibras),0)),sqlalchemy.Float).label('totalfibras'),
                          cast(func.round(func.ifnull(func.sum(Dieta.totalsodio),0)), sqlalchemy.Float).label('totalsodio')).first()


        resultjson = {'totalkcal':sumdieta[0],
                    'totalcarbo':sumdieta[1],
                    'totalproteina':sumdieta[2],
                    'totalgordura':sumdieta[3],
                    'totalfibras':sumdieta[4],
                    'totalsodio':sumdieta[5]}
        return resultjson
    except:
        return None