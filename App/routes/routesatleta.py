from flask import Blueprint,redirect,url_for,render_template
from flask_login import login_user,logout_user,login_required

from App import db
from App.views import atleta
from flask import render_template,request,jsonify


routesatleta= Blueprint('routesatleta',__name__)


# Enviar email atleta
@routesatleta.route('/send/email/atleta', methods=['GET'])
def sendemailatleta():
    return atleta.sendemailatleta()


# Ir para o Espaço Diário da Alimentação - Refeição
@routesatleta.route('/sisnutri/diario',methods=['GET','POST'])
def get_maindiarioatleta():
    return atleta.get_maindiarioatleta()


# Valida
@routesatleta.route('/sisnutri/atleta/validationacess',methods=['GET'])
def validationacessatleta():
    return atleta.validationacessatleta()


@routesatleta.route('/',methods=['GET','POST'])
def get_mainatleta():
    return atleta.get_maintelaatleta();

@routesatleta.route('/sisnutri/add/atleta',methods=['GET','POST'])
def add_atleta():
    return atleta.add_atleta()

@routesatleta.route('/sisnutri/update/atleta',methods=['POST'])
def updateatleta():
    return atleta.update_atleta()

@routesatleta.route('/sisnutri/atleta/login',methods=['POST'])
def loginatleta():
    return atleta.login()

@routesatleta.route('/sisnutri/atleta/logout')
@login_required
def logoutatleta():
    logout_user()
    return redirect(url_for('routesatleta.get_mainatleta'))

@routesatleta.route('/sisnutri/reset/pwd')
def resetpwd():
    from flask import jsonify
    return jsonify({})

@routesatleta.route('/sisnutri/forgoutit/pwd',methods=['GET'])
def forgoutitkey():
    email = ''
    if request.method == 'GET':
        try:
            email = request.args.get('email')
        except:
            email = ''

    return render_template('layouts/atleta/forgoutitpwd/main.html',email=email)


#BUSCA EMAIL ATLETA
@routesatleta.route('/sisnutri/getemail',methods=['GET'])
def get_email_atleta():
    if request.method == 'GET':
        try:
            email = request.args.get('email')
        except:
            email = ''
    if email != '':
        from App.views.atleta import get_email
        from App.schema.schema import Atletaschema
        atleta = get_email(email)
        if atleta:
            atletaschema = Atletaschema()
            result = atletaschema.dump(atleta)
            return jsonify({'data':result,'result':True})

    return jsonify({'result':False,'mensagem':'Não foi encontrado nenhum atleta com esse email!'})


#ENVIAEMAIL_CODIGOVERIFICACAO
@routesatleta.route('/sisnutri/sendemail/verifykey',methods=['POST'])
def sendemail_verifykey():
    envio = False
    if request.method == 'POST':
        from App.funcs.funcs import gera_keyacess_pdw
        data = request.form
        recipients = []
        recipients.append(data['email'])

        envio = atleta.sendEmail_keyacess_forgoutit_pwd(recipients,
                                                        gera_keyacess_pdw(7),
                                                        data['nome'],
                                                        data['id'])

    return jsonify({'result':envio})


#VERIFICA KEYACESS ATLETA
@routesatleta.route('/sisnutri/atleta/verifykeyacess',methods=['POST'])
def verifykey_atleta():
    if request.method=='POST':
        data = request.form
        key = ''
        try:
            key = data['edtkeyacess']
        except:
            key = ''

        idatleta = data['edtidatleta']

        if key !='':
            atl = atleta.verify_keyacess_atleta(key,idatleta)
            if atl:
                atl.bloqueado = 'N'
                atl.keyacess = None
                db.session.commit()
                #from App.schema.schema import Atletaschema
                #atletaschema = Atletaschema()

                return jsonify({'result': True,
                                'mensagem': atl.name+' desbloqueado',
                                'idatleta': atl.id})
    return jsonify({'result': False, 'mensagem': 'bloqueado','idatleta': 0})


#UPDATE NOVA SENHA ATLETA
@routesatleta.route('/sisnutri/atleta/update/newpwd',methods=['POST'])
def update_pwd_atleta():
    if request.method=='POST':
        data = request.form
        newpwd = ''
        idatleta = '0'
        try:
            newpwd = data['edtpwd']
        except:
            newpwd = ''
        try:
            idatleta = data['edtidatleta']
        except:
            idatleta = '0'

        if newpwd != '' and idatleta != '':
            result = atleta.update_password_atleta(newpwd,idatleta)
            return result

    return jsonify({'result': False, 'mensagem': 'Erro ao atualizar sennha.'})

@routesatleta.route('/go/telalogin/<idatleta>/<msg>',methods = ['GET'])
def go_tela_login(idatleta,msg):

    return atleta.go_tela_login_atleta(idatleta,msg)

@routesatleta.route('/redirect/telalogin/atleta/<idatleta>/<msg>',methods=['GET'])
def red(idatleta,msg):
    return redirect(url_for('routesatleta.go_tela_login',idatleta=idatleta,msg=msg))