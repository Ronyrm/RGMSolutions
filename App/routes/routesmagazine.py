from flask import Blueprint
from App.views import magazine

routesmagazine = Blueprint('routesmagazine',__name__)

@routesmagazine.route('/magazine',methods=['GET'])
def get_bydescricao():
    return magazine.get_magazine()


