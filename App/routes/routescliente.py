from flask import Blueprint
from App.views import cliente

routesclientes= Blueprint('routesclientes',__name__)

@routesclientes.route('/add/cliente.json',methods=['POST'])
def add_cliente():
    return cliente.add_cliente_json()

@routesclientes.route('/cliente/<idcliente>/',methods=['GET'])
def get_byid(idcliente):
    return cliente.get_byid(idcliente)