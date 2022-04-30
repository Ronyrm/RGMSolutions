from flask import jsonify,Blueprint,url_for
from App.views import alimentos

routestabalimentos = Blueprint('routestabalimentos',__name__)

@routestabalimentos.route('/add/food',methods=['POST'])
def post_alimento():
    return alimentos.post_food()

@routestabalimentos.route('/tabalimentos.json/<pageatual>/<totpage>/<orderby>',methods=['GET'])
def get_alimentobydesc(pageatual,totpage,orderby):
    return alimentos.get_alimento_bydesc(totpage,orderby)

@routestabalimentos.route('/tabalimentos',methods=['GET'])
def get_tabalimentos():
    return alimentos.get_tabalimentos()

@routestabalimentos.route('/tabfoods.json',methods=['GET'])
def get_tabalmentos():
    return alimentos.get_alimento_bydesc_json()

@routestabalimentos.route('/flipbook/',methods=['GET'])
def pagflipbook():
    return alimentos.pagflipbook();