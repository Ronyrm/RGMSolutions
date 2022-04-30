from App import db
from App.model.produtos.groupproducts import GroupProducts
from flask import jsonify, request
from App.schema.schema import GroupProductsSchema


def get_groupproduct_byid():
    try:
        id = request.args.get['id']
    except:
        id = '-1'

    groupproduct = GroupProducts.query.get(id)
    if groupproduct:
        groupproductschema = GroupProductsSchema
        result = groupproductschema.dump(groupproduct)
        return jsonify({'data':result,'achou':True})
    else:
        return jsonify({'data': {}, 'achou': False})


def get_groupproduct_bydesc(page,totporpag):
    groupproductschema = GroupProductsSchema()
    try:
        desc = request.args.get('descricao')
    except:
        desc = ''

    if desc == 'None':
        pagination = GroupProducts.query.paginate(page=int(page),max_per_page=int(totporpag), error_out=False)
        groupproduct = pagination.items
        totalgrupoprod = len(groupproduct)
        if groupproduct:
            result = groupproductschema.dump(groupproduct, many=True)
            datapag = '{"nextpag":"' + str(pagination.has_next) + '","prevpag":"' + str(pagination.has_prev) + '",'
            datapag += '"nextnum": "' + str(pagination.next_num if pagination.next_num != None else 0) + '",'
            datapag += '"pageatual": "' + str(pagination.page if pagination.page != None else 0) + '",'
            datapag += '"totpage": "' + str(pagination.pages if pagination.pages != None else 0) + '",'

            if pagination.per_page != None:
                datapag += '"per_page": "' + str(pagination.per_page) + '",'
            else:
                datapag += '"per_page": "' + str(0) + '",'

            if pagination.prev_num != None:
                datapag += '"prev_num": "' + str(pagination.prev_num) + '"}'
            else:
                datapag += '"prev_num": "' + str(0) + '"}'

            import json
            datapag = json.loads(datapag)


            return jsonify({'data': result, 'achou': True,'mensagem': '','datapag':datapag})
        else:
            return jsonify({'data': {}, 'achou': False, 'mensagem': 'Nenhum produto cadastrado no banco de dados'})


    groupproduct = GroupProducts.query.filter(GroupProducts.descricao.like("%"+desc+"%"))
    result = groupproductschema.dump(groupproduct)
    try:
        if len(result) > 0:
            result = groupproductschema.dump(groupproduct)
            return jsonify({'grupoprodutos':result,'achou': True,'mensagem': ''})
        else:
            return jsonify({'achou': False,'mensagem': ' Nenhum grupo encontrado com a descrição: '+desc})
    except:
        return jsonify({'achou': False, 'mensagem': ' Nenhum gupo encontrado com a descrição: ' + desc})


def get_all_groupproduct():
    groupproductschema = GroupProductsSchema()
    groupproduct = GroupProducts.query.all()
    totalgrupoprod = len(groupproduct)
    if groupproduct:
        result = groupproductschema.dump(groupproduct, many=True)
        return jsonify({'data': result, 'achou': True,'mensagem': ''})
    else:
        return jsonify({'data': {}, 'achou': False, 'mensagem': 'Nenhum produto cadastrado no banco de dados'})


def addedit_groupproduct():
    try:
        id = request.args.get('idgrupo')
        descricao = request.args.get('descgrupo')
    except:
        return jsonify({'data': {}, 'resultado': False, 'mensagem': 'Erro.Formulário não carregado'})


    acao = ''
    if id == '' or id == '-1':
        acao = 'I'
        groupproduct = GroupProducts()
    else:
        groupproduct = GroupProducts.query.get(id)

    try:
        groupproduct.descricao = descricao
        if acao == 'I':
            db.session.add(groupproduct)
        db.session.commit()
        groupproductschema = GroupProductsSchema()
        result = groupproductschema.dump(groupproduct)
        return jsonify(
            {'data': result, 'resultado': True, 'mensagem': 'Grupo de Produtos cadastrado com sucesso'})
    except:
        return jsonify({'data': {}, 'resultado': False, 'mensagem': 'Erro. Ao cadastrar no banco. Tente novamente mais tarde '})


def delete_groupproduct():
    try:
        id = request.args.get('idgrupo')
    except:
        id = '-1'

    if id == '-1':
        return jsonify({'mensagem': 'Erro ao carregar Id do grupo ', 'data': {},'resultado':False}), 404

    groupproduct = GroupProducts.query.get(id)
    if not groupproduct:
        return jsonify({'mensagem': 'Grupo de Produto não encontrado para ser excluido', 'data': {}, 'resultado':False}), 404
    try:
        db.session.delete(groupproduct)
        db.session.commit()
        groupproductschema = GroupProductsSchema()
        result = groupproductschema.dump(groupproduct)
        return jsonify({'mensagem': 'Grupo de Produtos Excluido com Sucesso', 'data': result,'resultado':True}), 201
    except:
        return jsonify({'mensagem': 'Não foi possível excluir o grupo de produtos: '+groupproduct.descricao, 'data': {},'resultado':False}), 500

