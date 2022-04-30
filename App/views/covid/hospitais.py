from App import db
from flask import request
from App.model.covid.hospitais_covid import Hospitais,SchemaHospitais
from flask_paginate import get_page_args
from App.funcs.getpagination import get_pagination, preenche_pagination

def get_hospital(idhospital):
    return Hospitais.query.get(idhospital)

def get_hostital_by_name(name):
    return Hospitais.query.filter(Hospitais.name==name).all()

def get_hospitais_json():
    if request.method == 'GET':
        name = request.args.get("name") if request.args.get("name") != None else None
        filterhosp = Hospitais.id != -1 if name == None else Hospitais.name.like("%"+name+"%")
        hospitais = Hospitais.query.filter(filterhosp).order_by(Hospitais.id).all()
        if hospitais:
            schemahosp = SchemaHospitais()
            return {'data': schemahosp.dump(hospitais,many=True),
                    'result':True,
                    'mensagem': 'Sucesso'
                    }
    return {'data': {},
            'result': False,
            'mensagem': 'Erro'
            }


def add_hospital(name):
    try:
        data = request.form
        hospital = Hospitais()
        hospital.name = name
        db.session.add(hospital)
        db.session.commit()
        return hospital
    except:
        return None