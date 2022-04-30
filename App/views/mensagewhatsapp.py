from App import db
from App.model.mensagewhatsapp import MensageWhatsApp

def getmensagewhatsapp(idpessoa):
    try:
        return MensageWhatsApp.query.filter(MensageWhatsApp.idpessoa==idpessoa).one()
    except:
        return None

def getmensagewhatsapp_by_phone(phone):
    try:
        return MensageWhatsApp.query.filter(MensageWhatsApp.pergunta.like(phone)).one()
    except:
        return None

def getmensagewhatsapp_by_phone_idpessoa_null(phone):
    try:
        from sqlalchemy import  and_
        return MensageWhatsApp.query.filter(and_(MensageWhatsApp.pergunta.like(phone),
                                                 MensageWhatsApp.idpessoa.is_(None))).one()
    except:
        return None


def postmensagewhatsapp(arraymsg):
    mensagezap = getmensagewhatsapp(arraymsg.idpessoa)
    if mensagezap:
        mensagezap.pergunta = arraymsg.pergunta
        mensagezap.reposta = arraymsg.resposta
        mensagezap.proceed = arraymsg.proceed
        db.session.commit()
    else:
        mensagezap = MensageWhatsApp(pergunta=arraymsg.pergunta,proceed='S',
                                     resposta=arraymsg.resposta,idpessoa=arraymsg.idpessoa)
        db.session.add(mensagezap)
        db.session.commit()