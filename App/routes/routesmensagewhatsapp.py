from flask import  Blueprint,jsonify,request
from App.views import mensagewhatsapp
routesmensagewhatsapp = Blueprint('routesmensagewhatsapp',__name__)

@routesmensagewhatsapp.route('/get/mensagewhatsapp/<idpessoa>',methods=['GET'])
def mensagwhatsapp(idpessoa):
    msg =  mensagewhatsapp.getmensagewhatsapp(idpessoa)
    if msg:
        from App.schema.schema import MensageWhatsAppSchema
        msgschema = MensageWhatsAppSchema()
        return jsonify({'data': msgschema.dump(msg,many=True),'result': True})


    return jsonify({'data': {},'result': False})



@routesmensagewhatsapp.route('/get/cep',methods=['GET'])
def get_cep():
    if request.method == 'GET':
        from App.views.several import busca_dados_CEP
        cep = request.args.get('cep')
        return jsonify(busca_dados_CEP(cep))