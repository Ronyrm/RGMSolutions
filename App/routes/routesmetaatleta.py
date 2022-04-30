from flask import Blueprint,redirect,url_for,request,jsonify
from App.views import metaatleta
from App.schema.schema import MetaAtletaschema
routesmetaatleta= Blueprint('routesmetaatleta',__name__)

# captura meta por id atleta e pelo get status
@routesmetaatleta.route('/sisnutri/meta/atleta/<idatleta>',methods=['GET'])
def get_metaatleta(idatleta):
    try:
        status = request.args.get('status')
    except:
        status = 'A'

    if status == None:
        status = 'A'
    metaschema = MetaAtletaschema
    return metaschema.dump(metaatleta.get_metaatleta(idatleta,status),many=True)

# captura meta por id pessoa e pelo get status
@routesmetaatleta.route('/sisnutri/meta/pessoa/<idpessoa>',methods=['GET'])
def get_metaatleta_idpessoa(idpessoa):
    try:
        status = request.args.get('status')
    except:
        status = 'A'
    if status == None:
        status = 'A'
    return metaatleta.get_metaatleta_porpessoa(idpessoa,status)


#insere meta
@routesmetaatleta.route('/post/metaatleta',methods=['POST'])
def post_metaatleta():
    return metaatleta.postmetaatleta();

# retorna total de meta atleta pelo id atleta
@routesmetaatleta.route('/count/metaatleta',methods=['GET'])
def count_metaatleta():
    return metaatleta.count_metaatleta()

# finaliza meta aberta
@routesmetaatleta.route('/sisnutri/finaliza/meta/atleta',methods=['POST'])
def finalizameta():
    return  metaatleta.finalizameta()


@routesmetaatleta.route('/gemeta/<idatleta>')
def getmeta(idatleta):
    meta = metaatleta.get_metaatleta(idatleta,'A')

    result = MetaAtletaschema()
    result = result.dump(meta, many=True)
    return jsonify({'data':result})