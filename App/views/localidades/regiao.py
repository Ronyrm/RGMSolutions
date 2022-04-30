from App.model.localidades.regiao import Regiao
from App.schema.localidades.localidades import RegiaoSchema
def get_regiao(idregiao):
    if idregiao == '' or idregiao == '0':
        regioes = Regiao.query.filter(Regiao.id != 0).all()
        if regioes:
            return regioes
    else:
        regiao = Regiao.query.filter(Regiao.id==idregiao).all()
        if regiao:
            return regiao

    return None
