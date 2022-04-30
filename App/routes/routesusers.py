from App import app
from flask import jsonify,Blueprint,url_for
from App.views import users,helper

routes = Blueprint('routes', __name__)


@routes.route('/users',methods=['POST'])
def post_user():
    return users.post_user()

@routes.route('/users.form',methods=['POST'])
def post_user_form():
    return users.post_user_form()


@routes.route('/users/<id>', methods=['PUT'])
def update_user(id):
    return users.update_user(id)


@routes.route('/users',methods=['GET'])
def get_users():
    return  users.get_users()


@routes.route('/users/<id>', methods=['GET'])
def get_user(id):
    return users.get_user(id)


@routes.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    return  users.delete_user(id)


@routes.route('/users/pag', methods=['GET'])
#@helper.token_required
def get_userstemplate():
    return users.get_userstemplate()


