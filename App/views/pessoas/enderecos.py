from App.model.pessoas.enderecos import Enderecos
from flask import request
from sqlalchemy import and_,or_
from App import db
import re

# Busca endereco por pessoas
def get_enderecos_by_pessoa(idpessoa):
    try:
        enderecos = Enderecos.query.filter(Enderecos.idpessoa==idpessoa).all()
        if enderecos:
            return enderecos
    except:
        return None
    return None


# Busca endereco por idendereco
def get_endereco_by_id(id):
    try:
        endereco = Enderecos.query.filter(Enderecos.id==id).one()
        if endereco:
            return endereco
    except:
        return None
    return None


# Captura endereço por tipo e idpessoa
def get_endereco_by_pessoa_tipo(idpessoa,tipo):
    try:
        endereco = Enderecos.query.filter(and_(Enderecos.idpessoa==idpessoa,Enderecos.tipo==tipo)).all()
        if endereco:
            return endereco
    except:
        return None
    return None


# Insere ou Atualiza Endereço de uma determinada pessoal
def add_update_enderecos_by_pessoa():
    if request.method == 'POST':
        try:
            endereco = request.form

            idendereco = endereco["edtidendereco"]
            idpessoa = endereco["edtidpessoa"]
            idcidade = endereco["edtidcidade"]
            localidade = endereco['edtlocalidade']
            uf = endereco['edtsiglauf']
            logradouro = endereco["edtlogradouro"]
            numero = endereco["edtnumero"]
            bairro = endereco["edtbairro"]
            complemento = endereco["edtcomplemento"]

            cep = endereco["edtcep"]
            cep = re.sub('\D',"",cep)

            tipo = endereco["edttipo"]
            padrao = endereco["edtpadrao"]

            arraytipo = ["Comercial","Entrega","Cobrança","Residencial","Rural"]
            desctipo = arraytipo[int(tipo)]

            if idendereco == '-1':
                endereco = Enderecos(cep=cep, logradouro=logradouro, complemento=complemento,
                                     bairro=bairro,numero=numero,idpessoa=idpessoa,idcidade=idcidade,
                                     tipo=tipo, padrao=padrao,localidade=localidade,uf=uf)
                db.session.add(endereco)
            else:
                endereco = get_endereco_by_id(idendereco)
                #if endereco.tipo != tipo:
                #    endetemp = get_endereco_by_pessoa_tipo(idpessoa,tipo)
                #    if endetemp:
                #        return {'result': False,
                #                'idpessoa':idpessoa,
                #                'mensagem': 'Já Existe um endereço cadastrado como: '+desctipo}

                if endereco:
                    endereco.cep = cep,
                    endereco.logradouro = logradouro
                    endereco.complemento = complemento
                    endereco.bairro = bairro
                    endereco.numero = numero
                    endereco.idpessoa = idpessoa
                    endereco.idcidade = idcidade
                    endereco.padrao = padrao
                    endereco.tipo = tipo
                    endereco.localidade = localidade
                    endereco.uf = uf

            db.session.commit()
            if endereco.padrao=='S':
                update_endereco_main(endereco.id, endereco.idpessoa)
                db.session.commit();

            return {'result': True,
                    'idpessoa': idpessoa,
                    'mensagem': 'Endereço cadastrado com Sucesso'}
        except:
            return {'result': False,
                    'idpessoa': idpessoa,
                    'mensagem': 'Erro ao tentar cadastrar endereço. Tente Novamente mais tarde'}


# atualiza endereço principal
def update_endereco_main(idendereco,idpessoa):
    from sqlalchemy import update,and_
    db.session.query(Enderecos).\
        filter(and_(Enderecos.id!=idendereco,Enderecos.idpessoa==idpessoa)).\
        update({Enderecos.padrao:'N'},synchronize_session=False)


# Deleta endereço
def delete_endereco(id,idpessoa):
    try:
        db.session.query(Enderecos).filter(Enderecos.id==id).delete()
        db.session.commit()
        return {'result': True, 'mensagem': 'Endereço Excluído com Sucesso!','idpessoa':idpessoa}
    except:
        return {'result':False, 'mensagem':'Erro ao excluir endereço','idpessoa':idpessoa}
