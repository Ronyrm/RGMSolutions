import numpy

from App.model.bolsavalores.balancopatrimonial_bolsa import BalancoPatrimonial,SchemaBalancoPatrimonialBolsa
from App.model.bolsavalores.empresa_bolsa import EmpresaBolsa
from App import db
from sqlalchemy.sql import and_


def get_balanco_patrimonial_by_papeldata(papel,data):
    try:
        papel = int(papel)
        filter_ = BalancoPatrimonial.idpapel == papel
    except:
        filter_ = EmpresaBolsa.papel == papel

    return BalancoPatrimonial.query.\
        filter(and_(filter_,BalancoPatrimonial.dt_apuracao == data)).first()


def get_balanco_patrimonial_by_papeldata_json(papel,data):
    try:
        papel = int(papel)
        filter_ = BalancoPatrimonial.idpapel == papel
    except:
        filter_ = EmpresaBolsa.papel == papel

    getbalanco = BalancoPatrimonial.query.\
        filter(and_(filter_,BalancoPatrimonial.dt_apuracao == data)).first()
    if getbalanco:
        schema = SchemaBalancoPatrimonialBolsa()
        return {'data':schema.dump(getbalanco,many=True)}
    return {'data': {}}

def get_balancopatrimonial_all_by_papel_json(papel):
    try:
        papel = int(papel)
        filter_ = BalancoPatrimonial.idpapel == papel
    except:
        filter_ = EmpresaBolsa.papel == papel

    balanco = BalancoPatrimonial.query.\
        join(EmpresaBolsa,BalancoPatrimonial.idpapel == EmpresaBolsa.id).\
        filter(filter_).all()
    if balanco:
        schema = SchemaBalancoPatrimonialBolsa()
        return {'data':schema.dump(balanco,many=True)}
    return {'data':{}}


def get_balanco_mais_recente(idpapel):
    maxreg = BalancoPatrimonial.query.\
        filter(BalancoPatrimonial.idpapel==idpapel).\
        order_by(BalancoPatrimonial.dt_apuracao.desc()).limit(1).all()
    return maxreg if maxreg else None

def add_balanco_patrimonial(data):

    balanco = get_balanco_patrimonial_by_papeldata(data['idpapel'],data['dt_apuracao'])
    add = False
    if not balanco:
        add = True
        balanco = BalancoPatrimonial()
    try:
        for key in data:
            #valor = data[key]
            #if isinstance(valor,numpy.float64):
            #    valor = int(data[key])
            setattr(balanco,key,data[key])

        if add:
            db.session.add(balanco)
        db.session.commit()
        return True
    except:
        pass

    return False
