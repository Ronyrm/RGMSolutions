from App import db,app
from App.model.users import Users
from App.schema.schema import UsersSchema
from werkzeug.security import generate_password_hash
from flask import jsonify, request, redirect, url_for, render_template
import jwt

def post_user():
    username = request.json['username']
    email = request.json['email']
    name = request.json['name']
    password = request.json['password']
    pass_hash = generate_password_hash(password)
    user = Users(username=username, password=pass_hash,name=name, email=email)
    try:
        db.session.add(user)
        db.session.commit()
        result = user_schema.dump(user)
        print(result)
        return jsonify({'message': 'successfully fetched', 'data': result}), 201
    except:
        return jsonify({'message': 'unable to create', 'data': {}}), 500


def post_user_form():
    data = request.form
    username = data['username']
    email = data['email']
    name = data['name']
    password = data['password']

    pass_hash = generate_password_hash(password)
    user = Users(username, pass_hash, name, email)
    try:
        db.session.add(user)
        db.session.commit()
        result = user_schema.dump(user)
        print(result)
        return jsonify({'message': 'successfully fetched', 'data': result}), 201
    except:
        return jsonify({'message': 'unable to create', 'data': {}}), 500



def update_user(id):
    username = request.json['username']
    email = request.json['email']
    name = request.json['name']
    password = request.json['password']

    user = Users.query.get(id)
    if not user:
        return jsonify({'mensagem': 'Usuário não Existe', 'data': {}}), 404

    pass_hash = generate_password_hash(password)

    try:
        user.username = username
        user.email = email
        user.password = pass_hash
        user.name = name
        db.session.commit()
        result = user_schema.dump(user)
        print(result)
        return jsonify({'message': 'successfully fetched', 'data': result}), 201
    except:
        return jsonify({'message': 'unable to create', 'data': {}}), 500


def get_users():
    users = Users.query.all()
    if users:
        result = users_schema.dump(users)
        return jsonify({'mensagem': 'Todos os Usuários', 'data': result}), 201

    return jsonify({'mensagem': 'Falha ao Carregar', 'data': {}}), 500


def get_userstemplate():
    token = request.args.get('token')
    data = []
    if token:
        data = jwt.decode(token, app.config['SECRET_KEY'])
        print('ID:'+str(data['id'])+', Nome: '+data['username'])
        print(token)
    users = Users.query.all()
    if users:

        return render_template('layouts/users.html',
                               users=users,
                               title='ROny',
                               idlogado= data['id'] if data == None else '',
                               usernamelogado=data['username']if data == None else '')
    else:
        return jsonify({'mensagem': 'Falha ao Carregar', 'data': {}}), 500



def get_user(id):
    user = Users.query.get(id)
    if user:
        result = user_schema.dump(user)
        return jsonify({'mensagem': 'Usuário Encontrado', 'data': result}), 201

    return jsonify({'mensagem': 'Usuário não encontrado', 'data': {}}), 404


def delete_user(id):
    user = Users.query.get(id)
    if not user:
        return jsonify({'mensagem': 'Usuário não encontrado', 'data': {}}), 404

    if user:

        try:
            db.session.delete(user)
            db.session.commit()
            result = user_schema.dump(user)
            return jsonify({'mensagem': 'Usuário Excluido com Sucesso', 'data': result}), 201
        except:
            return jsonify({'mensagem': 'Não foi possível excluir o Usuário', 'data': {}}), 500


def get_user_by_username(username):
    from sqlalchemy import or_
    try:
        user = Users.query.filter(or_(Users.username == username, Users.email == username)).one()
        return user
    except:
        return None
