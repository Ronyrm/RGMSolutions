from flask import Blueprint,redirect,url_for,render_template
from flask_login import login_user,logout_user,login_required

from App import db
from App.views.localidades import uf
from flask import render_template,request,jsonify


routesuf = Blueprint('routesuf',__name__)


@routesuf.route('/get/uf/<iduf>', methods=['GET'])
def get_all_uf(iduf):
    data = []
    if len(request.args) > 0:
        try:
            data = request.args.get('dataonly').split(',')
        except:
            data = []

    from App.schema.localidades.localidades import UfSchema
    ufschema = UfSchema(only=data)
    ufs =  uf.get_uf(iduf)
    result = ufschema.dump(ufs,many=True)
    return jsonify({'data':result})




