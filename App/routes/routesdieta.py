from flask import Blueprint
from App.views import dieta

routesdieta = Blueprint('routesdieta',__name__)



@routesdieta.route('/post/dieta/',methods=['POST'])
def post_dieta(idrefeicao):
    return dieta.post_dieta_json(idrefeicao)

#@routesdieta.route('/post/dieta/',methods=['GET','POST'])
#def post_dieta():
#    return dieta.post_dieta()


@routesdieta.route('/dietarefeicao/<idrefeicao>/<data>',methods=['GET'])
def get_dietarefeicao(idrefeicao,data):
    return dieta.getdietarefeicao(idrefeicao,data)