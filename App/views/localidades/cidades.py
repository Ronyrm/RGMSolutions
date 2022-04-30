from App.model.localidades.cidades import Cidades
from App.model.localidades.mesoregiao import MesoRegiao
from App.model.localidades.microregiao import MicroRegiao
from App.model.localidades.uf import UF
from App.model.localidades.regiao import Regiao
from sqlalchemy import or_,and_,asc


def get_cidade(id):
    id = str(id)
    if id == '' or id == '0':
        cidades = Cidades.query.all()
        if cidades:
            return cidades
    else:

        cidade = Cidades.query.filter(or_(Cidades.id==id,Cidades.nome.like('%'+id+'%'))).all()
        if cidade:
            return cidade

    return None


def get_cidade_by_uf(iduf,nomecity):
    iduf = str(iduf)
    try:
        city = Cidades.query.\
            join(UF,Cidades.iduf == UF.id).\
            filter(or_(UF.id == iduf, UF.nome.like('%' + iduf + '%'),UF.sigla == iduf)).\
            filter(and_(Cidades.nome.like('%'+nomecity+'%'))).\
            order_by(asc(Cidades.nome)).all()
        if city:
            return city
    except:
        return None


def get_cidade_by_uf_and_city(iduf,nomecity):
    iduf = str(iduf)
    try:
        city = Cidades.query.\
            join(UF,Cidades.iduf == UF.id).\
            filter(and_(UF.sigla == iduf,Cidades.nome==nomecity)).one()
        if city:
            return city
    except:
        return None
