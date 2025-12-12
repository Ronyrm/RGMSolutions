from App import db,login_manager
from flask  import current_app
from App.model.alimentos import Alimentos
from App.schema.schema import FoodsSchema
from App.model.atleta import Atleta
from flask import jsonify, request,render_template
from flask_login import current_user

import json

from flask_paginate import get_page_args


@login_manager.user_loader
def load_user(user_id):
    return Atleta.query.get(int(user_id))


def post_food():
    if request.method == 'POST':
        data = request.form
        try:
            descricao = data['edtdescricao']
        except:
            descricao = ''

        try:
            umidades = data['edtumidades']
        except:
            umidades = '0'

        try:
            calorias = data['edtcalorias']
        except:
            caloria = '0'

        try:
            joule = data['edtjoule']
        except:
            joule = '0'

        try:
            proteina = data['edtproteina']
        except:
            proteina = '0'

        try:
            lipidios = data['edtlipidios']
        except:
            lipidios = '0'

        try:
            colesterol = data['edtcolesterol']
        except:
            colesterol = '0'

        try:
            carboidrato = data['edtcarboidrato']
        except:
            carboidrato = '0'

        try:
            fibras = data['edtfibras']
        except:
            fibras = '0'

        try:
            cinzas = data['edtcinzas']
        except:
            cinzas = '0'

        try:
            calcio = data['edtcalcio']
        except:
            calcio = '0'

        try:
            magnesio = data['edtmagnesio']
        except:
            magnesio = '0'

        try:
            manganes = data['edtmanganes']
        except:
            manganes = '0'

        try:
            fosforo = data['edtfosforo']
        except:
            fosforo = '0'

        try:
            ferro = data['edtferro']
        except:
            ferro = '0'

        try:
            sodio = data['edtsodio']
        except:
            sodio = '0'

        try:
            potasio = data['edtpotasio']
        except:
            potasio = '0'

        try:
            cobre = data['edtcobre']
        except:
            cobre = '0'

        try:
            zinco = data['edtzinco']
        except:
            zinco = '0'

        try:
            retinol = data['edtretinol']
        except:
            retinol = '0'

        try:
            re = data['edtre']
        except:
            re = '0'
        try:
            rae = data['edtrae']
        except:
            rae = '0'

        try:
            tiamina = data['edttiamina ']
        except:
            tiamina = '0'

        try:
            riboflavina = data['edtriboflavina']
        except:
            riboflavina = '0'

        try:
            piridoxina = data['edtpiridoxina']
        except:
            piridoxina = '0'

        try:
            niacina = data['edtniacina']
        except:
            niacina = '0'

        try:
            vitaminac = data['edtvitaminac']
        except:
            vitaminac = '0'

        try:
            qtdgramasemcima = data['edtqtdnew']
        except:
            qtdgramasemcima = '0'

        try:
            idpessoa = data['edtidpessoa']
        except:
            idpessoa = ''

        try:
            idunmedidada = data['edtidunmedida']
        except:
            idpessoa = ''

        alimento = Alimentos(descricao, umidades, calorias, joule, proteina, lipidios, colesterol, carboidrato, fibras,
                     cinzas, calcio, magnesio, manganes, fosforo, ferro, sodio, potasio, cobre, zinco, retinol,re,
                     rae, tiamina, riboflavina, piridoxina, niacina, vitaminac, qtdgramasemcima,idpessoa,idunmedidada)
        try:
            db.session.add(alimento)
            db.session.commit()
            foodschema = FoodsSchema()
            result = foodschema.dump(alimento,many=True)
            return jsonify({'mensagem': 'Alimento registrado com sucesso', 'data': result,'result':True}), 201
        except:
            return jsonify({'message': 'Erro ao cadastrar alimento!', 'data': {},'result': False}), 500

def get_alimento_byid(idalimento):
    alimento = Alimentos.query.get(idalimento)
    try:
        return alimento
    except:
        return None

def get_alimento_bydesc():
    from datetime import datetime
    datenow = datetime.now()
    dia = datenow.day
    mes = datenow.month
    ano = datenow.year

    try:
        desc = request.args.get('descricao')
    except:
        desc = ''

    try:
        foodpeople = request.args.get('foodpeople')
    except:
        foodpeople = None



    totpage = request.args.get('totpage')
    if totpage == None or totpage == '':
        totpage = '10'

    orderby = request.args.get('orderby')
    if orderby == None or orderby == '':
        orderby = '0'

    try:
        page = request.args.get('page')
    except:
        page = ''
    if page == None:
        page = '1'



    if desc == None:
        desc = ''

    if totpage == '':
        totpage = '15'

    inputdesc = desc
    desc = "%"+desc+"%"
    idpessoa = None
    if current_user.is_authenticated:
        if foodpeople == 'S':
            idpessoa = current_user.pessoa.id

    if desc != '':
        from sqlalchemy import and_
        if orderby == '0':

            alimentopag = Alimentos.query.order_by(Alimentos.descricao.asc()). \
                filter(and_(Alimentos.descricao.like(desc),
                            Alimentos.idpessoa.is_(None) if idpessoa==None or idpessoa==''
                            else Alimentos.idpessoa==idpessoa)). \
                paginate(page=int(page),per_page=int(totpage), error_out=False)

        if orderby == '1':
            alimentopag = Alimentos.query.order_by(Alimentos.calorias.desc()). \
                filter(and_(Alimentos.descricao.like(desc), Alimentos.idpessoa.is_(None))). \
                paginate(page=int(page), max_per_page=int(totpage), error_out=False)

        if orderby == '2':
            alimentopag = Alimentos.query.order_by(Alimentos.carboidrato.desc()). \
                filter(and_(Alimentos.descricao.like(desc), Alimentos.idpessoa.is_(None))). \
                paginate(page=int(page), max_per_page=int(totpage), error_out=False)

        if orderby == '3':
            alimentopag = Alimentos.query.order_by(Alimentos.proteina.desc()). \
                filter(and_(Alimentos.descricao.like(desc), Alimentos.idpessoa.is_(None))). \
                paginate(page=int(page), max_per_page=int(totpage), error_out=False)

        if orderby == '4':
            alimentopag = Alimentos.query.order_by(Alimentos.lipidios.desc()). \
                filter(and_(Alimentos.descricao.like(desc), Alimentos.idpessoa.is_(None))). \
                paginate(page=int(page), max_per_page=int(totpage), error_out=False)

        if orderby == '5':
            alimentopag = Alimentos.query.order_by(Alimentos.fibras.desc()). \
                filter(and_(Alimentos.descricao.like(desc), Alimentos.idpessoa.is_(None))). \
                paginate(page=int(page), max_per_page=int(totpage), error_out=False)


        total = 0
        if alimentopag:
            total = alimentopag.total

            page, per_page, offset = get_page_args()

            per_page = totpage
            from current_app.funcs.getpagination import get_pagination
            pagination = get_pagination(
                page=page,
                per_page=per_page,
                total=total,

                record_name="alimentos",

            )

        #foodsschema = FoodsSchema(only=('id','descricao','carboidrato','proteina','lipidios','sodio','calorias','fibras','pessoa'))

    if alimentopag:
        foodsschema = FoodsSchema()
        tabfods = foodsschema.dump(alimentopag.items,many=True)
        #tabfoods = foodsschema.dump(alimentopag, many=True)
        return render_template('layouts/foods/mainfoods.html',
                               pagul=pagination,
                               result=True,
                               orderby=orderby,
                               tabfoods=tabfods,
                               inputdesc=inputdesc,
                               mensagem='Pesquisa Efetuada com Sucesso.',
                               dataatual=str(ano) + '-' + str(mes).zfill(2) + '-' + str(dia).zfill(2),
                               databr=str(dia).zfill(2) + '/' + str(mes).zfill(2) + '/' + str(ano))

        #return  jsonify({'result': True, 'mensagem':'Pesquisa Efetuada com Sucesso.','data':tabfoods, 'datapagination':returnPagination(alimentopag)})

    return jsonify({'result': False,  'data': {},'datapagination':{},'mensagem':'Nenhum item encontrado com a pesquisa fornecida'})
    #https://www.tutorialspoint.com/json/json_ajax_example.htm

def get_alimento_bydesc_json():

    try:
        desc = request.args.get('descricao')
    except:
        desc = ''

    try:
        idpessoa = request.args.get('idpessoa')
    except:
        idpessoa = '-1'

    totpage = request.args.get('totpage')
    if totpage == None or totpage == '':
        totpage = '10'


    try:
        page = request.args.get('page')
    except:
        page = ''
    if page == None:
        page = '1'



    if desc == None:
        desc = ''

    if totpage == '':
        totpage = '15'

    inputdesc = desc
    desc = "%"+desc+"%"

    if desc != '':
        from sqlalchemy import and_,or_
        alimentopag = Alimentos.query.order_by(Alimentos.descricao.asc()). \
                      filter(and_(Alimentos.descricao.like(desc),
                                  or_(Alimentos.idpessoa.is_(None),Alimentos.idpessoa==idpessoa))). \
                      paginate(page=int(page),per_page=int(totpage), error_out=False)
        total = 0
        if alimentopag:
            total = alimentopag.total

            page, per_page, offset = get_page_args()

            per_page = totpage
            from current_app.funcs.getpagination import get_pagination
            pagination = get_pagination(
                page=page,
                per_page=per_page,
                total=total,

                record_name="alimentos",

            )
    if alimentopag:
        foodsschema = FoodsSchema()
        tabfods = foodsschema.dump(alimentopag.items, many=True)
        # tabfoods = foodsschema.dump(alimentopag, many=True)
        return jsonify({'pagul': pagination.links, 'result': True, 'tabfoods': tabfods,
                        'inputdesc': inputdesc, 'mensagem': 'Pesquisa efetuada com sucesso!'})

    return jsonify({'pagul': {}, 'result': False, 'tabfoods': {},
                    'inputdesc': '', 'mensagem': 'Erro.'})


def get_tabalimentos():
    return get_alimento_bydesc()
    #res_json = result.json
    #dataalimentos = res_json['data']
    #datapagination = res_json['datapagination']
    #mensagem = res_json['mensagem']
    #orderby = orderby;
    #return render_template('layouts/foods/mainfoods.html',
    #                       datapagination=datapagination,
    #                       result=result,
    #                       orderby=orderby,
    #                       tabfoods=dataalimentos,
    #                       mensagem=mensagem)

