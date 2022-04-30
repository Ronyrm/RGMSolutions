from flask import Blueprint, render_template, session
from App.views import main,helper
from App.schema.schema import UsersSchema

main = Blueprint('main', __name__)


@main.route('/main/', methods=['GET'])
@helper.token_required
def indexmain(current_user, token):
    if token:
        from App.model import users
        user_schema = UsersSchema()
        user = user_schema.dump(current_user)
        session['current_user'] = user
        return render_template('layouts/index.html',current_user=current_user,token=token)

@main.route('/index/', methods=['GET'])
def index():
    user = {}
    session['current_user'] = user
    return render_template('layouts/index.html',current_user=user,token='')



@main.route('/login')
def login():
    return render_template('layouts/login.html')


