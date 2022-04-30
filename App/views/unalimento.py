from App import db
from App.model.unalimento import Unalimento
from flask import jsonify, request
from App.schema.schema import UnFoodsSchema

def get_bydescricao():
    try:
        desc = request.args.get('descricao')
    except:
        desc = ''

    from sqlalchemy import or_
    try:
        unfoods = Unalimento.query.filter(or_(Unalimento.descricao == desc,Unalimento.id == desc)).one()
        return unfoods
    except:
        return None

def get_bydescricaojson():
    try:
        desc = request.args.get('desc')
        desc = "%" + desc + "%"
    except:
        desc = ''

    if desc == None or desc=='' :
        desc = "%%"

    from sqlalchemy import or_
    try:
        if desc != '':
            unfoods = Unalimento.query.filter(or_(Unalimento.descricao.like(desc),Unalimento.sigla.like(desc)))
        else:
            unfoods = Unalimento.query.all()

        unfoodsschema = UnFoodsSchema()
        result = unfoodsschema.dump(unfoods,many=True)

        return jsonify({'data': result})

    except:
        return jsonify({'data':{}})


def pagflipbook():
    return