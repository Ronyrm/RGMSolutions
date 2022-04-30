from App import db
from flask import request, jsonify
from App.model.localidades.mesoregiao import MesoRegiao

def get_mesoregiao(id):
    id = str(id)
    if id == '' or id == '0':
        mesoregioes = MesoRegiao.query.all()
        if mesoregioes:
            return mesoregioes
    else:
        from sqlalchemy import or_
        mesoregiao = MesoRegiao.query.filter(or_(MesoRegiao.id == id,MesoRegiao.nome.like('%'+id+'%'))).all()
        if mesoregiao:
            return mesoregiao

    return None

def get_by_uf_mesoregiao(iduf):
    iduf=str(iduf)
    from App.model.localidades.uf import UF
    from sqlalchemy import or_


    mesoregiao = MesoRegiao.query.join(UF,MesoRegiao.iduf==UF.id). \
                 filter(or_(MesoRegiao.iduf==iduf,UF.sigla==iduf,UF.nome.like('%'+iduf+'%'))).all()
    if mesoregiao:
        return mesoregiao
    return None

def get_by_regiao_mesoregiao(iduf):
    iduf=str(iduf)
    from App.model.localidades.uf import UF
    from App.model.localidades.regiao import Regiao
    from sqlalchemy import or_

    mesoregiao = MesoRegiao.query.join(UF, MesoRegiao.iduf == UF.id).\
        join(Regiao, UF.idregiao == Regiao.id).\
        filter(or_(Regiao.id == iduf,Regiao.sigla == iduf,Regiao.nome.like('%'+iduf+'%'))).all()
    if mesoregiao:
        return mesoregiao
    return None
