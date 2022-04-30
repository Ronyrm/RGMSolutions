from App.model.bolsavalores.balancofinancas_bolsa import BalancoFinancas, SchemaBalancoFinancasBolsa
from App.model.bolsavalores.empresa_bolsa import EmpresaBolsa
from sqlalchemy import and_

def get_balancofinancas_json_by_papel(papel):
    filter_ = BalancoFinancas.idpapel==papel
    try:
        int(papel)
    except:
        filter_ = EmpresaBolsa.papel==papel

    balanco = BalancoFinancas.query.\
        join(EmpresaBolsa,BalancoFinancas.idpapel==EmpresaBolsa.id).\
        filter(filter_).all()
    if balanco:
        schema = SchemaBalancoFinancasBolsa()
        return {'data':schema.dump(balanco,many=True)}
    return {'data':{}}

def get_balancofinancas_by_papel_data(papel,dt):
    return BalancoFinancas.query.filter(and_(BalancoFinancas.idpapel==papel, BalancoFinancas.dt_apuracao==dt)).all()

def add_balancofinancas_bolsas(data):
    pass