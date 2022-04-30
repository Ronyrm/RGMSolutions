from App import db,app
from App.model.atleta import Atleta
from App.model.pessoas.pessoa import Pessoa
from App.views.metaatleta import get_metaatleta
from flask import jsonify, request,render_template,redirect,url_for
from werkzeug.security import generate_password_hash,check_password_hash
from App.schema.schema import Atletaschema,RefeicaoSchema,MetaAtletaschema
from flask_login import login_user,logout_user, LoginManager,current_user
from datetime import datetime

login_manager = LoginManager()
#login_manager.login_view = 'routesatleta.get_mainatleta'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return Atleta.query.get(int(user_id))


# VALIDA SE KEYACESS ENVIADO POR PARA O EMAIL É VALIDO PARA DESBLOQUEAR
def validationacessatleta():
    datenow = datetime.now()
    dia = datenow.day
    mes = datenow.month
    ano = datenow.year

    if request.method == 'GET':
        keyacess = request.args.get('keyacess')
        idatleta = request.args.get('idatleta')

        atleta = get_id(idatleta)
        if atleta:
            if atleta.keyacess == keyacess:
                atleta.bloqueado = 'N'
                atleta.keyacess = None
                db.session.commit()
                return render_template('layouts/atleta/maintelaatleta.html',
                                       mensagem='Usuário' + atleta.name + ' validado com sucesso !',
                                       tela='Login',
                                       atletalogado={'edtemail':atleta.email},
                                       result=True,
                                       refeicao=[], metaatleta=[],
                                       dataatual=str(ano) + '-' + str(mes).zfill(2) + '-' + str(dia).zfill(2),
                                       databr=str(dia).zfill(2) + '/' + str(mes).zfill(2) + '/' + str(ano),
                                       sumdieta=[]
                                       )


#Envia email atleta de teste
def sendemailatleta():
    from flask_mail import Mail,Message
    if request.method == 'GET':
        idatleta = request.args.get('idatleta')
        if idatleta != None and idatleta != '':
            atleta = Atleta.query.filter(Atleta.id == idatleta).first()
            if atleta:
                mail = Mail(app)
                msg = Message('Hello',sender='sisnutri@rgmsolutions.com', recipients=[atleta.email])
                msg.body = 'Estou te enviando de teste'
                mail.send(msg)
                return jsonify({'mensagem':'Enviado'})
    return jsonify({'mensagem':'Não Enviado'})


# Envia por email URL para liberar, desbloquear acesso
def sendEmail_verificationacess(recipients,keyacess,nomeatleta,id):
    from App import app
    from flask_mail import Mail, Message
    mail = Mail(app)
    try:
        datenow = datetime.now()
        dia = datenow.day
        mes = datenow.month
        ano = datenow.year

        urlpai = request.url_root
        urlpai += 'sisnutri/atleta/validationacess?keyacess=' + keyacess + '&idatleta=' + str(id)
        html = render_template('layouts/atleta/validationacess/main.html', keyacess=keyacess,
                        nomeatleta=nomeatleta)
        msg = Message('Validação Login Sisnutri - RGMSolutions', sender='sisnutri@rgmsolutions.com', recipients=recipients)
        msg.body = 'Validação de cadastro! Clique no link para ativar: '+urlpai


        mail.send(msg)
        return True
    except:
        return False

#IR PRA TELA DIARIO
def get_maindiarioatleta():
    databr = request.args.get('databr')
    dataatual = request.args.get('dataatual')

    if not current_user.is_authenticated:
        return render_template('layouts/atleta/diario/maindiario.html',atletalogado=[],
                               mensagem='',result=False,refeicao=[],
                               metaatleta=[],
                               dataatual=dataatual,
                               databr=databr,
                               sumdieta=[])
    else:


        schemaref = RefeicaoSchema()

        metaatleta = get_metaatleta(current_user.id,'A')

        from App.views.dieta import totalkcaldieta
        sumdieta = totalkcaldieta(current_user.metaatleta[0].id,dataatual)

        from App.views.refeicao import get_refeicao_byidpessoa
        refeicao = get_refeicao_byidpessoa(current_user.idpessoa)

        schemameta = MetaAtletaschema()

        schemaatleta = Atletaschema()

        return render_template('layouts/atleta/diario/maindiario.html', atletalogado=schemaatleta.dump(current_user), mensagem='', result=False,
                               #refeicao=schemaref.dump(current_user.pessoa.refeicao,many=True),
                               refeicao=schemaref.dump(refeicao,many=True),
                               metaatleta=schemameta.dump(metaatleta,many=True),
                               dataatual=dataatual,
                               databr=databr,
                               sumdieta=sumdieta)


def get_maintelaatleta():

    datenow = datetime.now()
    dia = datenow.day
    mes = datenow.month
    ano = datenow.year

    if not current_user.is_authenticated:
        return render_template('layouts/atleta/maintelaatleta.html',atletalogado=[],mensagem='',result=False,
                               refeicao=[],metaatleta = [],
                               dataatual=str(ano) + '-' + str(mes).zfill(2) + '-' + str(dia).zfill(2),
                               databr=str(dia).zfill(2) + '/' + str(mes).zfill(2) + '/' + str(ano),
                               sumdieta=[]
                               )
    else:
        dataatual = str(ano) + '-' + str(mes).zfill(2) + '-' + str(dia).zfill(2)

        metaatleta = get_metaatleta(current_user.id,'A')
        schemameta = MetaAtletaschema()

        schemaatleta = Atletaschema()

        schemaref = RefeicaoSchema()
        from App.views.refeicao import get_refeicao_byidpessoa
        refeicao = get_refeicao_byidpessoa(current_user.idpessoa)

        from App.views.dieta import totalkcaldieta

        sumdieta = []
        if len(current_user.metaatleta) != 0:
            sumdieta = totalkcaldieta(current_user.metaatleta[0].id, dataatual)

        return render_template('layouts/atleta/maintelaatleta.html', atletalogado=schemaatleta.dump(current_user), mensagem='', result=False,
                               refeicao=schemaref.dump(refeicao,many=True),
                               metaatleta=schemameta.dump(metaatleta,many=True),
                               dataatual=str(ano) + '-' + str(mes).zfill(2) + '-' + str(dia).zfill(2),
                               databr=str(dia).zfill(2) + '/' + str(mes).zfill(2) + '/' + str(ano),
                               sumdieta=sumdieta
                               )


# ATUALIZA DADOS ATLETA NO BANCO DE DADOS
def update_atleta():
    if request.method == 'POST':
        data = request.form
        try:
            id = data['edtid']
        except:
            id = None

        try:
            name = data['edtnomeatleta']
        except:
            name = ''

        try:
            username = data['edtusernameatleta']
        except:
            username = ''

        try:
            email = data['edtemailatleta']
        except:
            email = ''

        try:
            altura = data['edtalturaatleta']
        except:
            altura = None

        try:
            peso = data['edtpesoatleta']
        except:
            peso = None

        try:
            percfat = data['edtpercfatatleta']
        except:
            percfat = None

        try:
            dtbirth = data['edtdtbirthatleta']
        except:
            dtbirth = None

        try:
            selectgenero = data['selectgeneroatleta']
        except:
            selectgenero = None

        try:
            profilenamephone = data['edtprofilename']
        except:
            prolifenamephone = None

        try:
            phone = data['edtphone']
        except:
            phone = None

    if id != '' and id != None:
        atleta = get_id(id)
        if atleta:
            if atleta.email != email:
                atletatemp = get_email(email)
                if atletatemp:
                    atleschema = Atletaschema()
                    return jsonify({'messagem': 'Email: ' + email + ' já cadastrado no banco de dados', 'data': {},
                                    'result': False}), 201

            if atleta.username != username:
                atletatemp = get_username(username)
                if atletatemp:
                    atleschema = Atletaschema()
                    return jsonify(
                        {'messagem': 'UserName: ' + username + ' já cadastrado no banco de dados', 'data': {},
                         'result': False}), 201


            pessoa =  Pessoa.query.get(atleta.idpessoa)
            if pessoa:
                try:
                    pessoa.nome = name
                    pessoa.email = email
                    pessoa.username = username
                    pessoa.profilenamephone = profilenamephone
                    pessoa.phone = phone
                    db.session.commit()
                except:
                    return jsonify({'mensagem': 'Erro ao atualizar dados, tente novamente mais tarde!', 'data': {},
                                    'result': False}), 201

            atleta.name = name
            atleta.email = email
            atleta.username = username
            atleta.altura = altura
            atleta.peso = peso
            atleta.percfat = percfat
            atleta.genero = selectgenero
            atleta.dtnascimento = dtbirth
            atleta.profilenamephone = profilenamephone
            atleta.phone = phone
            try:
                db.session.commit()
                atletaschema = Atletaschema()
                result = atletaschema.dump(atleta)
                return jsonify({'mensagem': 'Dados do Usuário atualizado com sucesso', 'data': result, 'result': True}), 201
            except:
                return jsonify({'mensagem': 'Erro ao atualizar dados, tente novamente mais tarde!', 'data': {}, 'result': False}), 201

    return jsonify({'mensagem': 'Usuário Inválido', 'data': {}, 'result': False}), 201


# REIGISTRA ATLETA NO BANCO DE DADOS
def add_atleta():
    datenow = datetime.now()
    dia = datenow.day
    mes = datenow.month
    ano = datenow.year

    if request.method == 'POST':
        data = request.form
        try:
            id = data['edtid']
        except:
            id = ''

        if id == None:
            id = '-1'

        try:
            name = data['edtname']
        except:
            name = ''

        try:
            username = data['edtusername']
        except:
            username = ''

        try:
            email = data['edtemail']
        except:
            email = ''

        try:
            pwd= data['edtsenha']
        except:
            pwd = ''

        try:
            pwdconf = data['edtsenhaconf']
        except:
            pwdconf = ''

        try:
            profilenamephone = data['edtprofilename']
        except:
            profilenamephone = None

        try:
            phone = data['edtphone']
        except:
            phone = None


    if pwd != pwdconf:
        return render_template('layouts/atleta/maintelaatleta.html',
                               mensagem='Senha não confere',
                               tela='Registrar',
                               atletalogado=data,
                               result=False,
                               refeicao=[], metaatleta=[],
                               dataatual=str(ano) + '-' + str(mes).zfill(2) + '-' + str(dia).zfill(2),
                               databr=str(dia).zfill(2) + '/' + str(mes).zfill(2) + '/' + str(ano),
                               sumdieta=[]
                               )



    pass_hash = generate_password_hash(pwd)


    if id == '-1':
        atleta = get_username(username)
        if atleta:
            atletaschema = Atletaschema()
            return render_template('layouts/atleta/maintelaatleta.html',
                                   mensagem='UserName: '+username+' já cadastrado no banco de dados',
                                   tela='Registrar',
                                   atletalogado=data,
                                   result=False,
                                   refeicao=[], metaatleta=[],
                                   dataatual=str(ano) + '-' + str(mes).zfill(2) + '-' + str(dia).zfill(2),
                                   databr=str(dia).zfill(2) + '/' + str(mes).zfill(2) + '/' + str(ano),
                                   sumdieta=[]
                                   )


        atleta = get_email(email)
        if atleta:
            atletaschema = Atletaschema()
            return render_template('layouts/atleta/maintelaatleta.html',
                                   mensagem='Email: ' + email + ' já cadastrado no banco de dados',
                                   tela='Registrar',
                                   atletalogado=data,
                                   result=False,
                                   refeicao=[], metaatleta=[],
                                   dataatual=str(ano) + '-' + str(mes).zfill(2) + '-' + str(dia).zfill(2),
                                   databr=str(dia).zfill(2) + '/' + str(mes).zfill(2) + '/' + str(ano),
                                   sumdieta=[]
                                   )

        pessoa = Pessoa(username=username,nome=name,password=pass_hash,email=email,tipopessoa='AT',phone=phone,profilenamephone=profilenamephone)
        db.session.add(pessoa)
        db.session.commit()

        from App.funcs.funcs import gera_keyacess
        keyacess = gera_keyacess()

        try:
            atleta = Atleta(username=username,name=name, password=pass_hash,email=email,
                            idpessoa=pessoa.id,bloqueado='S',keyacess=keyacess,phone=phone,profilenamephone=profilenamephone)
            db.session.add(atleta)
        except:
            pass
    else:
        atleta = get_id(id)
        if atleta:
            if atleta.email != email:
                atletatemp = get_email(email)
                if atletatemp:
                    atleschema = Atletaschema()
                    return jsonify({'messagem': 'Email: ' + email + ' já cadastrado no banco de dados', 'data': {},
                                    'result': False}), 201

            if atleta.username != username:
                atletatemp = get_username(username)
                if atletatemp:
                    atleschema = Atletaschema()
                    return jsonify({'messagem': 'UserName: ' + username + ' já cadastrado no banco de dados', 'data': {},
                                    'result': False}), 201

            atleta.username = username
            atleta.name = name
            atleta.password = pass_hash
            atleta.email = email

        else:
            return jsonify({'messagem': 'Usuário Inválido', 'data': {}, 'result': False}), 201

    db.session.commit()

    try:
        # url = request.origin
        recipient = []
        recipient.append(email)
        envio = sendEmail_verificationacess(recipient, keyacess, atleta.name, atleta.id)

    except:
        envio = False;

    atletaschema = Atletaschema()
    result = atletaschema.dump(atleta)
    try:
        #return jsonify({'messagem': 'successfully fetched', 'data': result,'result': True}), 201
        return render_template('layouts/atleta/maintelaatleta.html',
                               mensagem='Usuário'+ username +' cadastrado com Sucesso. Verifique sua caixa de email para validar o acesso!',
                               tela='Login',
                               atletalogado=data,
                               result=True,
                               refeicao=[], metaatleta=[],
                               dataatual=str(ano) + '-' + str(mes).zfill(2) + '-' + str(dia).zfill(2),
                               databr=str(dia).zfill(2) + '/' + str(mes).zfill(2) + '/' + str(ano),
                               sumdieta=[]
                               )

    except:
        return jsonify({'messagem': 'unable to create', 'data': {},'result': False}), 201


def get_username(username):
    try:
        return Atleta.query.filter(Atleta.username == username).one()
    except:
        return None


def get_email(email):
    try:
        return Atleta.query.filter(Atleta.email == email).one()
    except:
        return None


def get_atleta_by_idpessoa(idpessoa):
    try:
        return Atleta.query.filter(Atleta.idpessoa == idpessoa).one()
    except:
        return None


# Captura atleta pelo numero de telefone zap
def get_atleta_by_phone(phone):
    phone2 = phone[2:len(phone)-1]
    try:
        from sqlalchemy import  or_
        return  Atleta.query.filter(or_(Atleta.phone==phone,Atleta.phone==phone2)).one()
    except:
        return None


def get_id(id):
    try:
        return Atleta.query.get(id)
    except:
        return None


def login():
    datenow = datetime.now()
    dia = datenow.day
    mes = datenow.month
    ano = datenow.year

    if request.method == 'POST':
        data = request.form
        username = data['edtemail']
        pwd = data['edtsenha']
        atleta = get_email(username)

        if not atleta:
            atleta = get_username(username)

        if atleta:
            if atleta.bloqueado == 'S':
                return render_template('layouts/atleta/maintelaatleta.html', tela='Login',
                                       mensagem='Usuário: '+username+ ' encontra-se bloqueado! Verifique sua caixa de email para ativar o login"', result=False,
                                       atletalogado={}, refeicao=[], metaatleta=[],
                                       dataatual=str(ano) + '-' + str(mes).zfill(2) + '-' + str(dia).zfill(2),
                                       databr=str(dia).zfill(2) + '/' + str(mes).zfill(2) + '/' + str(ano),
                                       sumdieta=[]
                                       )

            if check_password_hash(atleta.password,pwd):
                login_user(atleta)
                from App.views.refeicao import get_refeicao_byidpessoa
                refeicao = get_refeicao_byidpessoa(atleta.idpessoa)
                schemaref = RefeicaoSchema()

                from App.views.metaatleta import get_metaatleta
                metaatleta = get_metaatleta(atleta.id, 'A')
                schemameta = MetaAtletaschema()
                resultmeta = schemameta.dump(metaatleta, many=True)

                dataatual = str(ano) + '-' + str(mes).zfill(2) + '-' + str(dia).zfill(2)
                from App.views.dieta import totalkcaldieta
                sumdieta = []
                if metaatleta:
                    sumdieta = totalkcaldieta(metaatleta[0].id, dataatual)


                schematleta = Atletaschema()

                return render_template('layouts/atleta/maintelaatleta.html',atletalogado=schematleta.dump(atleta),result=True,
                                       mensagem='Usuário Logado com Sucesso!',
                                       refeicao=schemaref.dump(refeicao,many=True),
                                       metaatleta=resultmeta,
                                       dataatual=str(ano) + '-' + str(mes).zfill(2) + '-' + str(dia).zfill(2),
                                       databr=str(dia).zfill(2) + '/' + str(mes).zfill(2) + '/' + str(ano),
                                       sumdieta = sumdieta
                                       )

        return render_template('layouts/atleta/maintelaatleta.html',tela='Login',
                               mensagem='Atleta ou senha informado: '+username+' inválidos!',result=False,
                               atletalogado={},refeicao=[],metaatleta=[],
                               dataatual=str(ano) + '-' + str(mes).zfill(2) + '-' + str(dia).zfill(2),
                               databr=str(dia).zfill(2) + '/' + str(mes).zfill(2) + '/' + str(ano),
                               sumdieta = []
                               )


def logout():
    logout_user()
    redirect(url_for('routesatleta.get_mainatleta'))


# ENVIAR CODIGO DE ACESSO QUANDO ATLETA ESQUECE A SENHA PARA ALTERA LA
def sendEmail_keyacess_forgoutit_pwd(recipients,keyacess,nomeatleta,id):
    from App import app
    from flask_mail import Mail, Message
    mail = Mail(app)
    hash_key = generate_password_hash('RGM'+keyacess+'SysNutri')

    try:
        atleta = get_id(id)
        if atleta:
            atleta.bloqueado = 'S'
            atleta.keyacess = hash_key
            db.session.commit()
            try:
                msg = Message('Redefinição de Senha Sisnutri - RGMSolutions',
                              sender='sisnutri@rgmsolutions.com',
                              recipients=[atleta.email])
                msg.body = 'Redefinição de Senha ! Digite o este código :  '+keyacess+'  para cadastrar uma nova senha!';
                
                mail.send(msg)
                return True
            except:
                return False
        else:
            return False
    except:
        return False


#VERIFICA CODIGO ACESSO ENVIADO POR EMAIL DO ATLETA SE É VALIDO
def verify_keyacess_atleta(keyacess,idatleta):

    try:
        atleta = get_id(idatleta)
        if atleta:
            if check_password_hash(atleta.keyacess,'RGM'+keyacess+'SysNutri'):
                return atleta
            else:
                return None
    except:
        return None

# ATUALIZA PASSWORD ATLETA
def update_password_atleta(newpwd,idatleta):
    atleta_ = get_id(idatleta)
    if atleta_:
        try:
            atleta_.password = generate_password_hash(newpwd)
            atleta_.bloqueado = 'N'
            db.session.commit()
            return jsonify({'result': True, 'mensagem': atleta_.name+', sua senha foi atualizada com Sucesso.'})
        except:
            return jsonify({'result': False,'mensagem':'Erro ao atualizar sennha.'})

    return jsonify({'result': False, 'mensagem': 'Erro ao atualizar sennha.'})

def go_tela_login_atleta(idatleta,msg):
    atleta = get_id(idatleta)
    datenow = datetime.now()
    dia = datenow.day
    mes = datenow.month
    ano = datenow.year

    return render_template('layouts/atleta/maintelaatleta.html',
                           mensagem=msg,
                           tela='Login',
                           atletalogado={'edtemail': atleta.email},
                           result=True,
                           refeicao=[], metaatleta=[],
                           dataatual=str(ano) + '-' + str(mes).zfill(2) + '-' + str(dia).zfill(2),
                           databr=str(dia).zfill(2) + '/' + str(mes).zfill(2) + '/' + str(ano),
                           sumdieta=[]
                        )