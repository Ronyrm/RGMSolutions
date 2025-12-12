from App import db
from App.model.atleta import Atleta
from App.model.metaatleta import Metaatleta
from App.schema.schema import MetaAtletaschema
from flask import jsonify, request,render_template,redirect,url_for
from datetime import datetime, timedelta


def get_metaatleta(idatleta,status):
    if idatleta != '' and idatleta != '0':
        from sqlalchemy import and_
        metaatleta = Metaatleta.query.filter(and_(Metaatleta.idatleta==idatleta,Metaatleta.status==status)).\
                   order_by(Metaatleta.create_on.asc(),Metaatleta.status.asc()).all()
        if metaatleta:
            metaschema = MetaAtletaschema()
            return metaatleta

    return None


def get_metaatleta_porpessoa(idpessoa,status):
    if idpessoa != '' and idpessoa != '0':
        from sqlalchemy import and_
        metaatleta = Metaatleta.query.\
                    join(Atleta,Metaatleta.idatleta==Atleta.id).\
                    filter(and_(Atleta.idpessoa==idpessoa,Metaatleta.status==status)).\
                   order_by(Metaatleta.create_on.asc(),Metaatleta.status.asc()).all()
        if metaatleta:
            metaschema = MetaAtletaschema()
            return jsonify({'mensagem': 'Metas encontradas',
                            'data': metaschema.dump(metaatleta,many=True),
                            'result': False}), 201

    return jsonify({'mensagem': 'Nenhuma Meta Cadastrada para esse atleta', 'data': {},
                 'result': False}), 201


def postmetaatleta():
    if request.method == 'POST':
        data = request.form

        pesoinicial = data['edtpesoinicialmetaatleta']
        idatleta = data['edtidatleta']
        valalvocalorico = data['edtkcalalvo']
        valtmb = data['edttmb']
        valgcd = data['edtgcd']
        frmharrisbenedictoriginal = data['edtfrmharrisoriginal']
        frmharrisbenedictrevisada = data['edtfrmharrisrevisada']
        frmmifflin = data['edtfrmmiffin']
        frmkatch = data['edtfrmkatch']
        pesofinal = data['edtpesofinalmetaatleta']
        percentual_gordura = data['edtpercfatinicialmetaatleta']
        tipometa = data['edtobjetivometa']
        valtotkclmeta = data['edtkcalmetaatleta']
        valtotkclexercicio = data['edtkcalexercatleta']
        nivelatividade = data['edtnameta']
        #Divisao Macro - Proteina
        percproteina = data['edtpercproteina']
        valkcalproteina = data['edtkcalproteina']
        valgramasproteina = data['edtgramasproteina']
        valgrkgproteina = data['edtgrporkgproteina']
        # Divisao Macro - Carboidrato
        perccarb = data['edtperccarbo']
        valkcalcarb = data['edtkcalcarbo']
        valgramascarbo = data['edtgramascarbo']
        valgrkgcarbo = data['edtgrporkgcarbo']
        # Divisao Macro - GOrdura
        percfat = data['edtpercgordura']
        valkcalfat = data['edtkcalgordura']
        valgramasgordura = data['edtgramasgordura']
        valgrkggordura = data['edtgrporkggordura']
        totaldiasprevisto = data['edtdiasprevisto']

        datenow = datetime.now()
        dia = datenow.day
        mes = datenow.month
        ano = datenow.year
        descricao = 'Meta Iniciada:'+str(dia)+'/'+str(mes)+'/'+str(ano)
        dataprevisaofinal = datetime.now() + timedelta(days=int(totaldiasprevisto))


        metaatleta = Metaatleta(pesoinicial=pesoinicial, idatleta=idatleta, valalvocalorico=valalvocalorico, valtmb=valtmb,
                                valgcd=valgcd, frmharrisbenedictoriginal=frmharrisbenedictoriginal, frmharrisbenedictrevisada=frmharrisbenedictrevisada,
                                frmmifflin=frmmifflin, frmkatch=frmkatch, pesofinal=pesofinal, percentual_gordura=percentual_gordura,
                                tipometa=tipometa, valtotkclmeta=valtotkclmeta, valtotkclexercicio=valtotkclexercicio, nivelatividade=nivelatividade,
                                percproteina=percproteina, valkcalproteina=valkcalproteina, valgramasproteina=valgramasproteina, valgrkgproteina=valgrkgproteina,
                                perccarb=perccarb, valkcalcarb = valkcalcarb, valgramascarbo=valgramascarbo, valgrkgcarbo=valgrkgcarbo,
                                percfat=percfat, valkcalfat=valkcalfat, valgramasgordura=valgramasgordura, valgrkggordura=valgrkggordura,
                                descricao=descricao,status='A',totaldiasprevisto=totaldiasprevisto,dataprevisaofinal=dataprevisaofinal)
        try:
            db.session.add(metaatleta)
            db.session.commit()
            metaschema = MetaAtletaschema()
            return jsonify({'mensagem': 'Sua Meta foi Iniciada com Sucesso!',
                     'data': metaschema.dump(metaatleta), 'result': True}), 201
        except:
            return jsonify({'mensagem': 'Erro ao tentar gravar Meta no servidor. Tente novamente mais tarde!', 'data': {}, 'result': False}), 201



    return jsonify({'mensagem': 'Erro ao tentar gravar Meta no servidor. Tente novamente mais tarde!', 'data': {}, 'result': False}), 201

def count_metaatleta():

    from sqlalchemy import func
    idatleta = request.args.get('idatleta')
    countmeta = Metaatleta.query.filter(Metaatleta.idatleta==idatleta).count()
    return jsonify({'count':countmeta})


def finalizameta():
    if request.method == 'POST':
        data = request.form
        idmeta = data['edtidmetaatleta']
        pesofinal = data['edtpesofinal']
        meta = Metaatleta.query.get(idmeta)
        if meta:
            try:

                meta.status = 'F'
                meta.datafinalizada = datetime.now()
                meta.pesofinalizado = pesofinal
                db.session.commit()

                return jsonify({'result':True,'mensagem':'Meta finalizada com sucesso!'})
            except:
                return jsonify({'result': False, 'mensagem':'Erro ao finalizar a meta, tente novamente!'})

    return jsonify({'result': False, 'mensagem': 'Erro ao finalizar a meta, tente novamente!'})