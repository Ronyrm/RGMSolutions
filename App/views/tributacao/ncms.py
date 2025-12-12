from App import db
from App.model.tributacao.ncms import NCMS,SchemaNCMS
from flask import request,render_template,current_app
from werkzeug.utils import secure_filename
import os

def get_ncms_json(desc='',page=1,per_page=100):

    #captura tipo do filtro escolhido: por descricao, codigo, ou codigo que inicia com
    tpfiltro = request.args.get("select-tpfiltro") if request.args.get("select-tpfiltro") != None else '0'
    #captura o grau escolhido.
    grau = request.args.get("select-grau") if request.args.get("select-grau") != None else '0'

    from sqlalchemy import case, text, func,or_
    try:
        grau_max = db.session.query(func.Max(NCMS.grau)).scalar()
        print(grau_max)

        case_descricao = \
            case([
                (text('ncms.grau=1'), NCMS.descricao),
                (text('ncms.grau=2'), func.concat('   ', NCMS.descricao)),
                (text('ncms.grau=3'), func.concat('      ', NCMS.descricao)),
                (text('ncms.grau=4'), func.concat('         ', NCMS.descricao)),
                (text('ncms.grau=5'), func.concat('            ', NCMS.descricao)),
                (text('ncms.grau=6'), func.concat('               ', NCMS.descricao)),
            ], else_='').label('descricao')

        unidade = func.IF(NCMS.unidade!=None,NCMS.unidade,'').label('unidade')

        filtergrau = NCMS.grau != -1 if grau == '0' else NCMS.grau == grau

        if tpfiltro == '0':
            iffilter = NCMS.descricao.like("%" + desc + "%")
        elif tpfiltro == '1':
            iffilter = or_(NCMS.codigo == desc, NCMS.codncm == desc)
        elif tpfiltro == '2':
            iffilter = or_(NCMS.codigo.like(desc+"%"), NCMS.codncm.like(desc+"%"))


        tab_ncms = NCMS.query. \
            with_entities(NCMS.codncm, case_descricao, NCMS.grau, unidade). \
            filter(iffilter). \
            filter(filtergrau). \
            order_by(NCMS.grau1, NCMS.grau2, NCMS.grau3, NCMS.grau4).\
            paginate(page=page,per_page=per_page, error_out=False)

        if tab_ncms:
            from flask_paginate import get_page_args
            page, per_page, offset = get_page_args()

            from App.funcs.getpagination import get_pagination
            pagination = get_pagination(
                page=page,
                per_page=per_page,
                total=tab_ncms.total,
                record_name="ncms"
            )
            import simplejson
            # transforma lista em stringjson
            result = simplejson.dumps(tab_ncms.items)
            # transforma string em json
            resultjson = simplejson.loads(result)

            pages = {}
            if type(pagination.pages) is list:
                 pages = pagination.pages
            elif type(pagination.pages) is range:
                for num in pagination.pages:
                    pages.update({num:num})



            return {'ncms':resultjson,
                    'pagination':{
                        'links':pagination.links,
                        'page':pagination.page,
                        'per_page':pagination.per_page,
                        'info':pagination.info,
                        'pages':pages,
                        'total_pages':pagination.total_pages,
                        'total':pagination.total},
                    'result':True,
                    'mensagem':'Sucesso',
                    'tpfiltro':tpfiltro,
                    'grau':grau,
                    'desc':desc}
    except:
        pass
    return {'ncms':[],'pagination': [],'result':False,'mensagem':'Erro ao abrir tabela de NCMS',
            'tpfiltro':'0','grau':'0','desc':''}

def get_ncms_main(desc='',page=1,per_page=100):

    #captura tipo do filtro escolhido: por descricao, codigo, ou codigo que inicia com
    tpfiltro = request.args.get("select-tpfiltro") if request.args.get("select-tpfiltro") != None else '0'
    #captura o grau escolhido.
    grau = request.args.get("select-grau") if request.args.get("select-grau") != None else '0'

    from sqlalchemy import case, text, func,or_
    try:
        grau_max = db.session.query(func.Max(NCMS.grau)).scalar()
        print(grau_max)

        case_descricao = \
            case([
                (text('ncms.grau=1'), NCMS.descricao),
                (text('ncms.grau=2'), func.concat('   ', NCMS.descricao)),
                (text('ncms.grau=3'), func.concat('      ', NCMS.descricao)),
                (text('ncms.grau=4'), func.concat('         ', NCMS.descricao)),
                (text('ncms.grau=5'), func.concat('            ', NCMS.descricao)),
                (text('ncms.grau=6'), func.concat('               ', NCMS.descricao)),
            ], else_='').label('descricao')
        unidade = func.IF(NCMS.unidade!=None,NCMS.unidade,'').label('unidade')


        filtergrau = NCMS.grau != -1 if grau == '0' else NCMS.grau == grau

        if tpfiltro == '0':
            iffilter = NCMS.descricao.like("%" + desc + "%")
        elif tpfiltro == '1':
            iffilter = or_(NCMS.codigo == desc, NCMS.codncm == desc)
        elif tpfiltro == '2':
            iffilter = or_(NCMS.codigo.like(desc+"%"), NCMS.codncm.like(desc+"%"))


        tab_ncms = NCMS.query. \
            with_entities(NCMS.codncm, case_descricao, NCMS.grau, unidade). \
            filter(iffilter). \
            filter(filtergrau). \
            order_by(NCMS.grau1, NCMS.grau2, NCMS.grau3, NCMS.grau4).\
            paginate(page=page,per_page=per_page, error_out=False)

        if tab_ncms:
            from flask_paginate import get_page_args
            page, per_page, offset = get_page_args()

            from App.funcs.getpagination import get_pagination
            pagination = get_pagination(
                page=page,
                per_page=per_page,
                total=tab_ncms.total,
                record_name="ncms"
            )
            import simplejson
            # transforma lista em stringjson
            result = simplejson.dumps(tab_ncms.items)
            # transforma string em json
            resultjson = simplejson.loads(result)

            return render_template('layouts/tributacao/ncms/main.html',
                                   ncms=resultjson,
                                   pagination = pagination,
                                   result=True,
                                   mensagem='Sucesso',
                                   tpfiltro=tpfiltro,
                                   grau=grau,
                                   desc=desc)
    except:
        pass
    return render_template('layouts/products/ncms/main.html',
                            ncms=[],
                            pagination = [],
                            result=False,
                            mensagem='Erro ao abrir tabela de NCMS',
                            tpfiltro='0',
                            grau='0',
                            desc=''
                            )

def insert_into_sql():
    if request.method == 'POST':
        if 'file_sql' in request.files:
            file_sql = request.files['file_sql']
            #file_sql = file_sql.split('\n')

        if file_sql:
            try:
                filename = secure_filename(file_sql.filename)
                localesave = current_app.config['UPLOAD_FOLDER']

                spath = os.path.join(localesave, filename)

                if os.path.exists(spath):
                    os.remove(spath)

                file_sql.save(spath)
            except:
                return {'mensagem':f'Erro ao tentar salvar o arquivo {filename} no servidor',
                        'result':False,
                        'data':{}}

            tabncms = NCMS.query.all()

            if not tabncms:
                try:
                    from App.funcs.migrate_sql import insert_data_script_sql
                    insert_data_script_sql(spath)
                    os.remove(spath)
                except:
                    return {'mensagem': f'Erro ao inserir sql no banco de dados',
                            'result': True,
                            'data':{}}

                db.session.commit()
                tabncms = NCMS.query.all()
                schemancms = SchemaNCMS()

                return {'mensagem': f'Dados Inseridos com sucesso',
                        'result': True,
                        'data': schemancms.dump(tabncms,many=True)}