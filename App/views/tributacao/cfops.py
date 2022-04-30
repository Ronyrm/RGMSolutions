from App import app,db
from flask import request
from App.model.tributacao.cfops import CFOPs,SchemaCFOPs
from flask_paginate import get_page_args
from App.funcs.getpagination import get_pagination
from werkzeug.utils import secure_filename
import os


def get_CFOPs():
    try:
        if request.method == 'GET':
            desc = request.args.get('desc') if request.args.get('desc') != None else ''
            page = request.args.get('page') if request.args.get('page') != None else '1'
            per_page = request.args.get('per_page') if request.args.get('per_page') != None else '50'
            filtercests = ''


            cfops = CFOPs.query. \
                filter(CFOPs.descricao.like('%' + desc + '%')). \
                paginate(page=int(page), per_page=int(per_page), error_out=False)
            if cfops:
                page, per_page, offset = get_page_args()
                pagination = get_pagination(
                    page=page,
                    per_page=per_page,
                    total=cfops.total,
                    record_name="cests"
                )

                pages = {}
                if type(pagination.pages) is list:
                    pages = pagination.pages
                elif type(pagination.pages) is range:
                    for num in pagination.pages:
                        pages.update({num: num})

                schemacests = SchemaCFOPs()
                tabcfops = schemacests.dump(cfops.items, many=True)
                return {'cfops': tabcfops,
                        'pagination': {
                            'links': pagination.links,
                            'page': pagination.page,
                            'per_page': pagination.per_page,
                            'info': pagination.info,
                            'pages': pages,
                            'total_pages': pagination.total_pages,
                            'total': pagination.total},
                        'result': True,
                        'mensagem': 'Sucesso',
                        'desc': desc}

    except:
        pass
        return {'cfops': [], 'pagination': [], 'result': False,
                'mensagem': 'Erro ao abrir tabela de CFOPS', 'desc': ''}

def insert_into_sql():

    if request.method == 'POST':
        if 'file_sql' in request.files:
            file_sql = request.files['file_sql']
            #file_sql = file_sql.split('\n')

        if file_sql:
            try:
                filename = secure_filename(file_sql.filename)
                localesave = app.config['UPLOAD_FOLDER']

                spath = os.path.join(localesave, filename)

                if os.path.exists(spath):
                    os.remove(spath)

                file_sql.save(spath)
            except:
                return {'mensagem':f'Erro ao tentar salvar o arquivo {filename} no servidor',
                        'result':False,
                        'data':{}}

            tb = CFOPs.query.all()
            if not tb:
                try:
                    from App.funcs.migrate_sql import insert_data_script_sql
                    insert_data_script_sql(spath)
                    os.remove(spath)
                except:
                    return {'mensagem': f'Erro ao inserir sql no banco de dados',
                            'result': True,
                            'data':{}}

                db.session.commit()
                tb = CFOPs.query.all()

                schemacfops = SchemaCFOPs()

                return {'mensagem': f'Dados Inseridos com sucesso',
                        'result': True,
                        'data': schemacfops.dump(tb,many=True)}