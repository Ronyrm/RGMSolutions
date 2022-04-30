from App.model.bolsavalores.setor_bolsa import SchemaSetorBolsa, SetorBolsa
from App import db


def get_setor_by_name(name):
    return SetorBolsa.query.filter(SetorBolsa.name==name).all()


def get_all_setoresbolsa():
    setores = SetorBolsa.query.filter(SetorBolsa.id!=-1).all()
    schema = SchemaSetorBolsa()
    return {'data':schema.dump(setores,many=True)}



def add_setor(name):
    if not get_setor_by_name(name):
        setor = SetorBolsa()
        setor.name = name
        try:
            db.session.add(setor)
            db.session.commit()
            return {'data':{'id':setor.id,'name':setor.name},'result':True}
        except:
            pass

    return {'data': {}, 'return': False}