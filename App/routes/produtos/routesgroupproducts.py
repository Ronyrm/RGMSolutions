from flask import Blueprint
from App.views.produtos import groupproducts

routesgroupproducts = Blueprint('routesgroupproducts',__name__)

@routesgroupproducts.route('/post/grupoprodutos/',methods=['GET'])
def addedit_groupproduct():
    return groupproducts.addedit_groupproduct()

@routesgroupproducts.route('/grupoprodutos/id/',methods=['GET'])
def get_byidgroupproduct():
    return groupproducts.get_groupproduct_byid()

@routesgroupproducts.route('/all/grupoprodutos/',methods=['GET'])
def get_all_grupoproducts():
    return groupproducts.get_all_groupproduct()


@routesgroupproducts.route('/grupoprodutos/desc/<page>/<totporpag>',methods=['GET'])
def get_bydescgroupproduct(page,totporpag):
    return groupproducts.get_groupproduct_bydesc(page, totporpag)

@routesgroupproducts.route('/delete/grupoprodutos/',methods=['GET'])
def delete_groupproduct():
    return groupproducts.delete_groupproduct()
