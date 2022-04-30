from flask import  Blueprint,request, jsonify,render_template
from config import ACESS_TOKEN_MERCADOPAGO_VENDEDOR_TEST
import mercadopago
routemercadopago = Blueprint('routemercadopago',__name__)

@routemercadopago.route('/payment/mercadopago/rgmsolutions',methods=['POST'])
def paymentMercadoPago():
    try:
        if request.method == 'POST':
            data = request.json
            items = data['items']
            payer = data['payer']
            payment_methods = data['payment_methods']
            back_urls = data['back_urls']

            sdk = mercadopago.SDK(ACESS_TOKEN_MERCADOPAGO_VENDEDOR_TEST)
            preference_data = {
                "items": items,
                "payer": payer,
                "payment_methods": payment_methods,
                "back_urls": back_urls
            }

            preference_response = sdk.preference().create(preference_data)
            URLsandbox = preference_response["response"]["sandbox_init_point"]
            preference = preference_response["response"]["sandbox_init_point"]

            return jsonify({'urlsandbox':URLsandbox, 'preference':preference})
    except:
        pass
    return jsonify({'urlsandbox':{}, 'preference': {}})

@routemercadopago.route('/mercadopago/success')
def mercadopagoSucess():
    data = {'error':False,'mensagem':'Pagamento aprovado com sucesso'}
    return render_template('layouts/mercadopago/main.html',data=data)

@routemercadopago.route('/mercadopago/failure')
def mercadopagoFailure():
    data = {'error':True,'mensagem':'Pagamento não foi aprovado.'}
    return render_template('layouts/mercadopago/main.html',data=data)

@routemercadopago.route('/mercadopago/pedding')
def mercadopagoPedding():
    data = {'error':True,'mensagem':'Pagamento Pendente.'}
    return render_template('layouts/mercadopago/main.html',data=data)
