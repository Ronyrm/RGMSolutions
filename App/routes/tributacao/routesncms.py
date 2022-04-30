from flask import Blueprint,jsonify,request
from App.views.tributacao import ncms

routesncms = Blueprint('routesncms',__name__)

@routesncms.route('/get/tributacao/ncm/json',methods=['GET'])
def get_ncms_json():
    if request.method == 'GET':
        desc = request.args.get('desc')
        page = request.args.get('page')
        per_page = request.args.get('per_page')

    tab_ncms = ncms.get_ncms_json(desc if desc != None else '',
                                  int(page if page != None else '1'),
                                  int(per_page if per_page != None else '100'))
    if tab_ncms:
        import simplejson
        #transforma lista em stringjson
        result = simplejson.dumps(tab_ncms)
        #transforma string em json
        resultjson = simplejson.loads(result)

        #schemancms = SchemaNCMS(only=['codncm','descricao'])
        return jsonify({'data': resultjson, 'result': True})
    return jsonify({'data': {}, 'result': False})


@routesncms.route('/tributacao/ncms',methods=['GET'])
def get_ncms_main():
    if request.method == 'GET':
        desc = request.args.get('desc')
        page = request.args.get('page')
        per_page = request.args.get('per_page')

    if desc == None:
        desc = ''


    return ncms.get_ncms_main(desc, int(page if page != None else '1'), int(per_page if per_page != None else '100'))


@routesncms.route('/tributacao/ncm/insert/into/sql',methods=['POST'])
def insert_into_ncms():
    return ncms.insert_into_sql()
