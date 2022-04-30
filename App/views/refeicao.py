from App import db
from App.model.refeicao import Refeicao
from App.model.pessoas.pessoa import Pessoa
from App.model.atleta import Atleta
from App.model.cliente import Cliente
from flask import jsonify, request
from App.schema.schema import PessoaClienteRefeicoesSchema,RefeicaoSchema


def post_refeicao():
    if request.method == 'POST':
        data = request.form

        descricao = data['edtdescricao']
        hora = data['edthora']
        try:
            mostrar = data['edtmostrar']
            mostrar = 'S' if (mostrar == 'on') else 'N'
        except:
            mostrar = 'N'

        idpessoa = data['edtidpessoa']
        idrefeicao = data['edtidrefeicao']

        pessoa = Pessoa.query.get(idpessoa)
        if not pessoa:
            return jsonify({'mensagem': 'Cliente não encontrado na base de dados!', 'data': {}, 'result': False}), 201

        if idrefeicao == '-1':
            existrefeicao = get_bydescricao(descricao, idpessoa)
            if existrefeicao:
                return jsonify({'mensagem': 'A Refeição '+descricao+' ja existe para o usuário '+pessoa.nome,
                                'data': {},'result':False}), 201
            existrefeicao = get_byhora(hora,idpessoa)
            if existrefeicao:
                return jsonify({'mensagem': 'Já existe uma refeição cadastrada('+existrefeicao.descricao+') nesse horário: '+hora ,
                                'data': {},'result': False}), 201

            refeicao = Refeicao(descricao=descricao, hora=hora, mostrar=mostrar, idpessoa=idpessoa)
            db.session.add(refeicao)

        else:
            refeicao = Refeicao.query.get(idrefeicao)
            if refeicao:
                if refeicao.descricao.upper() != descricao.upper():
                    existrefeicao = get_bydescricao(descricao, idpessoa)
                    if existrefeicao:
                        return jsonify({'mensagem': 'A Refeição ' + descricao + ' ja existe para o usuário ' + pessoa.nome,
                                        'data': {}, 'result': False}), 201
                cphora = str(refeicao.hora)
                if cphora[0:5] != hora[0:5]:
                    existrefeicao = get_byhora(hora, idpessoa)
                    if existrefeicao:
                        return jsonify({'mensagem': 'Já existe uma refeição cadastrada(' + existrefeicao.descricao + ') nesse horário: ' + hora,
                                        'data': {}, 'result': False}), 201

                refeicao.descricao = descricao
                refeicao.hora = hora
                refeicao.mostrar = mostrar
        try:
            db.session.commit()
            refeicaoschema = RefeicaoSchema()
            refeicoes = get_refeicao_byidpessoa(idpessoa)
            result = refeicaoschema.dump(refeicoes,many=True)
            return jsonify({'mensagem': 'Refeição '+ 'cadastrada' if idrefeicao == "-1" else 'alterada'+' com sucesso!' , 'data': result,'result':True}), 201
        except:
            return jsonify({'mensagem': 'Erro ao Gravar a Refeição ' + descricao, 'data': {}, 'result': False}), 201

def get_bydescricao(descricao,idpessoa):
    from sqlalchemy import and_
    try:
        refeicao = Refeicao.query.filter(and_(Refeicao.descricao == descricao,Refeicao.idpessoa == idpessoa)).one()
        return refeicao
    except:
        return None


def get_byhora(hora,idpessoa):
    from sqlalchemy import and_
    try:
        refeicao = Refeicao.query.filter(and_(Refeicao.hora == hora,Refeicao.idpessoa == idpessoa)).one()
        return refeicao
    except:
        return None


def get_refeicao_byidpessoa(idpessoa):
    if idpessoa != '' and idpessoa != '0':
        refeicao = Refeicao.query.filter(Refeicao.idpessoa == idpessoa).\
                   order_by(Refeicao.hora.asc()).all()
        if refeicao:
            return refeicao

    return None


def get_refeicao_cliente(idcliente):

    cliente = Cliente.query.get(idcliente)
    clienterefshema = PessoaClienteRefeicoesSchema()
    resultcliente = clienterefshema.dump(cliente)

    return jsonify({'data': resultcliente})
    #result = db.session.query(Pessoa.nome,Cliente.cpf, Refeicao.descricao,Refeicao.hora,Refeicao.mostrar). \
    #join(Refeicao). \
    #join(Cliente). \
    #filter(Pessoa.id == idpessoa).all()

    #import simplejson
    #data = simplejson.dumps(result, default=formatdatetime_parser,ensure_ascii=False).encode('utf8')
    #return data


def get_refeicao_atleta():
    if request.method == 'GET':
        idatleta = request.args.get('idatleta')
        atleta = Atleta.query.filter(Atleta.id==idatleta).one()
        if atleta:
            refeicao =  get_refeicao_byidpessoa(atleta.idpessoa)
            if refeicao:

                refschema = RefeicaoSchema()
                result = refschema.dump(refeicao,many=True)
                return jsonify({'data': result,'result':True,'total':len(refeicao)})
    return jsonify({'data': {},'result':False})

def get_refeicao_id(id):
    try:
        return  Refeicao.query.get(id)
    except:
        return None
def delete_refeicao(id):
    refeicao = Refeicao.query.get(id)
    try:
        db.session.delete(refeicao)
        db.session.commit()
        refeicoes = get_refeicao_byidpessoa(refeicao.idpessoa)
        if refeicoes != None :
            totalreg = len(refeicoes)
            return jsonify( {'total': totalreg,'mensagem': 'Refeicao ' + refeicao.descricao + ' excluida com sucesso!', 'data': {}, 'result': True}), 201
        else:
            return jsonify( {'total': 0,'mensagem': 'Refeicao ' + refeicao.descricao + ' excluida com sucesso!', 'data': {}, 'result': True}), 201
    except:
        return jsonify({'mensagem': 'Houve um erro ao Excluir a Refeição '+ refeicao.descricao,
                        'data': {}, 'result': False}), 201