from flask import Blueprint,request,jsonify
from App.views.bolsavalores.fiis import getFiis
from App.views.bolsavalores.comprasfiis import GetComprasFiisByCarteira,GetComprasFiisByUser
from App.views.bolsavalores.carteirafiis import GetCarteiraFiisByuser

routesfiis = Blueprint('routesfiis',__name__)

@routesfiis.route('/get/fiis',methods=['POST'])
def GetFiisByStatusInvest():
    if not request.is_json:
        return {"erro": "Envie Content-Type: application/json"}, 400

    dados = request.get_json()

    print("Cheguei na rota!")
    print("JSON recebido:", dados)

    try:
        
 
        resultado = getFiis(dados)  # sua função
        print(resultado)
        return jsonify(resultado),200
    except Exception as e:
        print("Erro interno:", e)
        return jsonify({"erro": str(e)}), 500


@routesfiis.route('/get/comprasfiis/<idcarteira>') 
def GetComprasFiisByCarteira(idcarteira):
    return jsonify(GetComprasFiisByCarteira(idcarteira))


@routesfiis.route('/get/comprasfiis/users/<iduser>') 
def GetComprasFiisByUsers(iduser):
    return jsonify(GetComprasFiisByUser(iduser))


@routesfiis.route('/get/carteira/user/<iduser>')
def GetCarteiraByUser(iduser):
    return jsonify(GetCarteiraFiisByuser(iduser))