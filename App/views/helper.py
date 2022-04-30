from App import app
from flask import jsonify,request,render_template,session,url_for,redirect
from functools import wraps
import datetime
import jwt
from werkzeug.security import check_password_hash
from .users import get_user_by_username
from App.schema.schema import UsersSchema
def auth():

    aut = request.authorization
    if not aut or not aut.username or not aut.password:
        return jsonify({'mensage':'Não pode verificar','WWW-Authenticate':'Basic auth="Login Required"'}), 401

    user = get_user_by_username(aut.username)
    if not user:
        return jsonify({'mensage':'Nenhum Usuário não encontrado!','data':{}}),401

    if user and check_password_hash(user.password, aut.password):
        dtexp = datetime.datetime.now() + datetime.timedelta(hours=12)
        token = jwt.encode({'username': user.username, 'id': user.id, 'exp': dtexp},
                           app.config['SECRET_KEY'],
                           algorithm='HS256')
        try:
            token_decode = token.decode('utf-8')
        except ValueError as err:
            erro = err
            return jsonify({'message': 'Erro ao decodificar:'+err, 'WWW-Authenticate': 'Basic auth="Login required"'}), 401

        print(token_decode)

        return jsonify({'message': 'Validated successfully', 'token': token_decode,
                        'exp': datetime.datetime.now() + datetime.timedelta(hours=12)})

    return jsonify({'message':'Não pode verificar!','WWW-Authenticate':'Basic auth="Login required"'}), 401


def auth_form():

    data = request.form
    username = data['username']
    password = data['password']
    if not data or not username or not password:
        return jsonify({'mensage':'Não pode verificar','WWW-Authenticate':'Basic auth="Login Required"'}), 401

    user = get_user_by_username(username)
    current_user = user
    if not user:
        return render_template('layouts/login.html',
                               sucess=False,
                               mensage='Usuário '+username+' não encontrado na base de dados!'
                               )

        #return jsonify({'mensage':'Nenhum Usuário foi encontrado!','data':{}}), 401

    valida = check_password_hash(user.password, password)
    if user and valida:
        dtexp = datetime.datetime.now() + datetime.timedelta(hours=12)
        token = jwt.encode({'username': user.username, 'id': user.id, 'exp': dtexp},
                           app.config['SECRET_KEY'],
                           algorithm='HS256')
        try:
            token_decode = token.decode('utf-8')
        except ValueError as err:
            return jsonify({'message': 'Erro ao decodificar:'+err, 'WWW-Authenticate': 'Basic auth="Login required"'}), 401

        print(token_decode)

        #retorno = jsonify({'message': 'Validated successfully', 'token': token_decode,
        #                'exp': datetime.datetime.now() + datetime.timedelta(hours=12)})
        #return retorno
        user_schema = UsersSchema()
        userschema = user_schema.dump(current_user)
        session['current_user'] = userschema

        #return render_template('layouts/index.html',
        #                       sucess=True,
        #                       token=token_decode,
        #                       idlogado=user.id,
        #                       usernamelogado=username,
        #                       nameuser=user.name,
        #                       current_user=userschema)
        try:
            return redirect(url_for('main.indexmain',token=token))
            #return jsonify({'message': 'Login Efetuado com sucesso:', 'WWW-Authenticate': 'Sucesso',
            #               'token': token}), 202
        except:
            return jsonify({'message': 'Erro ao Carregar Pagina:', 'WWW-Authenticate': 'Basic auth="Login required"','token':token}), 401
    else:
        return render_template('layouts/login.html',
                               sucess=False,
                               mensage='Senha do Usuário ' + username +', inválida!')

        #return jsonify({'message':'Não pode verificar!','WWW-Authenticate':'Basic auth="Login required"'}), 401


def token_required(func):

    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'valide': False, 'mensage': ' Token não informado','data': {}}), 401
            #return render_template('layouts/index.html')
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = get_user_by_username(data['username'])

            #return jsonify({'valide': True, 'mensage': ' Token Valido', 'data': data}), 201

        except:
            return jsonify({'valide': False, 'mensage': ' Token inválido ou expirado', 'data': {}}), 401

        return func(current_user,token,*args, **kwargs)
    return decorated



