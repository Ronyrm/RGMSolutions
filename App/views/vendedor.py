from App import db
from App.model.pessoas.pessoa import Pessoa
from App.model.vendedor import Vendedor
from App.views.pessoas.pessoas import get_byusernamepessoa, get_byemailpessoa
from App.views.users import get_user_by_username
from flask import jsonify, request,render_template,current_app
from werkzeug.security import generate_password_hash
from App.schema.schema import VendedorSchema,UsersSchema


def add_vendedor(current_user, token,page,totporpag):

    if request.method == 'POST':
        data = request.form
        try:
            rg = data['edtrg']
        except:
            rg = ''
        try:
            titulo = data['edttitulo']
        except:
            titulo = ''

        try:
            cpfcnppj = data['edtcpfcnpj']
        except:
            cpfcnppj = ''
        try:
            orgaoemissor = data['edtorgaoemissor']
        except:
            orgaoemissor=''
        try:
            username = data['edtusername']
        except:
            username=''
        try:
            nome = data['edtnome']
        except:
            nome = ''
        try:
            email = data['edtemail']
        except:
            email = ''
        try:
            password = data['edtpassword']
        except:
            password = ''
        try:
            comissao = data['edtcomissao']
        except:
            comissao = 0
        try:
            razaosocial = data['edtrazaosocial']
        except:
            razaosocial = ''


    pessoa = get_byusernamepessoa(username)
    idpessoa  = 0
    if pessoa:
        idpessoa = pessoa.id
        vendedor = Vendedor.query.filter(Vendedor.idpessoa==idpessoa).one();
        msg = 'Vendedor já encontra-se cadastrado na base de dados com username fornecido'+ \
              ' para o vendedor ' + str(vendedor.id) + ' - ' + pessoa.nome + '!';
        return jsonify({'mensagem': msg,'result': False}), 201

    pessoa = get_byemailpessoa(email,'VE')
    idpessoa = 0
    if pessoa:
        idpessoa = pessoa.id
        vendedor = Vendedor.query.filter(Vendedor.idpessoa == idpessoa).one();
        msg = 'Vendedor já encontra-se cadastrado na base de dados com email fornecido' + \
              ' para o vendedor ' + str(vendedor.id) + ' - ' + pessoa.nome + '!';
        return jsonify({'mensagem': msg, 'result': False}), 201

    verificavendedor = get_bycpf(cpfcnppj)
    if verificavendedor:
        vendedorschema = VendedorSchema()
        result = vendedorschema.dump(verificavendedor)
        return jsonify({'mensagem': 'Vendedor já encontra-se cadastrado na base de dados com o cpf informado!','result':False,
                        'data': result}), 201

    pass_hash = generate_password_hash(password)
    nomepessoa = ''
    if idpessoa == 0:
        pessoa_add = Pessoa(username=username,nome=nome, razaosocial='',tipopessoa='VE',
                            password=pass_hash,email=email)
        db.session.add(pessoa_add)
        db.session.commit()
        idpessoa = pessoa_add.id
        nomepessoa = pessoa_add.nome
    else:
        pessoa.nome = nome
        nomepessoa = nome
        pessoa.username = username
        pessoa.razaosocial = razaosocial
        pessoa.password = pass_hash
        pessoa.email = email
        db.session.commit()

    vendedor_add = Vendedor(rg=rg,titulo=titulo,orgaoemissor=orgaoemissor,cpfcnpj=cpfcnppj,comissao = comissao, idpessoa=idpessoa)
    db.session.add(vendedor_add)
    db.session.commit()
    vendedorschema = VendedorSchema()
    result = vendedorschema.dump(vendedor_add)
    try:
        return jsonify({'mensagem': 'Vendedor '+ nomepessoa + ' cadastrado com sucesso!', 'data': result, 'result':True}), 201
    except:
        return jsonify({'mensagem': 'Error ao tentar cadastrar o vendedor', 'data': {}, 'result': False}), 201


def edit_vendedor(current_user, token,page,totporpag):

    if request.method == 'POST':
        data = request.form
        try:
            rg = data['edtrg']
        except:
            rg = ''
        try:
            titulo = data['edttitulo']
        except:
            titulo = ''

        try:
            cpfcnppj = data['edtcpfcnpj']
        except:
            cpfcnppj = ''
        try:
            orgaoemissor = data['edtorgaoemissor']
        except:
            orgaoemissor=''
        try:
            username = data['edtusername']
        except:
            username=''
        try:
            nome = data['edtnome']
        except:
            nome = ''
        try:
            email = data['edtemail']
        except:
            email = ''
        try:
            password = data['edtpassword']
        except:
            password = ''
        try:
            comissao = data['edtcomissao']
        except:
            comissao = 0
        try:
            razaosocial = data['edtrazaosocial']
        except:
            razaosocial = ''

        vendedor = Vendedor.query.get(data['edtid'])
        pessoa = Pessoa.query.get(vendedor.idpessoa)

        if username != pessoa.username:
            pessoatemp = get_byusernamepessoa(username)
            idpessoa  = 0
            if pessoatemp:
                vendedor = Vendedor.query.filter(Vendedor.idpessoa==pessoatemp.id).one();
                msg = 'Vendedor já encontra-se cadastrado na base de dados com username fornecido'+ \
                      ' para o vendedor ' + str(vendedor.id) + ' - ' + pessoatemp.nome + '!';
                return jsonify({'mensagem': msg,'result': False}), 201

        if email != pessoa.email:
            pessoatemp = get_byemailpessoa(email,'VE')
            if pessoatemp:
                vendedor = Vendedor.query.filter(Vendedor.idpessoa==pessoatemp).one();
                msg = 'Vendedor já encontra-se cadastrado na base de dados com email fornecido'+ \
                      ' para o vendedor ' + str(vendedor.id) + ' - ' + pessoa.nome + '!';
                return jsonify({'mensagem': msg,'result': False}), 201

        if cpfcnppj != vendedor.cpfcnpj:
            verificavendedor = get_bycpf(cpfcnppj)
            if verificavendedor:
                vendedorschema = VendedorSchema()
                result = vendedorschema.dump(verificavendedor)
                return jsonify({'mensagem': 'Vendedor já encontra-se cadastrado na base de dados com o cpf informado!','result':False,
                              'data': result}), 201

        pass_hash = generate_password_hash(password)

        pessoa.nome = nome
        nomepessoa = nome
        pessoa.username = username
        pessoa.razaosocial = razaosocial
        pessoa.password = pass_hash
        pessoa.email = email
        db.session.commit()

        vendedor.rg = rg
        vendedor.titulo = titulo
        vendedor.orgaoemissor = orgaoemissor
        vendedor.cpfcnpj = cpfcnppj
        vendedor.comissao = comissao
        db.session.commit()

        vendedorschema = VendedorSchema()
        result = vendedorschema.dump(vendedor)
        try:
            return jsonify({'mensagem': 'Vendedor '+ nomepessoa + ' alterado com sucesso!', 'data': result, 'result':True}), 201
        except:
            return jsonify({'mensagem': 'Error ao tentar cadastrar o vendedor', 'data': {}, 'result': False}), 201


def get_byid(idvendedor):
    vendedor = Vendedor.query.get(idvendedor)
    vendedorschema = VendedorSchema()
    result = vendedorschema.dump(vendedor)
    return jsonify({'data': result})


def get_allvendedores(current_user,token,page,totporpag,orderby):

    try:
        nome = request.args.get('nome')
        nome = "%" + nome + "%"
    except:
        nome = ''

    if not nome:
        nome = ''

    from sqlalchemy import desc,asc
    if nome != '':
        from sqlalchemy import or_
        if orderby == '0':
            pagination = Vendedor.query. \
                join(Pessoa,Vendedor.idpessoa==Pessoa.id). \
                filter(or_(Pessoa.nome.like(nome),Pessoa.username.like(nome))). \
                order_by(desc(Vendedor.id)). \
                paginate(page=int(page),max_per_page=int(totporpag), error_out=False)

        if orderby == '1':
            pagination = Vendedor.query. \
                join(Pessoa,Vendedor.idpessoa==Pessoa.id). \
                filter(or_(Pessoa.nome.like(nome),Pessoa.username.like(nome))). \
                order_by(asc(Vendedor.id)). \
                paginate(page=int(page),max_per_page=int(totporpag), error_out=False)

        if orderby == '2':
            pagination = Vendedor.query. \
                join(Pessoa, Vendedor.idpessoa == Pessoa.id). \
                filter(or_(Pessoa.nome.like(nome), Pessoa.username.like(nome))). \
                order_by(asc(Pessoa.nome)). \
                paginate(page=int(page), max_per_page=int(totporpag), error_out=False)


    else:
        if orderby == '0':
            pagination = Vendedor.query. \
                join(Pessoa, Vendedor.idpessoa == Pessoa.id). \
                order_by(desc(Vendedor.id)). \
                paginate(page=int(page), max_per_page=int(totporpag), error_out=False)
        if orderby == '1':
            pagination = Vendedor.query. \
                join(Pessoa, Vendedor.idpessoa == Pessoa.id). \
                order_by(asc(Vendedor.id)). \
                paginate(page=int(page), max_per_page=int(totporpag), error_out=False)

        if orderby == '2':
            pagination = Vendedor.query. \
                join(Pessoa, Vendedor.idpessoa == Pessoa.id). \
                order_by(asc(Pessoa.nome)). \
                paginate(page=int(page), max_per_page=int(totporpag), error_out=False)

    vendedores = pagination.items
    totalvendedores = len(vendedores)

    import jwt
    datauser = jwt.decode(token, current_app.config['SECRET_KEY'])
    current_user = get_user_by_username(datauser['username'])
    userschema = UsersSchema()



    if vendedores:
        vendedoresschema = VendedorSchema(many=True)

        result = vendedoresschema.dump(vendedores)



        #return jsonify({'mensagem': 'Todos os Produtos:. '+str(totalprod),'token': token,'data': result}), 201
        import  json
        datapag = '{"nextpag":"'+str(pagination.has_next)+'","prevpag":"'+str(pagination.has_prev)+'",'
        datapag +='"nextnum": "'+str(pagination.next_num if pagination.next_num!=None else 0) +'",'
        datapag +='"pageatual": "'+str(pagination.page if pagination.page!=None else 0)+'",'
        datapag += '"totpage": "'+str(pagination.pages if pagination.pages!=None else 0)+'",'

        if pagination.per_page != None:
            datapag +='"per_page": "'+ str(pagination.per_page)+'",'
        else:
            datapag += '"per_page": "' + str(0) + '",'

        if pagination.prev_num != None:
            datapag +='"prev_num": "'+ str(pagination.prev_num)+'"}'
        else:
            datapag += '"prev_num": "' + str(0) + '"}'



        datapag = json.loads(datapag)



        return jsonify({'datapagination': datapag, 'tabvendedor':result,
                        'token': token,
                        'mensagem':' Total de Vendedores encontrados:'+str(len(vendedores)),
                        'current_user': userschema.dump(current_user),
                        'result': True}),201

    return jsonify({'datapagination': {}, 'tabvendedor': {},
                    'token': token,
                    'mensagem': 'Nenhum Vendedor foi encontrado na base de dados',
                    'current_user': userschema.dump(current_user),
                    'result': False}),201


def get_allvendedoresmain(current_user,token,page,totporpag,order):
    result = get_allvendedores(current_user,token,page,totporpag,order)
    res_json= result[0].json
    current_user = res_json['current_user']
    result = res_json['result']
    datapagination = res_json['datapagination']
    tabvendedor = res_json['tabvendedor']
    mensagem  = res_json['mensagem']
    order = order;
    return render_template('layouts/vendedores/vendedores.html',
                           token=token,
                           mensagem = mensagem,
                           datapagination = datapagination,
                           result = result,
                           order = order,
                           tabvendedor = tabvendedor)


def get_bycpf(cpf):
    try:
        vendedor = Vendedor.query.filter(Vendedor.cpfcnpj == cpf).one()
        return vendedor
    except:
        return None


def delete_vendedor():
    try:
        id = request.args.get('idvendedor')
    except:
        id = '-1'

    if id == '-1':
        return jsonify({'mensagem': 'Erro ao carregar Id do vendedor ', 'data': {},'resultado':False}), 404

    vendedor = Vendedor.query.get(id)
    if not vendedor:
        return jsonify({'mensagem': 'Vendedor não encontrado para ser excluido', 'data': {}, 'result':False}), 404
    try:
        pessoa = Pessoa.query.get(vendedor.idpessoa)
        db.session.delete(pessoa)
        db.session.delete(vendedor)
        db.session.commit()
        vendedorschema = VendedorSchema()
        result = vendedorschema.dump(vendedor)
        return jsonify({'mensagem': 'Vendedor '+pessoa.nome+' excluido com sucesso!', 'data': result,'result':True}), 201
    except:
        return jsonify({'mensagem': 'Não foi possível excluir o vendedor: '+pessoa.nome, 'data': {},'result':False}), 500
