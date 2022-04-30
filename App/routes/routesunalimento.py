from flask import Blueprint
from App.views import unalimento

routesunalimentos = Blueprint('routesunalimentos',__name__)

@routesunalimentos.route('/unalimentos/',methods=['GET'])
def get_bydescricao():
    return unalimento.get_bydescricao()


@routesunalimentos.route('/unalimentos.json/',methods=['GET'])
def get_bydescricaojson():
    return unalimento.get_bydescricaojson()
