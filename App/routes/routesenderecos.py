from flask import Blueprint,jsonify
from App.views.pessoas import enderecos
from App.schema.pessoas.pessoas import EnderecosSchema
routesenderecos = Blueprint('routesenderecos',__name__)

@routesenderecos.route('/get/enderecos/pessoa/<idpessoa>')
def get_endereco_pessoa(idpessoa):
    tabenderecos = enderecos.get_enderecos_by_pessoa(idpessoa)
    tot=0
    if tabenderecos:
        enderecosschema = EnderecosSchema()
        tot = len(tabenderecos)
        return jsonify({'data': enderecosschema.dump(tabenderecos,many=True),'tot':tot})

    return jsonify({'data':{},'tot':tot})


@routesenderecos.route('/post/endereco/pessoa',methods=['POST'])
def post_endereco_pessoa():
        return jsonify(enderecos.add_update_enderecos_by_pessoa())


@routesenderecos.route('/delete/endereco/<idendereco>/<idpessoa>')
def delete_endereco(idendereco,idpessoa):
        return jsonify(enderecos.delete_endereco(idendereco,idpessoa))
