from App.model.bolsavalores.subsetor_bolsa import SchemaSubSetorBolsa,SubSetorBolsa
from App import db
def get_subsetor_by_name(name):
    return SubSetorBolsa.query.filter(SubSetorBolsa.name==name).all()

def add_subsetor(name):
    if not get_subsetor_by_name(name):
        subsetor = SubSetorBolsa()
        subsetor.name = name
        try:
            db.session.add(subsetor)
            db.session.commit()
            return {'data':{'id':subsetor.id,'name':subsetor.name},'result':True}
        except:
            pass

    return {'data': {}, 'return': False}


def get_all_subsetoresbolsa():
    subsetores = SubSetorBolsa.query.filter(SubSetorBolsa.id!=-1).all()
    schema = SchemaSubSetorBolsa()
    return {'data':schema.dump(subsetores,many=True)}
