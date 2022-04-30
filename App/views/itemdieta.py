from App import db
from App.model.itemdieta import ItemDieta
from App.model.dieta import Dieta
from flask import jsonify, request
from App.views.refeicao import get_refeicao_id
from App.views.alimentos import get_alimento_byid
from App.views.dieta import getdietarefeicao_id_data
from App.schema.schema import ItemDietaSchema
from App.funcs.funcalimentos import calcmacronutriente
import datetime


def post_itemdieta_form():
    if request.method == 'POST':
        data = request.form

        idalimento = data['edtidalimento']
        idmetaatleta = data['edtidmetaatleta']
        descalimento = data['edtdescfood']
        qtdgramas = data['edtqtd']
        idrefeicao = data['edtidrefeicao']
        dataatual = data['edtdataatual']
        totalcarbo = data['edtvalcarbo']
        totalproteina = data['edtvalproteina']
        totalgordura = data['edtvalfat']
        totalsodio = data['edtvalsodio']
        totalfibras = data['edtvalfibras']
        totalcalorias = data['edtvalkcal']
        iditem = data['edtiditem']

        #busca nome da refeição
        refeicao = get_refeicao_id(idrefeicao)
        descrefeicao = ''
        if refeicao:
            descrefeicao = refeicao.descricao

        # verifica se diario dieta existe no data corrente
        dieta = getdietarefeicao_id_data(idrefeicao,dataatual)
        iddieta = '-1'
        if dieta:
            iddieta = dieta[0].id
        else:
            try:
                dieta = Dieta(descricao='Diário Refeição:'+descrefeicao+', data:'+dataatual, data=dataatual, mesano='', totalcarbo=0,
                          totalproteina=0, totalgordura=0, totalfibras=0,
                          totalsodio=0, totalcalorias=0, idrefeicao=idrefeicao,idmetaatleta=idmetaatleta)
                db.session.add(dieta)
                db.session.commit()
                iddieta = dieta.id
            except:
                return jsonify({'mensagem': 'Erro ao gravar Diário da refeição:'+descrefeicao+' na data: '+dataatual,
                                'result':False}), 201
        # GRAVA ITEM REFEICAO
        if iditem == '-1' or iditem == '':
            try:
                itemdieta = ItemDieta(totalcarbo=totalcarbo, totalproteina=totalproteina,
                                      totalgordura=totalgordura, totalsodio=totalsodio,
                                      totalfibras=totalfibras, iddieta=iddieta, idalimento=idalimento,
                                      quantgramas=qtdgramas, totalcalorias=totalcalorias)
                db.session.add(itemdieta)
                db.session.commit()

                msg = 'Alimento ' + descalimento + ' gravado com sucesso na refeição: ' +descrefeicao+ ' na da data:' + dataatual
                return jsonify({'mensagem': msg , 'result': True}), 201
            except:
                return jsonify(
                    {'mensagem': 'Erro ao gravar Diário da refeição:' + descrefeicao +
                                 ' na data: ' + dataatual, 'result': False}), 201


def getitemdieta(iddieta):
    from sqlalchemy import and_
    try:
        itemdieta = ItemDieta.query.filter(ItemDieta.iddieta==iddieta).one()
        return itemdieta
    except:
        return None


def deleteitemdieta():

    id = request.args.get('id')
    descfood = request.args.get('descfood')
    descref = request.args.get('descrefeicao')

    itemdieta = ItemDieta.query.get(id)
    try:
        db.session.delete(itemdieta)
        db.session.commit()
        return jsonify({'mensagem': 'Item: '+ descfood+' excluído da refeição: '+descref+' com sucesso!',
                        'result': True})
    except:
        return jsonify({'mensagem':'Erro ao tentar excluir','result': False})
