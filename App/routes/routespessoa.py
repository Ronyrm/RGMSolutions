from App import app
from flask import jsonify,Blueprint,url_for,request
from App.views import pessoas

routespessoa = Blueprint('routespessoa', __name__)


@routespessoa.route('/pessoa/<id>',methods=['GET'])
def post_user(id):
    return pessoas.get_byid(id)

@routespessoa.route('/pessoa/get/email',methods=['GET'])
def get_email():
    if request.method == 'GET':
        email =  request.args.get('email')
        tp = request.args.get('tp')
        from App.schema.schema import PessoaSchema
        pessoaschema = PessoaSchema()
        pessoa = pessoas.get_byemailpessoa(email,tp)
        result = pessoaschema.dump(pessoa,many=True)
        return jsonify({'data':result})
    return jsonify({})
