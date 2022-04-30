from App.model.localidades.microregiao import MicroRegiao

def get_microregiao(id):
    id = str(id)
    if id == '' or id == '0':
        microregioes = MicroRegiao.query.all()
        if microregioes:
            return microregioes
    else:
        microregiao = MicroRegiao.query.filter(MicroRegiao.id==id).all()
        if microregiao:
            return microregiao

    return None

def get_by_uf_microregiao(iduf):
    iduf = str(iduf)
    from sqlalchemy import or_
    from App.model.localidades.uf import UF
    from App.model.localidades.mesoregiao import MesoRegiao

    microregioes = MicroRegiao.query. \
        join(MesoRegiao, MicroRegiao.idmesoregiao==MesoRegiao.id). \
        join(UF, MesoRegiao.iduf==UF.id). \
        filter(or_(UF.id==iduf,UF.sigla==iduf,UF.nome.like('%'+iduf+'%'))).all()

    if microregioes:
        return microregioes
    return None


def get_by_regiao_microregiao(idregiao):
    idregiao = str(idregiao)
    from sqlalchemy import or_
    from App.model.localidades.mesoregiao import MesoRegiao
    from App.model.localidades.uf import UF
    from App.model.localidades.regiao import Regiao
    microregioes = MicroRegiao.query. \
        join(MesoRegiao, MicroRegiao.idmesoregiao==MesoRegiao.id). \
        join(UF, MesoRegiao.iduf==UF.id). \
        join(Regiao,UF.idregiao==Regiao.id). \
        filter(or_(Regiao.id==idregiao,Regiao.sigla==idregiao,Regiao.nome==idregiao,Regiao.nome.like('%'+idregiao+'%'))).all()

    if microregioes:
        return microregioes
    return None
