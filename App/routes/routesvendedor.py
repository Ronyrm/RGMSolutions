from flask import Blueprint
from App.views import vendedor
from App.views import  helper
from flask import render_template

routesvendedores = Blueprint('routesvendedores',__name__)

@routesvendedores.route('/add/vendedor/<page>/<totporpag>/',methods=['GET','POST'])
@helper.token_required
def add_vendedor(current_user, token,page,totporpag):
    return vendedor.add_vendedor(current_user, token,page,totporpag)

@routesvendedores.route('/edit/vendedor/<page>/<totporpag>/',methods=['GET','POST'])
@helper.token_required
def edit_vendedor(current_user, token,page,totporpag):
    return vendedor.edit_vendedor(current_user, token,page,totporpag)


@routesvendedores.route('/allvendedores/<page>/<totporpag>/<order>',methods=['GET'])
@helper.token_required
def get_allvendedor(current_user,token,page,totporpag,order):
    return vendedor.get_allvendedores(current_user,token,page,totporpag,order)

@routesvendedores.route('/allvendedoresmain//<page>/<totporpag>/<order>',methods=['GET'])
@helper.token_required
def get_allvendedores_main(current_user,token,page,totporpag,order):
    return  vendedor.get_allvendedoresmain(current_user,token,page,totporpag,order)

@routesvendedores.route('/delete/vendedor',methods=['GET'])
def delete_vendedor():
    return vendedor.delete_vendedor()