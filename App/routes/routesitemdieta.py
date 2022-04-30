from flask import Blueprint
from App.views import itemdieta

routesitemdieta = Blueprint('routesitemdieta',__name__)

@routesitemdieta.route('/add/itemdieta',methods=['POST'])
def postitemdietajson():
    return itemdieta.post_itemdieta_form()

@routesitemdieta.route('/itemdieta.json/<iddieta>',methods=['GET'])
def get_dietarefeicao(iddieta):
    return itemdieta.getitemdieta(iddieta)

@routesitemdieta.route('/delete/itemdieta',methods=['GET'])
def delete_itemdieta():
    return itemdieta.deleteitemdieta()