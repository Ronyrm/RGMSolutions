from flask import Blueprint
from App.views import helper


auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return 'login'

@auth.route('/signup')
def signup():
    return 'Signup'

@auth.route('/logout')
def logout():
    return 'Logout'

@auth.route('/auth', methods=['POST'])
def authentication():
    return helper.auth()


@auth.route('/auth.form', methods=['POST'])
def auth_form():
    return helper.auth_form()

