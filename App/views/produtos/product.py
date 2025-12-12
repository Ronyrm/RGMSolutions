from flask import current_app
from App import db
from App.model.produtos.products import Product
from flask import flash, jsonify, request,redirect,render_template,url_for
from App.schema.schema import ProductSchema
from werkzeug.utils import secure_filename
import jwt
import os
import string
import random

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

## Adiciona Produto
def add_product_form(current_user, token,page,totporpag):

    random_str = string.ascii_letters + string.digits + string.ascii_uppercase
    key_img = ''.join(random.choice(random_str) for i in range(6))

    if request.method == 'POST':
        data = request.form
        descricao = data['edtdescricao']
        subdescricao = data['edtsubdescricao']
        estoquemin = data['edtestoqminimo']
        estoqueatual = data['edtestoqatual']
        precocusto = data['edtprecocusto']
        margemlucro = data['edtmargemlucro']
        precovenda = data['edtprecovenda']

        if 'fileimg' not in request.files:
            flash('Nenhum produto informado')
            #return redirect(request.url)
            caminhoimg = ''

        filephotoprod = request.files['fileimg']
        if filephotoprod.filename == '':
            caminhoimg = ''
            #flash('Arquivo não selecionado')
            #return redirect(request.url)
        if filephotoprod and allowed_file(filephotoprod.filename):
            filename = secure_filename(filephotoprod.filename)
            localesave = os.path.abspath(os.getcwd())+current_app.config['UPLOAD_FOLDER']
            filephotoprod.save(os.path.join(localesave, key_img + filename))
            caminhoimg = key_img + filename

    product = Product(descricao = descricao, subdescricao = subdescricao, estoquemin = estoquemin,
                      estoqueatual = estoqueatual, precocusto = precocusto, margemlucro = margemlucro,
                      precovenda = precovenda, caminhoimg = caminhoimg )
    try:
        db.session.add(product)
        db.session.commit()
        productschema = ProductSchema()
        result = productschema.dump(product)
        #return jsonify({'message': 'successfully fetched', 'data': result}), 201
        return redirect(url_for('outesproduct.get_allproducts',token=token,page=page,totporpag=totporpag,msg=''))
    except:
        return jsonify({'message': 'unable to create', 'data': {}}), 500

#Atualiza Product
def update_product_form(current_user, token,page,totporpag):
    random_str = string.ascii_letters + string.digits + string.ascii_uppercase
    key_img = ''.join(random.choice(random_str) for i in range(6))

    if request.method == 'POST':
        data = request.form
        id = data['edtid']

        if id != '-1' and id != '':
            product = Product.query.get(id)
            if not product:
                msg = 'O produto não existe na nossa base de dados'
                return get_allproducts(current_user, token, page, totporpag,msg)
                #return jsonify({'mensagem': 'Produto não Existe', 'data': {}}), 404

        else:
            product = Product.query.filter(Product.descricao == data['edtdescricao']).first()
            if product:
                msgerro = 'A Descrição do Produto:'+ product.descricao + ' já foi cadastrada com o id: ' + str(product.id) + ', verifique!'
                return redirect(url_for('routesproduct.get_allproducts', token=token, page=page, totporpag=totporpag,msgerro=msgerro))
            product = Product()

        descricao = data['edtdescricao']
        subdescricao = data['edtsubdescricao'] + current_app.config['DIRECTORY_APP']
        estoquemin = data['edtestoqminimo']
        estoqueatual = data['edtestoqatual']
        precocusto = data['edtprecocusto']
        margemlucro = data['edtmargemlucro']
        precovenda = data['edtprecovenda']
        idgrupoproduto = data['edtidgrupoproduto']
        if idgrupoproduto == '0':
            idgrupoproduto = None

        caminhoimgBD = Product.caminhoimg
        caminhoimg = ''


        if caminhoimg == '':

            if 'fileimg' not in request.files:
                flash('Nenhum produto informado')
                # return redirect(request.url)
                caminhoimg = ''

            try:
                filephotoprod = request.files['fileimg']
                tamanhoarq =len(filephotoprod.filename)
                if tamanhoarq == 0:
                    caminhoimg = ''
                else:
                    try:
                        if filephotoprod and allowed_file(filephotoprod.filename):
                            filename = secure_filename(filephotoprod.filename)
                            localesave = current_app.config['UPLOAD_FOLDER']
                            caminhoimg = key_img + filename
                    except:
                        caminhoimg = ''
            except:
                caminhoimg = ''



    product.descricao = descricao
    product.subdescricao = subdescricao
    product.estoquemin = estoquemin
    product.estoqueatual = estoqueatual
    product.precocusto = precocusto
    product.margemlucro = margemlucro
    product.precovenda = precovenda
    product.idgrupoproduto = idgrupoproduto
    try:
        if caminhoimg != "" and caminhoimg != None:

            filephotoprod.save(localesave+caminhoimg)
            if product.caminhoimg != '' and product.caminhoimg != None :
                filedelete = os.path.join(localesave, product.caminhoimg)
                os.remove(filedelete)
        else:
            caminhoimg = product.caminhoimg
    except:
        caminhoimg = ''


    caminhoimg = '' if caminhoimg == None else caminhoimg

    product.caminhoimg = caminhoimg
    msg = 'Produto: '+ str(product.id) + ' - ' + product.descricao+' alterado com sucesso!'
    if id == '-1':
        #product.caminhoimg = ''
        msg = 'Produto: '+ product.descricao+' inserindo com sucesso'
        db.session.add(product)

    db.session.commit()
    return redirect(url_for('routesproduct.get_allproducts', token=token, page=page, totporpag=totporpag,msg=msg))
    #except:
    #    msgerro = 'Houve uma falha ao Salvar o produto na base de dados, Tente novamente!'
    #    return redirect(url_for('routesproduct.get_allproducts', token=token, page=page, totporpag=totporpag, msgerro=msgerro))
        #return jsonify({'message': 'unable to create', 'data': {}}), 500


## Pesquisa por ID do Produto
def get_byid(idproduct):
    product = Product.query.get(idproduct)
    if product:
        productschema = ProductSchema()
        result = productschema.dump(product)
        return jsonify({'data': result})

    return jsonify({'message': 'Nenhum Produto foi encontrado com o código: '+idproduct, 'data': {}}), 500


## Filtra todos os produtos
def get_allproducts(current_user,token,page,totporpag):
    try:
        msg = request.args.get('msg')
    except:
        msg = ''

    if not msg:
        msg = ''

    try:
        msgerro = request.args.get('msgerro')
    except:
        msgerro = ''

    if not msgerro:
        msgerro = ''


    try:
        desc = request.args.get('desc')
        desc = "%" + desc + "%"
    except:
        desc = ''

    if not desc:
        desc = ''

    if desc != '':
        pagination = Product.query. \
            filter(Product.descricao.like(desc)). \
            paginate(page=int(page),max_per_page=int(totporpag), error_out=False)
    else:
        pagination = Product.query.paginate(page=int(page), max_per_page=int(totporpag), error_out=False)

    products = pagination.items
    totalprod = len(products)

    data = jwt.decode(token, current_app.config['SECRET_KEY'])

    if products:
        productsschema = ProductSchema(many=True)

        result = productsschema.dump(products)



        #return jsonify({'mensagem': 'Todos os Produtos:. '+str(totalprod),'token': token,'data': result}), 201
        import  json
        datapag = '{"nextpag":"'+str(pagination.has_next)+'","prevpag":"'+str(pagination.has_prev)+'",'
        datapag +='"nextnum": "'+str(pagination.next_num if pagination.next_num!=None else 0) +'",'
        datapag +='"pageatual": "'+str(pagination.page if pagination.page!=None else 0)+'",'
        datapag += '"totpage": "'+str(pagination.pages if pagination.pages!=None else 0)+'",'

        if pagination.per_page != None:
            datapag +='"per_page": "'+ str(pagination.per_page)+'",'
        else:
            datapag += '"per_page": "' + str(0) + '",'

        if pagination.prev_num != None:
            datapag +='"prev_num": "'+ str(pagination.prev_num)+'"}'
        else:
            datapag += '"prev_num": "' + str(0) + '"}'

        url = request.url_root

        datapag = json.loads(datapag)

        caminhoimg = current_app.config['DIRECTORY_APP']+current_app.config['UPLOAD_FOLDER']
        return render_template('layouts/products/products.html',
                                divmsg = msg,
                                divmsgerro=msgerro,
                                urlroot=url,
                                datapag = datapag,
                                tabproducts=result,
                                nextpag=pagination.has_next,
                                prevpag = pagination.has_prev,
                                nextnum = pagination.next_num,
                                pageatual = pagination.page,
                                totpage = pagination.pages,
                                perpage = pagination.per_page,
                                prev_num = pagination.prev_num,
                                caminhoimg=caminhoimg,
                                token=token,
                                idlogado=data['id'] if data==None else '',
                                usernamelogado=data['username'] if data==None else '')

    return render_template('layouts/products/products.html',
                                divmsg = '',
                                urlroot='',
                                datapag = 1,
                                tabproducts={},
                                nextpag=pagination.has_next,
                                prevpag = pagination.has_prev,
                                nextnum = pagination.next_num,
                                pageatual = pagination.page,
                                totpage = pagination.pages,
                                perpage = pagination.per_page,
                                prev_num = pagination.prev_num,
                                caminhoimg='',
                                token=token,
                                idlogado=data['id'] if data==None else '',
                                usernamelogado=data['username'] if data==None else '')


## Filtra por descrição
def get_product_by_desc():
    from sqlalchemy import or_
    try:
        desc = request.args.get('descricao')
        desc = "%" + desc + "%"
        products = Product.query.filter(or_(Product.descricao.like(desc), Product.subdescricao.like(desc)))
        productsschema = ProductSchema(many=True)
        data = productsschema.dump(products)
        return jsonify({'data': data})

    except:
        return jsonify({'data':{}})


def delete_product_by_id(current_user,token,page,totporpag):
    try:
        id = request.args.get('id')
    except:
        id='-1'

    product = Product.query.get(id)
    if not product:
        return jsonify({'mensagem': 'Produto não encontrado', 'data': {},
                        'delete':False,'token':token,'page':page,'totporpag':totporpag}), 404

    if product:

        try:
            prod = product.descricao
            db.session.delete(product)
            db.session.commit()
            product_schema = ProductSchema()
            result = product_schema.dump(product)
            return jsonify({'mensagem': 'O produto '+prod+' foi excluido com Sucesso', 'data': result,'delete':True,
                            'token':token,'page':page,'totporpag':totporpag}), 201
        except:
            return jsonify({'mensagem': 'Não foi possível excluir o Produto', 'data': {},'delete':False,
                            'token':token,'page':page,'totporpag':totporpag}), 500
