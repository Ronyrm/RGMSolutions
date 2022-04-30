from flask import Blueprint
from App.views.produtos import product
from App.views import helper


routesproduct = Blueprint('routesproduct',__name__)

@routesproduct.route('/add/produto/<page>/<totporpag>',methods=['POST'])
@helper.token_required
def add_product(current_user, token,page,totporpag):
    return product.add_product_form(current_user, token, page, totporpag)

@routesproduct.route('/produto/<idproduto>/',methods=['GET'])
def get_byid(idproduto):
    return product.get_byid(idproduto)

@routesproduct.route('/update/produto/<page>/<totporpag>',methods=['POST'])
@helper.token_required
def update_product(current_user, token,page,totporpag):
    return product.update_product_form(current_user, token, page, totporpag)

@routesproduct.route('/allprodutos/<page>/<totporpag>',methods=['GET'])
@helper.token_required
def get_allproducts(current_user,token,page,totporpag):
    return product.get_allproducts(current_user, token, page, totporpag)

@routesproduct.route('/del/produto/<page>/<totporpag>',methods=['GET'])
@helper.token_required
def del_product_by_id(current_user,token,page,totporpag):
    return product.delete_product_by_id(current_user, token, page, totporpag)


@routesproduct.route('/produtos/',methods=['GET'])
def get_product_by_desc():
    return product.get_product_by_desc()
